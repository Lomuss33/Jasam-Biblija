"""Bounded read-only validation of initial bank snapshots, with no network IO."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlsplit

from jeb.core import JebError, digest, latin, read_bytes, require, sha256, validate_schema

MAX_RECORDS = 10_000
MAX_TOTAL_BYTES = 64 * 1024 * 1024
MAX_FILE_BYTES = 1024 * 1024
ID_PATTERN = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}")


def safe_path(path: Path) -> Path:
    """Reject links/junctions before resolving; never follow a directory alias."""
    path = Path(path.absolute())
    for part in (path, *path.parents):
        require(not part.is_symlink() and not part.is_junction(), f"Linked bank path: {part}")
    return path


def children(path: Path, limit: int) -> list[Path]:
    result = []
    for child in path.iterdir():
        require(len(result) < limit, f"Too many bank entries in {path}")
        result.append(safe_path(child))
    return sorted(result)


def load_snapshot(
    root: Path, *, record_schema: str = "bank-record", managed: bool = False
) -> tuple[dict, dict[str, dict], dict[str, str]]:
    """Validate the entire supplied bank before returning any record."""
    root = safe_path(root)
    require(root.is_dir(), f"Bank directory not found: {root}")
    require(
        {p.name for p in children(root, 4)}
        == (
            {"workspace.json", "records", "manifest.json"}
            if managed
            else {"workspace.json", "records"}
        ),
        "Initial bank requires only workspace.json and records/; use a dedicated directory",
    )
    total = 0

    def payload(path: Path) -> bytes:
        nonlocal total
        data = read_bytes(safe_path(path), MAX_FILE_BYTES)
        total += len(data)
        require(total <= MAX_TOTAL_BYTES, "Bank snapshot exceeds total byte limit")
        return data

    def document(path: Path) -> dict:
        from jeb.core import json_loads

        try:
            return json_loads(payload(path).decode("utf-8"))
        except (ValueError, UnicodeError) as exc:
            raise JebError(f"{path}: {exc}") from exc

    # Use the same bounded reader for the workspace and every record.
    workspace = document(root / "workspace.json")
    validate_schema("bank-workspace", workspace)
    require(workspace["title"].strip() != "", "Workspace title is blank")
    latin(workspace["title"], "bank workspace title")
    records_dir = safe_path(root / "records")
    require(records_dir.is_dir(), "records must be a directory")
    records, bodies = {}, {}
    revisions = set()
    for directory in children(records_dir, MAX_RECORDS):
        require(
            bool(ID_PATTERN.fullmatch(directory.name)) and directory.is_dir(),
            f"Record directory must be a lowercase UUID4: {directory.name}",
        )
        entries = {p.name for p in children(directory, 3)}
        require(
            "record.json" in entries and entries <= {"record.json", "body.md"},
            f"Unexpected record files: {directory}",
        )
        record = document(directory / "record.json")
        try:
            validate_schema(record_schema, record)
            require(record["id"] == directory.name, "Record ID differs from directory")
            require(record["workspace_id"] == workspace["workspace_id"], "Foreign workspace ID")
            require(record["revision_id"] not in revisions, "Duplicate revision ID")
            revisions.add(record["revision_id"])
            for name in ("title",):
                require(bool(record[name].strip()), f"Blank {name}")
                latin(record[name], f"bank record {name}")
            latin(record["recorded_by"]["id"], "bank actor")
            if record["kind"] == "source":
                for key in ("creator", "translator", "edition", "limitations"):
                    if record["data"][key] is not None:
                        latin(record["data"][key], f"bank source {key}")
                url = record["data"]["url"]
                if url is not None:
                    parsed = urlsplit(url)
                    require(
                        parsed.scheme == "https"
                        and bool(parsed.hostname)
                        and parsed.username is None
                        and parsed.password is None
                        and not any(char.isspace() or ord(char) < 32 for char in url),
                        "Source URL must be HTTPS without credentials or whitespace",
                    )
            if record["body_sha256"] is None:
                require("body.md" not in entries, "Unbound body.md")
            else:
                require("body.md" in entries, "Missing body.md")
                data = payload(directory / "body.md")
                require(sha256(data) == record["body_sha256"], "body.md hash mismatch")
                body = data.decode("utf-8")
                latin(body, "bank article body")
                bodies[record["id"]] = body
            records[record["id"]] = record
        except (ValueError, UnicodeError) as exc:
            raise JebError(f"{directory / 'record.json'}: {exc}") from exc
    for record in records.values():
        if record["kind"] == "article":
            for field, target_kind in (("subjects", "entity"), ("sources", "source")):
                for target in record["data"][field]:
                    require(target in records, f"{record['id']}/{field}: missing target {target}")
                    require(
                        records[target]["kind"] == target_kind,
                        f"{record['id']}/{field}: expected {target_kind}, got {target}",
                    )
    return workspace, records, bodies


def load_bank(root: Path) -> tuple[dict, dict[str, dict], dict[str, str]]:
    from jeb.core import read_json

    root = safe_path(root)
    workspace = read_json(safe_path(root / "workspace.json"))
    if isinstance(workspace, dict) and workspace.get("schema_version") in ("2.0", "3.0"):
        from jeb.bank.storage import read_managed

        state = read_managed(root)
        return state["workspace"], state["records"], state["bodies"]
    return load_snapshot(root)


def validate_bank(root: Path) -> dict:
    workspace, records, bodies = load_bank(root)
    return {
        "workspace_id": workspace["workspace_id"],
        "valid_records": len(records),
        "bound_bodies": len(bodies),
        "records_sha256": digest([records[key] for key in sorted(records)]),
        "validation_scope": (
            "committed_history_structure_and_integrity_only"
            if workspace["schema_version"] in ("2.0", "3.0")
            else "initial_snapshot_structure_and_integrity_only"
        ),
        "approvals_created": 0,
    }


def show_record(root: Path, record_id: str) -> dict:
    require(bool(ID_PATTERN.fullmatch(record_id)), "Record ID must be a lowercase UUID4")
    _, records, bodies = load_bank(root)
    require(record_id in records, f"Record not found: {record_id}")
    return {"record": records[record_id], "body": bodies.get(record_id)}
