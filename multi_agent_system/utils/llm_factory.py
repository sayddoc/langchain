"""LLM factory to simplify model swapping."""

from __future__ import annotations

from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel

from multi_agent_system.config import Settings


def create_chat_model(settings: Settings) -> BaseChatModel:
    """Create a chat model according to project settings."""
    return init_chat_model(
        model=settings.model_name,
        model_provider=settings.model_provider,
        temperature=settings.temperature,
    )
