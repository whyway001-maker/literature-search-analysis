"""
数据导出工具

支持格式：
- BibTeX (.bib)
- CSV (.csv)
- JSON (.json)
- RIS (.ris)
- Markdown 表格 (.md)
"""

import json
import csv
from pathlib import Path
from typing import Optional


class Exporter:
    """文献元数据导出器"""

    FORMATS = ["json", "csv", "bibtex", "ris", "md"]

    def __init__(self):
        pass

    def export(
        self,
        papers: list[dict],
        output_path: str,
        format: str = "json",
    ) -> str:
        """导出文献元数据

        Args:
            papers: 文献数据列表
            output_path: 输出文件路径
            format: 导出格式

        Returns:
            输出文件路径
        """
        if format not in self.FORMATS:
            raise ValueError(f"不支持的格式: {format}，支持: {self.FORMATS}")

        exporter = {
            "json": self._to_json,
            "csv": self._to_csv,
            "bibtex": self._to_bibtex,
            "md": self._to_markdown,
        }.get(format)

        content = exporter(papers)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[Export] {len(papers)} 条记录 -> {output_path} ({format})")
        return output_path

    def _to_json(self, papers: list[dict]) -> str:
        return json.dumps(papers, ensure_ascii=False, indent=2)

    def _to_csv(self, papers: list[dict]) -> str:
        if not papers:
            return ""
        import io
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=papers[0].keys())
        writer.writeheader()
        writer.writerows(papers)
        return buf.getvalue()

    def _to_bibtex(self, papers: list[dict]) -> str:
        entries = []
        for i, p in enumerate(papers):
            key = f"ref{i+1}"
            entry = f"@article{{{key},\n"
            entry += f"  title = {{{p.get('title', '')}}},\n"
            authors = ' and '.join(p.get('authors', []))
            entry += f"  author = {{{authors}}},\n"
            entry += f"  journal = {{{p.get('journal', '')}}},\n"
            if p.get('year'):
                entry += f"  year = {{{p['year']}}},\n"
            if p.get('doi'):
                entry += f"  doi = {{{p['doi']}}},\n"
            entry += "}\n"
            entries.append(entry)
        return "\n".join(entries)

    def _to_markdown(self, papers: list[dict]) -> str:
        if not papers:
            return ""
        headers = list(papers[0].keys())
        lines = ["| " + " | ".join(headers) + " |"]
        lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
        for p in papers:
            row = [str(p.get(h, "")).replace("|", "\\|") for h in headers]
            lines.append("| " + " | ".join(row) + " |")
        return "\n".join(lines)
