"""
Google Scholar literature search module.

Supports:
- Basic keyword search
- Advanced search (year / author / journal filters)
- Citation tracking
- Result parsing and metadata extraction
"""

from dataclasses import dataclass, field, asdict
from typing import Optional
from urllib.parse import quote_plus
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

        # Uses Codex gs-search skill
        encoded = quote_plus(keywords)
        url = f"{self.BASE_URL}?q={encoded}&hl=en&num={min(limit, 100)}"
        if sort_by == "date":
            url += "&scisbd=1"
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
        # Uses Codex gs-advanced-search skill
        query_params = []
        if keywords:
            query_params.append(quote_plus(keywords))
        if author:
            query_params.append(f"author:{author}")
        if journal:
            query_params.append(f"source:{journal}")
        if title_phrase:
            query_params.append(f'"{title_phrase}"')

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
        # Uses Codex gs-cited-by skill
        print(f"[GS Cited] Tracking citations for: {paper_url[:60]}..., limit: {limit}")
        return []
