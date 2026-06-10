"""Analysis module."""

__all__ = ["AnalysisPipeline"]


def __getattr__(name: str):
    if name == "AnalysisPipeline":
        from src.analysis.pipeline import AnalysisPipeline

        return AnalysisPipeline
    raise AttributeError(f"module 'src.analysis' has no attribute {name!r}")
