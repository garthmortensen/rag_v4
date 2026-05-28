"""Load pipeline settings from rag.toml.

Uses stdlib tomllib (Python 3.11+) — no extra dependencies.
API keys are loaded from .env via python-dotenv.

Usage::

    from rag.config import load_config

    cfg = load_config()          # reads rag.toml from cwd
    cfg = load_config("my.toml") # explicit path
"""

import tomllib
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

project_root = Path(__file__).resolve().parents[1]


# define defaults
# load_config merges these with any toml overrides
@dataclass
class Config:
    # Chunking
    chunk_size: int = 1000
    chunk_overlap: int = 100

    # Storage
    collection_name: str = "rag_docs"
    # str(project_root / "corpus" / "vector_db") ensures the default is repo-root-relative
    vector_db_dir: str = str(project_root / "corpus" / "vector_db")

    # Embedder: "huggingface" | "ollama"
    embedder: str = "huggingface"
    embedder_model: str = "all-MiniLM-L6-v2"

    # LLM: "ollama" | "openai" | "anthropic"
    llm_provider: str = "ollama"
    llm_model: str = "llama3.2:3b"
    llm_temperature: float = 0.1

    # Evaluation — judge LLM for RAGAS scoring (needs structured-output capability)
    # provider: "ollama" | "openai" | "anthropic"
    eval_enabled: bool = False
    eval_provider: str = "ollama"
    eval_model: str = ""

    # Retrieval
    top_k: int = 5

    # Ingestion
    raw_data_dir: str = str(project_root / "corpus" / "raw_data")



def load_config(path: str = "rag.toml") -> Config:
    load_dotenv()

    try:
        with open(path, "rb") as f:
            raw = tomllib.load(f).get("rag", {})
    except FileNotFoundError:
        raw = {}

    chunking_cfg = raw.get("chunking", {})
    storage_cfg = raw.get("storage", {})
    embedder_cfg = raw.get("embedder", {})
    llm_cfg = raw.get("llm", {})
    retrieval_cfg = raw.get("retrieval", {})

    cfg = Config()
    cfg.chunk_size       = chunking_cfg.get("chunk_size",    cfg.chunk_size)
    cfg.chunk_overlap    = chunking_cfg.get("chunk_overlap", cfg.chunk_overlap)
    cfg.collection_name  = storage_cfg.get("collection_name", cfg.collection_name)
    cfg.vector_db_dir    = storage_cfg.get("vector_db_dir",   cfg.vector_db_dir)
    cfg.embedder         = embedder_cfg.get("type",  cfg.embedder)
    cfg.embedder_model   = embedder_cfg.get("model", cfg.embedder_model)
    cfg.llm_provider     = llm_cfg.get("provider",    cfg.llm_provider)
    cfg.llm_model        = llm_cfg.get("model",       cfg.llm_model)
    cfg.llm_temperature  = llm_cfg.get("temperature", cfg.llm_temperature)
    eval_cfg             = raw.get("evaluation", {})
    cfg.eval_enabled     = eval_cfg.get("enabled",   cfg.eval_enabled)
    cfg.eval_provider    = eval_cfg.get("provider",  cfg.eval_provider)
    cfg.eval_model       = eval_cfg.get("model",     cfg.eval_model)
    cfg.top_k            = retrieval_cfg.get("top_k", cfg.top_k)
    cfg.raw_data_dir     = raw.get("ingestion", {}).get("raw_data_dir", cfg.raw_data_dir)

    # Keep paths anchored at repo root when config uses a relative path.
    db_path = Path(cfg.vector_db_dir)
    if not db_path.is_absolute():
        cfg.vector_db_dir = str(project_root / db_path)

    raw_path = Path(cfg.raw_data_dir)
    if not raw_path.is_absolute():
        cfg.raw_data_dir = str(project_root / raw_path)

    return cfg
