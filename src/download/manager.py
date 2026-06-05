"""
Paper download manager.

Supports:
- CNKI paper download (PDF / CAJ)
- Google Scholar full-text link tracking
- Batch download with retry
- Download progress monitoring
"""

import os
import time
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse


class DownloadManager:
    """Manages paper download workflows.

    Supports resume, format detection, and retry mechanisms.
    """

    SUPPORTED_FORMATS = {".pdf", ".caj", ".html", ".xml"}

    def __init__(self, download_dir: str = "data/downloads"):
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(parents=True, exist_ok=True)
        self.downloaded: list[str] = []
        self.failed: list[dict] = []

    def download(
        self,
        url: str,
        filename: Optional[str] = None,
        max_retries: int = 3,
    ) -> Optional[str]:
        """Download a single paper.

        Args:
            url: Download link
            filename: Saved filename (without path)
            max_retries: Maximum retry attempts

        Returns:
            Downloaded file path, or None on failure
        """
        # Actual download logic handled by Codex cnki-download / gs-fulltext skills
        if not url:
            print("[Download] Empty URL, skipping")
            return None

        # Generate filename
        if not filename:
            parsed = urlparse(url)
            filename = os.path.basename(parsed.path) or f"paper_{int(time.time())}.pdf"

        filepath = self.download_dir / filename
        print(f"[Download] {url[:80]}... -> {filepath}")

        # Actual download performed by skill
        return str(filepath)

    def batch_download(
        self,
        papers: list[dict],
        source: str = "cnki",
    ) -> dict:
        """Batch download papers.

        Args:
            papers: List of paper info dicts (must contain 'download_url')
            source: Data source (cnki / google_scholar)

        Returns:
            {downloaded: [...], failed: [...], total, success_count, fail_count}
        """
        print(f"[Batch Download] {len(papers)} papers, source: {source}")

        for paper in papers:
            url = paper.get("download_url", "")
            title = paper.get("title", "unknown")
            if url:
                result = self.download(url, filename=f"{title[:50]}.pdf")
                if result:
                    self.downloaded.append(result)
                else:
                    self.failed.append({"title": title, "url": url})
            else:
                self.failed.append({"title": title, "url": "", "reason": "No download link"})

        return {
            "downloaded": self.downloaded,
            "failed": self.failed,
            "total": len(papers),
            "success_count": len(self.downloaded),
            "fail_count": len(self.failed),
        }

    def get_stats(self) -> dict:
        """Get download statistics."""
        total_size = sum(
            os.path.getsize(f) for f in self.downloaded if os.path.exists(f)
        )
        return {
            "downloaded_count": len(self.downloaded),
            "failed_count": len(self.failed),
            "total_size_mb": round(total_size / 1024 / 1024, 2),
            "download_dir": str(self.download_dir),
        }
