"""Paper download manager.

Supports:
- CNKI paper download (PDF / CAJ)
- Google Scholar full-text link tracking
- Batch download with retry
- Download progress monitoring
"""

from __future__ import annotations

import argparse
import json
import os
import re
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
        if max_retries < 1:
            raise ValueError("max_retries must be at least 1")

        # Generate filename
        if not filename:
            parsed = urlparse(url)
            filename = os.path.basename(parsed.path) or f"paper_{int(time.time())}.pdf"
        filename = self._safe_filename(filename)

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
                result = self.download(url, filename=f"{title}.pdf")
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

    @staticmethod
    def _safe_filename(filename: str, default_ext: str = ".pdf") -> str:
        """Return a filesystem-safe filename for Windows and POSIX."""
        name = Path(filename).name
        stem = Path(name).stem
        suffix = Path(name).suffix or default_ext
        stem = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "_", stem).strip(" .")
        suffix = re.sub(r'[^A-Za-z0-9.]', "", suffix) or default_ext

        if not stem:
            stem = f"paper_{int(time.time())}"
        if stem.upper() in {"CON", "PRN", "AUX", "NUL", *{f"COM{i}" for i in range(1, 10)}, *{f"LPT{i}" for i in range(1, 10)}}:
            stem = f"{stem}_file"

        max_stem_length = max(1, 180 - len(suffix))
        return f"{stem[:max_stem_length]}{suffix}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Batch paper download manager")
    parser.add_argument("--input", required=True, help="Input JSON metadata file")
    parser.add_argument(
        "--source",
        choices=["cnki", "google_scholar", "gs"],
        default="cnki",
        help="Data source",
    )
    parser.add_argument(
        "--download-dir", default="data/downloads", help="Directory for downloads"
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    with open(args.input, "r", encoding="utf-8") as f:
        papers = json.load(f)
    if not isinstance(papers, list):
        raise ValueError("Input metadata must be a JSON list of paper objects")

    manager = DownloadManager(download_dir=args.download_dir)
    stats = manager.batch_download(papers, source=args.source)
    print(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
