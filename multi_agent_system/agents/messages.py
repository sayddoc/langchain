"""Structured message schemas exchanged among agents."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field


class AgentMessage(BaseModel):
    """Envelope used for all inter-agent communication."""

    sender: str
    recipient: str
    stage: Literal["research", "analysis", "planning", "critique", "final"]
    payload: dict[str, Any]
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ResearchOutput(BaseModel):
    """Expected output format from the Research Agent."""

    query: str
    summary: str
    sources: list[dict[str, Any]]
    raw_data: list[dict[str, Any]]


class AnalysisOutput(BaseModel):
    """Expected output format from the Data Analysis Agent."""

    cleaned_data: list[dict[str, Any]]
    metrics: dict[str, Any]
    insights: list[str]


class PlanningOutput(BaseModel):
    """Expected output format from the Strategic Planning Agent."""

    objectives: list[str]
    priorities: list[str]
    risk_assessment: list[str]
    roadmap: list[dict[str, str]]


class CritiqueOutput(BaseModel):
    """Expected output format from the Critic Agent."""

    consistency_score: float
    detected_gaps: list[str]
    bias_alerts: list[str]
    recommendations: list[str]
