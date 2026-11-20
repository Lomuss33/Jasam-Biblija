"""Immutable full snapshots and one atomic HEAD; local cooperative single writer."""

from __future__ import annotations

import copy
import os
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from jeb.bank.validation import (
    ID_PATTERN,
    MAX_FILE_BYTES,
    children,
    load_snapshot,
    safe_path,
)
from jeb.core import (
    JebError,
    canonical,
    digest,
    latin,
    read_bytes,
    require,
    sha256,
    validate_schema,
)

MAX_HISTORY = 128
MAX_HISTORY_BYTES = 128 * 1024 * 1024


def format_schema(kind: str, version: str) -> str:
    require(version in ("2.0", "3.0"), "Unsupported managed bank version")
    if kind == "transaction" and version == "2.0":
        return "bank-transaction"
    return f"bank-{kind}-v{version[0]}"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def document(path: Path) -> dict:
    from jeb.core import json_loads

    return json_loads(read_bytes(safe_path(path), MAX_FILE_BYTES).decode("utf-8"))


def write_new(path: Path, data: bytes) -> None:
    path = safe_path(path)
    require(len(data) <= MAX_FILE_BYTES, "Snapshot file exceeds size limit")
    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def sync_directory(path: Path) -> None:
    # Windows has no portable directory fsync; do not promise power-loss durability.
    if os.name != "nt":
        descriptor = os.open(path, os.O_RDONLY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)


@contextmanager
def writer_lock(root: Path):
    """Kernel-released lock; persistent lock file is never deleted as 'stale'."""
    path = safe_path(root / ".writer.lock")
    with path.open("a+b") as stream:
        if path.stat().st_size == 0:
            stream.write(b"\0")
            stream.flush()
        stream.seek(0)
        try:
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise JebError("Bank writer is busy; retry after the other writer exits") from exc
        try:
            yield
        finally:
            stream.seek(0)
            if os.name == "nt":
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def layout(root: Path) -> dict:
    root = safe_path(root)
    names = {p.name for p in children(root, 7)}
    require(
        {"workspace.json", "snapshots", "staging"} <= names
        and names <= {"workspace.json", "snapshots", "staging", "HEAD.json", ".writer.lock"},
        "Managed bank requires its own workspace/snapshots/staging directory",
    )
    for name in ("snapshots", "staging"):
        require(safe_path(root / name).is_dir(), f"Missing {name} directory")
    workspace = document(root / "workspace.json")
    require(isinstance(workspace, dict), "Bank workspace must be an object")
    validate_schema(format_schema("workspace", workspace.get("schema_version")), workspace)
    require(bool(workspace["title"].strip()), "Blank workspace title")
    latin(workspace["title"], "bank workspace")
    return workspace


def head_at(root: Path) -> dict | None:
    path = safe_path(root / "HEAD.json")
    if not path.exists():
        return None
    value = document(path)
    validate_schema("bank-head", value)
    return value


def snapshot_at(path: Path, workspace: dict) -> dict:
    """Bind exact file bytes, including unchanged records' original spelling."""
    manifest_bytes = read_bytes(safe_path(path / "manifest.json"), MAX_FILE_BYTES)
    manifest = document(path / "manifest.json")
    validate_schema(format_schema("transaction", workspace["schema_version"]), manifest)
    require(manifest["transaction_id"] == path.name, "Transaction directory ID mismatch")
    local_workspace, records, bodies = load_snapshot(
        path, record_schema=format_schema("record", workspace["schema_version"]), managed=True
    )
    expected_workspace = {**workspace, "schema_version": "1.0"}
    require(local_workspace == expected_workspace, "Snapshot workspace metadata changed")
    file_hashes = {}
    byte_count = len(manifest_bytes) + (path / "workspace.json").stat().st_size
    for identity, record in records.items():
        directory = path / "records" / identity
        raw = read_bytes(directory / "record.json", MAX_FILE_BYTES)
        file_hashes[identity] = {"record": sha256(raw), "body": record["body_sha256"]}
        byte_count += len(raw)
        if identity in bodies:
            byte_count += len(bodies[identity].encode("utf-8"))
        require(
            timestamp(record["revised_at"]) >= timestamp(record["created_at"]),
            "Revision predates record creation",
        )
        require(
            timestamp(manifest["created_at"]) >= timestamp(record["revised_at"]),
            "Commit predates a record revision",
        )
        require(bool(record["reason"].strip()), "Blank revision reason")
        latin(record["reason"], "revision reason")
    content_digest = digest(
        {
            "workspace": sha256(read_bytes(path / "workspace.json", MAX_FILE_BYTES)),
            "files": file_hashes,
        }
    )
    require(content_digest == manifest["snapshot_sha256"], "Snapshot hash mismatch")
    require(bool(manifest["reason"].strip()), "Blank transaction reason")
    latin(manifest["reason"], "transaction reason")
    return {
        "manifest": manifest,
        "manifest_sha256": sha256(manifest_bytes),
        "records": records,
        "bodies": bodies,
        "file_hashes": file_hashes,
        "bytes": byte_count,
        "path": path,
    }


def check_transition(previous: dict | None, current: dict, seen: set[str]) -> None:
    records = current["records"]
    manifest = current["manifest"]
    if previous is None:
        require(
            not records and manifest["changed_record"] is None, "Genesis snapshot must be empty"
        )
        return
    old = previous["records"]
    require(
        timestamp(manifest["created_at"]) >= timestamp(previous["manifest"]["created_at"]),
        "Transaction time moved backwards",
    )
    require(old.keys() <= records.keys(), "Snapshot deleted existing records")
    changed = {
        identity
        for identity in records
        if current["file_hashes"][identity] != previous["file_hashes"].get(identity)
    }
    require(
        changed == {manifest["changed_record"]}, "Transaction must change exactly its named record"
    )
    identity = manifest["changed_record"]
    record = records[identity]
    require(record["revision_id"] not in seen, "Revision ID reused in history")
    seen.add(record["revision_id"])
    if identity in old:
        prior = old[identity]
        require(record["parent_revision"] == prior["revision_id"], "Broken revision parent")
        for field in ("id", "workspace_id", "kind", "created_at"):
            require(record[field] == prior[field], f"Immutable record field changed: {field}")
        require(
            timestamp(record["revised_at"]) >= timestamp(prior["revised_at"]),
            "Record revision time moved backwards",
        )
    else:
        require(record["parent_revision"] is None, "New record has a parent")


def read_managed(root: Path) -> dict:
    root = safe_path(root)
    workspace = layout(root)
    head = head_at(root)
    require(head is not None, "No committed HEAD; inspect bank recover")
    pointer, chain, visited, total = head, [], set(), 0
    while pointer is not None:
        transaction = pointer["transaction_id"]
        require(transaction not in visited and len(chain) < MAX_HISTORY, "History cycle or limit")
        visited.add(transaction)
        state = snapshot_at(safe_path(root / "snapshots" / transaction), workspace)
        require(state["manifest_sha256"] == pointer["manifest_sha256"], "Manifest hash mismatch")
        total += state["bytes"]
        require(total <= MAX_HISTORY_BYTES, "History exceeds byte limit")
        chain.append(state)
        pointer = state["manifest"]["parent_head"]
    from jeb.bank.references import add_revision

    previous, seen, revisions = None, set(), {}
    for state in reversed(chain):
        check_transition(previous, state, seen)
        add_revision(state, revisions)
        previous = state
    return {
        **chain[0],
        "head": head,
        "workspace": workspace,
        "chain": chain,
        "revisions": revisions,
    }


def publish_head(root: Path, pointer: dict) -> None:
    temporary = safe_path(root / "staging" / f"head-{uuid4()}.json")
    write_new(temporary, canonical(pointer))
    os.replace(temporary, safe_path(root / "HEAD.json"))
    sync_directory(root)


def check_candidate(previous: dict | None, candidate: dict) -> None:
    from jeb.bank.references import add_revision

    seen = (
        {r["revision_id"] for s in previous["chain"] for r in s["records"].values()}
        if previous
        else set()
    )
    check_transition(previous, candidate, seen)
    add_revision(candidate, dict(previous["revisions"]) if previous else {})
    require((len(previous["chain"]) if previous else 0) < MAX_HISTORY, "History limit")
    require(
        (sum(s["bytes"] for s in previous["chain"]) if previous else 0) + candidate["bytes"]
        <= MAX_HISTORY_BYTES,
        "History exceeds byte limit",
    )


def stage_snapshot(
    root: Path,
    workspace: dict,
    previous: dict | None,
    records: dict,
    bodies: dict,
    changed: str | None,
    reason: str,
) -> dict:
    transaction = str(uuid4())
    stage = safe_path(root / "staging" / transaction)
    stage.mkdir()
    (stage / "records").mkdir()
    write_new(stage / "workspace.json", canonical({**workspace, "schema_version": "1.0"}))
    file_hashes = {}
    for identity, record in records.items():
        directory = stage / "records" / identity
        directory.mkdir()
        if previous is not None and identity != changed:
            raw = read_bytes(
                previous["path"] / "records" / identity / "record.json", MAX_FILE_BYTES
            )
        else:
            raw = canonical(record)
        write_new(directory / "record.json", raw)
        if identity in bodies:
            write_new(directory / "body.md", bodies[identity].encode("utf-8"))
        file_hashes[identity] = {"record": sha256(raw), "body": record["body_sha256"]}
        sync_directory(directory)
    manifest = {
        "schema_version": workspace["schema_version"],
        "transaction_id": transaction,
        "parent_head": None if previous is None else previous["head"],
        "snapshot_sha256": digest(
            {
                "workspace": sha256(read_bytes(stage / "workspace.json", MAX_FILE_BYTES)),
                "files": file_hashes,
            }
        ),
        "changed_record": changed,
        "created_at": now(),
        "reason": reason,
    }
    # Last file in the prepared directory is the complete, validated manifest.
    write_new(stage / "manifest.json", canonical(manifest))
    candidate = snapshot_at(stage, workspace)
    check_candidate(previous, candidate)
    sync_directory(stage / "records")
    sync_directory(stage)
    destination = safe_path(root / "snapshots" / transaction)
    require(not destination.exists(), "Transaction ID already exists")
    os.rename(stage, destination)
    sync_directory(root / "snapshots")
    pointer = {"transaction_id": transaction, "manifest_sha256": candidate["manifest_sha256"]}
    publish_head(root, pointer)
    return pointer


def initialize(root: Path, title: str, version: str = "2.0") -> dict:
    root = safe_path(root)
    require(bool(title.strip()), "Blank workspace title")
    latin(title, "workspace title")
    workspace = {
        "schema_version": version,
        "workspace_id": str(uuid4()),
        "title": title,
        "created_at": now(),
    }
    validate_schema(format_schema("workspace", version), workspace)
    root.mkdir()  # Never reuse/overwrite an existing directory.
    (root / "snapshots").mkdir()
    (root / "staging").mkdir()
    write_new(root / "workspace.json", canonical(workspace))
    with writer_lock(root):
        pointer = stage_snapshot(root, workspace, None, {}, {}, None, "Initialize workspace")
    return {"workspace_id": workspace["workspace_id"], "head": pointer, "approvals_created": 0}


def save_record(
    root: Path,
    content: dict,
    actor: str,
    actor_kind: str,
    reason: str,
    body: str | None = None,
    record_id: str | None = None,
    expected_revision: str | None = None,
    *,
    expected_head: dict | None = None,
) -> dict:
    root = safe_path(root)
    # Reject legacy spaces before creating even the lock file.
    layout(root)
    require(
        isinstance(content, dict)
        and set(content) == {"kind", "title", "data", "visibility", "processing_state"},
        "Input requires exactly kind/title/data/visibility/processing_state",
    )
    require(bool(reason.strip()), "A revision reason is required")
    latin(reason, "revision reason")
    with writer_lock(root):
        previous = read_managed(root)
        require(
            expected_head is None or previous["head"] == expected_head,
            "Bank HEAD changed; retry operation",
        )
        records, bodies = copy.deepcopy(previous["records"]), dict(previous["bodies"])
        if record_id is None:
            require(expected_revision is None, "Create cannot name an expected revision")
            identity, prior = str(uuid4()), None
        else:
            require(bool(ID_PATTERN.fullmatch(record_id)), "Unsafe record ID")
            require(record_id in records, "Record not found")
            identity, prior = record_id, records[record_id]
            require(
                expected_revision == prior["revision_id"], "Revision conflict; reload and compare"
            )
        when = now()
        record = {
            **copy.deepcopy(content),
            "schema_version": previous["workspace"]["schema_version"],
            "workspace_id": previous["workspace"]["workspace_id"],
            "id": identity,
            "created_at": prior["created_at"] if prior else when,
            "recorded_by": {"id": actor, "kind": actor_kind},
            "revision_id": str(uuid4()),
            "parent_revision": prior["revision_id"] if prior else None,
            "revised_at": when,
            "reason": reason,
            "body_sha256": sha256(body.encode("utf-8")) if body is not None else None,
        }
        validate_schema(format_schema("record", record["schema_version"]), record)
        records[identity] = record
        if body is None:
            bodies.pop(identity, None)
        else:
            bodies[identity] = body
        pointer = stage_snapshot(
            root, previous["workspace"], previous, records, bodies, identity, reason
        )
    return {
        "id": identity,
        "revision_id": record["revision_id"],
        "head": pointer,
        "approvals_created": 0,
    }


def history(root: Path, identity: str) -> dict:
    require(bool(ID_PATTERN.fullmatch(identity)), "Unsafe record ID")
    state = read_managed(root)
    require(identity in state["records"], "Record not found")
    revisions = []
    for snapshot in reversed(state["chain"]):
        if snapshot["manifest"]["changed_record"] == identity:
            revisions.append(
                {
                    "transaction_id": snapshot["manifest"]["transaction_id"],
                    "record": snapshot["records"][identity],
                    "body": snapshot["bodies"].get(identity),
                }
            )
    return {"id": identity, "revisions": revisions}


def recover(root: Path, transaction: str | None = None) -> dict:
    root = safe_path(root)
    workspace = layout(root)
    with writer_lock(root):
        head = head_at(root)
        previous = read_managed(root) if head else None
        if transaction is None:
            active = (
                {s["manifest"]["transaction_id"] for s in previous["chain"]} if previous else set()
            )
            pending = []
            for area in ("staging", "snapshots"):
                for path in children(root / area, 10_000):
                    if path.name in active:
                        continue
                    status = "incomplete"
                    if ID_PATTERN.fullmatch(path.name) and path.is_dir():
                        try:
                            candidate = snapshot_at(path, workspace)
                            if candidate["manifest"]["parent_head"] == head:
                                check_candidate(previous, candidate)
                                status = "prepared"
                            else:
                                status = "conflict"
                        except (OSError, ValueError, UnicodeError):
                            pass
                    pending.append({"name": path.name, "area": area, "status": status})
            return {"head": head, "pending": pending, "approvals_created": 0}
        require(bool(ID_PATTERN.fullmatch(transaction)), "Unsafe transaction ID")
        if head and head["transaction_id"] == transaction:
            return {"head": head, "already_committed": True, "approvals_created": 0}
        stage = safe_path(root / "staging" / transaction)
        final = safe_path(root / "snapshots" / transaction)
        require(not (stage.exists() and final.exists()), "Ambiguous transaction locations")
        path = stage if stage.exists() else final
        candidate = snapshot_at(path, workspace)
        require(candidate["manifest"]["parent_head"] == head, "Recovery conflict: HEAD changed")
        check_candidate(previous, candidate)
        if path == stage:
            os.rename(stage, final)
            sync_directory(root / "snapshots")
        pointer = {"transaction_id": transaction, "manifest_sha256": candidate["manifest_sha256"]}
        publish_head(root, pointer)
        return {"head": pointer, "approvals_created": 0}


def diff(root: Path, identity: str, from_revision: str, to_revision: str) -> dict:
    from difflib import unified_diff

    versions = {
        item["record"]["revision_id"]: item for item in history(root, identity)["revisions"]
    }
    require(from_revision in versions and to_revision in versions, "Revision not in record history")
    old, new = versions[from_revision], versions[to_revision]
    return {
        "id": identity,
        "from_revision": from_revision,
        "to_revision": to_revision,
        "metadata_diff": "".join(
            unified_diff(
                canonical(old["record"]).decode("utf-8").splitlines(keepends=True),
                canonical(new["record"]).decode("utf-8").splitlines(keepends=True),
                fromfile=from_revision,
                tofile=to_revision,
            )
        ),
        "body_diff": "".join(
            unified_diff(
                (old["body"] or "").splitlines(keepends=True),
                (new["body"] or "").splitlines(keepends=True),
                fromfile=from_revision,
                tofile=to_revision,
            )
        ),
    }
