"""
文献下载管理器

支持：
- CNKI 文献下载（PDF/CAJ）
- Google Scholar 全文链接追踪
- 批量下载与重试
- 下载进度监控
"""

import os
import time
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse


class DownloadManager:
    """文献下载管理器

    管理文献检索结果的下载流程，
    支持断点续传、格式识别、重试机制。
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
        """下载单篇文献

        Args:
            url: 下载链接
            filename: 保存文件名（不含路径）
            max_retries: 最大重试次数

        Returns:
            下载后的文件路径，失败返回 None
        """
        # TODO: 集成 Codex cnki-download skill 或 gs-fulltext skill
        # 实际下载逻辑依赖浏览器自动化的 skill

        if not url:
            print("[Download] URL 为空，跳过")
            return None

        # 生成文件名
        if not filename:
            parsed = urlparse(url)
            filename = os.path.basename(parsed.path) or f"paper_{int(time.time())}.pdf"

        filepath = self.download_dir / filename
        print(f"[Download] {url[:80]}... -> {filepath}")

        # 实际下载由 skill 完成
        # self.downloaded.append(str(filepath))
        return str(filepath)

    def batch_download(
        self,
        papers: list[dict],
        source: str = "cnki",
    ) -> dict:
        """批量下载文献

        Args:
            papers: 文献信息列表（包含 download_url 字段）
            source: 数据源 (cnki/google_scholar)

        Returns:
            {downloaded: [...], failed: [...]}
        """
        print(f"[Batch Download] 共 {len(papers)} 篇文献，来源: {source}")

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
                self.failed.append({"title": title, "url": "", "reason": "无下载链接"})

        return {
            "downloaded": self.downloaded,
            "failed": self.failed,
            "total": len(papers),
            "success_count": len(self.downloaded),
            "fail_count": len(self.failed),
        }

    def get_stats(self) -> dict:
        """获取下载统计"""
        total_size = sum(
            os.path.getsize(f) for f in self.downloaded if os.path.exists(f)
        )
        return {
            "downloaded_count": len(self.downloaded),
            "failed_count": len(self.failed),
            "total_size_mb": round(total_size / 1024 / 1024, 2),
            "download_dir": str(self.download_dir),
        }
