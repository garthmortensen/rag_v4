"""Eval harness — runs a RAGPipeline against a list of EvalSamples.

Completely decoupled from ragas: just collects (question, answer, contexts)
triples that the metrics layer can then score however it likes.

Usage::

    from rag.eval.harness import run_eval
    from rag.eval.dataset import EVAL_DATASET

    results = run_eval(pipeline, EVAL_DATASET)
"""

import logging

from rag.core.pipeline import RAGPipeline
from rag.eval.types import EvalResult, EvalSample

logger = logging.getLogger(__name__)


def run_eval(
    pipeline: RAGPipeline,
    samples: list[EvalSample],
    k: int | None = None,
) -> list[EvalResult]:
    """Run the pipeline for each sample, collect answers and contexts.

    Parameters
    ----------
    pipeline : RAGPipeline
        Fully-configured pipeline to evaluate.
    samples : list[EvalSample]
        Ground-truth Q&A pairs.
    k : int | None
        Number of chunks to retrieve. Defaults to pipeline's configured top_k
        (falls back to 5 if not available).

    Returns
    -------
    list[EvalResult]
        One result per sample, in the same order as *samples*.
        No scores are populated — call a metrics function next.
    """
    if k is None:
        k = getattr(pipeline, "_top_k", 5)

    results: list[EvalResult] = []
    for i, sample in enumerate(samples, 1):
        logger.info("Eval %d/%d: %r", i, len(samples), sample.question[:60])
        try:
            search_results = pipeline.search(sample.question, k=k)
            contexts = [r.chunk.text for r in search_results]
            answer = pipeline.query(sample.question, k=k)
        except Exception as exc:
            logger.warning("Pipeline failed on sample %d: %s", i, exc)
            contexts = []
            answer = f"[error: {exc}]"

        results.append(
            EvalResult(sample=sample, answer=answer, contexts=contexts)
        )

    return results
