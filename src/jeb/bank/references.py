"""Exact prior-revision reference resolution for persistent unreviewed records."""

from __future__ import annotations

from jeb.core import latin_tree, require


def locator_check(locator: dict, body: str | None) -> str:
    if locator["type"] == "text_span":
        require(body is not None, "Text span requires locally bound source body")
        start, end = locator["start"], locator["end"]
        require(0 <= start < end <= len(body), "Text span is outside bound body")
        require(body[start:end] == locator["exact"], "Text span does not match exact source text")
        return "local_text_match"
    if locator["type"] == "page":
        require(
            locator["pdf_page"] is not None or locator["printed_page"] is not None,
            "Page locator requires PDF page or printed page label",
        )
    if locator["type"] == "time_range":
        require(locator["start_ms"] < locator["end_ms"], "Invalid time range")
    return "declared_only"


def binding(revision: dict) -> dict:
    record = revision["record"]
    return {
        "record_id": record["id"],
        "revision_id": record["revision_id"],
        "record_sha256": revision["record_sha256"],
        "body_sha256": record["body_sha256"],
    }


def resolve(reference: dict, kind: str, revisions: dict) -> dict:
    key = (reference["record_id"], reference["revision_id"])
    require(key in revisions, f"Missing prior {kind} revision: {key}")
    revision = revisions[key]
    require(revision["record"]["kind"] == kind, f"Reference requires {kind}")
    require(binding(revision) == reference, f"Historical {kind} binding differs")
    return revision


def _nonblank(value) -> None:
    if isinstance(value, str):
        require(bool(value.strip()), "Blank persistent claim/evidence text")
    elif isinstance(value, dict):
        for item in value.values():
            _nonblank(item)


def check_record(record: dict, revisions: dict) -> None:
    if record["kind"] not in ("claim", "evidence"):
        return
    data = record["data"]
    latin_tree(data, "persistent unreviewed claim/evidence")
    _nonblank(data)
    if record["kind"] == "claim":
        resolve(data["subject"], "entity", revisions)
    else:
        resolve(data["claim"], "claim", revisions)
        source = resolve(data["source"], "source", revisions)
        locator_check(data["locator"], source["body"])


def add_revision(snapshot: dict, revisions: dict) -> None:
    identity = snapshot["manifest"]["changed_record"]
    if identity is not None:
        record = snapshot["records"][identity]
        # Resolve only against earlier commits; self/forward/cyclic references fail.
        check_record(record, revisions)
        revisions[(identity, record["revision_id"])] = {
            "record": record,
            "body": snapshot["bodies"].get(identity),
            "record_sha256": snapshot["file_hashes"][identity]["record"],
        }


def record_reference(root, identity: str, revision_id: str | None = None) -> dict:
    from jeb.bank import storage
    from jeb.bank.validation import ID_PATTERN

    require(bool(ID_PATTERN.fullmatch(identity)), "Unsafe record ID")
    state = storage.read_managed(root)
    require(identity in state["records"], "Record not found")
    revision_id = state["records"][identity]["revision_id"] if revision_id is None else revision_id
    require(bool(ID_PATTERN.fullmatch(revision_id)), "Unsafe revision ID")
    key = (identity, revision_id)
    require(key in state["revisions"], "Record revision not found in committed history")
    return binding(state["revisions"][key])


def evidence_links(root, identity: str) -> dict:
    from jeb.bank import storage
    from jeb.bank.validation import ID_PATTERN

    require(bool(ID_PATTERN.fullmatch(identity)), "Unsafe claim ID")
    state = storage.read_managed(root)
    require(
        identity in state["records"] and state["records"][identity]["kind"] == "claim",
        "Claim record not found",
    )
    claim = state["records"][identity]
    links = []
    for record in sorted(state["records"].values(), key=lambda item: item["id"]):
        if record["kind"] != "evidence" or record["data"]["claim"]["record_id"] != identity:
            continue
        data = record["data"]
        source = resolve(data["source"], "source", state["revisions"])
        links.append(
            {
                "evidence_id": record["id"],
                "evidence_revision": record["revision_id"],
                "relation": data["relation"],
                "claim": data["claim"],
                "source": data["source"],
                "applies_to_current_claim": data["claim"]["revision_id"] == claim["revision_id"],
                "source_revision_matches_current": data["source"]["revision_id"]
                == state["records"][data["source"]["record_id"]]["revision_id"],
                "locator_verification": locator_check(data["locator"], source["body"]),
                "review_state": "unreviewed",
            }
        )
    return {
        "claim_id": identity,
        "claim_revision": claim["revision_id"],
        "links": links,
        "review_state": "unreviewed",
        "approval_authority": "none",
        "approvals_created": 0,
    }
