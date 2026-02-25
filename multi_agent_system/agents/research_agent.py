"""Research agent implementation."""

from __future__ import annotations

from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel

from multi_agent_system.agents.messages import AgentMessage, ResearchOutput
from multi_agent_system.tools.github_tools import github_recent_issues, github_repo_summary
from multi_agent_system.tools.web_tools import http_get_json, web_search
from multi_agent_system.utils.logger import setup_logger


class ResearchAgent:
    """Collects raw information from web, APIs, and GitHub."""

    def __init__(self, llm: BaseChatModel, *, log_level: str = "INFO") -> None:
        self._llm = llm
        self._logger = setup_logger(self.__class__.__name__, level=log_level)

    def run(self, user_query: str) -> AgentMessage:
        """Run research and return structured output."""
        self._logger.info("Starting research for query: %s", user_query)

        web_result = web_search.invoke({"query": user_query})
        repo_result = github_repo_summary.invoke({"owner": "langchain-ai", "repo": "langchain"})
        issues_result = github_recent_issues.invoke(
            {"owner": "langchain-ai", "repo": "langchain", "limit": 3}
        )

        api_result: dict[str, Any] = {}
        try:
            api_result = http_get_json.invoke({"url": "https://api.github.com/rate_limit"})
        except Exception as exc:  # noqa: BLE001
            self._logger.warning("External API call failed: %s", exc)

        structured_llm = self._llm.with_structured_output(ResearchOutput)
        prompt = (
            "Você é um agente de pesquisa. Sintetize os dados coletados em português. "
            "Priorize factualidade e preserve links de fonte."
        )
        result = structured_llm.invoke(
            [
                ("system", prompt),
                (
                    "human",
                    f"Consulta do usuário: {user_query}\n"
                    f"Dados web: {web_result}\n"
                    f"Dados repositório: {repo_result}\n"
                    f"Issues: {issues_result}\n"
                    f"Dados API: {api_result}",
                ),
            ]
        )

        payload = result.model_dump()
        payload["sources"] = payload.get("sources", []) + [repo_result]
        payload["raw_data"] = payload.get("raw_data", []) + issues_result

        return AgentMessage(
            sender="research_agent",
            recipient="data_analysis_agent",
            stage="research",
            payload=payload,
        )
