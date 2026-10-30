from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from jeb.core import JebError, canonical, read_json, sha256
from jeb.sword_diagnostic import (
    check_tool_lock,
    evaluate,
    expected_slots,
    fixture_entries,
    validate_capture,
    validate_probe,
    xml_tree,
)
from tests.support import REPO, WorkspaceTest

CAPTURE = REPO / "tests/fixtures/sword/synthetic-probe.jsonl"


class DiagnosticCaptureTests(unittest.TestCase):
    def rows(self):
        return [json.loads(line) for line in CAPTURE.read_text("utf-8").splitlines()]

    def payload(self, rows):
        return b"".join(canonical(row).replace(b"\n", b"") + b"\n" for row in rows)

    def test_actual_native_capture_is_explicitly_synthetic(self):
        result = validate_capture(CAPTURE)
        self.assertEqual(result["real_biblical_segments"], 0)
        self.assertEqual(result["requested_slots"], 10)
        self.assertEqual(result["present_slots"], 9)
        self.assertEqual(result["stored_entries"], 8)
        self.assertFalse(result["production_adapter_approved"])

    def test_link_is_not_inferred_from_identical_text(self):
        rows = {r["osis_id"]: r for r in self.rows()}
        self.assertEqual(rows["Gen.1.3"]["stored_osis"], rows["Gen.1.7"]["stored_osis"])
        self.assertEqual(rows["Gen.1.4"]["linked_to"], "Gen.1.3")
        self.assertIsNone(rows["Gen.1.7"]["linked_to"])
        changed = self.rows()
        changed[8]["linked_to"] = "Gen.1.3"
        with self.assertRaisesRegex(JebError, "Link was"):
            validate_probe(self.payload(changed))

    def test_raw_stored_bytes_and_engine_changes_remain_distinct(self):
        rows = {r["osis_id"]: r for r in self.rows()}
        self.assertIn("\nnovi red", rows["Gen.1.5"]["stored_osis"])
        self.assertNotIn("\n", rows["Gen.1.5"]["engine_osis"])
        result = validate_capture(CAPTURE)
        self.assertEqual(len(result["engine_transformations"]), 9)
        self.assertEqual(result["introduced_eof_lf"], ["Matt.5.1"])
        self.assertEqual(expected_slots()["Matt.5.1"], fixture_entries()["Matt.5.1"] + "\n")

    def test_heading_notes_nested_markup_and_poetry_preserved(self):
        rows = {r["osis_id"]: r for r in self.rows()}
        tree = xml_tree(rows["Gen.1.1"]["stored_osis"], fragment=True)
        self.assertEqual(len(tree.findall("title")), 1)
        self.assertEqual(len(tree.findall(".//note/hi/hi")), 1)
        poetry = xml_tree(rows["Gen.1.2"]["stored_osis"], fragment=True)
        self.assertEqual(len(poetry.findall(".//l")), 2)
        for form in ("svjet", "vrjeme", "razumit", "č", "ć", "đ", "š", "ž"):
            self.assertIn(form, rows["Gen.1.2"]["stored_osis"])

    def test_introductions_and_missing_slot_are_not_verses_or_filled_text(self):
        rows = self.rows()
        self.assertEqual(rows[0]["entry_kind"], "book_introduction")
        self.assertEqual(rows[1]["entry_kind"], "chapter_introduction")
        self.assertFalse(rows[7]["has_entry"])
        rows[7]["has_entry"] = True
        with self.assertRaisesRegex(JebError, "Empty-slot"):
            validate_probe(self.payload(rows))

    def test_fabricated_historical_and_outside_collection_records_rejected(self):
        original = self.rows()
        for key, value in (
            ("module_id", "SrKDIjekav"),
            ("scheme", "KJV"),
            ("osis_id", "Ps.1.1"),
            ("unexpected", "field"),
        ):
            rows = copy.deepcopy(original)
            rows[2][key] = value
            with self.subTest(key=key), self.assertRaises(JebError):
                validate_probe(self.payload(rows))

    def test_duplicate_missing_or_reordered_slot_rejected(self):
        original = self.rows()
        for rows in (
            original[:-1],
            list(reversed(original)),
            [original[0], *original[1:-1], original[0]],
        ):
            with self.subTest(rows=rows), self.assertRaises(JebError):
                validate_probe(self.payload(rows))

    def test_byte_lengths_and_unexplained_changes_rejected(self):
        for key in ("raw_length_bytes", "stored_length_bytes"):
            rows = self.rows()
            rows[2][key] += 1
            with self.subTest(key=key), self.assertRaisesRegex(JebError, "length mismatch"):
                validate_probe(self.payload(rows))
        rows = self.rows()
        rows[2]["stored_osis"] = rows[2]["stored_osis"].replace(" ne ", " ")
        rows[2]["stored_length_bytes"] = len(rows[2]["stored_osis"].encode("utf-8"))
        with self.assertRaisesRegex(JebError, "Stored entry differs"):
            validate_probe(self.payload(rows))

    def test_schema_and_original_capture_provenance(self):
        provenance = read_json(REPO / "tests/fixtures/sword/capture-provenance.json")
        self.assertEqual(provenance["fixture_sha256"], sha256(CAPTURE.read_bytes()))
        rows = self.rows()
        rows[0]["linked_to"] = "invented:GEN.1.1"
        with self.assertRaises(JebError):
            validate_probe(self.payload(rows))

    def test_xml_dtd_entities_external_entities_and_excessive_nesting_rejected(self):
        cases = [
            '<!DOCTYPE p [<!ENTITY x "expanded">]><p>&x;</p>',
            '<!DOCTYPE p SYSTEM "https://example.invalid/test.dtd"><p/>',
            '<!ENTITY x SYSTEM "file:///private"><p/>',
            "<p>" * 14 + "text" + "</p>" * 14,
            "<p>broken",
        ]
        with patch("urllib.request.urlopen", side_effect=AssertionError("No network")):
            for value in cases:
                with self.subTest(value=value), self.assertRaises(ValueError):
                    xml_tree(value, fragment=False)


class ToolExecutionGateTests(WorkspaceTest):
    def test_wrong_source_or_changed_executable_denied_before_execution(self):
        lock = read_json(REPO / "toolchains/sword-1.9.0/windows-local.lock.json")
        tools = self.project.path("tools")
        tools.mkdir()
        for record in lock["executables"].values():
            (tools / record["filename"]).write_bytes(b"changed")
        with patch("subprocess.run", side_effect=AssertionError("Do not run changed tools")):
            with self.assertRaisesRegex(JebError, "Changed executable"):
                check_tool_lock(lock, tools)
        lock["source"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(JebError, "Unreviewed SWORD"):
            check_tool_lock(lock, tools)

    def test_evaluate_does_not_write_production_source_or_approval_data(self):
        # Mock only native execution, using the already captured real synthetic result.
        from types import SimpleNamespace

        programs = {
            name: Path(name) for name in ("imp2vs", "mod2imp", "mod2osis", "jeb-synthetic-probe")
        }
        stock_xml = (
            b'<osis xmlns="urn:test"><header><refSystem>Bible.KJV</refSystem></header></osis>'
        )

        def native(args, *, stdout, stderr, **kwargs):
            name = args[0]
            if name == "jeb-synthetic-probe":
                stdout.write(CAPTURE.read_bytes())
            elif name == "mod2osis":
                stdout.write(stock_xml)
            else:
                stdout.write(b"synthetic tool output")
            return SimpleNamespace(returncode=0)

        lockpath = self.project.path("test-tool-lock.json")
        lockpath.write_bytes((REPO / "toolchains/sword-1.9.0/windows-local.lock.json").read_bytes())
        before = self.books()
        with (
            patch("jeb.sword_diagnostic.check_tool_lock", return_value=programs),
            patch("subprocess.run", side_effect=native),
        ):
            result = evaluate(self.project, lockpath, self.project.root, "dist/evaluation")
        self.assertFalse(result["production_adapter_approved"])
        self.assertEqual(self.books(), before)
        self.assertFalse(self.project.path("data/approved").exists())
        self.assertEqual(list(self.project.path("data/raw").iterdir())[0].name, self.source_id)

    def test_bad_archive_fails_before_build_or_output_creation(self):
        from jeb.sword_build import build

        path = self.project.path("not-sword.tar.gz")
        path.write_bytes(b"not an audited software archive")
        with patch("subprocess.run", side_effect=AssertionError("Do not build")):
            with self.assertRaisesRegex(JebError, "reviewed SWORD"):
                build(self.project, path, "dist/no-build", "g++", "gcc", "cmake")
        self.assertFalse(self.project.path("dist/no-build").exists())
