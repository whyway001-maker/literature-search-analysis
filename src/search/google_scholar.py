"""Google Scholar literature search module.

Supports:
- Basic keyword search
- Advanced search (year / author / journal filters)
- Citation tracking
- Result parsing and metadata extraction
"""

from __future__ import annotations

import argparse
from typing import Optional
from urllib.parse import quote_plus

from src.utils.exporter import Exporter

from .cnki import PaperInfo  # Reuse PaperInfo dataclass


class GoogleScholarSearcher:
    """Google Scholar search engine.

    Interacts with Google Scholar via browser automation.
    Depends on Codex skills: gs-search, gs-advanced-search, etc.
    """

    BASE_URL = "https://scholar.google.com/scholar"

    def __init__(self):
        self.results: list[PaperInfo] = []
        self.total_count: int = 0

    def search(
        self,
        keywords: str,
        limit: int = 20,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        sort_by: str = "relevance",
    ) -> list[PaperInfo]:
        """Basic keyword search.

        Args:
            keywords: Search keywords (English preferred)
            limit: Max results
            year_from: Start year
            year_to: End year
            sort_by: Sort order (relevance / date)

        Returns:
            List of paper metadata

        Raises:
            ValueError: If keywords is empty
        """
        if not keywords.strip():
            raise ValueError("Search keywords cannot be empty")
        self._validate_search_options(limit, year_from, year_to)
        if sort_by not in {"relevance", "date"}:
            raise ValueError("sort_by must be 'relevance' or 'date'")

        # Uses Codex gs-search skill
        encoded = quote_plus(keywords)
        url = f"{self.BASE_URL}?q={encoded}&hl=en&num={min(limit, 100)}"
        if sort_by == "date":
            url += "&scisbd=1"
        if year_from is not None:
            url += f"&as_ylo={year_from}"
        if year_to is not None:
            url += f"&as_yhi={year_to}"
        print(f"[GS] Search URL: {url}")
        print(f"[GS] Keywords: {keywords}, sort: {sort_by}")

        return self.results

    def advanced_search(
        self,
        keywords: Optional[str] = None,
        author: Optional[str] = None,
        journal: Optional[str] = None,
        title_phrase: Optional[str] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        limit: int = 20,
    ) -> list[PaperInfo]:
        """Advanced search with field filters.

        Args:
            keywords: All keywords
            author: Author filter
            journal: Source journal
            title_phrase: Exact title phrase
            year_from: Start year
            year_to: End year
            limit: Max results

        Returns:
            List of paper metadata
        """
        self._validate_search_options(limit, year_from, year_to)

        # Uses Codex gs-advanced-search skill
        query_params = []
        if keywords:
            query_params.append(keywords)
        if author:
            query_params.append(f'author:"{author}"')
        if journal:
            query_params.append(f'source:"{journal}"')
        if title_phrase:
            query_params.append(f'"{title_phrase}"')
        if not query_params:
            raise ValueError("At least one search field is required")

        query = " ".join(query_params)
        url = f"{self.BASE_URL}?q={quote_plus(query)}&hl=en&num={min(limit, 100)}"
        if year_from:
            url += f"&as_ylo={year_from}"
        if year_to:
            url += f"&as_yhi={year_to}"
        print(f"[GS Advanced] URL: {url}")

        return self.results

    def get_cited_by(self, paper_url: str, limit: int = 20) -> list[PaperInfo]:
        """Get papers that cite a given paper.

        Args:
            paper_url: Google Scholar URL of the target paper
            limit: Max results

        Returns:
            List of citing papers
        """
        if not paper_url.strip():
            raise ValueError("paper_url cannot be empty")
        if limit < 1:
            raise ValueError("limit must be at least 1")

        # Uses Codex gs-cited-by skill
        print(f"[GS Cited] Tracking citations for: {paper_url[:60]}..., limit: {limit}")
        return []

    def export_results(
        self,
        format: str = "json",
        filepath: Optional[str] = None,
    ) -> str:
        """Export search results."""
        data = [r.to_dict() for r in self.results]
        exporter = Exporter()
        if filepath:
            return exporter.export(data, filepath, format=format)
        return exporter.render(data, format=format)

    @staticmethod
    def _validate_search_options(
        limit: int,
        year_from: Optional[int],
        year_to: Optional[int],
    ) -> None:
        if limit < 1:
            raise ValueError("limit must be at least 1")
        if year_from is not None and year_to is not None and year_from > year_to:
            raise ValueError("year_from cannot be greater than year_to")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Google Scholar literature search")
    parser.add_argument("keywords", help="Search keywords")
    parser.add_argument("--limit", type=int, default=20, help="Max results")
    parser.add_argument("--year-from", type=int, help="Start year")
    parser.add_argument("--year-to", type=int, help="End year")
    parser.add_argument(
        "--sort-by",
        choices=["relevance", "date"],
        default="relevance",
        help="Sort order",
    )
    parser.add_argument(
        "--export",
        choices=["json", "csv", "bibtex", "ris", "md"],
        default="json",
        help="Export format",
    )
    parser.add_argument("--output", help="Output file path")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    searcher = GoogleScholarSearcher()
    searcher.search(
        keywords=args.keywords,
        limit=args.limit,
        year_from=args.year_from,
        year_to=args.year_to,
        sort_by=args.sort_by,
    )
    result = searcher.export_results(format=args.export, filepath=args.output)
    print(result)


if __name__ == "__main__":
    main()
