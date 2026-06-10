"""Tests for exporter, downloader, analysis, and search helpers."""

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.analysis.pipeline import AnalysisPipeline
from src.download.manager import DownloadManager
from src.search.google_scholar import GoogleScholarSearcher
from src.utils.exporter import Exporter


class ExporterTests(unittest.TestCase):
    def test_supports_ris(self):
        papers = [
            {
                "title": "Battery recycling review",
                "authors": ["Alice Zhang", "Bob Li"],
                "journal": "Journal of Logistics",
                "year": 2024,
                "doi": "10.1234/example",
                "keywords": ["recycling", "logistics"],
            }
        ]

        ris = Exporter().render(papers, format="ris")

        self.assertIn("TY  - JOUR", ris)
        self.assertIn("TI  - Battery recycling review", ris)
        self.assertIn("AU  - Alice Zhang", ris)
        self.assertIn("KW  - logistics", ris)
        self.assertTrue(ris.endswith("ER  -"))

    def test_csv_uses_union_fieldnames(self):
        papers = [{"title": "A"}, {"title": "B", "doi": "10.1/example"}]

        csv_text = Exporter().render(papers, format="csv")

        self.assertEqual(csv_text.splitlines()[0], "title,doi")
        self.assertIn("10.1/example", csv_text)


class DownloadManagerTests(unittest.TestCase):
    def test_sanitizes_filenames(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            manager = DownloadManager(download_dir=temp_dir)

            path = manager.download(
                "https://example.com/paper.pdf", filename="../bad:title?.pdf"
            )

            self.assertEqual(path, str(Path(temp_dir) / "bad_title_.pdf"))


class AnalysisPipelineTests(unittest.TestCase):
    def test_handles_string_metadata(self):
        papers = [
            {
                "title": "A",
                "authors": "Alice; Bob",
                "keywords": "battery, recycling",
                "year": "2024",
            },
            {
                "title": "B",
                "authors": ["Alice"],
                "keywords": ["battery"],
                "year": "bad",
            },
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "report.json"
            pipeline = AnalysisPipeline()
            pipeline.papers = papers
            pipeline.export_report(str(output), format="json")
            report = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(report["paper_count"], 2)
        self.assertEqual(report["keyword_freq"]["battery"], 2)
        self.assertEqual(report["author_freq"]["Alice"], 2)
        self.assertEqual(report["year_distribution"], {"2024": 1})


class GoogleScholarSearcherTests(unittest.TestCase):
    def test_export_and_advanced_search(self):
        searcher = GoogleScholarSearcher()

        self.assertEqual(searcher.export_results(format="json"), "[]")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            searcher.advanced_search(
                keywords="reverse logistics", author="Smith", limit=5
            )

        output = stdout.getvalue()
        self.assertNotIn("reverse%2Blogistics", output)
        self.assertIn("reverse+logistics", output)

    def test_search_applies_year_filters(self):
        searcher = GoogleScholarSearcher()
        stdout = io.StringIO()

        with contextlib.redirect_stdout(stdout):
            searcher.search(
                "reverse logistics",
                year_from=2020,
                year_to=2025,
            )

        output = stdout.getvalue()
        self.assertIn("as_ylo=2020", output)
        self.assertIn("as_yhi=2025", output)

    def test_invalid_search_options_raise(self):
        searcher = GoogleScholarSearcher()

        with self.assertRaises(ValueError):
            searcher.search("logistics", limit=0)
        with self.assertRaises(ValueError):
            searcher.search("logistics", year_from=2025, year_to=2020)
        with self.assertRaises(ValueError):
            searcher.get_cited_by("")


if __name__ == "__main__":
    unittest.main()
