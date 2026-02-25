"""Configuration for the multi-agent system."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(slots=True)
class Settings:
    """Runtime settings used across the project."""

    model_provider: str = os.getenv("MODEL_PROVIDER", "openai")
    model_name: str = os.getenv("MODEL_NAME", "gpt-4o-mini")
    temperature: float = float(os.getenv("MODEL_TEMPERATURE", "0.2"))
    max_retries: int = int(os.getenv("AGENT_MAX_RETRIES", "2"))
    timeout_seconds: int = int(os.getenv("AGENT_TIMEOUT_SECONDS", "45"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
