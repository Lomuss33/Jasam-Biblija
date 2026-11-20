"""Bounded read-only search over the current committed bank records."""

from __future__ import annotations

from pathlib import Path

from jeb.core import require

from .storage import read_managed
from .validation import safe_path


def search(root: Path, query: str) -> dict:
    root = safe_path(root)
    query = query.strip()
    require(query, "Search query must not be blank")
    lowered = query.casefold()
    state = read_managed(root)
    results = []
    for identity in sorted(state["records"]):
        record = state["records"][identity]
        data = record["data"]
        fields = {
            "title": record["title"],
            "kind": record["kind"],
            "processing_state": record["processing_state"],
            "data": str(data),
            "body": state["bodies"].get(identity, ""),
        }
        matches = [name for name, value in fields.items() if lowered in value.casefold()]
        if matches:
            results.append(
                {
                    "id": identity,
                    "revision_id": record["revision_id"],
                    "kind": record["kind"],
                    "title": record["title"],
                    "matches": matches,
                }
            )
    return {"query": query, "results": results, "approvals_created": 0}
