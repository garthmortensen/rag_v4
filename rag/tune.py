"""Hyperparameter tuning helper.

Runs a fixed set of 10 benchmark queries against the current rag.toml config,
scores each answer for faithfulness, and writes a timestamped JSON-lines log so
you can compare runs with different chunk_size / chunk_overlap / top_k / temperature.

Log format: one JSON object per line — events are run_start, query_result, run_summary.
Use parse_logs.py to aggregate logs into tune_comparison.md.

Workflow
--------
1. Edit rag.toml (chunk_size, chunk_overlap, top_k, temperature, …).
2. Re-ingest if you changed chunk_size or chunk_overlap::

       python -m rag.ingest

3. Run this script::

       python -m rag.tune

4. Inspect logs/tune_YYYYMMDD_HHMMSS.log or run parse_logs.py.

Usage::

    python -m rag.tune
"""

import logging
import os
import warnings
from datetime import datetime
from pathlib import Path
from statistics import mean

import structlog

os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
os.environ.setdefault("HF_HUB_VERBOSITY", "error")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")

logging.getLogger("sentence_transformers").setLevel(logging.ERROR)

# RAGAS/LiteLLM leave aiohttp sessions/connectors open after async scoring calls — suppress the noise.
warnings.filterwarnings("ignore", message="Unclosed client session", category=ResourceWarning)
warnings.filterwarnings("ignore", message="Unclosed connector", category=ResourceWarning)

from rag.config import load_config
from rag.evaluate import build_scorers
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


def open_json_log(log_path):
    """Open log_path for writing and configure structlog to emit JSON lines into it.

    Returns (logger, file_handle). Caller must close the file handle when done.
    Reconfigures structlog globally, so call once per tune run.
    """
    log_file = open(log_path, "w", encoding="utf-8")
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.PrintLoggerFactory(file=log_file),
    )
    return structlog.get_logger(), log_file


def format_score_for_print(v):
    if v is None:
        return "n/a (eval disabled or scoring failed)"
    return f"{v:.4f}"


def build_source_list(chunks):
    """Convert LangChain document chunks to a plain list of {name, page?} dicts."""
    sources = []
    for chunk in chunks:
        source = chunk.metadata.get("source", "unknown")
        entry = {"name": Path(source).name}
        page = chunk.metadata.get("page")
        if page is not None:
            entry["page"] = page
        sources.append(entry)
    return sources


def print_run_header(cfg):
    print(f"""\
=== RAG Hyperparameter Tune Run ===
Timestamp : {datetime.now().isoformat(timespec='seconds')}

[Hyperparameters]
  collection    = {cfg.collection_name}
  chunk_size    = {cfg.chunk_size}
  chunk_overlap = {cfg.chunk_overlap}
  top_k         = {cfg.top_k}
  temperature   = {cfg.llm_temperature}
  llm_provider  = {cfg.llm_provider}
  llm_model     = {cfg.llm_model}
  embedder      = {cfg.embedder_model}
  eval_enabled  = {cfg.eval_enabled}
  eval_provider = {cfg.eval_provider}
  eval_model    = {cfg.eval_model or '(inherits llm_model)'}
{'=' * 60}""")


def print_query_result(i, total, question, answer, sources, faith, ar, cp):
    print(f"""
--- Query {i} of {total} ---
Q: {question}

A: {answer}

Sources ({len(sources)} chunks):""")
    for j, source in enumerate(sources, 1):
        line = f"  [{j}] {source['name']}"
        if "page" in source:
            line += f"  (page {source['page']})"
        print(line)
    print(f"""
  Faithfulness     : {format_score_for_print(faith)}
  Answer Relevancy : {format_score_for_print(ar)}
  Context Precision: {format_score_for_print(cp)}""")


def print_run_summary(total_queries, faith_scores, ar_scores, cp_scores):
    def mean_str(vals):
        return f"{mean(vals):.4f}" if vals else "n/a"

    print(f"\n{'=' * 60}")
    print("[Summary]")
    print(f"  Queries run               : {total_queries}")

    any_scored = faith_scores or ar_scores or cp_scores
    if any_scored:
        scored = max(len(faith_scores), len(ar_scores), len(cp_scores))
        print(f"  Queries scored            : {scored}")
        print(f"  Mean faithfulness         : {mean_str(faith_scores)}")
        if faith_scores:
            print(f"  Min  faithfulness         : {min(faith_scores):.4f}")
            print(f"  Max  faithfulness         : {max(faith_scores):.4f}")
        print(f"  Mean answer_relevancy     : {mean_str(ar_scores)}")
        print(f"  Mean context_precision    : {mean_str(cp_scores)}")
    else:
        print("  Faithfulness scoring      : disabled")


def run(cfg=None):
    if cfg is None:
        cfg = load_config()

    LOG_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = LOG_DIR / f"tune_{timestamp}.log"

    scorers = build_scorers(cfg) if cfg.eval_enabled else {}

    print("Building pipeline…")
    embedder = build_embedder(cfg)
    vectorstore = build_vectorstore(cfg, embedder)
    llm = build_llm(cfg)
    chain = build_chain(vectorstore, llm, cfg.top_k)

    log, log_file = open_json_log(log_path)

    try:
        print_run_header(cfg)

        log.info(
            "run_start",
            collection=cfg.collection_name,
            chunk_size=cfg.chunk_size,
            chunk_overlap=cfg.chunk_overlap,
            top_k=cfg.top_k,
            temperature=cfg.llm_temperature,
            llm_provider=cfg.llm_provider,
            llm_model=cfg.llm_model,
            embedder=cfg.embedder_model,
            eval_enabled=cfg.eval_enabled,
            eval_provider=cfg.eval_provider,
            eval_model=cfg.eval_model or cfg.llm_model,
        )

        faith_scores = []
        ar_scores = []
        cp_scores = []

        for i, question in enumerate(QUERIES, 1):
            print(f"[{i}/{len(QUERIES)}] {question}")
            result = chain.invoke(question)
            answer = result["answer"]

            scores = {}
            for name, scorer in scorers.items():
                scores[name] = ragas_score(question, result, scorer)

            faith = scores.get("faithfulness")
            ar    = scores.get("answer_relevancy")
            cp    = scores.get("context_precision")

            if faith is not None:
                faith_scores.append(faith)
            if ar is not None:
                ar_scores.append(ar)
            if cp is not None:
                cp_scores.append(cp)

            sources = build_source_list(result["sources"])
            print_query_result(i, len(QUERIES), question, answer, sources, faith, ar, cp)

            log.info(
                "query_result",
                query_num=i,
                question=question,
                answer=answer,
                sources=sources,
                faithfulness=faith,
                answer_relevancy=ar,
                context_precision=cp,
            )

        mean_faith = mean(faith_scores) if faith_scores else None
        mean_ar    = mean(ar_scores)    if ar_scores    else None
        mean_cp    = mean(cp_scores)    if cp_scores    else None

        log.info(
            "run_summary",
            queries_run=len(QUERIES),
            queries_scored=max(len(faith_scores), len(ar_scores), len(cp_scores), 0),
            mean_faithfulness=mean_faith,
            min_faithfulness=min(faith_scores) if faith_scores else None,
            max_faithfulness=max(faith_scores) if faith_scores else None,
            mean_answer_relevancy=mean_ar,
            mean_context_precision=mean_cp,
        )

        print_run_summary(len(QUERIES), faith_scores, ar_scores, cp_scores)

    finally:
        log_file.close()

    print(f"\nLog written → {log_path}")


if __name__ == "__main__":
    run()
