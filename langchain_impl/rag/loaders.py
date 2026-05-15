"""Supported file extensions for the LangChain pipeline.

LangChain provides its own loaders (PyPDFLoader, TextLoader, etc.) —
these are used in the pipeline's ingest() method. This module just
exports the set of supported extensions so web.py can validate uploads.
"""

TEXT_EXTENSIONS: frozenset[str] = frozenset({".txt", ".md", ".rst", ".html", ".htm", ".csv"})
SUPPORTED: frozenset[str] = frozenset({".pdf"}) | TEXT_EXTENSIONS
