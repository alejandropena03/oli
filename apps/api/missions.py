from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from packages.mission_kernel.mission_state import EvidenceRef, Mission, MissionEvent, MissionReport
from packages.mission_kernel.state_machine import InvalidTransition
from packages.mission_store import get_mission_store
from packages.orchestrator import (
    approve_mission,
    complete_approved_draft_outreach,
    create_draft_outreach_mission,
    reject_mission,
    run_weekly_client_report_graph_v1,
)
from packages.orchestrator.slice_001_research_brief import SLICE_001_INPUT, run_research_brief_v1

router = APIRouter(prefix="/missions", tags=["missions"])

_STORE = get_mission_store()


class CreateResearchBriefRequest(BaseModel):
    raw_input: str = SLICE_001_INPUT


class CreateDraftOutreachRequest(BaseModel):
    raw_input: str = "Prepara un mensaje de outreach para una agencia."


class CreateWeeklyClientReportRequest(BaseModel):
    raw_input: str = "Prepara un reporte semanal para el cliente Acme Growth."
    performance_data: dict | None = None


class ApprovalRequest(BaseModel):
    actor: str = "alejandro"
    notes: str | None = None


class RejectionRequest(BaseModel):
    actor: str = "alejandro"
    reason: str


class MissionSummary(BaseModel):
    id: UUID
    status: str
    goal: str | None
    raw_input: str
    permission_class: int | None
    needs_approval: bool
    created_at: str


def _summary(mission: Mission) -> MissionSummary:
    return MissionSummary(
        id=mission.id,
        status=mission.status.value,
        goal=mission.interpreted_intent.goal if mission.interpreted_intent else None,
        raw_input=mission.raw_input,
        permission_class=int(mission.permission_class) if mission.permission_class is not None else None,
        needs_approval=mission.status.value == "awaiting_approval",
        created_at=mission.created_at.isoformat(),
    )


@router.get("", response_model=list[MissionSummary])
def list_missions() -> list[MissionSummary]:
    return [_summary(mission) for mission in _STORE.list()]


@router.post("/research-brief", response_model=Mission)
def create_research_brief(request: CreateResearchBriefRequest) -> Mission:
    mission = run_research_brief_v1(request.raw_input)
    _STORE.save(mission)
    return mission


@router.post("/draft-outreach", response_model=Mission)
def create_draft_outreach(request: CreateDraftOutreachRequest) -> Mission:
    mission = create_draft_outreach_mission(request.raw_input)
    _STORE.save(mission)
    return mission


@router.post("/weekly-client-report", response_model=Mission)
def create_weekly_client_report(request: CreateWeeklyClientReportRequest) -> Mission:
    mission = run_weekly_client_report_graph_v1(
        raw_input=request.raw_input,
        performance_data=request.performance_data,
    )
    _STORE.save(mission)
    return mission


@router.get("/{mission_id}", response_model=Mission)
def get_mission(mission_id: UUID) -> Mission:
    mission = _STORE.get(mission_id)
    if mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission


@router.get("/{mission_id}/events", response_model=list[MissionEvent])
def get_mission_events(mission_id: UUID) -> list[MissionEvent]:
    mission = get_mission(mission_id)
    return mission.events


@router.get("/{mission_id}/evidence", response_model=list[EvidenceRef])
def get_mission_evidence(mission_id: UUID) -> list[EvidenceRef]:
    mission = get_mission(mission_id)
    return mission.evidence


@router.get("/{mission_id}/report", response_model=MissionReport | None)
def get_mission_report(mission_id: UUID) -> MissionReport | None:
    mission = get_mission(mission_id)
    return mission.report


@router.post("/{mission_id}/approve", response_model=Mission)
def approve(mission_id: UUID, request: ApprovalRequest) -> Mission:
    mission = get_mission(mission_id)
    try:
        approved = approve_mission(mission, approved_by=request.actor, notes=request.notes)
        if approved.interpreted_intent and approved.interpreted_intent.goal == "draft_outreach_message":
            approved = complete_approved_draft_outreach(approved)
    except InvalidTransition as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    _STORE.save(approved)
    return approved


@router.post("/{mission_id}/reject", response_model=Mission)
def reject(mission_id: UUID, request: RejectionRequest) -> Mission:
    mission = get_mission(mission_id)
    try:
        rejected = reject_mission(mission, rejected_by=request.actor, reason=request.reason)
    except InvalidTransition as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    _STORE.save(rejected)
    return rejected


def clear_missions_for_tests() -> None:
    _STORE.clear()
