"""Rebuild from locked source bytes; never trust hand-edited normalized artifacts."""

from __future__ import annotations

from jeb.core import Project, digest, read_bytes, read_json, require, sha256, write_json
from jeb.fetch import MAX_DOWNLOAD
from jeb.normalize import normalize_book
from jeb.parse.transcript import parse_bytes
from jeb.sources import admitted


def rebuild(project: Project, source_id: str, *, normalized: bool) -> dict[str, dict]:
    source, lock = admitted(project, source_id)
    require(
        lock["format"] == "jeb-transcript-v1",
        "Unsupported source format; adapter evaluation required",
    )
    payload = read_bytes(project.path(f"data/raw/{source_id}/{lock['sha256']}.txt"), MAX_DOWNLOAD)
    require(
        sha256(payload) == lock["sha256"] and len(payload) == lock["size_bytes"],
        "Locked source bytes changed",
    )
    books = parse_bytes(project, source, lock, payload)
    return {key: normalize_book(book) if normalized else book for key, book in books.items()}


def ingest(project: Project, source_id: str, *, normalized: bool) -> dict:
    stage = "normalized" if normalized else "transcribed"
    try:
        books = rebuild(project, source_id, normalized=normalized)
    except (ValueError, UnicodeError, OSError) as exc:
        # Retain a diagnostic, never guessed or partially parsed text.
        write_json(
            project.path(f"data/quarantine/{source_id}/{stage}.json"),
            {"source_id": source_id, "stage": stage, "error": str(exc)},
        )
        raise
    for book_id, book in books.items():
        write_json(project.path(f"data/{stage}/{source_id}/{book_id}.json"), book, replace=False)
    return {
        "source_id": source_id,
        "stage": stage,
        "books": list(books),
        "segments": sum(len(b["segments"]) for b in books.values()),
        "corpus_sha256": digest(books),
    }


def load_corpus(project: Project, source_id: str) -> dict[str, dict]:
    books = rebuild(project, source_id, normalized=True)
    directory = project.path(f"data/normalized/{source_id}")
    require(directory.is_dir(), "No normalized corpus; run jeb normalize first")
    require(
        {p.name for p in directory.iterdir()} == {f"{b}.json" for b in books},
        "Unexpected or missing per-book normalized files",
    )
    for book_id, expected in books.items():
        actual = read_json(project.path(f"data/normalized/{source_id}/{book_id}.json"))
        require(
            actual == expected, f"Normalized artifact differs from locked source/rules: {book_id}"
        )
    return books


def segments(books: dict[str, dict]) -> dict[str, dict]:
    return {s["segment_id"]: s for book in books.values() for s in book["segments"]}
