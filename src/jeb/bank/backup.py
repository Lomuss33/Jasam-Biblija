"""Bounded private backups of committed v2 history, never arbitrary workspace ZIPs."""

from __future__ import annotations

import hashlib
import os
import re
import stat
import struct
import tempfile
import zipfile
import zlib
from contextlib import contextmanager
from importlib.resources import files
from pathlib import Path
from uuid import uuid4

from jeb.bank import storage
from jeb.bank.validation import MAX_FILE_BYTES, safe_path
from jeb.core import JebError, canonical, json_loads, read_bytes, require, sha256, validate_schema

MAX_FILES = 50_000
MAX_MANIFEST = 16 * 1024 * 1024
MAX_PAYLOAD = 130 * 1024 * 1024
MAX_ARCHIVE = 160 * 1024 * 1024
SCHEMAS = (
    "bank-workspace",
    "bank-workspace-v2",
    "bank-record-v2",
    "bank-head",
    "bank-transaction",
    "bank-backup",
)
UUID = r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"
MEMBER = re.compile(
    rf"(?:workspace\.json|HEAD\.json|snapshots/{UUID}/"
    rf"(?:workspace\.json|manifest\.json|records/{UUID}/(?:record\.json|body\.md)))"
)


def schema_hashes(version: str = "2.0") -> dict:
    require(version in ("2.0", "3.0"), "Unsupported backup bank format")
    names = (
        SCHEMAS
        if version == "2.0"
        else (
            "bank-workspace",
            "bank-workspace-v3",
            "bank-record-v3",
            "bank-head",
            "bank-transaction-v3",
            "bank-backup-v3",
        )
    )
    return {
        name: sha256(files("jeb").joinpath("schemas", name + ".json").read_bytes())
        for name in names
    }


def committed_paths(state: dict) -> list[str]:
    result = ["workspace.json", "HEAD.json"]
    for snapshot in state["chain"]:
        prefix = f"snapshots/{snapshot['manifest']['transaction_id']}"
        result.extend((f"{prefix}/workspace.json", f"{prefix}/manifest.json"))
        for identity, record in snapshot["records"].items():
            result.append(f"{prefix}/records/{identity}/record.json")
            if record["body_sha256"] is not None:
                result.append(f"{prefix}/records/{identity}/body.md")
    require(len(result) <= MAX_FILES, "Too many backup files")
    return sorted(result)


def _zip_info(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name)
    info.create_system = 3
    info.external_attr = (stat.S_IFREG | 0o600) << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    return info


def _zip_shape(path: Path) -> None:
    """Check ordinary ZIP end record before zipfile allocates the directory list."""
    require(path.stat().st_size <= MAX_ARCHIVE, "Backup archive too large")
    with path.open("rb") as stream:
        require(stream.read(4) == b"PK\x03\x04", "ZIP preamble unsupported")
        stream.seek(0, os.SEEK_END)
        require(stream.tell() >= 22, "Truncated backup archive")
        stream.seek(-22, os.SEEK_END)
        end_position = stream.tell()
        signature, disk, cd_disk, on_disk, count, size, offset, comment = struct.unpack(
            "<4s4H2LH", stream.read(22)
        )
        require(signature == b"PK\x05\x06" and comment == 0, "Unsupported ZIP end/comment")
        require(disk == cd_disk == 0 and on_disk == count, "Multi-disk ZIP unsupported")
        require(count <= MAX_FILES + 1, "Too many backup members")
        require(offset + size == end_position, "ZIP64 or noncanonical directory unsupported")
        # Do not trust the EOCD count: zipfile itself parses until directory end.
        stream.seek(offset)
        actual = 0
        while stream.tell() < end_position:
            header = stream.read(46)
            require(len(header) == 46 and header[:4] == b"PK\x01\x02", "Invalid ZIP directory")
            name_size, extra_size, comment_size = struct.unpack_from("<3H", header, 28)
            require(
                0 < name_size <= 250 and extra_size <= 1024 and comment_size == 0,
                "Oversized ZIP directory metadata",
            )
            actual += 1
            require(actual <= MAX_FILES + 1, "Too many backup members")
            stream.seek(name_size + extra_size, os.SEEK_CUR)
            require(stream.tell() <= end_position, "Truncated ZIP directory")
        require(actual == count, "ZIP member count differs")


def _manifest(archive: zipfile.ZipFile) -> tuple[dict, dict[str, zipfile.ZipInfo]]:
    infos, total = {}, 0
    for info in archive.infolist():
        name = info.filename
        require(name == info.orig_filename, "Noncanonical backup member")
        require(name not in infos, "Duplicate backup member")
        require(
            name == "backup.json" or bool(MEMBER.fullmatch(name)), f"Unexpected backup path: {name}"
        )
        require(not info.is_dir(), "Directory entries unsupported")
        mode = info.external_attr >> 16
        require(stat.S_IFMT(mode) in (0, stat.S_IFREG), "Link or special ZIP entry forbidden")
        require(not (info.flag_bits & 1), "Encrypted ZIP entries unsupported")
        require(
            info.compress_type in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED),
            "Unsupported ZIP compression",
        )
        limit = MAX_MANIFEST if name == "backup.json" else MAX_FILE_BYTES
        require(info.file_size <= limit, "Backup member too large")
        total += info.file_size
        require(total <= MAX_PAYLOAD + MAX_MANIFEST, "Expanded backup exceeds byte limit")
        infos[name] = info
    require("backup.json" in infos, "Missing backup manifest")
    with archive.open(infos["backup.json"]) as stream:
        payload = stream.read(MAX_MANIFEST + 1)
    require(len(payload) <= MAX_MANIFEST, "Backup manifest too large")
    manifest = json_loads(payload.decode("utf-8"))
    version = manifest.get("bank_format") if isinstance(manifest, dict) else None
    hashes = schema_hashes(version)
    validate_schema("bank-backup-v3" if version == "3.0" else "bank-backup", manifest)
    require(manifest["schema_hashes"] == hashes, "Backup schema identity differs")
    expected = {}
    total = 0
    for item in manifest["files"]:
        name = item["path"]
        require(bool(MEMBER.fullmatch(name)), f"Unsafe manifest path: {name}")
        require(name not in expected, "Duplicate manifest path")
        expected[name] = item
        require(
            name in infos and item["bytes"] == infos[name].file_size, "Backup file size differs"
        )
        total += item["bytes"]
    require(total <= MAX_PAYLOAD, "Backup payload exceeds byte limit")
    require(set(infos) == set(expected) | {"backup.json"}, "Backup inventory differs")
    return manifest, infos


def _write_tree(path: Path, data: bytes) -> None:
    path = safe_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    storage.write_new(path, data)


@contextmanager
def checked_backup(input_path: Path):
    """Verify every hash and the complete reconstructed history in isolated staging."""
    input_path = safe_path(input_path)
    _zip_shape(input_path)
    try:
        with (
            zipfile.ZipFile(input_path) as archive,
            tempfile.TemporaryDirectory(prefix="jeb-bank-backup-check-") as temporary,
        ):
            manifest, infos = _manifest(archive)
            tree = safe_path(Path(temporary))
            (tree / "snapshots").mkdir()
            (tree / "staging").mkdir()
            for item in manifest["files"]:
                with archive.open(infos[item["path"]]) as stream:
                    data = stream.read(MAX_FILE_BYTES + 1)
                require(
                    len(data) == item["bytes"] and sha256(data) == item["sha256"],
                    f"Backup checksum mismatch: {item['path']}",
                )
                _write_tree(tree / item["path"], data)
            # Empty record directories are structural and carry no ZIP members.
            for snapshot in (tree / "snapshots").iterdir():
                (snapshot / "records").mkdir(exist_ok=True)
            state = storage.read_managed(tree)
            require(state["head"] == manifest["head"], "Backup HEAD differs from manifest")
            require(
                state["workspace"]["workspace_id"] == manifest["workspace_id"],
                "Backup workspace differs from manifest",
            )
            require(
                set(committed_paths(state)) == {item["path"] for item in manifest["files"]},
                "Backup contains noncommitted or missing history files",
            )
            yield manifest, tree, state
    except (zipfile.BadZipFile, RuntimeError, NotImplementedError, EOFError, zlib.error) as exc:
        raise JebError(f"Invalid backup archive: {exc}") from exc


def verify(input_path: Path) -> dict:
    with checked_backup(input_path) as (manifest, _, state):
        return {
            "valid_backup": True,
            "workspace_id": manifest["workspace_id"],
            "head": state["head"],
            "snapshots": len(state["chain"]),
            "files": len(manifest["files"]),
            "privacy": "private_backup",
            "approvals_created": 0,
        }


def create(root: Path, output: Path) -> dict:
    root, output = safe_path(root), safe_path(output)
    require(not output.is_relative_to(root), "Backup output must be outside the bank")
    require(not output.exists(), "Backup output already exists")
    require(output.parent.is_dir(), "Backup parent directory must exist")
    storage.layout(root)
    # A cooperative writer cannot move HEAD while bytes are copied and verified.
    with (
        storage.writer_lock(root),
        tempfile.TemporaryDirectory(prefix=".jeb-bank-backup-", dir=output.parent) as temporary,
    ):
        state = storage.read_managed(root)
        entries, total = [], 0
        staged = Path(temporary) / "backup.zip"
        with zipfile.ZipFile(staged, "w", allowZip64=False) as archive:
            for name in committed_paths(state):
                data = read_bytes(safe_path(root / name), MAX_FILE_BYTES)
                total += len(data)
                require(total <= MAX_PAYLOAD, "Backup payload exceeds byte limit")
                entries.append({"path": name, "bytes": len(data), "sha256": sha256(data)})
                archive.writestr(_zip_info(name), data)
            manifest = {
                "schema_version": "1.0",
                "bank_format": state["workspace"]["schema_version"],
                "scope": "committed_bank_only",
                "privacy": "private_backup",
                "created_at": storage.now(),
                "workspace_id": state["workspace"]["workspace_id"],
                "head": state["head"],
                "schema_hashes": schema_hashes(state["workspace"]["schema_version"]),
                "files": entries,
            }
            validate_schema(
                "bank-backup-v3" if manifest["bank_format"] == "3.0" else "bank-backup", manifest
            )
            payload = canonical(manifest)
            require(len(payload) <= MAX_MANIFEST, "Backup manifest too large")
            archive.writestr(_zip_info("backup.json"), payload)
        staged.chmod(0o600)
        with staged.open("r+b") as stream:
            os.fsync(stream.fileno())
        result = verify(staged)
        # Atomic no-clobber publication; same-filesystem hard link, no replacement.
        os.link(staged, safe_path(output))
        storage.sync_directory(output.parent)
        with output.open("rb") as stream:
            output_hash = hashlib.file_digest(stream, "sha256").hexdigest()
        return {**result, "output": str(output), "sha256": output_hash, "pending_excluded": True}


def _cleanup_created(destination: Path, created: list[Path]) -> None:
    """Remove only paths created by this restore; never recursively delete a tree."""
    for path in reversed(created):
        path = safe_path(path)
        require(path.is_relative_to(destination), "Restore cleanup escaped destination")
        if path.is_dir():
            path.rmdir()  # Refuse unexpected contents.
        else:
            path.unlink(missing_ok=True)


def restore(input_path: Path, destination: Path) -> dict:
    destination = safe_path(destination)
    require(not destination.exists(), "Restore destination already exists")
    require(destination.parent.is_dir(), "Restore parent directory must exist")
    with checked_backup(input_path) as (manifest, tree, state):
        created = []
        try:
            destination.mkdir(mode=0o700)  # Never replace even an empty directory.
            created.append(destination)
            for name in ("snapshots", "staging"):
                path = destination / name
                path.mkdir()
                created.append(path)
            lock = destination / ".writer.lock"
            # Track the lock before acquiring it so errors cannot orphan our file.
            created.append(lock)
            storage.write_new(lock, b"\0")
            with storage.writer_lock(destination):
                for item in manifest["files"]:
                    name = item["path"]
                    if name == "HEAD.json":
                        continue
                    path = safe_path(destination / name)
                    missing = []
                    parent = path.parent
                    while not parent.exists():
                        missing.append(parent)
                        parent = parent.parent
                    for parent in reversed(missing):
                        parent.mkdir()
                        created.append(parent)
                    created.append(path)
                    storage.write_new(path, read_bytes(tree / name, MAX_FILE_BYTES))
                for snapshot in state["chain"]:
                    path = (
                        destination
                        / "snapshots"
                        / snapshot["manifest"]["transaction_id"]
                        / "records"
                    )
                    if not path.exists():
                        path.mkdir()
                        created.append(path)
                # Keep the bank unreadable until all its data has been copied.
                for path in reversed(created):
                    if path.is_dir():
                        storage.sync_directory(path)
                created.append(destination / "HEAD.json")
                temporary_head = destination / "staging" / f"head-{uuid4()}.json"
                storage.write_new(temporary_head, read_bytes(tree / "HEAD.json", MAX_FILE_BYTES))
                os.replace(temporary_head, safe_path(destination / "HEAD.json"))
                storage.sync_directory(destination)
                restored = storage.read_managed(destination)
                require(restored["head"] == state["head"], "Restored HEAD differs")
            return {
                "destination": str(destination),
                "workspace_id": manifest["workspace_id"],
                "head": manifest["head"],
                "snapshots": len(restored["chain"]),
                "files": len(manifest["files"]),
                "approvals_created": 0,
            }
        except BaseException:
            # HEAD temp files belong to this restore but are not in the archive inventory.
            if created:
                staging = safe_path(destination / "staging")
                if staging.is_dir():
                    for path in staging.iterdir():
                        safe_path(path)
                        require(
                            bool(re.fullmatch(rf"head-{UUID}\.json", path.name)),
                            "Unexpected restore staging contents; preserved for inspection",
                        )
                        path.unlink()
                _cleanup_created(destination, created)
            raise
