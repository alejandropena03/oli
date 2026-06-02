from packages.mission_kernel.mission_state import MissionStatus, PermissionClass, StepStatus
from packages.orchestrator import run_weekly_client_report_v1


def test_weekly_client_report_runs_end_to_end_for_agency_team():
    mission = run_weekly_client_report_v1()

    assert mission.status == MissionStatus.COMPLETED
    assert mission.permission_class == PermissionClass.READ_DRAFT
    assert mission.interpreted_intent is not None
    assert mission.interpreted_intent.goal == "weekly_client_report"
    assert mission.plan is not None
    assert all(step.status == StepStatus.COMPLETED for step in mission.plan.steps)
    assert mission.validation_result is not None
    assert mission.validation_result.passed
    assert mission.report is not None
    assert mission.report.playbook_candidate
    assert "Reporte semanal" in mission.output
    assert "Proximos pasos" in mission.output


def test_weekly_client_report_keeps_evidence_for_auditability():
    mission = run_weekly_client_report_v1()

    evidence_kinds = {item.kind for item in mission.evidence}
    assert {
        "input_data",
        "plan",
        "computed_metrics",
        "insights",
        "validation",
        "deliverable",
        "memory_suggestion",
    } <= evidence_kinds

