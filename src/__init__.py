"""
LitLab — Literature Auto Search, Download & Analysis

Supports CNKI and Google Scholar for:
- Literature search
- Batch download
- Metadata export
- AI-driven analysis

Usage:
    python -m src.search.cnki "keywords"
    python -m src.download.manager --source cnki --keywords "keywords"
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
