"""Component protocols (interfaces). No external dependencies.

Implement any of these to swap a backend without touching the pipeline.

Example — custom embedder::

    class MyEmbedder:
        def embed(self, texts: list[str]) -> list[list[float]]: ...
        def embed_query(self, text: str) -> list[float]: ...

    pipeline = RAGPipeline(..., embedder=MyEmbedder(), ...)
"""

from collections.abc import Iterator
from typing import Protocol, runtime_checkable

from rag.core.types import Chunk, Document, SearchResult


@runtime_checkable
class Loader(Protocol):
    def load(self, source: str) -> list[Document]: ...


@runtime_checkable
class Splitter(Protocol):
    def split(self, docs: list[Document]) -> list[Chunk]: ...


@runtime_checkable
class Embedder(Protocol):
    def embed(self, texts: list[str]) -> list[list[float]]: ...
    def embed_query(self, text: str) -> list[float]: ...


@runtime_checkable
class VectorStore(Protocol):
    def upsert(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None: ...
    def search(self, embedding: list[float], k: int) -> list[SearchResult]: ...


@runtime_checkable
class LLM(Protocol):
    def complete(self, system: str, user: str) -> str: ...
    def stream(self, system: str, user: str) -> Iterator[str]: ...
