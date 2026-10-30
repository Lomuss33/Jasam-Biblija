from __future__ import annotations

import copy
import unittest

from jeb.core import JebError, Project, file_id, json_loads, latin, read_json, read_yaml, write_json
from jeb.fetch import fetch
from jeb.sources import admitted, audit
from tests.support import REPO, WorkspaceTest


class StrictInputTests(unittest.TestCase):
    def test_json_duplicate_keys_rejected(self):
        with self.assertRaisesRegex(JebError, "Duplicate key"):
            json_loads('{"id": 1,"id": 2}')

    def test_nan_and_infinity_rejected(self):
        for number in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(number=number), self.assertRaises(JebError):
                json_loads(number)

    def test_latin_diacritics_and_literal_choices(self):
        latin("svjet vrjeme covik razumit čćđšž ČĆĐŠŽ")

    def test_non_latin_display_and_bidi_controls_rejected(self):
        for text in ("\u0418sus", "\u0399esous", "a\u202eb"):
            with self.subTest(text=text), self.assertRaises(JebError):
                latin(text)

    def test_unsafe_windows_and_path_ids_rejected(self):
        for value in ("../x", "a/b", "C:x", "CON", "nul.txt", "COM1", "id..x"):
            with self.subTest(value=value), self.assertRaises(JebError):
                file_id(value)

    def test_production_register_has_no_admitted_sources(self):
        result = audit(Project(REPO))
        self.assertEqual(result["admitted_count"], 0)
        self.assertEqual(result["sources"][2]["status"], "excluded")

    def test_excluded_source_never_downloaded(self):
        with self.assertRaisesRegex(JebError, "excluded"):
            fetch(Project(REPO), "ebible-hrv-saric")


class SourceGateTests(WorkspaceTest):
    def test_unknown_source(self):
        with self.assertRaisesRegex(JebError, "Unknown source"):
            admitted(self.project, "invented-source")

    def test_source_statuses_fail_closed(self):
        registry = read_yaml(self.project.path("sources/registry.yaml"))
        for status in ("candidate", "needs_review", "excluded", "unknown"):
            changed = copy.deepcopy(registry)
            changed["sources"][0]["status"] = status
            write_json(self.project.path("sources/registry.yaml"), changed)
            with self.subTest(status=status), self.assertRaises(JebError):
                admitted(self.project, self.source_id)

    def test_source_record_edit_invalidates_lock(self):
        data = read_yaml(self.project.path("sources/registry.yaml"))
        data["sources"][0]["title"] += " altered"
        write_json(self.project.path("sources/registry.yaml"), data)
        with self.assertRaisesRegex(JebError, "assessment changed"):
            admitted(self.project, self.source_id)

    def test_missing_jurisdiction_denied(self):
        self.project.edition["jurisdictions"].append("DE")
        with self.assertRaisesRegex(JebError, "rights for DE"):
            admitted(self.project, self.source_id)

    def test_synthetic_requires_explicit_opt_in(self):
        with self.assertRaisesRegex(JebError, "--synthetic"):
            Project(self.project.root)

    def test_synthetic_cannot_enter_historical_workspace(self):
        self.project.synthetic = False
        with self.assertRaisesRegex(JebError, "cannot be mixed"):
            admitted(self.project, self.source_id)

    def test_contextual_reference_cannot_be_admitted_as_corpus(self):
        data = read_yaml(self.project.path("sources/registry.yaml"))
        data["sources"][0]["kind"] = "contextual"
        write_json(self.project.path("sources/registry.yaml"), data)
        self.project.synthetic = False
        with self.assertRaisesRegex(JebError, "cannot be mixed"):
            admitted(self.project, self.source_id)

    def test_collection_cannot_expand_or_shrink(self):
        data = self.project.collection
        for books in ([*data["books"], "PSA"], data["books"][:-1], list(reversed(data["books"]))):
            write_json(self.project.path("config/collection.yaml"), {**data, "books": books})
            with self.subTest(books=books), self.assertRaises(JebError):
                Project(self.project.root, synthetic=True)

    def test_yaml_duplicate_keys_and_aliases(self):
        path = self.project.path("bad.yaml")
        for value in ("id: 1\nid: 2\n", "a: &x [one]\nb: *x\n"):
            path.write_text(value, encoding="utf-8")
            with self.subTest(value=value), self.assertRaises(JebError):
                read_yaml(path)

    def test_paths_cannot_escape_project(self):
        with self.assertRaisesRegex(JebError, "escapes"):
            self.project.path("../external.txt")

    def test_duplicate_or_overlapping_manifest_rejected(self):
        original = read_json(self.project.path("sources/lock.json"))
        for overlap in (False, True):
            data = copy.deepcopy(original)
            refs = data["sources"][0]["coverage"]["GEN"]
            if overlap:
                refs[1]["verse_labels"] = refs[0]["verse_labels"]
            else:
                refs[1] = refs[0]
            write_json(self.project.path("sources/lock.json"), data)
            with self.subTest(overlap=overlap), self.assertRaises(JebError):
                admitted(self.project, self.source_id)
