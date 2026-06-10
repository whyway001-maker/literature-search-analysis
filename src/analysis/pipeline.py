"""Intelligent literature analysis pipeline.

Supports keyword extraction, author/year statistics, lightweight topic-cluster
placeholders, knowledge graph placeholders, and draft report generation.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Optional


class AnalysisPipeline:
    """Literature analysis pipeline."""

    def __init__(self, input_path: Optional[str] = None):
        self.input_path = Path(input_path) if input_path else None
        self.papers: list[dict] = []
        self.keywords_freq: Counter = Counter()
        self.author_freq: Counter = Counter()
        self.year_dist: dict = {}

    def load_data(self, filepath: str) -> None:
        """Load paper metadata from a JSON list file."""
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("Input metadata must be a JSON list of paper objects")
        self.papers = data
        print(f"[Analysis] Loaded {len(self.papers)} papers")

    def extract_keywords(self) -> Counter:
        """Extract high-frequency keywords."""
        self.keywords_freq = Counter()
        all_keywords = []
        for paper in self.papers:
            keywords = self._as_list(paper.get("keywords", []))
            all_keywords.extend(keywords)
        self.keywords_freq = Counter(all_keywords)
        return self.keywords_freq

    def author_analysis(self) -> Counter:
        """Analyze author publication frequency."""
        self.author_freq = Counter()
        for paper in self.papers:
            for author in self._as_list(paper.get("authors", [])):
                self.author_freq[author] += 1
        return self.author_freq

    def year_distribution(self) -> dict:
        """Analyze publication year distribution."""
        years = Counter()
        for paper in self.papers:
            year = paper.get("year")
            if not year:
                continue
            try:
                years[int(year)] += 1
            except (TypeError, ValueError):
                continue
        self.year_dist = dict(sorted(years.items()))
        return self.year_dist

    def cluster_topics(self, n_clusters: int = 5) -> list[dict]:
        """Return placeholder topic clusters."""
        if n_clusters < 1:
            raise ValueError("n_clusters must be at least 1")
        if not self.papers:
            return []

        print(f"[Analysis] Topic clustering, n_clusters={n_clusters}")
        return [{"topic_id": i, "keywords": [], "papers": []} for i in range(n_clusters)]

    def build_knowledge_graph(self) -> dict:
        """Build a knowledge graph skeleton from paper metadata."""
        nodes = []
        edges = []
        for i, paper in enumerate(self.papers):
            title = paper.get("title", f"Paper_{i}")
            nodes.append({"id": i, "label": title[:50], "year": paper.get("year")})
        print(f"[Analysis] Knowledge graph: {len(nodes)} nodes")
        return {"nodes": nodes, "edges": edges}

    def generate_summary(self, max_papers: int = 50) -> str:
        """Generate a draft literature review in Markdown."""
        self.extract_keywords()
        self.year_distribution()

        top_papers = self.papers[:max_papers]
        start_year = min(self.year_dist.keys(), default="N/A")
        end_year = max(self.year_dist.keys(), default="N/A")
        keywords = ", ".join(
            f"{kw}({cnt})" for kw, cnt in self.keywords_freq.most_common(10)
        ) or "N/A"

        summary = "# Literature Review (Auto-Generated)\n\n"
        summary += "## Overview\n\n"
        summary += f"- Papers included: {len(top_papers)}\n"
        summary += f"- Time span: {start_year} - {end_year}\n"
        summary += f"- Top keywords: {keywords}\n\n"
        summary += "## Key Research Directions\n\n"
        summary += "_(Auto-generated based on topic clustering)_\n\n"
        return summary

    def export_report(self, output_path: str, format: str = "md") -> str:
        """Export an analysis report."""
        format = format.lower()
        if format not in {"md", "json"}:
            raise ValueError("format must be 'md' or 'json'")

        if format == "md":
            report = self.generate_summary()
        else:
            self.extract_keywords()
            self.author_analysis()
            self.year_distribution()
            report = json.dumps(
                {
                    "keyword_freq": dict(self.keywords_freq.most_common(30)),
                    "author_freq": dict(self.author_freq.most_common(30)),
                    "year_distribution": self.year_dist,
                    "paper_count": len(self.papers),
                },
                ensure_ascii=False,
                indent=2,
            )

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"[Analysis] Report exported: {output_path}")
        return output_path

    @staticmethod
    def _as_list(value) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            return [item.strip() for item in re.split(r"[,;]", value) if item.strip()]
        if isinstance(value, (list, tuple, set)):
            return [str(item).strip() for item in value if str(item).strip()]
        return [str(value).strip()] if str(value).strip() else []


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze paper metadata")
    parser.add_argument("--input", required=True, help="Input JSON metadata file")
    parser.add_argument("--output", required=True, help="Output report path")
    parser.add_argument(
        "--format", choices=["md", "json"], default="md", help="Output format"
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    pipeline = AnalysisPipeline()
    pipeline.load_data(args.input)
    pipeline.export_report(args.output, format=args.format)


if __name__ == "__main__":
    main()
