"""LitLab - Literature Auto Search, Download, and Analysis.

Supports CNKI and Google Scholar workflows for literature search, batch
download, metadata export, and lightweight analysis.
"""

__version__ = "0.1.0"
__author__ = "whyway001-maker"

__all__ = [
    "CNKISearcher",
    "GoogleScholarSearcher",
    "DownloadManager",
    "AnalysisPipeline",
]


def __getattr__(name: str):
    if name == "CNKISearcher":
        from src.search.cnki import CNKISearcher

        return CNKISearcher
    if name == "GoogleScholarSearcher":
        from src.search.google_scholar import GoogleScholarSearcher

        return GoogleScholarSearcher
    if name == "DownloadManager":
        from src.download.manager import DownloadManager

        return DownloadManager
    if name == "AnalysisPipeline":
        from src.analysis.pipeline import AnalysisPipeline

        return AnalysisPipeline
    raise AttributeError(f"module 'src' has no attribute {name!r}")
