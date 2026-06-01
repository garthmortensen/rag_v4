"""Parse all logs/*.log tune run JSON-lines files and produce tune_comparison.md."""

import json
from pathlib import Path

LOG_DIR = Path(__file__).parent / "logs"
OUTPUT = Path(__file__).parent / "tune_comparison.md"


def parse_log(path):
    """Return {collection, queries} from a JSON-lines log file.

    Each query dict has keys: query_num, question, answer, sources,
    faithfulness, answer_relevancy, context_precision.
    """
    collection = path.stem
    queries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue  # skip non-JSON lines (e.g. old-format logs)
        event = entry.get("event")
        if event == "run_start":
            collection = entry.get("collection", path.stem)
        elif event == "query_result":
            queries.append(entry)
    return dict(collection=collection, queries=queries)


def mean_metric(queries, key):
    vals = []
    for q in queries:
        v = q.get(key)
        if v is not None:
            vals.append(v)
    return sum(vals) / len(vals) if vals else None


def format_score(v):
    if v is None:
        return "n/a"
    return f"{v:.4f}"


def sort_key_faithfulness_desc(v):
    """Sort key for descending faithfulness: real values first (high→low), None last."""
    if v is None:
        return (1, 0.0)
    return (0, -v)


def build_query_map(run):
    """Return {query_num: query_dict} for fast lookup within a single run."""
    q_map = {}
    for q in run["queries"]:
        q_map[q["query_num"]] = q
    return q_map


def collect_query_metadata(runs):
    """Return (sorted_query_nums, {query_num: question_text}) from all runs in one pass."""
    nums = set()
    texts = {}
    for run in runs:
        for q in run["queries"]:
            num = q["query_num"]
            nums.add(num)
            if num not in texts and q.get("question"):
                texts[num] = q["question"]
    return sorted(nums), texts


def build_summary_table(runs_sorted, all_q_nums):
    header_cols = ["Collection"]
    for n in all_q_nums:
        header_cols.append(f"Q{n}")
    header_cols.append("**F Mean**")
    header_cols.append("**AR Mean**")
    header_cols.append("**CP Mean**")

    lines = []
    lines.append("| " + " | ".join(header_cols) + " |")
    lines.append("| " + " | ".join(["---"] * len(header_cols)) + " |")

    for run in runs_sorted:
        q_map = build_query_map(run)
        row = [f"`{run['collection']}`"]
        for n in all_q_nums:
            q = q_map.get(n)
            row.append(format_score(q["faithfulness"]) if q else "—")
        row.append(f"**{format_score(mean_metric(run['queries'], 'faithfulness'))}**")
        row.append(f"**{format_score(mean_metric(run['queries'], 'answer_relevancy'))}**")
        row.append(f"**{format_score(mean_metric(run['queries'], 'context_precision'))}**")
        lines.append("| " + " | ".join(row) + " |")

    return lines


def build_per_question_sections(runs, all_q_nums, question_texts):
    lines = []
    for q_num in all_q_nums:
        q_text = question_texts.get(q_num, f"Question {q_num}")
        lines.append(f"## Question {q_num}: {q_text}\n")

        entries = []
        for run in runs:
            q_map = build_query_map(run)
            if q_num in q_map:
                entries.append((run["collection"], q_map[q_num]))

        entries.sort(key=lambda x: sort_key_faithfulness_desc(x[1].get("faithfulness")))

        for rank, (collection, q) in enumerate(entries, 1):
            f_label  = format_score(q.get("faithfulness"))
            ar_label = format_score(q.get("answer_relevancy"))
            cp_label = format_score(q.get("context_precision"))
            lines.append(f"### {rank}. `{collection}` \u2014 F: {f_label} | AR: {ar_label} | CP: {cp_label}\n")
            lines.append(q.get("answer") or "*No answer recorded.*")
            lines.append("")

        lines.append("---\n")

    return lines


def main():
    log_files = sorted(LOG_DIR.glob("*.log"))
    if not log_files:
        print("No .log files found in logs/")
        return

    runs = []
    for f in log_files:
        parsed = parse_log(f)
        if parsed["queries"]:
            runs.append(parsed)

    if not runs:
        print("No parseable JSON-lines log files found. Re-run rag.tune to generate new logs.")
        return

    runs_sorted = sorted(
        runs,
        key=lambda r: sort_key_faithfulness_desc(mean_metric(r["queries"], "faithfulness")),
    )

    all_q_nums, question_texts = collect_query_metadata(runs)

    lines = []
    lines.append("# RAG Hyperparameter Tune Comparison\n")
    lines.append(f"Generated from {len(runs)} log files in `logs/`.\n")

    lines.append("## Summary Table\n")
    lines.append("> - **Faithfulness (F)**: Measures whether every claim in the generated answer is supported by the retrieved context. The judge LLM extracts atomic statements from the answer and verifies each one against the chunks. A score of 1.0 means nothing was hallucinated; 0.0 means the answer is entirely unsupported. Low faithfulness usually signals the LLM is drawing on parametric knowledge instead of the retrieved documents. *Example: if the answer states \"the stress test threshold is 4.5%\" but no retrieved chunk mentions that figure, that claim is unfaithful and lowers the score.*")
    lines.append("> - **Answer Relevancy (AR)**: Measures how directly the answer addresses the question — penalising vague, incomplete, or off-topic responses. It works by prompting the LLM to generate several questions that the answer could plausibly answer, then computing the average cosine similarity of those synthetic questions back to the original. High AR means the answer is focused and on-point; low AR means it drifted or hedged excessively. *Example: if the question asks \"what is the purpose of stress testing?\" and the answer spends most of its content describing who conducts stress tests rather than why, the synthetic questions generated from it will not closely match the original, pulling AR down.*")
    lines.append("> - **Context Precision (CP)**: Measures whether the most relevant chunks appear near the top of the retrieved set. The judge LLM decides for each chunk whether it actually contributed to answering the question, then computes a precision-at-k style score that rewards relevant chunks ranked early and penalises relevant chunks buried at the bottom. Low CP suggests the retriever is returning a lot of noise before the useful material. *Example: if the single chunk that contains the answer is ranked 9th out of 10, CP will be low even though the answer was technically reachable — a better embedding or smaller chunk size would surface it earlier.*")
    lines.append("> ")
    lines.append("> Collections sorted by F mean (descending). `n/a` = eval disabled or scoring failed.\n")

    table_lines = build_summary_table(runs_sorted, all_q_nums)
    lines.extend(table_lines)
    lines.append("")
    lines.append("---\n")

    per_q_lines = build_per_question_sections(runs, all_q_nums, question_texts)
    lines.extend(per_q_lines)

    OUTPUT.write_text("\n".join(lines))
    print(f"Written: {OUTPUT}")
    print(f"  {len(runs)} collections × {len(all_q_nums)} questions")


if __name__ == "__main__":
    main()
