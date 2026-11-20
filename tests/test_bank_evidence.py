"""Original evidence drafts only; no historical text or human approvals."""

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

from jeb.bank import backup, evidence, storage
from jeb.core import JebError, canonical, digest


class BankEvidenceTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.root = self.base / "bank"
        storage.initialize(self.root, "Originalna probna baza dokaza")
        self.entity_content = {
            "kind": "entity",
            "title": "Probni predmet",
            "data": {"entity_type": "concept"},
            "visibility": "private",
            "processing_state": "inbox",
        }
        self.subject = storage.save_record(
            self.root, self.entity_content, "test-tool", "tool", "Originalni predmet"
        )
        self.source_content = {
            "kind": "source",
            "title": "Originalni probni dokument",
            "data": {
                "source_type": "document",
                "creator": "Autor probnih podataka",
                "translator": None,
                "edition": "Originalni test, prvo izdanje",
                "url": None,
                "accessed_at": None,
                "limitations": "Izmisljeno za offline test, nije historijski izvor.",
            },
            "visibility": "private",
            "processing_state": "inbox",
        }
        self.body = "Čitanje.\r\nsvjet vrjeme covik razumit\r\n"
        self.source = storage.save_record(
            self.root, self.source_content, "test-tool", "tool", "Originalni dokument", self.body
        )
        self.claim_id, self.evidence_id = str(uuid4()), str(uuid4())
        self.draft = {
            "schema_version": "1.0",
            "claims": [
                {
                    "id": self.claim_id,
                    "subject_id": self.subject["id"],
                    "statement": "Probni dokument sadrzi oznacene rijeci.",
                    "category": "source_statement",
                    "limitations": "Originalni tehnicki primjer.",
                }
            ],
            "evidence": [
                {
                    "id": self.evidence_id,
                    "claim_id": self.claim_id,
                    "source_id": self.source["id"],
                    "relation": "supports",
                    "locator": {"type": "text_span", "start": 10, "end": 15, "exact": "svjet"},
                    "rationale": "Izravna provjera probnog teksta.",
                    "limitations": "Ne dokazuje stvarni historijski dogadjaj.",
                }
            ],
        }
        self.input, self.output = self.base / "draft.json", self.base / "packet.json"

    def prepare(self, draft=None, output=None):
        self.input.write_bytes(canonical(draft or self.draft))
        return evidence.prepare(self.root, self.input, output or self.output, "test-tool", "tool")

    def packet(self):
        return storage.document(self.output)

    def rewrite(self, packet, reseal=False):
        if reseal:
            packet["packet_sha256"] = digest(
                {k: v for k, v in packet.items() if k != "packet_sha256"}
            )
        self.output.write_bytes(canonical(packet))

    def test_prepare_validate_inspect_and_no_bank_changes(self):
        before = {str(p): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        result = self.prepare()
        checked = evidence.validate(self.root, self.output)
        self.assertEqual(result["packet_sha256"], checked["packet_sha256"])
        self.assertEqual(checked["evidence"][0]["locator_verification"], "local_text_match")
        self.assertEqual(checked["claims_without_evidence"], [])
        self.assertEqual(checked["approvals_created"], 0)
        view = evidence.inspect(self.root, self.output)
        self.assertEqual(
            view["bound_records"][self.source["id"]]["data"]["creator"], "Autor probnih podataka"
        )
        self.assertEqual(view["packet"]["draft"]["evidence"][0]["locator"]["exact"], "svjet")
        self.assertEqual(
            before, {str(p): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        )

    def test_page_section_and_time_are_declared_not_verified(self):
        for locator in (
            {
                "type": "page",
                "pdf_page": 7,
                "printed_page": "iv",
                "note": "Probni lokator, nije citana stranica.",
            },
            {"type": "section", "label": "Probni odjeljak", "note": "Samo deklaracija."},
            {"type": "time_range", "start_ms": 100, "end_ms": 200, "note": "Probni interval."},
        ):
            with self.subTest(locator=locator):
                draft = copy.deepcopy(self.draft)
                draft["evidence"][0]["locator"] = locator
                output = self.base / f"{uuid4()}.json"
                self.prepare(draft, output)
                self.assertEqual(
                    evidence.validate(self.root, output)["evidence"][0]["locator_verification"],
                    "declared_only",
                )

    def test_invalid_span_range_exact_text_and_utf8_byte_offsets(self):
        for start, end, exact in (
            (15, 10, "svjet"),
            (10, 999, "svjet"),
            (10, 15, "svijet"),
            (11, 16, "svjet"),
        ):
            with self.subTest(start=start, end=end):
                draft = copy.deepcopy(self.draft)
                draft["evidence"][0]["locator"].update(start=start, end=end, exact=exact)
                with self.assertRaises(JebError):
                    self.prepare(draft)
                self.assertFalse(self.output.exists())

    def test_text_span_requires_source_body(self):
        storage.save_record(
            self.root,
            self.source_content,
            "test-tool",
            "tool",
            "Bez tijela",
            record_id=self.source["id"],
            expected_revision=self.source["revision_id"],
        )
        with self.assertRaisesRegex(JebError, "locally bound"):
            self.prepare()

    def test_invalid_page_and_time_ranges(self):
        for locator in (
            {"type": "page", "pdf_page": None, "printed_page": None, "note": "Nepotpun lokator."},
            {"type": "page", "pdf_page": 0, "printed_page": None, "note": "Nevaljan broj."},
            {"type": "time_range", "start_ms": 200, "end_ms": 100, "note": "Pogresan redoslijed."},
        ):
            draft = copy.deepcopy(self.draft)
            draft["evidence"][0]["locator"] = locator
            with self.subTest(locator=locator), self.assertRaises(JebError):
                self.prepare(draft)

    def test_typed_missing_and_foreign_record_references(self):
        for field, value in (("subject_id", self.source["id"]), ("subject_id", str(uuid4()))):
            draft = copy.deepcopy(self.draft)
            draft["claims"][0][field] = value
            with self.assertRaises(JebError):
                self.prepare(draft)
        draft = copy.deepcopy(self.draft)
        draft["evidence"][0]["source_id"] = self.subject["id"]
        with self.assertRaisesRegex(JebError, "Expected source"):
            self.prepare(draft)

    def test_duplicate_ids_missing_claim_and_record_namespace_collision(self):
        for which in ("duplicate", "missing", "collision"):
            draft = copy.deepcopy(self.draft)
            if which == "duplicate":
                draft["evidence"][0]["id"] = self.claim_id
            elif which == "missing":
                draft["evidence"][0]["claim_id"] = str(uuid4())
            else:
                draft["claims"][0]["id"] = self.subject["id"]
            with self.subTest(which=which), self.assertRaises(JebError):
                self.prepare(draft)

    def test_unlinked_claim_is_explicitly_listed(self):
        draft = copy.deepcopy(self.draft)
        draft["evidence"] = []
        self.prepare(draft)
        self.assertEqual(
            evidence.validate(self.root, self.output)["claims_without_evidence"], [self.claim_id]
        )

    def test_support_and_contradiction_remain_separate_without_truth_decision(self):
        draft = copy.deepcopy(self.draft)
        second = copy.deepcopy(draft["evidence"][0])
        second.update(id=str(uuid4()), relation="contradicts")
        draft["evidence"].append(second)
        self.prepare(draft)
        view = evidence.inspect(self.root, self.output)
        self.assertEqual(
            [e["relation"] for e in view["packet"]["draft"]["evidence"]],
            ["supports", "contradicts"],
        )
        self.assertEqual(view["packet"]["review_state"], "unreviewed")

    def test_head_change_makes_packet_stale_even_if_unrelated(self):
        self.prepare()
        storage.save_record(self.root, self.entity_content, "test-tool", "tool", "Drugi predmet")
        with self.assertRaisesRegex(JebError, "Stale evidence"):
            evidence.validate(self.root, self.output)

    def test_source_revision_change_cannot_rebind_old_packet(self):
        self.prepare()
        storage.save_record(
            self.root,
            self.source_content,
            "test-tool",
            "tool",
            "Dopunjen izvor",
            self.body,
            self.source["id"],
            self.source["revision_id"],
        )
        packet = self.packet()
        packet["base_head"] = storage.head_at(self.root)
        self.rewrite(packet, reseal=True)
        with self.assertRaisesRegex(JebError, "bindings differ"):
            evidence.validate(self.root, self.output)

    def test_packet_hash_and_resealed_binding_tampering(self):
        self.prepare()
        original = self.packet()
        packet = copy.deepcopy(original)
        packet["draft"]["claims"][0]["statement"] = "Druga probna tvrdnja."
        self.rewrite(packet)
        with self.assertRaisesRegex(JebError, "hash mismatch"):
            evidence.validate(self.root, self.output)
        for field, value in (
            ("revision_id", str(uuid4())),
            ("record_sha256", "0" * 64),
            ("body_sha256", "0" * 64),
        ):
            packet = copy.deepcopy(original)
            packet["bindings"][0][field] = value
            self.rewrite(packet, reseal=True)
            with self.assertRaisesRegex(JebError, "bindings differ"):
                evidence.validate(self.root, self.output)

    def test_workspace_schema_review_and_actor_fields(self):
        self.prepare()
        original = self.packet()
        for field, value in (
            ("workspace_id", str(uuid4())),
            (
                "schema_hashes",
                {
                    "bank-evidence-draft": "0" * 64,
                    "bank-evidence-packet": "0" * 64,
                },
            ),
            ("review_state", "approved"),
            ("human_attestation", True),
        ):
            packet = copy.deepcopy(original)
            packet[field] = value
            self.rewrite(packet, reseal=True)
            with self.subTest(field=field), self.assertRaises(JebError):
                evidence.validate(self.root, self.output)

    def test_blank_non_latin_unknown_and_oversized_drafts(self):
        for statement in (" ", "\u041f\u0440\u043e\u0431\u0430", "x" * 4001):
            draft = copy.deepcopy(self.draft)
            draft["claims"][0]["statement"] = statement
            with self.assertRaises(JebError):
                self.prepare(draft)
        draft = copy.deepcopy(self.draft)
        draft["claims"][0]["human_attestation"] = True
        with self.assertRaises(JebError):
            self.prepare(draft)

    def test_output_is_outside_bank_and_never_overwritten(self):
        self.prepare()
        original = self.output.read_bytes()
        with self.assertRaisesRegex(JebError, "already exists"):
            self.prepare()
        self.assertEqual(self.output.read_bytes(), original)
        with self.assertRaisesRegex(JebError, "outside managed"):
            self.prepare(output=self.root / "evidence.json")

    def test_failed_publication_leaves_no_artifact(self):
        with patch.object(evidence.os, "link", side_effect=OSError("simulated failure")):
            with self.assertRaises(OSError):
                self.prepare()
        self.assertFalse(self.output.exists())
        self.assertFalse(list(self.base.glob(".jeb-evidence-*")))

    def test_existing_backup_format_and_old_schema_identities_unchanged(self):
        before = backup.schema_hashes()
        self.prepare()
        output = self.base / "backup.zip"
        backup.create(self.root, output)
        destination = self.base / "restored"
        backup.restore(output, destination)
        self.assertEqual(backup.schema_hashes(), before)
        self.assertTrue(evidence.validate(destination, self.output)["valid_packet"])
        self.assertFalse((destination / "evidence.json").exists())

    def test_cli_prepare_validate_inspect_without_project(self):
        self.input.write_bytes(canonical(self.draft))
        operations = [
            [
                "prepare",
                "--input",
                str(self.input),
                "--output",
                str(self.output),
                "--actor",
                "test-tool",
                "--actor-kind",
                "tool",
            ],
            ["validate", "--input", str(self.output)],
            ["inspect", "--input", str(self.output)],
        ]
        for operation in operations:
            process = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "jeb",
                    "bank",
                    "evidence",
                    *operation,
                    "--bank-root",
                    str(self.root),
                ],
                capture_output=True,
                timeout=20,
            )
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertEqual(json.loads(process.stdout)["approvals_created"], 0)


if __name__ == "__main__":
    unittest.main()
