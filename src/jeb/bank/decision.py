"""Read-only validation of an external migration decision record."""

from __future__ import annotations

from pathlib import Path

from jeb.core import JebError, json_loads, latin_tree, read_bytes, require, sha256, validate_schema

from .migration import MAX_REPORT_BYTES, verify_plan
from .validation import safe_path


def validate(root: Path, plan_path: Path, decision_path: Path) -> dict:
    """Validate a synthetic/external decision without creating approval state."""
    root = safe_path(root)
    plan_path = safe_path(Path(plan_path))
    decision_path = safe_path(Path(decision_path))
    require(not plan_path.is_relative_to(root), "Migration plan must be outside bank-root")
    require(not decision_path.is_relative_to(root), "Decision record must be outside bank-root")
    try:
        plan = json_loads(read_bytes(plan_path, MAX_REPORT_BYTES).decode("utf-8"))
        decision = json_loads(read_bytes(decision_path, MAX_REPORT_BYTES).decode("utf-8"))
    except (UnicodeError, ValueError) as exc:
        raise JebError(f"Invalid migration input: {exc}") from exc
    validate_schema("bank-migration-decision-v1", decision)
    latin_tree(decision, "migration decision")
    require(decision["decision"] in ("proceed", "reject"), "Unsupported decision")
    verify_plan(root, plan_path)
    require(
        sha256(read_bytes(plan_path, MAX_REPORT_BYTES)) == decision["plan_sha256"],
        "Decision plan hash differs",
    )
    require(
        plan["source_workspace_id"] == decision["source_workspace_id"], "Decision workspace differs"
    )
    require(plan["source_head"] == decision["source_head"], "Decision HEAD differs")
    require(
        plan["source_records_sha256"] == decision["source_records_sha256"],
        "Decision record digest differs",
    )
    require(plan["counts"]["blocked"] == 0, "Decision cannot proceed with blocked records")
    target = Path(decision["target_path"]).absolute()
    require(not target.is_relative_to(root), "Decision target must be outside bank-root")
    require(not target.exists(), "Decision target already exists")
    return {
        "valid_decision": True,
        "decision": decision["decision"],
        "can_write": decision["decision"] == "proceed",
        "source_workspace_id": decision["source_workspace_id"],
        "source_head": decision["source_head"],
        "target_path": str(target),
        "approvals_created": 0,
    }
