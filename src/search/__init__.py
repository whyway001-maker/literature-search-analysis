"""检索模块初始化"""
from .cnki import CNKISearcher, PaperInfo
from .google_scholar import GoogleScholarSearcher

__all__ = ["CNKISearcher", "GoogleScholarSearcher", "PaperInfo"]
