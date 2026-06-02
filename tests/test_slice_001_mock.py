from packages.mission_kernel.mission_state import MissionStatus, PermissionClass, StepStatus
from packages.orchestrator import run_research_brief_v1


def test_slice_001_research_brief_runs_end_to_end_in_mock_mode():
    mission = run_research_brief_v1()

    assert mission.status == MissionStatus.COMPLETED
    assert mission.permission_class == PermissionClass.READ_DRAFT
    assert mission.interpreted_intent is not None
    assert mission.interpreted_intent.goal == "competitor_research_brief"
    assert mission.plan is not None
    assert len(mission.plan.steps) == 7
    assert all(step.status == StepStatus.COMPLETED for step in mission.plan.steps)
    assert mission.validation_result is not None
    assert mission.validation_result.passed
    assert mission.report is not None
    assert mission.report.playbook_candidate
    assert "supervisor de ejecucion" in mission.output


def test_slice_001_leaves_auditable_trace():
    mission = run_research_brief_v1()

    event_names = [event.to_status for event in mission.events]
    assert event_names == [
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
    evidence_kinds = {item.kind for item in mission.evidence}
    assert {"context", "plan", "mock_research", "validation", "deliverable", "memory_suggestion"} <= evidence_kinds

