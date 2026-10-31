"""Immutable owner withdrawals, reactivations and explicit knowledge version choices."""

from __future__ import annotations

from pathlib import Path

from jeb.core import (
    JebError,
    Project,
    atomic_write,
    canonical,
    digest,
    file_id,
    json_loads,
    latin_tree,
    native_path,
    read_bytes,
    require,
    validate_schema,
    write_json,
)
from jeb.knowledge import stored_records, target_identity, version_scope
from jeb.sources import registry

MAX_DECISIONS = 32 * 1024
MAX_RECEIPT = 256 * 1024
REFERENCES = ("evidence_ids", "claim_ids", "entity_ids", "related_ids")
CHECKS = {
    "withdraw": {"record_identity_checked", "impact_checked"},
    "reactivate": {
        "record_identity_checked",
        "impact_checked",
        "withdrawal_reason_resolved",
        "current_dependencies_checked",
    },
    "select": {
        "record_identity_checked",
        "impact_checked",
        "current_dependencies_checked",
        "alternatives_compared",
    },
}


def read_decisions(path: Path) -> dict:
    value = json_loads(read_bytes(path, MAX_DECISIONS).decode("utf-8", errors="strict"))
    validate_schema("knowledge-curation-decisions", value)
    latin_tree(value)
    return value


def item_key(item: dict) -> str:
    return (
        "group:" + item["group_id"]
        if item["kind"] == "select"
        else "record:" + item["target"]["record_id"]
    )


def item_targets(item: dict) -> list[dict]:
    return item["candidates"] if item["kind"] == "select" else [item["target"]]


def _bindings(receipt: dict) -> None:
    decisions = receipt["decisions"]
    records = {r["record_id"]: r for r in receipt["records"]}
    require(len(records) == len(receipt["records"]), "Duplicate curation snapshot ID")
    used, keys = set(), set()
    for item in decisions["items"]:
        key = item_key(item)
        require(key not in keys, "Duplicate curation subject in one decision")
        keys.add(key)
        require(
            set(item["checks"]) == CHECKS[item["kind"]],
            "Curation requires every explicit owner check for its action",
        )
        targets = item_targets(item)
        ids = [t["record_id"] for t in targets]
        require(len(ids) == len(set(ids)), "Duplicate version candidate ID")
        for target in targets:
            record = records.get(target["record_id"])
            require(
                record is not None and target == target_identity(record),
                "Curation record/approval/provenance identity changed",
            )
            require(
                record["approval"]["content_sha256"]
                == digest({k: v for k, v in record.items() if k != "approval"}),
                "Curation snapshot edited after approval",
            )
            require(
                decisions["reviewed_at"] >= record["approval"]["date"],
                "Curation predates the original approval",
            )
            used.add(target["record_id"])
        if item["kind"] == "select":
            file_id(item["group_id"])
            require(item["selected_record_id"] in ids, "Selected version is not a bound candidate")
            scopes = {version_scope(records[key]) for key in ids}
            require(len(scopes) == 1, "Version candidates differ in category or passage scope")
            for candidate in ids:
                parent = records[candidate].get("provenance", {}).get("version_of")
                if parent is not None:
                    require(
                        parent["record_id"] in ids
                        and parent == target_identity(records[parent["record_id"]]),
                        "Version group must include the exact original revision ancestry",
                    )
    require(used == set(records), "Missing or extraneous curation snapshots")


def read_receipts(project: Project) -> dict[str, dict]:
    receipts = {}
    directory = native_path(project.path("data/knowledge-curation"))
    if directory.exists():
        for path in sorted(directory.glob("*/*.json")):
            logical = project.path(f"data/knowledge-curation/{path.parent.name}/{path.name}")
            receipt = json_loads(read_bytes(logical, MAX_RECEIPT).decode("utf-8", errors="strict"))
            validate_schema("knowledge-curation-receipt", receipt)
            latin_tree(receipt)
            _bindings(receipt)
            key = file_id(receipt["decisions"]["action_id"])
            require(
                path.parent.name == key and path.stem == digest(receipt),
                "Curation receipt filename/hash mismatch",
            )
            require(
                key.casefold() not in {used.casefold() for used in receipts},
                "Curation action ID already used, including a filename case variant",
            )
            receipts[key] = receipt
    heads(receipts)
    return receipts


def heads(receipts: dict[str, dict]) -> dict[str, tuple[str, dict]]:
    entries = {}
    memberships = {}
    for action_id, receipt in receipts.items():
        for item in receipt["decisions"]["items"]:
            key = item_key(item)
            require((action_id, key) not in entries, "Duplicate curation subject")
            entries[(action_id, key)] = item
            if item["kind"] == "select":
                for target in item["candidates"]:
                    old_group = memberships.setdefault(target["record_id"], item["group_id"])
                    require(
                        old_group == item["group_id"],
                        "A knowledge record cannot belong to competing version groups",
                    )
    replaced = set()
    for (action_id, key), item in entries.items():
        previous, seen = item["supersedes"], {action_id}
        if item["kind"] == "reactivate":
            require(previous is not None, "Reactivation requires an explicit prior withdrawal")
        while previous is not None:
            require(previous not in seen, "Cycle in curation history")
            seen.add(previous)
            require(
                (previous, key) in entries,
                "Missing or different-subject superseded curation action",
            )
            old = entries[(previous, key)]
            require(
                receipts[action_id]["decisions"]["reviewed_at"]
                >= receipts[previous]["decisions"]["reviewed_at"],
                "Curation replacement predates its predecessor",
            )
            if previous == item["supersedes"]:
                require((previous, key) not in replaced, "Branching curation history")
                replaced.add((previous, key))
                if item["kind"] == "reactivate":
                    require(
                        old["kind"] == "withdraw",
                        "Reactivation must supersede the current withdrawal",
                    )
                elif item["kind"] == "withdraw":
                    require(old["kind"] != "withdraw", "Record is already explicitly withdrawn")
                else:
                    require(
                        {t["record_id"] for t in old["candidates"]}
                        <= {t["record_id"] for t in item["candidates"]},
                        "Version groups cannot drop prior candidates",
                    )
            previous = old["supersedes"]
    active = {}
    for (action_id, key), item in entries.items():
        if (action_id, key) not in replaced:
            require(
                key not in active,
                "Conflicting curation heads; explicitly supersede the current action",
            )
            active[key] = (action_id, item)
    return active


def validate_targets(receipts: dict[str, dict], records: dict[str, dict]) -> None:
    for receipt in receipts.values():
        for snapshot in receipt["records"]:
            key = snapshot["record_id"]
            require(
                key in records and target_identity(records[key]) == target_identity(snapshot),
                "Missing or changed canonical curation target; restore the immutable approval archive",
            )


def state(records: dict[str, dict], receipts: dict[str, dict]) -> dict:
    active = heads(receipts)
    withdrawn = {
        item["target"]["record_id"] for _, item in active.values() if item["kind"] == "withdraw"
    }
    groups = {item["group_id"]: item for _, item in active.values() if item["kind"] == "select"}
    selected = {key: item["selected_record_id"] for key, item in groups.items()}
    inactive = {
        t["record_id"]
        for item in groups.values()
        for t in item["candidates"]
        if t["record_id"] != item["selected_record_id"]
    }
    inactive |= {
        key
        for key, r in records.items()
        if r.get("provenance", {}).get("version_of") is not None
        and key not in set(selected.values())
    }
    return {
        "receipt_sha256": sorted(digest(r) for r in receipts.values()),
        "head_action_ids": sorted({action_id for action_id, _ in active.values()}),
        "withdrawn_record_ids": sorted(withdrawn),
        "inactive_version_ids": sorted(inactive),
        "selected_versions": dict(sorted(selected.items())),
    }


def filter_records(records: dict, eligible: dict, receipts: dict) -> dict:
    selection = state(records, receipts)
    excluded = set(selection["withdrawn_record_ids"]) | set(selection["inactive_version_ids"])
    retained = {key: record for key, record in eligible.items() if key not in excluded}
    while True:
        current = {
            key: record
            for key, record in retained.items()
            if all(ref in retained for field in REFERENCES for ref in record[field])
        }
        if len(current) == len(retained):
            return current
        retained = current


def validate_decisions(project: Project, value: dict) -> dict:
    require(len(canonical(value)) <= MAX_DECISIONS, "Curation decisions exceed 32 KiB bound")
    validate_schema("knowledge-curation-decisions", value)
    latin_tree(value)
    file_id(value["action_id"])
    require(value["policy_sha256"] == project.policy_hash(), "Curation decision has stale policy")
    if value["source_id"] is not None:
        require(
            value["source_id"] in {r["source_id"] for r in registry(project)["sources"]},
            "Unknown curation source ID",
        )
    records, existing = stored_records(project), read_receipts(project)
    validate_targets(existing, records)
    require(
        value["action_id"].casefold() not in {used.casefold() for used in existing},
        "Curation action ID already used; preserve history",
    )
    directory = native_path(project.path(f"data/knowledge-curation/{value['action_id']}"))
    require(
        not directory.exists() or directory.resolve().name == value["action_id"],
        "Existing curation directory has different filename casing; use its exact spelling",
    )
    targets = {t["record_id"] for item in value["items"] for t in item_targets(item)}
    require(targets <= set(records), "Unknown canonical curation target")
    receipt = {
        "schema_version": "1.0",
        "kind": "human_knowledge_curation",
        "decisions": value,
        "records": [records[key] for key in sorted(targets)],
    }
    require(len(canonical(receipt)) <= MAX_RECEIPT, "Curation receipt exceeds 256 KiB bound")
    validate_schema("knowledge-curation-receipt", receipt)
    _bindings(receipt)
    previous = heads(existing)
    for item in value["items"]:
        key = item_key(item)
        require(
            item["supersedes"] == (previous[key][0] if key in previous else None),
            "Explicitly supersede the current curation head for this subject",
        )
    combined = existing | {value["action_id"]: receipt}
    heads(combined)
    activating = {
        item["selected_record_id"] if item["kind"] == "select" else item["target"]["record_id"]
        for item in value["items"]
        if item["kind"] != "withdraw"
    }
    if activating:
        from jeb.export import reader

        require(
            value["source_id"] is not None,
            "Selection/reactivation requires a current eligible source",
        )
        preview = reader(project, value["source_id"], "preview", _apply_curation=False)
        base = {r["record_id"]: r for r in preview["knowledge"]}
        available = filter_records(records, base, combined)
        require(
            activating <= set(available),
            "Selected/reactivated records need current source, support and an explicit compatible version choice",
        )
    return receipt


def apply(project: Project, path: Path) -> dict:
    value = read_decisions(path)
    receipt = validate_decisions(project, value)
    identity = digest(receipt)
    output = f"data/knowledge-curation/{value['action_id']}/{identity}.json"
    write_json(project.path(output), receipt, replace=False)
    return {
        "output": output,
        "receipt_sha256": identity,
        "recorded": len(value["items"]),
        "knowledge_records_changed": False,
        "text_decisions_changed": False,
        "approvals_created": 0,
    }


def report(project: Project, output: str, source_id: str | None = None) -> dict:
    from jeb.review_assistance import fenced

    records, receipts = stored_records(project), read_receipts(project)
    validate_targets(receipts, records)
    current, assessment = None, "Current reader eligibility was not assessed; no source requested."
    if source_id is not None:
        from jeb.export import reader

        try:
            preview = reader(project, source_id, "preview")
            current = {r["record_id"] for r in preview["knowledge"]}
            assessment = "Current reader eligibility assessed using source " + source_id + "."
        except JebError as exc:
            assessment = "Current reader eligibility unavailable: " + str(exc)
    selection = state(records, receipts)
    subjects = [
        {
            "target": target_identity(record),
            "record_type": record["record_type"],
            "book_id": record["book_id"],
            "layer": record["layer"],
            "evidence_category": record["evidence_category"],
            "segment_ids": record["segment_ids"],
            "version_of": record.get("provenance", {}).get("version_of"),
            "current_reader_eligible": None if current is None else key in current,
        }
        for key, record in sorted(records.items())
        if record["review_state"] == "approved"
    ]
    bindings = {
        "policy_sha256": project.policy_hash(),
        "source_id": source_id,
        "subjects": subjects,
        "curation": selection,
    }
    lines = [
        "# Knowledge withdrawal and version selection — unsigned report",
        "",
        "Synthetic fixture; not scripture."
        if project.synthetic
        else "Canonical knowledge metadata; no source wording reproduced.",
        "",
        "This report creates no owner action, approval, withdrawal or selection. Target hashes identify existing approved records; original approvals and attribution remain immutable. Stored text bodies are omitted. Use the separate knowledge-curation-decisions schema for a truthful owner action.",
        "",
        fenced(assessment, "text"),
        "",
        fenced(canonical(bindings).decode("utf-8"), "json"),
        "",
        "Withdrawals can be recorded even when source display is blocked. Selection and reactivation require current eligible source/support. A declared revision is withheld until explicitly selected with its original ancestry. No candidate is automatically substituted when a selected version becomes stale or withdrawn.",
        "",
    ]
    atomic_write(project.path(output), "\n".join(lines).encode("utf-8"), replace=False)
    return {
        "output": output,
        "approved_subjects": len(subjects),
        "curation_receipts": len(receipts),
        "owner_actions_created": 0,
        "approvals_created": 0,
    }
