"""Persistent unreviewed v3 knowledge with original offline text only."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

from jeb.bank import backup, evidence, references, storage
from jeb.bank.validation import show_record, validate_bank
from jeb.core import JebError, canonical


class PersistentEvidenceTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.root = self.base / "bank"
        storage.initialize(self.root, "Originalni probni prostor v3", "3.0")
        self.common = {"visibility": "private", "processing_state": "inbox"}
        self.entity_input = {
            **self.common,
            "kind": "entity",
            "title": "Probni predmet",
            "data": {"entity_type": "concept"},
        }
        self.entity = self.save(self.entity_input)
        self.body = "Čitanje.\r\nsvjet vrjeme covik razumit\r\n"
        self.source_input = {
            **self.common,
            "kind": "source",
            "title": "Originalni probni izvor",
            "data": {
                "source_type": "document",
                "creator": "Autor probnih podataka",
                "translator": None,
                "edition": "Probno izdanje",
                "url": None,
                "accessed_at": None,
                "limitations": "Originalni test, nije historijski dokaz.",
            },
        }
        self.source = self.save(self.source_input, body=self.body)
        self.claim_input = {
            **self.common,
            "kind": "claim",
            "title": "Probna tvrdnja",
            "data": {
                "subject": self.ref(self.entity),
                "statement": "Probni dokument sadrzi oznacenu rijec.",
                "category": "source_statement",
                "limitations": "Samo originalni test.",
                "review_state": "unreviewed",
            },
        }
        self.claim = self.save(self.claim_input)
        self.evidence_input = {
            **self.common,
            "kind": "evidence",
            "title": "Probni dokaz",
            "data": {
                "claim": self.ref(self.claim),
                "source": self.ref(self.source),
                "relation": "supports",
                "locator": {"type": "text_span", "start": 10, "end": 15, "exact": "svjet"},
                "rationale": "Doslovni raspon originalnog probnog teksta.",
                "limitations": "Ne dokazuje historijski dogadjaj.",
                "review_state": "unreviewed",
            },
        }
        self.evidence = self.save(self.evidence_input)

    def save(self, content, body=None, prior=None):
        return storage.save_record(
            self.root,
            content,
            "test-tool",
            "tool",
            "Originalna probna promjena",
            body,
            prior["id"] if prior else None,
            prior["revision_id"] if prior else None,
        )

    def ref(self, result):
        return references.record_reference(self.root, result["id"], result["revision_id"])

    def test_create_read_exact_references_and_links(self):
        self.assertEqual(validate_bank(self.root)["valid_records"], 4)
        record = show_record(self.root, self.evidence["id"])["record"]
        self.assertEqual(record["schema_version"], "3.0")
        self.assertEqual(record["data"]["source"], self.ref(self.source))
        links = references.evidence_links(self.root, self.claim["id"])
        self.assertEqual(links["links"][0]["locator_verification"], "local_text_match")
        self.assertTrue(links["links"][0]["applies_to_current_claim"])
        self.assertEqual(links["approvals_created"], 0)

    def test_source_revision_change_keeps_old_text_binding_valid(self):
        old = self.ref(self.source)
        self.save(self.source_input, body="Drugi izvorni probni tekst\n", prior=self.source)
        self.assertEqual(validate_bank(self.root)["valid_records"], 4)
        links = references.evidence_links(self.root, self.claim["id"])["links"]
        self.assertFalse(links[0]["source_revision_matches_current"])
        self.assertTrue(links[0]["applies_to_current_claim"])
        self.assertEqual(links[0]["locator_verification"], "local_text_match")
        self.assertEqual(links[0]["source"], old)
        self.assertEqual(
            references.record_reference(self.root, self.source["id"], self.source["revision_id"]),
            old,
        )

    def test_claim_revision_does_not_inherit_old_support(self):
        changed = copy.deepcopy(self.claim_input)
        changed["data"]["statement"] = "Druga originalna probna tvrdnja."
        revised = self.save(changed, prior=self.claim)
        link = references.evidence_links(self.root, self.claim["id"])["links"][0]
        self.assertFalse(link["applies_to_current_claim"])
        self.assertEqual(link["claim"]["revision_id"], self.claim["revision_id"])
        self.assertEqual(
            storage.history(self.root, self.claim["id"])["revisions"][-1]["record"]["revision_id"],
            revised["revision_id"],
        )

    def test_explicit_evidence_revision_can_bind_new_claim(self):
        revised = self.save(self.claim_input, prior=self.claim)
        changed = copy.deepcopy(self.evidence_input)
        changed["data"]["claim"] = self.ref(revised)
        self.save(changed, prior=self.evidence)
        self.assertTrue(
            references.evidence_links(self.root, self.claim["id"])["links"][0][
                "applies_to_current_claim"
            ]
        )
        self.assertEqual(len(storage.history(self.root, self.evidence["id"])["revisions"]), 2)

    def test_wrong_hash_revision_kind_and_foreign_refs_fail_without_head_change(self):
        before = storage.head_at(self.root)
        for field, value in (
            ("record_sha256", "0" * 64),
            ("body_sha256", "0" * 64),
            ("revision_id", str(uuid4())),
            ("record_id", str(uuid4())),
        ):
            changed = copy.deepcopy(self.evidence_input)
            changed["data"]["source"][field] = value
            with self.subTest(field=field), self.assertRaises(JebError):
                self.save(changed)
            self.assertEqual(storage.head_at(self.root), before)
        changed = copy.deepcopy(self.evidence_input)
        changed["data"]["source"] = self.ref(self.entity)
        with self.assertRaisesRegex(JebError, "requires source"):
            self.save(changed)

    def test_mismatched_span_and_declared_locators(self):
        changed = copy.deepcopy(self.evidence_input)
        changed["data"]["locator"]["exact"] = "svijet"
        with self.assertRaisesRegex(JebError, "exact source"):
            self.save(changed)
        for locator in (
            {"type": "page", "pdf_page": 3, "printed_page": None, "note": "Deklarirano."},
            {"type": "section", "label": "Probni odjeljak", "note": "Deklarirano."},
            {"type": "time_range", "start_ms": 0, "end_ms": 1, "note": "Deklarirano."},
        ):
            changed["data"]["locator"] = locator
            self.save(changed)
        statuses = references.evidence_links(self.root, self.claim["id"])["links"]
        self.assertEqual(
            sum(item["locator_verification"] == "declared_only" for item in statuses), 3
        )

    def test_approval_fields_and_extra_body_rejected(self):
        for field, value in (("review_state", "approved"), ("human_attestation", True)):
            changed = copy.deepcopy(self.claim_input)
            changed["data"][field] = value
            with self.assertRaises(JebError):
                self.save(changed)
        with self.assertRaises(JebError):
            self.save(self.claim_input, body="Nedopusteno dodatno tijelo\n")

    def test_v2_default_still_rejects_new_kinds_and_keeps_bytes(self):
        root = self.base / "v2"
        storage.initialize(root, "Stari format po zadanim pravilima")
        before = (root / "HEAD.json").read_bytes()
        with self.assertRaises(JebError):
            storage.save_record(root, self.claim_input, "test-tool", "tool", "Originalni test")
        self.assertEqual((root / "HEAD.json").read_bytes(), before)
        self.assertEqual(storage.layout(root)["schema_version"], "2.0")

    def test_v3_backup_restore_retains_historical_reference_graph(self):
        self.save(self.source_input, body=None, prior=self.source)
        output = self.base / "backup.zip"
        backup.create(self.root, output)
        self.assertTrue(backup.verify(output)["valid_backup"])
        destination = self.base / "restored"
        backup.restore(output, destination)
        self.assertEqual(validate_bank(destination)["valid_records"], 4)
        self.assertEqual(
            references.evidence_links(self.root, self.claim["id"]),
            references.evidence_links(destination, self.claim["id"]),
        )
        self.assertEqual(
            references.record_reference(destination, self.source["id"], self.source["revision_id"]),
            self.ref(self.source),
        )

    def test_v2_draft_packet_cannot_be_mislabeled_from_v3(self):
        draft = {
            "schema_version": "1.0",
            "claims": [
                {
                    "id": str(uuid4()),
                    "subject_id": self.entity["id"],
                    "statement": "Originalna probna tvrdnja.",
                    "category": "source_statement",
                    "limitations": "Samo test.",
                }
            ],
            "evidence": [],
        }
        path = self.base / "draft.json"
        path.write_bytes(canonical(draft))
        output = self.base / "packet.json"
        with self.assertRaisesRegex(JebError, "require format2.0"):
            evidence.prepare(self.root, path, output, "test-tool", "tool")
        self.assertFalse(output.exists())

    def test_interrupted_evidence_commit_can_recover_with_reference_validation(self):
        with patch.object(storage, "publish_head", side_effect=OSError("interruption")):
            with self.assertRaises(OSError):
                self.save(self.evidence_input)
        self.assertEqual(validate_bank(self.root)["valid_records"], 4)
        pending = storage.recover(self.root)["pending"]
        candidate = next(item for item in pending if item["status"] == "prepared")
        storage.recover(self.root, candidate["name"])
        self.assertEqual(validate_bank(self.root)["valid_records"], 5)

    def test_contradiction_stays_independent_of_support(self):
        changed = copy.deepcopy(self.evidence_input)
        changed["data"]["relation"] = "contradicts"
        self.save(changed)
        links = references.evidence_links(self.root, self.claim["id"])
        self.assertEqual({item["relation"] for item in links["links"]}, {"supports", "contradicts"})
        self.assertEqual(links["review_state"], "unreviewed")

    def test_reference_rejects_missing_revision_and_invalid_ids(self):
        for identity, revision in (
            (self.claim["id"], str(uuid4())),
            ("../escape", None),
            (self.claim["id"], ""),
        ):
            with self.assertRaises(JebError):
                references.record_reference(self.root, identity, revision)

    def test_cli_v3_init_reference_create_and_links(self):
        root = self.base / "cli-bank"
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "jeb",
                "bank",
                "init",
                "--bank-root",
                str(root),
                "--title",
                "Originalni CLI test",
                "--format",
                "3.0",
            ],
            capture_output=True,
            timeout=20,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        for operation in (
            ["reference", self.source["id"], "--revision", self.source["revision_id"]],
            ["evidence", "links", self.claim["id"]],
        ):
            result = subprocess.run(
                [sys.executable, "-m", "jeb", "bank", *operation, "--bank-root", str(self.root)],
                capture_output=True,
                timeout=20,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIsInstance(json.loads(result.stdout), dict)


if __name__ == "__main__":
    unittest.main()
