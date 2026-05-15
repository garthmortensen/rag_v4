"""Load pipeline settings from rag.toml.

Uses stdlib tomllib (Python 3.11+) — no extra dependencies.
API keys are loaded from .env via python-dotenv.

Usage::

    from rag.config import load_config

    cfg = load_config()          # reads rag.toml from cwd
    cfg = load_config("my.toml") # explicit path
"""

import tomllib
from dataclasses import dataclass, fields
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]  # project root


# define defaults
# load_config merges these with any toml overrides
@dataclass
class Config:
    # Chunking
    chunk_size: int = 1000
    chunk_overlap: int = 100

    # Storage
    collection_name: str = "rag_docs_lc"
    vector_db_dir: str = str(_ROOT / "corpus" / "vector_db")

    # Embedder: "huggingface" | "ollama"
    embedder: str = "huggingface"
    embedder_model: str = "all-MiniLM-L6-v2"

    # LLM: "ollama" | "openai" | "anthropic"
    llm_provider: str = "ollama"
    llm_model: str = "llama3.2:3b"
    llm_temperature: float = 0.1

    # Retrieval
    top_k: int = 5



def load_config(path: str = "rag.toml") -> Config:
    """Parse *path* and return a merged Config (defaults + overrides).

    Missing file → all defaults. Unknown keys in the file are silently ignored.
    """
    from dotenv import load_dotenv

    load_dotenv()

    try:
        with open(path, "rb") as f:
            raw = tomllib.load(f).get("rag", {})
    except FileNotFoundError:
        raw = {}

    known = {
        field.name
        for field in fields(Config)
    }
    merged: dict = {
        k: v
        for k, v in raw.items()
        if k in known
    }

    # Read each section of rag.toml and copy recognised keys into merged.
    chunking = raw.get("chunking", {})
    if "chunk_size" in chunking:
        merged["chunk_size"] = chunking["chunk_size"]
    if "chunk_overlap" in chunking:
        merged["chunk_overlap"] = chunking["chunk_overlap"]

    storage = raw.get("storage", {})
    if "collection_name" in storage:
        merged["collection_name"] = storage["collection_name"]
    if "vector_db_dir" in storage:
        merged["vector_db_dir"] = storage["vector_db_dir"]

    embedder = raw.get("embedder", {})
    if "type" in embedder:
        merged["embedder"] = embedder["type"]
    if "model" in embedder:
        merged["embedder_model"] = embedder["model"]

    llm = raw.get("llm", {})
    if "provider" in llm:
        merged["llm_provider"] = llm["provider"]
    if "model" in llm:
        merged["llm_model"] = llm["model"]
    if "temperature" in llm:
        merged["llm_temperature"] = llm["temperature"]

    retrieval = raw.get("retrieval", {})
    if "top_k" in retrieval:
        merged["top_k"] = retrieval["top_k"]

    cfg = Config(**merged)

    # Keep vector DB path anchored at repo root when config uses a relative path.
    db_path = Path(cfg.vector_db_dir)
    if not db_path.is_absolute():
        cfg.vector_db_dir = str(_ROOT / db_path)

    return cfg
