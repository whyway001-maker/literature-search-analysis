"""
文献自动检索下载分析 - 主入口

支持 CNKI（中国知网）和 Google Scholar 的：
- 文献检索
- 批量下载
- 元数据导出
- AI 分析

Usage:
    python -m src.search.cnki "关键词"
    python -m src.download.manager --source cnki --keywords "关键词"
    python -m src.analysis.pipeline --input results.json
"""

__version__ = "0.1.0"
__author__ = "whyway001-maker"

from src.search.cnki import CNKISearcher
from src.search.google_scholar import GoogleScholarSearcher
from src.download.manager import DownloadManager
from src.analysis.pipeline import AnalysisPipeline

__all__ = [
    "CNKISearcher",
    "GoogleScholarSearcher",
    "DownloadManager",
    "AnalysisPipeline",
]
