"""Ground-truth evaluation dataset.

Replace the placeholder entries with domain-specific Q&A pairs.
ground_truth is optional — omit it (or leave empty) if you don't have
reference answers yet. Faithfulness and ResponseRelevancy still work
without it; LLMContextRecall and FactualCorrectness require it.

Usage::

    from rag.eval.dataset import EVAL_DATASET
    results = run_pipeline_evaluation(pipeline, EVAL_DATASET)
"""

from rag.eval.harness import EvalSample

EVAL_DATASET: list[EvalSample] = [
    EvalSample(
        question="What is the main topic of the ingested documents?",
        ground_truth="",  # fill in with the expected answer
    ),
    EvalSample(
        question="Summarize the key findings or conclusions.",
        ground_truth="",
    ),
    # Add more domain-specific samples here.
]
