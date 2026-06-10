"""
Data export utility.

Supported formats:
- BibTeX (.bib)
- CSV (.csv)
- JSON (.json)
- RIS (.ris)
- Markdown table (.md)
"""

from __future__ import annotations

import json
import csv
from pathlib import Path


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
        content = self.render(papers, format=format)
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(content)
        print(f"[Export] {len(papers)} records -> {output_path} ({format})")
        return output_path

    def render(self, papers: list[dict], format: str = "json") -> str:
        """Render paper metadata without writing it to disk."""
        format = format.lower()
        if format not in self.FORMATS:
            raise ValueError(f"Unsupported format: {format}. Supported: {self.FORMATS}")

        exporter = {
            "json": self._to_json,
            "csv": self._to_csv,
            "bibtex": self._to_bibtex,
            "ris": self._to_ris,
            "md": self._to_markdown,
        }.get(format)
        return exporter(papers)

    @staticmethod
    def _to_json(papers: list[dict]) -> str:
        return json.dumps(papers, ensure_ascii=False, indent=2)

    @staticmethod
    def _to_csv(papers: list[dict]) -> str:
        if not papers:
            return ""
        import io

        buf = io.StringIO()
        fieldnames = Exporter._fieldnames(papers)
        writer = csv.DictWriter(buf, fieldnames=fieldnames, extrasaction="ignore")
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
    def _to_ris(papers: list[dict]) -> str:
        entries = []
        for p in papers:
            lines = ["TY  - JOUR"]
            if p.get("title"):
                lines.append(f"TI  - {p['title']}")
            for author in p.get("authors", []):
                lines.append(f"AU  - {author}")
            if p.get("journal"):
                lines.append(f"JO  - {p['journal']}")
            if p.get("year"):
                lines.append(f"PY  - {p['year']}")
            if p.get("doi"):
                lines.append(f"DO  - {p['doi']}")
            if p.get("url"):
                lines.append(f"UR  - {p['url']}")
            for keyword in p.get("keywords", []):
                lines.append(f"KW  - {keyword}")
            if p.get("abstract"):
                lines.append(f"AB  - {p['abstract']}")
            lines.append("ER  -")
            entries.append("\n".join(lines))
        return "\n\n".join(entries)

    @staticmethod
    def _to_markdown(papers: list[dict]) -> str:
        if not papers:
            return ""
        headers = Exporter._fieldnames(papers)
        lines = ["| " + " | ".join(headers) + " |"]
        lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
        for p in papers:
            row = [str(p.get(h, "")).replace("|", "\\|") for h in headers]
            lines.append("| " + " | ".join(row) + " |")
        return "\n".join(lines)

    @staticmethod
    def _fieldnames(papers: list[dict]) -> list[str]:
        names: list[str] = []
        for paper in papers:
            for key in paper.keys():
                if key not in names:
                    names.append(key)
        return names
