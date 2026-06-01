"""Ingest and tune all chunk_size × chunk_overlap combinations.

Phases:
  ingest  — build ChromaDB collections (skips existing ones)
  tune    — run benchmark queries and write timestamped logs
  all     — ingest then tune (default)

Usage:
    python run_all.py          # ingest + tune
    python run_all.py ingest
    python run_all.py tune
"""

import sys
from itertools import product

from rag.config import load_config
from rag.ingest import ingest
from rag.tune import run as tune_run

CHUNK_SIZES    = [500, 1000, 2000, 3000]
CHUNK_OVERLAPS = [50, 100, 200, 300]


def _each_combination(base_cfg):
    for size, overlap in product(CHUNK_SIZES, CHUNK_OVERLAPS):
        base_cfg.chunk_size      = size
        base_cfg.chunk_overlap   = overlap
        base_cfg.collection_name = f"chunk_size_{size}_chunk_overlap_{overlap}"
        print(f"\n{'=' * 60}\n  {base_cfg.collection_name}\n{'=' * 60}")
        yield base_cfg


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode not in ("ingest", "tune", "all"):
        print(f"Unknown mode '{mode}'. Use: ingest | tune | all")
        sys.exit(1)

    n = len(CHUNK_SIZES) * len(CHUNK_OVERLAPS)
    print(f"Mode: {mode}  |  {n} combinations\n")

    base_cfg = load_config()

    if mode in ("ingest", "all"):
        print("=== INGEST ===")
        for cfg in _each_combination(base_cfg):
            ingest(cfg)

    if mode in ("tune", "all"):
        print("\n=== TUNE ===")
        for cfg in _each_combination(base_cfg):
            tune_run(cfg)


if __name__ == "__main__":
    main()
