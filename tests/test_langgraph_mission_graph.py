from packages.mission_kernel.mission_state import MissionStatus, PermissionClass, StepStatus
from packages.orchestrator.mission_graph import (
    build_weekly_report_graph,
    run_weekly_client_report_graph_v1,
)


def test_weekly_report_langgraph_builds_and_runs_to_completion():
    graph = build_weekly_report_graph(use_memory_checkpointer=False)

    mission = run_weekly_client_report_graph_v1()

    assert graph is not None
    assert mission.status == MissionStatus.COMPLETED
    assert mission.permission_class == PermissionClass.READ_DRAFT
    assert mission.validation_result is not None
    assert mission.validation_result.passed
    assert mission.report is not None
    assert mission.report.playbook_candidate
    assert all(step.status == StepStatus.COMPLETED for step in mission.plan.steps)


def test_weekly_report_langgraph_compiles_with_memory_checkpointer():
    graph = build_weekly_report_graph()

    assert graph is not None


def test_weekly_report_langgraph_preserves_tdd_node_state_flow():
    mission = run_weekly_client_report_graph_v1()

    transitions = [event.to_status for event in mission.events]

    assert transitions == [
        MissionStatus.INTAKE_RECEIVED,
        MissionStatus.INTERPRETING_INTENT,
        MissionStatus.RETRIEVING_CONTEXT,
        MissionStatus.CLASSIFYING_PERMISSIONS,
        MissionStatus.PLANNING,
        MissionStatus.EXECUTING,
        MissionStatus.VALIDATING,
        MissionStatus.DELIVERING,
        MissionStatus.GENERATING_REPORT,
        MissionStatus.UPDATING_MEMORY,
        MissionStatus.COMPLETED,
    ]


def test_weekly_report_langgraph_records_model_routing_decision():
    mission = run_weekly_client_report_graph_v1()

    routing_evidence = [item for item in mission.evidence if item.kind == "model_routing"]

    assert len(routing_evidence) == 1
    assert routing_evidence[0].data["task_type"] == "report_generation"
    assert routing_evidence[0].data["tier"] == "development_fallback"
