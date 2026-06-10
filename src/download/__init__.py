"""Download module."""

__all__ = ["DownloadManager"]


def __getattr__(name: str):
    if name == "DownloadManager":
        from src.download.manager import DownloadManager

        return DownloadManager
    raise AttributeError(f"module 'src.download' has no attribute {name!r}")
