from __future__ import annotations

import copy
import json
import subprocess
import sys
from unittest.mock import patch

from jeb.core import JebError, Project, digest, read_json, read_yaml, write_json
from jeb.corpus import rebuild
from jeb.source_assessment import CHECKS, historical_gaps, inspect_source, load_assessment
from jeb.sources import admitted, audit
from tests.support import REPO, WorkspaceTest


class SourceAssessmentTests(WorkspaceTest):
    def historical_fixture(self):
        """Simulated historical gate input in a temporary synthetic test project only."""
        registry = read_yaml(self.project.path("sources/registry.yaml"))
        source = registry["sources"][0]
        source["kind"] = "historical"
        source["download_urls"] = ["https://example.invalid/synthetic-test.txt"]
        source["edition"].update(
            year="1900 (synthetic test)",
            publication_place="TEST PLACE",
            transcriber="TEST FIXTURE ONLY",
        )
        write_json(self.project.path("sources/registry.yaml"), registry)
        locks = read_json(self.project.path("sources/lock.json"))
        locks["sources"][0]["source_record_sha256"] = digest(source)
        locks["sources"][0]["download_url"] = source["download_urls"][0]
        write_json(self.project.path("sources/lock.json"), locks)
        self.project.synthetic = False
        return source

    def assessment(self, source, status="unresolved"):
        return {
            "schema_version": "1.0",
            "source_id": source["source_id"],
            "source_record_sha256": digest(source),
            "checked_at": "2026-10-30",
            "assessor": "Synthetic test, no real rights assessment or review",
            "checks": {
                name: {
                    "status": status,
                    "summary": "Synthetic test evidence only",
                    "evidence_ids": ["test-evidence"],
                }
                for name in CHECKS
            },
            "evidence": [
                {
                    "evidence_id": "test-evidence",
                    "category": "provider_metadata",
                    "url": "urn:jeb:synthetic:metadata",
                    "locator": "Synthetic fixture declaration",
                    "access_date": "2026-10-30",
                    "summary": "Synthetic assertion, no external review",
                    "snapshot": None,
                }
            ],
            "module_metadata": None,
            "unresolved_questions": [],
        }

    def save(self, assessment):
        write_json(self.project.path(f"sources/assessments/{self.source_id}.json"), assessment)

    def test_production_inspection_explains_real_gaps_without_download(self):
        with patch("urllib.request.urlopen", side_effect=AssertionError("Must be offline")):
            result = inspect_source(Project(REPO), "crosswire-srkdijekav")
        codes = {g["code"] for g in result["admission_blockers"]}
        self.assertFalse(result["admitted"])
        self.assertIn("missing_edition_year", codes)
        self.assertIn("unresolved_digital_provenance", codes)
        self.assertIn("unresolved_adapter", codes)
        self.assertIn("missing_lock", codes)
        self.assertIsNone(result["source_artifact"]["sha256"])
        self.assertEqual(
            result["assessment"]["module_metadata"]["declared_fields"]["Versification"], "Calvin"
        )

    def test_metadata_hash_does_not_clear_or_lock_a_corpus(self):
        source = read_yaml(REPO / "sources/registry.yaml")["sources"][0]
        assessment = load_assessment(Project(REPO), source)
        self.assertEqual(assessment["module_metadata"]["size_bytes"], 910)
        self.assertIsNone(source["artifact"]["sha256"])
        self.assertEqual(read_json(REPO / "sources/lock.json")["sources"], [])
        with self.assertRaisesRegex(JebError, "needs_review"):
            admitted(Project(REPO), source["source_id"])

    def test_synthetic_demo_does_not_need_a_historical_assessment(self):
        result = inspect_source(self.project, self.source_id)
        self.assertTrue(result["admitted"])
        self.assertEqual(result["admission_blockers"], [])
        self.assertIsNone(result["assessment"])

    def test_audit_rejects_orphan_assessment(self):
        write_json(self.project.path("sources/assessments/not-registered.json"), {})
        with self.assertRaisesRegex(JebError, "Orphan source assessment"):
            audit(self.project)

    def test_status_and_hash_alone_cannot_admit_undocumented_historical_source(self):
        source = self.historical_fixture()
        with self.assertRaisesRegex(JebError, "missing_source_assessment"):
            admitted(self.project, self.source_id)
        self.save(self.assessment(source))
        with self.assertRaisesRegex(JebError, "unresolved_exact_edition"):
            admitted(self.project, self.source_id)

    def test_missing_edition_and_provenance_fields_remain_blocking(self):
        source = self.historical_fixture()
        source["edition"]["transcriber"] = None
        registry = read_yaml(self.project.path("sources/registry.yaml"))
        registry["sources"][0] = source
        write_json(self.project.path("sources/registry.yaml"), registry)
        self.save(self.assessment(source, status="verified"))
        self.assertIn(
            "missing_edition_transcriber",
            {g["code"] for g in historical_gaps(self.project, source)},
        )

    def test_complete_simulated_evidence_can_pass_structural_gate_without_legal_claim(self):
        source = self.historical_fixture()
        self.save(self.assessment(source, status="verified"))
        self.assertEqual(admitted(self.project, self.source_id)[0], source)

    def test_registry_edit_invalidates_assessment(self):
        source = self.historical_fixture()
        self.save(self.assessment(source))
        changed = copy.deepcopy(source)
        changed["edition"]["transcriber"] = "Changed synthetic fixture identity"
        with self.assertRaisesRegex(JebError, "stale"):
            load_assessment(self.project, changed)

    def test_dangling_duplicate_and_unbacked_evidence_rejected(self):
        source = self.historical_fixture()
        original = self.assessment(source, status="verified")
        variants = []
        dangling = copy.deepcopy(original)
        dangling["checks"]["exact_edition"]["evidence_ids"] = ["invented-source"]
        variants.append(dangling)
        duplicate = copy.deepcopy(original)
        duplicate["evidence"].append(duplicate["evidence"][0])
        variants.append(duplicate)
        unbacked = copy.deepcopy(original)
        unbacked["checks"]["adapter"]["evidence_ids"] = []
        variants.append(unbacked)
        for value in variants:
            self.save(value)
            with self.subTest(value=value), self.assertRaises(JebError):
                load_assessment(self.project, source)

    def test_snapshot_path_and_hash_mismatch_rejected(self):
        source = self.historical_fixture()
        value = self.assessment(source)
        value["evidence"][0]["snapshot"] = {
            "sha256": "1" * 64,
            "size_bytes": 10,
            "content_scope": "metadata_only",
            "private_cache_path": "../escape",
        }
        self.save(value)
        with self.assertRaises(JebError):
            load_assessment(self.project, source)
        value["evidence"][0]["snapshot"]["private_cache_path"] = None
        value["module_metadata"] = {
            "module_id": "Synthetic",
            "url": "urn:jeb:synthetic:metadata",
            "sha256": "2" * 64,
            "size_bytes": 10,
            "declared_fields": {},
        }
        self.save(value)
        with self.assertRaisesRegex(JebError, "matching evidence snapshot"):
            load_assessment(self.project, source)

    def test_transcript_cannot_relabel_the_assessed_versification(self):
        raw = self.raw().replace(b'"scheme":"synthetic-test-v1"', b'"scheme":"unreviewed-scheme"')
        self.rewrite_fixture(raw)
        with self.assertRaisesRegex(JebError, "versification differs"):
            rebuild(self.project, self.source_id, normalized=False)

    def test_declared_versification_mismatch_is_not_silently_adopted(self):
        source = self.historical_fixture()
        value = self.assessment(source)
        value["evidence"][0]["snapshot"] = {
            "sha256": "1" * 64,
            "size_bytes": 10,
            "content_scope": "metadata_only",
            "private_cache_path": None,
        }
        value["module_metadata"] = {
            "module_id": "Synthetic",
            "url": "urn:jeb:synthetic:metadata",
            "sha256": "1" * 64,
            "size_bytes": 10,
            "declared_fields": {"Versification": "wrong-scheme"},
        }
        self.save(value)
        with self.assertRaisesRegex(JebError, "versification disagree"):
            load_assessment(self.project, source)

    def test_inspection_cli_is_read_only_and_reports_blocking_status(self):
        before = (REPO / "sources/registry.yaml").read_bytes()
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "jeb",
                "--root",
                str(REPO),
                "sources",
                "inspect",
                "--source",
                "crosswire-srkdijekav",
            ],
            capture_output=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(json.loads(result.stdout)["admitted"])
        self.assertEqual((REPO / "sources/registry.yaml").read_bytes(), before)
