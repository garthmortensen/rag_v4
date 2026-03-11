"""ChromaDB vector store (no LangChain)."""

import chromadb

from rag.core.types import Chunk, SearchResult

_BATCH_SIZE = 500  # safe under ChromaDB's SQLite param ceiling


class ChromaStore:
    """Persistent ChromaDB collection.

    Lazy-connects on first use so construction is cheap.
    """

    def __init__(
        self,
        persist_dir: str = "corpus/vector_db",
        collection_name: str = "rag_docs",
    ) -> None:
        self.persist_dir = persist_dir
        self.collection_name = collection_name
        self._collection = None

    def _col(self):
        if self._collection is None:
            client = chromadb.PersistentClient(path=self.persist_dir)
            self._collection = client.get_or_create_collection(self.collection_name)
        return self._collection

    def upsert(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        col = self._col()
        ids = [f"{c.doc_id}_chunk_{c.chunk_index:04d}" for c in chunks]
        texts = [c.text for c in chunks]
        metas = [_sanitize_meta(c.metadata) for c in chunks]

        for start in range(0, len(ids), _BATCH_SIZE):
            end = min(start + _BATCH_SIZE, len(ids))
            col.upsert(
                ids=ids[start:end],
                embeddings=embeddings[start:end],
                documents=texts[start:end],
                metadatas=metas[start:end],
            )

    def search(self, embedding: list[float], k: int = 5) -> list[SearchResult]:
        col = self._col()
        raw = col.query(
            query_embeddings=[embedding],
            n_results=min(k, col.count() or 1),
            include=["documents", "metadatas", "distances"],
        )
        results: list[SearchResult] = []
        for i, chunk_id in enumerate(raw["ids"][0]):
            meta = raw["metadatas"][0][i]
            base_id = chunk_id.rsplit("_chunk_", 1)[0]
            chunk = Chunk(
                text=raw["documents"][0][i],
                doc_id=base_id,
                chunk_index=i,
                metadata=meta,
            )
            # ChromaDB returns L2 distance; convert to a [0,1] similarity proxy
            distance = raw["distances"][0][i]
            score = 1.0 / (1.0 + distance)
            results.append(SearchResult(chunk=chunk, score=score, rank=i + 1))
        return results

    def count(self) -> int:
        return self._col().count()


def _sanitize_meta(meta: dict) -> dict:
    """ChromaDB only accepts str/int/float/bool metadata values."""
    return {
        k: v
        for k, v in meta.items()
        if isinstance(v, (str, int, float, bool))
    }
