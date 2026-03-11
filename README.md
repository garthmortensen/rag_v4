# rag_v3

## Project Purpose

Repo contains a small RAG framework:
- Ingest documents (`loaders/`)
- Split into chunks (`splitters/`)
- Embed chunks (`embedders/`)
- Store/retrieve vectors (`stores/`)
- Orchestrate retrieval + LLM calls (`core/pipeline.py`)
- Provide provider-specific LLM adapters (`llms/`)

## File Map (important files)
- [rag/__main__.py](rag/__main__.py) — CLI entrypoint
- [rag/config.py](rag/config.py) — config loader & defaults
- [rag/core/pipeline.py](rag/core/pipeline.py) — main pipeline orchestration
- [rag/core/protocols.py](rag/core/protocols.py) — type protocols/interfaces
- [rag/embedders](rag/embedders) — embedder implementations
- [rag/llms](rag/llms) — LLM provider adapters
- [rag/loaders](rag/loaders) — document loaders (pdf, text)
- [rag/splitters](rag/splitters) — chunking logic
- [rag/stores](rag/stores) — vector DB integrations (chroma)

## Architecture Overview

- The entrypoint loads configuration, prepares the pipeline, and executes ingestion or query flows.
- Each subsystem provides a small interface (protocols) so components are swappable.

## Class Diagram (Mermaid)

```mermaid
classDiagram
    class Pipeline {
        +run_ingest(path)
        +run_query(query)
    }
    class Loader {
        +load(path) List<Document>
    }
    class Splitter {
        +split(Document) List<Chunk>
    }
    class Embedder {
        +embed(List<Chunk>) List<Vector>
    }
    class Store {
        +add(List<Vector>)
        +query(Vector, top_k) List<Chunk>
    }
    class LLM {
        +generate(prompt, **kwargs) Response
    }

    Pipeline --> Loader : uses
    Pipeline --> Splitter : uses
    Pipeline --> Embedder : uses
    Pipeline --> Store : uses
    Pipeline --> LLM : uses

    Loader <|-- rag.loaders.pdf.PDFLoader
    Loader <|-- rag.loaders.text.TextLoader
    Splitter <|-- rag.splitters.recursive.RecursiveSplitter
    Embedder <|-- rag.embedders.huggingface.HFEmbedder
    Embedder <|-- rag.embedders.ollama.OllamaEmbedder
    Store <|-- rag.stores.chroma.ChromaStore
    LLM <|-- rag.llms.ollama.Ollama
    LLM <|-- rag.llms.openai.OpenAI
```

## Pipeline Flowchart (Mermaid)

```mermaid
flowchart TD
  A[Start] --> B[Load Documents]
  B --> C[Split into Chunks]
  C --> D[Create Embeddings]
  D --> E[Store in Vector DB]
  E --> F[Client Query]
  F --> G[Retrieve top_k Chunks]
  G --> H[Construct LLM Prompt]
  H --> I[LLM Generate Answer]
  I --> J[Return Answer]
```

## Sequence Diagram: Query

```mermaid
sequenceDiagram
  participant Client
  participant Pipeline
  participant Store
  participant LLM

  Client->>Pipeline: query(q)
  Pipeline->>Store: search(q_embedding, top_k)
  Store-->>Pipeline: top_k chunks
  Pipeline->>LLM: generate(prompt_with_chunks)
  LLM-->>Pipeline: answer
  Pipeline-->>Client: answer
```

## Config Example (nested TOML)

The project uses `rag.toml` with nested tables. Example structure produced in this repo:

```toml
[rag.chunking]
chunk_size = 1000
chunk_overlap = 100

[rag.storage]
collection_name = "rag_docs"
vector_db_dir = "corpus/vector_db"

[rag.embedder]
type = "huggingface"
model = "all-MiniLM-L6-v2"

[rag.llm]
provider = "ollama"
model = "llama3.2:3b"
temperature = 0.1

[rag.retrieval]
top_k = 5

[rag.infrastructure]
ollama_host = "http://localhost:11434"
```

## Quickstart

1. Create a virtualenv and install (editable):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

2. Run tests:

```bash
pytest -q
```

3. Run CLI (example):

```bash
python -m rag --help
# or run an ingest
python -m rag ingest /path/to/docs
# or query
python -m rag query "What is ...?"
```

## How to read the code

- Start at [rag/__main__.py](rag/__main__.py) to see CLI wiring.
- Inspect [rag/core/pipeline.py](rag/core/pipeline.py) for the main high-level flow.
- Look at [rag/core/protocols.py](rag/core/protocols.py) to understand interfaces you can implement.

