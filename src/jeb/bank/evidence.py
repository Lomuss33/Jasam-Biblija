"""Revision-bound claim/evidence drafts; no canonical promotion or human approvals."""

from __future__ import annotations

import os
import tempfile
from importlib.resources import files
from pathlib import Path
from uuid import uuid4

from jeb.bank import storage
from jeb.bank.validation import MAX_FILE_BYTES, safe_path
from jeb.core import canonical, digest, latin, latin_tree, require, sha256, validate_schema

SCHEMAS = ("bank-evidence-draft", "bank-evidence-packet")


def schema_hashes() -> dict:
    return {
        name: sha256(files("jeb").joinpath("schemas", name + ".json").read_bytes())
        for name in SCHEMAS
    }


def reference(state: dict, identity: str, kind: str) -> dict:
    require(identity in state["records"], f"Missing {kind} record: {identity}")
    record = state["records"][identity]
    require(record["kind"] == kind, f"Expected {kind} record: {identity}")
    return {
        "record_id": identity,
        "revision_id": record["revision_id"],
        "record_sha256": state["file_hashes"][identity]["record"],
        "body_sha256": record["body_sha256"],
    }


def _nonblank_tree(value) -> None:
    if isinstance(value, str):
        require(bool(value.strip()), "Blank evidence draft text")
    elif isinstance(value, dict):
        for item in value.values():
            _nonblank_tree(item)
    elif isinstance(value, list):
        for item in value:
            _nonblank_tree(item)


def check_draft(state: dict, draft: dict) -> tuple[list[dict], list[dict]]:
    validate_schema("bank-evidence-draft", draft)
    latin_tree(draft, "authored bank evidence draft")
    _nonblank_tree(draft)
    identities, claims, bindings, statuses = set(), {}, {}, []
    for claim in draft["claims"]:
        identity = claim["id"]
        require(identity not in identities, "Duplicate claim/evidence ID")
        require(identity not in state["records"], "Draft ID collides with bank record")
        identities.add(identity)
        claims[identity] = claim
        subject = claim["subject_id"]
        bindings[subject] = reference(state, subject, "entity")
    for evidence in draft["evidence"]:
        identity = evidence["id"]
        require(identity not in identities, "Duplicate claim/evidence ID")
        require(identity not in state["records"], "Draft ID collides with bank record")
        identities.add(identity)
        require(evidence["claim_id"] in claims, "Evidence names a missing claim")
        source = evidence["source_id"]
        bindings[source] = reference(state, source, "source")
        locator = evidence["locator"]
        verification = "declared_only"
        if locator["type"] == "text_span":
            require(source in state["bodies"], "Text span requires locally bound source body")
            body = state["bodies"][source]
            start, end = locator["start"], locator["end"]
            require(0 <= start < end <= len(body), "Text span is outside bound body")
            require(
                body[start:end] == locator["exact"],
                "Text span does not match exact source text",
            )
            verification = "local_text_match"
        elif locator["type"] == "page":
            require(
                locator["pdf_page"] is not None or locator["printed_page"] is not None,
                "Page locator requires PDF page or printed page label",
            )
        elif locator["type"] == "time_range":
            require(locator["start_ms"] < locator["end_ms"], "Invalid time range")
        statuses.append(
            {
                "evidence_id": identity,
                "locator_verification": verification,
                "review_state": "unreviewed",
            }
        )
    return [bindings[key] for key in sorted(bindings)], statuses


def check_packet(state: dict, packet: dict) -> list[dict]:
    require(state["workspace"]["schema_version"] == "2.0", "Draft packets require format2.0")
    validate_schema("bank-evidence-packet", packet)
    require(
        packet["workspace_id"] == state["workspace"]["workspace_id"], "Foreign evidence workspace"
    )
    require(packet["base_head"] == state["head"], "Stale evidence packet: bank HEAD changed")
    require(packet["schema_hashes"] == schema_hashes(), "Evidence schema identity changed")
    envelope = {key: value for key, value in packet.items() if key != "packet_sha256"}
    require(packet["packet_sha256"] == digest(envelope), "Evidence packet hash mismatch")
    require(bool(packet["prepared_by"]["id"].strip()), "Blank evidence actor")
    latin(packet["prepared_by"]["id"], "evidence actor")
    require(
        storage.timestamp(packet["created_at"])
        >= storage.timestamp(state["workspace"]["created_at"]),
        "Evidence packet predates workspace",
    )
    bindings, statuses = check_draft(state, packet["draft"])
    require(packet["bindings"] == bindings, "Evidence revision bindings differ")
    return statuses


def _publish(root: Path, output: Path, value: dict) -> None:
    root, output = safe_path(root), safe_path(output)
    require(not output.is_relative_to(root), "Evidence artifacts must stay outside managed bank")
    require(not output.exists(), "Evidence output already exists")
    require(output.parent.is_dir(), "Evidence output parent must exist")
    payload = canonical(value)
    require(len(payload) <= MAX_FILE_BYTES, "Evidence artifact exceeds byte limit")
    with tempfile.TemporaryDirectory(prefix=".jeb-evidence-", dir=output.parent) as temporary:
        path = Path(temporary) / "artifact.json"
        storage.write_new(path, payload)
        path.chmod(0o600)
        os.link(path, safe_path(output))
        storage.sync_directory(output.parent)


def prepare(root: Path, input_path: Path, output: Path, actor: str, actor_kind: str) -> dict:
    state = storage.read_managed(root)
    draft = storage.document(input_path)
    bindings, _ = check_draft(state, draft)
    packet = {
        "schema_version": "1.0",
        "bank_format": "2.0",
        "packet_id": str(uuid4()),
        "workspace_id": state["workspace"]["workspace_id"],
        "base_head": state["head"],
        "created_at": storage.now(),
        "prepared_by": {"id": actor, "kind": actor_kind},
        "review_state": "unreviewed",
        "approval_authority": "none",
        "schema_hashes": schema_hashes(),
        "draft": draft,
        "bindings": bindings,
    }
    packet["packet_sha256"] = digest(packet)
    check_packet(state, packet)
    _publish(root, output, packet)
    return {
        "output": str(output),
        "packet_id": packet["packet_id"],
        "packet_sha256": packet["packet_sha256"],
        "claims": len(draft["claims"]),
        "evidence": len(draft["evidence"]),
        "review_state": "unreviewed",
        "approval_authority": "none",
        "approvals_created": 0,
    }


def validate(root: Path, input_path: Path) -> dict:
    state = storage.read_managed(root)
    packet = storage.document(input_path)
    statuses = check_packet(state, packet)
    linked = {item["claim_id"] for item in packet["draft"]["evidence"]}
    return {
        "valid_packet": True,
        "packet_sha256": packet["packet_sha256"],
        "claims": len(packet["draft"]["claims"]),
        "evidence": statuses,
        "claims_without_evidence": sorted(
            item["id"] for item in packet["draft"]["claims"] if item["id"] not in linked
        ),
        "review_state": "unreviewed",
        "approval_authority": "none",
        "approvals_created": 0,
    }


def inspect(root: Path, input_path: Path) -> dict:
    state = storage.read_managed(root)
    packet = storage.document(input_path)
    statuses = check_packet(state, packet)
    records = {
        binding["record_id"]: state["records"][binding["record_id"]]
        for binding in packet["bindings"]
    }
    return {
        "packet": packet,
        "bound_records": records,
        "locator_checks": statuses,
        "limitations": [
            "Structural validation is not historical corroboration or human review.",
            "Declared page/section/time locators have no verified media artifact.",
            "Packet is a private draft outside canonical bank and its backups.",
        ],
        "approvals_created": 0,
    }
