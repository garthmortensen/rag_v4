"""Unit tests for RAGPipeline — all components mocked, no I/O."""

from unittest.mock import MagicMock

from rag.core.pipeline import RAGPipeline, _format_context
from rag.core.types import Chunk, Document, SearchResult


def _make_chunk(text: str = "chunk text", source: str = "test.pdf") -> Chunk:
    return Chunk(text=text, doc_id="abc123", chunk_index=0, metadata={"source": source})


def _make_result(text: str = "chunk text", score: float = 0.9) -> SearchResult:
    return SearchResult(chunk=_make_chunk(text), score=score, rank=1)


def _make_pipeline(answer: str = "mocked answer") -> RAGPipeline:
    loader = MagicMock()
    loader.load.return_value = [Document(text="content", metadata={"source": "t.pdf"})]

    splitter = MagicMock()
    splitter.split.return_value = [_make_chunk()]

    embedder = MagicMock()
    embedder.embed.return_value = [[0.1] * 384]
    embedder.embed_query.return_value = [0.1] * 384

    store = MagicMock()
    store.search.return_value = [_make_result()]
    store.upsert.return_value = None

    llm = MagicMock()
    llm.complete.return_value = answer
    llm.stream.return_value = iter(["tok1", "tok2"])

    return RAGPipeline(
        loader=loader,
        splitter=splitter,
        embedder=embedder,
        store=store,
        llm=llm,
    )


# ── ingest ───────────────────────────────────────────────────────────

def test_ingest_returns_chunk_count():
    pipeline = _make_pipeline()
    assert pipeline.ingest(["t.pdf"]) == 1


def test_ingest_calls_loader_for_each_source():
    pipeline = _make_pipeline()
    pipeline.ingest(["a.pdf", "b.pdf"])
    assert pipeline.loader.load.call_count == 2


def test_ingest_empty_docs_returns_zero():
    pipeline = _make_pipeline()
    pipeline.loader.load.return_value = []
    assert pipeline.ingest(["empty.pdf"]) == 0
    pipeline.store.upsert.assert_not_called()


# ── search ────────────────────────────────────────────────────────────

def test_search_embeds_query_and_calls_store():
    pipeline = _make_pipeline()
    results = pipeline.search("test query", k=3)
    pipeline.embedder.embed_query.assert_called_once_with("test query")
    pipeline.store.search.assert_called_once()
    assert len(results) == 1
    assert results[0].rank == 1


# ── query ─────────────────────────────────────────────────────────────

def test_query_returns_llm_answer():
    pipeline = _make_pipeline(answer="The answer is 42.")
    assert pipeline.query("What is the answer?") == "The answer is 42."


def test_query_passes_context_to_llm():
    pipeline = _make_pipeline()
    pipeline.query("Something?")
    call_args = pipeline.llm.complete.call_args
    user_msg = call_args[0][1]  # second positional arg
    assert "CONTEXT" in user_msg
    assert "QUESTION" in user_msg


# ── stream ────────────────────────────────────────────────────────────

def test_stream_yields_tokens():
    pipeline = _make_pipeline()
    tokens = list(pipeline.stream("What?"))
    assert tokens == ["tok1", "tok2"]


# ── context formatting ────────────────────────────────────────────────

def test_format_context_uses_source_when_no_title():
    results = [_make_result("content about X")]
    ctx = _format_context(results)
    assert "test.pdf" in ctx
    assert "content about X" in ctx


def test_format_context_prefers_title_over_source():
    chunk = Chunk(
        text="body text",
        doc_id="id1",
        chunk_index=0,
        metadata={"source": "file.pdf", "title": "My Report"},
    )
    results = [SearchResult(chunk=chunk, score=0.9, rank=1)]
    ctx = _format_context(results)
    assert "My Report" in ctx
    assert "file.pdf" not in ctx


def test_format_context_separates_multiple_results():
    results = [_make_result(f"chunk {i}") for i in range(3)]
    ctx = _format_context(results)
    assert ctx.count("---") == 2
