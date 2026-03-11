"""Ollama LLM via direct HTTP — no LangChain."""

import json
from collections.abc import Iterator

import httpx


class OllamaLLM:
    """Calls the Ollama /api/chat endpoint.

    Example::

        llm = OllamaLLM(model="llama3.2:3b")
        print(llm.complete("You are helpful.", "What is RAG?"))
    """

    def __init__(
        self,
        model: str = "llama3.2:3b",
        host: str = "http://localhost:11434",
        temperature: float = 0.1,
        timeout: float = 120.0,
    ) -> None:
        self.model = model
        self.host = host.rstrip("/")
        self.temperature = temperature
        self.timeout = timeout

    def complete(self, system: str, user: str) -> str:
        resp = httpx.post(
            f"{self.host}/api/chat",
            json=self._payload(system, user, stream=False),
            timeout=self.timeout,
        )
        resp.raise_for_status()
        return resp.json()["message"]["content"]

    def stream(self, system: str, user: str) -> Iterator[str]:
        with httpx.stream(
            "POST",
            f"{self.host}/api/chat",
            json=self._payload(system, user, stream=True),
            timeout=self.timeout,
        ) as resp:
            resp.raise_for_status()
            for line in resp.iter_lines():
                if not line:
                    continue
                data = json.loads(line)
                if token := data.get("message", {}).get("content"):
                    yield token
                if data.get("done"):
                    break

    def _payload(self, system: str, user: str, *, stream: bool) -> dict:
        return {
            "model": self.model,
            "stream": stream,
            "options": {"temperature": self.temperature},
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
