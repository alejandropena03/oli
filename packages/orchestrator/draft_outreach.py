from __future__ import annotations

from packages.mission_kernel.mission_state import (
    EvidenceRef,
    InterpretedIntent,
    Mission,
    MissionContext,
    MissionPlan,
    MissionSource,
    MissionStatus,
    MissionStep,
    PermissionClass,
)
from packages.mission_kernel.policies import max_permission_class, plan_requires_approval
from packages.mission_kernel.state_machine import create_mission, transition


DEFAULT_OUTREACH_INPUT = (
    "Prepara un mensaje de outreach para una agencia interesada en automatizar reportes semanales."
)


def create_draft_outreach_mission(raw_input: str = DEFAULT_OUTREACH_INPUT) -> Mission:
    """Create a mission that intentionally stops at the approval gate.

    V0 uses this to prove the permission model: class 3 work can be planned and
    drafted, but it cannot execute external/brand-impact actions without human
    approval.
    """

    mission = create_mission(raw_input=raw_input, source=MissionSource.CHAT)

    transition(mission, MissionStatus.INTERPRETING_INTENT, trigger="auto")
    mission.interpreted_intent = InterpretedIntent(
        goal="draft_outreach_message",
        success_criteria=[
            "mensaje personalizado para agencia",
            "no se envia sin aprobacion humana",
            "incluye propuesta de valor de Oli",
        ],
        output_format="draft_message",
        scope={
            "in_scope": ["draft", "agency_context", "approval_gate"],
            "out_of_scope": ["send_email", "crm_update"],
        },
        confidence=0.88,
    )

    transition(mission, MissionStatus.RETRIEVING_CONTEXT, trigger="intent_clarified")
    mission.context = MissionContext(
        user_preferences={"tone": "directo, profesional, critico"},
        company_context={
            "target_customer": "agencias y teams",
            "oli_value": "misiones auditables con evidencia y reportes repetibles",
        },
    )

    transition(mission, MissionStatus.CLASSIFYING_PERMISSIONS, trigger="context_ready")
    steps = [
        MissionStep(
            order=1,
            description="Redactar mensaje de outreach",
            executor="GrowthSuboperator",
            required_tools=["development_model"],
            permission_class=PermissionClass.READ_DRAFT,
        ),
        MissionStep(
            order=2,
            description="Enviar mensaje al prospecto",
            executor="ExecutionSuboperator",
            required_tools=["email"],
            permission_class=PermissionClass.EXTERNAL_BRAND_IMPACT,
            reversible=False,
        ),
    ]
    total_permission = max_permission_class(steps)
    mission.permission_class = total_permission

    transition(mission, MissionStatus.PLANNING, trigger="permissions_set")
    mission.plan = MissionPlan(
        steps=steps,
        total_permission_class=total_permission,
        estimates={
            "duration_ms": 2 * 60 * 1000,
            "cost_usd": 0.03,
            "human_time_saved_hr": 0.25,
        },
    )
    mission.output = (
        "Hola, vi que su agencia probablemente dedica horas a reportes y seguimiento operativo. "
        "Estoy construyendo Oli: un supervisor de misiones que convierte solicitudes en entregables "
        "validados, con evidencia y reporte. Podria ayudarles a volver repetibles sus reportes "
        "semanales y reducir trabajo manual sin perder control humano."
    )
    mission.evidence.append(
        EvidenceRef(
            kind="draft",
            title="Mensaje preparado, pendiente de aprobacion",
            data={"draft": mission.output},
        )
    )

    if plan_requires_approval(mission.plan):
        transition(mission, MissionStatus.AWAITING_APPROVAL, trigger="plan_ready")
    else:
        transition(mission, MissionStatus.EXECUTING, trigger="plan_ready")

    return mission
