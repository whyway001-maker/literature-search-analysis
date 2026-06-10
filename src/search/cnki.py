"""CNKI (China National Knowledge Infrastructure) literature search module.

Supports:
- Basic keyword search
- Advanced search (multi-field combination)
- Journal search
- Result parsing and metadata extraction
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, field
from typing import Optional

from src.utils.exporter import Exporter


@dataclass
class PaperInfo:
    """Paper metadata container"""

    title: str = ""
    authors: list[str] = field(default_factory=list)
    journal: str = ""
    year: Optional[int] = None
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: str = ""
    keywords: list[str] = field(default_factory=list)
    abstract: str = ""
    doi: str = ""
    url: str = ""
    download_url: str = ""
    cited_count: int = 0
    source_db: str = "cnki"

    def to_dict(self) -> dict:
        return asdict(self)


class CNKISearcher:
    """CNKI search engine.

    Interacts with CNKI via browser automation (Playwright / Chrome DevTools Protocol).
    Depends on Codex skills: cnki-search, cnki-advanced-search, etc.
    """

    BASE_URL = "https://kns.cnki.net/kns8s/search"

    def __init__(self):
        self.results: list[PaperInfo] = []
        self.total_count: int = 0

    def search(
        self,
        keywords: str,
        limit: int = 20,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
    ) -> list[PaperInfo]:
        """Basic keyword search.

        Args:
            keywords: Search keywords (Chinese or English)
            limit: Max number of results
            year_from: Start year (optional)
            year_to: End year (optional)

        Returns:
            List of paper metadata

        Raises:
            ValueError: If keywords is empty
        """
        if not keywords.strip():
            raise ValueError("Search keywords cannot be empty")
        self._validate_search_options(limit, year_from, year_to)

        # Actual search performed by Codex cnki-search skill
        # Results are populated into self.results by the skill
        print(f"[CNKI] Searching: {keywords}, limit: {limit}")
        if year_from or year_to:
            print(f"[CNKI] Year filter: {year_from or 'any'} - {year_to or 'any'}")

        return self.results

    def advanced_search(
        self,
        title: Optional[str] = None,
        author: Optional[str] = None,
        journal: Optional[str] = None,
        keywords: Optional[str] = None,
        abstract: Optional[str] = None,
        limit: int = 20,
    ) -> list[PaperInfo]:
        """Advanced search with multi-field combination.

        Args:
            title: Paper title
            author: Author name
            journal: Journal name
            keywords: Keywords
            abstract: Abstract text
            limit: Max results

        Returns:
            List of paper metadata

        Raises:
            ValueError: If no search fields provided
        """
        if limit < 1:
            raise ValueError("limit must be at least 1")
        fields = {
            k: v for k, v in locals().items() if v and k not in ("self", "limit")
        }
        if not fields:
            raise ValueError("At least one search field is required")

        # Uses Codex cnki-advanced-search skill
        query_parts = [f"{k}={v}" for k, v in fields.items()]
        print(f"[CNKI Advanced] Query: {', '.join(query_parts)}, limit: {limit}")

        return self.results

    def search_journal(
        self,
        journal_name: str,
        year: Optional[int] = None,
        issue: Optional[str] = None,
    ) -> list[PaperInfo]:
        """Search within a specific journal.

        Args:
            journal_name: Journal name
            year: Publication year
            issue: Issue number

        Returns:
            Papers in the specified journal/issue
        """
        if not journal_name.strip():
            raise ValueError("journal_name cannot be empty")

        # Uses Codex cnki-journal-search, cnki-journal-toc
        print(f"[CNKI Journal] Journal: {journal_name}, year: {year}, issue: {issue}")
        return self.results

    def export_results(
        self,
        format: str = "json",
        filepath: Optional[str] = None,
    ) -> str:
        """Export search results.

        Args:
            format: Export format (json / csv / bibtex)
            filepath: Output file path (optional)

        Returns:
            Export content or file path
        """
        data = [r.to_dict() for r in self.results]
        exporter = Exporter()
        if filepath:
            return exporter.export(data, filepath, format=format)
        return exporter.render(data, format=format)

    @staticmethod
    def _to_bibtex(papers: list[dict]) -> str:
        """Convert results to BibTeX format."""
        return Exporter._to_bibtex(papers)

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
    parser = argparse.ArgumentParser(description="CNKI literature search")
    parser.add_argument("keywords", help="Search keywords")
    parser.add_argument("--limit", type=int, default=20, help="Max results")
    parser.add_argument("--year-from", type=int, help="Start year")
    parser.add_argument("--year-to", type=int, help="End year")
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
    searcher = CNKISearcher()
    searcher.search(
        keywords=args.keywords,
        limit=args.limit,
        year_from=args.year_from,
        year_to=args.year_to,
    )
    result = searcher.export_results(format=args.export, filepath=args.output)
    print(result)


if __name__ == "__main__":
    main()
