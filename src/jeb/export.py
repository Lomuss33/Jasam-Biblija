"""Deterministic reader artifacts, exact coverage and independent release gates."""

from __future__ import annotations

from jeb.batch import names
from jeb.core import Project, atomic_write, digest, latin_tree, require, sha256, validate_schema
from jeb.corpus import load_corpus, segments
from jeb.knowledge import provenance_current, source_cards, validate_knowledge
from jeb.review import all_decisions, decision_item, heads
from jeb.sources import admitted


def reader(project: Project, source_id: str, maturity: str, profile: str = "five-book") -> dict:
    require(profile == "five-book", "Unknown collection profile")
    require(maturity in ("preview", "release"), "Unknown export maturity")
    source, lock = admitted(project, source_id)
    books = load_corpus(project, source_id)
    names(project)
    knowledge = validate_knowledge(project, books)
    decisions = heads(all_decisions(project))
    known = segments(books)
    selected_decisions = {k: d for k, d in decisions.items() if k in known}
    approved = {}
    for segment_id, decision in selected_decisions.items():
        _, item = decision_item(project, decision)
        if decision["state"] == "approved":
            approved[segment_id] = item
    complete = all(
        book_id in books and book_id in lock["complete_books"]
        for book_id in project.collection["books"]
    )
    if maturity == "release":
        require(not project.synthetic, "Synthetic fixtures can never be a public edition release")
        require(complete, "Five complete source books have not been verified")
        require(set(approved) == set(known), "Every included passage requires exact owner approval")
        require(
            project.edition["release_preface_approved"], "Honest release preface is not approved"
        )
        require(
            bool(source["credits"]) and bool(source["license_notice"]),
            "Missing upstream credits/license notices",
        )
    output_books = []
    for book_id in project.collection["books"]:
        if book_id not in books:
            continue
        book = books[book_id]
        output_segments = []
        for segment in book["segments"]:
            item = approved.get(segment["segment_id"])
            text = item["proposed_text"] if item else segment["normalized_text"]
            output_segments.append(
                {
                    "segment_id": segment["segment_id"],
                    "source_reference": segment["source_reference"],
                    "source_span": segment["source_span"],
                    "text": text,
                    "text_sha256": sha256(text.encode("utf-8")),
                    "editorial_status": (
                        "approved_unchanged"
                        if item and item["action"] == "no_change"
                        else "approved_modernization"
                        if item
                        else "source_only"
                    ),
                    "decision_id": selected_decisions[segment["segment_id"]]["decision_id"]
                    if item
                    else None,
                }
            )
        output_books.append(
            {
                "book_id": book_id,
                "segments": output_segments,
                "blocks": book["blocks"],
                "source_annotations": book["annotations"],
            }
        )
    display_hashes = {
        s["segment_id"]: s["text_sha256"] for b in output_books for s in b["segments"]
    }
    eligible_metadata = {}
    metadata_hash = digest(source_cards(project))
    policy_hash = project.policy_hash()
    for record in knowledge.values():
        current = all(display_hashes.get(s) == h for s, h in record["depends_on"].items())
        if (
            record["review_state"] == "approved"
            and current
            and provenance_current(record, knowledge, policy_hash, metadata_hash, digest(books))
        ):
            eligible_metadata[record["record_id"]] = record
    # Never publish a current note whose supporting claim/evidence is stale.
    # Remove stale dependencies transitively while allowing documented cycles.
    while True:
        retained = {
            key: record
            for key, record in eligible_metadata.items()
            if all(
                ref in eligible_metadata
                for field in ("evidence_ids", "claim_ids", "entity_ids", "related_ids")
                for ref in record[field]
            )
        }
        if len(retained) == len(eligible_metadata):
            break
        eligible_metadata = retained
    approved_metadata = list(eligible_metadata.values())
    pending_metadata = len(knowledge) - len(approved_metadata)
    artifact = {
        "schema_version": "1.0",
        "edition_id": project.edition["edition_id"],
        "edition_version": project.edition["version"],
        "maturity": maturity,
        "corpus_kind": project.edition["corpus_kind"],
        "title": project.edition["title"],
        "description": "Synthetic software fixture; NOT biblical text."
        if project.synthetic
        else "Selected collection; independently edited modernization of credited historical text.",
        "collection_profile": profile,
        "approved_books": project.collection["books"],
        "collection_complete": complete,
        "jurisdictions": project.edition["jurisdictions"],
        "policy_sha256": project.policy_hash(),
        "normalized_corpus_sha256": digest(books),
        "sources": [
            {
                "source_id": source_id,
                "sha256": lock["sha256"],
                "credits": source["credits"],
                "license_notice": source["license_notice"],
                "rights_status": source["status"],
            }
        ],
        "coverage": [
            {
                "book_id": b,
                "source_complete": b in lock["complete_books"],
                "source_segments": len(books.get(b, {}).get("segments", [])),
                "approved_segments": sum(
                    s["segment_id"] in approved for s in books.get(b, {}).get("segments", [])
                ),
                "state": "available"
                if b in books
                else next(
                    (
                        a["state"]
                        for a in lock["absences"]
                        if a["book_id"] == b and a["chapter_label"] is None
                    ),
                    "not_ingested",
                ),
            }
            for b in project.collection["books"]
        ],
        "annotation_coverage": {
            "records": len(knowledge),
            "approved_current": len(approved_metadata),
            "pending_or_stale": pending_metadata,
        },
        "absences": lock["absences"],
        "books": output_books,
        "knowledge": approved_metadata,
    }
    validate_schema("reader", artifact)
    latin_tree(artifact)
    return artifact


def export(
    project: Project, source_id: str, maturity: str, fmt: str, output: str, profile: str
) -> dict:
    artifact = reader(project, source_id, maturity, profile)
    from jeb.core import canonical

    if fmt == "json":
        payload = canonical(artifact)
    else:
        require(fmt == "markdown", "Only JSON and Markdown exports are implemented")
        lines = [
            f"# {artifact['title']}",
            "",
            artifact["description"],
            "",
            f"Maturity: {maturity}. Collection complete: {artifact['collection_complete']}.",
            "",
            "Approved collection: GEN, MAT, MRK, LUK, JHN.",
            f"Rights assessment scope: {', '.join(artifact['jurisdictions'])}.",
            "No unapproved modernization is included.",
            "",
        ]
        for source in artifact["sources"]:
            lines.extend(
                [
                    f"Source: {source['source_id']}; SHA-256: {source['sha256']}",
                    source["credits"],
                    source["license_notice"],
                    "",
                ]
            )
        for coverage in artifact["coverage"]:
            lines.append(
                f"{coverage['book_id']}: {coverage['source_segments']} source segments; "
                f"{coverage['approved_segments']} approved; {coverage['state']}; "
                f"source complete: {coverage['source_complete']}."
            )
        for book in artifact["books"]:
            lines.extend(["", f"## {book['book_id']}", ""])
            for segment in book["segments"]:
                ref = segment["source_reference"]
                lines.extend(
                    [
                        f"### {ref['chapter_label']}:{ref['verse_label']} ({segment['editorial_status']})",
                        "",
                        segment["text"],
                        "",
                    ]
                )
            # Preserve the same typed annotations/layout as JSON without merging them into verse text.
            import json

            lines.extend(
                [
                    "Source layout and notes (typed data):",
                    "",
                    "```json",
                    json.dumps(
                        {
                            "blocks": book["blocks"],
                            "source_annotations": book["source_annotations"],
                        },
                        ensure_ascii=False,
                        sort_keys=True,
                        indent=2,
                    ),
                    "```",
                    "",
                ]
            )
        if artifact["knowledge"]:
            import json

            lines.extend(
                [
                    "Approved knowledge records:",
                    "",
                    "```json",
                    json.dumps(artifact["knowledge"], ensure_ascii=False, sort_keys=True, indent=2),
                    "```",
                ]
            )
        payload = ("\n".join(lines).rstrip() + "\n").encode("utf-8")
    atomic_write(project.path(output), payload)
    return {
        "output": output,
        "sha256": sha256(payload),
        "maturity": maturity,
        "synthetic": project.synthetic,
        "source_segments": sum(c["source_segments"] for c in artifact["coverage"]),
    }
