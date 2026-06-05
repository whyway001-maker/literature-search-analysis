"""
CNKI 检索模块测试
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.search.cnki import CNKISearcher, PaperInfo


def test_paper_info_creation():
    """测试 PaperInfo 数据类"""
    paper = PaperInfo(
        title="闭环供应链协调机制研究",
        authors=["张三", "李四"],
        journal="中国管理科学",
        year=2024,
        keywords=["闭环供应链", "协调机制"],
    )
    d = paper.to_dict()
    assert d["title"] == "闭环供应链协调机制研究"
    assert len(d["authors"]) == 2
    assert d["source_db"] == "cnki"


def test_cnki_searcher_init():
    """测试 CNKI 检索器初始化"""
    searcher = CNKISearcher()
    assert searcher.results == []
    assert searcher.total_count == 0


def test_empty_keywords_raises():
    """测试空关键词抛出异常"""
    searcher = CNKISearcher()
    try:
        searcher.search("")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_export_empty_json():
    """测试导出空结果为 JSON"""
    searcher = CNKISearcher()
    result = searcher.export_results(format="json")
    assert result == "[]"


if __name__ == "__main__":
    test_paper_info_creation()
    test_cnki_searcher_init()
    test_empty_keywords_raises()
    test_export_empty_json()
    print("All tests passed!")
