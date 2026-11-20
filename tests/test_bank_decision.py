import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from jeb.bank import decision, migration, storage
from jeb.core import JebError, atomic_write, canonical, sha256


class BankDecisionTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.root = self.base / "bank"
        self.plan_path = self.base / "plan.json"
        self.target = self.base / "new-v3-bank"
        storage.initialize(self.root, "Originalni decision test prostor")
        migration.write_plan(self.root, self.plan_path)

    def tearDown(self):
        self.temp.cleanup()

    def _decision(self, **changes):
        plan = migration.plan(self.root)
        value = {
            "schema_version": "1.0",
            "decision_id": str(uuid4()),
            "decision": "proceed",
            "actor": {"id": "synthetic-test-owner", "kind": "human", "role": "owner"},
            "decided_at": datetime.now(timezone.utc).isoformat(),
            "plan_sha256": sha256(self.plan_path.read_bytes()),
            "source_workspace_id": plan["source_workspace_id"],
            "source_head": plan["source_head"],
            "source_records_sha256": plan["source_records_sha256"],
            "target_path": str(self.target),
            "f3a_packets": "excluded",
            "approval_authority": "owner_decision",
            "notes": "Sintetički testni zapis; nije stvarna odluka vlasnika.",
        }
        value.update(changes)
        return value

    def _write_decision(self, value):
        path = self.base / "decision.json"
        atomic_write(path, canonical(value), replace=False)
        return path

    def test_valid_synthetic_decision_is_only_a_binding_check(self):
        result = decision.validate(
            self.root, self.plan_path, self._write_decision(self._decision())
        )
        self.assertTrue(result["valid_decision"])
        self.assertTrue(result["can_write"])
        self.assertEqual(result["approvals_created"], 0)
        self.assertFalse(self.target.exists())

    def test_plan_hash_mismatch_fails_closed(self):
        value = self._decision(plan_sha256="0" * 64)
        with self.assertRaises(JebError):
            decision.validate(self.root, self.plan_path, self._write_decision(value))

    def test_existing_target_fails_before_any_write(self):
        self.target.mkdir()
        with self.assertRaises(JebError):
            decision.validate(self.root, self.plan_path, self._write_decision(self._decision()))


if __name__ == "__main__":
    unittest.main()
