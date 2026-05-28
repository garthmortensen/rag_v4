# rag_v4

LangChain RAG pipeline over a local corpus of HTML, PDF, and CSV documents.

Justification for RAGing open source docs: enclosed answer space. I want answers sourced from these docs and these docs alone, with confidence.

Consider CRAG.

## Repository layout

```text
corpus/
  data_sources.csv      # source list: Name, Category, Filetype, Link
  downloader.py         # step 1 — fetch source documents
  raw_data/             # documents already downloaded
  raw_data2/            # output directory for downloader.py (created on first run)
  vector_db/            # ChromaDB persistence (created by ingest)
rag/
  config.py           # loads rag.toml into a Config dataclass
  ingest.py           # step 2 — embed documents into ChromaDB
  query.py            # step 3 — ask questions, get answers
  ui.py               # Streamlit chat UI  (streamlit run rag/ui.py)
  benchmark.py        # time each pipeline stage
```

## Setup

```bash
uv sync --extra hf --extra ollama
```

`--extra hf` installs the HuggingFace sentence-transformers embedder.  
`--extra ollama` installs the Ollama LLM client. Ollama must be running locally.

## Step 1 — Download source documents

Run from the **repo root**:

```bash
python corpus/downloader.py
```

Reads URLs from `corpus/data_sources.csv` and saves files to `corpus/raw_data2/`.  
Already-downloaded files are skipped. Update `raw_data_dir` in `rag.toml` to point at `raw_data2/` if you want to ingest the freshly downloaded files instead of the existing `raw_data/`.

## Step 2 — Ingest documents into ChromaDB

Run from the **repo root**:

```bash
uv run python -m rag.ingest
```

Reads all `.html` and `.pdf` files from `raw_data_dir`, splits them into
chunks, embeds each chunk with the HuggingFace model, and stores everything in
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

## Configuration

Edit `rag.toml`:

```toml
[rag.chunking]
chunk_size    = 1000
chunk_overlap = 100

[rag.storage]
collection_name = "rag_docs"
vector_db_dir   = "corpus/vector_db"

[rag.embedder]
type  = "huggingface"
model = "all-MiniLM-L6-v2"

[rag.llm]
provider    = "ollama"
model       = "llama3.2:3b"
temperature = 0.1

[rag.retrieval]
top_k = 5

[rag.ingestion]
raw_data_dir = "corpus/raw_data"
```

All paths are relative to the repo root.

