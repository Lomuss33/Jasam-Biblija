import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from jeb.bank import migration, storage
from jeb.core import JebError, json_loads


class BankMigrationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "bank"
        storage.initialize(self.root, "Originalni dry-run prostor")

    def tearDown(self):
        self.temp.cleanup()

    def test_plan_is_bound_and_does_not_write_bank(self):
        item = {
            "kind": "source",
            "title": "Probni izvor",
            "data": {
                "source_type": "document",
                "creator": "Probni autor",
                "translator": None,
                "edition": "Probno izdanje",
                "url": None,
                "accessed_at": None,
                "limitations": "Samo test.",
            },
            "visibility": "private",
            "processing_state": "inbox",
        }
        storage.save_record(self.root, item, "test", "tool", "Dodaj probni izvor")
        before = (self.root / "HEAD.json").read_bytes()
        report = migration.plan(self.root)
        self.assertEqual(report["mode"], "dry_run")
        self.assertEqual(report["source_format"], "2.0")
        self.assertFalse(report["writable"])
        self.assertEqual(report["counts"]["claims"], 0)
        self.assertEqual(report["external_inputs"]["f3a_packets"], "excluded")
        self.assertEqual(report["counts"]["copy"], 1)
        self.assertEqual((self.root / "HEAD.json").read_bytes(), before)

    def test_output_must_be_external_and_no_clobber(self):
        inside = self.root / "plan.json"
        with self.assertRaises(JebError):
            migration.write_plan(self.root, inside)
        outside = Path(self.temp.name) / "plan.json"
        migration.write_plan(self.root, outside)
        with self.assertRaises(JebError):
            migration.write_plan(self.root, outside)
        self.assertEqual(json_loads(outside.read_bytes())["mode"], "dry_run")

    def test_v3_source_is_rejected(self):
        v3 = Path(self.temp.name) / "v3"
        storage.initialize(v3, "Probni v3 prostor", "3.0")
        with self.assertRaises(JebError):
            migration.plan(v3)

    def test_stale_plan_is_rejected_after_source_head_changes(self):
        output = Path(self.temp.name) / "plan.json"
        migration.write_plan(self.root, output)
        storage.save_record(
            self.root,
            {
                "kind": "entity",
                "title": "Novi probni predmet",
                "data": {"entity_type": "concept"},
                "visibility": "private",
                "processing_state": "inbox",
            },
            "test",
            "tool",
            "Promijeni v2 HEAD nakon plana",
        )
        with self.assertRaises(JebError):
            migration.verify_plan(self.root, output)

    def test_blocked_record_is_reported_without_target_identity(self):
        storage.save_record(
            self.root,
            {
                "kind": "source",
                "title": "Sintetički blokirani izvor",
                "data": {
                    "source_type": "document",
                    "creator": "Probni autor",
                    "translator": None,
                    "edition": "Probno izdanje",
                    "url": None,
                    "accessed_at": None,
                    "limitations": "Samo test.",
                },
                "visibility": "private",
                "processing_state": "inbox",
            },
            "test",
            "tool",
            "Sintetički blocker",
        )
        with patch.object(migration, "SUPPORTED_KINDS", ("entity", "article")):
            report = migration.plan(self.root)
        row = report["records"][0]
        self.assertEqual(row["action"], "blocked")
        self.assertIsNone(row["target_record_id"])
        self.assertEqual(row["target_revision_ids"], [])
        self.assertEqual(report["counts"]["blocked"], 1)


if __name__ == "__main__":
    unittest.main()
