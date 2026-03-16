"""Corpus download and ingest adapter.

Wraps the standalone corpus/downloader.py logic into functions
callable from the API layer, yielding structured progress events
instead of printing to the rich console.
"""

import csv
import json
import logging
import mimetypes
import os
import random
import re
import shutil
import subprocess
import time
import uuid
from datetime import datetime, timezone
from typing import Generator
from urllib.parse import urlparse

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

# ── Paths (relative to project root) ────────────────────────────────

SOURCES_CSV = "corpus/data_sources.csv"
CITATIONS_CSV = "corpus/citations.csv"
RAW_DATA_DIR = "corpus/raw_data"
CITATIONS_DIR = "corpus/raw_data/citations"
METADATA_CSV = "corpus/metadata.csv"

METADATA_FIELDS = [
    "doc_id", "source_type", "source_url", "local_path", "title",
    "category", "source_org", "author", "retrieved_at",
    "last_modified_at", "content_type", "content_length_bytes",
]

MIN_DELAY = 1
MAX_DELAY = 3


# ── Helpers (adapted from corpus/downloader.py) ─────────────────────


def _sanitize_filename(text: str) -> str:
    clean = re.sub(r"[^\w\s-]", "", text)
    clean = re.sub(r"[\s_-]+", "_", clean)
    return clean.strip("_").lower()


def _generate_doc_id() -> str:
    return uuid.uuid4().hex


def _get_session() -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=3, backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"], raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close",
    })
    return session


def _construct_filepath(base_dir: str, category: str, name: str, filetype: str) -> str:
    clean_cat = _sanitize_filename(category)
    clean_name = _sanitize_filename(name)
    return os.path.join(base_dir, f"{clean_cat}_{clean_name}.{filetype}")


def _write_response_to_file(response: requests.Response, filepath: str) -> None:
    tmp = f"{filepath}.part"
    with open(tmp, "wb") as f:
        for chunk in response.iter_content(chunk_size=256 * 1024):
            if chunk:
                f.write(chunk)
    os.replace(tmp, filepath)


def _download_with_wget(url: str, filepath: str, ua: str, timeout: int) -> bool:
    wget = shutil.which("wget")
    if not wget:
        return False
    tmp = f"{filepath}.part"
    cmd = [wget, "--quiet", "--max-redirect=10", "--timeout", str(timeout),
           "--tries", "3", "--user-agent", ua, "--output-document", tmp, url]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.replace(tmp, filepath)
        return True
    except Exception:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except OSError:
                pass
        return False


def _download_with_curl(url: str, filepath: str, ua: str, timeout: int) -> bool:
    curl = shutil.which("curl")
    if not curl:
        return False
    tmp = f"{filepath}.part"
    cmd = [curl, "--fail", "--location", "--silent", "--show-error",
           "--max-time", str(timeout), "--retry", "3", "--retry-delay", "1",
           "-A", ua, "-o", tmp, url]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.replace(tmp, filepath)
        return True
    except Exception:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except OSError:
                pass
        return False


def _download_file(session: requests.Session, url: str, filepath: str, timeout: int = 60):
    """Download url to filepath. Returns (response | None, used_fallback)."""
    try:
        resp = session.get(url, timeout=timeout, stream=True)
        resp.raise_for_status()
        _write_response_to_file(resp, filepath)
        return resp, False
    except RequestException:
        ua = session.headers.get("User-Agent", "")
        if _download_with_wget(url, filepath, ua, timeout):
            return None, True
        if _download_with_curl(url, filepath, ua, timeout):
            return None, True
        raise


def _capture_metadata(response, filepath, filetype, url, name, category="", source_org=""):
    lm_raw = response.headers.get("Last-Modified", "") if response else ""
    if lm_raw:
        try:
            lm = datetime.strptime(lm_raw, "%a, %d %b %Y %H:%M:%S %Z").strftime("%Y%m%d%H%M%S")
        except ValueError:
            lm = ""
    else:
        lm = ""
    return {
        "doc_id": _generate_doc_id(),
        "source_type": filetype,
        "source_url": url,
        "local_path": filepath,
        "title": name,
        "category": category,
        "source_org": source_org,
        "author": urlparse(url).hostname or "Unknown",
        "retrieved_at": datetime.now(timezone.utc).strftime("%Y%m%d%H%M"),
        "last_modified_at": lm,
        "content_type": response.headers.get("Content-Type", "") if response else
                        (mimetypes.guess_type(filepath)[0] or ""),
        "content_length_bytes": response.headers.get("Content-Length", "") if response else
                                str(os.path.getsize(filepath)) if os.path.exists(filepath) else "",
    }


def _load_metadata(path: str) -> dict:
    meta = {}
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                meta[row["local_path"]] = row
    return meta


def _save_metadata(metadata: dict, path: str) -> None:
    rows = sorted(metadata.values(), key=lambda r: r["doc_id"])
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=METADATA_FIELDS)
        w.writeheader()
        w.writerows(rows)


# ── Public API ───────────────────────────────────────────────────────


def list_sources() -> list[dict]:
    """Return the list of data sources from the CSV."""
    if not os.path.exists(SOURCES_CSV):
        return []
    with open(SOURCES_CSV, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def corpus_status() -> dict:
    """Return counts of total sources, downloaded files, and pending."""
    sources = list_sources()
    downloaded = 0
    pending = 0
    for row in sources:
        category = row.get("Category", "Uncategorized").strip()
        name = row.get("Name", "Unknown").strip()
        filetype = row.get("Filetype", "html").strip().lower()
        filepath = _construct_filepath(RAW_DATA_DIR, category, name, filetype)
        if os.path.exists(filepath):
            downloaded += 1
        else:
            pending += 1
    return {"total": len(sources), "downloaded": downloaded, "pending": pending}


def download_corpus() -> Generator[str, None, None]:
    """Download all sources, yielding SSE-formatted progress lines.

    Each yielded string is a ``data: {...}\\n\\n`` SSE message with JSON
    containing keys: ``type``, ``name``, ``index``, ``total``, ``status``.
    """
    sources = list_sources()
    if not sources:
        yield _sse({"type": "done", "downloaded": 0, "skipped": 0, "failed": 0})
        return

    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    session = _get_session()
    metadata = _load_metadata(METADATA_CSV)

    downloaded = skipped = failed = 0
    total = len(sources)

    for i, row in enumerate(sources):
        category = row.get("Category", "Uncategorized").strip()
        source_org = row.get("Source", "").strip()
        name = row.get("Name", "Unknown").strip()
        filetype = row.get("Filetype", "html").strip().lower()
        url = row.get("Link", "").strip()

        if not url:
            skipped += 1
            yield _sse({"type": "progress", "name": name, "index": i + 1,
                         "total": total, "status": "skipped"})
            continue

        filepath = _construct_filepath(RAW_DATA_DIR, category, name, filetype)

        if os.path.exists(filepath):
            skipped += 1
            yield _sse({"type": "progress", "name": name, "index": i + 1,
                         "total": total, "status": "exists"})
            continue

        try:
            resp, used_fallback = _download_file(session, url, filepath)
            metadata[filepath] = _capture_metadata(
                resp if not used_fallback else None,
                filepath, filetype, url, name, category, source_org,
            )
            downloaded += 1
            yield _sse({"type": "progress", "name": name, "index": i + 1,
                         "total": total, "status": "downloaded"})
            time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
        except Exception as exc:
            failed += 1
            logger.warning("Download failed %s: %s", name, exc)
            yield _sse({"type": "progress", "name": name, "index": i + 1,
                         "total": total, "status": "failed", "error": str(exc)})

    _save_metadata(metadata, METADATA_CSV)
    yield _sse({"type": "done", "downloaded": downloaded,
                "skipped": skipped, "failed": failed})


def list_downloaded_files() -> list[str]:
    """Return paths of all downloaded corpus files suitable for ingestion."""
    from rag.loaders import SUPPORTED

    files = []
    if not os.path.isdir(RAW_DATA_DIR):
        return files
    for root, _, filenames in os.walk(RAW_DATA_DIR):
        for fname in sorted(filenames):
            if os.path.splitext(fname)[1].lower() in SUPPORTED:
                files.append(os.path.join(root, fname))
    return files


def _sse(data: dict) -> str:
    return f"data: {json.dumps(data)}\n\n"
