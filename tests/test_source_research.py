from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from jeb.core import JebError, Project, digest, read_json, read_yaml, write_json
from jeb.source_assessment import inspect_source
from jeb.source_research import (
    MAX_RESPONSE,
    current_packet,
    import_response,
    prepare,
    read_response,
    report,
    validate_response,
)
from tests.support import REPO


class SourceResearchTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        shutil.copytree(REPO / "config", self.root / "config")
        shutil.copytree(
            REPO / "sources", self.root / "sources", ignore=shutil.ignore_patterns("private")
        )
        (self.root / "docs").mkdir()
        shutil.copyfile(REPO / "docs/RIGHTS_POLICY.md", self.root / "docs/RIGHTS_POLICY.md")
        self.project = Project(self.root)
        self.source = "crosswire-srkdijekav"
        self.packet_id = "source-metadata-test"

    def response(self):
        packet = prepare(self.project, self.source, self.packet_id)
        return {
            "schema_version": "1.0",
            "packet_id": self.packet_id,
            "source_id": self.source,
            "packet_sha256": packet["packet_sha256"],
            "tool": {
                "name": "Synthetic metadata response fixture; no real research or human sign-off",
                "model_identifier": None,
                "reported_at": "2026-10-30",
            },
            "items": [
                {
                    "question_id": question["question_id"],
                    "outcome": "no_new_evidence",
                    "summary": "Synthetic response fixture only; question remains unresolved.",
                    "known_evidence_ids": [],
                    "lead_ids": [],
                    "limitations": "No actual evidence inspected by this automated test.",
                }
                for question in packet["questions"]
            ],
            "leads": [],
            "review_state": "unreviewed",
            "corpus_permission": False,
        }

    def with_lead(self):
        response = self.response()
        response["leads"] = [
            {
                "lead_id": "synthetic-lead",
                "url": "https://example.invalid/synthetic-metadata",
                "locator": "Synthetic example; no live request is made",
                "access_date": "2026-10-30",
                "summary": "Original synthetic metadata, not an actual source witness.",
                "relationship": "unknown",
            }
        ]
        response["items"][1].update(outcome="leads_found", lead_ids=["synthetic-lead"])
        return response

    def test_uncleared_source_packet_is_deterministic_metadata_only(self):
        with patch("urllib.request.urlopen", side_effect=AssertionError("No network")):
            first = prepare(self.project, self.source, self.packet_id)
            second = prepare(self.project, self.source, self.packet_id)
        self.assertEqual(first, second)
        self.assertFalse(first["corpus_permission"])
        self.assertFalse(first["contact_authorized"])
        self.assertFalse(first["scripture_payload_included"])
        self.assertEqual(len(first["questions"]), 5)
        self.assertEqual(first["source_snapshot"]["status"], "needs_review")
        self.assertNotIn("segments", first)
        self.assertFalse(self.project.path("data/raw").exists())

    def test_unknown_source_and_unsafe_ids_fail_without_outputs(self):
        for source, packet in (
            ("invented", "safe-id"),
            (self.source, "../escape"),
            (self.source, "CON"),
        ):
            with self.subTest(source=source, packet=packet), self.assertRaises(JebError):
                prepare(self.project, source, packet)
        self.assertFalse(self.project.path("data/source-research").exists())

    def test_missing_dossier_is_not_invented(self):
        with self.assertRaisesRegex(JebError, "dossier"):
            prepare(self.project, "ebible-srp1865", self.packet_id)

    def test_oversized_response_is_refused_before_parsing_or_import(self):
        path = self.project.path("oversized.json")
        path.write_bytes(b" " * (MAX_RESPONSE + 1))
        with self.assertRaisesRegex(JebError, "exceeds"):
            read_response(path)
        response = self.response()
        response["items"][0]["summary"] = "x" * (MAX_RESPONSE + 1)
        with self.assertRaisesRegex(JebError, "24 KiB"):
            validate_response(self.project, response)

    def test_packet_hash_and_resealed_prompt_or_schema_substitution_rejected(self):
        packet = prepare(self.project, self.source, self.packet_id)
        target = self.project.path(f"data/source-research/{self.packet_id}/input.json")
        changed = copy.deepcopy(packet)
        changed["prompt"] = "Modified prompt"
        write_json(target, changed)
        with self.assertRaisesRegex(JebError, "hash changed"):
            current_packet(self.project, self.packet_id)
        for field in ("prompt", "output_schema"):
            changed = copy.deepcopy(packet)
            changed[field] = "Modified prompt" if field == "prompt" else {"type": "string"}
            changed["packet_sha256"] = digest(
                {k: v for k, v in changed.items() if k != "packet_sha256"}
            )
            write_json(target, changed)
            with self.subTest(field=field), self.assertRaisesRegex(JebError, "substituted"):
                current_packet(self.project, self.packet_id)

    def test_changed_dossier_scope_or_policy_invalidates_packet(self):
        response = self.response()
        paths = [
            self.project.path(f"sources/assessments/{self.source}.json"),
            self.project.path("docs/RIGHTS_POLICY.md"),
            self.project.path("config/edition.yaml"),
        ]
        for path in paths:
            original = path.read_bytes()
            if path.suffix == ".json":
                value = read_json(path)
                value["checks"]["digital_provenance"]["summary"] += " Changed test observation."
                write_json(path, value)
            elif path.suffix == ".yaml":
                value = read_yaml(path)
                value["jurisdictions"] = ["DE", "US"]
                write_json(path, value)
            else:
                path.write_bytes(original + b"\nChanged synthetic test policy.\n")
            try:
                with self.subTest(path=path.name), self.assertRaisesRegex(JebError, "Stale"):
                    validate_response(self.project, response)
            finally:
                path.write_bytes(original)

    def test_changed_registry_makes_assessment_stale(self):
        response = self.response()
        path = self.project.path("sources/registry.yaml")
        value = read_yaml(path)
        value["sources"][0]["title"] += " Changed metadata"
        write_json(path, value)
        with self.assertRaisesRegex(JebError, "stale"):
            validate_response(self.project, response)

    def test_missing_duplicate_reordered_or_invented_questions_rejected(self):
        original = self.response()
        for items in (
            original["items"][:-1],
            list(reversed(original["items"])),
            [original["items"][0]] * 5,
        ):
            response = copy.deepcopy(original)
            response["items"] = items
            with self.subTest(items=items), self.assertRaises(JebError):
                validate_response(self.project, response)
        original["items"][0]["question_id"] = "PS"
        with self.assertRaises(JebError):
            validate_response(self.project, original)

    def test_dangling_or_fabricated_evidence_and_unreferenced_leads_rejected(self):
        original = self.with_lead()
        variants = []
        response = copy.deepcopy(original)
        response["items"][0]["known_evidence_ids"] = ["invented-evidence"]
        variants.append(response)
        response = copy.deepcopy(original)
        response["items"][1]["lead_ids"] = ["invented-lead"]
        variants.append(response)
        response = copy.deepcopy(original)
        response["items"][1].update(outcome="no_new_evidence", lead_ids=[])
        variants.append(response)
        for response in variants:
            with self.subTest(response=response), self.assertRaises(JebError):
                validate_response(self.project, response)

    def test_duplicate_shadowed_or_duplicate_url_leads_rejected(self):
        original = self.with_lead()
        for change in ("id", "url", "shadow"):
            response = copy.deepcopy(original)
            if change == "shadow":
                response["leads"][0]["lead_id"] = "cw-config"
            else:
                extra = copy.deepcopy(response["leads"][0])
                if change == "url":
                    extra["lead_id"] = "other-lead"
                response["leads"].append(extra)
            with self.subTest(change=change), self.assertRaises(JebError):
                validate_response(self.project, response)

    def test_unapproved_states_extra_fields_scripts_and_unsafe_urls_rejected(self):
        original = self.with_lead()
        for field, value in (
            ("review_state", "approved"),
            ("corpus_permission", True),
            ("approval", {"human_attestation": True}),
        ):
            response = copy.deepcopy(original)
            response[field] = value
            with self.subTest(field=field), self.assertRaises(JebError):
                validate_response(self.project, response)
        for url in (
            "file:///private",
            "javascript:alert(1)",
            "https://user:password@example.invalid/",
        ):
            response = copy.deepcopy(original)
            response["leads"][0]["url"] = url
            with self.subTest(url=url), self.assertRaises(JebError):
                validate_response(self.project, response)
        original["items"][0]["summary"] = "\u0410"
        with self.assertRaisesRegex(JebError, "display-script"):
            validate_response(self.project, original)

    def test_source_hash_outcome_and_date_mismatches_rejected(self):
        original = self.with_lead()
        for change in ("source", "hash", "outcome", "date"):
            response = copy.deepcopy(original)
            if change == "source":
                response["source_id"] = "ebible-srp1865"
            elif change == "hash":
                response["packet_sha256"] = "0" * 64
            elif change == "outcome":
                response["items"][1]["outcome"] = "no_new_evidence"
            else:
                response["leads"][0]["access_date"] = "2026-10-31"
            with self.subTest(change=change), self.assertRaises(JebError):
                validate_response(self.project, response)

    def test_import_is_unreviewed_duplicate_protected_and_cannot_change_admission(self):
        response = self.with_lead()
        path = self.project.path("returned.json")
        write_json(path, response)
        before = inspect_source(self.project, self.source)
        with patch("urllib.request.urlopen", side_effect=AssertionError("No network")):
            result = import_response(self.project, path)
        self.assertEqual(read_json(self.project.path(result["output"])), response)
        self.assertFalse(result["source_clearance_changed"])
        self.assertEqual(result["review_state"], "unreviewed")
        self.assertEqual(inspect_source(self.project, self.source), before)
        self.assertFalse(self.project.path("data/raw").exists())
        self.assertFalse(self.project.path("data/approved").exists())
        with self.assertRaisesRegex(JebError, "Duplicate"):
            import_response(self.project, path)
        response["items"][0]["summary"] += " Changed after import."
        write_json(self.project.path(result["output"]), response)
        with self.assertRaisesRegex(JebError, "content changed"):
            read_response(self.project.path(result["output"]))

    def test_review_report_fences_untrusted_content_and_preserves_existing_output(self):
        response = self.response()
        response["items"][0]["summary"] = (
            "```\nUntrusted sample instructions, not commands to execute."
        )
        path = self.project.path("returned.json")
        write_json(path, response)
        report(self.project, path, "review.md")
        text = self.project.path("review.md").read_text("utf-8")
        self.assertIn("````json", text)
        self.assertIn("unreviewed observations", text)
        response["items"][0]["summary"] = "Changed response"
        write_json(path, response)
        with self.assertRaisesRegex(JebError, "Existing artifact differs"):
            report(self.project, path, "review.md")

    def test_cli_prepares_without_source_clearance_and_reports_input_errors(self):
        args = [sys.executable, "-m", "jeb", "--root", str(self.root), "sources", "research"]
        process = subprocess.run(
            args + ["prepare", "--source", self.source, "--packet-id", self.packet_id],
            capture_output=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertFalse(json.loads(process.stdout)["corpus_permission"])
        invalid = self.project.path("invalid.json")
        invalid.write_text("{}", encoding="utf-8")
        process = subprocess.run(
            args + ["validate", "--input", str(invalid)],
            capture_output=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(process.returncode, 2)
        self.assertNotIn("Traceback", process.stderr)
