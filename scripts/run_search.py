"""One-click literature search launcher.

Examples:
    python scripts/run_search.py --source cnki --keywords "battery recycling"
    python scripts/run_search.py --source gs --keywords "reverse logistics" --export csv
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.search.cnki import CNKISearcher
from src.search.google_scholar import GoogleScholarSearcher


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Literature search tool for CNKI and Google Scholar"
    )
    parser.add_argument(
        "--source", choices=["cnki", "gs"], required=True, help="Search source"
    )
    parser.add_argument("--keywords", required=True, help="Search keywords")
    parser.add_argument("--limit", type=int, default=20, help="Max results")
    parser.add_argument("--year-from", type=int, help="Start year")
    parser.add_argument("--year-to", type=int, help="End year")
    parser.add_argument(
        "--export",
        choices=["json", "csv", "bibtex", "ris", "md"],
        default="json",
        help="Export format",
    )
    parser.add_argument("--output", help="Output file path")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    searcher = CNKISearcher() if args.source == "cnki" else GoogleScholarSearcher()
    results = searcher.search(
        keywords=args.keywords,
        limit=args.limit,
        year_from=args.year_from,
        year_to=args.year_to,
    )

    exported = searcher.export_results(format=args.export, filepath=args.output)
    if args.output:
        print(f"Search complete: {len(results)} results written to {exported}")
    else:
        print(exported)


if __name__ == "__main__":
    main()
