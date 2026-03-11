"""Recursive character text splitter — pure Python, no LangChain.

Algorithm (mirrors LangChain's RecursiveCharacterTextSplitter):
  1. Try to split on the first separator in the list.
  2. For any piece that is still too large, recurse with the next separator.
  3. Merge small pieces greedily up to chunk_size, maintaining chunk_overlap
     between consecutive chunks.
"""

import hashlib

from rag.core.types import Chunk, Document

_SEPARATORS = ["\n\n", "\n", ". ", " ", ""]


class RecursiveSplitter:
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 100,
        separators: list[str] | None = None,
    ) -> None:
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators if separators is not None else _SEPARATORS

    # ── public ──────────────────────────────────────────────────────

    def split(self, docs: list[Document]) -> list[Chunk]:
        chunks: list[Chunk] = []
        for doc in docs:
            source = doc.metadata.get("source", "")
            doc_id = hashlib.sha256(source.encode()).hexdigest()[:12]
            texts = self._split_text(doc.text, self.separators)
            for i, text in enumerate(texts):
                chunks.append(
                    Chunk(
                        text=text,
                        doc_id=doc_id,
                        chunk_index=i,
                        metadata=dict(doc.metadata),
                    )
                )
        return chunks

    # ── internals ────────────────────────────────────────────────────

    def _split_text(self, text: str, separators: list[str]) -> list[str]:
        """Recursively split *text* using the first separator that works."""
        if not text.strip():
            return []

        sep = separators[0]
        next_seps = separators[1:]

        raw_splits = text.split(sep) if sep else list(text)

        # For each raw split: keep if small, recurse if too large
        good: list[str] = []
        for piece in raw_splits:
            if not piece.strip():
                continue
            if len(piece) <= self.chunk_size:
                good.append(piece)
            elif next_seps:
                good.extend(self._split_text(piece, next_seps))
            else:
                good.append(piece)  # can't split further

        return self._merge(good, sep)

    def _merge(self, splits: list[str], sep: str) -> list[str]:
        """Greedily merge splits into chunks of at most chunk_size chars,
        preserving chunk_overlap between consecutive chunks."""
        chunks: list[str] = []
        buf: list[str] = []
        buf_len: int = 0
        sep_len = len(sep)

        for piece in splits:
            piece_len = len(piece)
            # +sep between existing buf and new piece (if buf non-empty)
            add_len = piece_len + (sep_len if buf else 0)

            if buf_len + add_len > self.chunk_size and buf:
                chunks.append(sep.join(buf))
                # Roll back buf to maintain overlap
                while buf and buf_len > self.chunk_overlap:
                    removed = buf.pop(0)
                    buf_len -= len(removed) + sep_len
                buf_len = max(buf_len, 0)

            buf.append(piece)
            buf_len += add_len

        if buf:
            chunks.append(sep.join(buf))

        return [c for c in chunks if c.strip()]
