from __future__ import annotations

import copy
import json
import subprocess
import sys
from unittest.mock import patch

from jeb import narrative_packets, narrative_review
from jeb.core import JebError, digest, native_path, read_yaml, sha256, write_json
from jeb.export import reader
from jeb.knowledge import validate_knowledge
from jeb.review import all_decisions
from tests import test_narrative_packets as helpers
from tests.support import WorkspaceTest


class NarrativeReviewTests(WorkspaceTest):
    packet = helpers.NarrativePacketTests.packet
    response = helpers.NarrativePacketTests.response
    cover = helpers.NarrativePacketTests.cover
    draft = helpers.NarrativePacketTests.draft
    evidence = helpers.NarrativePacketTests.evidence
    claim = helpers.NarrativePacketTests.claim
    returned = helpers.NarrativePacketTests.returned

    def stage(self, value=None):
        value = self.response() if value is None else value
        return value, narrative_packets.import_response(self.project, self.returned(value))

    def export(self, value, output="reports/narrative-review.md"):
        return narrative_review.report(self.project, value["packet_id"], digest(value), output)

    def text(self, output="reports/narrative-review.md"):
        return native_path(self.project.path(output)).read_text("utf-8")

    def test_only_exact_imported_responses_and_safe_full_identities_are_accepted(self):
        value = self.response()
        with self.assertRaisesRegex(JebError, "Import the narrative"):
            self.export(value)
        self.assertFalse(self.project.path("reports/narrative-review.md").exists())
        self.stage(value)
        for packet, identity in (
            ("../escape", digest(value)),
            ("CON", digest(value)),
            (value["packet_id"], digest(value)[:16]),
            (value["packet_id"], "A" * 64),
            (value["packet_id"], "../escape"),
        ):
            with self.subTest(packet=packet, identity=identity), self.assertRaises(JebError):
                narrative_review.report(
                    self.project, packet, identity, "reports/narrative-review.md"
                )
        with self.assertRaisesRegex(JebError, "Markdown"):
            self.export(value, "reports/decision.json")
        self.assertFalse(self.project.path("reports/decision.json").exists())

    def test_another_valid_packet_response_cannot_be_substituted(self):
        value = self.response()
        other = self.packet("other-narrative")
        value.update(packet_id=other["packet_id"], packet_sha256=other["packet_sha256"])
        self.stage(value)
        # Copying a valid response into a different packet directory must not redirect the handoff.
        write_json(
            self.project.path(
                f"data/narrative-proposals/test-narrative/responses/{digest(value)}.json"
            ),
            value,
        )
        with self.assertRaisesRegex(JebError, "another packet"):
            narrative_review.report(
                self.project, "test-narrative", digest(value), "reports/substituted.md"
            )
        self.assertFalse(self.project.path("reports/substituted.md").exists())

    def test_report_is_deterministic_unsigned_and_only_writes_the_requested_file(self):
        value, _ = self.stage()
        before_reader = reader(self.project, self.source_id, "preview")
        before = {
            p.relative_to(self.project.root).as_posix(): sha256(native_path(p).read_bytes())
            for p in self.project.root.rglob("*")
            if p.is_file()
        }
        result = self.export(value)
        self.assertEqual(result["human_decisions_created"], 0)
        self.assertEqual(result["approvals_created"], 0)
        self.assertFalse(result["canonical_knowledge_changed"])
        self.assertEqual(result["narrative_nodes"], 8)
        self.assertEqual(result["support_records"], 1)
        self.assertEqual(result["indexed_spans"], 4)
        self.assertEqual(result["response_sha256"], digest(value))
        after = {
            p.relative_to(self.project.root).as_posix(): sha256(native_path(p).read_bytes())
            for p in self.project.root.rglob("*")
            if p.is_file()
        }
        after.pop(result["output"])
        self.assertEqual(after, before)
        self.assertEqual(all_decisions(self.project), {})
        self.assertEqual(validate_knowledge(self.project, self.books()), {})
        self.assertEqual(reader(self.project, self.source_id, "preview"), before_reader)
        self.assertEqual(self.export(value), result)
        self.export(value, "reports/second-copy.md")
        self.assertEqual(self.text(), self.text("reports/second-copy.md"))
        self.assertIn("unsigned inspection handoff", self.text())
        self.assertIn(digest(value["nodes"][0]), self.text())

    def test_exact_unicode_spans_roles_and_basis_separation_are_visible(self):
        value, _ = self.stage()
        self.export(value)
        text = self.text()
        self.assertIn("Mention: [span-001](#span-001) — covik", text)
        self.assertIn("Anchor: [span-002](#span-002) — ne mijenja 2 broja", text)
        self.assertIn(sha256("probni zapis".encode("utf-8")), text)
        self.assertIn("end is exclusive", text)
        self.assertIn("original_record_byte_span", text)
        self.assertIn("Source narration only", text)
        self.assertIn("## historical_claim\n\nUnverified historical claims", text)
        self.assertIn("None proposed.", text)
        self.assertIn("## fiction", text)
        reading = text.split("### event: `reading`", 1)[1].split("### story:", 1)[0]
        self.assertIn("| `object` | patient | probni zapis |", reading)
        self.assertNotIn("| `person` | agent |", reading)
        self.assertIn("No omitted subject or motive", reading)
        self.assertIn("Presentation only; no historical chronology asserted", text)
        self.assertIn("no evidentiary role", text)

    def test_approved_display_offsets_and_original_source_remain_separate(self):
        modernization = WorkspaceTest.response(self)
        original = modernization["items"][0]["proposed_text"]
        changed = "Probni uvod. " + original
        modernization["items"][0].update(
            action="propose", proposed_text=changed, change_class="C", flags=["linguistic"]
        )
        proposal = self.import_test_response(modernization)
        self.apply_test_decisions([self.decision(proposal)])  # isolated temporary test attestation
        value = self.response()
        value["support_drafts"][0]["record"]["depends_on"] = copy.deepcopy(
            value["nodes"][0]["depends_on"]
        )
        self.stage(value)
        before = copy.deepcopy(all_decisions(self.project))
        self.export(value)
        text = self.text()
        self.assertIn("Original source transcription:\n\n```text\n" + original, text)
        self.assertIn(
            "Current reader wording (span coordinate space):\n\n```text\n" + changed, text
        )
        self.assertIn(f'"start": {changed.index("covik")}', text)
        self.assertIn("approved_modernization", text)
        self.assertIn('"text_decision_id": "test-decision"', text)
        self.assertEqual(all_decisions(self.project), before)

    def test_stale_policy_namespace_and_rights_fail_before_output(self):
        value, _ = self.stage()
        policy = self.project.path("docs/EDITORIAL_POLICY.md")
        original = policy.read_bytes()
        policy.write_bytes(original + b"\nTemporary test policy change.\n")
        with self.assertRaises(JebError):
            self.export(value)
        policy.write_bytes(original)
        self.write_knowledge(self.knowledge_record("new-namespace-record"))
        with self.assertRaisesRegex(JebError, "Stale or substituted"):
            self.export(value)
        self.project.path("data/knowledge/records.jsonl").unlink()
        registry = read_yaml(self.project.path("sources/registry.yaml"))
        registry["sources"][0]["status"] = "needs_review"
        write_json(self.project.path("sources/registry.yaml"), registry)
        with self.assertRaisesRegex(JebError, "needs_review"):
            self.export(value)
        self.assertFalse(self.project.path("reports/narrative-review.md").exists())

    def test_tampered_cached_response_or_resealed_packet_is_rejected(self):
        value, imported = self.stage()
        altered = copy.deepcopy(value)
        altered["limitations"].append("Changed cached text")
        write_json(self.project.path(imported["output"]), altered)
        with self.assertRaisesRegex(JebError, "content changed"):
            self.export(value)
        write_json(self.project.path(imported["output"]), value)
        packet = self.packet()
        packet["prompt"] = "Substituted prompt"
        packet["packet_sha256"] = digest({k: v for k, v in packet.items() if k != "packet_sha256"})
        write_json(
            self.project.path(f"data/narrative-proposals/{value['packet_id']}/input.json"), packet
        )
        with self.assertRaisesRegex(JebError, "Stale or substituted"):
            self.export(value)
        self.assertFalse(self.project.path("reports/narrative-review.md").exists())

    def test_support_chains_keep_typed_edges_and_do_not_copy_canonical_note_text(self):
        known = self.evidence("known-evidence")
        known["text"] = "CANONICAL_NOTE_BODY_MUST_NOT_BE_COPIED"
        self.write_knowledge(known)
        value = self.response()
        first = self.claim("claim-a", "known-evidence")
        second = self.claim("claim-b")
        second["claim_ids"] = ["claim-a"]
        value["support_drafts"].extend([self.draft(first), self.draft(second)])
        for node in value["nodes"][:5]:
            node["claim_ids"] = ["claim-b"]
        self.cover(value)
        self.stage(value)
        result = self.export(value)
        self.assertEqual(result["support_records"], 4)
        text = self.text()
        self.assertIn("| evidence_ids | `known-evidence` | evidence |", text)
        self.assertIn("| claim_ids | `claim-a` | claim |", text)
        self.assertIn(digest(known), text)
        self.assertIn("attached_canonical_metadata", text)
        self.assertNotIn(known["text"], text)
        self.assertIn("Original synthetic fixture", text)
        self.assertIn("urn:jeb:synthetic:fixture-v1", text)

    def test_related_cycles_are_displayed_as_links_without_invented_corroboration(self):
        value = self.response()
        first, second = self.claim("claim-a"), self.claim("claim-b")
        first["related_ids"], second["related_ids"] = ["claim-b"], ["claim-a"]
        value["support_drafts"].extend([self.draft(first), self.draft(second)])
        self.cover(value)
        self.stage(value)
        result = self.export(value)
        self.assertEqual(result["support_records"], 3)
        self.assertIn("| related_ids | `claim-b` | claim |", self.text())
        self.assertIn("Related/entity links are not evidentiary corroboration", self.text())

    def test_selected_name_mapping_retains_its_exact_prior_approval_identity(self):
        mapping = {
            "mapping_id": "test-name",
            "entity_id": "test-entity",
            "attested_form_latin": "probni zapis",
            "display_form": "Probni",
            "aliases": [],
            "source_language": "Original synthetic test",
            "witness_source_id": self.source_id,
            "witness_locator": "First invented segment",
            "historical_form": None,
            "historical_form_status": "unknown",
            "competing_forms": [],
            "transliteration_scheme": "Original Latin test; no transliteration",
            "rationale": "Isolated test only; not an actual owner approval",
            "status": "approved",
        }
        mapping["approval"] = {
            "reviewer_id": "SYNTHETIC-TEST-OWNER",
            "date": "2026-10-31",
            "human_attestation": True,
            "content_sha256": digest(mapping),
        }
        write_json(
            self.project.path("config/name_registry.yaml"),
            {"schema_version": "1.0", "scheme_status": "unapproved", "mappings": [mapping]},
        )
        value = self.response()
        value["nodes"][1].update(label="Probni", name_mapping_id=mapping["mapping_id"])
        self.stage(value)
        result = self.export(value)
        text = self.text()
        for identity in (
            digest(mapping),
            digest(mapping["approval"]),
            mapping["approval"]["content_sha256"],
        ):
            self.assertIn(identity, text)
        self.assertIn("original_mapping", text)
        self.assertIn("probni zapis", text)
        self.assertEqual(result["approvals_created"], 0)
        self.assertIn("do not approve this narrative", text)

    def test_all_three_relation_boundaries_and_exact_anchors_remain_visible(self):
        value = self.response()
        relations = value["nodes"][4]["relations"]
        relations.extend(
            [
                {
                    "from_event_id": "state",
                    "to_event_id": "reading",
                    "relation": "source_stated_before",
                    "anchor": copy.deepcopy(value["nodes"][3]["anchor"]),
                    "uncertainty": "Synthetic semantic test: an in-range span does not establish before.",
                },
                {
                    "from_event_id": "reading",
                    "to_event_id": "state",
                    "relation": "uncertain",
                    "anchor": None,
                    "uncertainty": "Unresolved reverse relation, not a chronology edge.",
                },
            ]
        )
        self.stage(value)
        result = self.export(value)
        text = self.text()
        self.assertIn("Presentation only; no historical chronology asserted", text)
        self.assertIn("Proposed source-stated chronology; inspect the anchor's meaning", text)
        self.assertIn("Unresolved relation; establishes no ordering edge", text)
        self.assertEqual(result["indexed_spans"], 4)  # shared relation/event anchor is indexed once

    def test_untrusted_free_text_is_fenced_and_table_cells_are_literal(self):
        value = self.response()
        value["nodes"][5]["label"] = "| [bad](https://invalid.example) <script> `\n# fake"
        value["nodes"][6]["description"] = "````\n# injected heading\n<script>alert(1)</script>"
        value["nodes"][6]["participants"][0]["uncertainty"] = "first | second\n# third"
        self.stage(value)
        self.export(value)
        text = self.text()
        row = next(
            line for line in text.splitlines() if line.startswith("| `fiction-person` | agent |")
        )
        self.assertIn("&#124;", row)
        self.assertIn("&#91;bad&#93;", row)
        self.assertIn("&#60;script&#62;", row)
        self.assertNotIn("[bad](", row)
        self.assertIn(" ↵ ", row)
        self.assertIn("`````text", text)
        self.assertIn("`````json", text)

    def test_report_bound_and_immutable_output_fail_without_partial_writes(self):
        value, _ = self.stage()
        with (
            patch("jeb.narrative_review.MAX_REPORT", 200),
            self.assertRaisesRegex(JebError, "1 MiB"),
        ):
            self.export(value)
        self.assertFalse(self.project.path("reports/narrative-review.md").exists())
        self.export(value)
        original = self.text()
        value["limitations"].append("Another valid candidate")
        self.stage(value)
        with self.assertRaises(JebError):
            self.export(value)
        self.assertEqual(self.text(), original)

    def test_empty_support_only_and_reordered_nodes_are_inspectable(self):
        original, _ = self.stage()
        self.export(original)
        spans = self.text().split("## Exact display spans", 1)[1].split("## Support chains", 1)[0]
        changed = copy.deepcopy(original)
        changed["nodes"].reverse()
        self.cover(changed)
        self.stage(changed)
        self.export(changed, "reports/reordered.md")
        self.assertEqual(
            spans,
            self.text("reports/reordered.md")
            .split("## Exact display spans", 1)[1]
            .split("## Support chains", 1)[0],
        )
        for support in (True, False):
            value = copy.deepcopy(original)
            value["nodes"] = []
            if not support:
                value["support_drafts"] = []
            self.cover(value)
            self.stage(value)
            result = self.export(value, f"reports/empty-{support}.md")
            self.assertEqual(result["narrative_nodes"], 0)
            self.assertEqual(result["indexed_spans"], 0)
            self.assertEqual(result["support_records"], int(support))
            self.assertIn("No source spans proposed.", self.text(f"reports/empty-{support}.md"))

    def test_cli_exports_only_unsigned_handoff_and_has_no_apply_operation(self):
        value, _ = self.stage()
        prefix = [
            sys.executable,
            "-m",
            "jeb",
            "--root",
            str(self.project.root),
            "--synthetic",
            "knowledge",
            "narrative",
            "review",
        ]
        args = [
            "export",
            "--packet-id",
            value["packet_id"],
            "--response-sha256",
            digest(value),
            "--output",
            "reports/cli-review.md",
        ]
        result = subprocess.run(prefix + args, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["approvals_created"], 0)
        for bad_args in (
            ["apply"],
            args[:4] + [digest(value)[:16]] + args[5:],
            args[:-1] + ["../outside.md"],
        ):
            result = subprocess.run(
                prefix + bad_args, capture_output=True, text=True, encoding="utf-8"
            )
            self.assertEqual(result.returncode, 2, result.stdout)
            self.assertNotIn("Traceback", result.stderr)
        self.assertFalse(self.project.path("data/knowledge-reviews").exists())


class NarrativeDecisionTests(WorkspaceTest):
    packet = helpers.NarrativePacketTests.packet
    response = helpers.NarrativePacketTests.response
    cover = helpers.NarrativePacketTests.cover
    draft = helpers.NarrativePacketTests.draft
    evidence = helpers.NarrativePacketTests.evidence
    claim = helpers.NarrativePacketTests.claim
    returned = helpers.NarrativePacketTests.returned
    stage = NarrativeReviewTests.stage

    def narrative_decision(self, value):
        packet = narrative_review._staged(self.project, value["packet_id"], digest(value))[0]
        targets = {"node:" + n["node_id"]: digest(n) for n in value["nodes"]}
        targets.update(
            {"support:" + d["record"]["record_id"]: digest(d) for d in value["support_drafts"]}
        )
        return {
            "schema_version": "1.0",
            "review_id": "temporary-test",
            "packet_id": value["packet_id"],
            "context_sha256": digest(packet),
            "response_sha256": digest(value),
            "reviewer_id": "synthetic test only",
            "reviewer_role": "owner",
            "human_attestation": True,
            "reviewed_at": "2026-10-31",
            "items": [
                {
                    "target_id": key,
                    "target_sha256": identity,
                    "state": "needs_review",
                    "rationale": "Temporary synthetic inspection only",
                    "checks": [
                        "meaning_and_roles_checked",
                        "support_inspected",
                        "category_and_uncertainty_checked",
                        "contribution_rights_checked",
                        "attribution_checked",
                    ],
                }
                for key, identity in targets.items()
            ],
        }

    def test_validation_only_and_tampered_attestations(self):
        value, _ = self.stage()
        decision = self.narrative_decision(value)
        path = self.project.path("temporary-decisions.json")
        write_json(path, decision)
        before = {
            str(p): sha256(p.read_bytes()) for p in self.project.root.rglob("*") if p.is_file()
        }
        self.assertTrue(narrative_review.validate_decisions(self.project, path)["validation_only"])
        self.assertEqual(
            before,
            {str(p): sha256(p.read_bytes()) for p in self.project.root.rglob("*") if p.is_file()},
        )
        for mutate in (
            lambda d: d.update(context_sha256="0" * 64),
            lambda d: d.update(human_attestation=False),
            lambda d: d["items"].pop(),
            lambda d: d["items"][0].update(target_sha256="0" * 64),
            lambda d: d["items"][0].update(checks=[]),
            lambda d: d.update(reviewer_id=" "),
        ):
            bad = copy.deepcopy(decision)
            mutate(bad)
            write_json(path, bad)
            with self.assertRaises(JebError):
                narrative_review.validate_decisions(self.project, path)
