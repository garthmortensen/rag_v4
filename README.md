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
  vector_db/            # ChromaDB persistence (created by ingest)
rag/
  config.py             # loads rag.toml into a Config dataclass
  ingest.py             # step 2 — embed documents into ChromaDB
  query.py              # step 3 — ask questions, get answers
  ui.py                 # Streamlit chat UI  (streamlit run rag/ui.py)
  benchmark.py          # time each pipeline stage
  evaluate.py           # RAGAS faithfulness / relevancy / precision scoring
  tune.py               # hyperparameter tuning — runs benchmark queries and logs results
run_all.py              # ingest and/or tune all chunk_size × chunk_overlap combinations
parse_logs.py           # aggregate logs/ into tune_comparison.md
plot_logs.py            # render faithfulness / relevancy / precision heatmaps from logs/
logs/                   # timestamped JSON-lines tune logs (created by run_all.py)
```

## Setup

```bash
# minimum — HuggingFace embedder + whichever LLM provider you use
uv sync --extra hf --extra ollama        # Ollama (local)
uv sync --extra hf --extra openai        # OpenAI
uv sync --extra hf --extra anthropic     # Anthropic
```

Add `--extra ragas` to enable RAGAS faithfulness scoring (`eval_enabled = true` in `rag.toml`).

`--extra hf` installs the HuggingFace sentence-transformers embedder.  
Ollama must be running locally when using the `ollama` provider.

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

## Hyperparameter tuning

Edit `CHUNK_SIZES` and `CHUNK_OVERLAPS` at the top of `run_all.py`, then run:

```bash
uv run python run_all.py          # ingest all combinations, then tune each one
uv run python run_all.py ingest   # ingest only (skips existing collections)
uv run python run_all.py tune     # tune only (collections must already exist)
```

Tune logs are written to `logs/` as JSON-lines files. Summarise and compare:

```bash
uv run python parse_logs.py   # writes tune_comparison.md
uv run python plot_logs.py    # writes faithfulness/answer_relevancy/context_precision heatmaps (PNG)
```
