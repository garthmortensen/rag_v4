"""Load raw documents into ChromaDB.

Reads all supported files from cfg.raw_data_dir, splits them into chunks,
and rebuilds the ChromaDB collection from scratch.

Full rebuild on every run
Embedder: HuggingFace (langchain_huggingface / sentence-transformers)
Vector store: ChromaDB (persistent, local)
Text splitter: RecursiveCharacterTextSplitter
Supported file types: HTML, PDF, CSV
"""

from pathlib import Path

import chromadb
from langchain_chroma import Chroma
from langchain_community.document_loaders import BSHTMLLoader, CSVLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

from rag.config import load_config

LOADERS = {
    ".html": BSHTMLLoader,
    ".pdf":  PyPDFLoader,
    ".csv":  CSVLoader,
}


def load_docs(source_dir: Path) -> list:
    docs = []
    for file in sorted(source_dir.iterdir()):
        loader_cls = LOADERS.get(file.suffix.lower())
        if loader_cls:
            docs.extend(loader_cls(str(file)).load())
    return docs


def build_embedder(cfg):
    return HuggingFaceEmbeddings(model_name=cfg.embedder_model)


def ingest():
    cfg = load_config()
    source_dir = Path(cfg.raw_data_dir)

    print(f"Loading documents from {source_dir} ...")
    docs = load_docs(source_dir)
    print(f"  {len(docs)} documents loaded")

    chunks = RecursiveCharacterTextSplitter(
        chunk_size=cfg.chunk_size,
        chunk_overlap=cfg.chunk_overlap,
    ).split_documents(docs)
    print(f"  {len(chunks)} chunks after splitting")

    embedder = build_embedder(cfg)

    # Reset: delete the collection so every run starts fresh.
    client = chromadb.PersistentClient(path=cfg.vector_db_dir)
    try:
        client.delete_collection(cfg.collection_name)
        print(f"  Dropped existing collection '{cfg.collection_name}'")
    except ValueError:
        pass  # collection didn't exist yet

    Chroma.from_documents(
        chunks,
        embedder,
        client=client,
        collection_name=cfg.collection_name,
    )
    print(f"Done — {len(chunks)} chunks stored in '{cfg.collection_name}'")


if __name__ == "__main__":
    ingest()
