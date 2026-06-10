"""Tests for the CNKI search module."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.search.cnki import CNKISearcher, PaperInfo


class CNKISearcherTests(unittest.TestCase):
    def test_paper_info_creation(self):
        paper = PaperInfo(
            title="Closed-Loop Supply Chain Coordination",
            authors=["Zhang San", "Li Si"],
            journal="Chinese Journal of Management Science",
            year=2024,
            keywords=["closed-loop supply chain", "coordination"],
        )

        data = paper.to_dict()

        self.assertEqual(data["title"], "Closed-Loop Supply Chain Coordination")
        self.assertEqual(len(data["authors"]), 2)
        self.assertEqual(data["source_db"], "cnki")

    def test_cnki_searcher_init(self):
        searcher = CNKISearcher()

        self.assertEqual(searcher.results, [])
        self.assertEqual(searcher.total_count, 0)

    def test_empty_keywords_raises(self):
        searcher = CNKISearcher()

        with self.assertRaises(ValueError):
            searcher.search("")

    def test_invalid_search_options_raise(self):
        searcher = CNKISearcher()

        with self.assertRaises(ValueError):
            searcher.search("logistics", limit=0)
        with self.assertRaises(ValueError):
            searcher.search("logistics", year_from=2025, year_to=2020)
        with self.assertRaises(ValueError):
            searcher.search_journal(" ")

    def test_export_empty_json(self):
        searcher = CNKISearcher()

        self.assertEqual(searcher.export_results(format="json"), "[]")


if __name__ == "__main__":
    unittest.main()
