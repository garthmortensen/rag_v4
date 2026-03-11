"""Eval data types. No external dependencies."""

from dataclasses import dataclass, field


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
