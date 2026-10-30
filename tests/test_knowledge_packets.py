from __future__ import annotations

import copy
import json
import subprocess
import sys
from unittest.mock import patch

from jeb.core import JebError, canonical, digest, read_yaml, write_json
from jeb.export import reader
from jeb.knowledge import validate_knowledge
from jeb.knowledge_packets import (
    MAX_RESPONSE,
    current_packet,
    import_response,
    prepare,
    read_response,
    report,
    validate_response,
)
from jeb.review import all_decisions
from tests.support import WorkspaceTest


class KnowledgePacketTests(WorkspaceTest):
    def packet(self, task="annotate", packet_id=None):
        return prepare(self.project, self.source_id, "fixture", task, packet_id or f"test-{task}")

    def response(self, task="annotate"):
        packet = self.packet(task)
        result = {
            "schema_version": "1.0",
            "packet_id": packet["packet_id"],
            "packet_sha256": packet["packet_sha256"],
            "source_id": self.source_id,
            "task": task,
            "tool": {
                "name": "Automated synthetic packet fixture; no real research or human review",
                "model_identifier": None,
                "reported_at": "2026-10-30",
            },
            "limitations": [
                "Original synthetic software test only; no actual evidence or human participation."
            ],
            "review_state": "unreviewed",
            "approval_authority": "none",
            "human_attestation": False,
        }
        if task == "research":
            result["leads"] = []
            result["items"] = [
                {
                    "segment_id": row["display"]["segment_id"],
                    "text_sha256": row["display"]["text_sha256"],
                    "outcome": "no_new_evidence",
                    "summary": "Synthetic example only; no research finding.",
                    "known_evidence_ids": [],
                    "lead_ids": [],
                    "questions": ["What evidence is still missing?"],
                    "uncertainty": "No real research performed.",
                }
                for row in packet["segments"]
            ]
        else:
            result["drafts"] = [self.draft(self.knowledge_record("draft-reflection"))]
            result["items"] = [
                {
                    "segment_id": row["display"]["segment_id"],
                    "text_sha256": row["display"]["text_sha256"],
                    "action": "no_draft",
                    "record_ids": [],
                    "rationale": "Synthetic coverage fixture.",
                }
                for row in packet["segments"]
            ]
            self.cover(result)
        return result

    def draft(self, record):
        return {
            "record": record,
            "attribution": {
                "kind": "ai_assisted_draft",
                "credit": "Synthetic test author/tool; no owner voice",
            },
            "rationale": "Automated fixture, not an actual scholarly contribution.",
        }

    def cover(self, response):
        for item in response["items"]:
            ids = [
                d["record"]["record_id"]
                for d in response["drafts"]
                if item["segment_id"] in d["record"]["segment_ids"]
            ]
            item.update(record_ids=ids, action="drafts_proposed" if ids else "no_draft")

    def evidence(self, record_id="draft-evidence"):
        record = self.knowledge_record(record_id)
        record.update(
            record_type="evidence",
            layer="source_witness",
            evidence_category="primary_witness",
            source_id=self.source_id,
            bibliographic_details="Original synthetic fixture",
            url="urn:jeb:synthetic:fixture-v1",
            locator="First invented segment",
            access_date="2026-10-30",
        )
        return record

    def claim(self, record_id="draft-claim", evidence_id="draft-evidence"):
        record = self.knowledge_record(record_id)
        record.update(
            record_type="claim",
            layer="literary",
            evidence_category="editorial_inference",
            evidence_ids=[evidence_id],
        )
        return record

    def returned(self, value):
        path = self.project.path("returned-knowledge.json")
        write_json(path, value)
        return path

    def test_both_protocols_are_deterministic_bounded_and_non_approving(self):
        for task in ("research", "annotate"):
            with (
                self.subTest(task=task),
                patch("urllib.request.urlopen", side_effect=AssertionError("No network")),
            ):
                first, second = self.packet(task), self.packet(task)
                self.assertEqual(first, second)
                self.assertEqual(first["approval_authority"], "none")
                self.assertFalse(first["human_attestation"])
                self.assertEqual(len(first["coverage_manifest"]), 4)
                self.assertIn("display", first["segments"][0])
                self.assertLess(len(canonical(first)), 65536)

    def test_missing_pilot_coverage_unknown_source_and_unsafe_ids_fail(self):
        for selection in ("GEN", "MAT", "MRK", "LUK", "JHN"):
            with (
                self.subTest(selection=selection),
                self.assertRaisesRegex(JebError, "missing/ambiguous"),
            ):
                prepare(self.project, self.source_id, selection, "research", f"pilot-{selection}")
        for source, packet in (
            ("unknown", "safe"),
            (self.source_id, "../escape"),
            (self.source_id, "CON"),
        ):
            with self.subTest(source=source, packet=packet), self.assertRaises((JebError, OSError)):
                prepare(self.project, source, "fixture", "annotate", packet)

    def test_source_admission_is_not_bypassed(self):
        response = self.response()
        path = self.project.path("sources/registry.yaml")
        value = read_yaml(path)
        value["sources"][0]["status"] = "needs_review"
        write_json(path, value)
        with self.assertRaisesRegex(JebError, "needs_review"):
            validate_response(self.project, response)

    def test_packet_hash_and_resealed_policy_prompt_or_schema_substitution_rejected(self):
        packet = self.packet()
        path = self.project.path("data/knowledge-proposals/test-annotate/input.json")
        changed = copy.deepcopy(packet)
        changed["prompt"] = "Substituted prompt"
        write_json(path, changed)
        with self.assertRaisesRegex(JebError, "hash changed"):
            current_packet(self.project, "test-annotate")
        for field in ("policy", "prompt", "output_schema"):
            changed = copy.deepcopy(packet)
            changed[field] = {"type": "string"} if field == "output_schema" else "Substituted text"
            changed["packet_sha256"] = digest(
                {k: v for k, v in changed.items() if k != "packet_sha256"}
            )
            write_json(path, changed)
            with self.subTest(field=field), self.assertRaisesRegex(JebError, "substituted"):
                current_packet(self.project, "test-annotate")

    def test_policy_change_makes_response_stale(self):
        response = self.response()
        path = self.project.path("docs/EDITORIAL_POLICY.md")
        path.write_bytes(path.read_bytes() + b"\nChanged synthetic policy.\n")
        with self.assertRaisesRegex(JebError, "Stale"):
            validate_response(self.project, response)

    def test_display_uses_approved_wording_and_later_text_decisions_invalidate_packet(self):
        response = self.response()
        modernization = super().response(batch_id="changed-text")
        modernization["items"][0].update(
            action="propose",
            change_class="C",
            proposed_text=modernization["items"][0]["proposed_text"] + " Added synthetic sentence.",
        )
        proposal = self.import_test_response(modernization)
        # An unapproved proposal is not the annotation basis and does not stale this packet.
        validate_response(self.project, response)
        self.apply_test_decisions([self.decision(proposal)])
        with self.assertRaisesRegex(JebError, "Stale"):
            validate_response(self.project, response)
        packet = self.packet(packet_id="approved-display")
        self.assertNotEqual(
            packet["segments"][0]["display"]["text"],
            packet["segments"][0]["source"]["normalized_text"],
        )
        response.update(packet_id=packet["packet_id"], packet_sha256=packet["packet_sha256"])
        response["items"][0]["text_sha256"] = packet["segments"][0]["display"]["text_sha256"]
        response["drafts"][0]["record"]["depends_on"] = {
            response["items"][0]["segment_id"]: response["items"][0]["text_sha256"]
        }
        validate_response(self.project, response)

    def test_evidence_catalog_excludes_text_and_changes_or_namespace_additions_stale_packet(self):
        evidence = self.evidence("known-evidence")
        evidence["text"] = "PRIVATE SYNTHETIC BODY EXCLUDED FROM THE PACKET"
        self.write_knowledge(evidence)
        response = self.response()
        packet = current_packet(self.project, "test-annotate")
        self.assertNotIn("PRIVATE SYNTHETIC BODY", canonical(packet).decode("utf-8"))
        self.assertEqual(packet["knowledge_catalog"][0]["record_sha256"], digest(evidence))
        evidence["text"] = "Changed body"
        self.write_knowledge(evidence)
        with self.assertRaisesRegex(JebError, "Stale"):
            validate_response(self.project, response)

    def test_stale_support_is_excluded_transitively(self):
        old = self.evidence("known-old")
        old["depends_on"] = {s: "0" * 64 for s in old["segment_ids"]}
        claim = self.claim("known-claim", "known-old")
        current = self.evidence("known-current")
        self.write_knowledge(old, claim, current)
        response = self.response()
        packet = current_packet(self.project, "test-annotate")
        states = {r["record_id"]: r["current"] for r in packet["knowledge_catalog"]}
        self.assertFalse(states["known-old"])
        self.assertFalse(states["known-claim"])
        self.assertTrue(states["known-current"])
        record = response["drafts"][0]["record"]
        record.update(
            layer="literary",
            evidence_category="editorial_inference",
            evidence_ids=["known-current"],
            claim_ids=["known-claim"],
        )
        with self.assertRaisesRegex(JebError, "stale or unbound"):
            validate_response(self.project, response)

    def test_missing_duplicate_reordered_outside_ids_and_wrong_text_hashes_rejected(self):
        original = self.response()
        for items in (
            original["items"][:-1],
            list(reversed(original["items"])),
            [original["items"][0]] * 4,
        ):
            response = copy.deepcopy(original)
            response["items"] = items
            with self.subTest(items=items), self.assertRaisesRegex(JebError, "passage IDs"):
                validate_response(self.project, response)
        original["items"][0]["segment_id"] = "fixture:PSA.1.1"
        with self.assertRaisesRegex(JebError, "out-of-scope"):
            validate_response(self.project, original)
        original = self.response()
        original["items"][0]["text_sha256"] = "0" * 64
        with self.assertRaisesRegex(JebError, "display text hashes"):
            validate_response(self.project, original)

    def test_research_leads_are_unverified_and_require_valid_links_and_registered_ids(self):
        response = self.response("research")
        lead = {
            "lead_id": "test-lead",
            "source_id": None,
            "url": "https://example.invalid/metadata",
            "bibliographic_details": "Synthetic locator; not an actual source",
            "locator": "Example only",
            "access_date": "2026-10-30",
            "summary": "Unverified synthetic lead",
            "relationship": "unknown",
        }
        response["leads"] = [lead]
        response["items"][0].update(outcome="leads_found", lead_ids=["test-lead"])
        validate_response(self.project, response)
        variants = []
        changed = copy.deepcopy(response)
        changed["leads"][0]["source_id"] = "invented-source"
        variants.append(changed)
        changed = copy.deepcopy(response)
        changed["items"][0]["known_evidence_ids"] = ["invented-evidence"]
        variants.append(changed)
        changed = copy.deepcopy(response)
        changed["items"][0]["lead_ids"] = ["invented-lead"]
        variants.append(changed)
        changed = copy.deepcopy(response)
        changed["items"][0].update(outcome="no_new_evidence", lead_ids=[])
        variants.append(changed)
        changed = copy.deepcopy(response)
        changed["leads"].append({**lead, "lead_id": "other-lead"})
        variants.append(changed)
        changed = copy.deepcopy(response)
        changed["leads"][0]["url"] = "https://user:secret@example.invalid/"
        variants.append(changed)
        changed = copy.deepcopy(response)
        changed["leads"][0]["access_date"] = "2026-10-31"
        variants.append(changed)
        for changed in variants:
            with self.subTest(changed=changed), self.assertRaises(JebError):
                validate_response(self.project, changed)

    def test_annotation_graph_is_jointly_validated_and_does_not_enter_the_bank(self):
        response = self.response()
        evidence, claim = self.evidence(), self.claim()
        annotation = self.knowledge_record("draft-explanation")
        annotation.update(
            layer="literary",
            evidence_category="editorial_inference",
            evidence_ids=[evidence["record_id"]],
            claim_ids=[claim["record_id"]],
        )
        response["drafts"] += [self.draft(r) for r in (evidence, claim, annotation)]
        self.cover(response)
        before = reader(self.project, self.source_id, "preview")
        result = import_response(self.project, self.returned(response))
        self.assertFalse(result["canonical_knowledge_changed"])
        self.assertEqual(validate_knowledge(self.project, self.books()), {})
        self.assertEqual(reader(self.project, self.source_id, "preview"), before)
        self.assertEqual(all_decisions(self.project), {})

    def test_reflection_fiction_and_explanation_cannot_be_mislabelled(self):
        original = self.response()
        changes = [
            {"record_type": "evidence"},
            {"evidence_category": "primary_witness"},
            {"source_id": self.source_id},
            {"layer": "creative_adaptation"},
            {"layer": "literary", "evidence_category": "editorial_inference"},
        ]
        for fields in changes:
            response = copy.deepcopy(original)
            response["drafts"][0]["record"].update(fields)
            with self.subTest(fields=fields), self.assertRaises(JebError):
                validate_response(self.project, response)
        original["drafts"][0]["record"].update(
            layer="creative_adaptation", evidence_category="creative_adaptation"
        )
        validate_response(self.project, original)

    def test_draft_dependencies_scope_collision_coverage_and_record_types_rejected(self):
        original = self.response()
        variants = []
        value = copy.deepcopy(original)
        value["drafts"][0]["record"]["depends_on"] = {}
        variants.append(value)
        value = copy.deepcopy(original)
        value["drafts"][0]["record"]["depends_on"] = {original["items"][0]["segment_id"]: "0" * 64}
        variants.append(value)
        value = copy.deepcopy(original)
        value["drafts"][0]["record"]["segment_ids"] = ["fixture:PSA.1.1"]
        variants.append(value)
        value = copy.deepcopy(original)
        value["drafts"][0]["record"]["book_id"] = "MAT"
        variants.append(value)
        value = copy.deepcopy(original)
        value["items"][0]["record_ids"] = []
        variants.append(value)
        value = copy.deepcopy(original)
        value["drafts"].append(copy.deepcopy(value["drafts"][0]))
        variants.append(value)
        value = copy.deepcopy(original)
        value["drafts"][0]["record"]["record_type"] = "story"
        variants.append(value)
        value = copy.deepcopy(original)
        value["drafts"][0]["record"]["selected_name_mapping_id"] = "invented-native-name"
        variants.append(value)
        for value in variants:
            with self.subTest(value=value), self.assertRaises(JebError):
                validate_response(self.project, value)
        self.write_knowledge(self.knowledge_record("draft-reflection"))
        packet = self.packet(packet_id="collision-test")
        original.update(packet_id=packet["packet_id"], packet_sha256=packet["packet_sha256"])
        with self.assertRaisesRegex(JebError, "collides"):
            validate_response(self.project, original)

    def test_invented_reference_self_support_and_support_cycles_rejected(self):
        response = self.response()
        response["drafts"][0]["record"]["related_ids"] = ["invented-record"]
        with self.assertRaisesRegex(JebError, "unattached knowledge"):
            validate_response(self.project, response)
        response["drafts"][0]["record"]["related_ids"] = ["draft-reflection"]
        with self.assertRaisesRegex(JebError, "itself"):
            validate_response(self.project, response)
        evidence, first, second = self.evidence(), self.claim("first"), self.claim("second")
        first["claim_ids"], second["claim_ids"] = ["second"], ["first"]
        response["drafts"] = [self.draft(r) for r in (evidence, first, second)]
        self.cover(response)
        with self.assertRaisesRegex(JebError, "Circular support"):
            validate_response(self.project, response)
        first, second = self.knowledge_record("first-note"), self.knowledge_record("second-note")
        first["related_ids"], second["related_ids"] = ["second-note"], ["first-note"]
        response["drafts"] = [self.draft(r) for r in (first, second)]
        self.cover(response)
        validate_response(self.project, response)

    def test_approval_impersonation_wrong_task_and_unsupported_script_rejected(self):
        original = self.response()
        for field, value in (
            ("human_attestation", True),
            ("approval_authority", "owner"),
            ("review_state", "approved"),
        ):
            response = copy.deepcopy(original)
            response[field] = value
            with self.subTest(field=field), self.assertRaisesRegex(JebError, "schema"):
                validate_response(self.project, response)
        for fields in ({"review_state": "approved"}, {"approval": {"human_attestation": True}}):
            response = copy.deepcopy(original)
            response["drafts"][0]["record"].update(fields)
            with self.subTest(fields=fields), self.assertRaisesRegex(JebError, "schema"):
                validate_response(self.project, response)
        original["drafts"][0]["record"]["text"] = "\u0410"
        with self.assertRaisesRegex(JebError, "display-script"):
            validate_response(self.project, original)
        research = self.response("research")
        research.update(packet_id="test-annotate", packet_sha256=self.packet()["packet_sha256"])
        with self.assertRaisesRegex(JebError, "identity mismatch"):
            validate_response(self.project, research)

    def test_empty_drafts_duplicate_import_tampering_and_competing_responses(self):
        response = self.response()
        response["drafts"] = []
        self.cover(response)
        first = import_response(self.project, self.returned(response))
        with self.assertRaisesRegex(JebError, "Duplicate"):
            import_response(self.project, self.returned(response))
        response["items"][0]["rationale"] = "Alternative synthetic response"
        second = import_response(self.project, self.returned(response))
        self.assertNotEqual(first["response_sha256"], second["response_sha256"])
        write_json(self.project.path(first["output"]), response)
        with self.assertRaisesRegex(JebError, "content changed"):
            read_response(self.project.path(first["output"]))

    def test_context_bounds_and_report_fencing_preserve_different_outputs(self):
        response = self.response()
        path = self.project.path("oversized.json")
        path.write_bytes(b" " * (MAX_RESPONSE + 1))
        with self.assertRaisesRegex(JebError, "exceeds"):
            read_response(path)
        huge = copy.deepcopy(response)
        huge["limitations"] = ["x" * (MAX_RESPONSE + 1)]
        with self.assertRaisesRegex(JebError, "32 KiB"):
            validate_response(self.project, huge)
        response["limitations"] = ["```\nUntrusted sample instructions remain data."]
        report(self.project, self.returned(response), "reports/notes.md")
        self.assertIn("````json", self.project.path("reports/notes.md").read_text("utf-8"))
        response["limitations"] = ["Changed response"]
        with self.assertRaisesRegex(JebError, "Existing artifact differs"):
            report(self.project, self.returned(response), "reports/notes.md")

    def test_cli_preparation_and_validation_reject_incomplete_input_without_traceback(self):
        args = [
            sys.executable,
            "-m",
            "jeb",
            "--root",
            str(self.project.root),
            "--synthetic",
            "knowledge",
        ]
        process = subprocess.run(
            args
            + [
                "prepare",
                "--source",
                self.source_id,
                "--selection",
                "fixture",
                "--task",
                "research",
                "--packet-id",
                "cli-research",
            ],
            capture_output=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(json.loads(process.stdout)["approval_authority"], "none")
        path = self.project.path("invalid.json")
        path.write_text("{}", encoding="utf-8")
        process = subprocess.run(
            args + ["validate", "--input", str(path)],
            capture_output=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(process.returncode, 2)
        self.assertNotIn("Traceback", process.stderr)
