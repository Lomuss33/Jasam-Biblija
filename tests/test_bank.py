"""Original offline data only; no historical claims or human attestations."""

from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from uuid import uuid4

from jeb.bank import validation
from jeb.core import JebError, canonical, sha256


class BankTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "bank"
        (self.root / "records").mkdir(parents=True)
        self.workspace_id = str(uuid4())
        self.put(
            self.root / "workspace.json",
            {
                "schema_version": "1.0",
                "workspace_id": self.workspace_id,
                "title": "Originalni probni prostor",
                "created_at": "2026-11-15T10:00:00Z",
            },
        )
        self.entity = self.record("entity", {"entity_type": "concept"})
        self.source = self.record(
            "source",
            {
                "source_type": "document",
                "creator": "Autor probnih podataka",
                "translator": None,
                "edition": None,
                "url": None,
                "accessed_at": None,
                "limitations": "Originalan test, nije historijski dokaz.",
            },
        )
        self.article = self.record(
            "article",
            {
                "subjects": [self.entity["id"]],
                "sources": [self.source["id"]],
            },
            "# Probni tekst\n\nsvjet vrjeme covik razumit\n",
        )

    def put(self, path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(canonical(value))

    def record(self, kind, data, body=None):
        value = {
            "schema_version": "1.0",
            "workspace_id": self.workspace_id,
            "id": str(uuid4()),
            "kind": kind,
            "title": "Probni zapis",
            "created_at": "2026-11-15T10:01:00Z",
            "recorded_by": {"id": "offline-test-tool", "kind": "tool"},
            "revision_id": str(uuid4()),
            "parent_revision": None,
            "body_sha256": None if body is None else sha256(body.encode("utf-8")),
            "visibility": "private",
            "processing_state": "inbox",
            "data": data,
        }
        self.save(value)
        if body is not None:
            (self.directory(value) / "body.md").write_bytes(body.encode("utf-8"))
        return value

    def directory(self, value):
        return self.root / "records" / value["id"]

    def save(self, value):
        self.put(self.directory(value) / "record.json", value)

    def assert_invalid(self, pattern):
        with self.assertRaisesRegex(JebError, pattern):
            validation.validate_bank(self.root)

    def test_valid_snapshot_is_read_only_and_deterministic(self):
        before = {str(p): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        result = validation.validate_bank(self.root)
        self.assertEqual(result["valid_records"], 3)
        self.assertEqual(result["approvals_created"], 0)
        self.assertEqual(result, validation.validate_bank(self.root))
        self.assertEqual(
            before, {str(p): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        )
        shown = validation.show_record(self.root, self.article["id"])
        self.assertIn("svjet vrjeme covik razumit", shown["body"])

    def test_cli_works_without_project_config(self):
        for operation, extra in (("validate", []), ("show", [self.article["id"]])):
            process = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "jeb",
                    "--root",
                    str(self.root),
                    "bank",
                    operation,
                    "--bank-root",
                    str(self.root),
                    *extra,
                ],
                capture_output=True,
            )
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertIsInstance(json.loads(process.stdout), dict)

    def test_unknown_version_and_unrecognized_approval_fields(self):
        for key, value in (("schema_version", "2.0"), ("human_attestation", True)):
            with self.subTest(key=key):
                changed = copy.deepcopy(self.entity)
                changed[key] = value
                self.save(changed)
                self.assert_invalid("bank-record schema")
        self.save(self.entity)

    def test_duplicate_json_key(self):
        path = self.directory(self.entity) / "record.json"
        path.write_text('{"id": "x", "id": "y"}', encoding="utf-8")
        self.assert_invalid("Duplicate key")

    def test_foreign_workspace_and_directory_mismatch(self):
        self.entity["workspace_id"] = str(uuid4())
        self.save(self.entity)
        self.assert_invalid("Foreign workspace")
        self.entity["workspace_id"] = self.workspace_id
        path = self.directory(self.entity) / "record.json"
        value = copy.deepcopy(self.entity)
        value["id"] = str(uuid4())
        self.put(path, value)
        self.assert_invalid("ID differs")

    def test_changed_missing_and_unbound_body(self):
        path = self.directory(self.article) / "body.md"
        path.write_text("changed", encoding="utf-8")
        self.assert_invalid("hash mismatch")
        path.unlink()
        self.assert_invalid("Missing body")
        self.article["body_sha256"] = None
        self.save(self.article)
        self.assert_invalid("bank-record schema")

    def test_unbound_entity_body(self):
        (self.directory(self.entity) / "body.md").write_text("unbound", encoding="utf-8")
        self.assert_invalid("Unbound body")

    def test_typed_and_missing_references(self):
        self.article["data"]["subjects"] = [self.source["id"]]
        self.save(self.article)
        self.assert_invalid("expected entity")
        self.article["data"]["subjects"] = [str(uuid4())]
        self.save(self.article)
        self.assert_invalid("missing target")

    def test_duplicate_revision(self):
        self.source["revision_id"] = self.entity["revision_id"]
        self.save(self.source)
        self.assert_invalid("Duplicate revision")

    def test_only_initial_revisions_supported(self):
        self.entity["parent_revision"] = str(uuid4())
        self.save(self.entity)
        self.assert_invalid("parent_revision")

    def test_no_paths_in_ids_or_extra_files(self):
        for bad in ("../record", "CON", self.entity["id"].upper()):
            with self.subTest(bad=bad):
                with self.assertRaises(JebError):
                    validation.show_record(self.root, bad)
        (self.root / "private").mkdir()
        self.assert_invalid("dedicated directory")

    def test_invalid_utf8_and_non_latin_display(self):
        (self.directory(self.entity) / "record.json").write_bytes(b"\xff")
        self.assert_invalid("utf-8")
        self.entity["title"] = "\u041f\u0440\u043e\u0431\u0430"
        self.save(self.entity)
        self.assert_invalid("display-script")

    def test_urls_are_inert_https_references(self):
        for bad in ("file:///private", "http://example.org", "https://a:b@example.org", "https://"):
            with self.subTest(url=bad):
                self.source["data"]["url"] = bad
                self.save(self.source)
                self.assert_invalid("HTTPS")
        self.source["data"]["url"] = "https://example.invalid/source"
        self.save(self.source)
        self.assertEqual(validation.validate_bank(self.root)["valid_records"], 3)

    def test_limits(self):
        from unittest.mock import patch

        with patch.object(validation, "MAX_RECORDS", 2):
            self.assert_invalid("Too many")
        with patch.object(validation, "MAX_TOTAL_BYTES", 10):
            self.assert_invalid("total byte limit")
        with patch.object(validation, "MAX_FILE_BYTES", 10):
            self.assert_invalid("exceeds")

    def test_links_rejected_when_available(self):
        link = self.root.parent / "linked-bank"
        try:
            os.symlink(self.root, link, target_is_directory=True)
        except OSError:
            self.skipTest("OS does not permit symlink creation")
        with self.assertRaisesRegex(JebError, "Linked bank path"):
            validation.validate_bank(link)

    def test_junction_and_link_guards_without_os_privileges(self):
        from unittest.mock import patch

        for method in ("is_junction", "is_symlink"):
            with self.subTest(method=method), patch.object(Path, method, return_value=True):
                with self.assertRaisesRegex(JebError, "Linked bank path"):
                    validation.validate_bank(self.root)

    def test_failed_validation_cli_has_no_success_payload(self):
        self.article["data"]["sources"] = [str(uuid4())]
        self.save(self.article)
        process = subprocess.run(
            [sys.executable, "-m", "jeb", "bank", "validate", "--bank-root", str(self.root)],
            capture_output=True,
        )
        self.assertEqual(process.returncode, 2)
        self.assertEqual(process.stdout, b"")
        self.assertIn(b"missing target", process.stderr)


if __name__ == "__main__":
    unittest.main()
