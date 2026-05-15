"""Scoring functions for EvalResult lists.

Two modes:

1. **ragas** (full LLM-as-judge) — requires ``uv sync --extra eval``
   and a LangChain-compatible LLM passed as ``langchain_llm``.
   Metrics: Faithfulness, ResponseRelevancy, LLMContextRecall, FactualCorrectness.

2. **Embedding similarity** (zero LLM calls) — cosine similarity between
   question and answer embeddings. Fast proxy for answer relevancy; suitable
   for CI smoke tests or when a judge LLM isn't available.

Usage::

    # Full ragas scoring (Ollama judge)
    from langchain_ollama import ChatOllama
    from rag.eval.metrics import score_with_ragas_metrics

    scores = score_with_ragas_metrics(results, langchain_llm=ChatOllama(model="llama3.2:3b"))

    # Fast embedding-only scoring
    from rag.eval.metrics import score_with_embedding_similarity

    sims = score_with_embedding_similarity(results, embedder=pipeline.embedder)
"""

import math

from rag.eval.harness import EvalResult


# ── ragas ────────────────────────────────────────────────────────────


def score_with_ragas_metrics(
    results: list[EvalResult],
    langchain_llm=None,
) -> dict[str, float]:
    """Score *results* with ragas LLM-as-judge metrics.

    Parameters
    ----------
    results : list[EvalResult]
        Output of run_pipeline_evaluation().
    langchain_llm : BaseChatModel | None
        Any LangChain chat model to use as the judge.
        Example: ``ChatOllama(model="llama3.2:3b")``
        If None, ragas uses its default (requires OPENAI_API_KEY).

    Returns
    -------
    dict[str, float]
        Mean scores across all samples, keyed by metric name.
        Also populates result.scores on each EvalResult in-place.

    Raises
    ------
    ImportError
        If ragas or langchain-core are not installed.
    """
    try:
        from ragas import EvaluationDataset, SingleTurnSample, evaluate
        from ragas.llms import LangchainLLMWrapper
        from ragas.metrics._answer_relevance import ResponseRelevancy
        from ragas.metrics._context_recall import LLMContextRecall
        from ragas.metrics._factual_correctness import FactualCorrectness
        from ragas.metrics._faithfulness import Faithfulness
    except ImportError:
        raise ImportError(
            "ragas is not installed. Run: uv sync --extra eval\n"
            "You will also need a LangChain provider, e.g.: uv add langchain-ollama"
        )

    judge = LangchainLLMWrapper(langchain_llm) if langchain_llm else None

    has_ground_truth = any(r.sample.ground_truth for r in results)
    metric_classes = [Faithfulness, ResponseRelevancy]
    if has_ground_truth:
        metric_classes += [LLMContextRecall, FactualCorrectness]

    metrics = []
    for cls in metric_classes:
        if judge:
            metrics.append(cls(llm=judge))
        else:
            metrics.append(cls())

    samples = [
        SingleTurnSample(
            user_input=r.sample.question,
            response=r.answer,
            retrieved_contexts=r.contexts,
            reference=r.sample.ground_truth or None,
        )
        for r in results
    ]
    dataset = EvaluationDataset(samples=samples)
    result = evaluate(dataset=dataset, metrics=metrics)
    df = result.to_pandas()

    # Populate per-result scores
    score_cols = [
        c
        for c in df.columns
        if c not in ("user_input", "response", "retrieved_contexts", "reference")
    ]
    for i, eval_result in enumerate(results):
        for col in score_cols:
            try:
                eval_result.scores[col] = float(df.iloc[i][col])
            except (ValueError, TypeError):
                pass

    return {
        col: float(df[col].mean())
        for col in score_cols
    }


# ── Lightweight embedding similarity ─────────────────────────────────


def score_with_embedding_similarity(
    results: list[EvalResult],
    embedder,
) -> list[float]:
    """Cosine similarity between question and answer embeddings.

    A zero-LLM-call proxy for answer relevancy. Useful in CI or when
    you want a quick sanity check without burning API credits.

    Returns one score per result (higher = more relevant answer).
    """
    scores: list[float] = []
    for r in results:
        q_vec = embedder.embed_query(r.sample.question)
        a_vec = embedder.embed_query(r.answer)
        score = _cosine_similarity(q_vec, a_vec)
        r.scores["embedding_similarity"] = score
        scores.append(score)
    return scores


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0


# ── Reporting ────────────────────────────────────────────────────────


def print_eval_summary(
    results: list[EvalResult],
    mean_scores: dict[str, float] | None = None,
) -> None:
    """Print a human-readable eval summary to stdout."""
    bar = "=" * 64
    print(f"\n{bar}")
    print(f"Eval Summary — {len(results)} sample(s)")
    print(bar)

    for i, r in enumerate(results, 1):
        ans_preview = r.answer[:120] + ("…" if len(r.answer) > 120 else "")
        print(f"\n[{i}] Q: {r.sample.question}")
        print(f"     A: {ans_preview}")
        print(f"     Contexts retrieved: {len(r.contexts)}")
        if r.scores:
            scores_str = "  ".join(
                f"{k}={v:.3f}"
                for k, v in r.scores.items()
            )
            print(f"     Scores: {scores_str}")

    if mean_scores:
        print(f"\n{'─' * 40}")
        print("Mean scores:")
        for k, v in mean_scores.items():
            print(f"  {k}: {v:.4f}")

    print(f"{bar}\n")
