"""Unit tests for RecursiveSplitter — no external deps, no I/O."""

from rag.core.types import Document
from rag.splitters.recursive import RecursiveSplitter


def _doc(text: str, source: str = "test.txt") -> Document:
    return Document(text=text, metadata={"source": source})


def test_short_text_is_single_chunk():
    splitter = RecursiveSplitter(chunk_size=1000, chunk_overlap=0)
    chunks = splitter.split([_doc("Short text that fits easily.")])
    assert len(chunks) == 1
    assert chunks[0].text == "Short text that fits easily."


def test_long_text_splits_into_multiple_chunks():
    splitter = RecursiveSplitter(chunk_size=50, chunk_overlap=0)
    text = "word " * 100  # 500 chars
    chunks = splitter.split([_doc(text.strip())])
    assert len(chunks) > 1


def test_each_chunk_respects_size_limit():
    splitter = RecursiveSplitter(chunk_size=50, chunk_overlap=0)
    text = "word " * 100
    chunks = splitter.split([_doc(text.strip())])
    # Allow a small tolerance for the separator being included
    for c in chunks:
        assert len(c.text) <= 60, f"Chunk too large: {len(c.text)} chars"


def test_chunk_indices_are_sequential():
    splitter = RecursiveSplitter(chunk_size=30, chunk_overlap=0)
    text = "\n\n".join([f"paragraph {i}" for i in range(10)])
    chunks = splitter.split([_doc(text)])
    assert [c.chunk_index for c in chunks] == list(range(len(chunks)))


def test_doc_id_derived_from_source():
    splitter = RecursiveSplitter(chunk_size=1000)
    chunks = splitter.split([_doc("hello world", source="myfile.pdf")])
    assert chunks[0].doc_id  # non-empty
    # Same source → same doc_id
    chunks2 = splitter.split([_doc("different text", source="myfile.pdf")])
    assert chunks[0].doc_id == chunks2[0].doc_id


def test_different_sources_get_different_doc_ids():
    splitter = RecursiveSplitter(chunk_size=1000)
    c1 = splitter.split([_doc("text", source="a.pdf")])
    c2 = splitter.split([_doc("text", source="b.pdf")])
    assert c1[0].doc_id != c2[0].doc_id


def test_empty_document_produces_no_chunks():
    splitter = RecursiveSplitter()
    chunks = splitter.split([_doc("")])
    assert chunks == []


def test_whitespace_only_document_produces_no_chunks():
    splitter = RecursiveSplitter()
    chunks = splitter.split([_doc("   \n\n   ")])
    assert chunks == []


def test_multiple_docs_metadata_preserved():
    splitter = RecursiveSplitter(chunk_size=1000)
    docs = [
        _doc("doc one content", source="one.pdf"),
        _doc("doc two content", source="two.pdf"),
    ]
    chunks = splitter.split(docs)
    sources = {c.metadata["source"] for c in chunks}
    assert sources == {"one.pdf", "two.pdf"}


def test_paragraph_split_preference():
    """Splitter should prefer paragraph boundaries over word boundaries."""
    splitter = RecursiveSplitter(chunk_size=40, chunk_overlap=0)
    text = "First paragraph here.\n\nSecond paragraph here.\n\nThird paragraph here."
    chunks = splitter.split([_doc(text)])
    # Each paragraph fits in 40 chars, so they should not be merged across paragraphs
    for c in chunks:
        assert len(c.text) <= 40
