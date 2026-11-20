"""Untrusted source-discovery candidates; never source admission or rights clearance."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import urlsplit

from jeb.core import (
    Project,
    digest,
    file_id,
    latin_tree,
    native_path,
    read_json,
    require,
    validate_schema,
    write_json,
)


def _validate(value: dict) -> dict:
    validate_schema("source-candidate-batch", value)
    latin_tree(value)
    file_id(value["batch_id"])
    urls = set()
    ids = set()
    for candidate in value["candidates"]:
        file_id(candidate["candidate_id"])
        require(candidate["candidate_id"] not in ids, "Duplicate candidate ID")
        ids.add(candidate["candidate_id"])
        parsed = urlsplit(candidate["url"])
        require(
            parsed.scheme == "https"
            and parsed.hostname
            and not parsed.username
            and not parsed.password
            and parsed.port in (None, 443)
            and not parsed.fragment,
            "Candidates require credential-free HTTPS URLs on port 443",
        )
        require(candidate["url"] not in urls, "Duplicate candidate URL")
        urls.add(candidate["url"])
        require(
            candidate["content_acquired"] is False,
            "Candidate intake never records acquired content; use the audited fetch gate",
        )
    return value


def validate(path: Path) -> dict:
    return _validate(read_json(path))


def import_batch(project: Project, path: Path) -> dict:
    value = validate(path)
    target = project.path(f"data/source-candidates/{value['batch_id']}/{digest(value)}.json")
    require(not native_path(target).exists(), "Duplicate source-candidate batch already imported")
    write_json(target, value, replace=False)
    return {
        "output": str(target.relative_to(project.root)),
        "batch_id": value["batch_id"],
        "candidates": len(value["candidates"]),
        "review_state": "unreviewed",
        "corpus_permission": False,
        "source_clearance_changed": False,
    }
