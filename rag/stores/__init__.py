"""VectorStore factory."""

from rag.core.protocols import VectorStore


def get_store(config) -> VectorStore:
    from rag.stores.chroma import ChromaStore

    return ChromaStore(
        persist_dir=config.vector_db_dir,
        collection_name=config.collection_name,
    )
