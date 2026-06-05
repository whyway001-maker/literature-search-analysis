"""
Data export utility.

Supported formats:
- BibTeX (.bib)
- CSV (.csv)
- JSON (.json)
- RIS (.ris)
- Markdown table (.md)
"""

import json
import csv
from pathlib import Path
from typing import Optional


class Exporter:
    """Paper metadata exporter."""

    FORMATS = ["json", "csv", "bibtex", "ris", "md"]

    def __init__(self):
        pass

    def export(
        self,
        papers: list[dict],
        output_path: str,
        format: str = "json",
    ) -> str:
        """Export paper metadata.

        Args:
            papers: Paper data list
            output_path: Output file path
            format: Export format (json / csv / bibtex / md)

        Returns:
            Output file path

        Raises:
            ValueError: If format is unsupported
        """
        if format not in self.FORMATS:
            raise ValueError(f"Unsupported format: {format}. Supported: {self.FORMATS}")

        exporter = {
            "json": self._to_json,
            "csv": self._to_csv,
            "bibtex": self._to_bibtex,
            "md": self._to_markdown,
        }.get(format)

        content = exporter(papers)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[Export] {len(papers)} records -> {output_path} ({format})")
        return output_path

    @staticmethod
    def _to_json(papers: list[dict]) -> str:
        return json.dumps(papers, ensure_ascii=False, indent=2)

    @staticmethod
    def _to_csv(papers: list[dict]) -> str:
        if not papers:
            return ""
        import io

        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=papers[0].keys())
        writer.writeheader()
        writer.writerows(papers)
        return buf.getvalue()

    @staticmethod
    def _to_bibtex(papers: list[dict]) -> str:
        entries = []
        for i, p in enumerate(papers):
            key = f"ref{i+1}"
            entry = f"@article{{{key},\n"
            entry += f"  title = {{{p.get('title', '')}}},\n"
            authors = " and ".join(p.get("authors", []))
            entry += f"  author = {{{authors}}},\n"
            entry += f"  journal = {{{p.get('journal', '')}}},\n"
            if p.get("year"):
                entry += f"  year = {{{p['year']}}},\n"
            if p.get("doi"):
                entry += f"  doi = {{{p['doi']}}},\n"
            entry += "}\n"
            entries.append(entry)
        return "\n".join(entries)

    @staticmethod
    def _to_markdown(papers: list[dict]) -> str:
        if not papers:
            return ""
        headers = list(papers[0].keys())
        lines = ["| " + " | ".join(headers) + " |"]
        lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
        for p in papers:
            row = [str(p.get(h, "")).replace("|", "\\|") for h in headers]
            lines.append("| " + " | ".join(row) + " |")
        return "\n".join(lines)
