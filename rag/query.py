"""Answer questions using the ChromaDB vector store and a configured LLM.

Pipeline:
  1. embed the question with the same embedder used during ingest
  2. retrieve top-k matching chunks from ChromaDB
  3. format a prompt: context chunks + question
  4. send the prompt to the LLM
  5. return the answer text and source documents

Design decisions
----------------
Orchestration uses LangChain LCEL (LangChain Expression Language).
build_chain() composes Runnables with the | operator and returns a
RunnableParallel that runs the answer chain and the retriever together,
so a single chain.invoke(question) returns both the answer text and the
source documents.

build_embedder() is intentionally duplicated from ingest.py to keep modules
independent. Both must use the same model name so vectors are compatible.

cfg.embedder selects the provider ("huggingface" or "ollama"); ingest.py and
query.py must stay in sync so query vectors match the ingested vectors.

Supported LLM providers: "ollama", "openai", "anthropic".
build_llm() selects the appropriate LangChain chat model from cfg.llm_provider.

Two calling patterns are supported:
  query(question)          Single-shot. Rebuilds all objects on every call.
                           Useful for scripts and tests.
                           Do NOT call in a loop — the embedder reloads each time.

  python -m rag.query      Interactive REPL. Builds the chain once then loops,
                           avoiding the cost of reloading the embedder on every
                           question.
"""

import logging
import os
from pathlib import Path

# Inference runs entirely locally — text never leaves
# HF Hub only downloads model weights
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")      # disables analytics/usage telemetry
os.environ.setdefault("HF_HUB_VERBOSITY", "error")           # suppresses "unauthenticated requests" warning
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")  # suppresses model-download progress bars
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")     # suppresses transformers key-mismatch warnings

# sentence-transformers prints a "BertModel LOAD REPORT" table via its own logger;
# the TRANSFORMERS_VERBOSITY env var doesn't reach it — silence it directly.
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)

import chromadb
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama

from rag.config import load_config
from rag.ragas_scoring import build_scorer, print_scores, score as ragas_score


PROMPT_TEMPLATE = """\
You are a helpful assistant. Use only the context below to answer the question.
If the context does not contain enough information, say "I don't know."

Context:
{context}

Question: {question}

Answer:"""


def build_embedder(cfg):
    if cfg.embedder == "ollama":
        from langchain_ollama import OllamaEmbeddings
        return OllamaEmbeddings(model=cfg.embedder_model)
    return HuggingFaceEmbeddings(model_name=cfg.embedder_model)


def build_vectorstore(cfg, embedder):
    client = chromadb.PersistentClient(path=cfg.vector_db_dir)
    try:
        count = client.get_collection(cfg.collection_name).count()
        if count == 0:
            import logging
            logging.getLogger(__name__).warning(
                "Collection '%s' exists but is empty — did you forget to run ingest?",
                cfg.collection_name,
            )
    except Exception:
        pass
    return Chroma(
        client=client,
        collection_name=cfg.collection_name,
        embedding_function=embedder,
    )


def build_llm(cfg):
    provider = cfg.llm_provider
    if provider == "ollama":
        return ChatOllama(model=cfg.llm_model, temperature=cfg.llm_temperature)
    if provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=cfg.llm_model, temperature=cfg.llm_temperature)
    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(model=cfg.llm_model, temperature=cfg.llm_temperature)
    raise ValueError(f"Unknown llm provider {provider!r}. Choose: ollama, openai, anthropic")


def build_chain(vectorstore, llm, top_k):
    retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})  # LCEL: vectorstore → Runnable
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)        # LCEL: prompt → Runnable

    def _format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # Retrieve once, then share docs between the answer chain and sources output.
    # Previously the retriever was invoked twice in parallel (once for context, once
    # for sources), which caused concurrent SQLite access and intermittent CANTOPEN errors.
    return (
        RunnableParallel(sources=retriever, question=RunnablePassthrough())
        | RunnablePassthrough.assign(
            answer=RunnableLambda(
                lambda x: prompt.invoke({"context": _format_docs(x["sources"]), "question": x["question"]})
            )
            | llm
            | StrOutputParser()
        )
        | RunnableLambda(lambda x: {"answer": x["answer"], "sources": x["sources"]})
    )


def query(question):
    """Single-shot convenience wrapper. Builds all objects from config on every call.

    Do not call in a loop — the embedder model reloads on every invocation.
    For repeated queries build the chain once and call chain.invoke() directly.
    """
    cfg = load_config()
    embedder = build_embedder(cfg)
    vectorstore = build_vectorstore(cfg, embedder)
    llm = build_llm(cfg)
    chain = build_chain(vectorstore, llm, cfg.top_k)
    return chain.invoke(question)


def _print_result(result, question: str = ""):
    # --- ChromaDB retrieval (printed first so you can audit before reading the answer) ---
    print(f"\nChromaDB query: {question!r}")
    print(f"Retrieved {len(result['sources'])} chunk(s):")
    for i, chunk in enumerate(result["sources"], 1):  # 1-indexed, e.g. [1], [2],
        source = chunk.metadata.get("source", "unknown")  # e.g. "/path/to/credit_risk_models.pdf"
        page = chunk.metadata.get("page")                 # e.g. 196  (only PDF)
        header = f"  [{i}] {Path(source).name}"       # e.g. "  [1] credit_risk_models.pdf"
        if page is not None:
            header += f"  (page {page})"              # e.g. "  [1] credit_risk_models.pdf  (page 196)"
        print(header)

        # All metadata fields — lets you audit exactly what ChromaDB returned
        for key, val in chunk.metadata.items():
            print(f"    {key}: {val}")

        # Full chunk text, untruncated
        print("    --- chunk content ---")
        for line in chunk.page_content.strip().splitlines():
            print(f"    {line}")
        print()

    # --- LLM answer ---
    print("Answer:")
    print(result["answer"])


def main():
    cfg = load_config()
    print("Loading embedder ...")
    embedder = build_embedder(cfg)
    vectorstore = build_vectorstore(cfg, embedder)
    llm = build_llm(cfg)
    print(f"Ready. LLM: {cfg.llm_provider}/{cfg.llm_model}  top_k={cfg.top_k}")
    print("Type 'quit' or 'exit' to stop.\n")

    chain = build_chain(vectorstore, llm, cfg.top_k)
    scorer = build_scorer(cfg) if cfg.eval_enabled else None

    while True:
        question = input("Question: ").strip()
        if question.lower() in ("quit", "exit", "q"):
            break
        if not question:
            continue
        result = chain.invoke(question)
        _print_result(result, question)
        if scorer is not None:
            print_scores(ragas_score(question, result, scorer))
        print()


if __name__ == "__main__":
    main()
