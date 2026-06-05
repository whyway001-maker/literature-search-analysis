"""
文献检索、下载、分析 — 快速启动脚本

Usage:
    python scripts/run_search.py --source cnki --keywords "动力电池回收"
    python scripts/run_search.py --source gs --keywords "reverse logistics"
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.search.cnki import CNKISearcher
from src.search.google_scholar import GoogleScholarSearcher


def main():
    parser = argparse.ArgumentParser(description="文献检索工具")
    parser.add_argument("--source", choices=["cnki", "gs"], required=True, help="检索来源")
    parser.add_argument("--keywords", required=True, help="检索关键词")
    parser.add_argument("--limit", type=int, default=20, help="结果数量上限")
    parser.add_argument("--year-from", type=int, help="起始年份")
    parser.add_argument("--year-to", type=int, help="结束年份")
    parser.add_argument("--export", choices=["json", "csv", "bibtex"], default="json", help="导出格式")
    parser.add_argument("--output", help="输出文件路径")

    args = parser.parse_args()

    if args.source == "cnki":
        searcher = CNKISearcher()
        results = searcher.search(
            keywords=args.keywords,
            limit=args.limit,
            year_from=args.year_from,
            year_to=args.year_to,
        )
    else:
        searcher = GoogleScholarSearcher()
        results = searcher.search(
            keywords=args.keywords,
            limit=args.limit,
            year_from=args.year_from,
            year_to=args.year_to,
        )

    if args.output:
        print(searcher.export_results(format=args.export, filepath=args.output))
    else:
        print(f"\n检索完成: {len(results)} 条结果")


if __name__ == "__main__":
    main()
