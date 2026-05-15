"""CLI entry point for the LangChain RAG implementation.

    python -m rag ingest path/to/file.pdf [dir/ ...]
    python -m rag query "What is X?"
    python -m rag query "What is X?" --stream
    python -m rag eval
    python -m rag eval --fast
    python -m rag serve

The pipeline's LLM is already a LangChain ChatModel, so it can be used
directly as the ragas judge.
"""

import argparse
import logging
import os
import sys

from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(
    level=logging.WARNING,
    format="%(levelname)s  %(name)s  %(message)s",
)
logging.getLogger("rag").setLevel(logging.INFO)


def cmd_ingest(args) -> None:
    from rag.config import load_config
    from rag.pipeline import create_pipeline
    from rag.loaders import SUPPORTED

    cfg = load_config()
    pipeline = create_pipeline(cfg)

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
    from rag.pipeline import create_pipeline

    cfg = load_config()
    pipeline = create_pipeline(cfg)

    if args.stream:
        for token in pipeline.stream(args.question, k=cfg.top_k):
            print(token, end="", flush=True)
        print()
    else:
        print(pipeline.query(args.question, k=cfg.top_k))


def cmd_serve(args) -> None:
    from rag.web import run
    run(host=args.host, port=args.port)


def cmd_eval(args) -> None:
    from rag.config import load_config
    from rag.pipeline import create_pipeline
    from rag.eval.dataset import EVAL_DATASET
    from rag.eval.harness import run_pipeline_evaluation
    from rag.eval.metrics import print_eval_summary, score_with_embedding_similarity, score_with_ragas_metrics

    cfg = load_config()
    pipeline = create_pipeline(cfg)

    print(f"Running eval on {len(EVAL_DATASET)} sample(s)…")
    results = run_pipeline_evaluation(pipeline, EVAL_DATASET, k=cfg.top_k)

    if args.fast:
        score_with_embedding_similarity(results, pipeline.embedder)
        print_eval_summary(results)
        return

    # LangChain advantage: pipeline.llm is already a LangChain ChatModel —
    # pass it directly to ragas, no extra judge setup needed.
    try:
        mean_scores = score_with_ragas_metrics(results, langchain_llm=pipeline.llm)
        print_eval_summary(results, mean_scores)
    except ImportError as exc:
        print(f"Warning: {exc}\nFalling back to embedding similarity.")
        score_with_embedding_similarity(results, pipeline.embedder)
        print_eval_summary(results)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="rag",
        description="LangChain RAG pipeline",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_ingest = sub.add_parser("ingest", help="Ingest files or directories")
    p_ingest.add_argument("sources", nargs="+", help="Files or directories to ingest")

    p_query = sub.add_parser("query", help="Query the pipeline")
    p_query.add_argument("question", help="Question to ask")
    p_query.add_argument("--stream", action="store_true", help="Stream tokens")

    p_eval = sub.add_parser("eval", help="Run ragas evaluation")
    p_eval.add_argument("--fast", action="store_true", help="Embedding similarity only")

    p_serve = sub.add_parser("serve", help="Start the web UI")
    p_serve.add_argument("--host", default="127.0.0.1")
    p_serve.add_argument("--port", type=int, default=8000)

    args = parser.parse_args()

    if args.command == "ingest":
        cmd_ingest(args)
    elif args.command == "query":
        cmd_query(args)
    elif args.command == "eval":
        cmd_eval(args)
    elif args.command == "serve":
        cmd_serve(args)


if __name__ == "__main__":
    main()
