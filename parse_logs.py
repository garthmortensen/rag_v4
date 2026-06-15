"""Parse all logs/*.log tune run JSON-lines files and produce tuning_results.md."""

import csv
import json
from pathlib import Path

LOG_DIR = Path(__file__).parent / "logs"
RESULTS_DIR = Path(__file__).parent / "results"
OUTPUT = RESULTS_DIR / "tuning_results.md"
CSV_OUTPUT = RESULTS_DIR / "tuning_results.csv"


def parse_log(path):
    """Return {collection, queries, complete} from a JSON-lines log file.

    Each query dict has keys: query_num, question, answer, sources,
    faithfulness, answer_relevancy, context_precision, context_recall,
    answer_correctness, noise_sensitivity.
    complete is True only when a run_summary event is present (run finished without crashing).

    If a companion _metrics.csv exists (written by tune.py), numeric scores are
    loaded from it and merged in; the JSON log is used only for question/answer text.
    """
    _SCORE_KEYS = [
        "faithfulness", "answer_relevancy", "context_precision",
        "context_recall", "answer_correctness", "noise_sensitivity",
    ]
    collection = path.stem
    queries = []
    complete = False
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
        elif event == "run_summary":
            complete = True

    # Overlay numeric scores from companion CSV if present.
    csv_path = path.with_name(path.stem + "_metrics.csv")
    if csv_path.exists():
        q_map = {q["query_num"]: q for q in queries}
        with csv_path.open(newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                num = int(row["query_num"])
                scores = {k: (float(row[k]) if row.get(k) else None) for k in _SCORE_KEYS}
                if num in q_map:
                    q_map[num].update(scores)
                else:
                    # CSV row with no matching log entry — add a minimal stub
                    queries.append({"query_num": num, **scores})
        if not complete:
            # A complete CSV means the run finished even if run_summary is absent
            complete = len([q for q in queries if any(q.get(k) is not None for k in _SCORE_KEYS)]) > 0

    return dict(collection=collection, queries=queries, complete=complete)


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
    header_cols.append("**CR Mean**")
    header_cols.append("**AC Mean**")
    header_cols.append("**NS Mean**")

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
        row.append(f"**{format_score(mean_metric(run['queries'], 'context_recall'))}**")
        row.append(f"**{format_score(mean_metric(run['queries'], 'answer_correctness'))}**")
        row.append(f"**{format_score(mean_metric(run['queries'], 'noise_sensitivity'))}**")
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
            cr_label = format_score(q.get("context_recall"))
            ac_label = format_score(q.get("answer_correctness"))
            ns_label = format_score(q.get("noise_sensitivity"))
            lines.append(f"### {rank}. `{collection}` \u2014 F: {f_label} | AR: {ar_label} | CP: {cp_label} | CR: {cr_label} | AC: {ac_label} | NS: {ns_label}\n")
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
    skipped = 0
    for f in log_files:
        parsed = parse_log(f)
        if parsed["queries"] and parsed["complete"]:
            runs.append(parsed)
        elif parsed["queries"] and not parsed["complete"]:
            skipped += 1
            print(f"Skipping incomplete run (no run_summary): {f.name}  ({len(parsed['queries'])} queries logged before crash)")

    if not runs:
        print("No parseable JSON-lines log files found. Re-run rag.tune to generate new logs.")
        return

    runs_sorted = sorted(
        runs,
        key=lambda r: sort_key_faithfulness_desc(mean_metric(r["queries"], "faithfulness")),
    )

    all_q_nums, question_texts = collect_query_metadata(runs)

    RESULTS_DIR.mkdir(exist_ok=True)

    lines = []
    lines.append("# RAG Tuning Results\n")
    lines.append(f"Generated from {len(runs)} log files in `logs/`.\n")

    lines.append("## Summary Table\n")
    lines.append("> - **Faithfulness (F)**: Measures whether every claim in the generated answer is supported by the retrieved context. The judge LLM extracts atomic statements from the answer and verifies each one against the chunks. A score of 1.0 means nothing was hallucinated; 0.0 means the answer is entirely unsupported. Low faithfulness usually signals the LLM is drawing on parametric knowledge instead of the retrieved documents. *Example: if the answer states \"the stress test threshold is 4.5%\" but no retrieved chunk mentions that figure, that claim is unfaithful and lowers the score.*")
    lines.append("> - **Answer Relevancy (AR)**: Measures how directly the answer addresses the question — penalising vague, incomplete, or off-topic responses. It works by prompting the LLM to generate several questions that the answer could plausibly answer, then computing the average cosine similarity of those synthetic questions back to the original. High AR means the answer is focused and on-point; low AR means it drifted or hedged excessively. *Example: if the question asks \"what is the purpose of stress testing?\" and the answer spends most of its content describing who conducts stress tests rather than why, the synthetic questions generated from it will not closely match the original, pulling AR down.*")
    lines.append("> - **Context Precision (CP)**: Measures whether the most relevant chunks appear near the top of the retrieved set. The judge LLM decides for each chunk whether it actually contributed to answering the question, then computes a precision-at-k style score that rewards relevant chunks ranked early and penalises relevant chunks buried at the bottom. Low CP suggests the retriever is returning a lot of noise before the useful material. *Example: if the single chunk that contains the answer is ranked 9th out of 10, CP will be low even though the answer was technically reachable — a better embedding or smaller chunk size would surface it earlier.*")
    lines.append("> - **Context Recall (CR)**: What fraction of the reference answer's claims are supported by the retrieved context. High recall means the retriever found all the content needed to answer correctly. Only computed for queries with a ground-truth reference (`n/a` for no-reference queries).")
    lines.append("> - **Answer Correctness (AC)**: How closely the generated answer matches the reference, combining factual claim overlap (NLI) with semantic similarity. Only computed for ref queries.")
    lines.append("> - **Noise Sensitivity (NS)**: How often the LLM produces incorrect claims even when relevant context was retrieved. Lower is better. Only computed for ref queries.")
    lines.append("> ")
    lines.append("> Collections sorted by F mean (descending). `n/a` = eval disabled, scoring failed, or no reference available.\n")

    table_lines = build_summary_table(runs_sorted, all_q_nums)
    lines.extend(table_lines)
    lines.append("")
    lines.append("---\n")

    per_q_lines = build_per_question_sections(runs, all_q_nums, question_texts)
    lines.extend(per_q_lines)

    OUTPUT.write_text("\n".join(lines))
    print(f"Written: {OUTPUT}")
    print(f"  {len(runs)} collections × {len(all_q_nums)} questions  ({skipped} incomplete runs skipped)")

    metrics = ["faithfulness", "answer_relevancy", "context_precision", "context_recall", "answer_correctness", "noise_sensitivity"]
    csv_header = ["collection"] + [f"{m}_mean" for m in metrics] + [f"q{n}_faithfulness" for n in all_q_nums]
    with CSV_OUTPUT.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(csv_header)
        for run in runs_sorted:
            q_map = build_query_map(run)
            row = [run["collection"]]
            for m in metrics:
                v = mean_metric(run["queries"], m)
                row.append(v if v is not None else "")
            for n in all_q_nums:
                q = q_map.get(n)
                row.append(q["faithfulness"] if q and q.get("faithfulness") is not None else "")
            writer.writerow(row)
    print(f"Written: {CSV_OUTPUT}")


if __name__ == "__main__":
    main()
