"""CLI entry point.

    python -m rag ingest path/to/file.pdf [dir/ ...]
    python -m rag query "What is X?"
    python -m rag query "What is X?" --stream
    python -m rag eval
    python -m rag eval --fast          # embedding similarity only, no LLM judge
    python -m rag eval --provider ollama --model llama3.2:3b
"""

import argparse
import logging
import sys

from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(
    level=logging.WARNING,  # keep third-party noise quiet; pipeline logs at INFO
    format="%(levelname)s  %(name)s  %(message)s",
)
logging.getLogger("rag").setLevel(logging.INFO)


# ── sub-commands ─────────────────────────────────────────────────────


def cmd_ingest(args) -> None:
    import os

    from rag.config import load_config
    from rag.core.pipeline import build_pipeline
    from rag.loaders import SUPPORTED

    cfg = load_config()
    pipeline = build_pipeline(cfg)

    sources: list[str] = []
    for path in args.sources:
        if os.path.isdir(path):
            for root, _, files in os.walk(path):
                for fname in sorted(files):
                    if os.path.splitext(fname)[1].lower() in SUPPORTED:
                        sources.append(os.path.join(root, fname))
        else:
            sources.append(path)

    if not sources:
        print("No supported files found.", file=sys.stderr)
        sys.exit(1)

    count = pipeline.ingest(sources)
    print(f"Ingested {count} chunk(s) from {len(sources)} file(s).")


def cmd_query(args) -> None:
    from rag.config import load_config
    from rag.core.pipeline import build_pipeline

    cfg = load_config()
    pipeline = build_pipeline(cfg)

    if args.stream:
        for token in pipeline.stream(args.question, k=cfg.top_k):
            print(token, end="", flush=True)
        print()
    else:
        print(pipeline.query(args.question, k=cfg.top_k))


def cmd_eval(args) -> None:
    from rag.config import load_config
    from rag.core.pipeline import build_pipeline
    from rag.eval.dataset import EVAL_DATASET
    from rag.eval.harness import run_eval
    from rag.eval.metrics import (
        print_summary,
        score_embedding_similarity,
        score_with_ragas,
    )

    cfg = load_config()
    pipeline = build_pipeline(cfg)

    print(f"Running eval on {len(EVAL_DATASET)} sample(s)…")
    results = run_eval(pipeline, EVAL_DATASET, k=cfg.top_k)

    if args.fast:
        score_embedding_similarity(results, pipeline.embedder)
        print_summary(results)
        return

    # Full ragas scoring — build the judge LLM from CLI args (or config)
    provider = args.provider or cfg.llm_provider
    model = args.model or cfg.llm_model

    try:
        langchain_llm = _make_langchain_llm(provider, model)
        mean_scores = score_with_ragas(results, langchain_llm=langchain_llm)
        print_summary(results, mean_scores)
    except ImportError as exc:
        print(f"Warning: {exc}\nFalling back to embedding similarity.")
        score_embedding_similarity(results, pipeline.embedder)
        print_summary(results)


def _make_langchain_llm(provider: str, model: str):
    """Return a LangChain chat model for use as a ragas judge."""
    if provider == "ollama":
        from langchain_ollama import ChatOllama

        return ChatOllama(model=model)
    if provider == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model=model)
    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(model=model)
    raise ValueError(f"Unknown provider for ragas judge: {provider!r}")


# ── arg parser ───────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="rag",
        description="Lightweight RAG pipeline",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # ingest
    p_ingest = sub.add_parser("ingest", help="Ingest files or directories")
    p_ingest.add_argument("sources", nargs="+", help="Files or directories to ingest")

    # query
    p_query = sub.add_parser("query", help="Query the pipeline")
    p_query.add_argument("question", help="Question to ask")
    p_query.add_argument("--stream", action="store_true", help="Stream the answer token-by-token")

    # eval
    p_eval = sub.add_parser("eval", help="Run ragas evaluation")
    p_eval.add_argument(
        "--fast",
        action="store_true",
        help="Use embedding similarity only (no LLM judge, no ragas required)",
    )
    p_eval.add_argument("--provider", default=None, help="Judge LLM provider (overrides rag.toml)")
    p_eval.add_argument("--model", default=None, help="Judge LLM model (overrides rag.toml)")

    args = parser.parse_args()

    if args.command == "ingest":
        cmd_ingest(args)
    elif args.command == "query":
        cmd_query(args)
    elif args.command == "eval":
        cmd_eval(args)


if __name__ == "__main__":
    main()
