"""Benchmark each stage of the query pipeline.

Usage::

    python -m rag.benchmark
    python -m rag.benchmark "your question here"
"""

import sys
import time

from rag.config import load_config
from rag.query import build_chain, build_embedder, build_llm, build_vectorstore

_DEFAULT_QUESTION = "What are the stress test transparency changes?"


def run(question: str) -> None:
    cfg = load_config()
    t = time.perf_counter
    print(f"Question: {question!r}\n")

    t0 = t()
    embedder = build_embedder(cfg)
    print(f"[1] Embedder load  {t()-t0:.2f}s   ({cfg.embedder_model})")

    t0 = t()
    vectorstore = build_vectorstore(cfg, embedder)
    retriever = vectorstore.as_retriever(search_kwargs={"k": cfg.top_k})
    llm = build_llm(cfg)
    chain = build_chain(vectorstore, llm, cfg.top_k)
    print(f"[2] Chain setup    {t()-t0:.2f}s   ({cfg.llm_provider}/{cfg.llm_model})")

    t0 = t()
    docs = retriever.invoke(question)
    print(f"[3] Retrieval      {t()-t0:.3f}s  ({len(docs)} chunks)")

    t0 = t()
    result = chain.invoke(question)
    print(f"[4] LLM + retrieval  {t()-t0:.2f}s")

    print(f"\nAnswer: {result['answer']}")


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else _DEFAULT_QUESTION
    run(question)
