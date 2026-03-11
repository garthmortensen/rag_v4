"""Unit tests for config loading."""

import tempfile
import os

from rag.config import Config, load_config


def test_defaults_when_file_missing():
    cfg = load_config("/nonexistent/path/rag.toml")
    assert cfg == Config()


def test_override_from_toml():
    content = b"[rag]\nchunk_size = 500\ncollection_name = \"my_col\"\n"
    with tempfile.NamedTemporaryFile(suffix=".toml", delete=False) as f:
        f.write(content)
        path = f.name
    try:
        cfg = load_config(path)
        assert cfg.chunk_size == 500
        assert cfg.collection_name == "my_col"
        # Unspecified fields keep defaults
        assert cfg.chunk_overlap == Config().chunk_overlap
    finally:
        os.unlink(path)


def test_unknown_keys_ignored():
    content = b"[rag]\nchunk_size = 200\nunknown_key = \"ignored\"\n"
    with tempfile.NamedTemporaryFile(suffix=".toml", delete=False) as f:
        f.write(content)
        path = f.name
    try:
        cfg = load_config(path)
        assert cfg.chunk_size == 200
        assert not hasattr(cfg, "unknown_key")
    finally:
        os.unlink(path)
