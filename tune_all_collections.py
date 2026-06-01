"""Run rag.tune for every collection in rag.toml's collection_names list.

Usage:
    python tune_all_collections.py
"""

import re
import sys
import tomllib
from pathlib import Path

TOML_PATH = Path("rag.toml")

_ACTIVE_LINE_RE = re.compile(r'(collection_name\s*=\s*")[^"]+(")')


def main() -> None:
    original_toml = TOML_PATH.read_text(encoding="utf-8")

    with open(TOML_PATH, "rb") as f:
        collections = tomllib.load(f)["rag"]["storage"].get("collection_names", [])

    if not collections:
        print("No collection_names list found in rag.toml — nothing to do.")
        sys.exit(0)

    print(f"Collections to tune: {collections}\n")

    from rag.tune import run as tune_run

    try:
        for name in collections:
            print(f"\n{'=' * 60}")
            print(f"  Collection: {name}")
            print(f"{'=' * 60}")

            updated = _ACTIVE_LINE_RE.sub(rf'\g<1>{name}\g<2>', original_toml)
            TOML_PATH.write_text(updated, encoding="utf-8")

            tune_run()
    finally:
        TOML_PATH.write_text(original_toml, encoding="utf-8")
        print("\nRestored original rag.toml.")


if __name__ == "__main__":
    main()
