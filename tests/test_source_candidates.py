from __future__ import annotations

import copy
import shutil
import tempfile
import unittest
from pathlib import Path

from jeb.core import JebError, Project, read_json, write_json
from jeb.source_candidates import import_batch, validate
from tests.support import REPO


class SourceCandidateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "config").mkdir()
        shutil.copyfile(REPO / "config/edition.yaml", self.root / "config/edition.yaml")
        shutil.copyfile(REPO / "config/collection.yaml", self.root / "config/collection.yaml")
        self.project = Project(self.root)

    def batch(self):
        return {
            "schema_version": "1.0",
            "batch_id": "alexander-search",
            "query": "Alexander the Great Illyrian perspective",
            "jurisdictions": ["DE", "HR"],
            "captured_at": "2026-11-18",
            "candidates": [
                {
                    "candidate_id": "lead-1",
                    "url": "https://example.invalid/catalogue",
                    "title": "Synthetic catalogue result",
                    "provider": "Synthetic search fixture",
                    "access_date": "2026-11-18",
                    "rights_state": "unknown",
                    "rights_basis": "No legal assessment performed.",
                    "notes": "Metadata only; no page or payload copied.",
                    "content_acquired": False,
                }
            ],
        }

    def test_validation_is_metadata_only(self):
        path = self.root / "candidates.json"
        write_json(path, self.batch())
        self.assertEqual(validate(path)["candidates"][0]["rights_state"], "unknown")
        result = import_batch(self.project, path)
        self.assertFalse(result["corpus_permission"])
        self.assertFalse(result["source_clearance_changed"])
        stored = self.root / result["output"]
        self.assertEqual(read_json(stored), self.batch())

    def test_rejects_acquisition_and_unsafe_urls(self):
        value = self.batch()
        value["candidates"][0]["content_acquired"] = True
        path = self.root / "bad.json"
        write_json(path, value)
        with self.assertRaises(JebError):
            validate(path)
        value = copy.deepcopy(self.batch())
        value["candidates"][0]["url"] = "http://example.invalid/catalogue"
        write_json(path, value)
        with self.assertRaises(JebError):
            validate(path)


if __name__ == "__main__":
    unittest.main()
