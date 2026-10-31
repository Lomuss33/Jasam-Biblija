from __future__ import annotations

import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from jeb.core import (
    JebError,
    Project,
    canonical,
    digest,
    native_path,
    read_bytes,
    read_yaml,
    write_json,
)
from jeb.export import export, reader
from jeb.knowledge import validate_knowledge
from jeb.knowledge_packets import import_response, prepare, validate_response
from jeb.knowledge_review import (
    APPROVAL_CHECKS,
    MAX_DECISIONS,
    apply,
    read_decisions,
    read_receipts,
    report,
    review_heads,
    validate_decisions,
)
from jeb.review import all_decisions
from tests.support import WorkspaceTest


class KnowledgeReviewTests(WorkspaceTest):
    def annotation_response(self, records=None, packet_id="review-notes"):
        packet = prepare(self.project, self.source_id, "fixture", "annotate", packet_id)
        records = records if records is not None else [self.knowledge_record("reflection")]
        response = {
            "schema_version": "1.0",
            "packet_id": packet_id,
            "packet_sha256": packet["packet_sha256"],
            "source_id": self.source_id,
            "task": "annotate",
            "tool": {
                "name": "Synthetic automated drafting fixture; no actual human",
                "model_identifier": None,
                "reported_at": "2026-10-30",
            },
            "limitations": ["Invented technical records, not scholarship or scripture."],
            "review_state": "unreviewed",
            "approval_authority": "none",
            "human_attestation": False,
            "drafts": [
                {
                    "record": r,
                    "attribution": {
                        "kind": "ai_assisted_draft",
                        "credit": "Synthetic AI-assisted fixture; not the owner voice",
                    },
                    "rationale": "Synthetic draft only",
                }
                for r in records
            ],
            "items": [],
        }
        for segment in packet["segments"]:
            key = segment["display"]["segment_id"]
            ids = [r["record_id"] for r in records if key in r["segment_ids"]]
            response["items"].append(
                {
                    "segment_id": key,
                    "text_sha256": segment["display"]["text_sha256"],
                    "action": "drafts_proposed" if ids else "no_draft",
                    "record_ids": ids,
                    "rationale": "Synthetic coverage fixture",
                }
            )
        return response

    def evidence(self, key="evidence"):
        record = self.knowledge_record(key)
        record.update(
            record_type="evidence",
            layer="source_witness",
            evidence_category="primary_witness",
            source_id=self.source_id,
            bibliographic_details="Original synthetic fixture",
            url="urn:jeb:synthetic:fixture-v1",
            locator="First invented technical sentence",
            access_date="2026-10-30",
        )
        return record

    def graph(self):
        evidence = self.evidence()
        claim = self.knowledge_record("claim")
        claim.update(
            record_type="claim",
            layer="literary",
            evidence_category="editorial_inference",
            evidence_ids=["evidence"],
        )
        note = self.knowledge_record("note")
        note.update(
            layer="literary",
            evidence_category="editorial_inference",
            evidence_ids=["evidence"],
            claim_ids=["claim"],
        )
        return [evidence, claim, note]

    def stage(self, response):
        path = self.project.path("returned-annotation.json")
        write_json(path, response)
        return import_response(self.project, path)

    def decisions(self, response, state="approved", review_id="synthetic-review", selected=None):
        return {
            "schema_version": "1.0",
            "review_id": review_id,
            "packet_id": response["packet_id"],
            "packet_sha256": response["packet_sha256"],
            "response_sha256": digest(response),
            "policy_sha256": self.project.policy_hash(),
            "reviewer_id": "SYNTHETIC-TEST-OWNER; simulated attestation inside temporary test only",
            "reviewer_role": "owner",
            "human_attestation": True,
            "reviewed_at": "2026-10-30",
            "items": [
                {
                    "record_id": d["record"]["record_id"],
                    "draft_sha256": digest(d),
                    "state": state,
                    "rationale": "Simulated review for a temporary software test; no actual owner participation",
                    "checks": sorted(APPROVAL_CHECKS) if state == "approved" else [],
                    "supersedes": None,
                }
                for d in response["drafts"]
                if selected is None or d["record"]["record_id"] in selected
            ],
        }

    def apply_value(self, value):
        path = self.project.path("synthetic-human-decisions.json")
        write_json(path, value)
        return apply(self.project, path)

    def test_unsigned_report_retains_bindings_attribution_and_zero_authority(self):
        response = self.annotation_response()
        self.stage(response)
        before = canonical(reader(self.project, self.source_id, "preview"))
        result = report(
            self.project, response["packet_id"], digest(response), "reports/human-notes.md"
        )
        text = read_bytes(self.project.path(result["output"])).decode("utf-8")
        for value in (
            digest(response),
            digest(response["drafts"][0]),
            "unsigned",
            "unreviewed",
            "ai_assisted_draft",
            "not the owner voice",
            "reflection",
        ):
            self.assertIn(value, text)
        self.assertEqual(result["approvals_created"], 0)
        self.assertEqual(read_receipts(self.project), {})
        self.assertEqual(all_decisions(self.project), {})
        self.assertEqual(before, canonical(reader(self.project, self.source_id, "preview")))

    def test_only_imported_annotation_responses_are_reviewable(self):
        response = self.annotation_response()
        with self.assertRaisesRegex(JebError, "Import the annotation"):
            validate_decisions(self.project, self.decisions(response))
        packet = prepare(self.project, self.source_id, "fixture", "research", "research-only")
        with self.assertRaisesRegex(JebError, "SHA-256"):
            report(self.project, packet["packet_id"], "../bad", "reports/x.md")
        # A structurally valid research envelope is still outside the human annotation interface.
        research = {
            k: copy.deepcopy(v) for k, v in response.items() if k not in ("drafts", "items")
        }
        research.update(
            packet_id=packet["packet_id"],
            packet_sha256=packet["packet_sha256"],
            task="research",
            leads=[],
        )
        research["items"] = [
            {
                "segment_id": row["display"]["segment_id"],
                "text_sha256": row["display"]["text_sha256"],
                "outcome": "no_new_evidence",
                "summary": "Synthetic research fixture",
                "known_evidence_ids": [],
                "lead_ids": [],
                "questions": ["Which evidence is still missing?"],
                "uncertainty": "No real finding",
            }
            for row in packet["segments"]
        ]
        self.stage(research)
        with self.assertRaisesRegex(JebError, "Only staged annotation"):
            report(self.project, packet["packet_id"], digest(research), "reports/x.md")

    def test_approval_projects_closed_graph_with_full_provenance_and_unchanged_text(self):
        response = self.annotation_response(self.graph())
        self.stage(response)
        before = reader(self.project, self.source_id, "preview")
        value = self.decisions(response)
        validated = validate_decisions(self.project, value)
        self.assertEqual(read_receipts(self.project), {})
        result = self.apply_value(value)
        self.assertEqual(result["promoted"], 3)
        self.assertEqual(len(read_receipts(self.project)), 1)
        self.assertEqual(validated, next(iter(read_receipts(self.project).values())))
        records = validate_knowledge(self.project, self.books())
        self.assertEqual(set(records), {"evidence", "claim", "note"})
        artifact = reader(self.project, self.source_id, "preview")
        self.assertEqual(len(artifact["knowledge"]), 3)
        self.assertEqual(artifact["books"], before["books"])
        self.assertEqual(artifact["coverage"], before["coverage"])
        self.assertEqual(all_decisions(self.project), {})
        for record, draft in zip(
            records.values(),
            sorted(response["drafts"], key=lambda d: d["record"]["record_id"]),
            strict=True,
        ):
            self.assertEqual(record["provenance"]["draft_sha256"], digest(draft))
            self.assertEqual(record["provenance"]["attribution"], draft["attribution"])
            self.assertEqual(record["provenance"]["tool"], response["tool"])
            for key in draft["record"]:
                if key not in ("approval", "review_state"):
                    self.assertEqual(record[key], draft["record"][key])
        export(self.project, self.source_id, "preview", "markdown", "exports/notes.md", "five-book")
        self.assertIn("ai_assisted_draft", self.project.path("exports/notes.md").read_text("utf-8"))
        with self.assertRaisesRegex(JebError, "Synthetic"):
            reader(self.project, self.source_id, "release")

    def test_partial_closed_promotion_can_resume_the_same_original_response(self):
        response = self.annotation_response(self.graph())
        self.stage(response)
        value = self.decisions(response, selected={"claim", "note"})
        with self.assertRaisesRegex(JebError, "dependency closure"):
            self.apply_value(value)
        self.assertEqual(read_receipts(self.project), {})
        self.apply_value(self.decisions(response, selected={"evidence"}, review_id="first"))
        report(self.project, response["packet_id"], digest(response), "reports/partial.md")
        self.apply_value(self.decisions(response, selected={"claim", "note"}, review_id="second"))
        self.assertEqual(len(reader(self.project, self.source_id, "preview")["knowledge"]), 3)
        with self.assertRaisesRegex(JebError, "Stale|collides"):
            validate_response(self.project, response)

    def test_rejected_and_pending_records_do_not_enter_bank_or_reader(self):
        response = self.annotation_response(self.graph())
        self.stage(response)
        before = canonical(reader(self.project, self.source_id, "preview"))
        value = self.decisions(response, state="needs_review")
        value["items"][0]["state"] = "rejected"
        result = self.apply_value(value)
        self.assertEqual(result["promoted"], 0)
        self.assertEqual(validate_knowledge(self.project, self.books()), {})
        self.assertEqual(before, canonical(reader(self.project, self.source_id, "preview")))
        self.assertEqual(len(review_heads(read_receipts(self.project))), 3)

    def test_owner_attestation_checks_dates_and_scope_are_required(self):
        response = self.annotation_response()
        self.stage(response)
        original = self.decisions(response)
        changes = [
            ("human_attestation", False),
            ("reviewer_role", "ai"),
            ("review_id", "../bad"),
            ("packet_sha256", "0" * 64),
            ("response_sha256", "0" * 64),
            ("policy_sha256", "0" * 64),
            ("reviewed_at", "2026-10-29"),
        ]
        for field, changed in changes:
            value = copy.deepcopy(original)
            value[field] = changed
            with self.subTest(field=field), self.assertRaises(JebError):
                validate_decisions(self.project, value)
        for fields in (
            {"draft_sha256": "0" * 64},
            {"record_id": "invented"},
            {"checks": []},
            {"state": "verified_history"},
        ):
            value = copy.deepcopy(original)
            value["items"][0].update(fields)
            with self.subTest(fields=fields), self.assertRaises(JebError):
                validate_decisions(self.project, value)
        value = copy.deepcopy(original)
        value["items"].append(copy.deepcopy(value["items"][0]))
        with self.assertRaisesRegex(JebError, "Duplicate"):
            validate_decisions(self.project, value)
        self.assertEqual(read_receipts(self.project), {})

    def test_stale_policy_or_changed_source_context_blocks_every_decision_state(self):
        response = self.annotation_response()
        self.stage(response)
        value = self.decisions(response, state="rejected")
        policy = self.project.path("docs/EDITORIAL_POLICY.md")
        policy.write_bytes(policy.read_bytes() + b"\nChanged synthetic test policy\n")
        with self.assertRaisesRegex(JebError, "Stale"):
            self.apply_value(value)
        self.assertEqual(read_receipts(self.project), {})

    def test_competing_responses_need_explicit_pending_head_supersession(self):
        response = self.annotation_response()
        self.stage(response)
        self.apply_value(self.decisions(response, "needs_review", "first"))
        alternative = copy.deepcopy(response)
        alternative["drafts"][0]["record"]["text"] += " Alternative synthetic reflection."
        self.stage(alternative)
        value = self.decisions(alternative, review_id="second")
        with self.assertRaisesRegex(JebError, "Explicitly supersede"):
            self.apply_value(value)
        value["items"][0]["supersedes"] = "first"
        self.apply_value(value)
        record = validate_knowledge(self.project, self.books())["reflection"]
        self.assertEqual(record["text"], alternative["drafts"][0]["record"]["text"])
        self.assertEqual(record["provenance"]["response_sha256"], digest(alternative))
        self.assertEqual(len(read_receipts(self.project)), 2)

    def test_promoted_ids_and_used_review_ids_cannot_be_overwritten(self):
        response = self.annotation_response()
        self.stage(response)
        value = self.decisions(response)
        self.apply_value(value)
        with self.assertRaisesRegex(JebError, "already used"):
            self.apply_value(value)
        replacement = self.decisions(response, "rejected", "replacement")
        replacement["items"][0]["supersedes"] = value["review_id"]
        with self.assertRaisesRegex(JebError, "collision"):
            self.apply_value(replacement)
        self.assertEqual(len(reader(self.project, self.source_id, "preview")["knowledge"]), 1)

    def test_unapproved_canonical_support_cannot_support_human_promotion(self):
        evidence = self.evidence()
        self.write_knowledge(evidence)
        claim = self.graph()[1]
        response = self.annotation_response([claim])
        self.stage(response)
        with self.assertRaisesRegex(JebError, "dependency closure"):
            self.apply_value(self.decisions(response))
        self.assertEqual(read_receipts(self.project), {})

    def test_changed_approved_canonical_support_hides_dependent_promotions(self):
        evidence = self.approve_test_knowledge(self.evidence())
        self.write_knowledge(evidence)
        response = self.annotation_response(self.graph()[1:])
        self.stage(response)
        self.apply_value(self.decisions(response))
        self.assertEqual(len(reader(self.project, self.source_id, "preview")["knowledge"]), 3)
        evidence["text"] += " Changed inspected synthetic support."
        evidence = self.approve_test_knowledge(evidence)
        self.write_knowledge(evidence)
        self.assertEqual(
            [r["record_id"] for r in reader(self.project, self.source_id, "preview")["knowledge"]],
            ["evidence"],
        )

    def test_passage_changes_hide_notes_without_modifying_text_approval(self):
        response = self.annotation_response()
        self.stage(response)
        self.apply_value(self.decisions(response))
        text_response = self.response()
        text_response["items"][0].update(
            action="propose",
            change_class="C",
            proposed_text=text_response["items"][0]["proposed_text"].replace(
                "mijenja", "prepravlja"
            ),
        )
        proposal = self.import_test_response(text_response)
        self.apply_test_decisions([self.decision(proposal)])
        artifact = reader(self.project, self.source_id, "preview")
        self.assertEqual(artifact["annotation_coverage"]["approved_current"], 0)
        self.assertEqual(artifact["coverage"][0]["approved_segments"], 1)
        self.assertEqual(len(read_receipts(self.project)), 1)

    def test_policy_or_bibliography_changes_make_promotions_pending(self):
        response = self.annotation_response()
        self.stage(response)
        self.apply_value(self.decisions(response))
        registry = read_yaml(self.project.path("sources/registry.yaml"))
        extra = copy.deepcopy(registry["sources"][0])
        extra.update(
            source_id="contextual-lead",
            kind="contextual",
            title="Synthetic contextual bibliography only",
        )
        registry["sources"].append(extra)
        write_json(self.project.path("sources/registry.yaml"), registry)
        self.assertEqual(reader(self.project, self.source_id, "preview")["knowledge"], [])
        packet = prepare(self.project, self.source_id, "fixture", "annotate", "new-context")
        self.assertFalse(packet["knowledge_catalog"][0]["current"])

    def test_changed_policy_hides_approved_notes_and_keeps_the_review_receipt(self):
        response = self.annotation_response()
        self.stage(response)
        self.apply_value(self.decisions(response))
        policy = self.project.path("docs/EDITORIAL_POLICY.md")
        policy.write_bytes(policy.read_bytes() + b"\nChanged temporary policy input\n")
        artifact = reader(self.project, self.source_id, "preview")
        self.assertEqual(artifact["knowledge"], [])
        self.assertEqual(artifact["annotation_coverage"]["pending_or_stale"], 1)
        self.assertEqual(len(read_receipts(self.project)), 1)

    def test_changed_source_context_hides_note_even_when_its_own_text_is_unchanged(self):
        response = self.annotation_response()
        self.stage(response)
        self.apply_value(self.decisions(response))
        changed_books = copy.deepcopy(self.books())
        changed_books["GEN"]["segments"][1]["normalized_text"] += (
            " Changed adjacent synthetic context."
        )
        with patch("jeb.export.load_corpus", return_value=changed_books):
            artifact = reader(self.project, self.source_id, "preview")
        self.assertEqual(artifact["knowledge"], [])
        self.assertEqual(artifact["annotation_coverage"]["pending_or_stale"], 1)
        self.assertEqual(len(read_receipts(self.project)), 1)

    def test_history_refuses_cycles_missing_predecessors_and_branching(self):
        response = self.annotation_response()
        self.stage(response)
        first = validate_decisions(self.project, self.decisions(response, "needs_review", "first"))
        second = copy.deepcopy(first)
        second["decisions"]["review_id"] = "second"
        second["decisions"]["items"][0]["supersedes"] = "first"
        third = copy.deepcopy(second)
        third["decisions"]["review_id"] = "third"
        with self.assertRaisesRegex(JebError, "Branching"):
            review_heads({"first": first, "second": second, "third": third})
        first["decisions"]["items"][0]["supersedes"] = "second"
        with self.assertRaisesRegex(JebError, "Cycle"):
            review_heads({"first": first, "second": second})
        with self.assertRaisesRegex(JebError, "Missing"):
            review_heads({"second": second})

    def test_receipt_preserves_original_inputs_after_working_caches_are_removed(self):
        response = self.annotation_response()
        imported = self.stage(response)
        self.apply_value(self.decisions(response))
        self.project.path(imported["output"]).unlink()
        self.project.path(f"data/knowledge-proposals/{response['packet_id']}/input.json").unlink()
        self.assertEqual(len(reader(self.project, self.source_id, "preview")["knowledge"]), 1)
        receipt = next(iter(read_receipts(self.project).values()))
        self.assertEqual(receipt["response"], response)

    def test_receipt_hash_tampering_and_manual_provenance_copy_are_rejected(self):
        response = self.annotation_response()
        self.stage(response)
        result = self.apply_value(self.decisions(response))
        receipt = next(iter(read_receipts(self.project).values()))
        record = next(iter(validate_knowledge(self.project, self.books()).values()))
        self.write_knowledge(record)
        with self.assertRaisesRegex(JebError, "must derive"):
            validate_knowledge(self.project, self.books())
        self.write_knowledge()
        receipt["response"]["drafts"][0]["rationale"] += " Tampered"
        write_json(self.project.path(result["output"]), receipt)
        with self.assertRaisesRegex(JebError, "binding changed|envelope|filename/hash"):
            read_receipts(self.project)

    def test_related_note_cycles_require_joint_approval_but_remain_allowed(self):
        first, second = self.knowledge_record("first"), self.knowledge_record("second")
        first["related_ids"], second["related_ids"] = ["second"], ["first"]
        response = self.annotation_response([first, second])
        self.stage(response)
        with self.assertRaisesRegex(JebError, "dependency closure"):
            self.apply_value(self.decisions(response, selected={"first"}))
        self.apply_value(self.decisions(response))
        self.assertEqual(len(reader(self.project, self.source_id, "preview")["knowledge"]), 2)

    def test_decision_bounds_invalid_sets_and_write_failure_leave_no_partial_commit(self):
        response = self.annotation_response(self.graph())
        self.stage(response)
        value = self.decisions(response)
        value["items"][-1]["draft_sha256"] = "0" * 64
        with self.assertRaises(JebError):
            self.apply_value(value)
        self.assertEqual(read_receipts(self.project), {})
        path = self.project.path("too-large.json")
        path.write_bytes(b" " * (MAX_DECISIONS + 1))
        with self.assertRaisesRegex(JebError, "exceeds"):
            read_decisions(path)
        with (
            patch(
                "jeb.knowledge_review.write_json",
                side_effect=OSError("Simulated pre-commit failure"),
            ),
            self.assertRaises(OSError),
        ):
            self.apply_value(self.decisions(response))
        self.assertEqual(read_receipts(self.project), {})
        self.assertEqual(validate_knowledge(self.project, self.books()), {})

    def test_cli_validation_and_apply_require_the_separate_human_decision_schema(self):
        response = self.annotation_response()
        self.stage(response)
        path = self.project.path("returned-ai.json")
        write_json(path, response)
        command = [
            sys.executable,
            "-m",
            "jeb",
            "--root",
            str(self.project.root),
            "--synthetic",
            "knowledge",
            "review",
            "apply",
            "--decisions",
            str(path),
        ]
        result = subprocess.run(command, capture_output=True, encoding="utf-8", check=False)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(read_receipts(self.project), {})
        write_json(path, self.decisions(response))
        validation = command.copy()
        validation[-3] = "validate"
        result = subprocess.run(validation, capture_output=True, encoding="utf-8", check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["approvals_created"], 0)
        self.assertEqual(read_receipts(self.project), {})
        result = subprocess.run(command, capture_output=True, encoding="utf-8", check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["promoted"], 1)
        self.assertEqual(len(read_receipts(self.project)), 1)

    @unittest.skipUnless(os.name == "nt", "Windows extended-length review receipt paths")
    def test_long_windows_review_receipts_remain_readable_and_duplicate_safe(self):
        response = self.annotation_response()
        self.stage(response)
        with tempfile.TemporaryDirectory(dir=native_path(Path(tempfile.gettempdir()))) as directory:
            root = Path(directory.removeprefix("\\\\?\\")) / ("deep-" + "x" * 50)
            shutil.copytree(self.project.root, native_path(root))
            project = Project(root, synthetic=True)
            value = self.decisions(response, review_id="r" * 80)
            path = project.path("test-decisions.json")
            write_json(path, value)
            result = apply(project, path)
            self.assertGreater(len(str(project.path(result["output"]))), 260)
            self.assertEqual(len(read_receipts(project)), 1)
            self.assertEqual(len(reader(project, self.source_id, "preview")["knowledge"]), 1)
            with self.assertRaisesRegex(JebError, "already used"):
                apply(project, path)
