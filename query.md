# RAG Pipeline

## Full Pipeline

```mermaid
flowchart TD
    CSV[data_sources.csv]
    DL["downloader.py<br/>fetch each URL"]
    RAW["corpus/raw_data/<br/>.html · .pdf · .csv"]
    INGEST["ingest.py<br/>load → split → embed → store"]
    DB[("ChromaDB<br/>vector_db/")]
    Q["query.py<br/>question → answer"]

    CSV --> DL --> RAW --> INGEST --> DB
    DB --> Q
```

## Generalized lifecycle

### Ingest

```
documents
↓
chunking
↓
embedding model
↓
vectors
↓
stored in Chroma

```

### query

```
question
↓
same embedding model
↓
query vector
↓
nearest chunks from Chroma
↓
LLM prompt
↓
answer
```

## query.py Internal Flow — LCEL

```mermaid
flowchart TD
    CFG["load_config<br/>rag.toml"]
    EMB["build_embedder<br/>HuggingFaceEmbeddings"]
    VS["build_vectorstore<br/>Chroma read-only"]
    LLM["build_llm<br/>ChatOllama / ChatOpenAI / ChatAnthropic"]
    Q([question])

    subgraph build_chain["build_chain() → chain.invoke(question)"]
        PAR["RunnableParallel"]

        subgraph answer_branch["answer branch"]
            direction LR
            RPAR["context: retriever<br/>question: passthrough"]
            PRM[ChatPromptTemplate]
            OL[LLM]
            STR[StrOutputParser]
            RPAR --> PRM --> OL --> STR
        end

        RET2["sources: retriever<br/>top-k docs"]
    end

    ANS([answer: str])
    SRC([sources: list])

    CFG --> EMB --> VS
    CFG --> LLM
    VS --> build_chain
    LLM --> build_chain
    Q --> PAR
    PAR --> answer_branch
    PAR --> RET2
    STR --> ANS
    RET2 --> SRC
```

## Huge thing

The embedding model quality often matters MORE than the LLM for RAG quality.

Bad retrieval = bad answers.

Watch for:

- bad chunking
- weak embeddings
- wrong top-k
- noisy documents
- overlap settings
- retrieval strategy
