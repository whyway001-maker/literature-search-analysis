"""Search module"""
from .cnki import CNKISearcher, PaperInfo
from .google_scholar import GoogleScholarSearcher

__all__ = ["CNKISearcher", "GoogleScholarSearcher", "PaperInfo"]
