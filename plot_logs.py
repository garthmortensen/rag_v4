"""Render heatmaps comparing tune-run metrics across the chunk_size × chunk_overlap grid.

Reads every logs/*.log file produced by run_all.py / rag.tune, extracts the mean
faithfulness, answer_relevancy, and context_precision across all queries in the
run, then writes one PNG per metric to the repo root.

Collection names are expected to look like:
    chunk_size_<SIZE>_chunk_overlap_<OVERLAP>

Logs whose collection name doesn't match that pattern are skipped (with a notice).

Usage:
    python plot_logs.py
"""

import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from parse_logs import mean_metric, parse_log

LOG_DIR = Path(__file__).parent / "logs"
OUTPUT_DIR = Path(__file__).parent

COLLECTION_NAME_RE = re.compile(r"chunk_size_(\d+)_chunk_overlap_(\d+)")

METRICS = [
    ("faithfulness",      "Faithfulness",      "faithfulness_heatmap.png"),
    ("answer_relevancy",  "Answer Relevancy",  "answer_relevancy_heatmap.png"),
    ("context_precision", "Context Precision", "context_precision_heatmap.png"),
]


def collect_runs():
    """Return a list of dicts: {chunk_size, chunk_overlap, queries}."""
    runs = []
    for path in sorted(LOG_DIR.glob("*.log")):
        parsed = parse_log(path)
        if not parsed["queries"]:
            continue

        match = COLLECTION_NAME_RE.search(parsed["collection"])
        if not match:
            print(f"Skipping {path.name}: collection '{parsed['collection']}' is not a chunk_size/overlap grid point.")
            continue

        runs.append({
            "chunk_size":    int(match.group(1)),
            "chunk_overlap": int(match.group(2)),
            "queries":       parsed["queries"],
        })
    return runs


def build_grid(runs, metric_key):
    """Return (sizes, overlaps, grid) where grid[i, j] = mean metric for overlaps[i], sizes[j]."""
    sizes    = sorted({r["chunk_size"]    for r in runs})
    overlaps = sorted({r["chunk_overlap"] for r in runs})

    grid = np.full((len(overlaps), len(sizes)), np.nan)
    for run in runs:
        i = overlaps.index(run["chunk_overlap"])
        j = sizes.index(run["chunk_size"])
        value = mean_metric(run["queries"], metric_key)
        if value is not None:
            grid[i, j] = value

    return sizes, overlaps, grid


def plot_heatmap(sizes, overlaps, grid, title, output_path):
    fig, ax = plt.subplots(figsize=(7, 5))

    image = ax.imshow(grid, cmap="viridis", aspect="auto", origin="lower")

    ax.set_xticks(range(len(sizes)))
    ax.set_xticklabels(sizes)
    ax.set_yticks(range(len(overlaps)))
    ax.set_yticklabels(overlaps)

    ax.set_xlabel("chunk_size")
    ax.set_ylabel("chunk_overlap")
    ax.set_title(f"{title} (mean across all queries)")

    # Annotate each cell with its numeric value.
    for i in range(len(overlaps)):
        for j in range(len(sizes)):
            value = grid[i, j]
            if np.isnan(value):
                label = "n/a"
            else:
                label = f"{value:.3f}"
            ax.text(j, i, label, ha="center", va="center", color="white", fontsize=9)

    fig.colorbar(image, ax=ax, label=title)
    fig.tight_layout()
    fig.savefig(output_path, dpi=120)
    plt.close(fig)


def main():
    runs = collect_runs()
    if not runs:
        print("No usable log files found in logs/. Run `python run_all.py tune` first.")
        return

    print(f"Loaded {len(runs)} runs from logs/.")

    for metric_key, title, filename in METRICS:
        sizes, overlaps, grid = build_grid(runs, metric_key)
        output_path = OUTPUT_DIR / filename
        plot_heatmap(sizes, overlaps, grid, title, output_path)
        print(f"  wrote {output_path.name}  ({len(sizes)} sizes × {len(overlaps)} overlaps)")


if __name__ == "__main__":
    main()
