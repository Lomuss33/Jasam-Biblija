"""Read JEB-TRANSCRIPT/1. Never guess the structure of another TXT format."""

from __future__ import annotations

from jeb.core import Project, digest, identifier, json_loads, require, validate_schema

HEADER = b"JEB-TRANSCRIPT/1\n"


def plain_parts(parts: list[dict]) -> str:
    return "".join(p["text"] for p in parts if p["type"] == "text")


def check_nodes(nodes: list[dict], depth: int = 0) -> None:
    require(depth <= 8, "Nested note depth exceeds 8")
    for node in nodes:
        if node["type"] == "emphasis":
            check_nodes(node["children"], depth + 1)


def parse_bytes(project: Project, source: dict, lock: dict, payload: bytes) -> dict[str, dict]:
    require(
        payload.startswith(HEADER), "Wrong format: expected LF-terminated JEB-TRANSCRIPT/1 header"
    )
    text = payload.decode("utf-8", errors="strict")
    require(not text.startswith("\ufeff"), "Unexpected BOM")
    require(
        "\r" not in text, "Physical CR/CRLF unsupported; preserve bytes and make a reviewed adapter"
    )
    require(payload.endswith(b"\n"), "Missing final line terminator")
    books: dict[str, dict] = {}
    active = None
    block_ids: set[str] = set()
    note_ids: set[str] = set()
    offset = len(HEADER)
    ended = False
    for line_number, raw in enumerate(payload.splitlines(keepends=True)[1:], start=2):
        require(not ended, f"Record after end marker at line {line_number}")
        require(raw.strip(), f"Blank record at line {line_number}")
        record = json_loads(raw.decode("utf-8"))
        validate_schema("transcript-record", record)
        kind = record["type"]
        if kind == "book":
            book_id = record["book_id"]
            require(
                book_id in project.collection["books"],
                f"Book {book_id} is outside the approved collection",
            )
            require(book_id in lock["coverage"], f"Book {book_id} not in exact-edition manifest")
            require(
                record["scheme"] == source["versification"],
                "Transcript versification differs from the assessed source",
            )
            require(book_id not in books, f"Duplicate book {book_id}")
            require(
                not books
                or project.collection["books"].index(book_id)
                > project.collection["books"].index(next(reversed(books))),
                "Book ordering mismatch",
            )
            active = {
                "schema_version": "1.0",
                "corpus_kind": project.edition["corpus_kind"],
                "book_id": book_id,
                "source_id": source["source_id"],
                "source_sha256": lock["sha256"],
                "versification_scheme": record["scheme"],
                "expected_coverage_sha256": digest(lock["coverage"][book_id]),
                "segments": [],
                "blocks": [],
                "annotations": [],
            }
            books[book_id] = active
            block_ids = set()
        elif kind == "block":
            require(active is not None, "Block before book")
            identifier(record["block_id"])
            require(record["block_id"] not in block_ids, "Duplicate block ID")
            block_ids.add(record["block_id"])
            active["blocks"].append(
                {
                    "block_id": record["block_id"],
                    "kind": record["kind"],
                    "level": record["level"],
                    "segment_ids": [],
                }
            )
        elif kind == "segment":
            require(active is not None, "Segment before book")
            reference = {
                key: record[key]
                for key in ("chapter_label", "verse_label", "verse_labels", "alternate_labels")
            }
            expected = lock["coverage"][active["book_id"]]
            index = len(active["segments"])
            require(
                index < len(expected) and reference == expected[index],
                f"Missing, duplicate, reordered or unexpected reference at line {line_number}",
            )
            segment_id = f"{source['source_id']}:{active['book_id']}.{record['chapter_label']}.{record['verse_label']}"
            identifier(segment_id)
            source_span = {
                "file": f"data/raw/{source['source_id']}/{lock['sha256']}.txt",
                "line": line_number,
                "byte_start": offset,
                "byte_end": offset + len(raw),
            }
            require(any(p["type"] == "text" for p in record["parts"]), "Segment has no main text")
            for position, part in enumerate(record["parts"]):
                if part["type"] == "text":
                    require(part["block_id"] in block_ids, "Dangling block ID")
                    block = next(b for b in active["blocks"] if b["block_id"] == part["block_id"])
                    if segment_id not in block["segment_ids"]:
                        block["segment_ids"].append(segment_id)
                else:
                    check_nodes(part["content"])
                    identifier(part["annotation_id"])
                    require(part["annotation_id"] not in note_ids, "Duplicate annotation ID")
                    note_ids.add(part["annotation_id"])
                    active["annotations"].append(
                        {
                            "annotation_id": part["annotation_id"],
                            "segment_id": segment_id,
                            "kind": part["kind"],
                            "origin": "source",
                            "rights_source_id": source["source_id"],
                            "part_index": position,
                            "source_span": source_span,
                            "content": part["content"],
                        }
                    )
            reference["scheme"] = active["versification_scheme"]
            active["segments"].append(
                {
                    "segment_id": segment_id,
                    "book_id": active["book_id"],
                    "source_reference": reference,
                    "source_span": source_span,
                    "original_record": raw.decode("utf-8"),
                    "source_text": plain_parts(record["parts"]),
                    "normalized_text": None,
                    "normalization_changes": [],
                    "editorial_status": "source_only",
                }
            )
        else:
            require(active is not None, "End before any book")
            ended = True
        offset += len(raw)
    require(ended, "Truncated transcript: missing end record")
    require(
        set(books) == set(lock["coverage"]),
        "Source has missing books against exact-edition manifest",
    )
    for book_id, book in books.items():
        require(
            len(book["segments"]) == len(lock["coverage"][book_id]),
            f"Missing segments in {book_id}",
        )
        require(all(b["segment_ids"] for b in book["blocks"]), "Empty/unmapped layout block")
        validate_schema("book", book)
    return books
