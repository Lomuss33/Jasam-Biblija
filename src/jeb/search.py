"""Rebuildable SQLite FTS5. No cloud, embeddings or changes to canonical IDs."""

from __future__ import annotations

import sqlite3
from contextlib import closing

from jeb.batch import names
from jeb.core import Project, digest, require
from jeb.export import reader


def build_index(project: Project, source_id: str) -> dict:
    artifact = reader(project, source_id, "preview")
    mappings = [m for m in names(project).values() if m["status"] == "approved"]
    path = project.path("data/index/search.sqlite3")
    path.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(path)) as connection, connection:
        connection.execute("DROP TABLE IF EXISTS passage_search")
        connection.execute("DROP TABLE IF EXISTS metadata")
        connection.execute(
            "CREATE VIRTUAL TABLE passage_search USING fts5(segment_id UNINDEXED, book_id UNINDEXED, text, aliases)"
        )
        connection.execute(
            "CREATE TABLE metadata (artifact_sha256 TEXT NOT NULL, source_id TEXT NOT NULL)"
        )
        count = 0
        for book in artifact["books"]:
            for segment in book["segments"]:
                aliases = " ".join(
                    alias
                    for mapping in mappings
                    if mapping["display_form"] in segment["text"]
                    for alias in [*mapping["aliases"], mapping["attested_form_latin"]]
                )
                connection.execute(
                    "INSERT INTO passage_search VALUES (?,?,?,?)",
                    (segment["segment_id"], book["book_id"], segment["text"], aliases),
                )
                count += 1
        connection.execute("INSERT INTO metadata VALUES (?,?)", (digest(artifact), source_id))
    return {
        "path": "data/index/search.sqlite3",
        "segments": count,
        "corpus_kind": artifact["corpus_kind"],
    }


def search(project: Project, query: str, source_id: str) -> list[dict]:
    artifact = reader(project, source_id, "preview")
    path = project.path("data/index/search.sqlite3")
    require(path.exists(), "No search index; run jeb index first")
    with closing(sqlite3.connect(path)) as connection:
        expected = connection.execute("SELECT artifact_sha256, source_id FROM metadata").fetchone()
        require(expected == (digest(artifact), source_id), "Stale index; rebuild before searching")
        # Quote a user's literal query, rather than expose FTS query syntax or SQL interpolation.
        literal = '"' + query.replace('"', '""') + '"'
        rows = connection.execute(
            "SELECT segment_id,book_id,text FROM passage_search WHERE passage_search MATCH ? LIMIT 25",
            (literal,),
        )
        return [{"segment_id": r[0], "book_id": r[1], "text": r[2]} for r in rows]
