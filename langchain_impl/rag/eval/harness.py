"""Eval harness — runs the pipeline against a list of test questions.

Uses duck typing so it works with any pipeline exposing
`search(question, k)` and `query(question, k)`.

Usage::

    from rag.eval.harness import run_pipeline_evaluation, EvalSample
    from rag.eval.dataset import EVAL_DATASET

    results = run_pipeline_evaluation(pipeline, EVAL_DATASET)
"""

import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


# ── Data types ────────────────────────────────────────────────────────


@dataclass
class EvalSample:
    """One test case.

    ground_truth is optional — needed for LLMContextRecall and
    FactualCorrectness but not for Faithfulness or ResponseRelevancy.
    """

    question: str
    ground_truth: str = ""


@dataclass
class EvalResult:
    """Pipeline output for one EvalSample, ready for scoring."""

    sample: EvalSample
    answer: str
    contexts: list[str]  # raw chunk texts retrieved
    scores: dict[str, float] = field(default_factory=dict)


# ── Harness ───────────────────────────────────────────────────────────


def run_pipeline_evaluation(pipeline, samples: list[EvalSample], k: int = 5) -> list[EvalResult]:
    """Run the pipeline for each sample, collect answers and retrieved contexts."""
    results: list[EvalResult] = []
    for i, sample in enumerate(samples, 1):
        logger.info("Eval %d/%d: %r", i, len(samples), sample.question[:60])
        try:
            search_results = pipeline.search(sample.question, k=k)
            contexts = [
                r.chunk.text
                for r in search_results
            ]
            answer = pipeline.query(sample.question, k=k)
        except Exception as exc:
            logger.warning("Pipeline failed on sample %d: %s", i, exc)
            contexts = []
            answer = f"[error: {exc}]"

        results.append(EvalResult(sample=sample, answer=answer, contexts=contexts))

    return results
