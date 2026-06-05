"""
CNKI（中国知网）文献检索模块

支持：
- 基础关键词检索
- 高级检索（多字段组合）
- 期刊检索
- 结果解析与元数据提取
"""

import json
import re
from dataclasses import dataclass, field, asdict
from typing import Optional
from datetime import datetime


@dataclass
class PaperInfo:
    """论文元数据"""
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
    """CNKI 检索引擎

    通过浏览器自动化（Playwright / Chrome DevTools Protocol）与 CNKI 交互。
    依赖 Codex skill: cnki-search, cnki-advanced-search 等提供底层浏览器操作。
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
        """基础关键词检索

        Args:
            keywords: 检索关键词（中英文均可）
            limit: 返回结果数量上限
            year_from: 起始年份（可选）
            year_to: 结束年份（可选）

        Returns:
            论文信息列表
        """
        # 实际检索逻辑由 Codex cnki-search skill 执行
        # 此处为本地数据结构与参数验证
        if not keywords.strip():
            raise ValueError("检索关键词不能为空")

        # TODO: 集成 Codex skill 调用
        # 结果由 skill 返回后填充到 self.results
        print(f"[CNKI] 检索关键词: {keywords}, 限制: {limit}")
        if year_from or year_to:
            print(f"[CNKI] 年份筛选: {year_from or '不限'} - {year_to or '不限'}")

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
        """高级检索（多字段组合）

        Args:
            title: 题名
            author: 作者
            journal: 刊名
            keywords: 关键词
            abstract: 摘要
            limit: 结果数量

        Returns:
            论文信息列表
        """
        fields = {k: v for k, v in locals().items()
                  if v and k not in ('self', 'limit')}
        if not fields:
            raise ValueError("至少填写一个检索字段")

        # TODO: 集成 Codex cnki-advanced-search skill
        query_parts = [f"{k}={v}" for k, v in fields.items()]
        print(f"[CNKI Advanced] 检索条件: {', '.join(query_parts)}, 限制: {limit}")

        return self.results

    def search_journal(
        self,
        journal_name: str,
        year: Optional[int] = None,
        issue: Optional[str] = None,
    ) -> list[PaperInfo]:
        """期刊目录检索

        Args:
            journal_name: 期刊名称
            year: 年份
            issue: 期号

        Returns:
            该期刊指定期数的论文列表
        """
        # TODO: 集成 Codex cnki-journal-search, cnki-journal-toc
        print(f"[CNKI Journal] 期刊: {journal_name}, 年份: {year}, 期号: {issue}")
        return self.results

    def export_results(
        self,
        format: str = "json",
        filepath: Optional[str] = None,
    ) -> str:
        """导出检索结果

        Args:
            format: 导出格式 (json/csv/bibtex)
            filepath: 保存路径（可选）

        Returns:
            导出内容或文件路径
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
        """转换为 BibTeX 格式"""
        entries = []
        for i, p in enumerate(papers):
            key = f"ref{i+1}"
            entry = "@article{" + key + ",\n"
            entry += f"  title = {{{p.get('title', '')}}},\n"
            entry += f"  author = {{{' and '.join(p.get('authors', []))}}},\n"
            entry += f"  journal = {{{p.get('journal', '')}}},\n"
            if p.get('year'):
                entry += f"  year = {{{p['year']}}},\n"
            if p.get('doi'):
                entry += f"  doi = {{{p['doi']}}},\n"
            entry += "}\n"
            entries.append(entry)
        return "\n".join(entries)
