from packages.mission_kernel.mission_state import MissionStatus, PermissionClass
from packages.orchestrator import (
    approve_mission,
    complete_approved_draft_outreach,
    create_draft_outreach_mission,
)


def test_draft_outreach_stops_at_human_approval_gate():
    mission = create_draft_outreach_mission()

    assert mission.status == MissionStatus.AWAITING_APPROVAL
    assert mission.permission_class == PermissionClass.EXTERNAL_BRAND_IMPACT
    assert mission.output is not None
    assert any(item.kind == "draft" for item in mission.evidence)


def test_approval_records_human_decision_and_resumes_mission():
    mission = create_draft_outreach_mission()

    approved = approve_mission(mission, approved_by="alejandro", notes="approved in test")

    assert approved.status == MissionStatus.EXECUTING
    assert approved.approval_records[0]["decision"] == "approved"
    assert any(item.kind == "approval" for item in approved.evidence)


def test_approved_draft_outreach_completes_with_audit_trail():
    mission = create_draft_outreach_mission()
    approved = approve_mission(mission, approved_by="alejandro")

    completed = complete_approved_draft_outreach(approved)

    assert completed.status == MissionStatus.COMPLETED
    assert completed.validation_result is not None
    assert completed.validation_result.passed
    assert completed.report is not None
    assert completed.report.playbook_candidate
    assert any(item.kind == "simulated_external_action" for item in completed.evidence)
