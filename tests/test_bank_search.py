import tempfile
import unittest
from pathlib import Path

from jeb.bank import search, storage
from jeb.core import JebError


class BankSearchTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "bank"
        storage.initialize(self.root, "Probna baza pretrage")
        storage.save_record(
            self.root,
            {
                "kind": "source",
                "title": "Aleksandar probni izvor",
                "data": {
                    "source_type": "document",
                    "creator": "Probni autor",
                    "translator": None,
                    "edition": "Probno izdanje",
                    "url": None,
                    "accessed_at": None,
                    "limitations": "Samo sintetički test.",
                },
                "visibility": "private",
                "processing_state": "inbox",
            },
            "test",
            "tool",
            "Dodaj probni izvor",
            "svjet vrjeme covik razumit",
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_search_returns_exact_current_revision_and_match_fields(self):
        result = search.search(self.root, "svjet")
        self.assertEqual(len(result["results"]), 1)
        self.assertIn("body", result["results"][0]["matches"])
        self.assertEqual(result["approvals_created"], 0)

    def test_search_is_casefolded_and_blank_is_rejected(self):
        self.assertEqual(len(search.search(self.root, "ALEKSANDAR")["results"]), 1)
        with self.assertRaises(JebError):
            search.search(self.root, " ")


if __name__ == "__main__":
    unittest.main()
