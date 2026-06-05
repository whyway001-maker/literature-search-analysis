"""
Tests for CNKI search module.
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.search.cnki import CNKISearcher, PaperInfo


def test_paper_info_creation():
    """Test PaperInfo dataclass."""
    paper = PaperInfo(
        title="Closed-Loop Supply Chain Coordination",
        authors=["Zhang San", "Li Si"],
        journal="Chinese Journal of Management Science",
        year=2024,
        keywords=["closed-loop supply chain", "coordination"],
    )
    d = paper.to_dict()
    assert d["title"] == "Closed-Loop Supply Chain Coordination"
    assert len(d["authors"]) == 2
    assert d["source_db"] == "cnki"


def test_cnki_searcher_init():
    """Test CNKI searcher initialization."""
    searcher = CNKISearcher()
    assert searcher.results == []
    assert searcher.total_count == 0


def test_empty_keywords_raises():
    """Test that empty keywords raise ValueError."""
    searcher = CNKISearcher()
    try:
        searcher.search("")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_export_empty_json():
    """Test exporting empty results as JSON."""
    searcher = CNKISearcher()
    result = searcher.export_results(format="json")
    assert result == "[]"


if __name__ == "__main__":
    test_paper_info_creation()
    test_cnki_searcher_init()
    test_empty_keywords_raises()
    test_export_empty_json()
    print("All tests passed!")
