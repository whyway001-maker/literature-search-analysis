# LitLab - Literature Auto Search, Download, and Analysis

LitLab is a small Python toolkit for academic literature workflows. It provides
structured placeholders for multi-source search, batch download, metadata export,
and lightweight analysis of paper metadata.

## Features

- Multi-source search interfaces for CNKI and Google Scholar
- Batch download workflow with retry-oriented bookkeeping
- Metadata export to JSON, CSV, BibTeX, RIS, and Markdown
- Basic metadata analysis: keyword frequency, author frequency, year distribution
- Draft literature review report generation from structured paper metadata
- Utilities for PDF metadata extraction and future full-text parsing

## Project Structure

```text
literature-search-analysis/
|-- src/
|   |-- search/       # Search engines for CNKI and Google Scholar
|   |-- download/     # Download manager
|   |-- analysis/     # Literature analysis pipeline
|   `-- utils/        # PDF parser and export helpers
|-- data/
|   |-- raw/          # Raw search results
|   `-- processed/    # Cleaned data
|-- scripts/          # Command-line helpers
|-- outputs/
|   |-- figures/      # Visualization outputs
|   `-- tables/       # Analysis tables
|-- paper/            # Manuscript drafts
|-- tests/            # Test cases
`-- .github/workflows/
```

## Quick Start

```bash
python -m pip install -r requirements.txt

python scripts/run_search.py --source cnki --keywords "closed-loop supply chain" --limit 20
python scripts/run_search.py --source gs --keywords "reverse logistics" --year-from 2020 --year-to 2025

python -m src.analysis.pipeline --input data/raw/results.json --output outputs/tables/report.md
```

The search modules are currently integration points for browser/Codex-assisted
search workflows. They validate input and build/export structured result objects,
but they do not scrape CNKI or Google Scholar directly yet.

## Development

```bash
python -m unittest discover -s tests -v
python -m pytest tests -v
```

The standard-library command works without installing pytest. GitHub Actions
runs the pytest suite on Python 3.11.

## License

MIT License
