"""
Google Scholar 文献检索模块

支持：
- 基础关键词检索
- 高级检索（年份/作者/期刊过滤）
- 引用追踪
- 结果解析与元数据提取
"""

from dataclasses import dataclass, field, asdict
from typing import Optional
from urllib.parse import quote_plus
from .cnki import PaperInfo  # 复用 PaperInfo 数据类


class GoogleScholarSearcher:
    """Google Scholar 检索引擎

    通过浏览器自动化与 Google Scholar 交互。
    依赖 Codex skill: gs-search, gs-advanced-search 等。
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
        """基础关键词检索

        Args:
            keywords: 检索关键词（英文为主）
            limit: 返回结果数量上限
            year_from: 起始年份
            year_to: 结束年份
            sort_by: 排序方式 (relevance/date)

        Returns:
            论文信息列表
        """
        if not keywords.strip():
            raise ValueError("检索关键词不能为空")

        # TODO: 集成 Codex gs-search skill
        encoded = quote_plus(keywords)
        url = f"{self.BASE_URL}?q={encoded}&hl=en&num={min(limit, 100)}"
        if sort_by == "date":
            url += "&scisbd=1"
        print(f"[GS] 检索 URL: {url}")
        print(f"[GS] 关键词: {keywords}, 排序: {sort_by}")

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
        """高级检索

        Args:
            keywords: 关键词（所有词）
            author: 作者
            journal: 发表期刊
            title_phrase: 标题精确短语
            year_from: 起始年份
            year_to: 结束年份
            limit: 结果数量

        Returns:
            论文信息列表
        """
        # TODO: 集成 Codex gs-advanced-search skill
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
        """获取引用某论文的文献列表

        Args:
            paper_url: 目标论文的 Google Scholar URL
            limit: 结果数量

        Returns:
            引用该论文的文献列表
        """
        # TODO: 集成 Codex gs-cited-by skill
        print(f"[GS Cited] 追踪引用: {paper_url[:60]}..., 限制: {limit}")
        return []
