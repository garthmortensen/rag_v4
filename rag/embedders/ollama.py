"""Ollama embeddings via direct HTTP (no LangChain)."""

import httpx


class OllamaEmbedder:
    """Calls the Ollama /api/embeddings endpoint.

    Good local alternative to HuggingFace — no GPU required,
    just a running Ollama server with the model pulled.

    Example::

        embedder = OllamaEmbedder(model="nomic-embed-text")
        vec = embedder.embed_query("hello world")
    """

    def __init__(
        self,
        model: str = "nomic-embed-text",
        host: str = "http://localhost:11434",
        timeout: float = 30.0,
    ) -> None:
        self.model = model
        self.host = host.rstrip("/")
        self.timeout = timeout

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_query(t) for t in texts]

    def embed_query(self, text: str) -> list[float]:
        resp = httpx.post(
            f"{self.host}/api/embeddings",
            json={"model": self.model, "prompt": text},
            timeout=self.timeout,
        )
        resp.raise_for_status()
        return resp.json()["embedding"]
