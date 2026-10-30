"""Versioned JSONL relationships; claims are not made true merely by validation."""

from __future__ import annotations

from jeb.core import (
    Project,
    digest,
    file_id,
    json_loads,
    latin_tree,
    read_bytes,
    require,
    validate_schema,
)
from jeb.corpus import segments
from jeb.sources import registry


def validate_knowledge(project: Project, books: dict) -> dict[str, dict]:
    directory = project.path("data/knowledge")
    values = []
    if directory.exists():
        for path in sorted(directory.glob("*.jsonl")):
            for line in read_bytes(path).decode("utf-8").splitlines():
                require(bool(line.strip()), f"Blank knowledge record in {path.name}")
                values.append(json_loads(line))
    return validate_records(project, books, values)


def validate_records(project: Project, books: dict, values: list[dict]) -> dict[str, dict]:
    """Validate a complete in-memory graph without writing it to the canonical bank."""
    known_segments = segments(books)
    known_sources = {s["source_id"] for s in registry(project)["sources"]}
    records = {}
    for record in values:
        validate_schema("knowledge", record)
        latin_tree(record)
        file_id(record["record_id"])
        require(record["record_id"] not in records, "Duplicate knowledge ID")
        require(
            record["book_id"] in project.collection["books"],
            "Knowledge book outside collection",
        )
        require(
            all(
                s in known_segments and known_segments[s]["book_id"] == record["book_id"]
                for s in record["segment_ids"]
            ),
            "Dangling or out-of-book knowledge segment",
        )
        if record["source_id"] is not None:
            require(record["source_id"] in known_sources, "Unknown bibliographic source ID")
        if record["record_type"] == "evidence":
            require(
                bool(record["source_id"]) and bool(record["url"]) and bool(record["locator"]),
                "Evidence requires registered source, URL and exact locator",
            )
        if record["record_type"] == "claim" and record["layer"] in (
            "historical",
            "linguistic",
            "literary",
        ):
            require(
                bool(record["evidence_ids"]),
                "Nontrivial explanatory claim needs inspectable evidence",
            )
        require(
            not record["layer"] == "personal_reflection"
            or record["evidence_category"] == "personal_reflection",
            "Personal reflection mislabelled as evidence",
        )
        for segment_id in record["depends_on"]:
            require(segment_id in known_segments, "Dangling annotation/alignment dependency")
        if record["review_state"] == "approved":
            approval = record["approval"]
            require(
                approval is not None and approval["human_attestation"],
                "Annotation/claim approval needs an actual human review record",
            )
            unsigned = {k: v for k, v in record.items() if k != "approval"}
            require(
                approval["content_sha256"] == digest(unsigned),
                "Knowledge edited after approval",
            )
            require(
                set(record["depends_on"]) == set(record["segment_ids"]),
                "Approved metadata needs exact text hashes for every dependent segment",
            )
        records[record["record_id"]] = record
    for record in records.values():
        for key, expected_kind in (
            ("evidence_ids", "evidence"),
            ("claim_ids", "claim"),
            ("entity_ids", "entity"),
        ):
            require(
                all(
                    i in records and records[i]["record_type"] == expected_kind for i in record[key]
                ),
                f"Broken {key} foreign key in {record['record_id']}",
            )
        if record["review_state"] == "approved":
            require(
                all(
                    records[i]["review_state"] == "approved"
                    for key in ("evidence_ids", "claim_ids", "entity_ids")
                    for i in record[key]
                ),
                "Approved metadata depends on unreviewed records",
            )
        require(all(i in records for i in record["related_ids"]), "Dangling related record")
        if record["record_type"] == "entity" and record["selected_name_mapping_id"] is not None:
            # Local import avoids a dependency cycle with packet validation.
            from jeb.batch import names

            mappings = names(project)
            mapping_id = record["selected_name_mapping_id"]
            require(
                mapping_id in mappings and mappings[mapping_id]["status"] == "approved",
                "Entity uses unapproved display-name mapping",
            )
    return records
