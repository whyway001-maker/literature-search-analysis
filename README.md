# LitLab — Literature Auto Search, Download & Analysis

> Multi-source academic literature search, batch download, and AI-driven analysis — supports CNKI, Google Scholar, and more.

## Features

- **Multi-source Search**: CNKI (China National Knowledge Infrastructure) + Google Scholar — keyword, advanced, and journal search
- **Batch Download**: Auto-detect full-text links, batch download PDF/CAJ papers
- **Metadata Export**: Structured export in BibTeX / CSV / JSON formats
- **AI Analysis**: Auto-summarization, knowledge graph construction, topic clustering
- **Citation Analysis**: Citation chain tracking, highly-cited paper filtering
- **Reading Assistant**: PDF parsing, key info extraction, literature review generation

## Project Structure

```
literature-search-analysis/
├── src/
│   ├── search/          # Search engines (CNKI, Google Scholar)
│   ├── download/        # Download manager
│   ├── analysis/        # Literature analysis (NLP, clustering, knowledge graph)
│   └── utils/           # Utilities (PDF parser, format converter)
├── data/
│   ├── raw/             # Raw search results
│   └── processed/       # Cleaned data
├── scripts/             # Automation scripts
├── outputs/
│   ├── figures/         # Visualization charts
│   └── tables/          # Analysis tables
├── paper/               # Manuscripts
├── tests/               # Test cases
└── .github/workflows/   # CI/CD
```

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# CNKI literature search
python -m src.search.cnki "closed-loop supply chain" --count 20

# Google Scholar search
python -m src.search.google_scholar "reverse logistics" --years 2020-2025

# Batch download
python -m src.download.manager --source cnki --keywords "battery recycling"

# Literature analysis
python -m src.analysis.pipeline --input data/raw/results.json
```

## Tech Stack

| Component | Technology |
|-----------|------------|
| Browser Automation | Playwright / Chrome DevTools Protocol |
| Data Extraction | BeautifulSoup4, lxml |
| NLP Analysis | spaCy, jieba, scikit-learn |
| Knowledge Graph | NetworkX |
| PDF Parsing | PyMuPDF, pdfplumber |
| Reference Management | Zotero API |

## Codex Skills Integration

This project integrates with the following Codex skill modules for browser automation and academic search:

- `cnki-search` — CNKI basic search
- `cnki-advanced-search` — CNKI advanced search
- `cnki-download` — CNKI paper download
- `cnki-export` — CNKI data export
- `cnki-paper-detail` — CNKI paper details
- `cnki-navigate-pages` — CNKI pagination
- `cnki-journal-search` — CNKI journal search
- `cnki-journal-toc` — CNKI journal TOC
- `cnki-journal-index` — CNKI journal index
- `gs-search` — Google Scholar search
- `gs-advanced-search` — Google Scholar advanced search
- `gs-cited-by` — Google Scholar citation tracking
- `gs-export` — Google Scholar export
- `gs-fulltext` — Google Scholar full-text access
- `gs-navigate-pages` — Google Scholar pagination
- `nature-*` — Nature suite (academic writing, reading, figures, etc.)
- `PaperSpine` — Academic paper writing guidance
- `zotero-mcp` — Zotero reference management integration

## License

MIT License
