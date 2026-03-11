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


# define defaults
# load_config merges these with any toml overrides
@dataclass
class Config:
    # Chunking
    chunk_size: int = 1000
    chunk_overlap: int = 100

    # Storage
    collection_name: str = "rag_docs"
    vector_db_dir: str = "corpus/vector_db"

    # Embedder: "huggingface" | "ollama"
    embedder: str = "huggingface"
    embedder_model: str = "all-MiniLM-L6-v2"

    # LLM: "ollama" | "openai" | "anthropic"
    llm_provider: str = "ollama"
    llm_model: str = "llama3.2:3b"
    llm_temperature: float = 0.1

    # Retrieval
    top_k: int = 5

    # Infrastructure
    ollama_host: str = "http://localhost:11434"


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

    known = {field.name for field in fields(Config)}
    valid = {k: v for k, v in raw.items() if k in known}
    return Config(**valid)
