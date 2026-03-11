"""OpenAI chat completion via direct HTTP — no LangChain."""

import json
import os
from collections.abc import Iterator

import httpx

_BASE = "https://api.openai.com/v1"


class OpenAILLM:
    def __init__(
        self,
        model: str = "gpt-4o-mini",
        temperature: float = 0.1,
        api_key: str | None = None,
        timeout: float = 60.0,
    ) -> None:
        self.model = model
        self.temperature = temperature
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.timeout = timeout

    def complete(self, system: str, user: str) -> str:
        resp = httpx.post(
            f"{_BASE}/chat/completions",
            headers=self._headers(),
            json=self._payload(system, user, stream=False),
            timeout=self.timeout,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]

    def stream(self, system: str, user: str) -> Iterator[str]:
        with httpx.stream(
            "POST",
            f"{_BASE}/chat/completions",
            headers=self._headers(),
            json=self._payload(system, user, stream=True),
            timeout=self.timeout,
        ) as resp:
            resp.raise_for_status()
            for line in resp.iter_lines():
                line = line.strip()
                if not line or line == "data: [DONE]":
                    continue
                if line.startswith("data: "):
                    data = json.loads(line[6:])
                    if token := data["choices"][0]["delta"].get("content"):
                        yield token

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _payload(self, system: str, user: str, *, stream: bool) -> dict:
        return {
            "model": self.model,
            "temperature": self.temperature,
            "stream": stream,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
