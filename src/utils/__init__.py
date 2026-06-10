"""Utility modules."""

__all__ = ["PDFParser", "Exporter"]


def __getattr__(name: str):
    if name == "PDFParser":
        from src.utils.pdf_parser import PDFParser

        return PDFParser
    if name == "Exporter":
        from src.utils.exporter import Exporter

        return Exporter
    raise AttributeError(f"module 'src.utils' has no attribute {name!r}")
