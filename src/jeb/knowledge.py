"""Versioned JSONL relationships; claims are not made true merely by validation."""

from __future__ import annotations

from jeb.core import (
    Project,
    digest,
    file_id,
    json_loads,
    latin_tree,
    native_path,
    read_bytes,
    require,
    validate_schema,
)
from jeb.corpus import segments
from jeb.sources import registry


def stored_records(project: Project) -> dict[str, dict]:
    """Read canonical identities without requiring rights to display current corpus text."""
    from jeb.knowledge_review import promoted_records, read_receipts

    directory = native_path(project.path("data/knowledge"))
    values = []
    if directory.exists():
        for path in sorted(directory.glob("*.jsonl")):
            for line in read_bytes(path).decode("utf-8").splitlines():
                require(bool(line.strip()), f"Blank knowledge record in {path.name}")
                record = json_loads(line)
                require(
                    "provenance" not in record,
                    "Staged provenance must derive from its immutable review receipt",
                )
                values.append(record)
    values.extend(promoted_records(read_receipts(project)))
    records = {}
    for record in values:
        validate_schema("knowledge", record)
        latin_tree(record)
        file_id(record["record_id"])
        require(record["record_id"] not in records, "Duplicate knowledge ID")
        require(
            record["book_id"] in project.collection["books"], "Knowledge book outside collection"
        )
        if record["review_state"] == "approved":
            require(record["approval"] is not None, "Approved knowledge lacks human approval")
            require(
                record["approval"]["content_sha256"]
                == digest({k: v for k, v in record.items() if k != "approval"}),
                "Knowledge edited after approval",
            )
        records[record["record_id"]] = record
    return records


def target_identity(record: dict) -> dict:
    require(
        record["review_state"] == "approved" and record["approval"] is not None,
        "Curation targets must already be human-approved",
    )
    return {
        "record_id": record["record_id"],
        "record_sha256": digest(record),
        "approval_sha256": digest(record["approval"]),
        "provenance_sha256": digest(record["provenance"]) if "provenance" in record else None,
    }


def version_scope(record: dict) -> tuple:
    return (
        record["record_type"],
        record["book_id"],
        record["layer"],
        record["evidence_category"],
        tuple(sorted(record["segment_ids"])),
    )


def validate_knowledge(project: Project, books: dict) -> dict[str, dict]:
    from jeb.knowledge_curation import read_receipts, validate_targets

    records = validate_records(project, books, list(stored_records(project).values()))
    validate_targets(read_receipts(project), records)
    return records


def source_cards(project: Project) -> list[dict]:
    """Bibliographic metadata only; listing a source grants no reuse permission."""
    return [
        {
            field: source[field]
            for field in (
                "source_id",
                "title",
                "kind",
                "status",
                "landing_url",
                "rights_statement_url",
            )
        }
        for source in registry(project)["sources"]
    ]


def provenance_current(
    record: dict, records: dict, policy_hash: str, metadata_hash: str, corpus_hash: str
) -> bool:
    origin = record.get("provenance")
    if origin is None:
        return True
    if (
        origin["policy_sha256"] != policy_hash
        or origin["source_metadata_sha256"] != metadata_hash
        or origin["corpus_sha256"] != corpus_hash
    ):
        return False
    for ref, binding in origin["support"].items():
        target = records.get(ref)
        if target is None:
            return False
        if binding["kind"] == "canonical":
            if digest(target) != binding["sha256"]:
                return False
        else:
            target_origin = target.get("provenance", {})
            if not (
                target_origin.get("packet_sha256") == origin["packet_sha256"]
                and target_origin.get("response_sha256") == origin["response_sha256"]
                and target_origin.get("draft_sha256") == binding["sha256"]
            ):
                return False
    return True


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
        if "provenance" in record:
            require(
                record["review_state"] == "approved",
                "Review projection must retain its approved state",
            )
            require(
                set(record["provenance"]["support"])
                == {
                    ref
                    for field in ("evidence_ids", "claim_ids", "entity_ids", "related_ids")
                    for ref in record[field]
                },
                "Promoted knowledge needs exact support provenance",
            )
        records[record["record_id"]] = record
    for record in records.values():
        parent = record.get("provenance", {}).get("version_of")
        if parent is not None:
            require(
                parent["record_id"] in records and parent["record_id"] != record["record_id"],
                "Missing/self original knowledge version",
            )
            original = records[parent["record_id"]]
            require(
                parent == target_identity(original), "Original knowledge version identity changed"
            )
            require(
                version_scope(record) == version_scope(original),
                "Knowledge revision changes its category or passage scope",
            )
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
