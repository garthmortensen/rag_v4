"""Core data types. No external dependencies."""

from dataclasses import dataclass, field


@dataclass
class Document:
    """Raw text loaded from a source file."""

    text: str
    metadata: dict = field(default_factory=dict)


@dataclass
class Chunk:
    """A fragment of a Document, ready for embedding."""

    text: str
    doc_id: str
    chunk_index: int
    metadata: dict = field(default_factory=dict)


@dataclass
class SearchResult:
    """A retrieved chunk with its relevance score."""

    chunk: Chunk
    score: float   # higher = more similar
    rank: int      # 1-based
