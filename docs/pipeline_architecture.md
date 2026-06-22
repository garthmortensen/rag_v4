# RAG Pipeline

## Full Pipeline

```mermaid
flowchart TD
    CSV[data_sources.csv]
    DL["downloader.py<br/>fetch each URL"]
    RAW["corpus/raw_data/<br/>.html · .pdf"]
    INGEST["ingest.py<br/>load → split → embed → store"]
    DB[("ChromaDB<br/>vector_db/")]
    Q["query.py<br/>question → answer"]

    CSV --> DL --> RAW --> INGEST --> DB
    DB --> Q
```

## Generalized lifecycle

### Ingest

```
documents > chunking > embedding model > vectors > stored in Chroma
```

### query

```
question > same embedding model > query vector > nearest chunks from Chroma > LLM prompt > answer
```

## query.py Internal Flow — LCEL

```mermaid
flowchart TD
    CFG["load_config<br/>rag.toml"]
    EMB["build_embedder<br/>HuggingFace / Ollama"]
    VS["build_vectorstore<br/>Chroma read-only"]
    LLM["build_llm<br/>ChatOllama / ChatOpenAI / ChatAnthropic"]
    Q([question])

    subgraph build_chain["build_chain() → chain.invoke(question)"]
        PAR["RunnableParallel<br/>sources: retriever (top-k)<br/>question: passthrough"]
        ASSIGN["RunnablePassthrough.assign(answer=…)"]

        subgraph answer_branch["answer branch (consumes sources + question)"]
            direction LR
            FMT["_format_docs(sources)<br/>join chunks → context"]
            PRM[ChatPromptTemplate]
            OL[LLM]
            STR[StrOutputParser]
            FMT --> PRM --> OL --> STR
        end

        REPACK["RunnableLambda<br/>{answer, sources}"]

        PAR --> ASSIGN --> answer_branch
        STR --> REPACK
        PAR -. sources reused .-> REPACK
    end

    ANS([answer: str])
    SRC([sources: list])

    CFG --> EMB --> VS
    CFG --> LLM
    VS --> build_chain
    LLM --> build_chain
    Q --> PAR
    REPACK --> ANS
    REPACK --> SRC
```

