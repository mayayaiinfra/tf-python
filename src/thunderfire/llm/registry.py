"""
THUNDERFIRE LLM Provider Registry — Auto-detect provider from environment.

EDGE: Platform-agnostic provider selection.
"""

import os
from typing import Optional

from .base import ThunderFireLLMProvider
from .openai_provider import OpenAIProvider
from .anthropic_provider import AnthropicProvider
from .local_provider import LocalProvider
from ..client import ThunderFireClientSync


def get_provider(
    name: str = "auto",
    client: Optional[ThunderFireClientSync] = None
) -> ThunderFireLLMProvider:
    """Get LLM provider by name or auto-detect from environment.

    Auto-detection priority:
      1. THUNDERFIRE_LLM_PROVIDER env var (explicit: "openai" | "anthropic" | "local")
      2. ANTHROPIC_API_KEY set → Anthropic
      3. OPENAI_API_KEY set → OpenAI
      4. STREAM_LOCAL_URL set → Local
      5. Default → OpenAI (backward compatibility)

    Args:
        name: Provider name or "auto" for auto-detection
        client: Optional ThunderFireClientSync instance (shared across providers)

    Returns:
        ThunderFireLLMProvider instance

    Examples:
        >>> provider = get_provider()  # Auto-detect
        >>> provider = get_provider("anthropic")  # Explicit
        >>> provider = get_provider("local", client=my_client)  # With shared client

    Environment Variables:
        THUNDERFIRE_LLM_PROVIDER: Explicit provider selection
        ANTHROPIC_API_KEY: Anthropic API key (triggers auto-detect)
        OPENAI_API_KEY: OpenAI API key (triggers auto-detect)
        STREAM_LOCAL_URL: Local inference URL (triggers auto-detect)
    """
    # Explicit provider name
    if name != "auto":
        return _get_provider_by_name(name, client)

    # Auto-detect from environment
    explicit = os.getenv("THUNDERFIRE_LLM_PROVIDER", "").lower()
    if explicit:
        return _get_provider_by_name(explicit, client)

    # Check API keys and endpoints
    if os.getenv("ANTHROPIC_API_KEY"):
        return AnthropicProvider(client)

    if os.getenv("OPENAI_API_KEY"):
        return OpenAIProvider(client)

    if os.getenv("STREAM_LOCAL_URL"):
        return LocalProvider(client)

    # Default: OpenAI (backward compatibility)
    return OpenAIProvider(client)


def _get_provider_by_name(
    name: str,
    client: Optional[ThunderFireClientSync]
) -> ThunderFireLLMProvider:
    """Get provider by explicit name."""
    providers = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "local": LocalProvider,
    }

    provider_cls = providers.get(name.lower())
    if not provider_cls:
        raise ValueError(
            f"Unknown provider: {name}. "
            f"Supported: {list(providers.keys())}"
        )

    return provider_cls(client)


def list_providers() -> list[str]:
    """Return list of supported provider names.

    Returns:
        ["openai", "anthropic", "local"]
    """
    return ["openai", "anthropic", "local"]
