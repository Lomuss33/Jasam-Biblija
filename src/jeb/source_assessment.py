"""Evidence-linked readiness checks, separate from source acquisition and legal opinions."""

from __future__ import annotations

from jeb.core import Project, digest, file_id, latin_tree, read_json, require, validate_schema

CHECKS = (
    "exact_edition",
    "digital_provenance",
    "component_rights",
    "versification_fidelity",
    "adapter",
)


def load_assessment(project: Project, source: dict) -> dict | None:
    path = project.path(f"sources/assessments/{file_id(source['source_id'])}.json")
    if not path.exists():
        return None
    value = read_json(path)
    validate_schema("source-assessment", value)
    latin_tree(value)
    require(value["source_id"] == source["source_id"], "Source assessment filename/ID mismatch")
    require(
        value["source_record_sha256"] == digest(source),
        "Source assessment is stale; re-evaluate after registry changes",
    )
    ids = [e["evidence_id"] for e in value["evidence"]]
    require(len(ids) == len(set(ids)), "Duplicate source-assessment evidence ID")
    for name in CHECKS:
        check = value["checks"][name]
        require(
            all(e in ids for e in check["evidence_ids"]),
            f"Dangling source-assessment evidence in {name}",
        )
        if check["status"] == "verified":
            require(bool(check["evidence_ids"]), f"Verified {name} has no evidence")
    for item in value["evidence"]:
        snapshot = item["snapshot"]
        if snapshot is not None and snapshot["private_cache_path"] is not None:
            cache = project.path(snapshot["private_cache_path"])
            require(
                cache.resolve().is_relative_to(project.path("sources/evidence/private").resolve()),
                "Metadata snapshot cache must stay in sources/evidence/private",
            )
    metadata = value["module_metadata"]
    if metadata is not None:
        require(
            any(
                e["url"] == metadata["url"]
                and e["snapshot"] is not None
                and e["snapshot"]["sha256"] == metadata["sha256"]
                and e["snapshot"]["size_bytes"] == metadata["size_bytes"]
                for e in value["evidence"]
            ),
            "Module metadata lacks matching evidence snapshot",
        )
        declared_scheme = metadata["declared_fields"].get("Versification")
        require(
            declared_scheme is None or declared_scheme == source["versification"],
            "Provider metadata and registered versification disagree",
        )
    return value


def historical_gaps(project: Project, source: dict) -> list[dict]:
    if project.synthetic:
        return []
    result = []
    for field in ("year", "publication_place", "transcriber"):
        if not source["edition"][field]:
            result.append(
                {
                    "code": f"missing_edition_{field}",
                    "detail": f"Exact source edition {field} is not established.",
                }
            )
    if not source["versification"]:
        result.append(
            {"code": "missing_versification", "detail": "Source-specific versification is unknown."}
        )
    assessment = load_assessment(project, source)
    if assessment is None:
        result.append(
            {
                "code": "missing_source_assessment",
                "detail": "No evidence-linked source assessment exists.",
            }
        )
    else:
        for name in CHECKS:
            check = assessment["checks"][name]
            if check["status"] != "verified":
                result.append({"code": f"unresolved_{name}", "detail": check["summary"]})
    return result


def inspect_source(project: Project, source_id: str) -> dict:
    # Imports here keep this read-only reporting module independent of registry admission.
    from jeb.core import JebError
    from jeb.sources import admitted, registry, source_lock

    file_id(source_id)
    records = {s["source_id"]: s for s in registry(project)["sources"]}
    require(source_id in records, f"Unknown source: {source_id}")
    source = records[source_id]
    assessment = load_assessment(project, source)
    gaps = historical_gaps(project, source)
    if source["status"] != "verified_for_scope":
        gaps.insert(
            0, {"code": "source_not_verified", "detail": f"Source status is {source['status']}."}
        )
    for country in project.edition["jurisdictions"]:
        rights = source["rights_by_jurisdiction"].get(country)
        if (
            rights is None
            or rights["status"] != "verified"
            or not rights["basis"]
            or not rights["evidence_urls"]
        ):
            gaps.append(
                {
                    "code": f"unresolved_rights_{country}",
                    "detail": f"Exact-artifact rights remain unverified for {country}.",
                }
            )
    locks = {s["source_id"]: s for s in source_lock(project)["sources"]}
    if source_id not in locks:
        gaps.append(
            {"code": "missing_lock", "detail": "No reviewed corpus artifact/coverage lock exists."}
        )
    allowed = False
    gate_error = None
    try:
        admitted(project, source_id)
        allowed = True
    except JebError as exc:
        gate_error = str(exc)
    return {
        "schema_version": "1.0",
        "source_id": source_id,
        "status": source["status"],
        "source_record_sha256": digest(source),
        "admitted": allowed,
        "scope": project.edition["jurisdictions"],
        "admission_blockers": gaps,
        "admission_error": gate_error,
        "source_artifact": source["artifact"],
        "assessment": assessment,
        "notice": "Metadata snapshot hashes identify evidence only; they are not corpus hashes or clearance.",
    }
