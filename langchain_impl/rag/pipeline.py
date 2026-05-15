"""LangChain RAG pipeline using LCEL.

Components:
  - Loader:    langchain_community PyPDFLoader / TextLoader
  - Splitter:  langchain_text_splitters RecursiveCharacterTextSplitter
  - Embedder:  langchain_ollama OllamaEmbeddings / langchain_huggingface HuggingFaceEmbeddings
  - Store:     langchain_chroma Chroma
  - LLM:       langchain_ollama ChatOllama (or OpenAI / Anthropic)
  - Chain:     LCEL — retriever | format_docs | prompt | llm | StrOutputParser

Usage::

    from rag.config import load_config
    from rag.pipeline import create_pipeline

    pipeline = create_pipeline(load_config())
    pipeline.ingest(["path/to/docs/"])
    answer = pipeline.query("What is X?")
    for token in pipeline.stream("What is X?"):
        print(token, end="", flush=True)
"""

import logging
import textwrap
from collections.abc import Iterator
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

DEFAULT_SYSTEM_PROMPT = textwrap.dedent("""\
    You are a precise research assistant.

    RULES:
    1. Answer ONLY from the provided context chunks.
    2. Cite the source document for every claim (use the title or filename from the metadata).
    3. If the context does not contain enough information, say "Insufficient info to answer."
    4. Be concise — prefer bullet points over long paragraphs.
    5. Never fabricate data, figures, or document names.
""")


# ── Types used by web/eval layers ─────────────────────────────────────


@dataclass
class Chunk:
    text: str
    doc_id: str
    chunk_index: int
    metadata: dict = field(default_factory=dict)


@dataclass
class SearchResult:
    chunk: Chunk
    score: float   # higher = more similar
    rank: int      # 1-based


# ── Pipeline ───────────────────────────────────────────────────────────


class RAGPipeline:
    """RAG pipeline built entirely from LangChain / LCEL components.

    Exposes a stable interface for the web and eval layers.
    """

    def __init__(
        self,
        vectorstore,
        llm,
        embeddings,
        config,
        system_prompt: str = DEFAULT_SYSTEM_PROMPT,
    ) -> None:
        self.vectorstore = vectorstore
        self.llm = llm           # LangChain ChatModel — also used as ragas judge
        self.embedder = EmbeddingModelAdapter(embeddings)
        self.config = config
        self.system_prompt = system_prompt
        self._prompt = _create_chat_prompt(system_prompt)

    # ── Ingest ───────────────────────────────────────────────────────

    def ingest(self, sources: list[str]) -> int:
        """Load, split, embed, and store documents. Returns chunk count."""
        from langchain_community.document_loaders import PyPDFLoader, TextLoader
        from langchain_text_splitters import RecursiveCharacterTextSplitter

        all_docs = []
        for source in sources:
            try:
                loader = PyPDFLoader(source) if source.lower().endswith(".pdf") else TextLoader(source)
                all_docs.extend(loader.load())
            except Exception as exc:
                logger.warning("Skipping %s: %s", source, exc)

        if not all_docs:
            logger.warning("No documents loaded from: %s", sources)
            return 0

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.chunk_size,
            chunk_overlap=self.config.chunk_overlap,
        )
        chunks = splitter.split_documents(all_docs)
        logger.info("Split %d doc(s) into %d chunk(s)", len(all_docs), len(chunks))

        self.vectorstore.add_documents(chunks)
        logger.info("Stored %d chunk(s)", len(chunks))
        return len(chunks)

    # ── Search ───────────────────────────────────────────────────────

    def search(self, question: str, k: int = 5) -> list[SearchResult]:
        """Embed question and return the top-k nearest chunks."""
        raw = self.vectorstore.similarity_search_with_score(question, k=k)
        return [
            SearchResult(
                chunk=Chunk(
                    text=doc.page_content,
                    doc_id=doc.metadata.get("source", ""),
                    chunk_index=i,
                    metadata=doc.metadata,
                ),
                # Chroma returns L2 distance; convert to [0,1] similarity proxy
                score=1.0 / (1.0 + dist),
                rank=i + 1,
            )
            for i, (doc, dist) in enumerate(raw)
        ]

    # ── Query / Stream ───────────────────────────────────────────────

    def query(self, question: str, k: int = 5) -> str:
        """Retrieve context and generate an answer."""
        # Step 1: find the most relevant document chunks
        docs = self.vectorstore.similarity_search(question, k=k)
        # Step 2: join them into a single context string
        context = _format_docs_as_context(docs)
        # Step 3: fill the prompt template
        prompt = self._prompt.invoke({"context": context, "question": question})
        # Step 4: ask the LLM and return its text response
        response = self.llm.invoke(prompt)
        return response.content

    def stream(self, question: str, k: int = 5) -> Iterator[str]:
        """Like query() but yields tokens one at a time as the LLM generates them."""
        # Steps 1-3 are the same as query()
        docs = self.vectorstore.similarity_search(question, k=k)
        context = _format_docs_as_context(docs)
        prompt = self._prompt.invoke({"context": context, "question": question})
        # Step 4: stream tokens instead of waiting for the full response
        for chunk in self.llm.stream(prompt):
            yield chunk.content


# ── Helpers ────────────────────────────────────────────────────────────


class EmbeddingModelAdapter:
    """Wraps a LangChain Embeddings object to match the interface expected by the eval harness."""

    def __init__(self, embeddings) -> None:
        self._emb = embeddings

    def embed(self, texts: list[str]) -> list[list[float]]:
        return self._emb.embed_documents(texts)

    def embed_query(self, text: str) -> list[float]:
        return self._emb.embed_query(text)


def _format_docs_as_context(docs) -> str:
    parts = []
    for doc in docs:
        title = doc.metadata.get("title", doc.metadata.get("source", "Unknown"))
        parts.append(f"[Source: {title}]\n{doc.page_content}")
    return "\n\n---\n\n".join(parts)


def _create_chat_prompt(system_prompt: str):
    from langchain_core.prompts import ChatPromptTemplate

    return ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "CONTEXT:\n{context}\n\nQUESTION:\n{question}\n\nANSWER:"),
    ])


# ── Factory ────────────────────────────────────────────────────────────


def create_pipeline(
    config=None,
    system_prompt: str = DEFAULT_SYSTEM_PROMPT,
) -> RAGPipeline:
    """Wire together LangChain components from rag.toml config."""
    if config is None:
        from rag.config import load_config
        config = load_config()

    embeddings = _load_embedding_model(config)

    from langchain_chroma import Chroma
    vectorstore = Chroma(
        collection_name=config.collection_name,
        embedding_function=embeddings,
        persist_directory=config.vector_db_dir,
    )

    llm = _load_language_model(config)
    return RAGPipeline(
        vectorstore=vectorstore,
        llm=llm,
        embeddings=embeddings,
        config=config,
        system_prompt=system_prompt,
    )


def _load_embedding_model(config):
    if config.embedder == "huggingface":
        from langchain_huggingface import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(model_name=config.embedder_model)
    if config.embedder == "ollama":
        from langchain_ollama import OllamaEmbeddings
        return OllamaEmbeddings(model=config.embedder_model)
    raise ValueError(f"Unknown embedder: {config.embedder!r}. Supported: huggingface, ollama")


def _load_language_model(config):
    if config.llm_provider == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(
            model=config.llm_model,
            temperature=config.llm_temperature,
        )
    if config.llm_provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=config.llm_model, temperature=config.llm_temperature)
    if config.llm_provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(model=config.llm_model, temperature=config.llm_temperature)
    raise ValueError(
        f"Unknown llm_provider: {config.llm_provider!r}. Supported: ollama, openai, anthropic"
    )
