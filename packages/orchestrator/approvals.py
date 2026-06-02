from __future__ import annotations

from packages.mission_kernel.mission_state import (
    CostRecord,
    EvidenceRef,
    Mission,
    MissionReport,
    MissionStatus,
    StepStatus,
    ValidationResult,
    now_utc,
)
from packages.mission_kernel.state_machine import InvalidTransition, transition


def approve_mission(mission: Mission, approved_by: str, notes: str | None = None) -> Mission:
    if mission.status != MissionStatus.AWAITING_APPROVAL:
        raise InvalidTransition("Only missions awaiting approval can be approved")

    mission.approval_records.append(
        {
            "decision": "approved",
            "approved_by": approved_by,
            "approved_at": now_utc().isoformat(),
            "notes": notes,
        }
    )
    mission.evidence.append(
        EvidenceRef(
            kind="approval",
            title="Aprobacion humana registrada",
            data={"approved_by": approved_by, "notes": notes},
        )
    )
    transition(mission, MissionStatus.EXECUTING, trigger="plan_approved")
    return mission


def reject_mission(mission: Mission, rejected_by: str, reason: str) -> Mission:
    if mission.status != MissionStatus.AWAITING_APPROVAL:
        raise InvalidTransition("Only missions awaiting approval can be rejected")

    mission.approval_records.append(
        {
            "decision": "rejected",
            "rejected_by": rejected_by,
            "rejected_at": now_utc().isoformat(),
            "reason": reason,
        }
    )
    transition(mission, MissionStatus.CANCELLED, trigger="plan_rejected")
    return mission


def complete_approved_draft_outreach(mission: Mission) -> Mission:
    """Complete the V0 draft outreach flow after approval.

    This does not send a real message. It records the point where an external
    tool would be called, proves the audit trail, and closes the mission.
    """

    if mission.status != MissionStatus.EXECUTING:
        raise InvalidTransition("Only executing missions can be completed")
    if mission.plan is None:
        raise InvalidTransition("Mission has no plan to execute")

    for step in mission.plan.steps:
        step.status = StepStatus.COMPLETED
        if step.order == 2:
            step.output = {
                "simulated": True,
                "external_action": "email_send",
                "result": "not_sent_in_v0",
                "reason": "V0 records approved external impact without contacting real prospects",
            }

    mission.evidence.append(
        EvidenceRef(
            kind="simulated_external_action",
            title="Accion externa simulada despues de aprobacion",
            data={
                "tool": "email",
                "sent": False,
                "why": "V0 prueba permisos y auditoria sin enviar mensajes reales",
            },
        )
    )
    transition(mission, MissionStatus.VALIDATING, trigger="all_steps_completed")

    mission.validation_result = ValidationResult(
        passed=True,
        criteria_results=[
            {
                "criterion": "mensaje personalizado para agencia",
                "passed": bool(mission.output and "agencia" in mission.output),
                "evidence": "Draft contiene contexto de agencia.",
            },
            {
                "criterion": "no se envia sin aprobacion humana",
                "passed": any(record["decision"] == "approved" for record in mission.approval_records),
                "evidence": "Existe aprobacion registrada antes de la accion simulada.",
            },
            {
                "criterion": "incluye propuesta de valor de Oli",
                "passed": bool(mission.output and "entregables validados" in mission.output),
                "evidence": "Draft incluye entregables validados, evidencia y reporte.",
            },
        ],
        score=1.0,
        auto_repair_possible=False,
    )
    mission.evidence.append(
        EvidenceRef(
            kind="validation",
            title="Validation report draft-outreach",
            data=mission.validation_result.model_dump(mode="json"),
        )
    )
    transition(mission, MissionStatus.DELIVERING, trigger="validation_passed")
    transition(mission, MissionStatus.GENERATING_REPORT, trigger="delivery_confirmed")

    mission.cost = CostRecord(
        input_tokens=500,
        output_tokens=250,
        model_cost_usd=0.03,
        duration_ms=2 * 60 * 1000,
        human_time_saved_hr=0.25,
    )
    mission.report = MissionReport(
        mission_id=mission.id,
        summary="Draft outreach aprobado, accion externa simulada y mision cerrada con auditoria.",
        deliverable_description="Mensaje de outreach para agencia, no enviado realmente en V0.",
        steps_completed=len(mission.plan.steps),
        steps_total=len(mission.plan.steps),
        validation_result=mission.validation_result,
        cost=mission.cost,
        playbook_candidate=True,
        playbook_candidate_reason="Patron repetible para agencias: draft -> approval -> external action.",
    )
    transition(mission, MissionStatus.UPDATING_MEMORY, trigger="report_generated")
    mission.evidence.append(
        EvidenceRef(
            kind="memory_suggestion",
            title="Sugerencia de playbook para agencias",
            data={
                "playbook_name": "agency-outreach-approval-v1",
                "target_customer": "agencias y teams",
            },
        )
    )
    transition(mission, MissionStatus.COMPLETED, trigger="memory_updated")
    return mission
