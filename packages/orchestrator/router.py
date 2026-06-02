from __future__ import annotations

from typing import Any

from packages.mission_kernel.mission_state import Mission
from packages.orchestrator.mission_graph import run_weekly_client_report_graph_v1
from packages.orchestrator.weekly_client_report import DEFAULT_WEEKLY_REPORT_INPUT


def run_mission_graph(
    goal: str,
    *,
    raw_input: str | None = None,
    payload: dict[str, Any] | None = None,
) -> Mission:
    if goal == "weekly_client_report":
        return run_weekly_client_report_graph_v1(
            raw_input=raw_input or DEFAULT_WEEKLY_REPORT_INPUT,
            performance_data=payload,
        )
    raise ValueError(f"Unsupported mission graph goal: {goal}")
