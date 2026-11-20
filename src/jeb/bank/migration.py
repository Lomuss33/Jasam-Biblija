"""Read-only v2 to v3 migration planning; never creates a target bank."""

from __future__ import annotations

from pathlib import Path

from jeb.core import atomic_write, canonical, digest, json_loads, read_bytes, require

from .storage import read_managed
from .validation import safe_path

SUPPORTED_KINDS = ("article", "entity", "source")
MAX_REPORT_BYTES = 16 * 1024 * 1024


def plan(root: Path) -> dict:
    """Return a deterministic migration plan bound to the current v2 HEAD."""
    root = safe_path(root)
    state = read_managed(root)
    workspace = state["workspace"]
    require(workspace["schema_version"] == "2.0", "Migration plan requires managed format 2.0")

    by_id: dict[str, dict] = {}
    revision_rows: dict[str, list[dict]] = {}
    for snapshot in reversed(state["chain"]):
        for identity, record in sorted(snapshot["records"].items()):
            by_id[identity] = record
            revision_rows.setdefault(identity, []).append(
                {
                    "revision_id": record["revision_id"],
                    "source_record_sha256": snapshot["file_hashes"][identity]["record"],
                    "body_sha256": record["body_sha256"],
                }
            )

    rows = []
    blocked = 0
    for identity in sorted(revision_rows):
        record = by_id[identity]
        blockers = []
        if record["kind"] not in SUPPORTED_KINDS:
            blockers.append(f"unsupported_v2_kind:{record['kind']}")
        action = "blocked" if blockers else "copy"
        blocked += action == "blocked"
        rows.append(
            {
                "record_id": identity,
                "kind": record["kind"],
                "source_revision_ids": [item["revision_id"] for item in revision_rows[identity]],
                "target_record_id": None if blockers else identity,
                "target_revision_ids": (
                    [] if blockers else [item["revision_id"] for item in revision_rows[identity]]
                ),
                "revisions": revision_rows[identity],
                "action": action,
                "blockers": blockers,
            }
        )

    return {
        "report_version": "1.0",
        "mode": "dry_run",
        "source_format": "2.0",
        "target_format": "3.0",
        "source_workspace_id": workspace["workspace_id"],
        "source_head": {
            "transaction_id": state["head"]["transaction_id"],
            "manifest_sha256": state["head"]["manifest_sha256"],
        },
        "source_records_sha256": digest(
            [state["records"][key] for key in sorted(state["records"])]
        ),
        "counts": {
            "copy": len(rows) - blocked,
            "blocked": blocked,
            "claims": 0,
            "evidence": 0,
        },
        "records": rows,
        "external_inputs": {"f3a_packets": "excluded"},
        "approvals_created": 0,
        "writable": False,
    }


def write_plan(root: Path, output: Path) -> dict:
    """Write a no-clobber report outside the source bank."""
    root = safe_path(root)
    output = Path(output).absolute()
    require(not output.is_relative_to(root), "Migration report must be outside bank-root")
    require(not output.exists(), "Migration report already exists")
    report = plan(root)
    atomic_write(output, canonical(report), replace=False)
    return {"output": str(output), **report}


def verify_plan(root: Path, input_path: Path) -> dict:
    """Verify that a saved plan still describes the current v2 source HEAD."""
    root = safe_path(root)
    input_path = safe_path(Path(input_path))
    require(not input_path.is_relative_to(root), "Migration report must be outside bank-root")
    try:
        report = json_loads(read_bytes(input_path, MAX_REPORT_BYTES).decode("utf-8"))
    except (UnicodeError, ValueError) as exc:
        raise ValueError(f"Invalid migration report: {exc}") from exc
    require(isinstance(report, dict), "Migration report must be an object")
    require(
        report.get("mode") == "dry_run"
        and report.get("report_version") == "1.0"
        and report.get("source_format") == "2.0"
        and report.get("target_format") == "3.0"
        and report.get("writable") is False,
        "Unsupported migration report",
    )
    current = plan(root)
    for field in ("source_workspace_id", "source_head", "source_records_sha256"):
        require(report.get(field) == current[field], f"Migration report is stale: {field}")
    return {
        "valid_plan": True,
        "mode": "dry_run",
        "source_workspace_id": current["source_workspace_id"],
        "source_head": current["source_head"],
        "source_records_sha256": current["source_records_sha256"],
        "approvals_created": 0,
    }
