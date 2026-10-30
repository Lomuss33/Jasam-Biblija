"""Explicit human-owner decisions bound to exact proposal, policy and text hashes."""

from __future__ import annotations

from pathlib import Path

from jeb.batch import load_proposal
from jeb.core import (
    Project,
    atomic_write,
    digest,
    file_id,
    latin_tree,
    read_json,
    require,
    validate_schema,
    write_json,
)


def decision_item(project: Project, decision: dict) -> tuple[dict, dict]:
    validate_schema("decision", decision)
    latin_tree(decision)
    file_id(decision["decision_id"])
    proposal = load_proposal(project, decision["proposal_id"])
    require(decision["proposal_sha256"] == digest(proposal), "Decision targets a changed proposal")
    matches = [i for i in proposal["items"] if i["segment_id"] == decision["segment_id"]]
    require(len(matches) == 1, "Decision segment not in proposal")
    item = matches[0]
    require(
        decision["text_sha256"] == item["text_sha256"], "Decision does not match exact text hash"
    )
    require(decision["policy_sha256"] == project.policy_hash(), "Decision has stale policy hash")
    if decision["state"] == "approved":
        require(
            decision["reviewer_role"] == "owner" and decision["human_attestation"],
            "Exact owner approval required",
        )
        require(item["action"] != "needs_review", "Unresolved proposal cannot be approved")
        require(
            item["change_class"] != "D" and "meaning_sensitive" not in item["flags"],
            "Meaning-sensitive approval requires a future expert-review workflow; currently blocked",
        )
        resolved = {r["flag"] for r in decision["resolutions"]}
        require(
            len(resolved) == len(decision["resolutions"]) and resolved == set(item["flags"]),
            "Each flagged issue needs an explicit human resolution; no invented flags",
        )
    return proposal, item


def all_decisions(project: Project) -> dict[str, dict]:
    result = {}
    directory = project.path("data/approved")
    if directory.exists():
        for path in sorted(directory.glob("*.json")):
            decision = read_json(path)
            # Historical decisions can be stale. Validate current heads at use time;
            # otherwise an old policy would prevent a new decision superseding them.
            validate_schema("decision", decision)
            latin_tree(decision)
            require(path.stem == decision["decision_id"], "Decision filename/ID mismatch")
            require(decision["decision_id"] not in result, "Duplicate decision")
            result[decision["decision_id"]] = decision
    return result


def heads(decisions: dict[str, dict]) -> dict[str, dict]:
    superseded = set()
    for decision in decisions.values():
        previous = decision["supersedes"]
        if previous is not None:
            require(
                previous in decisions and previous != decision["decision_id"],
                "Missing/self superseded decision",
            )
            require(
                decisions[previous]["segment_id"] == decision["segment_id"],
                "Cannot supersede a different segment",
            )
            require(
                previous not in superseded,
                "Branching decision history; resolve conflict explicitly",
            )
            superseded.add(previous)
        seen = {decision["decision_id"]}
        while previous is not None:
            require(previous not in seen, "Cycle in decision history")
            seen.add(previous)
            require(previous in decisions, "Broken decision history")
            previous = decisions[previous]["supersedes"]
    active = {}
    for decision_id, decision in decisions.items():
        if decision_id not in superseded:
            require(
                decision["segment_id"] not in active, "Conflicting active decisions; use supersedes"
            )
            active[decision["segment_id"]] = decision
    return active


def apply(project: Project, path: Path) -> dict:
    value = read_json(path)
    validate_schema("decisions", value)
    existing = all_decisions(project)
    additions = {}
    for decision in value["decisions"]:
        decision_item(project, decision)
        require(
            decision["decision_id"] not in existing and decision["decision_id"] not in additions,
            "Decision ID already used; preserve history and create a new decision",
        )
        additions[decision["decision_id"]] = decision
    heads(existing | additions)
    # Validate the whole submitted set before persisting any decision.
    for decision in additions.values():
        write_json(
            project.path(f"data/approved/{decision['decision_id']}.json"), decision, replace=False
        )
    return {"recorded": len(additions), "states": [d["state"] for d in additions.values()]}


def report(project: Project, proposal_id: str, output: str) -> dict:
    proposal = load_proposal(project, proposal_id)
    lines = [
        "# Editorial review",
        "",
        f"Proposal: {proposal_id}",
        f"Proposal SHA-256: {digest(proposal)}",
        f"Policy SHA-256: {project.policy_hash()}",
        "",
        "Synthetic fixture; not scripture."
        if project.synthetic
        else "Unapproved working proposal.",
        "",
    ]
    active = heads(all_decisions(project))
    for decision in active.values():
        decision_item(project, decision)
    packet = read_json(project.path(f"data/batches/{proposal['response']['batch_id']}/input.json"))
    source_text = {s["segment_id"]: s["normalized_text"] for s in packet["segments"]}
    for item in proposal["items"]:
        lines.extend(
            [
                f"## {item['segment_id']}",
                "",
                "Source:",
                "",
                source_text[item["segment_id"]],
                "",
                "Proposal:",
                "",
                item["proposed_text"] or "No proposed text; needs review.",
                "",
                f"Action: {item['action']}; class: {item['change_class']}",
                f"Text SHA-256: {item['text_sha256']}",
                f"Rationale: {item['rationale']}",
                f"Flags: {', '.join(item['flags']) or 'none (not a fidelity guarantee)'}",
                f"Decision: {active.get(item['segment_id'], {}).get('state', 'unreviewed')}",
                "",
                "Diff (source to proposal):",
                "",
                "```diff",
                item["diff"],
                "```",
                "",
            ]
        )
    atomic_write(project.path(output), "\n".join(lines).encode("utf-8"))
    return {"output": output, "segments": len(proposal["items"]), "status": "review report only"}
