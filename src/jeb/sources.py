"""Source admission is separate from acquisition. No automatic registration or unlock."""

from __future__ import annotations

from jeb.core import (
    Project,
    digest,
    file_id,
    latin_tree,
    read_json,
    read_yaml,
    require,
    validate_schema,
)


def registry(project: Project) -> dict:
    value = read_yaml(project.path("sources/registry.yaml"))
    validate_schema("registry", value)
    latin_tree(value)
    ids = [s["source_id"] for s in value["sources"]]
    require(len(ids) == len(set(ids)), "Duplicate source ID")
    return value


def source_lock(project: Project) -> dict:
    value = read_json(project.path("sources/lock.json"))
    validate_schema("lock", value)
    ids = [s["source_id"] for s in value["sources"]]
    require(len(ids) == len(set(ids)), "Duplicate locked source ID")
    return value


def admitted(project: Project, source_id: str) -> tuple[dict, dict]:
    file_id(source_id)
    sources = {s["source_id"]: s for s in registry(project)["sources"]}
    require(source_id in sources, f"Unknown source: {source_id}")
    source = sources[source_id]
    require(
        source["status"] == "verified_for_scope",
        f"Source {source_id}: {source['status']}; ingestion blocked",
    )
    require(
        source["kind"] == ("synthetic" if project.synthetic else "historical"),
        "Synthetic and historical source workspaces cannot be mixed",
    )
    scope = project.edition["jurisdictions"]
    for country in scope:
        assessment = source["rights_by_jurisdiction"].get(country)
        require(
            assessment is not None and assessment["status"] == "verified",
            f"Unverified source rights for {country}",
        )
        require(
            bool(assessment["basis"]) and bool(assessment["evidence_urls"]),
            f"Missing rights evidence for {country}",
        )
    require(
        bool(source["assessment"]["author"]) and bool(source["assessment"]["review_date"]),
        "Missing assessment author/date",
    )
    from jeb.source_assessment import historical_gaps

    gaps = historical_gaps(project, source)
    require(not gaps, "Unresolved source admission checks: " + "; ".join(g["code"] for g in gaps))
    locks = {s["source_id"]: s for s in source_lock(project)["sources"]}
    require(source_id in locks, f"Source {source_id} has no reviewed lock")
    lock = locks[source_id]
    require(
        lock["source_record_sha256"] == digest(source),
        "Source assessment changed; re-evaluate lock",
    )
    require(
        source["artifact"]["sha256"] == lock["sha256"]
        and source["artifact"]["size_bytes"] == lock["size_bytes"]
        and source["artifact"]["format"] == lock["format"],
        "Registry/lock artifact mismatch",
    )
    require(
        lock["download_url"] in source["download_urls"]
        or (project.synthetic and lock["download_url"] is None),
        "Locked URL not allowlisted",
    )
    require(
        set(lock["coverage"]).issubset(project.collection["books"]),
        "Locked production coverage includes an unapproved book",
    )
    require(bool(lock["coverage"]), "Missing exact-edition coverage manifest")
    require(
        set(lock["complete_books"]).issubset(lock["coverage"]),
        "Complete book missing from manifest",
    )
    for book_id, references in lock["coverage"].items():
        ids, mapped = set(), set()
        for reference in references:
            key = (reference["chapter_label"], reference["verse_label"])
            require(key not in ids, f"Duplicate manifest segment: {book_id} {key}")
            ids.add(key)
            for label in reference["verse_labels"]:
                key = (reference["chapter_label"], label)
                require(
                    key not in mapped, "Overlapping reference mappings unsupported by this adapter"
                )
                mapped.add(key)
        for absence in lock["absences"]:
            if absence["book_id"] == book_id:
                require(absence["chapter_label"] is not None, "Available book marked wholly absent")
                require(
                    (absence["chapter_label"], absence["verse_label"]) not in mapped,
                    "Available verse marked absent",
                )
    return source, lock


def audit(project: Project) -> dict:
    data = registry(project)
    locks = source_lock(project)
    known = {s["source_id"] for s in data["sources"]}
    require(all(s["source_id"] in known for s in locks["sources"]), "Orphan source lock")
    from jeb.source_assessment import load_assessment

    directory = project.path("sources/assessments")
    require(
        not directory.exists() or all(p.stem in known for p in directory.glob("*.json")),
        "Orphan source assessment",
    )
    results = []
    for source in data["sources"]:
        load_assessment(project, source)
        allowed = False
        reason = source["status"]
        if source["status"] == "verified_for_scope":
            admitted(project, source["source_id"])
            allowed, reason = True, "admitted for configured scope only"
        results.append(
            {
                "source_id": source["source_id"],
                "status": source["status"],
                "admitted": allowed,
                "reason": reason,
            }
        )
    return {
        "schema_version": "1.0",
        "corpus_kind": project.edition["corpus_kind"],
        "jurisdictions": project.edition["jurisdictions"],
        "sources": results,
        "admitted_count": sum(item["admitted"] for item in results),
    }
