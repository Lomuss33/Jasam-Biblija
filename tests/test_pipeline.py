from __future__ import annotations

import copy
import json

from jeb.core import JebError, canonical, read_json, write_json
from jeb.corpus import ingest, load_corpus, rebuild
from jeb.normalize import normalize_book, normalize_text
from tests.support import WorkspaceTest


class ParserTests(WorkspaceTest):
    def test_source_roundtrip_and_precise_offsets(self):
        raw = self.raw()
        book = self.books()["GEN"]
        for segment in book["segments"]:
            span = segment["source_span"]
            self.assertEqual(
                raw[span["byte_start"] : span["byte_end"]].decode("utf-8"),
                segment["original_record"],
            )
            original = json.loads(segment["original_record"])
            main = "".join(p["text"] for p in original["parts"] if p["type"] == "text")
            self.assertEqual(main, segment["source_text"])

    def test_multiline_nested_notes_poetry_bridges_and_alternate_numbers(self):
        book = self.books()["GEN"]
        self.assertEqual(len(book["segments"]), 4)
        self.assertIn("\n", book["segments"][0]["source_text"])
        self.assertEqual(book["segments"][1]["source_reference"]["alternate_labels"], ["2"])
        self.assertEqual(book["segments"][2]["source_reference"]["verse_labels"], ["3", "4"])
        self.assertEqual(book["blocks"][1]["kind"], "poetry")
        self.assertIn(book["segments"][2]["segment_id"], book["blocks"][0]["segment_ids"])
        self.assertIn(book["segments"][2]["segment_id"], book["blocks"][1]["segment_ids"])
        self.assertEqual(len(book["annotations"]), 3)
        self.assertEqual(book["annotations"][1]["content"][1]["children"][1]["type"], "emphasis")
        self.assertNotIn("Sintetički naslov", book["segments"][0]["source_text"])
        self.assertNotIn("Probna bilješka", book["segments"][0]["source_text"])

    def test_nfc_lf_and_explained_differences(self):
        segment = self.books()["GEN"]["segments"][-1]
        self.assertIn("C\u030c", segment["source_text"])
        self.assertIn("Čitanje", segment["normalized_text"])
        self.assertNotIn("\r", segment["normalized_text"])
        self.assertEqual(segment["normalization_changes"][0]["before"], segment["source_text"])
        self.assertEqual(segment["normalization_changes"][0]["after"], segment["normalized_text"])

    def test_normalization_idempotence_and_preserves_negation_numbers_names(self):
        sample = "covik ne mijenja 2 broja. Ana čuva svjet, vrjeme i razumit."
        self.assertEqual(normalize_text(sample), sample)
        book = self.books()["GEN"]
        self.assertEqual(normalize_book(normalize_book(book)), normalize_book(book))

    def test_source_hash_change_blocks_rebuild(self):
        lock = read_json(self.project.path("sources/lock.json"))["sources"][0]
        path = self.project.path(f"data/raw/{self.source_id}/{lock['sha256']}.txt")
        path.write_bytes(path.read_bytes() + b"x")
        with self.assertRaisesRegex(JebError, "bytes changed"):
            rebuild(self.project, self.source_id, normalized=False)

    def test_parser_failures_quarantine_without_partial_records(self):
        original = self.raw()
        variants = {
            "usfm": b"\\id GEN\n\\c 1\n\\v 1 synthetic\n",
            "unknown_marker": original.replace(b'"type":"block"', b'"type":"unknown"', 1),
            "duplicate": original.replace(b'"verse_label":"2a"', b'"verse_label":"1"'),
            "missing": original.replace(original.splitlines(keepends=True)[4], b""),
            "truncated": original.rsplit(b'{"type":"end"}', 1)[0],
            "decoding": original.replace(b"covik", b"\xff\xfe"),
            "outside_book": original.replace(b'"book_id":"GEN"', b'"book_id":"PSA"'),
            "unknown_fields": original.replace(b'"type":"end"', b'"type":"end","invented":1'),
        }
        for name, payload in variants.items():
            self.rewrite_fixture(payload)
            with self.subTest(name=name), self.assertRaises((JebError, UnicodeError)):
                ingest(self.project, self.source_id, normalized=False)
            self.assertTrue(
                self.project.path(f"data/quarantine/{self.source_id}/transcribed.json").exists()
            )

    def test_source_script_preserved_but_display_requires_transliteration(self):
        payload = self.raw().replace(b"covik", "\u0447ovik".encode("utf-8"))
        self.rewrite_fixture(payload)
        parsed = rebuild(self.project, self.source_id, normalized=False)
        self.assertIn("\u0447ovik", parsed["GEN"]["segments"][0]["source_text"])
        with self.assertRaisesRegex(JebError, "display-script"):
            rebuild(self.project, self.source_id, normalized=True)

    def test_modified_normalized_and_extra_books_rejected(self):
        path = self.project.path(f"data/normalized/{self.source_id}/GEN.json")
        original = read_json(path)
        changed = copy.deepcopy(original)
        changed["segments"][0]["normalized_text"] += " changed"
        write_json(path, changed)
        with self.assertRaisesRegex(JebError, "differs"):
            load_corpus(self.project, self.source_id)
        write_json(path, original)
        write_json(self.project.path(f"data/normalized/{self.source_id}/PSA.json"), original)
        with self.assertRaisesRegex(JebError, "Unexpected"):
            load_corpus(self.project, self.source_id)

    def test_deterministic_rebuild(self):
        self.assertEqual(
            canonical(self.books()),
            canonical(rebuild(self.project, self.source_id, normalized=True)),
        )

    def test_unsupported_nested_character_structure_rejected(self):
        payload = self.raw().replace(b'"type":"emphasis"', b'"type":"milestone"', 1)
        self.rewrite_fixture(payload)
        with self.assertRaises(JebError):
            rebuild(self.project, self.source_id, normalized=False)
