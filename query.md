# RAG Pipeline

## Full Pipeline

```mermaid
flowchart TD
    CSV[data_sources.csv]
    DL[downloader.py\nfetch each URL]
    RAW[corpus/raw_data/\n.html · .pdf · .csv]
    INGEST[ingest.py\nload → split → embed → store]
    DB[(ChromaDB\nvector_db/)]
    Q[query.py\nquestion → answer]

    CSV --> DL --> RAW --> INGEST --> DB
    DB --> Q
```

## query.py Internal Flow — Manual Orchestration

```mermaid
flowchart TD
    CFG[load_config\nrag.toml]
    EMB[build_embedder\nHuggingFaceEmbeddings]
    VS[build_vectorstore\nChroma read-only]
    LLM[build_llm\nChatOllama]
    Q([question])
    RET[retrieve_chunks\nsimilarity_search top-k]
    CTX[build_context\njoin chunk text]
    PRM[build_prompt\nPROMPT_TEMPLATE]
    ASK[ask_llm\nllm.invoke]
    RES([answer + sources])

    CFG --> EMB --> VS
    CFG --> LLM
    Q --> RET
    VS --> RET
    RET --> CTX --> PRM
    Q --> PRM
    PRM --> ASK
    LLM --> ASK
    ASK --> RES
```

## query.py Internal Flow — LCEL

```mermaid
flowchart TD
    CFG[load_config\nrag.toml]
    EMB[build_embedder\nHuggingFaceEmbeddings]
    VS[build_vectorstore\nChroma read-only]
    LLM[build_llm\nChatOllama]
    Q([question])

    subgraph build_chain["build_chain() → chain.invoke(question)"]
        PAR["RunnableParallel"]

        subgraph answer_branch["answer branch"]
            direction LR
            RPAR["context: retriever\nquestion: passthrough"]
            PRM[ChatPromptTemplate]
            OL[ChatOllama]
            STR[StrOutputParser]
            RPAR --> PRM --> OL --> STR
        end

        RET2["sources: retriever\ntop-k docs"]
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
