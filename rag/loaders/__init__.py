"""Loader dispatcher and directory walker.

Usage::

    from rag.loaders import MultiLoader, load_directory

    loader = MultiLoader()
    docs = loader.load("report.pdf")
    docs = load_directory("corpus/raw_data/")
"""

import logging
import os

from rag.core.types import Document
from rag.loaders.pdf import PDFLoader
from rag.loaders.text import TEXT_EXTENSIONS, TextLoader

logger = logging.getLogger(__name__)

SUPPORTED: frozenset[str] = frozenset({".pdf"}) | TEXT_EXTENSIONS

_pdf = PDFLoader()
_text = TextLoader()


class MultiLoader:
    """Dispatches to the right loader based on file extension."""

    def load(self, source: str) -> list[Document]:
        ext = os.path.splitext(source)[1].lower()
        if ext == ".pdf":
            return _pdf.load(source)
        if ext in TEXT_EXTENSIONS:
            return _text.load(source)
        raise ValueError(
            f"Unsupported file type: {ext!r}. Supported: {sorted(SUPPORTED)}"
        )


def load_directory(directory: str) -> list[Document]:
    """Recursively load all supported files under *directory*."""
    loader = MultiLoader()
    docs: list[Document] = []
    for root, _, files in os.walk(directory):
        for fname in sorted(files):
            if os.path.splitext(fname)[1].lower() not in SUPPORTED:
                continue
            path = os.path.join(root, fname)
            try:
                docs.extend(loader.load(path))
            except Exception as exc:
                logger.warning("Skipping %s: %s", path, exc)
    return docs
