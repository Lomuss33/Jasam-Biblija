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

from jeb import reading
from jeb.bank import storage
from jeb.bank.references import binding
from jeb.core import JebError, canonical, sha256


class ReadingTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="jeb-reading-test-")
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.root = self.base / "desk"
        reading.create_demo(self.root, synthetic=True)

    def payload(self, kind="note", **changes):
        data = reading.view(self.root, synthetic=True)
        value = {
            "view_ref": data["view_ref"],
            "request_id": str(uuid4()),
            "kind": kind,
            "passage_id": "ledger-entry",
            "text": "Original private test note",
            "anchor": None,
            "target_id": None,
            "edit_record_id": None,
            "expected_revision": None,
        }
        if kind == "highlight":
            body = data["passages"][0]["text"]
            start = body.index("blue ribbon")
            value["anchor"] = {"start": start, "end": start + 11, "exact": "blue ribbon"}
        if kind == "connection":
            value["target_id"] = "reading-room"
        return {**value, **changes}

    def fingerprint(self):
        return {
            str(path.relative_to(self.root)): sha256(path.read_bytes())
            for path in self.root.rglob("*")
            if path.is_file()
        }

    def replace_record(self, identity, body):
        state = storage.read_managed(self.root)
        prior = state["records"][identity]
        content = {
            key: prior[key] for key in ("kind", "title", "visibility", "processing_state", "data")
        }
        return storage.save_record(
            self.root,
            content,
            "test-tool",
            "tool",
            "Synthetic revision",
            body,
            identity,
            prior["revision_id"],
        )

    def test_opt_in_exclusive_demo_and_reads_never_modify_the_bank(self):
        before = self.fingerprint()
        result = reading.view(self.root, synthetic=True)
        self.assertTrue(result["synthetic"])
        self.assertFalse(result["releasable"])
        self.assertEqual(result["passages"][-1]["id"], "john-9")
        self.assertIsNone(result["passages"][-1]["text"])
        self.assertEqual(result["passages"][-1]["evidence"], [])
        with self.assertRaises(JebError):
            reading.view(self.root, synthetic=False)
        with self.assertRaises(FileExistsError):
            reading.create_demo(self.root, synthetic=True)
        self.assertEqual(before, self.fingerprint())

    def test_all_private_types_survive_reopen_and_bank_backup_restore(self):
        requests = [self.payload(kind) for kind in ("note", "highlight", "connection")]
        for request in requests:
            saved = reading.save(self.root, request, synthetic=True)
            self.assertEqual(saved["approvals_created"], 0)
        current = reading.view(self.root, synthetic=True)
        self.assertEqual(
            {item["kind"] for item in current["items"]}, {"note", "highlight", "connection"}
        )
        archive = self.base / "desk.zip"
        reading.create_backup(self.root, archive, synthetic=True)
        restored = self.base / "restored"
        reading.restore_backup(archive, restored, synthetic=True)
        self.assertEqual(current, reading.view(restored, synthetic=True))
        with self.assertRaises(JebError):
            reading.restore_backup(archive, restored, synthetic=True)

    def test_retries_are_idempotent_even_after_editing_and_reused_ids_cannot_change_content(self):
        request = self.payload()
        first = reading.save(self.root, request, synthetic=True)
        second = reading.save(self.root, request, synthetic=True)
        self.assertEqual(first["id"], second["id"])
        self.assertTrue(second["replayed"])
        edited = self.payload(
            text="Changed private note",
            edit_record_id=first["id"],
            expected_revision=first["revision_id"],
        )
        reading.save(self.root, edited, synthetic=True)
        reading.save(self.root, request, synthetic=True)
        self.assertEqual(len(reading.view(self.root, synthetic=True)["items"]), 1)
        conflict = reading.rpc(
            self.root, "save", synthetic=True, payload={**request, "text": "Different content"}
        )
        self.assertEqual(conflict["error"], "request_id_conflict")

    def test_stale_edits_and_invalid_destinations_leave_existing_notes_unchanged(self):
        first = reading.save(self.root, self.payload(), synthetic=True)
        old_edit = self.payload(edit_record_id=first["id"], expected_revision=first["revision_id"])
        reading.save(
            self.root,
            {**old_edit, "request_id": str(uuid4()), "text": "New revision"},
            synthetic=True,
        )
        before = self.fingerprint()
        self.assertEqual(
            reading.rpc(self.root, "save", synthetic=True, payload=old_edit)["error"],
            "revision_conflict",
        )
        for bad in (
            self.payload("connection", target_id="../../outside"),
            self.payload("connection", target_id="ledger-entry"),
            {**self.payload(), "file": "outside.json"},
            self.payload("highlight", anchor={"start": 0, "end": 4, "exact": "Luma"}),
        ):
            self.assertEqual(
                reading.rpc(self.root, "save", synthetic=True, payload=bad)["error"],
                "invalid_reading_input",
            )
        self.assertEqual(before, self.fingerprint())

    def test_book_level_note_allowed_without_source_but_highlight_needs_exact_source(self):
        reading.save(self.root, self.payload(passage_id="john-9"), synthetic=True)
        invalid = self.payload("highlight", passage_id="john-9")
        self.assertEqual(
            reading.rpc(self.root, "save", synthetic=True, payload=invalid)["error"],
            "invalid_reading_input",
        )
        self.assertEqual(len(reading.view(self.root, synthetic=True)["items"]), 1)

    def test_source_and_view_changes_keep_original_anchors_instead_of_reanchoring(self):
        request = self.payload("highlight")
        reading.save(self.root, request, synthetic=True)
        data = reading.load(self.root, synthetic=True)
        source_id = data["view"]["passages"][0]["source_ref"]["record_id"]
        original = reading.source(data["state"], data["view"]["passages"][0])["body"]
        self.replace_record(source_id, "😀 " + original)
        unchanged = reading.view(self.root, synthetic=True)
        self.assertEqual(unchanged["passages"][0]["text"], original)
        self.assertFalse(unchanged["passages"][0]["source"]["is_current"])
        updated = copy.deepcopy(data["view"])
        state = storage.read_managed(self.root)
        record = state["records"][source_id]
        updated["passages"][0]["source_ref"] = binding(
            state["revisions"][(source_id, record["revision_id"])]
        )
        for evidence in updated["passages"][0]["evidence"]:
            evidence["anchor"]["start"] += 2
            evidence["anchor"]["end"] += 2
        self.replace_record(data["view_ref"]["record_id"], canonical(updated).decode())
        changed = reading.view(self.root, synthetic=True)
        self.assertFalse(changed["items"][0]["current_view"])
        self.assertEqual(changed["items"][0]["anchor"], request["anchor"])
        new_request = self.payload("highlight")
        self.assertEqual(new_request["anchor"]["start"], request["anchor"]["start"] + 2)
        reading.save(self.root, new_request, synthetic=True)
        self.assertEqual(
            reading.rpc(
                self.root, "save", synthetic=True, payload={**request, "request_id": str(uuid4())}
            )["error"],
            "stale_view",
        )

    def test_uncertain_post_commit_failure_is_resolved_by_retry_without_duplicate(self):
        request = self.payload()
        original_sync = storage.sync_directory

        def fail_after_head(path):
            if path == self.root:
                raise OSError("Synthetic post-commit sync failure")
            return original_sync(path)

        with patch("jeb.bank.storage.sync_directory", side_effect=fail_after_head):
            result = reading.rpc(self.root, "save", synthetic=True, payload=request)
        self.assertEqual(result["error"], "reading_unavailable")
        self.assertTrue(reading.save(self.root, request, synthetic=True)["replayed"])
        self.assertEqual(len(reading.view(self.root, synthetic=True)["items"]), 1)

    def test_expected_head_check_prevents_a_double_create_after_an_interleaved_write(self):
        request = self.payload()
        other = self.payload(text="Independent concurrent note")
        original = storage.save_record
        advanced = False

        def interleave(*args, **kwargs):
            nonlocal advanced
            if not advanced:
                advanced = True
                reading.save(self.root, other, synthetic=True)
            return original(*args, **kwargs)

        with patch("jeb.bank.storage.save_record", side_effect=interleave):
            reading.save(self.root, request, synthetic=True)
        self.assertEqual(len(reading.view(self.root, synthetic=True)["items"]), 2)
        self.assertTrue(reading.save(self.root, request, synthetic=True)["replayed"])

    def test_history_limit_and_writer_busy_are_explicit_without_deleting_data(self):
        count = len(storage.read_managed(self.root)["chain"])
        with patch("jeb.bank.storage.MAX_HISTORY", count + 1):
            reading.save(self.root, self.payload(), synthetic=True)
            result = reading.rpc(self.root, "save", synthetic=True, payload=self.payload())
            self.assertEqual(result["error"], "history_limit")
            self.assertEqual(len(reading.view(self.root, synthetic=True)["items"]), 1)
        with storage.writer_lock(self.root):
            result = reading.rpc(self.root, "save", synthetic=True, payload=self.payload())
        self.assertEqual(result["error"], "reading_busy")

    def test_tampered_contract_or_foreign_bank_is_not_adopted_and_duplicate_json_is_rejected(self):
        request = self.payload()
        data = reading.load(self.root, synthetic=True)
        modified = copy.deepcopy(data["view"])
        modified["contracts"]["reading-item-v1"] = "0" * 64
        self.replace_record(data["view_ref"]["record_id"], canonical(modified).decode())
        before = self.fingerprint()
        self.assertEqual(
            reading.rpc(self.root, "view", synthetic=True)["error"], "invalid_reading_input"
        )
        self.assertEqual(before, self.fingerprint())
        foreign = self.base / "foreign"
        storage.initialize(foreign, "Ordinary synthetic bank", "3.0")
        self.assertEqual(
            reading.rpc(foreign, "save", synthetic=True, payload=request)["error"],
            "invalid_reading_input",
        )
        result = subprocess.run(
            [
                sys.executable,
                "-B",
                "-m",
                "jeb",
                "--synthetic",
                "reading",
                "save",
                "--bank-root",
                str(foreign),
            ],
            input='{"kind":"note","kind":"highlight"}',
            capture_output=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["error"], "invalid_reading_input")
