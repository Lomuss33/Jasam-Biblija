from __future__ import annotations

import copy
import json
import subprocess
import sys
from unittest.mock import patch

from jeb.core import JebError, canonical, digest, read_json, read_yaml, write_json
from jeb.export import reader
from jeb.review import all_decisions, apply
from jeb.review_assistance import (
    MAX_RESPONSE,
    current_packet,
    import_response,
    prepare,
    read_response,
    report,
    validate_response,
)
from tests.support import WorkspaceTest


class ReviewAssistanceTests(WorkspaceTest):
    def critique(self, mode="plain"):
        modernization = self.response()
        if mode == "flagged":
            item = modernization["items"][0]
            item.update(
                action="propose",
                change_class="C",
                proposed_text=item["proposed_text"].replace(" ne ", " ").replace("2", "3"),
            )
        elif mode == "sensitive":
            modernization["items"][0]["change_class"] = "D"
        elif mode == "unresolved":
            modernization["items"][0].update(
                action="needs_review", change_class="D", proposed_text=None
            )
        self.proposal = self.import_test_response(modernization)
        self.packet_id = "test-review-assistance"
        packet = prepare(self.project, self.proposal["proposal_id"], self.packet_id)
        return {
            "schema_version": "1.0",
            "packet_id": self.packet_id,
            "packet_sha256": packet["packet_sha256"],
            "proposal_id": self.proposal["proposal_id"],
            "proposal_sha256": digest(self.proposal),
            "tool": {
                "name": "Automated synthetic critique fixture; no real model or human review",
                "model_identifier": None,
                "reported_at": "2026-10-30",
            },
            "reviewer_kind": "ai_assistance",
            "items": [
                {
                    "segment_id": item["segment_id"],
                    "source_text_sha256": item["source_text_sha256"],
                    "proposed_text_sha256": item["text_sha256"],
                    "observation": "needs_expert_review"
                    if "meaning_sensitive" in item["flags"]
                    else "concerns"
                    if item["flags"]
                    else "no_issues_observed",
                    "rationale": "Synthetic software fixture only, not an actual fidelity judgment.",
                    "flag_assessments": [
                        {
                            "flag": flag,
                            "assessment": "requires_expert"
                            if flag == "meaning_sensitive"
                            else "question_for_owner",
                            "rationale": "Synthetic open-flag assessment only.",
                        }
                        for flag in item["flags"]
                    ],
                    "issues": [],
                    "uncertainty": "Original invented test data; no historical or expert assessment.",
                }
                for item in self.proposal["items"]
            ],
            "limitations": [
                "Automated fixture only; no actual human, expert or model-review participation."
            ],
            "review_state": "unreviewed",
            "approval_authority": "none",
            "human_attestation": False,
        }

    def issue(self, issue_id="synthetic-issue"):
        return {
            "issue_id": issue_id,
            "category": "uncertainty",
            "summary": "Synthetic concern only.",
            "suggested_check": "Inspect the exact source and proposal; do not infer approval.",
            "evidence_ids": [],
        }

    def returned(self, response):
        path = self.project.path("returned-critique.json")
        write_json(path, response)
        return path

    def test_packet_is_self_contained_deterministic_and_non_approving(self):
        response = self.critique("flagged")
        with patch("urllib.request.urlopen", side_effect=AssertionError("No network")):
            first = current_packet(self.project, self.packet_id)
            second = prepare(self.project, self.proposal["proposal_id"], self.packet_id)
        self.assertEqual(first, second)
        self.assertEqual(first["proposal"], self.proposal)
        self.assertEqual(first["coverage_manifest"], [i["segment_id"] for i in response["items"]])
        self.assertIn("context", first["source_packet"])
        self.assertIn("policy", first["source_packet"])
        self.assertEqual(first["approval_authority"], "none")
        self.assertFalse(first["human_attestation"])
        self.assertEqual(all_decisions(self.project), {})

    def test_source_clearance_is_not_bypassed(self):
        response = self.critique()
        path = self.project.path("sources/registry.yaml")
        value = read_yaml(path)
        value["sources"][0]["status"] = "needs_review"
        write_json(path, value)
        with self.assertRaisesRegex(JebError, "needs_review"):
            validate_response(self.project, response)

    def test_unsafe_packet_filename_is_rejected(self):
        self.critique()
        for packet_id in ("../escape", "CON", "unsafe:windows"):
            with self.subTest(packet_id=packet_id), self.assertRaises(JebError):
                prepare(self.project, self.proposal["proposal_id"], packet_id)

    def test_packet_hash_and_resealed_prompt_schema_or_text_substitution_rejected(self):
        self.critique()
        path = self.project.path(f"data/review-assistance/{self.packet_id}/input.json")
        original = read_json(path)
        changed = copy.deepcopy(original)
        changed["prompt"] = "Altered prompt"
        write_json(path, changed)
        with self.assertRaisesRegex(JebError, "hash changed"):
            current_packet(self.project, self.packet_id)
        for field in ("prompt", "output_schema", "proposal"):
            changed = copy.deepcopy(original)
            if field == "prompt":
                changed[field] = "Altered prompt"
            elif field == "output_schema":
                changed[field] = {"type": "string"}
            else:
                changed[field]["items"][0]["proposed_text"] += " Substituted wording."
            changed["packet_sha256"] = digest(
                {k: v for k, v in changed.items() if k != "packet_sha256"}
            )
            write_json(path, changed)
            with self.subTest(field=field), self.assertRaisesRegex(JebError, "substituted"):
                current_packet(self.project, self.packet_id)

    def test_policy_source_and_proposal_edits_invalidate_critique(self):
        response = self.critique()
        policy = self.project.path("docs/EDITORIAL_POLICY.md")
        original = policy.read_bytes()
        policy.write_bytes(original + b"\nChanged synthetic test policy.\n")
        with self.assertRaisesRegex(JebError, "Stale policy"):
            validate_response(self.project, response)
        policy.write_bytes(original)
        proposal_path = self.project.path(f"data/proposals/{self.proposal['proposal_id']}.json")
        changed = copy.deepcopy(self.proposal)
        changed["items"][0]["proposed_text"] += " Edited after import."
        write_json(proposal_path, changed)
        with self.assertRaisesRegex(JebError, "changed or is stale"):
            validate_response(self.project, response)
        write_json(proposal_path, self.proposal)
        lock = read_json(self.project.path("sources/lock.json"))["sources"][0]
        raw_path = self.project.path(f"data/raw/{self.source_id}/{lock['sha256']}.txt")
        raw_path.write_bytes(raw_path.read_bytes() + b"changed")
        with self.assertRaisesRegex(JebError, "source bytes changed"):
            validate_response(self.project, response)

    def test_evidence_catalog_is_metadata_only_and_content_changes_make_it_stale(self):
        evidence = self.knowledge_record("fixture-evidence")
        evidence.update(
            record_type="evidence",
            layer="source_witness",
            evidence_category="primary_witness",
            source_id=self.source_id,
            url="urn:jeb:synthetic:evidence",
            locator="Original fixture only",
            text="PRIVATE SYNTHETIC NOTE BODY MUST NOT BE SENT",
        )
        self.write_knowledge(evidence)
        response = self.critique()
        packet = current_packet(self.project, self.packet_id)
        self.assertEqual(packet["evidence_catalog"][0]["record_sha256"], digest(evidence))
        self.assertNotIn("PRIVATE SYNTHETIC NOTE BODY", canonical(packet).decode("utf-8"))
        response["items"][0].update(observation="concerns", issues=[self.issue()])
        response["items"][0]["issues"][0]["evidence_ids"] = ["fixture-evidence"]
        validate_response(self.project, response)
        evidence["text"] = "Changed evidence content, not copied into the packet."
        self.write_knowledge(evidence)
        with self.assertRaisesRegex(JebError, "Stale"):
            validate_response(self.project, response)

    def test_missing_duplicate_reordered_and_outside_collection_items_rejected(self):
        original = self.critique()
        for items in (
            original["items"][:-1],
            list(reversed(original["items"])),
            [original["items"][0]] * 4,
        ):
            response = copy.deepcopy(original)
            response["items"] = items
            with self.subTest(items=items), self.assertRaisesRegex(JebError, "segment IDs"):
                validate_response(self.project, response)
        original["items"][0]["segment_id"] = "fixture:PSA.1.1"
        with self.assertRaisesRegex(JebError, "out-of-scope"):
            validate_response(self.project, original)

    def test_changed_proposal_packet_or_item_hashes_rejected(self):
        original = self.critique()
        for field in (
            "packet_sha256",
            "proposal_sha256",
            "source_text_sha256",
            "proposed_text_sha256",
        ):
            response = copy.deepcopy(original)
            target = (
                response if field in ("packet_sha256", "proposal_sha256") else response["items"][0]
            )
            target[field] = "0" * 64
            with self.subTest(field=field), self.assertRaises(JebError):
                validate_response(self.project, response)

    def test_existing_flags_cannot_be_dropped_reordered_invented_or_cleared(self):
        original = self.critique("flagged")
        flags = original["items"][0]["flag_assessments"]
        self.assertGreater(len(flags), 1)
        for assessments in (flags[:-1], list(reversed(flags)), [flags[0]] * len(flags)):
            response = copy.deepcopy(original)
            response["items"][0]["flag_assessments"] = assessments
            with (
                self.subTest(assessments=assessments),
                self.assertRaisesRegex(JebError, "Every existing flag"),
            ):
                validate_response(self.project, response)
        original["items"][0]["flag_assessments"][0]["assessment"] = "resolved"
        with self.assertRaisesRegex(JebError, "schema"):
            validate_response(self.project, original)

    def test_no_issues_cannot_hide_open_flags_or_reported_issues(self):
        response = self.critique("flagged")
        response["items"][0]["observation"] = "no_issues_observed"
        with self.assertRaisesRegex(JebError, "Open concerns"):
            validate_response(self.project, response)
        response["items"][0]["observation"] = "concerns"
        response["items"][1]["issues"] = [self.issue()]
        with self.assertRaisesRegex(JebError, "Open concerns"):
            validate_response(self.project, response)

    def test_meaning_sensitive_escalation_and_human_gate_stay_blocked(self):
        response = self.critique("sensitive")
        response["items"][0]["observation"] = "concerns"
        with self.assertRaisesRegex(JebError, "expert-review escalation"):
            validate_response(self.project, response)
        response["items"][0]["observation"] = "needs_expert_review"
        response["items"][0]["flag_assessments"][0]["assessment"] = "question_for_owner"
        with self.assertRaisesRegex(JebError, "open for an expert"):
            validate_response(self.project, response)
        response["items"][0]["flag_assessments"][0]["assessment"] = "requires_expert"
        import_response(self.project, self.returned(response))
        with self.assertRaisesRegex(JebError, "Meaning-sensitive"):
            self.apply_test_decisions([self.decision(self.proposal)])

    def test_unresolved_text_remains_null_and_no_rewrite_field_is_accepted(self):
        response = self.critique("unresolved")
        self.assertIsNone(response["items"][0]["proposed_text_sha256"])
        validate_response(self.project, response)
        response["items"][0]["replacement_text"] = "Invented replacement"
        with self.assertRaisesRegex(JebError, "schema"):
            validate_response(self.project, response)

    def test_invented_evidence_and_duplicate_issue_ids_rejected(self):
        response = self.critique()
        response["items"][0].update(observation="concerns", issues=[self.issue()])
        response["items"][0]["issues"][0]["evidence_ids"] = ["invented-scholarship"]
        with self.assertRaisesRegex(JebError, "unattached review evidence"):
            validate_response(self.project, response)
        response["items"][0]["issues"][0]["evidence_ids"] = []
        response["items"][1].update(observation="concerns", issues=[self.issue()])
        with self.assertRaisesRegex(JebError, "Duplicate review issue"):
            validate_response(self.project, response)

    def test_human_approval_impersonation_and_wrong_script_rejected(self):
        original = self.critique()
        for field, value in (
            ("human_attestation", True),
            ("approval_authority", "owner"),
            ("reviewer_kind", "expert"),
            ("review_state", "approved"),
        ):
            response = copy.deepcopy(original)
            response[field] = value
            with self.subTest(field=field), self.assertRaisesRegex(JebError, "schema"):
                validate_response(self.project, response)
        with self.assertRaisesRegex(JebError, "decisions schema"):
            apply(self.project, self.returned(original))
        original["items"][0]["rationale"] = "\u0410"
        with self.assertRaisesRegex(JebError, "display-script"):
            validate_response(self.project, original)
        self.assertEqual(all_decisions(self.project), {})

    def test_import_is_immutable_duplicate_protected_and_reader_neutral(self):
        response = self.critique("flagged")
        before = reader(self.project, self.source_id, "preview")
        proposal_path = self.project.path(f"data/proposals/{self.proposal['proposal_id']}.json")
        proposal_bytes = proposal_path.read_bytes()
        with patch("urllib.request.urlopen", side_effect=AssertionError("No network")):
            result = import_response(self.project, self.returned(response))
        self.assertEqual(result["approval_authority"], "none")
        self.assertFalse(result["human_decisions_changed"])
        self.assertEqual(reader(self.project, self.source_id, "preview"), before)
        self.assertEqual(proposal_path.read_bytes(), proposal_bytes)
        self.assertEqual(all_decisions(self.project), {})
        with self.assertRaisesRegex(JebError, "Duplicate"):
            import_response(self.project, self.returned(response))
        response["items"][0]["rationale"] += " Changed after import."
        write_json(self.project.path(result["output"]), response)
        with self.assertRaisesRegex(JebError, "content changed"):
            read_response(self.project.path(result["output"]))

    def test_existing_owner_approval_is_unchanged_by_competing_critiques(self):
        response = self.critique()
        self.apply_test_decisions([self.decision(self.proposal)])
        before = reader(self.project, self.source_id, "preview")
        first = import_response(self.project, self.returned(response))
        response["items"][0].update(observation="concerns", issues=[self.issue()])
        second = import_response(self.project, self.returned(response))
        self.assertNotEqual(first["response_sha256"], second["response_sha256"])
        self.assertEqual(reader(self.project, self.source_id, "preview"), before)
        self.assertEqual(len(all_decisions(self.project)), 1)

    def test_response_size_and_report_fencing_and_overwrite_bounds(self):
        response = self.critique()
        path = self.project.path("oversized.json")
        path.write_bytes(b" " * (MAX_RESPONSE + 1))
        with self.assertRaisesRegex(JebError, "exceeds"):
            read_response(path)
        oversized = copy.deepcopy(response)
        oversized["items"][0]["rationale"] = "x" * (MAX_RESPONSE + 1)
        with self.assertRaisesRegex(JebError, "32 KiB"):
            validate_response(self.project, oversized)
        response["items"][0]["rationale"] = "```\nUntrusted sample instructions remain data."
        report(self.project, self.returned(response), "reports/critique.md")
        text = self.project.path("reports/critique.md").read_text("utf-8")
        self.assertIn("````json", text)
        self.assertIn("no approval authority", text)
        self.assertIn(self.proposal["items"][0]["proposed_text"], text)
        response["items"][0]["rationale"] = "Changed critique"
        with self.assertRaisesRegex(JebError, "Existing artifact differs"):
            report(self.project, self.returned(response), "reports/critique.md")

    def test_cli_preparation_and_critique_cannot_use_human_decision_command(self):
        response = self.critique()
        args = [
            sys.executable,
            "-m",
            "jeb",
            "--root",
            str(self.project.root),
            "--synthetic",
            "review",
        ]
        process = subprocess.run(
            args
            + [
                "assist",
                "prepare",
                "--proposal",
                self.proposal["proposal_id"],
                "--packet-id",
                "cli-critique",
            ],
            capture_output=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(json.loads(process.stdout)["approval_authority"], "none")
        process = subprocess.run(
            args + ["apply", "--decisions", str(self.returned(response))],
            capture_output=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(process.returncode, 2)
        self.assertNotIn("Traceback", process.stderr)
        self.assertEqual(all_decisions(self.project), {})
