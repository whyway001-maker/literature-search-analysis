"""
CNKI (China National Knowledge Infrastructure) literature search module.

Supports:
- Basic keyword search
- Advanced search (multi-field combination)
- Journal search
- Result parsing and metadata extraction
"""

import json
import re
from dataclasses import dataclass, field, asdict
from typing import Optional
from datetime import datetime


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
        output = ""

        if format == "json":
            output = json.dumps(data, ensure_ascii=False, indent=2)
        elif format == "csv":
            import csv, io

            buf = io.StringIO()
            writer = csv.DictWriter(buf, fieldnames=data[0].keys() if data else [])
            writer.writeheader()
            writer.writerows(data)
            output = buf.getvalue()
        elif format == "bibtex":
            output = self._to_bibtex(data)

        if filepath:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(output)
            return filepath
        return output

    @staticmethod
    def _to_bibtex(papers: list[dict]) -> str:
        """Convert results to BibTeX format."""
        entries = []
        for i, p in enumerate(papers):
            key = f"ref{i+1}"
            entry = "@article{" + key + ",\n"
            entry += f"  title = {{{p.get('title', '')}}},\n"
            entry += f"  author = {{{' and '.join(p.get('authors', []))}}},\n"
            entry += f"  journal = {{{p.get('journal', '')}}},\n"
            if p.get("year"):
                entry += f"  year = {{{p['year']}}},\n"
            if p.get("doi"):
                entry += f"  doi = {{{p['doi']}}},\n"
            entry += "}\n"
            entries.append(entry)
        return "\n".join(entries)
