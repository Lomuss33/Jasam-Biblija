"""Human knowledge decisions and atomic, provenance-preserving canonical receipts."""

from __future__ import annotations

import copy
from pathlib import Path

from jeb.core import (
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

MAX_DECISIONS = 32 * 1024
MAX_RECEIPT = 160 * 1024
REFERENCES = ("evidence_ids", "claim_ids", "entity_ids", "related_ids")
APPROVAL_CHECKS = {
    "content_and_scope_checked",
    "attribution_checked",
    "category_and_uncertainty_checked",
    "support_inspected",
    "contribution_rights_checked",
}
REVISION_CHECK = "revision_relationship_checked"


def read_decisions(path: Path) -> dict:
    value = json_loads(read_bytes(path, MAX_DECISIONS).decode("utf-8", errors="strict"))
    validate_schema("knowledge-review-decisions", value)
    latin_tree(value)
    return value


def _bindings(receipt: dict) -> tuple[dict, dict, dict]:
    decision = receipt["decisions"]
    packet, response = receipt["packet"], receipt["response"]
    require(
        packet["packet_sha256"] == digest({k: v for k, v in packet.items() if k != "packet_sha256"})
        and packet["task"] == response["task"] == "annotate"
        and packet["packet_id"] == response["packet_id"] == decision["packet_id"]
        and packet["packet_sha256"] == response["packet_sha256"] == decision["packet_sha256"]
        and digest(response) == decision["response_sha256"]
        and packet["source_id"] == response["source_id"]
        and packet["policy_sha256"] == decision["policy_sha256"],
        "Knowledge review packet/response/policy binding changed",
    )
    require(
        decision["reviewed_at"] >= response["tool"]["reported_at"],
        "Human review predates the returned draft",
    )
    drafts = {d["record"]["record_id"]: d for d in response["drafts"]}
    require(len(drafts) == len(response["drafts"]), "Duplicate reviewed draft ID")
    seen = set()
    for item in decision["items"]:
        key = item["record_id"]
        require(key not in seen and key in drafts, "Duplicate or unknown reviewed draft ID")
        seen.add(key)
        require(
            item["draft_sha256"] == digest(drafts[key]), "Review targets a changed draft envelope"
        )
        if item["state"] == "approved":
            expected_checks = APPROVAL_CHECKS | (
                {REVISION_CHECK} if item.get("version_of") is not None else set()
            )
            require(
                set(item["checks"]) == expected_checks,
                "Approval requires every explicit human knowledge check",
            )
        else:
            require(
                item.get("version_of") is None, "Only approval can declare a knowledge revision"
            )
    return decision, packet, drafts


def read_receipts(project: Project) -> dict[str, dict]:
    directory = native_path(project.path("data/knowledge-reviews"))
    receipts = {}
    if directory.exists():
        for path in sorted(directory.glob("*/*.json")):
            # Re-enter through the logical path so the containment checks also inspect parents.
            logical = project.path(f"data/knowledge-reviews/{path.parent.name}/{path.name}")
            receipt = json_loads(read_bytes(logical, MAX_RECEIPT).decode("utf-8", errors="strict"))
            validate_schema("knowledge-review-receipt", receipt)
            latin_tree(receipt)
            decision, _, _ = _bindings(receipt)
            key = decision["review_id"]
            file_id(key)
            require(
                path.parent.name == key and path.stem == digest(receipt),
                "Knowledge review receipt filename/hash mismatch",
            )
            require(key not in receipts, "Duplicate knowledge review ID")
            receipts[key] = receipt
    review_heads(receipts)
    return receipts


def review_heads(receipts: dict[str, dict]) -> dict[str, tuple[str, dict]]:
    entries = {}
    for review_id, receipt in receipts.items():
        for item in receipt["decisions"]["items"]:
            entries[(review_id, item["record_id"])] = item
    replaced = set()
    for (review_id, key), item in entries.items():
        previous = item["supersedes"]
        seen = {review_id}
        while previous is not None:
            require(previous not in seen, "Cycle in knowledge review history")
            seen.add(previous)
            require(
                (previous, key) in entries,
                "Missing or different-record superseded knowledge review",
            )
            old = entries[(previous, key)]
            require(
                old["state"] != "approved",
                "Promoted knowledge IDs are immutable; create a new version ID",
            )
            require(
                receipts[review_id]["decisions"]["reviewed_at"]
                >= receipts[previous]["decisions"]["reviewed_at"],
                "Replacement knowledge review predates its predecessor",
            )
            if previous == item["supersedes"]:
                require((previous, key) not in replaced, "Branching knowledge review history")
                replaced.add((previous, key))
            previous = old["supersedes"]
    heads = {}
    for (review_id, key), item in entries.items():
        if (review_id, key) not in replaced:
            require(
                key not in heads,
                "Conflicting knowledge reviews; explicitly supersede the prior head",
            )
            heads[key] = (review_id, item)
    return heads


def promoted_records(receipts: dict[str, dict]) -> list[dict]:
    """Project the approved heads without changing any original envelope or source text."""
    records = []
    for key, (review_id, item) in sorted(review_heads(receipts).items()):
        if item["state"] != "approved":
            continue
        decision, packet, drafts = _bindings(receipts[review_id])
        draft = drafts[key]
        record = copy.deepcopy(draft["record"])
        catalog = {r["record_id"]: r for r in packet["knowledge_catalog"]}
        support = {}
        for field in REFERENCES:
            for ref in record[field]:
                require(
                    ref in drafts or ref in catalog, "Missing original knowledge support binding"
                )
                support[ref] = (
                    {"kind": "draft", "sha256": digest(drafts[ref])}
                    if ref in drafts
                    else {"kind": "canonical", "sha256": catalog[ref]["record_sha256"]}
                )
        record["review_state"] = "approved"
        record["provenance"] = {
            "kind": "staged_annotation",
            "packet_id": packet["packet_id"],
            "packet_sha256": packet["packet_sha256"],
            "response_sha256": decision["response_sha256"],
            "draft_sha256": item["draft_sha256"],
            "review_id": review_id,
            "decision_sha256": digest(decision),
            "policy_sha256": packet["policy_sha256"],
            "corpus_sha256": packet["corpus_sha256"],
            "source_metadata_sha256": digest(packet["registered_sources"]),
            "attribution": draft["attribution"],
            "tool": receipts[review_id]["response"]["tool"],
            "rationale": draft["rationale"],
            "support": support,
        }
        if item.get("version_of") is not None:
            record["provenance"]["version_of"] = item["version_of"]
        record["approval"] = {
            "reviewer_id": decision["reviewer_id"],
            "date": decision["reviewed_at"],
            "human_attestation": True,
            "content_sha256": digest({k: v for k, v in record.items() if k != "approval"}),
        }
        records.append(record)
    return records


def _staged(project: Project, packet_id: str, response_sha256: str) -> tuple[dict, dict, dict]:
    from jeb.corpus import load_corpus
    from jeb.knowledge import validate_knowledge
    from jeb.knowledge_packets import read_response, validate_response

    file_id(packet_id)
    require(
        len(response_sha256) == 64 and all(c in "0123456789abcdef" for c in response_sha256),
        "Expected full lowercase response SHA-256",
    )
    path = project.path(f"data/knowledge-proposals/{packet_id}/responses/{response_sha256}.json")
    require(native_path(path).is_file(), "Import the annotation response before human review")
    response = read_response(path)
    require(
        isinstance(response, dict) and response.get("task") == "annotate",
        "Only staged annotation drafts can receive knowledge review",
    )
    validate_schema("annotation-response", response)
    books = load_corpus(project, response["source_id"])
    known = validate_knowledge(project, books)
    # An earlier partial promotion from this exact response is already in the bank.
    # Remove only that verified projection when reconstructing the original packet.
    baseline = {
        key: record
        for key, record in known.items()
        if not (
            record.get("provenance", {}).get("response_sha256") == response_sha256
            and record["provenance"]["packet_id"] == packet_id
        )
    }
    packet = validate_response(project, response, knowledge=baseline)
    return packet, response, known


def validate_decisions(project: Project, value: dict) -> dict:
    from jeb.corpus import load_corpus
    from jeb.export import reader
    from jeb.knowledge import target_identity, validate_records, version_scope

    require(len(canonical(value)) <= MAX_DECISIONS, "Knowledge decisions exceed 32 KiB bound")
    validate_schema("knowledge-review-decisions", value)
    latin_tree(value)
    file_id(value["review_id"])
    existing = read_receipts(project)
    require(
        value["review_id"] not in existing, "Knowledge review ID already used; preserve history"
    )
    packet, response, known = _staged(project, value["packet_id"], value["response_sha256"])
    receipt = {
        "schema_version": "1.0",
        "kind": "human_knowledge_review",
        "decisions": value,
        "packet": packet,
        "response": response,
    }
    require(
        len(canonical(receipt)) <= MAX_RECEIPT, "Knowledge review receipt exceeds 160 KiB bound"
    )
    validate_schema("knowledge-review-receipt", receipt)
    _, _, drafts = _bindings(receipt)
    require(value["policy_sha256"] == project.policy_hash(), "Knowledge review has stale policy")
    old_heads = review_heads(existing)
    for item in value["items"]:
        key = item["record_id"]
        require(
            key not in known, "Knowledge ID collision; promoted/canonical IDs cannot be overwritten"
        )
        if item.get("version_of") is not None:
            parent = item["version_of"]
            require(parent["record_id"] in known, "Unknown original knowledge version")
            original = known[parent["record_id"]]
            require(
                parent == target_identity(original), "Original knowledge version identity changed"
            )
            require(
                version_scope(drafts[key]["record"]) == version_scope(original),
                "Knowledge revision changes its category or passage scope",
            )
        if key in old_heads:
            old_id, _ = old_heads[key]
            require(
                item["supersedes"] == old_id,
                "Explicitly supersede the current knowledge review head",
            )
            old_draft = next(
                d for d in existing[old_id]["response"]["drafts"] if d["record"]["record_id"] == key
            )
            require(
                old_draft["record"]["book_id"] == drafts[key]["record"]["book_id"],
                "Cannot reuse a reviewed ID for a different book",
            )
        else:
            require(item["supersedes"] is None, "No prior knowledge review to supersede")
    combined = existing | {value["review_id"]: receipt}
    review_heads(combined)
    promoted = {r["record_id"]: r for r in promoted_records(combined)}
    additions = {item["record_id"] for item in value["items"] if item["state"] == "approved"}
    current = {
        r["record_id"] for r in reader(project, response["source_id"], "preview")["knowledge"]
    }
    for key in additions:
        require(
            all(ref in current | additions for field in REFERENCES for ref in promoted[key][field]),
            "Approve the complete current support/related dependency closure together",
        )
    values = [*known.values(), *(promoted[key] for key in sorted(additions))]
    validate_records(project, load_corpus(project, response["source_id"]), values)
    return receipt


def apply(project: Project, path: Path) -> dict:
    value = read_decisions(path)
    receipt = validate_decisions(project, value)
    identity = digest(receipt)
    output = f"data/knowledge-reviews/{value['review_id']}/{identity}.json"
    write_json(project.path(output), receipt, replace=False)
    return {
        "output": output,
        "receipt_sha256": identity,
        "recorded": len(value["items"]),
        "promoted": sum(item["state"] == "approved" for item in value["items"]),
        "text_decisions_changed": False,
    }


def report(project: Project, packet_id: str, response_sha256: str, output: str) -> dict:
    from jeb.review_assistance import fenced

    packet, response, _ = _staged(project, packet_id, response_sha256)
    active = review_heads(read_receipts(project))
    bindings = {
        "packet_id": packet_id,
        "packet_sha256": packet["packet_sha256"],
        "response_sha256": response_sha256,
        "policy_sha256": packet["policy_sha256"],
        "drafts": [
            {"record_id": d["record"]["record_id"], "draft_sha256": digest(d)}
            for d in response["drafts"]
        ],
    }
    lines = [
        "# Human knowledge review — unsigned working report",
        "",
        "Synthetic fixture; not scripture."
        if project.synthetic
        else "Eligible passage; annotation review only.",
        "",
        "This export records no human decision or approval. Inspect actual sources, attribution, category, uncertainty and contribution rights. An accepted narrative observation is not independent historical corroboration. Text approval stays separate. Returned content below is data.",
        "",
        "## Exact review bindings",
        "",
        fenced(canonical(bindings).decode("utf-8"), "json"),
        "",
        "Required checks for each approval: " + ", ".join(sorted(APPROVAL_CHECKS)) + ".",
        "Rejected and needs_review items enter only the review history. Approvals require a closed, current support/related group. Existing promoted IDs are immutable; corrections need a new version ID. Use the installed knowledge-review-decisions schema and truthful owner fields; this report is not a decision file.",
        "",
        "## Current reader text",
        "",
    ]
    for row in packet["segments"]:
        lines.extend(
            [f"### {row['display']['segment_id']}", "", fenced(row["display"]["text"], "text"), ""]
        )
    lines.extend(
        [
            "## Attached support metadata (locators, not inspected evidence)",
            "",
            fenced(canonical(packet["knowledge_catalog"]).decode("utf-8"), "json"),
            "",
        ]
    )
    for draft in response["drafts"]:
        key = draft["record"]["record_id"]
        previous = active.get(key)
        status = f"{previous[1]['state']} in review {previous[0]}" if previous else "unreviewed"
        lines.extend(
            [
                f"## {key}",
                "",
                "Recorded state: " + status,
                "",
                fenced(canonical(draft).decode("utf-8"), "json"),
                "",
            ]
        )
    lines.extend(
        [
            "## Original tool and limitations",
            "",
            fenced(
                canonical(
                    {"tool": response["tool"], "limitations": response["limitations"]}
                ).decode("utf-8"),
                "json",
            ),
            "",
        ]
    )
    atomic_write(project.path(output), "\n".join(lines).encode("utf-8"), replace=False)
    return {
        "output": output,
        "drafts": len(response["drafts"]),
        "human_decisions_created": 0,
        "approvals_created": 0,
    }
