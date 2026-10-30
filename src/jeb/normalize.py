"""Class A only: NFC and line-ending normalization, with exact before/after records."""

from __future__ import annotations

import copy
import unicodedata

from jeb.core import latin, require, validate_schema


def normalize_text(text: str) -> str:
    return unicodedata.normalize("NFC", text.replace("\r\n", "\n").replace("\r", "\n"))


def normalize_book(book: dict) -> dict:
    result = copy.deepcopy(book)
    for segment in result["segments"]:
        original = segment["source_text"]
        normalized = normalize_text(original)
        latin(normalized, segment["segment_id"])
        segment["normalized_text"] = normalized
        segment["normalization_changes"] = (
            []
            if normalized == original
            else [
                {
                    "rule_id": "A-NFC-LF-v1",
                    "change_class": "A",
                    "before": original,
                    "after": normalized,
                }
            ]
        )

    # Notes are preserved exactly. If display transliteration is needed, this adapter is insufficient.
    def nodes_latin(nodes):
        for node in nodes:
            if node["type"] == "text":
                latin(
                    node["text"],
                    "source annotation display; a reviewed transliteration is required",
                )
            else:
                nodes_latin(node["children"])

    for annotation in result["annotations"]:
        nodes_latin(annotation["content"])
    require(
        all(s["normalized_text"] is not None for s in result["segments"]),
        "Normalization incomplete",
    )
    validate_schema("book", result)
    return result
