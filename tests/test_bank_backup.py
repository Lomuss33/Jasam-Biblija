"""Private committed-chain backups tested only with original offline fixtures."""

from __future__ import annotations

import copy
import json
import stat
import subprocess
import sys
import tempfile
import unittest
import warnings
import zipfile
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

from jeb.bank import backup, storage
from jeb.bank.validation import show_record, validate_bank
from jeb.core import JebError, canonical, sha256


class BankBackupTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.root, self.output = self.base / "bank", self.base / "backup.zip"
        storage.initialize(self.root, "Originalna probna baza za kopiranje")
        self.content = {
            "kind": "entity",
            "title": "Probni pojam",
            "data": {"entity_type": "concept"},
            "visibility": "private",
            "processing_state": "inbox",
        }
        self.first = storage.save_record(
            self.root,
            self.content,
            "test-tool",
            "tool",
            "Originalni prvi zapis",
            "svjet vrjeme covik razumit\r\n",
        )
        self.second = storage.save_record(
            self.root,
            {**self.content, "title": "Dopunjen pojam"},
            "test-tool",
            "tool",
            "Originalna dopuna",
            "Novi tekst\n",
            self.first["id"],
            self.first["revision_id"],
        )

    def make(self):
        return backup.create(self.root, self.output)

    def entries(self):
        with zipfile.ZipFile(self.output) as archive:
            return {info.filename: archive.read(info) for info in archive.infolist()}

    def rewrite(self, entries, path=None):
        target = path or self.base / "changed.zip"
        with zipfile.ZipFile(target, "w") as archive:
            for name, data in entries.items():
                archive.writestr(backup._zip_info(name), data)
        return target

    def assert_rejected(self, path):
        destination = self.base / "rejected"
        with self.assertRaises((JebError, OSError)):
            backup.restore(path, destination)
        self.assertFalse(destination.exists())

    def test_round_trip_retains_exact_committed_bytes_and_is_writable(self):
        result = self.make()
        original = storage.read_managed(self.root)
        paths = backup.committed_paths(original)
        before = {name: (self.root / name).read_bytes() for name in paths}
        self.root.rename(self.base / "disconnected-original")
        destination = self.base / "restored"
        restored = backup.restore(self.output, destination)
        self.assertEqual(result["head"], restored["head"])
        self.assertEqual(before, {name: (destination / name).read_bytes() for name in paths})
        self.assertEqual(sha256(self.output.read_bytes()), result["sha256"])
        self.assertEqual(
            storage.history(destination, self.first["id"])["revisions"][0]["body"],
            "svjet vrjeme covik razumit\r\n",
        )
        self.assertEqual(validate_bank(destination)["valid_records"], 1)
        storage.save_record(
            destination,
            self.content,
            "test-tool",
            "tool",
            "Nakon oporavka",
            record_id=self.first["id"],
            expected_revision=self.second["revision_id"],
        )

    def test_pending_private_material_and_lock_not_in_backup(self):
        with patch.object(storage, "publish_head", side_effect=OSError("interruption")):
            with self.assertRaises(OSError):
                storage.save_record(
                    self.root,
                    {**self.content, "title": "Privatni neaktivni prijedlog"},
                    "test-tool",
                    "tool",
                    "Neaktivno",
                )
        partial = self.root / "staging" / str(uuid4())
        partial.mkdir()
        (partial / "private-note.txt").write_text("private original test", encoding="utf-8")
        self.make()
        entries = self.entries()
        self.assertFalse(any("staging" in name or "lock" in name for name in entries))
        self.assertEqual(
            set(entries) - {"backup.json"},
            set(backup.committed_paths(storage.read_managed(self.root))),
        )
        destination = self.base / "restored"
        backup.restore(self.output, destination)
        self.assertEqual(storage.recover(destination)["pending"], [])
        self.assertEqual(
            show_record(destination, self.first["id"])["record"]["title"], "Dopunjen pojam"
        )

    def test_empty_bank_round_trip_recreates_empty_record_directories(self):
        empty = self.base / "empty"
        storage.initialize(empty, "Prazna probna baza")
        output = self.base / "empty.zip"
        backup.create(empty, output)
        destination = self.base / "restored"
        backup.restore(output, destination)
        self.assertEqual(validate_bank(destination)["valid_records"], 0)

    def test_existing_outputs_and_destinations_never_overwritten(self):
        self.make()
        before = self.output.read_bytes()
        with self.assertRaises(JebError):
            backup.create(self.root, self.output)
        self.assertEqual(before, self.output.read_bytes())
        for name in ("empty-dest", "full-dest"):
            destination = self.base / name
            destination.mkdir()
            if name == "full-dest":
                (destination / "keep.txt").write_text("keep", encoding="utf-8")
            with self.assertRaises(JebError):
                backup.restore(self.output, destination)
            self.assertTrue(destination.is_dir())

    def test_backup_output_inside_bank_rejected_without_artifact(self):
        output = self.root / "copy.zip"
        with self.assertRaisesRegex(JebError, "outside"):
            backup.create(self.root, output)
        self.assertFalse(output.exists())

    def test_output_race_uses_no_clobber_publication(self):
        original = backup.os.link

        def race(source, destination):
            Path(destination).write_bytes(b"other writer artifact")
            original(source, destination)

        with patch.object(backup.os, "link", side_effect=race):
            with self.assertRaises(FileExistsError):
                self.make()
        self.assertEqual(self.output.read_bytes(), b"other writer artifact")
        self.assertFalse(list(self.base.glob(".jeb-bank-backup-*")))

    def test_destination_race_is_exclusively_reserved_and_preserved(self):
        self.make()
        destination = self.base / "restored"
        original = Path.mkdir

        def race(path, *args, **kwargs):
            if path == destination:
                original(path)
                (path / "keep.txt").write_text("other user", encoding="utf-8")
            return original(path, *args, **kwargs)

        with patch.object(Path, "mkdir", race):
            with self.assertRaises(FileExistsError):
                backup.restore(self.output, destination)
        self.assertEqual((destination / "keep.txt").read_text(), "other user")

    def test_checksum_damage_fails_before_destination_creation(self):
        self.make()
        entries = self.entries()
        body = next(name for name in entries if name.endswith("body.md"))
        entries[body] = b"x" * len(entries[body])
        self.assert_rejected(self.rewrite(entries))

    def test_resealed_inventory_does_not_bypass_snapshot_hash(self):
        self.make()
        entries = self.entries()
        name = next(name for name in entries if name.endswith("record.json"))
        record = json.loads(entries[name])
        record["title"] = "Neovlastena promjena probnog zapisa"
        entries[name] = canonical(record)
        manifest = json.loads(entries["backup.json"])
        for item in manifest["files"]:
            if item["path"] == name:
                item.update(bytes=len(entries[name]), sha256=sha256(entries[name]))
        entries["backup.json"] = canonical(manifest)
        self.assert_rejected(self.rewrite(entries))

    def test_malicious_paths_directories_and_special_entries(self):
        self.make()
        entries = self.entries()
        for name in (
            "../escape",
            "/escape",
            "C:/escape",
            "a\\escape",
            "workspace.json/",
            "snapshots/../workspace.json",
            "staging/private.txt",
            ".writer.lock",
            "CON",
        ):
            with self.subTest(name=name):
                self.assert_rejected(self.rewrite({**entries, name: b"bad"}))
        for kind in (stat.S_IFLNK, stat.S_IFIFO, stat.S_IFDIR):
            path = self.base / "special.zip"
            with zipfile.ZipFile(path, "w") as archive:
                for name, data in entries.items():
                    info = backup._zip_info(name)
                    if name == "workspace.json":
                        info.external_attr = (kind | 0o600) << 16
                    archive.writestr(info, data)
            self.assert_rejected(path)

    def test_duplicate_members_and_duplicate_manifest_paths(self):
        self.make()
        entries = self.entries()
        path = self.base / "duplicates.zip"
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(path, "w") as archive:
                for name, data in entries.items():
                    archive.writestr(backup._zip_info(name), data)
                archive.writestr(backup._zip_info("workspace.json"), entries["workspace.json"])
        self.assert_rejected(path)
        manifest = json.loads(entries["backup.json"])
        manifest["files"].append(copy.deepcopy(manifest["files"][0]))
        entries["backup.json"] = canonical(manifest)
        self.assert_rejected(self.rewrite(entries))

    def test_manifest_workspace_head_schema_and_inventory_mismatches(self):
        self.make()
        original = self.entries()
        for field, value in (
            ("workspace_id", str(uuid4())),
            ("schema_version", "9.0"),
            ("schema_hashes", {}),
            ("head", {"transaction_id": str(uuid4()), "manifest_sha256": "0" * 64}),
            ("privacy", "public"),
        ):
            with self.subTest(field=field):
                entries = dict(original)
                manifest = json.loads(entries["backup.json"])
                manifest[field] = value
                entries["backup.json"] = canonical(manifest)
                self.assert_rejected(self.rewrite(entries))
        entries = dict(original)
        entries.pop("HEAD.json")
        self.assert_rejected(self.rewrite(entries))

    def test_inactive_snapshot_in_inventory_rejected(self):
        self.make()
        entries = self.entries()
        source = next(name for name in entries if name.endswith("manifest.json"))
        orphan = f"snapshots/{uuid4()}/manifest.json"
        entries[orphan] = entries[source]
        manifest = json.loads(entries["backup.json"])
        manifest["files"].append(
            {"path": orphan, "bytes": len(entries[orphan]), "sha256": sha256(entries[orphan])}
        )
        entries["backup.json"] = canonical(manifest)
        self.assert_rejected(self.rewrite(entries))

    def test_limits_enforced_before_restore(self):
        self.make()
        for limit, value in (
            ("MAX_ARCHIVE", 10),
            ("MAX_FILES", 1),
            ("MAX_MANIFEST", 10),
            ("MAX_PAYLOAD", 10),
            ("MAX_FILE_BYTES", 10),
        ):
            with self.subTest(limit=limit), patch.object(backup, limit, value):
                self.assert_rejected(self.output)

    def test_zip_comments_truncation_and_unknown_compression_rejected(self):
        self.make()
        path = self.base / "invalid.zip"
        path.write_bytes(self.output.read_bytes()[:-10])
        self.assert_rejected(path)
        with zipfile.ZipFile(path, "w") as archive:
            archive.comment = b"unsupported comment"
            for name, data in self.entries().items():
                archive.writestr(backup._zip_info(name), data)
        self.assert_rejected(path)
        with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_BZIP2) as archive:
            for name, data in self.entries().items():
                archive.writestr(name, data)
        self.assert_rejected(path)

    def test_restore_failures_clean_only_the_new_destination(self):
        self.make()
        original = storage.write_new
        for checkpoint in ("workspace.json", "record.json", "head"):
            destination = self.base / "restored"

            def fail(path, data):
                if path.is_relative_to(destination) and (
                    path.name == checkpoint
                    or (checkpoint == "head" and path.name.startswith("head-"))
                ):
                    # Simulate a partial file, not only an exception before creation.
                    path.write_bytes(data[:3])
                    raise OSError("simulated restore interruption")
                original(path, data)

            with (
                self.subTest(checkpoint=checkpoint),
                patch.object(storage, "write_new", side_effect=fail),
            ):
                with self.assertRaises(OSError):
                    backup.restore(self.output, destination)
            self.assertFalse(destination.exists())
            self.assertEqual(validate_bank(self.root)["valid_records"], 1)

    def test_invalid_source_and_writer_contention_never_publish_backup(self):
        with storage.writer_lock(self.root):
            process = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "jeb",
                    "bank",
                    "backup",
                    "--bank-root",
                    str(self.root),
                    "--output",
                    str(self.output),
                ],
                capture_output=True,
                timeout=20,
            )
        self.assertEqual(process.returncode, 2)
        self.assertIn(b"busy", process.stderr)
        self.assertFalse(self.output.exists())
        (self.root / "HEAD.json").write_bytes(b"{}")
        with self.assertRaises(JebError):
            self.make()
        self.assertFalse(self.output.exists())

    def test_cli_backup_verify_restore_without_project(self):
        destination = self.base / "restored"
        operations = (
            ["backup", "--bank-root", str(self.root), "--output", str(self.output)],
            ["backup-verify", "--input", str(self.output)],
            ["restore", "--input", str(self.output), "--destination", str(destination)],
        )
        for operation in operations:
            result = subprocess.run(
                [sys.executable, "-m", "jeb", "bank", *operation], capture_output=True, timeout=20
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["approvals_created"], 0)
        self.assertEqual(validate_bank(destination)["valid_records"], 1)

    def test_false_directory_count_and_corrupt_deflate_are_rejected(self):
        import struct

        self.make()
        payload = bytearray(self.output.read_bytes())
        struct.pack_into("<HH", payload, len(payload) - 14, 1, 1)
        path = self.base / "false-count.zip"
        path.write_bytes(payload)
        self.assert_rejected(path)

        with zipfile.ZipFile(self.output) as archive:
            member = next(item for item in archive.infolist() if item.filename.endswith("body.md"))
        payload = bytearray(self.output.read_bytes())
        name_size, extra_size = struct.unpack_from("<HH", payload, member.header_offset + 26)
        position = member.header_offset + 30 + name_size + extra_size
        payload[position] = 0xFF
        path = self.base / "corrupt-deflate.zip"
        path.write_bytes(payload)
        self.assert_rejected(path)

    def test_noncanonical_but_valid_head_bytes_are_preserved(self):
        original = json.dumps(storage.head_at(self.root), separators=(",", ":")).encode("utf-8")
        (self.root / "HEAD.json").write_bytes(original)
        self.make()
        destination = self.base / "restored"
        backup.restore(self.output, destination)
        self.assertEqual((destination / "HEAD.json").read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
