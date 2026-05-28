"""Streamlit chat UI for the RAG pipeline.

Usage::

    streamlit run rag/ui.py
"""

from pathlib import Path

import streamlit as st

from rag.config import load_config
from rag.query import build_chain, build_embedder, build_llm, build_vectorstore

st.set_page_config(page_title="RAG Chat", layout="centered")
st.title("RAG Chat")

_PREVIEW_LEN = 300


@st.cache_resource(show_spinner="Loading model...")
def _load_chain():
    cfg = load_config()
    embedder = build_embedder(cfg)
    vectorstore = build_vectorstore(cfg, embedder)
    llm = build_llm(cfg)
    chain = build_chain(vectorstore, llm, cfg.top_k)
    return chain, cfg


def _format_sources(docs) -> str:
    """Return a markdown string listing each source chunk."""
    lines = []
    for i, doc in enumerate(docs, 1):
        name = Path(doc.metadata.get("source", "unknown")).name
        content = doc.page_content.strip().replace("\n", " ")
        preview = content[:_PREVIEW_LEN] + ("..." if len(content) > _PREVIEW_LEN else "")
        lines.append(f"**[{i}] {name}**\n{preview}")
    return "\n\n".join(lines)


def _stream(chain, question: str) -> tuple[str, str]:
    """Stream the chain response; return (answer, sources_markdown)."""
    placeholder = st.empty()
    full_answer = ""
    sources_text = ""

    for chunk in chain.stream(question):
        if "answer" in chunk:
            full_answer += chunk["answer"]
            placeholder.markdown(full_answer + "▌")
        if "sources" in chunk:
            sources_text = _format_sources(chunk["sources"])

    placeholder.markdown(full_answer)
    return full_answer, sources_text


chain, cfg = _load_chain()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Render previous turns
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("Sources"):
                st.markdown(msg["sources"])

# New question
if question := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        answer, sources_text = _stream(chain, question)
        if sources_text:
            with st.expander("Sources"):
                st.markdown(sources_text)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": sources_text}
    )
