"""RAGPipeline and build_pipeline factory.

Usage::

    from rag.config import load_config
    from rag.core.pipeline import build_pipeline

    cfg = load_config()
    pipeline = build_pipeline(cfg)

    pipeline.ingest(["corpus/raw_data/"])
    answer = pipeline.query("What is X?")

    for token in pipeline.stream("What is X?"):
        print(token, end="", flush=True)
"""

import logging
import textwrap
from collections.abc import Iterator

from rag.core.protocols import Embedder, LLM, Loader, Splitter, VectorStore
from rag.core.types import SearchResult

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


class RAGPipeline:
    def __init__(
        self,
        loader: Loader,
        splitter: Splitter,
        embedder: Embedder,
        store: VectorStore,
        llm: LLM,
        system_prompt: str = DEFAULT_SYSTEM_PROMPT,
    ) -> None:
        self.loader = loader
        self.splitter = splitter
        self.embedder = embedder
        self.store = store
        self.llm = llm
        self.system_prompt = system_prompt

    def ingest(self, sources: list[str]) -> int:
        """Load, chunk, embed, and store documents. Returns chunk count."""
        docs = [doc for s in sources for doc in self.loader.load(s)]
        if not docs:
            logger.warning("No documents loaded from: %s", sources)
            return 0
        chunks = self.splitter.split(docs)
        logger.info("Split %d doc(s) into %d chunk(s)", len(docs), len(chunks))
        embeddings = self.embedder.embed([c.text for c in chunks])
        self.store.upsert(chunks, embeddings)
        logger.info("Upserted %d chunk(s)", len(chunks))
        return len(chunks)

    def search(self, question: str, k: int = 5) -> list[SearchResult]:
        """Embed *question* and return the top-k nearest chunks."""
        return self.store.search(self.embedder.embed_query(question), k)

    def query(self, question: str, k: int = 5) -> str:
        """Retrieve relevant chunks and generate an answer."""
        results = self.search(question, k)
        context = _format_context(results)
        return self.llm.complete(
            self.system_prompt,
            f"CONTEXT:\n{context}\n\nQUESTION:\n{question}\n\nANSWER:",
        )

    def stream(self, question: str, k: int = 5) -> Iterator[str]:
        """Like query() but yields tokens as they arrive."""
        results = self.search(question, k)
        context = _format_context(results)
        yield from self.llm.stream(
            self.system_prompt,
            f"CONTEXT:\n{context}\n\nQUESTION:\n{question}\n\nANSWER:",
        )


def _format_context(results: list[SearchResult]) -> str:
    parts = []
    for r in results:
        title = r.chunk.metadata.get("title", r.chunk.metadata.get("source", "Unknown"))
        parts.append(f"[Source: {title}]\n{r.chunk.text}")
    return "\n\n---\n\n".join(parts)


def build_pipeline(
    config=None,
    system_prompt: str = DEFAULT_SYSTEM_PROMPT,
) -> RAGPipeline:
    """Wire together the default implementations from rag.toml config.

    Parameters
    ----------
    config : Config | None
        Loaded config object. Calls load_config() if None.
    system_prompt : str
        Override the default RAG system prompt.
    """
    if config is None:
        from rag.config import load_config
        config = load_config()

    from rag.embedders import get_embedder
    from rag.llms import get_llm
    from rag.loaders import MultiLoader
    from rag.splitters.recursive import RecursiveSplitter
    from rag.stores import get_store

    return RAGPipeline(
        loader=MultiLoader(),
        splitter=RecursiveSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
        ),
        embedder=get_embedder(config),
        store=get_store(config),
        llm=get_llm(config),
        system_prompt=system_prompt,
    )
