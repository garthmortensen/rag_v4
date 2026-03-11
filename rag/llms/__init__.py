"""LLM factory."""

from rag.core.protocols import LLM


def get_llm(config) -> LLM:
    """Return the LLM specified in *config*.

    config.llm_provider values:
      "ollama"    — local Ollama server (no API key needed)
      "openai"    — OpenAI API (OPENAI_API_KEY in .env)
      "anthropic" — Anthropic API (ANTHROPIC_API_KEY in .env)
    """
    if config.llm_provider == "ollama":
        from rag.llms.ollama import OllamaLLM

        return OllamaLLM(
            model=config.llm_model,
            host=config.ollama_host,
            temperature=config.llm_temperature,
        )

    if config.llm_provider == "openai":
        from rag.llms.openai import OpenAILLM

        return OpenAILLM(model=config.llm_model, temperature=config.llm_temperature)

    if config.llm_provider == "anthropic":
        from rag.llms.anthropic import AnthropicLLM

        return AnthropicLLM(model=config.llm_model, temperature=config.llm_temperature)

    raise ValueError(
        f"Unknown llm_provider: {config.llm_provider!r}. "
        "Supported: ollama, openai, anthropic"
    )
