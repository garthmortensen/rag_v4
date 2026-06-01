"""Ingest all chunk_size × chunk_overlap combinations into ChromaDB.

Existing collections are skipped. Edit CHUNK_SIZES and CHUNK_OVERLAPS below
to control what gets ingested.

Usage:
    python ingest_all_combinations.py
"""

from itertools import product

from rag.config import load_config
from rag.ingest import ingest

CHUNK_SIZES    = [500, 1000, 2000, 3000]
CHUNK_OVERLAPS = [50, 100, 200, 300]


def main() -> None:
    combinations = list(product(CHUNK_SIZES, CHUNK_OVERLAPS))
    print(f"Combinations to ingest: {len(combinations)}")
    for s, o in combinations:
        print(f"  chunk_size_{s}_chunk_overlap_{o}")
    print()

    base_cfg = load_config()

    for size, overlap in combinations:
        name = f"chunk_size_{size}_chunk_overlap_{overlap}"
        print(f"\n{'=' * 60}\n  {name}\n{'=' * 60}")

        base_cfg.chunk_size      = size
        base_cfg.chunk_overlap   = overlap
        base_cfg.collection_name = name

        ingest(base_cfg)


if __name__ == "__main__":
    main()
