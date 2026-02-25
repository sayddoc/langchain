"""Strategic planning agent implementation."""

from __future__ import annotations

from langchain_core.language_models.chat_models import BaseChatModel

from multi_agent_system.agents.messages import AgentMessage, PlanningOutput
from multi_agent_system.utils.logger import setup_logger


class PlanningAgent:
    """Converts analysis artifacts into an action plan."""

    def __init__(self, llm: BaseChatModel, *, log_level: str = "INFO") -> None:
        self._llm = llm
        self._logger = setup_logger(self.__class__.__name__, level=log_level)

    def run(self, incoming: AgentMessage) -> AgentMessage:
        """Generate roadmap, priorities, and risk assessment."""
        self._logger.info("Building strategic planning output")
        structured_llm = self._llm.with_structured_output(PlanningOutput)
        result = structured_llm.invoke(
            [
                (
                    "system",
                    "Você é um estrategista. Crie um plano tático executável e baseado em evidências.",
                ),
                (
                    "human",
                    f"Métricas: {incoming.payload.get('metrics', {})}\n"
                    f"Insights: {incoming.payload.get('insights', [])}",
                ),
            ]
        )

        return AgentMessage(
            sender="planning_agent",
            recipient="critic_agent",
            stage="planning",
            payload=result.model_dump(),
        )
