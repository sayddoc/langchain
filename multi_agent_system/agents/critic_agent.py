"""Critic and validation agent implementation."""

from __future__ import annotations

from langchain_core.language_models.chat_models import BaseChatModel

from multi_agent_system.agents.messages import AgentMessage, CritiqueOutput
from multi_agent_system.utils.logger import setup_logger


class CriticAgent:
    """Performs consistency checks and quality validation."""

    def __init__(self, llm: BaseChatModel, *, log_level: str = "INFO") -> None:
        self._llm = llm
        self._logger = setup_logger(self.__class__.__name__, level=log_level)

    def run(self, research: AgentMessage, analysis: AgentMessage, planning: AgentMessage) -> AgentMessage:
        """Evaluate outputs and return critical recommendations."""
        self._logger.info("Running critical validation")
        structured_llm = self._llm.with_structured_output(CritiqueOutput)
        result = structured_llm.invoke(
            [
                (
                    "system",
                    "Você é um crítico técnico. Busque inconsistências, vieses e lacunas relevantes.",
                ),
                (
                    "human",
                    f"Pesquisa: {research.payload}\n"
                    f"Análise: {analysis.payload}\n"
                    f"Planejamento: {planning.payload}",
                ),
            ]
        )

        return AgentMessage(
            sender="critic_agent",
            recipient="coordinator_agent",
            stage="critique",
            payload=result.model_dump(),
        )
