from __future__ import annotations

from typing import Any

from langgraph.graph import END, StateGraph

from packages.mission_kernel.mission_state import Mission, MissionSource
from packages.mission_kernel.state_machine import create_mission
from packages.orchestrator.checkpointer import get_checkpointer
from packages.orchestrator.model_adapter import ModelAdapter
from packages.orchestrator.nodes import (
    MissionGraphState,
    classify_permissions_node,
    create_plan_node,
    deliver_node,
    execute_step_node,
    generate_report_node,
    human_approval_node,
    interpret_intent_node,
    retrieve_context_node,
    route_after_execution,
    route_after_plan,
    route_after_validation,
    troubleshoot_node,
    update_memory_node,
    validate_output_node,
)
from packages.orchestrator.weekly_client_report import (
    DEFAULT_WEEKLY_REPORT_DATA,
    DEFAULT_WEEKLY_REPORT_INPUT,
)


def _build_graph_topology() -> StateGraph:
    """Build the mission graph topology (nodes + edges) without a checkpointer."""
    builder = StateGraph(MissionGraphState)
    builder.add_node("interpret_intent", interpret_intent_node)
    builder.add_node("retrieve_context", retrieve_context_node)
    builder.add_node("classify_permissions", classify_permissions_node)
    builder.add_node("create_plan", create_plan_node)
    builder.add_node("human_approval", human_approval_node)
    builder.add_node("execute_step", execute_step_node)
    builder.add_node("troubleshoot", troubleshoot_node)
    builder.add_node("validate_output", validate_output_node)
    builder.add_node("deliver", deliver_node)
    builder.add_node("generate_report", generate_report_node)
    builder.add_node("update_memory", update_memory_node)

    builder.set_entry_point("interpret_intent")
    builder.add_edge("interpret_intent", "retrieve_context")
    builder.add_edge("retrieve_context", "classify_permissions")
    builder.add_edge("classify_permissions", "create_plan")
    builder.add_conditional_edges(
        "create_plan",
        route_after_plan,
        {
            "human_approval": "human_approval",
            "execute_step": "execute_step",
        },
    )
    builder.add_edge("human_approval", "execute_step")
    builder.add_conditional_edges(
        "execute_step",
        route_after_execution,
        {
            "execute_step": "execute_step",
            "troubleshoot": "troubleshoot",
            "validate_output": "validate_output",
        },
    )
    builder.add_edge("troubleshoot", END)
    builder.add_conditional_edges(
        "validate_output",
        route_after_validation,
        {
            "deliver": "deliver",
            "end": END,
        },
    )
    builder.add_edge("deliver", "generate_report")
    builder.add_edge("generate_report", "update_memory")
    builder.add_edge("update_memory", END)
    return builder


def build_weekly_report_graph(*, use_memory_checkpointer: bool = True):
    """Compile the weekly report graph.

    - use_memory_checkpointer=True (default): uses MemorySaver for dev/test.
    - use_memory_checkpointer=False: no checkpointer (stateless, for testing topology).
    - When OLI_MISSION_STORE=sqlalchemy and OLI_DATABASE_URL points to Postgres,
      get_checkpointer() returns PostgresSaver automatically.
    """
    builder = _build_graph_topology()
    checkpointer = get_checkpointer() if use_memory_checkpointer else None
    return builder.compile(checkpointer=checkpointer)


def run_weekly_client_report_graph_v1(
    raw_input: str = DEFAULT_WEEKLY_REPORT_INPUT,
    performance_data: dict[str, Any] | None = None,
    model: ModelAdapter | None = None,
) -> Mission:
    mission = create_mission(raw_input=raw_input, source=MissionSource.CHAT)
    graph = build_weekly_report_graph(use_memory_checkpointer=model is None)
    initial_state: dict[str, Any] = {
        "mission": mission,
        "performance_data": performance_data or DEFAULT_WEEKLY_REPORT_DATA,
    }
    if model is not None:
        initial_state["model"] = model
    config = {"configurable": {"thread_id": str(mission.id)}} if model is None else None
    result = graph.invoke(initial_state, config=config)
    return result["mission"]
