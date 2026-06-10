"""Search module."""

__all__ = ["CNKISearcher", "GoogleScholarSearcher", "PaperInfo"]


def __getattr__(name: str):
    if name in {"CNKISearcher", "PaperInfo"}:
        from src.search.cnki import CNKISearcher, PaperInfo

        return {"CNKISearcher": CNKISearcher, "PaperInfo": PaperInfo}[name]
    if name == "GoogleScholarSearcher":
        from src.search.google_scholar import GoogleScholarSearcher

        return GoogleScholarSearcher
    raise AttributeError(f"module 'src.search' has no attribute {name!r}")
