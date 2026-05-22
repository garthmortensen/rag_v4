"""Load raw documents into ChromaDB.

Reads all supported files from cfg.raw_data_dir, splits them into chunks,
and rebuilds the ChromaDB collection from scratch.

Full rebuild on every run
Embedder: HuggingFace (langchain_huggingface / sentence-transformers)
Vector store: ChromaDB (persistent, local)
Text splitter: RecursiveCharacterTextSplitter
Supported file types: HTML, PDF
"""

from pathlib import Path
import logging

import chromadb
from chromadb.errors import NotFoundError as ChromaNotFoundError
from langchain_chroma import Chroma
from langchain_community.document_loaders import BSHTMLLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

from rag.config import load_config

# pypdf logs a warning for every malformed object in a corrupt PDF — suppress them.
logging.getLogger("pypdf").setLevel(logging.ERROR)

LOADERS = {
    ".html": BSHTMLLoader,
    ".pdf":  PyPDFLoader,
}


def load_docs(source_dir: Path) -> list:
    docs = []
    for file in sorted(source_dir.iterdir()):
        loader_cls = LOADERS.get(file.suffix.lower())
        if loader_cls is None:
            continue
        if file.suffix.lower() == ".html":
            # latin-1 maps all 256 byte values, so it never raises UnicodeDecodeError.
            # Scraped HTML files often mix encodings; latin-1 is a safe fallback.
            loader = BSHTMLLoader(str(file), open_encoding="latin-1")
        else:
            loader = loader_cls(str(file))
        docs.extend(loader.load())
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

    client = chromadb.PersistentClient(path=cfg.vector_db_dir)

    # Skip if collection already exists — delete corpus/vector_db/ to force a rebuild.
    try:
        client.get_collection(cfg.collection_name)
        print(f"  Collection '{cfg.collection_name}' already exists — skipping.")
        return
    except ChromaNotFoundError:
        pass  # collection doesn't exist yet, proceed

    Chroma.from_documents(
        chunks,
        embedder,
        client=client,
        collection_name=cfg.collection_name,
    )
    print(f"Done — {len(chunks)} chunks stored in '{cfg.collection_name}'")


if __name__ == "__main__":
    ingest()
