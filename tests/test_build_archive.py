from __future__ import annotations

import copy
import io
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
import warnings
import zipfile
from pathlib import Path
from unittest.mock import patch

from jeb.build_archive import create, restore, validate
from jeb.core import (
    JebError,
    Project,
    canonical,
    digest,
    native_path,
    read_bytes,
    read_yaml,
    sha256,
    write_json,
)
from jeb.export import reader
from jeb.knowledge import stored_records
from jeb.knowledge_curation import read_receipts as curations
from jeb.knowledge_review import read_receipts as reviews
from jeb.review import all_decisions
from jeb.search import search
from tests import test_knowledge_curation as fixtures
from tests.support import REPO, WorkspaceTest


class BuildArchiveTests(WorkspaceTest):
    annotation_response = fixtures.KnowledgeCurationTests.annotation_response
    evidence = fixtures.KnowledgeCurationTests.evidence
    graph = fixtures.KnowledgeCurationTests.graph
    stage = fixtures.KnowledgeCurationTests.stage
    decisions = fixtures.KnowledgeCurationTests.decisions
    approve_values = fixtures.KnowledgeCurationTests.approve_values
    promote = fixtures.KnowledgeCurationTests.promote
    version_pair = fixtures.KnowledgeCurationTests.version_pair
    item = fixtures.KnowledgeCurationTests.item
    choice = fixtures.KnowledgeCurationTests.choice
    action = fixtures.KnowledgeCurationTests.action
    govern = fixtures.KnowledgeCurationTests.govern

    def archive(self):
        result = create(self.project, self.source_id, "test-build", "dist/test-build.zip")
        return self.project.path(result["output"]), result

    def members(self, path):
        with zipfile.ZipFile(io.BytesIO(read_bytes(path))) as archive:
            return {name: archive.read(name) for name in archive.namelist()}

    def changed(self, members, *, seal=False):
        members = copy.deepcopy(members)
        if seal:
            manifest = json.loads(members["manifest.json"])
            manifest["files"] = [
                {"path": name, "size_bytes": len(data), "sha256": sha256(data)}
                for name, data in sorted(members.items())
                if name != "manifest.json"
            ]
            members["manifest.json"] = canonical(manifest)
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name, data in members.items():
                archive.writestr(name, data)
        path = self.base / "changed.zip"
        path.write_bytes(stream.getvalue())
        return path

    def test_snapshot_is_deterministic_and_binds_current_source_policy_and_reader(self):
        before = canonical(reader(self.project, self.source_id, "preview"))
        path, first = self.archive()
        second = create(self.project, self.source_id, "test-build", "dist/test-build.zip")
        self.assertEqual(first, second)
        checked = validate(path, synthetic=True)
        self.assertTrue(checked["valid"])
        self.assertFalse(checked["release"])
        self.assertEqual(checked["manifest"]["build"]["reader_sha256"], sha256(before))
        self.assertEqual(checked["manifest"]["build"]["policy_sha256"], self.project.policy_hash())
        self.assertEqual(first["manifest_sha256"], digest(checked["manifest"]))
        self.assertEqual(before, canonical(reader(self.project, self.source_id, "preview")))

    def test_only_allowlisted_build_inputs_are_copied_and_cached_outputs_are_not_trusted(self):
        for relative in (
            ".env",
            "data/source-research/private.json",
            "data/knowledge-proposals/unused/input.json",
            "exports/reader.json",
            "data/index/search.sqlite3",
            "src/evil.py",
            "data/raw/uncleared/source.txt",
        ):
            path = self.project.path(relative)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"NOT A BUILD INPUT; local synthetic exclusion fixture")
        path, _ = self.archive()
        names = set(self.members(path))
        self.assertFalse(
            any(
                name.startswith(
                    (
                        "exports/",
                        "src/",
                        "data/index/",
                        "data/knowledge-proposals/",
                        "data/source-research/",
                    )
                )
                for name in names
            )
        )
        self.assertNotIn(".env", names)
        self.assertNotIn("data/raw/uncleared/source.txt", names)
        result = restore(self.base, path, "restored", synthetic=True)
        restored = Project(self.base / result["output"], synthetic=True)
        self.assertEqual(search(restored, "covik", self.source_id)[0]["book_id"], "GEN")
        self.assertTrue(restored.path("exports/reader.json").read_bytes().startswith(b"{\n"))

    def test_source_gate_and_synthetic_opt_in_cannot_be_relaxed_by_archiving(self):
        with self.assertRaisesRegex(JebError, "needs_review"):
            create(Project(REPO), "crosswire-srkdijekav", "blocked", "dist/blocked.zip")
        path, _ = self.archive()
        with self.assertRaisesRegex(JebError, "--synthetic"):
            validate(path)
        with self.assertRaisesRegex(JebError, "--synthetic"):
            restore(self.base, path, "not-created")
        self.assertFalse((self.base / "not-created").exists())
        registry = read_yaml(self.project.path("sources/registry.yaml"))
        registry["sources"][0]["status"] = "needs_review"
        write_json(self.project.path("sources/registry.yaml"), registry)
        with self.assertRaisesRegex(JebError, "needs_review"):
            create(self.project, self.source_id, "blocked", "dist/blocked.zip")
        self.assertFalse(self.project.path("dist/blocked.zip").exists())

    def test_restore_works_without_the_original_project_and_rebuilds_disposable_artifacts(self):
        path, expected = self.archive()
        host = self.base / "empty-host"
        host.mkdir()
        archive_copy = host / "backup.zip"
        shutil.copyfile(path, archive_copy)
        result = restore(host, archive_copy, "recovered", synthetic=True)
        recovered = Project(host / "recovered", synthetic=True)
        self.assertEqual(result["build"], expected["build"])
        self.assertTrue(result["exports_and_index_rebuilt"])
        self.assertEqual(
            read_bytes(recovered.path("exports/reader.json")),
            canonical(reader(self.project, self.source_id, "preview")),
        )
        self.assertEqual(len(search(recovered, "covik", self.source_id)), 1)
        with self.assertRaisesRegex(JebError, "Synthetic"):
            reader(recovered, self.source_id, "release")

    def test_review_versions_withdrawals_and_text_decisions_recover_exactly(self):
        proposal = self.import_test_response()
        self.apply_test_decisions([self.decision(proposal)])
        records = self.version_pair()
        self.govern(
            self.action(
                self.choice(records.values(), "revision"),
                self.item("withdraw", records["original"]),
            )
        )
        original = reader(self.project, self.source_id, "preview")
        path, _ = self.archive()
        result = restore(self.base, path, "recovered-history", synthetic=True)
        recovered = Project(self.base / result["output"], synthetic=True)
        self.assertEqual(stored_records(recovered), stored_records(self.project))
        self.assertEqual(reviews(recovered), reviews(self.project))
        self.assertEqual(curations(recovered), curations(self.project))
        self.assertEqual(all_decisions(recovered), all_decisions(self.project))
        self.assertEqual(reader(recovered, self.source_id, "preview"), original)
        self.assertEqual({r["record_id"] for r in original["knowledge"]}, {"revision"})
        self.assertEqual(result["build"]["knowledge_records"], 2)
        self.assertEqual(result["build"]["review_receipts"], 2)
        self.assertEqual(result["build"]["curation_receipts"], 1)
        self.assertFalse(recovered.path("data/knowledge-proposals").exists())

    def test_superseded_stale_text_history_is_preserved_while_current_heads_are_validated(self):
        old = self.import_test_response()
        self.apply_test_decisions([self.decision(old)])
        policy = self.project.path("docs/EDITORIAL_POLICY.md")
        policy.write_bytes(policy.read_bytes() + b"\nNew temporary test policy\n")
        new = self.import_test_response(self.response("new-policy-batch"))
        decision = self.decision(new, decision_id="new-policy-decision")
        decision["supersedes"] = "test-decision"
        self.apply_test_decisions([decision])
        path, _ = self.archive()
        restore(self.base, path, "history", synthetic=True)
        recovered = Project(self.base / "history", synthetic=True)
        self.assertEqual(len(all_decisions(recovered)), 2)
        self.assertEqual(
            reader(recovered, self.source_id, "preview"),
            reader(self.project, self.source_id, "preview"),
        )

    def test_existing_destinations_and_archive_outputs_are_never_overwritten(self):
        path, _ = self.archive()
        for name in ("existing-empty", "existing-data"):
            directory = self.base / name
            directory.mkdir()
            if name == "existing-data":
                (directory / "keep.txt").write_bytes(b"keep")
            with self.subTest(name=name), self.assertRaisesRegex(JebError, "new nonexistent"):
                restore(self.base, path, name, synthetic=True)
        self.assertEqual((self.base / "existing-data/keep.txt").read_bytes(), b"keep")
        with self.assertRaisesRegex(JebError, "Existing artifact differs"):
            create(self.project, self.source_id, "different-id", "dist/test-build.zip")

    def test_restore_path_escape_and_invalid_output_type_fail_without_destination_writes(self):
        path, _ = self.archive()
        for destination in ("../outside", str(self.base / "absolute"), "."):
            with self.subTest(destination=destination), self.assertRaises(JebError):
                restore(self.base, path, destination, synthetic=True)
        with self.assertRaisesRegex(JebError, ".zip"):
            create(self.project, self.source_id, "bad", "dist/not-a-zip.txt")

    def test_checksum_damage_is_rejected_before_a_destination_is_published(self):
        path, _ = self.archive()
        members = self.members(path)
        raw = next(key for key in members if key.startswith("data/raw/"))
        members[raw] += b"altered"
        changed = self.changed(members)
        with self.assertRaisesRegex(JebError, "size/checksum"):
            restore(self.base, changed, "damaged", synthetic=True)
        self.assertFalse((self.base / "damaged").exists())

    def test_resealed_but_ineligible_source_and_false_reader_identity_are_rejected(self):
        path, _ = self.archive()
        members = self.members(path)
        registry = read_yaml(self.project.path("sources/registry.yaml"))
        registry["sources"][0]["status"] = "needs_review"
        members["sources/registry.yaml"] = canonical(registry)
        with self.assertRaisesRegex(JebError, "needs_review"):
            restore(self.base, self.changed(members, seal=True), "not-cleared", synthetic=True)
        members = self.members(path)
        manifest = json.loads(members["manifest.json"])
        manifest["build"]["reader_sha256"] = "0" * 64
        members["manifest.json"] = canonical(manifest)
        with self.assertRaisesRegex(JebError, "rebuilt corpus, reader"):
            restore(self.base, self.changed(members), "wrong-reader", synthetic=True)
        self.assertFalse((self.base / "not-cleared").exists())
        self.assertFalse((self.base / "wrong-reader").exists())

    def test_engine_schema_identity_and_manifest_structure_are_strict(self):
        path, _ = self.archive()
        original = self.members(path)
        for field, value in (
            ("engine_sha256", "0" * 64),
            ("package_version", "future-version"),
            ("schema_version", "2.0"),
            ("extra", True),
        ):
            members = copy.deepcopy(original)
            manifest = json.loads(members["manifest.json"])
            manifest[field] = value
            members["manifest.json"] = canonical(manifest)
            with self.subTest(field=field), self.assertRaises(JebError):
                validate(self.changed(members), synthetic=True)
        members = copy.deepcopy(original)
        members.pop("manifest.json")
        with self.assertRaisesRegex(JebError, "Missing"):
            validate(self.changed(members), synthetic=True)

    def test_secret_or_orphan_members_are_rejected_even_with_recomputed_manifest_hashes(self):
        path, _ = self.archive()
        for name in (
            ".env",
            "data/raw/synthetic-v1/" + "a" * 64 + ".txt",
            "data/knowledge-proposals/unreviewed/input.json",
        ):
            members = self.members(path)
            members[name] = b"not a canonical build input"
            with self.subTest(name=name), self.assertRaises(JebError):
                validate(self.changed(members, seal=True), synthetic=True)

    def test_missing_proposal_dependency_and_tampered_curator_receipt_block_recovery(self):
        proposal = self.import_test_response()
        record = self.promote()["reflection"]
        self.govern(self.action(self.item("withdraw", record)))
        path, _ = self.archive()
        members = self.members(path)
        packet = f"data/batches/{proposal['response']['batch_id']}/input.json"
        members.pop(packet)
        with self.assertRaises(OSError):
            restore(self.base, self.changed(members, seal=True), "missing-packet", synthetic=True)
        members = self.members(path)
        key = next(key for key in members if key.startswith("data/knowledge-curation/"))
        receipt = json.loads(members[key])
        receipt["decisions"]["items"][0]["rationale"] += " Changed"
        members[key] = canonical(receipt)
        with self.assertRaisesRegex(JebError, "filename/hash"):
            restore(self.base, self.changed(members, seal=True), "tampered-history", synthetic=True)
        self.assertFalse((self.base / "missing-packet").exists())
        self.assertFalse((self.base / "tampered-history").exists())

    def test_archive_paths_links_duplicates_and_directories_are_rejected(self):
        path, _ = self.archive()
        for name, mode in (
            ("../escape.txt", stat.S_IFREG),
            ("C:/escape.txt", stat.S_IFREG),
            ("config\\edition.yaml", stat.S_IFREG),
            ("config/link", stat.S_IFLNK),
            ("empty/", stat.S_IFDIR),
        ):
            stream = io.BytesIO()
            with warnings.catch_warnings(), zipfile.ZipFile(stream, "w") as archive:
                warnings.filterwarnings("ignore", message="Duplicate name:.*", category=UserWarning)
                for key, data in self.members(path).items():
                    archive.writestr(key, data)
                info = zipfile.ZipInfo(name)
                info.create_system = 3
                info.external_attr = (mode | 0o600) << 16
                archive.writestr(info, b"outside")
            changed = self.base / "unsafe.zip"
            changed.write_bytes(stream.getvalue())
            with self.subTest(name=name), self.assertRaises(JebError):
                validate(changed, synthetic=True)
        members = self.members(path)
        members["CONFIG/edition.yaml"] = members["config/edition.yaml"]
        with self.assertRaisesRegex(JebError, "Duplicate archive"):
            validate(self.changed(members), synthetic=True)

    def test_size_member_limits_and_unsupported_formats_are_bounded(self):
        path, _ = self.archive()
        with (
            patch("jeb.build_archive.MAX_DOWNLOAD", 16),
            self.assertRaisesRegex(JebError, "exceeds"),
        ):
            validate(path, synthetic=True)
        with (
            patch("jeb.build_archive.MAX_MANIFEST", 8),
            self.assertRaisesRegex(JebError, "oversized"),
        ):
            validate(path, synthetic=True)
        with (
            patch("jeb.build_archive.MAX_MEMBERS", 2),
            self.assertRaisesRegex(JebError, "Too many"),
        ):
            create(self.project, self.source_id, "too-many", "dist/too-many.zip")
        with (
            patch("jeb.build_archive.MAX_EXPANDED", 16),
            self.assertRaisesRegex(JebError, "expanded size"),
        ):
            create(self.project, self.source_id, "too-large", "dist/too-large.zip")
        bad = self.base / "unsupported.tar"
        bad.write_bytes(b"Not a ZIP archive")
        with self.assertRaisesRegex(ValueError, "Invalid build ZIP"):
            validate(bad, synthetic=True)

    def test_bad_normalized_state_or_missing_history_dependency_never_creates_an_archive(self):
        proposal = self.import_test_response()
        packet = self.project.path(f"data/batches/{proposal['response']['batch_id']}/input.json")
        original = read_bytes(packet)
        packet.unlink()
        with self.assertRaises(OSError):
            self.archive()
        self.assertFalse(self.project.path("dist/test-build.zip").exists())
        packet.write_bytes(original)
        normalized = self.project.path(f"data/normalized/{self.source_id}/GEN.json")
        book = json.loads(read_bytes(normalized))
        book["segments"][0]["normalized_text"] += " Corrupted cached artifact."
        write_json(normalized, book)
        with self.assertRaisesRegex(JebError, "Normalized artifact differs"):
            self.archive()
        self.assertFalse(self.project.path("dist/test-build.zip").exists())

    def test_failed_commit_does_not_publish_a_partial_restore(self):
        path, _ = self.archive()
        with (
            patch("jeb.build_archive.os.rename", side_effect=OSError("Simulated commit failure")),
            self.assertRaises(OSError),
        ):
            restore(self.base, path, "failed", synthetic=True)
        self.assertFalse((self.base / "failed").exists())
        self.assertEqual(list(self.base.glob(".jeb-restore-*")), [])

    def test_cli_can_validate_and_restore_without_a_project_configuration(self):
        path, _ = self.archive()
        host = self.base / "blank-host"
        host.mkdir()
        prefix = [sys.executable, "-m", "jeb", "--root", str(host), "--synthetic", "archive"]
        checked = subprocess.run(
            prefix + ["validate", "--input", str(path)],
            capture_output=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(checked.returncode, 0, checked.stderr)
        self.assertTrue(json.loads(checked.stdout)["valid"])
        restored = subprocess.run(
            prefix + ["restore", "--input", str(path), "--destination", "recovered"],
            capture_output=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(restored.returncode, 0, restored.stderr)
        self.assertFalse(json.loads(restored.stdout)["release"])

    @unittest.skipUnless(os.name == "nt", "Windows long canonical receipt paths")
    def test_long_windows_review_history_survives_archive_restore(self):
        record = self.promote()["reflection"]
        self.govern(self.action(self.item("withdraw", record), action_id="a" * 80))
        path, expected = self.archive()
        with tempfile.TemporaryDirectory(dir=native_path(Path(tempfile.gettempdir()))) as temporary:
            host = Path(temporary.removeprefix("\\\\?\\"))
            relative = "deep-" + "x" * 70
            result = restore(host, path, relative, synthetic=True)
            recovered = Project(host / relative, synthetic=True)
            receipt = next(native_path(recovered.path("data/knowledge-curation")).glob("*/*.json"))
            self.assertGreater(len(str(receipt)), 260)
            self.assertEqual(result["build"], expected["build"])
            self.assertEqual(curations(recovered), curations(self.project))
            self.assertEqual(reader(recovered, self.source_id, "preview")["knowledge"], [])
