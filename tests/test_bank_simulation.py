import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

from jeb.bank import migration, simulation, storage
from jeb.core import JebError, atomic_write, canonical, sha256


class BankSimulationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.root = self.base / "v2-bank"
        self.plan_path = self.base / "plan.json"
        self.target = self.base / "synthetic-v3-bank"
        storage.initialize(self.root, "Sintetička baza za simulaciju")
        source = {
            "kind": "source",
            "title": "Sintetički izvor",
            "data": {
                "source_type": "document",
                "creator": "Sintetički autor",
                "translator": None,
                "edition": "Sintetičko izdanje",
                "url": None,
                "accessed_at": None,
                "limitations": "Nije historijski dokaz.",
            },
            "visibility": "private",
            "processing_state": "inbox",
        }
        self.source_result = storage.save_record(
            self.root, source, "synthetic-test", "tool", "Dodaj sintetički izvor", "svjet\n"
        )
        storage.save_record(
            self.root,
            {**source, "title": "Sintetički izvor druga revizija"},
            "synthetic-test",
            "tool",
            "Druga sintetička revizija",
            "svjet\nvrjeme\n",
            self.source_result["id"],
            self.source_result["revision_id"],
        )
        migration.write_plan(self.root, self.plan_path)

    def tearDown(self):
        self.temp.cleanup()

    def _write_decision(self):
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
            "notes": "Sintetička simulacija; nije stvarna odluka vlasnika.",
        }
        path = self.base / "decision.json"
        atomic_write(path, canonical(value), replace=False)
        return path

    def test_simulation_creates_marked_unreleasable_v3_copy(self):
        source_head_before = (self.root / "HEAD.json").read_bytes()
        result = simulation.simulate(
            self.root, self.plan_path, self._write_decision(), synthetic=True
        )
        self.assertTrue(result["synthetic"])
        self.assertFalse(result["releasable"])
        self.assertEqual(result["approvals_created"], 0)
        state = storage.read_managed(self.target)
        self.assertEqual(state["workspace"]["schema_version"], "3.0")
        self.assertIn("[SYNTHETIC MIGRATION]", state["workspace"]["title"])
        self.assertEqual(state["bodies"], {next(iter(state["bodies"])): "svjet\nvrjeme\n"})
        self.assertEqual(len(state["chain"]), 3)
        self.assertEqual(
            [snapshot["bodies"] for snapshot in reversed(state["chain"])],
            [
                {},
                {self.source_result["id"]: "svjet\n"},
                {self.source_result["id"]: "svjet\nvrjeme\n"},
            ],
        )
        self.assertEqual((self.root / "HEAD.json").read_bytes(), source_head_before)

    def test_simulation_requires_explicit_opt_in(self):
        with self.assertRaises(JebError):
            simulation.simulate(self.root, self.plan_path, self._write_decision())

    def test_validation_failure_cleans_only_owned_staging(self):
        decision_path = self._write_decision()
        with patch.object(simulation, "validate_bank", side_effect=JebError("synthetic failure")):
            with self.assertRaises(JebError):
                simulation.simulate(self.root, self.plan_path, decision_path, synthetic=True)
        self.assertFalse(self.target.exists())
        self.assertEqual(list(self.base.glob(".synthetic-v3-bank.staging-*")), [])


if __name__ == "__main__":
    unittest.main()
