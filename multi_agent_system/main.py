"""CLI entry point for the collaborative multi-agent system."""

from __future__ import annotations

import argparse
import asyncio
import json

from multi_agent_system.agents.coordinator_agent import CoordinatorAgent
from multi_agent_system.agents.critic_agent import CriticAgent
from multi_agent_system.agents.data_analysis_agent import DataAnalysisAgent
from multi_agent_system.agents.planning_agent import PlanningAgent
from multi_agent_system.agents.research_agent import ResearchAgent
from multi_agent_system.config import settings
from multi_agent_system.memory.shared_memory import SharedMemory
from multi_agent_system.utils.llm_factory import create_chat_model


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run the LangChain multi-agent workflow.")
    parser.add_argument("query", type=str, help="Pergunta inicial enviada pelo usuário")
    return parser.parse_args()


async def run_workflow(query: str) -> dict:
    """Instantiate dependencies and execute the orchestration workflow."""
    llm = create_chat_model(settings)
    memory = SharedMemory()

    coordinator = CoordinatorAgent(
        research_agent=ResearchAgent(llm, log_level=settings.log_level),
        analysis_agent=DataAnalysisAgent(llm, log_level=settings.log_level),
        planning_agent=PlanningAgent(llm, log_level=settings.log_level),
        critic_agent=CriticAgent(llm, log_level=settings.log_level),
        memory=memory,
        settings=settings,
    )
    return await coordinator.run(query)


def main() -> None:
    """Run the CLI app."""
    args = parse_args()
    output = asyncio.run(run_workflow(args.query))
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
