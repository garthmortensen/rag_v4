"""Embedder factory."""

from rag.core.protocols import Embedder


def get_embedder(config) -> Embedder:
    """Return the embedder specified in *config*.

    config.embedder values:
      "huggingface"  — sentence-transformers (requires --extra hf)
      "ollama"       — Ollama /api/embeddings endpoint
    """
    if config.embedder == "huggingface":
        from rag.embedders.huggingface import HuggingFaceEmbedder

        return HuggingFaceEmbedder(model_name=config.embedder_model)

    if config.embedder == "ollama":
        from rag.embedders.ollama import OllamaEmbedder

        return OllamaEmbedder(model=config.embedder_model, host=config.ollama_host)

    raise ValueError(
        f"Unknown embedder: {config.embedder!r}. Supported: huggingface, ollama"
    )
