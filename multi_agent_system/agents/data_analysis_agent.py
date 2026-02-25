"""Data analysis agent implementation."""

from __future__ import annotations

from langchain_core.language_models.chat_models import BaseChatModel

from multi_agent_system.agents.messages import AnalysisOutput, AgentMessage
from multi_agent_system.tools.data_tools import clean_records, descriptive_metrics
from multi_agent_system.utils.logger import setup_logger


class DataAnalysisAgent:
    """Cleans and analyzes collected records."""

    def __init__(self, llm: BaseChatModel, *, log_level: str = "INFO") -> None:
        self._llm = llm
        self._logger = setup_logger(self.__class__.__name__, level=log_level)

    def run(self, incoming: AgentMessage) -> AgentMessage:
        """Process research output and emit analysis."""
        self._logger.info("Running data analysis on research payload")
        raw_data = incoming.payload.get("raw_data", [])

        cleaned_data = clean_records.invoke({"records": raw_data})
        metrics = descriptive_metrics.invoke({"records": cleaned_data})

        structured_llm = self._llm.with_structured_output(AnalysisOutput)
        result = structured_llm.invoke(
            [
                (
                    "system",
                    "Você é um analista de dados. Gere insights objetivos com base nos dados de entrada.",
                ),
                (
                    "human",
                    f"Resumo de pesquisa: {incoming.payload.get('summary', '')}\n"
                    f"Dados limpos: {cleaned_data}\n"
                    f"Métricas: {metrics}",
                ),
            ]
        )

        payload = result.model_dump()
        payload["cleaned_data"] = cleaned_data
        payload["metrics"] = metrics

        return AgentMessage(
            sender="data_analysis_agent",
            recipient="planning_agent",
            stage="analysis",
            payload=payload,
        )
