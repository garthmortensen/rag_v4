# rag_v4

LangChain RAG pipeline over a local corpus of HTML and PDF documents.

Justification for RAGing open source docs: enclosed answer space. I want answers sourced from these docs and these docs alone, with confidence.

Consider CRAG.

## Repository layout

```text
corpus/
  data_sources.csv      # source list: Name, Category, Filetype, Link
  downloader.py         # step 1 — fetch source documents
  raw_data/             # documents already downloaded
  vector_db/            # ChromaDB persistence (created by ingest)
rag/
  config.py             # loads rag.toml into a Config dataclass
  ingest.py             # step 2 — embed documents into ChromaDB
  query.py              # step 3 — ask questions, get answers
  ui.py                 # Streamlit chat UI  (streamlit run rag/ui.py)
  ragas_scoring.py      # RAGAS faithfulness scoring
```

## Setup

```bash
# minimum — HuggingFace embedder + whichever LLM provider you use
uv sync --extra hf --extra ollama        # Ollama (local)
uv sync --extra hf --extra openai        # OpenAI
uv sync --extra hf --extra anthropic     # Anthropic
```

RAGAS faithfulness scoring is built in; enable it with `eval_enabled = true` under `[rag.evaluation]` in `rag.toml`.

`--extra hf` installs the HuggingFace sentence-transformers embedder (`[rag.embedder] type = "huggingface"`).  
`--extra ollama` additionally enables the Ollama embedder (`type = "ollama"`) plus the Ollama LLM provider.  
Ollama must be running locally when using the `ollama` embedder or LLM provider.

## Step 1 — Download source documents

Run from the **repo root**:

```bash
python corpus/downloader.py
```

Reads URLs from `corpus/data_sources.csv` and saves files to `corpus/raw_data/` — the
default `raw_data_dir` in `rag.toml`. Already-downloaded files are skipped.

## Step 2 — Ingest documents into ChromaDB

Run from the **repo root**:

```bash
uv run python -m rag.ingest
```

Reads all `.html` and `.pdf` files from `raw_data_dir`, splits them into
chunks, embeds each chunk with the configured embedder (HuggingFace or Ollama,
set under `[rag.embedder]` in `rag.toml`), and stores everything in
ChromaDB. **Skips ingestion if the collection already exists.**  
Delete `corpus/vector_db/` to force a full rebuild.

## Step 3 — Query

**Interactive REPL** (builds the chain once, loop until you quit):

```bash
uv run python -m rag.query
```

**Single-shot from a script or Python session:**

```python
from rag.query import query

result = query("What happens to bank capital under the severely adverse scenario?")
print(result["answer"])
for chunk in result["sources"]:
    print(chunk.metadata["source"])
```

`result` is always `{"answer": str, "sources": list[Document]}`.
