"""HuggingFace sentence-transformers embedder (no LangChain)."""


class HuggingFaceEmbedder:
    """Wraps sentence-transformers SentenceTransformer.

    Lazy-loads the model on first use so import is fast.
    Requires: uv sync --extra hf
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self.model_name = model_name
        self._model = None

    def _model_(self):
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
            except ImportError:
                raise ImportError(
                    "sentence-transformers is required: uv sync --extra hf"
                )
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def embed(self, texts: list[str]) -> list[list[float]]:
        return self._model_().encode(texts, convert_to_numpy=True).tolist()

    def embed_query(self, text: str) -> list[float]:
        return self.embed([text])[0]
