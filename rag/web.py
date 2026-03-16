"""FastAPI web server for the RAG pipeline.

    python -m rag serve
    python -m rag serve --host 0.0.0.0 --port 8080
"""

import logging
import os
import tempfile
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from rag.config import load_config
from rag.core.pipeline import build_pipeline
from rag.loaders import SUPPORTED

logger = logging.getLogger(__name__)

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(title="RAG Pipeline")

# ── Lazy pipeline singleton ─────────────────────────────────────────

_pipeline = None


def _get_pipeline():
    global _pipeline
    if _pipeline is None:
        cfg = load_config()
        _pipeline = build_pipeline(cfg)
    return _pipeline


# ── Request / response models ───────────────────────────────────────


class QueryRequest(BaseModel):
    question: str
    k: int = 5


class QueryResponse(BaseModel):
    answer: str
    sources: list[dict]


class IngestResponse(BaseModel):
    chunks: int
    files: int


class CorpusStatusResponse(BaseModel):
    total: int
    downloaded: int
    pending: int


class CorpusIngestResponse(BaseModel):
    chunks: int
    files: int


# ── API routes ───────────────────────────────────────────────────────


@app.post("/api/query", response_model=QueryResponse)
def api_query(req: QueryRequest):
    pipeline = _get_pipeline()
    results = pipeline.search(req.question, k=req.k)
    answer = pipeline.query(req.question, k=req.k)
    sources = [
        {
            "title": r.chunk.metadata.get("title", r.chunk.metadata.get("source", "Unknown")),
            "score": round(r.score, 4),
            "text": r.chunk.text[:300],
        }
        for r in results
    ]
    return QueryResponse(answer=answer, sources=sources)


@app.post("/api/query/stream")
def api_query_stream(req: QueryRequest):
    pipeline = _get_pipeline()

    def generate():
        for token in pipeline.stream(req.question, k=req.k):
            yield token

    return StreamingResponse(generate(), media_type="text/plain")


@app.post("/api/ingest", response_model=IngestResponse)
async def api_ingest(files: list[UploadFile]):
    pipeline = _get_pipeline()
    saved_paths: list[str] = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for upload in files:
            ext = os.path.splitext(upload.filename or "")[1].lower()
            if ext not in SUPPORTED:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file type: {ext}. Supported: {sorted(SUPPORTED)}",
                )
            dest = os.path.join(tmpdir, upload.filename)
            content = await upload.read()
            with open(dest, "wb") as f:
                f.write(content)
            saved_paths.append(dest)

        count = pipeline.ingest(saved_paths)

    return IngestResponse(chunks=count, files=len(saved_paths))


# ── Static files & SPA fallback ──────────────────────────────────────


# ── Corpus endpoints ─────────────────────────────────────────────────


@app.get("/api/corpus/sources")
def api_corpus_sources():
    from rag.corpus import list_sources
    return list_sources()


@app.get("/api/corpus/status", response_model=CorpusStatusResponse)
def api_corpus_status():
    from rag.corpus import corpus_status
    return corpus_status()


@app.post("/api/corpus/download")
def api_corpus_download():
    from rag.corpus import download_corpus
    return StreamingResponse(download_corpus(), media_type="text/event-stream")


@app.post("/api/corpus/ingest", response_model=CorpusIngestResponse)
def api_corpus_ingest():
    from rag.corpus import list_downloaded_files

    pipeline = _get_pipeline()
    files = list_downloaded_files()
    if not files:
        return CorpusIngestResponse(chunks=0, files=0)
    count = pipeline.ingest(files)
    return CorpusIngestResponse(chunks=count, files=len(files))


# ── Static files & SPA fallback ──────────────────────────────────────


@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


def run(host: str = "127.0.0.1", port: int = 8000):
    """Start the uvicorn server."""
    import uvicorn

    uvicorn.run(app, host=host, port=port)
