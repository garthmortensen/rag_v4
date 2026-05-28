"""Hyperparameter tuning helper.

Runs a fixed set of 10 benchmark queries against the current rag.toml config,
scores each answer for faithfulness, and writes a timestamped log so you can
compare runs with different chunk_size / chunk_overlap / top_k / temperature.

Workflow
--------
1. Edit rag.toml (chunk_size, chunk_overlap, top_k, temperature, …).
2. Re-ingest if you changed chunk_size or chunk_overlap::

       python -m rag.ingest

3. Run this script::

       python -m rag.tune

4. Inspect logs/tune_YYYYMMDD_HHMMSS.log.

Usage::

    python -m rag.tune
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from statistics import mean

os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
os.environ.setdefault("HF_HUB_VERBOSITY", "error")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")

logging.getLogger("sentence_transformers").setLevel(logging.ERROR)

from rag.config import load_config
from rag.evaluate import build_scorer
from rag.evaluate import score as ragas_score
from rag.query import build_chain, build_embedder, build_llm, build_vectorstore

# ---------------------------------------------------------------------------
# Benchmark queries — edit these to match your corpus
# ---------------------------------------------------------------------------
QUERIES = [
    "What changes to model disclosure were proposed in the stress test transparency rule?",  # extremely general
    "How did stress testing start, and how has it evolved?",  # general_stress_testing_101_pdf.pdf
    "How does the Projections Calculator handle missing values in regulatory reports?",  # proposed_stress_test_model_documentation_aggregation_models.pdf
    "In the first lien model, how are 2008 and after vintages are combined",  # proposed_stress_test_model_documentation_credit_risk_models.pdf pg 182
    "Tell me about how quickly first lien model can transition current loans to default",  # proposed_stress_test_model_documentation_credit_risk_models.pdf pg 151
    "What studies and academic literature does the first lien model draw on?",  # proposed_stress_test_model_documentation_credit_risk_models.pdf pg 146, for instance
    "How does the home equity model leverage the zillow price database?",  # it does not. hallucination test
    "What did Alan Greenspan say about the stress test reform announcement?",  # he said nothing. hallucination test
    "What did Chair Powell say about the stress test reform announcement?",
    "What is the purpose of the Dodd-Frank Act stress tests and who must participate?",
    "What criticisms did the BPI raise about the Fed's stress test methodology?",
]

LOG_DIR = Path(__file__).resolve().parents[1] / "logs"


def _hyperparams_block(cfg):
    lines = [
        "[Hyperparameters]",
        f"  chunk_size    = {cfg.chunk_size}",
        f"  chunk_overlap = {cfg.chunk_overlap}",
        f"  top_k         = {cfg.top_k}",
        f"  temperature   = {cfg.llm_temperature}",
        f"  llm_provider  = {cfg.llm_provider}",
        f"  llm_model     = {cfg.llm_model}",
        f"  embedder      = {cfg.embedder_model}",
        f"  eval_enabled  = {cfg.eval_enabled}",
        f"  eval_provider = {cfg.eval_provider}",
        f"  eval_model    = {cfg.eval_model or '(inherits llm_model)'}",
    ]
    return "\n".join(lines)


def run():
    cfg = load_config()

    LOG_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = LOG_DIR / f"tune_{timestamp}.log"

    scorer = build_scorer(cfg) if cfg.eval_enabled else None

    print("Building pipeline…")
    embedder = build_embedder(cfg)
    vectorstore = build_vectorstore(cfg, embedder)
    llm = build_llm(cfg)
    chain = build_chain(vectorstore, llm, cfg.top_k)

    header = (
        f"=== RAG Hyperparameter Tune Run ===\n"
        f"Timestamp : {datetime.now().isoformat(timespec='seconds')}\n\n"
        f"{_hyperparams_block(cfg)}\n"
        f"{'=' * 60}\n"
    )
    print(header)

    sections = [header, ]
    faithfulness_scores = []

    for i, question in enumerate(QUERIES, 1):
        print(f"[{i}/{len(QUERIES)}] {question}")
        result = chain.invoke(question)
        answer = result["answer"]

        faith = ragas_score(question, result, scorer) if scorer else None
        if faith is not None:
            faithfulness_scores.append(faith)

        faith_str = f"{faith:.4f}" if faith is not None else "n/a (eval disabled or scoring failed)"

        citation_lines = []
        for j, chunk in enumerate(result["sources"], 1):
            source = chunk.metadata.get("source", "unknown")
            page = chunk.metadata.get("page")
            citation = f"  [{j}] {Path(source).name}"
            if page is not None:
                citation += f"  (page {page})"
            citation_lines.append(citation)
        citations = "\n".join(citation_lines)

        block = (
            f"\n--- Query {i} of {len(QUERIES)} ---\n"
            f"Q: {question}\n\n"
            f"A: {answer}\n\n"
            f"Sources ({len(result['sources'])} chunks):\n{citations}\n\n"
            f"Faithfulness: {faith_str}\n"
        )
        print(block)
        sections.append(block)

    # Summary
    if faithfulness_scores:
        avg = mean(faithfulness_scores)
        scored = len(faithfulness_scores)
        summary = (
            f"\n{'=' * 60}\n"
            f"[Summary]\n"
            f"  Queries run          : {len(QUERIES)}\n"
            f"  Queries scored       : {scored}\n"
            f"  Mean faithfulness    : {avg:.4f}\n"
            f"  Min  faithfulness    : {min(faithfulness_scores):.4f}\n"
            f"  Max  faithfulness    : {max(faithfulness_scores):.4f}\n"
        )
    else:
        summary = (
            f"\n{'=' * 60}\n"
            f"[Summary]\n"
            f"  Queries run          : {len(QUERIES)}\n"
            f"  Faithfulness scoring : disabled\n"
        )

    print(summary)
    sections.append(summary)

    log_path.write_text("".join(sections), encoding="utf-8")
    print(f"\nLog written → {log_path}")


if __name__ == "__main__":
    run()
