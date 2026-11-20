"""Crash/conflict tests use original local records, never historical text."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

from jeb.bank import storage
from jeb.bank.validation import load_bank, show_record, validate_bank
from jeb.core import JebError, canonical, digest, sha256


class BankStorageTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.root = self.base / "bank"
        storage.initialize(self.root, "Originalna probna baza")
        self.content = {
            "kind": "entity",
            "title": "Probni pojam",
            "data": {"entity_type": "concept"},
            "visibility": "private",
            "processing_state": "inbox",
        }

    def save(self, content=None, **kwargs):
        return storage.save_record(
            self.root,
            content or self.content,
            "test-tool",
            "tool",
            "Originalna probna promjena",
            **kwargs,
        )

    def edit(self, result, content=None, **kwargs):
        return self.save(
            content, record_id=result["id"], expected_revision=result["revision_id"], **kwargs
        )

    def pending(self, status="prepared"):
        return [item for item in storage.recover(self.root)["pending"] if item["status"] == status]

    def test_init_create_edit_history_diff_and_old_bytes(self):
        self.assertEqual(validate_bank(self.root)["valid_records"], 0)
        first = self.save(body="Prvi tekst\r\nsvjet vrjeme covik razumit\r\n")
        old_path = self.root / "snapshots" / first["head"]["transaction_id"]
        old_bytes = {
            str(p.relative_to(old_path)): p.read_bytes() for p in old_path.rglob("*") if p.is_file()
        }
        content = {**self.content, "title": "Dopunjen pojam"}
        second = self.edit(first, content, body="Drugi tekst\n")
        self.assertEqual(second["id"], first["id"])
        self.assertNotEqual(second["revision_id"], first["revision_id"])
        self.assertEqual(show_record(self.root, first["id"])["body"], "Drugi tekst\n")
        versions = storage.history(self.root, first["id"])["revisions"]
        self.assertEqual(len(versions), 2)
        self.assertEqual(versions[0]["body"], "Prvi tekst\r\nsvjet vrjeme covik razumit\r\n")
        self.assertEqual(versions[1]["record"]["parent_revision"], first["revision_id"])
        self.assertEqual(
            old_bytes,
            {
                str(p.relative_to(old_path)): p.read_bytes()
                for p in old_path.rglob("*")
                if p.is_file()
            },
        )
        delta = storage.diff(self.root, first["id"], first["revision_id"], second["revision_id"])
        self.assertIn("+Drugi tekst", delta["body_diff"])
        self.assertIn("Dopunjen pojam", delta["metadata_diff"])

    def test_conflict_does_not_stage_or_change_head(self):
        first = self.save()
        self.edit(first)
        before = storage.head_at(self.root)
        staged = list((self.root / "staging").iterdir())
        with self.assertRaisesRegex(JebError, "Revision conflict"):
            self.edit(first)
        self.assertEqual(before, storage.head_at(self.root))
        self.assertEqual(staged, list((self.root / "staging").iterdir()))

    def test_second_process_cannot_write_while_locked(self):
        path = self.base / "input.json"
        path.write_bytes(canonical(self.content))
        with storage.writer_lock(self.root):
            process = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "jeb",
                    "bank",
                    "create",
                    "--bank-root",
                    str(self.root),
                    "--input",
                    str(path),
                    "--actor",
                    "test-tool",
                    "--actor-kind",
                    "tool",
                    "--reason",
                    "Originalni test",
                ],
                capture_output=True,
                timeout=20,
            )
        self.assertEqual(process.returncode, 2)
        self.assertIn(b"writer is busy", process.stderr)
        self.assertEqual(validate_bank(self.root)["valid_records"], 0)
        self.save()  # lock released, persistent lock file does not block use

    def test_process_exit_releases_lock_without_stale_file_removal(self):
        process = subprocess.run(
            [
                sys.executable,
                "-c",
                "from pathlib import Path; import os,sys; "
                "from jeb.bank.storage import writer_lock; "
                "lock=writer_lock(Path(sys.argv[1])); lock.__enter__(); os._exit(0)",
                str(self.root),
            ],
            capture_output=True,
            timeout=20,
        )
        self.assertEqual(process.returncode, 0, process.stderr)
        self.save()

    def test_failure_at_each_file_write_keeps_previous_state(self):
        first = self.save()
        old_head = storage.head_at(self.root)
        # workspace, record, body, manifest, temporary HEAD
        for count in range(1, 6):
            with self.subTest(count=count):
                writes = 0
                original = storage.write_new

                def fail(path, data):
                    nonlocal writes
                    writes += 1
                    if writes == count:
                        raise OSError("simulated interruption")
                    original(path, data)

                with patch.object(storage, "write_new", side_effect=fail):
                    with self.assertRaisesRegex(OSError, "interruption"):
                        self.edit(first, body="Novi probni tekst\n")
                self.assertEqual(storage.head_at(self.root), old_head)
                self.assertIsNone(show_record(self.root, first["id"])["body"])
        self.assertTrue(self.pending("incomplete"))

    def test_prepared_stage_recovery_and_idempotence(self):
        first = self.save()
        with patch.object(storage.os, "rename", side_effect=OSError("interruption")):
            with self.assertRaises(OSError):
                self.edit(first, body="Pripremljen tekst\n")
        candidate = self.pending()[0]
        self.assertEqual(candidate["area"], "staging")
        self.assertIsNone(show_record(self.root, first["id"])["body"])
        result = storage.recover(self.root, candidate["name"])
        self.assertEqual(show_record(self.root, first["id"])["body"], "Pripremljen tekst\n")
        self.assertEqual(result["head"], storage.recover(self.root, candidate["name"])["head"])

    def test_snapshot_published_before_head_is_not_visible_until_recovery(self):
        first = self.save()
        with patch.object(storage, "publish_head", side_effect=OSError("interruption")):
            with self.assertRaises(OSError):
                self.edit(first, body="Nevidljivo do oporavka\n")
        candidate = self.pending()[0]
        self.assertEqual(candidate["area"], "snapshots")
        self.assertIsNone(show_record(self.root, first["id"])["body"])
        storage.recover(self.root, candidate["name"])
        self.assertIn("Nevidljivo", show_record(self.root, first["id"])["body"])

    def test_head_replace_failure_and_old_reader_during_staging(self):
        first = self.save()
        original = storage.write_new
        observed = []

        def observe(path, data):
            if path.name == "manifest.json":
                observed.append(show_record(self.root, first["id"])["body"])
            original(path, data)

        with patch.object(storage, "write_new", side_effect=observe):
            with patch.object(storage.os, "replace", side_effect=OSError("interruption")):
                with self.assertRaises(OSError):
                    self.edit(first, body="Novi tekst\n")
        self.assertEqual(observed, [None])
        self.assertIsNone(show_record(self.root, first["id"])["body"])
        storage.recover(self.root, self.pending()[0]["name"])
        self.assertEqual(show_record(self.root, first["id"])["body"], "Novi tekst\n")

    def test_recovery_refuses_conflicting_or_incomplete_work(self):
        first = self.save()
        with patch.object(storage, "publish_head", side_effect=OSError("interruption")):
            with self.assertRaises(OSError):
                self.edit(first, body="Odvojeni prijedlog\n")
        pending = self.pending()[0]["name"]
        second = self.edit(first, body="Prihvacena promjena\n")
        with self.assertRaisesRegex(JebError, "Recovery conflict"):
            storage.recover(self.root, pending)
        self.assertEqual(storage.head_at(self.root), second["head"])
        self.assertTrue(self.pending("conflict"))
        with self.assertRaises(JebError):
            storage.recover(self.root, "../outside")

    def test_interrupted_genesis_can_be_recovered(self):
        other = self.base / "other"
        with patch.object(storage, "publish_head", side_effect=OSError("interruption")):
            with self.assertRaises(OSError):
                storage.initialize(other, "Drugi probni prostor")
        with self.assertRaisesRegex(JebError, "No committed HEAD"):
            validate_bank(other)
        pending = storage.recover(other)["pending"][0]["name"]
        storage.recover(other, pending)
        self.assertEqual(validate_bank(other)["valid_records"], 0)

    def test_invalid_body_reference_and_kind_change_never_commit(self):
        first = self.save()
        for content, body in (
            (
                {
                    **self.content,
                    "kind": "article",
                    "data": {"subjects": [str(uuid4())], "sources": []},
                },
                "Tekst\n",
            ),
            (
                {
                    **self.content,
                    "kind": "article",
                    "data": {"subjects": [first["id"]], "sources": []},
                },
                "Tekst\n",
            ),
            (self.content, "\u041f\u0440\u043e\u0431\u0430"),
        ):
            with self.subTest(content=content), self.assertRaises(JebError):
                self.edit(first, content, body=body)
        self.assertEqual(storage.head_at(self.root), first["head"])

    def test_typed_article_and_body_removal(self):
        subject = self.save()
        article = self.save(
            {
                **self.content,
                "kind": "article",
                "data": {
                    "subjects": [subject["id"]],
                    "sources": [],
                },
            },
            body="# Originalni probni clanak\n",
        )
        self.assertEqual(validate_bank(self.root)["valid_records"], 2)
        with self.assertRaises(JebError):
            self.edit(
                article,
                {
                    **self.content,
                    "kind": "article",
                    "data": {
                        "subjects": [subject["id"]],
                        "sources": [],
                    },
                },
            )
        entity = self.save(body="Opcionalna biljeska\n")
        self.edit(entity)
        self.assertIsNone(show_record(self.root, entity["id"])["body"])

    def reseal(self, path):
        manifest = storage.document(path / "manifest.json")
        files = {}
        for directory in (path / "records").iterdir():
            record = storage.document(directory / "record.json")
            files[directory.name] = {
                "record": sha256((directory / "record.json").read_bytes()),
                "body": record["body_sha256"],
            }
        manifest["snapshot_sha256"] = digest(
            {
                "workspace": sha256((path / "workspace.json").read_bytes()),
                "files": files,
            }
        )
        (path / "manifest.json").write_bytes(canonical(manifest))
        (self.root / "HEAD.json").write_bytes(
            canonical(
                {
                    "transaction_id": path.name,
                    "manifest_sha256": sha256(canonical(manifest)),
                }
            )
        )

    def test_tampered_old_snapshot_is_rejected(self):
        first = self.save(body="Izvorni tekst\n")
        self.edit(first)
        old = self.root / "snapshots" / first["head"]["transaction_id"]
        (old / "records" / first["id"] / "body.md").write_text("changed", encoding="utf-8")
        with self.assertRaisesRegex(JebError, "hash mismatch"):
            validate_bank(self.root)

    def test_resealed_parent_and_immutable_field_tampering_rejected(self):
        first = self.save()
        second = self.edit(first)
        path = self.root / "snapshots" / second["head"]["transaction_id"]
        record_path = path / "records" / first["id"] / "record.json"
        original = storage.document(record_path)
        for field, value, pattern in (
            ("parent_revision", str(uuid4()), "Broken revision parent"),
            ("revision_id", first["revision_id"], "reused"),
            ("created_at", "2000-01-01T00:00:00Z", "Immutable"),
        ):
            with self.subTest(field=field):
                changed = {**original, field: value}
                record_path.write_bytes(canonical(changed))
                self.reseal(path)
                with self.assertRaisesRegex(JebError, pattern):
                    validate_bank(self.root)

    def test_limits_and_existing_target(self):
        with self.assertRaises(FileExistsError):
            storage.initialize(self.root, "Novi naslov")
        first = self.save()
        with patch.object(storage, "MAX_HISTORY", 2):
            with self.assertRaisesRegex(JebError, "History limit"):
                self.edit(first)
        self.assertEqual(storage.head_at(self.root), first["head"])
        with patch.object(storage, "MAX_HISTORY_BYTES", 1):
            with self.assertRaisesRegex(JebError, "byte limit"):
                validate_bank(self.root)

    def test_cli_create_edit_history_diff_and_validation(self):
        input_path = self.base / "input.json"
        input_path.write_bytes(canonical(self.content))

        def run(*args):
            result = subprocess.run(
                [sys.executable, "-m", "jeb", "bank", *args, "--bank-root", str(self.root)],
                capture_output=True,
                timeout=20,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            return json.loads(result.stdout)

        first = run(
            "create",
            "--input",
            str(input_path),
            "--actor",
            "test-tool",
            "--actor-kind",
            "tool",
            "--reason",
            "Originalni test",
        )
        second = run(
            "edit",
            first["id"],
            "--expected-revision",
            first["revision_id"],
            "--input",
            str(input_path),
            "--actor",
            "test-tool",
            "--actor-kind",
            "tool",
            "--reason",
            "Nova probna revizija",
        )
        self.assertEqual(len(run("history", first["id"])["revisions"]), 2)
        self.assertIn(
            "metadata_diff",
            run(
                "diff",
                first["id"],
                "--from-revision",
                first["revision_id"],
                "--to-revision",
                second["revision_id"],
            ),
        )
        self.assertEqual(run("validate")["valid_records"], 1)
        self.assertEqual(run("recover")["pending"], [])

    def test_legacy_snapshot_is_not_silently_migrated(self):
        legacy = self.base / "legacy"
        (legacy / "records").mkdir(parents=True)
        workspace = {**storage.document(self.root / "workspace.json"), "schema_version": "1.0"}
        (legacy / "workspace.json").write_bytes(canonical(workspace))
        self.assertEqual(load_bank(legacy)[1], {})
        with self.assertRaises(JebError):
            storage.save_record(legacy, self.content, "tool", "tool", "Originalni test")
        self.assertFalse((legacy / ".writer.lock").exists())

    def test_abrupt_process_exit_before_head_keeps_old_state_and_can_recover(self):
        first = self.save()
        code = """
import os, sys
from pathlib import Path
from jeb.bank import storage
storage.publish_head = lambda *args: os._exit(42)
storage.save_record(Path(sys.argv[1]), {
    'kind':'entity', 'title':'Probna dopuna', 'data':{'entity_type':'concept'},
    'visibility':'private', 'processing_state':'inbox'
}, 'test-tool', 'tool', 'Originalni test prekida', 'Novi tekst\\n', sys.argv[2], sys.argv[3])
"""
        process = subprocess.run(
            [sys.executable, "-c", code, str(self.root), first["id"], first["revision_id"]],
            capture_output=True,
            timeout=20,
        )
        self.assertEqual(process.returncode, 42, process.stderr)
        self.assertEqual(storage.head_at(self.root), first["head"])
        self.assertIsNone(show_record(self.root, first["id"])["body"])
        storage.recover(self.root, self.pending()[0]["name"])
        self.assertEqual(show_record(self.root, first["id"])["body"], "Novi tekst\n")

    def test_recovery_rejects_incomplete_directory_without_deleting_it(self):
        identity = str(uuid4())
        incomplete = self.root / "staging" / identity
        incomplete.mkdir()
        (incomplete / "partial.txt").write_text("original test", encoding="utf-8")
        with self.assertRaises(OSError):
            storage.recover(self.root, identity)
        self.assertTrue((incomplete / "partial.txt").exists())
        self.assertEqual(validate_bank(self.root)["valid_records"], 0)


if __name__ == "__main__":
    unittest.main()
