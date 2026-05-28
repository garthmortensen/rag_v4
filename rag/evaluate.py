"""RAGAS Faithfulness scoring — LiteLLM judge.

Faithfulness measures what fraction of claims in the answer are supported
by the retrieved context. Score is 0–1; 1.0 means fully grounded.

The judge LLM routes through LiteLLM. Supported providers:
  ollama    — local, air-gapped (localhost:11434)
  openai    — requires OPENAI_API_KEY in .env
  anthropic — requires ANTHROPIC_API_KEY in .env

Two calls are made per evaluation:
  1. Claim extraction  — LLM breaks the answer into atomic statements
  2. Verification      — LLM checks each claim against the retrieved context
"""

import logging
import math
import os

# Silence LiteLLM's AWS/botocore pre-load warnings before the import triggers them.
os.environ.setdefault("LITELLM_LOG", "ERROR")
logging.getLogger("LiteLLM").setLevel(logging.ERROR)

import litellm
from ragas.llms import llm_factory
from ragas.metrics.collections import Faithfulness

litellm.suppress_debug_info = True

logger = logging.getLogger(__name__)


def build_scorer(cfg):
    eval_model = cfg.eval_model or cfg.llm_model
    if not cfg.eval_model:
        logger.warning(
            "No [rag.evaluation] model configured; falling back to %s. "
            "Small models often fail structured-output scoring — set a capable model "
            "under [rag.evaluation] in rag.toml for reliable results.",
            eval_model,
        )
    litellm_model = f"{cfg.eval_provider}/{eval_model}"
    llm = llm_factory(litellm_model, provider="litellm", client=litellm.acompletion)
    return Faithfulness(llm=llm)


def score(question, result, scorer):
    contexts = [doc.page_content for doc in result["sources"]]
    try:
        val = scorer.score(
            user_input=question,
            response=result["answer"],
            retrieved_contexts=contexts,
        ).value
        if val is None or (isinstance(val, float) and math.isnan(val)):
            return None
        return val
    except Exception as exc:
        logger.warning("RAGAS scoring failed (%s: %s); skipping quality score.", type(exc).__name__, exc)
        return None


def print_scores(faithfulness):
    if faithfulness is None:
        print("Quality:  faithfulness n/a  (scoring failed — use a larger eval model)")
        return
    filled = int(round(faithfulness * 10))
    bar = "█" * filled + "░" * (10 - filled)
    print(f"Quality:  faithfulness {faithfulness:.2f}  [{bar}]")
    print("          (1.0 = every claim in the answer is grounded in retrieved context)")
