from __future__ import annotations

import copy

from jeb.batch import import_response, prepare, validate_response
from jeb.core import JebError, digest, read_json, write_json
from jeb.export import export, reader
from jeb.knowledge import validate_knowledge
from jeb.review import all_decisions, heads, report
from jeb.search import build_index, search
from tests.support import WorkspaceTest


class BatchTests(WorkspaceTest):
    def test_packet_is_self_contained_bounded_and_non_approving(self):
        packet = prepare(self.project, self.source_id, "test-batch", "fixture", "modernize")
        self.assertIn("EDITORIAL", packet["policy"].upper())
        self.assertIn("needs_review", str(packet["output_schema"]))
        self.assertEqual(packet["coverage_manifest"], [s["segment_id"] for s in packet["segments"]])
        self.assertTrue(all(s["book_id"] == "GEN" for s in packet["segments"]))

    def test_pilot_cannot_be_filled_from_memory(self):
        for selection in ("GEN", "MAT", "MRK", "LUK", "JHN"):
            with (
                self.subTest(selection=selection),
                self.assertRaisesRegex(JebError, "missing/ambiguous"),
            ):
                prepare(self.project, self.source_id, f"pilot-{selection}", selection, "modernize")

    def test_modernization_endpoint_refuses_other_packet_protocols(self):
        for task in ("research", "annotate", "review"):
            with self.subTest(task=task), self.assertRaisesRegex(JebError, "Only modernization"):
                prepare(self.project, self.source_id, f"task-{task}", "fixture", task)

    def test_scope_duplicates_missing_and_invented_references_rejected(self):
        original = self.response()
        variants = []
        missing = copy.deepcopy(original)
        missing["items"].pop()
        variants.append(missing)
        duplicate = copy.deepcopy(original)
        duplicate["items"][1] = duplicate["items"][0]
        variants.append(duplicate)
        invented = copy.deepcopy(original)
        invented["items"][0]["segment_id"] = "fake:GEN.1.1"
        variants.append(invented)
        outside = copy.deepcopy(original)
        outside["items"][0]["segment_id"] = "synthetic-v1:PSA.1.1"
        variants.append(outside)
        reordered = copy.deepcopy(original)
        reordered["items"].reverse()
        variants.append(reordered)
        for index, response in enumerate(variants):
            with self.subTest(index=index), self.assertRaisesRegex(JebError, "response IDs"):
                validate_response(self.project, response)

    def test_strict_schema_and_fabricated_evidence_rejected(self):
        response = self.response()
        response["unapproved_extra"] = True
        with self.assertRaisesRegex(JebError, "schema"):
            validate_response(self.project, response)
        response.pop("unapproved_extra")
        response["items"][0]["evidence_ids"] = ["imagined-paper"]
        with self.assertRaisesRegex(JebError, "evidence reference"):
            validate_response(self.project, response)

    def test_unapproved_original_name_mapping_rejected(self):
        response = self.response()
        response["items"][0]["name_mapping_ids"] = ["unapproved-native-name"]
        with self.assertRaisesRegex(JebError, "name mapping"):
            validate_response(self.project, response)

    def test_policy_and_packet_hash_staleness(self):
        response = self.response()
        policy = self.project.path("docs/EDITORIAL_POLICY.md")
        policy.write_bytes(policy.read_bytes() + b"\nPolicy changed.\n")
        with self.assertRaisesRegex(JebError, "Stale policy"):
            validate_response(self.project, response)

    def test_edited_packet_is_rejected(self):
        response = self.response()
        path = self.project.path("data/batches/test-batch/input.json")
        packet = read_json(path)
        packet["segments"][0]["normalized_text"] += " invented"
        write_json(path, packet)
        with self.assertRaisesRegex(JebError, "edited"):
            validate_response(self.project, response)

    def test_import_is_proposal_only_and_duplicates_rejected(self):
        response = self.response()
        proposal = self.import_test_response(response)
        self.assertEqual(proposal["review_state"], "proposed")
        self.assertEqual(all_decisions(self.project), {})
        with self.assertRaisesRegex(JebError, "Duplicate response"):
            import_response(self.project, self.project.path("returned.json"))

    def test_automatic_flags_do_not_approve_or_silently_correct(self):
        response = self.response()
        item = response["items"][0]
        item.update(
            action="propose",
            proposed_text=item["proposed_text"].replace("covik ne", "čovjek").replace("2", "3"),
            change_class="C",
        )
        _, items = validate_response(self.project, response)
        self.assertEqual(
            set(items[0]["flags"]),
            {"linguistic", "negation_changed", "number_changed", "protected_form_changed"},
        )
        self.assertIn("čovjek", items[0]["proposed_text"])

    def test_no_change_and_needs_review_contracts(self):
        response = self.response()
        response["items"][0]["proposed_text"] += " altered"
        with self.assertRaisesRegex(JebError, "no_change"):
            validate_response(self.project, response)
        response["items"][0].update(action="needs_review", proposed_text=None, change_class="D")
        _, items = validate_response(self.project, response)
        self.assertIn("meaning_sensitive", items[0]["flags"])


class ReviewAndExportTests(WorkspaceTest):
    def test_preview_exports_source_and_never_unapproved_modernization(self):
        response = self.response()
        response["items"][0].update(
            action="propose",
            change_class="C",
            proposed_text="Probni zamjenski tekst, bez odobrenja.",
        )
        self.import_test_response(response)
        artifact = reader(self.project, self.source_id, "preview")
        self.assertNotIn("Probni zamjenski tekst", str(artifact))
        self.assertTrue(
            all(s["editorial_status"] == "source_only" for s in artifact["books"][0]["segments"])
        )
        self.assertFalse(artifact["collection_complete"])
        self.assertEqual(len(artifact["coverage"]), 5)
        self.assertEqual(artifact["coverage"][1]["source_segments"], 0)

    def test_text_approval_is_bound_and_unchanged_text_is_labelled(self):
        proposal = self.import_test_response()
        self.apply_test_decisions([self.decision(proposal)])
        segment = reader(self.project, self.source_id, "preview")["books"][0]["segments"][0]
        self.assertEqual(segment["editorial_status"], "approved_unchanged")
        self.assertEqual(segment["decision_id"], "test-decision")

    def test_wrong_text_hash_and_nonhuman_decision_rejected(self):
        proposal = self.import_test_response()
        decision = self.decision(proposal)
        decision["text_sha256"] = "0" * 64
        with self.assertRaisesRegex(JebError, "exact text hash"):
            self.apply_test_decisions([decision])
        decision = self.decision(proposal)
        decision["human_attestation"] = False
        with self.assertRaises(JebError):
            self.apply_test_decisions([decision])

    def test_flagged_issues_need_individual_resolution(self):
        response = self.response()
        response["items"][0].update(
            action="propose", change_class="C", proposed_text="Probni drugi tekst."
        )
        proposal = self.import_test_response(response)
        decision = self.decision(proposal)
        decision["resolutions"] = []
        with self.assertRaisesRegex(JebError, "flagged issue"):
            self.apply_test_decisions([decision])

    def test_meaning_sensitive_approval_stays_blocked(self):
        response = self.response()
        response["items"][0]["change_class"] = "D"
        proposal = self.import_test_response(response)
        with self.assertRaisesRegex(JebError, "Meaning-sensitive"):
            self.apply_test_decisions([self.decision(proposal)])

    def test_edit_after_approval_invalidates_export(self):
        proposal = self.import_test_response()
        self.apply_test_decisions([self.decision(proposal)])
        path = self.project.path(f"data/proposals/{proposal['proposal_id']}.json")
        proposal["items"][0]["proposed_text"] += " changed"
        write_json(path, proposal)
        with self.assertRaisesRegex(JebError, "changed or is stale"):
            reader(self.project, self.source_id, "preview")

    def test_conflicting_approval_requires_explicit_supersession(self):
        proposal = self.import_test_response()
        first = self.decision(proposal)
        self.apply_test_decisions([first])
        second = self.decision(proposal, decision_id="replacement")
        second["state"] = "rejected"
        with self.assertRaisesRegex(JebError, "Conflicting"):
            self.apply_test_decisions([second])
        second["supersedes"] = first["decision_id"]
        self.apply_test_decisions([second])
        self.assertEqual(len(all_decisions(self.project)), 2)
        self.assertEqual(list(heads(all_decisions(self.project)).values())[0]["state"], "rejected")

    def test_policy_change_invalidates_approval_but_can_be_superseded(self):
        first = self.import_test_response()
        decision = self.decision(first)
        self.apply_test_decisions([decision])
        policy = self.project.path("docs/EDITORIAL_POLICY.md")
        policy.write_bytes(policy.read_bytes() + b"\nReviewed new policy.\n")
        with self.assertRaisesRegex(JebError, "Stale policy"):
            reader(self.project, self.source_id, "preview")
        new = self.import_test_response(self.response(batch_id="new-policy-batch"))
        replacement = self.decision(new, decision_id="new-policy-decision")
        replacement["supersedes"] = decision["decision_id"]
        self.apply_test_decisions([replacement])
        self.assertEqual(
            reader(self.project, self.source_id, "preview")["coverage"][0]["approved_segments"], 1
        )

    def test_synthetic_release_forbidden(self):
        with self.assertRaisesRegex(JebError, "Synthetic fixtures"):
            reader(self.project, self.source_id, "release")

    def test_exports_reproduce_identical_bytes(self):
        first = export(
            self.project, self.source_id, "preview", "json", "exports/a.json", "five-book"
        )
        second = export(
            self.project, self.source_id, "preview", "json", "exports/b.json", "five-book"
        )
        self.assertEqual(first["sha256"], second["sha256"])
        self.assertEqual(
            self.project.path("exports/a.json").read_bytes(),
            self.project.path("exports/b.json").read_bytes(),
        )
        self.assertNotIn("timestamp", self.project.path("exports/a.json").read_text("utf-8"))

    def test_markdown_preserves_typed_source_notes_and_layout(self):
        export(
            self.project, self.source_id, "preview", "markdown", "exports/reader.md", "five-book"
        )
        text = self.project.path("exports/reader.md").read_text("utf-8")
        self.assertIn('"source_annotations"', text)
        self.assertIn('"poetry"', text)
        self.assertIn("NOT biblical text", text)

    def test_review_report_has_source_diff_hash_and_no_fabricated_reviewer(self):
        proposal = self.import_test_response()
        report(self.project, proposal["proposal_id"], "reports/review.md")
        text = self.project.path("reports/review.md").read_text("utf-8")
        self.assertIn("Source:", text)
        self.assertIn("Diff", text)
        self.assertIn(digest(proposal), text)
        self.assertIn("unreviewed", text)

    def test_sqlite_rebuild_search_and_outside_book_rejection(self):
        build_index(self.project, self.source_id)
        matches = search(self.project, "covik", self.source_id)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["book_id"], "GEN")
        self.assertEqual(search(self.project, "' OR 1=1 --", self.source_id), [])
        write_json(self.project.path(f"data/normalized/{self.source_id}/PSA.json"), {})
        with self.assertRaises(JebError):
            build_index(self.project, self.source_id)

    def test_index_is_stale_after_review_changes(self):
        build_index(self.project, self.source_id)
        proposal = self.import_test_response()
        self.apply_test_decisions([self.decision(proposal)])
        with self.assertRaisesRegex(JebError, "Stale index"):
            search(self.project, "covik", self.source_id)


class KnowledgeTests(WorkspaceTest):
    def test_personal_reflection_and_creative_drafts_stay_separate(self):
        reflection = self.knowledge_record()
        creative = self.knowledge_record("test-creative")
        creative.update(layer="creative_adaptation", evidence_category="creative_adaptation")
        self.write_knowledge(reflection, creative)
        records = validate_knowledge(self.project, self.books())
        self.assertEqual(records[reflection["record_id"]]["layer"], "personal_reflection")
        self.assertEqual(
            reader(self.project, self.source_id, "preview")["annotation_coverage"][
                "pending_or_stale"
            ],
            2,
        )

    def test_dangling_evidence_claim_and_segment_links_fail(self):
        for field, value in (
            ("claim_ids", ["unknown-claim"]),
            ("evidence_ids", ["unknown-evidence"]),
            ("segment_ids", ["fake:GEN.1.1"]),
        ):
            record = self.knowledge_record()
            record[field] = value
            self.write_knowledge(record)
            with self.subTest(field=field), self.assertRaises(JebError):
                validate_knowledge(self.project, self.books())

    def test_historical_claim_requires_evidence(self):
        record = self.knowledge_record()
        record.update(
            record_type="claim", layer="historical", evidence_category="secondary_scholarship"
        )
        self.write_knowledge(record)
        with self.assertRaisesRegex(JebError, "inspectable evidence"):
            validate_knowledge(self.project, self.books())

    def test_evidence_needs_registered_source_and_exact_locator(self):
        record = self.knowledge_record()
        record.update(
            record_type="evidence",
            layer="source_witness",
            evidence_category="primary_witness",
            source_id=self.source_id,
            url="urn:jeb:synthetic:fixture-v1",
        )
        self.write_knowledge(record)
        with self.assertRaisesRegex(JebError, "exact locator"):
            validate_knowledge(self.project, self.books())

    def test_non_latin_authored_metadata_rejected(self):
        record = self.knowledge_record()
        record["text"] = "\u041evo nije Latin script."
        self.write_knowledge(record)
        with self.assertRaisesRegex(JebError, "display-script"):
            validate_knowledge(self.project, self.books())

    def test_text_change_invalidates_dependent_annotation_without_changing_approval(self):
        record = self.approve_test_knowledge(self.knowledge_record())
        self.write_knowledge(record)
        self.assertEqual(
            reader(self.project, self.source_id, "preview")["annotation_coverage"][
                "approved_current"
            ],
            1,
        )
        response = self.response()
        response["items"][0].update(
            action="propose",
            change_class="C",
            proposed_text=response["items"][0]["proposed_text"].replace("mijenja", "prepravlja"),
        )
        proposal = self.import_test_response(response)
        self.apply_test_decisions([self.decision(proposal)])
        artifact = reader(self.project, self.source_id, "preview")
        self.assertEqual(artifact["coverage"][0]["approved_segments"], 1)
        self.assertEqual(artifact["annotation_coverage"]["approved_current"], 0)
        self.assertEqual(artifact["annotation_coverage"]["pending_or_stale"], 1)

    def test_editing_note_does_not_change_approved_scripture(self):
        proposal = self.import_test_response()
        self.apply_test_decisions([self.decision(proposal)])
        before = reader(self.project, self.source_id, "preview")["books"]
        record = self.knowledge_record()
        record["text"] += " New draft question."
        self.write_knowledge(record)
        self.assertEqual(reader(self.project, self.source_id, "preview")["books"], before)

    def test_metadata_approval_hash_checked(self):
        record = self.approve_test_knowledge(self.knowledge_record())
        record["text"] += " Changed after review."
        self.write_knowledge(record)
        with self.assertRaisesRegex(JebError, "edited after approval"):
            validate_knowledge(self.project, self.books())

    def test_stale_supporting_record_invalidates_current_annotation_transitively(self):
        supporting = self.knowledge_record("supporting-record")
        first_segment = supporting["segment_ids"][0]
        supporting["depends_on"][first_segment] = "0" * 64
        supporting = self.approve_test_knowledge(supporting)
        note = self.knowledge_record("dependent-note")
        note["related_ids"] = [supporting["record_id"]]
        note = self.approve_test_knowledge(note)
        self.write_knowledge(supporting, note)
        artifact = reader(self.project, self.source_id, "preview")
        self.assertEqual(artifact["knowledge"], [])
        self.assertEqual(artifact["annotation_coverage"]["pending_or_stale"], 2)
