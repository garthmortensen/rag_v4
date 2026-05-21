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

cfg.embedder type field is currently ignored (always HuggingFace), matching
ingest.py behaviour.

Only Ollama is supported as an LLM provider. build_llm() constructs a
ChatOllama instance from cfg.llm_model and cfg.llm_temperature.

Two calling patterns are supported:
  query(question)          Single-shot. Rebuilds all objects on every call.
                           Useful for scripts and tests.
                           Do NOT call in a loop — the embedder reloads each time.

  python -m rag.query      Interactive REPL. Builds the chain once then loops,
                           avoiding the cost of reloading the embedder on every
                           question.
"""

import os
import textwrap
from pathlib import Path

# Inference runs entirely locally — text never leaves
# HF Hub only downloads model weights
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")  # e.g. suppresses model-download progress bars

import chromadb
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama

from rag.config import load_config


PROMPT_TEMPLATE = """\
You are a helpful assistant. Use only the context below to answer the question.
If the context does not contain enough information, say "I don't know."

Context:
{context}

Question: {question}

Answer:"""


def build_embedder(cfg):
    return HuggingFaceEmbeddings(model_name=cfg.embedder_model)


def build_vectorstore(cfg, embedder):
    client = chromadb.PersistentClient(path=cfg.vector_db_dir)
    return Chroma(
        client=client,
        collection_name=cfg.collection_name,
        embedding_function=embedder,
    )


def build_llm(cfg):
    return ChatOllama(model=cfg.llm_model, temperature=cfg.llm_temperature)


def build_chain(vectorstore, llm, top_k):
    retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})  # LCEL: vectorstore → Runnable
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)        # LCEL: prompt → Runnable

    # LCEL: | pipes each step's output into the next.
    # The dict runs retriever + passthrough in parallel to fill {context} and {question}.
    answer_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()  # LCEL: AIMessage → plain string
    )

    # LCEL: runs answer_chain and retriever in parallel → {"answer": str, "sources": list}
    return RunnableParallel(answer=answer_chain, sources=retriever)


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


# dont flood terminal
_PREVIEW_LEN = 400  # e.g. "196 Model Documentation: First Lien Mortgage Model lower interest…"
# Fits in terminal width
_WRAP_WIDTH = 88

def _print_result(result):
    print("\nAnswer:")
    print(result["answer"])
    print("\nSources:")
    for i, chunk in enumerate(result["sources"], 1):  # 1-indexed, e.g. [1], [2],
        source = chunk.metadata.get("source", "unknown")  # e.g. "/path/to/credit_risk_models.pdf"
        page = chunk.metadata.get("page")                 # e.g. 196  (only PDF)
        # modify and join newlines so the text wraps nicely
        content = chunk.page_content.strip().replace("\n", " ")
        truncated = len(content) > _PREVIEW_LEN  # when chunk is longer than preview
        # Append "..." only when we actually cut the text short;
        # avoids a misleading "..." on already-short chunks.
        if truncated:
            preview = content[:_PREVIEW_LEN] + "..."  # e.g. "…lower monthly payment..."
        else:
            preview = content  # short enough to show in full

        # built-in textwrap.fill produces a single string with embedded newlines
        # this allows you to print indented block prints with one print() sans loop
        wrapped = textwrap.fill(
            preview,
            width=_WRAP_WIDTH,
            initial_indent="    ",
            subsequent_indent="    ",
        )
        header = f"  [{i}] {Path(source).name}"       # e.g. "  [1] credit_risk_models.pdf"
        if page is not None:
            header += f"  (page {page})"              # e.g. "  [1] credit_risk_models.pdf  (page 196)"
        print(header)
        print(wrapped)


def main():
    cfg = load_config()
    print("Loading embedder ...")
    embedder = build_embedder(cfg)
    vectorstore = build_vectorstore(cfg, embedder)
    llm = build_llm(cfg)
    print(f"Ready. LLM: {cfg.llm_provider}/{cfg.llm_model}  top_k={cfg.top_k}")
    print("Type 'quit' or 'exit' to stop.\n")

    chain = build_chain(vectorstore, llm, cfg.top_k)

    while True:
        question = input("Question: ").strip()
        if question.lower() in ("quit", "exit", "q"):
            break
        if not question:
            continue
        result = chain.invoke(question)
        _print_result(result)
        print()


if __name__ == "__main__":
    main()
