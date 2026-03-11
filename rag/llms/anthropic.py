"""Anthropic Messages API via direct HTTP — no LangChain."""

import json
import os
from collections.abc import Iterator

import httpx

_BASE = "https://api.anthropic.com/v1"
_API_VERSION = "2023-06-01"


class AnthropicLLM:
    def __init__(
        self,
        model: str = "claude-sonnet-4-6",
        temperature: float = 0.1,
        max_tokens: int = 4096,
        api_key: str | None = None,
        timeout: float = 60.0,
    ) -> None:
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        self.timeout = timeout

    def complete(self, system: str, user: str) -> str:
        resp = httpx.post(
            f"{_BASE}/messages",
            headers=self._headers(),
            json=self._payload(system, user, stream=False),
            timeout=self.timeout,
        )
        resp.raise_for_status()
        return resp.json()["content"][0]["text"]

    def stream(self, system: str, user: str) -> Iterator[str]:
        with httpx.stream(
            "POST",
            f"{_BASE}/messages",
            headers=self._headers(),
            json=self._payload(system, user, stream=True),
            timeout=self.timeout,
        ) as resp:
            resp.raise_for_status()
            for line in resp.iter_lines():
                line = line.strip()
                if not line or not line.startswith("data: "):
                    continue
                data = json.loads(line[6:])
                if data.get("type") == "content_block_delta":
                    if token := data.get("delta", {}).get("text"):
                        yield token

    def _headers(self) -> dict:
        return {
            "x-api-key": self.api_key,
            "anthropic-version": _API_VERSION,
            "Content-Type": "application/json",
        }

    def _payload(self, system: str, user: str, *, stream: bool) -> dict:
        return {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "stream": stream,
            "system": system,
            "messages": [{"role": "user", "content": user}],
        }
