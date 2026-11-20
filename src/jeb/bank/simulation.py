"""Opt-in synthetic v2 to v3 writer simulation; never a release migration."""

from __future__ import annotations

import copy
import os
import shutil
from pathlib import Path
from uuid import uuid4

from jeb.core import atomic_write, canonical, digest, require, sha256, validate_schema

from . import decision, storage
from .validation import safe_path, validate_bank


def simulate(root: Path, plan_path: Path, decision_path: Path, *, synthetic: bool = False) -> dict:
    """Create an isolated, marked synthetic target after binding checks."""
    require(synthetic, "Synthetic simulation requires explicit opt-in")
    root = safe_path(root)
    with storage.writer_lock(root):
        check = decision.validate(root, plan_path, decision_path)
        require(
            check["decision"] == "proceed" and check["can_write"],
            "Decision does not permit simulation",
        )
        target = safe_path(Path(check["target_path"]))
        require(
            "synthetic" in target.name.casefold(), "Synthetic target name must include synthetic"
        )
        require(not target.exists(), "Synthetic target already exists")
        state = storage.read_managed(root)
        require(
            state["workspace"]["schema_version"] == "2.0",
            "Simulation requires managed format 2.0",
        )
        staging = safe_path(target.parent / f".{target.name}.staging-{uuid4()}")
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            staging.mkdir()
            (staging / "snapshots").mkdir()
            (staging / "staging").mkdir()
            target_workspace = {
                **state["workspace"],
                "schema_version": "3.0",
                "title": f"{state['workspace']['title']} [SYNTHETIC MIGRATION]",
            }
            validate_schema("bank-workspace-v3", target_workspace)
            atomic_write(staging / "workspace.json", canonical(target_workspace), replace=False)

            previous_head = None
            for snapshot in reversed(state["chain"]):
                transaction = snapshot["manifest"]["transaction_id"]
                destination = staging / "snapshots" / transaction
                (destination / "records").mkdir(parents=True)
                local_workspace = {**target_workspace, "schema_version": "1.0"}
                atomic_write(
                    destination / "workspace.json", canonical(local_workspace), replace=False
                )
                file_hashes = {}
                for identity, source_record in sorted(snapshot["records"].items()):
                    record = copy.deepcopy(source_record)
                    record["schema_version"] = "3.0"
                    validate_schema("bank-record-v3", record)
                    record_bytes = canonical(record)
                    record_path = destination / "records" / identity / "record.json"
                    record_path.parent.mkdir()
                    atomic_write(record_path, record_bytes, replace=False)
                    if identity in snapshot["bodies"]:
                        atomic_write(
                            record_path.parent / "body.md",
                            snapshot["bodies"][identity].encode("utf-8"),
                            replace=False,
                        )
                    file_hashes[identity] = {
                        "record": sha256(record_bytes),
                        "body": record["body_sha256"],
                    }
                manifest = copy.deepcopy(snapshot["manifest"])
                manifest["schema_version"] = "3.0"
                manifest["parent_head"] = previous_head
                manifest["snapshot_sha256"] = digest(
                    {"workspace": sha256(canonical(local_workspace)), "files": file_hashes}
                )
                manifest_bytes = canonical(manifest)
                atomic_write(destination / "manifest.json", manifest_bytes, replace=False)
                previous_head = {
                    "transaction_id": transaction,
                    "manifest_sha256": sha256(manifest_bytes),
                }
            require(previous_head is not None, "Synthetic source has no committed HEAD")
            atomic_write(staging / "HEAD.json", canonical(previous_head), replace=False)
            validate_bank(staging)
            os.rename(staging, target)
        except Exception:
            if staging.exists():
                shutil.rmtree(staging)
            raise
    summary = validate_bank(target)
    return {
        "synthetic": True,
        "releasable": False,
        "target": str(target),
        "workspace_id": summary["workspace_id"],
        "head": previous_head,
        "valid_records": summary["valid_records"],
        "approvals_created": 0,
    }
