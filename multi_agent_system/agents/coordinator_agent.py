"""Coordinator/orchestrator agent for the multi-agent workflow."""

from __future__ import annotations

import asyncio
from typing import Any, Callable, TypeVar

from multi_agent_system.agents.critic_agent import CriticAgent
from multi_agent_system.agents.data_analysis_agent import DataAnalysisAgent
from multi_agent_system.agents.messages import AgentMessage
from multi_agent_system.agents.planning_agent import PlanningAgent
from multi_agent_system.agents.research_agent import ResearchAgent
from multi_agent_system.config import Settings
from multi_agent_system.memory.shared_memory import SharedMemory
from multi_agent_system.utils.logger import setup_logger

RunResult = TypeVar("RunResult")


class CoordinatorAgent:
    """Coordinates all agents, controls state, and consolidates outputs."""

    def __init__(
        self,
        research_agent: ResearchAgent,
        analysis_agent: DataAnalysisAgent,
        planning_agent: PlanningAgent,
        critic_agent: CriticAgent,
        memory: SharedMemory,
        settings: Settings,
    ) -> None:
        self._research_agent = research_agent
        self._analysis_agent = analysis_agent
        self._planning_agent = planning_agent
        self._critic_agent = critic_agent
        self._memory = memory
        self._settings = settings
        self._logger = setup_logger(self.__class__.__name__, level=settings.log_level)

    async def run(self, user_input: str) -> dict[str, Any]:
        """Execute the end-to-end workflow and consolidate final output."""
        self._logger.info("Workflow started")
        self._memory.write("user_input", user_input)

        research_msg = await self._with_retry(lambda: self._research_agent.run(user_input), "research")
        self._memory.write("research", research_msg.payload)

        analysis_msg = await self._with_retry(
            lambda: self._analysis_agent.run(research_msg), "analysis"
        )
        self._memory.write("analysis", analysis_msg.payload)

        planning_msg = await self._with_retry(
            lambda: self._planning_agent.run(analysis_msg), "planning"
        )
        self._memory.write("planning", planning_msg.payload)

        critic_msg = await self._with_retry(
            lambda: self._critic_agent.run(research_msg, analysis_msg, planning_msg), "critique"
        )
        self._memory.write("critique", critic_msg.payload)

        final_output = self._consolidate(research_msg, analysis_msg, planning_msg, critic_msg)
        self._memory.write("final_output", final_output)
        self._logger.info("Workflow completed")
        return final_output

    async def _with_retry(self, fn: Callable[[], RunResult], stage: str) -> RunResult:
        """Run a stage with bounded retries and timeout control."""
        for attempt in range(1, self._settings.max_retries + 2):
            try:
                self._logger.info("Stage=%s attempt=%s", stage, attempt)
                return await asyncio.wait_for(
                    asyncio.to_thread(fn), timeout=self._settings.timeout_seconds
                )
            except Exception as exc:  # noqa: BLE001
                if attempt > self._settings.max_retries:
                    self._logger.exception("Stage %s failed after retries: %s", stage, exc)
                    raise
                self._logger.warning("Stage %s failed (attempt=%s): %s", stage, attempt, exc)
                await asyncio.sleep(0.8 * attempt)
        raise RuntimeError(f"Stage {stage} failed unexpectedly")

    def _consolidate(
        self,
        research: AgentMessage,
        analysis: AgentMessage,
        planning: AgentMessage,
        critique: AgentMessage,
    ) -> dict[str, Any]:
        """Create final structured response."""
        return {
            "query": self._memory.read("user_input", ""),
            "research": research.payload,
            "analysis": analysis.payload,
            "planning": planning.payload,
            "critique": critique.payload,
            "status": "completed",
        }
