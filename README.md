# rag_v4

LangChain-only RAG implementation.

## Repository layout

```text
corpus/
  raw_data/           # source documents (HTML, CSV, PDF)
  vector_db/          # Chroma persistence
langchain_impl/
  rag/
    core/pipeline.py  # LangChain + LCEL pipeline
    eval/             # eval dataset, harness, metrics, types
    static/index.html # web UI
    web.py            # FastAPI server
  rag.toml            # runtime config for langchain_impl
```

## Quick start

```bash
cd langchain_impl
uv sync --extra web --extra ollama
uv run python -m rag ingest ../corpus/raw_data/
uv run python -m rag serve
```

Open <http://127.0.0.1:8000>

## CLI

```bash
uv run python -m rag ingest <sources...>
uv run python -m rag query "question"
uv run python -m rag query "question" --stream
uv run python -m rag eval
uv run python -m rag eval --fast
uv run python -m rag serve [--host] [--port]
```

## Configuration

Edit `langchain_impl/rag.toml`:

```toml
[rag.chunking]
chunk_size = 1000
chunk_overlap = 100

[rag.storage]
collection_name = "rag_docs_lc"
vector_db_dir = "corpus/vector_db"

[rag.embedder]
type = "huggingface"   # or "ollama"
model = "all-MiniLM-L6-v2"

[rag.llm]
provider = "ollama"    # or "openai", "anthropic"
model = "llama3.2:3b"
temperature = 0.1

[rag.retrieval]
top_k = 5

[rag.infrastructure]
ollama_host = "http://localhost:11434"
```

## Notes

- API keys for OpenAI/Anthropic are read from environment variables.
  - `eval --fast` skips LLM-based ragas scoring and runs embedding-only checks.
