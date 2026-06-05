"""
文献智能分析流水线

支持：
- 关键词提取与主题聚类
- 文献共引/共词分析
- 知识图谱构建
- 自动化综述生成
- 热点趋势分析
"""

import json
from pathlib import Path
from typing import Optional
from collections import Counter


class AnalysisPipeline:
    """文献分析流水线

    对检索下载后的文献数据进行智能分析，
    输出可视化图表、统计报告和综述草稿。
    """

    def __init__(self, input_path: Optional[str] = None):
        self.input_path = Path(input_path) if input_path else None
        self.papers: list[dict] = []
        self.keywords_freq: Counter = Counter()
        self.author_freq: Counter = Counter()
        self.year_dist: dict = {}

    def load_data(self, filepath: str) -> None:
        """加载文献数据

        Args:
            filepath: JSON 格式的文献元数据文件
        """
        with open(filepath, "r", encoding="utf-8") as f:
            self.papers = json.load(f)
        print(f"[Analysis] 加载 {len(self.papers)} 篇文献")

    def extract_keywords(self) -> Counter:
        """提取高频关键词"""
        all_keywords = []
        for paper in self.papers:
            kws = paper.get("keywords", [])
            all_keywords.extend(kws)
        self.keywords_freq = Counter(all_keywords)
        return self.keywords_freq

    def author_analysis(self) -> Counter:
        """作者发文频次分析"""
        for paper in self.papers:
            authors = paper.get("authors", [])
            for author in authors:
                self.author_freq[author] += 1
        return self.author_freq

    def year_distribution(self) -> dict:
        """年份分布分析"""
        years = Counter()
        for paper in self.papers:
            year = paper.get("year")
            if year:
                years[year] += 1
        self.year_dist = dict(sorted(years.items()))
        return self.year_dist

    def cluster_topics(self, n_clusters: int = 5) -> list[dict]:
        """主题聚类分析

        Args:
            n_clusters: 聚类数量

        Returns:
            聚类结果列表
        """
        # TODO: 集成 scikit-learn TF-IDF + KMeans 聚类
        print(f"[Analysis] 主题聚类, n_clusters={n_clusters}")
        return [{"topic_id": i, "keywords": [], "papers": []} for i in range(n_clusters)]

    def build_knowledge_graph(self) -> dict:
        """构建知识图谱

        Returns:
            图谱节点与边数据（可用于 NetworkX 可视化）
        """
        # TODO: 基于共引/共词关系构建图谱
        nodes = []
        edges = []
        for i, paper in enumerate(self.papers):
            title = paper.get("title", f"Paper_{i}")
            nodes.append({"id": i, "label": title[:50], "year": paper.get("year")})
        print(f"[Analysis] 知识图谱: {len(nodes)} 节点")
        return {"nodes": nodes, "edges": edges}

    def generate_summary(
        self,
        max_papers: int = 50,
    ) -> str:
        """生成文献综述草稿

        Args:
            max_papers: 纳入分析的文献数量上限

        Returns:
            综述文本（Markdown 格式）
        """
        self.extract_keywords()
        self.year_distribution()

        top_papers = self.papers[:max_papers]

        summary = f"# 文献综述（自动生成）\n\n"
        summary += f"## 概览\n\n"
        summary += f"- 纳入文献：{len(top_papers)} 篇\n"
        summary += f"- 时间跨度：{min(self.year_dist.keys(), default='N/A')}"
        summary += f" - {max(self.year_dist.keys(), default='N/A')}\n"
        summary += f"- 高频关键词："
        summary += ", ".join(
            f"{kw}({cnt})" for kw, cnt in self.keywords_freq.most_common(10)
        )
        summary += f"\n\n## 主要研究方向\n\n"
        summary += "_（基于主题聚类自动生成）_\n\n"

        return summary

    def export_report(self, output_path: str, format: str = "md") -> str:
        """导出分析报告

        Args:
            output_path: 输出路径
            format: 输出格式 (md/json)

        Returns:
            输出文件路径
        """
        if format == "md":
            report = self.generate_summary()
        else:
            report = json.dumps({
                "keyword_freq": dict(self.keywords_freq.most_common(30)),
                "year_distribution": self.year_dist,
                "paper_count": len(self.papers),
            }, ensure_ascii=False, indent=2)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"[Analysis] 报告已导出: {output_path}")
        return output_path
