"""
Mission: Communication Cockpit
Quiero un cockpit donde todas mis herramientas de comunicacion (WhatsApp, Slack,
Gmail, Instagram) me lea todos los mensajes, estructure pendientes, haga resumenes
y me recuerde cuando no haya respondido.

Esta mision demuestra el Mission Kernel en una mision real que Oli ejecutaria
cuando tenga conectores. Hoy el kernel funciona completo — los conectores son mock.
"""
from __future__ import annotations

from typing import Any

from packages.mission_kernel.mission_state import (
    CostRecord,
    EvidenceRef,
    InterpretedIntent,
    Mission,
    MissionContext,
    MissionPlan,
    MissionReport,
    MissionSource,
    MissionStatus,
    MissionStep,
    PermissionClass,
    StepStatus,
    ValidationResult,
)
from packages.mission_kernel.policies import max_permission_class, plan_requires_approval
from packages.mission_kernel.state_machine import create_mission, transition


COCKPIT_INPUT = (
    "Quiero un cockpit donde todas mis herramientas de comunicacion: "
    "WhatsApp, Slack, Gmail e Instagram me lean todos los mensajes, "
    "estructuren mis pendientes, me hagan resumenes y me recuerden "
    "cuando no haya respondido algo importante."
)


def run_cockpit_comms_mission(raw_input: str = COCKPIT_INPUT) -> Mission:
    mission = create_mission(raw_input=raw_input, source=MissionSource.CHAT)

    # ── 1. INTERPRETAR INTENCIÓN ─────────────────────────────────────────────
    transition(mission, MissionStatus.INTERPRETING_INTENT, trigger="auto")
    mission.interpreted_intent = InterpretedIntent(
        goal="communication_cockpit_v1",
        success_criteria=[
            "mensajes de WhatsApp, Slack, Gmail e Instagram consolidados en una vista",
            "pendientes estructurados por urgencia y canal",
            "resumen ejecutivo diario de conversaciones activas",
            "alertas de mensajes sin respuesta despues de umbral configurable",
            "ningun mensaje enviado sin aprobacion del usuario",
        ],
        output_format="structured_cockpit_briefing",
        scope={
            "in_scope": [
                "leer mensajes de todos los canales",
                "clasificar por urgencia y tipo",
                "detectar conversaciones sin respuesta",
                "generar resumen y lista de pendientes",
                "notificar al usuario con contexto suficiente para decidir",
            ],
            "out_of_scope": [
                "responder mensajes automaticamente sin aprobacion",
                "acceder a archivos adjuntos sin permiso explicito",
                "leer conversaciones de grupos sin autorizacion por grupo",
                "retener contenido de mensajes en memoria sin consentimiento",
            ],
        },
        confidence=0.88,
    )
    mission.evidence.append(EvidenceRef(
        kind="intent",
        title="Intención interpretada — Communication Cockpit",
        data={
            "goal": mission.interpreted_intent.goal,
            "canales_detectados": ["WhatsApp", "Slack", "Gmail", "Instagram"],
            "tipo_mision": "recurring_digest",
            "frecuencia_sugerida": "diaria o bajo demanda",
            "confidence": mission.interpreted_intent.confidence,
        },
    ))

    # ── 2. RECUPERAR CONTEXTO ────────────────────────────────────────────────
    transition(mission, MissionStatus.RETRIEVING_CONTEXT, trigger="intent_clarified")
    mission.context = MissionContext(
        user_preferences={
            "idioma": "es",
            "formato_resumen": "ejecutivo — maximo 5 items por canal",
            "umbral_sin_respuesta_horas": 4,
            "canales_prioritarios": ["Gmail", "Slack"],
            "privacidad": "ningun contenido de mensajes fuera del dispositivo sin consentimiento",
        },
        company_context={
            "rol_usuario": "founder",
            "volumen_mensajes_estimado": "alto — 50-200 mensajes/dia entre canales",
            "pain_point": "contexto fragmentado, mensajes perdidos, seguimiento manual",
        },
    )
    mission.evidence.append(EvidenceRef(
        kind="context",
        title="Contexto del usuario recuperado",
        data={
            "preferencias": mission.context.user_preferences,
            "memoria_aplicada": [
                "el usuario prefiere resumen ejecutivo sin detalles de cada mensaje",
                "Gmail y Slack son canales de mayor urgencia",
                "umbral de 4 horas para alertas de no-respuesta",
            ],
            "playbooks_aplicables": [],
        },
    ))

    # ── 3. CLASIFICAR PERMISOS ───────────────────────────────────────────────
    transition(mission, MissionStatus.CLASSIFYING_PERMISSIONS, trigger="context_ready")
    steps = _build_cockpit_plan()
    total_permission = max_permission_class(steps)
    mission.permission_class = total_permission
    mission.evidence.append(EvidenceRef(
        kind="permissions",
        title="Clasificación de permisos por paso",
        data={
            "permission_class_total": total_permission.value,
            "label": total_permission.name,
            "razon": (
                "La lectura de mensajes (clase 1) requiere OAuth por canal. "
                "Ningun paso llega a clase 3+ porque esta mision NO envia mensajes. "
                "Solo lee, clasifica y notifica al usuario para que decida."
            ),
            "pasos_por_clase": {
                "clase_0_sin_permiso": ["generar_resumen", "estructurar_pendientes", "generar_briefing"],
                "clase_1_reversible": ["leer_whatsapp", "leer_slack", "leer_gmail", "leer_instagram", "detectar_sin_respuesta"],
                "clase_3_nunca_automatica": ["responder_mensajes — FUERA DE SCOPE"],
            },
        },
    ))

    # ── 4. CREAR PLAN ────────────────────────────────────────────────────────
    transition(mission, MissionStatus.PLANNING, trigger="permissions_set")
    mission.plan = MissionPlan(
        steps=steps,
        total_permission_class=total_permission,
        estimates={
            "duration_ms": 3 * 60 * 1000,
            "cost_usd": 0.04,
            "human_time_saved_hr": 0.5,
        },
    )
    mission.evidence.append(EvidenceRef(
        kind="plan",
        title="Plan detallado — Communication Cockpit",
        data={
            "total_steps": len(steps),
            "steps": [
                {
                    "order": s.order,
                    "description": s.description,
                    "executor": s.executor,
                    "tools": s.required_tools,
                    "permission_class": s.permission_class.name,
                }
                for s in steps
            ],
            "topologia": "sequential_pipeline — cada paso depende del anterior",
            "approval_gate": plan_requires_approval(mission.plan),
        },
    ))

    # Esta mision es clase 1 — no necesita aprobacion previa al ejecutar
    if plan_requires_approval(mission.plan):
        transition(mission, MissionStatus.AWAITING_APPROVAL, trigger="plan_ready")
        return mission

    # ── 5. EJECUTAR ──────────────────────────────────────────────────────────
    transition(mission, MissionStatus.EXECUTING, trigger="plan_ready")
    cockpit_payload = _execute_mock_cockpit(mission)

    # ── 6. VALIDAR ───────────────────────────────────────────────────────────
    transition(mission, MissionStatus.VALIDATING, trigger="all_steps_completed")
    mission.validation_result = _validate_cockpit(mission, cockpit_payload)

    if not mission.validation_result.passed:
        transition(
            mission, MissionStatus.FAILED,
            trigger="validation_failed",
            reason="cockpit output no cumple criterios de exito",
        )
        return mission

    # ── 7. ENTREGAR ──────────────────────────────────────────────────────────
    transition(mission, MissionStatus.DELIVERING, trigger="validation_passed")
    mission.output = cockpit_payload["briefing"]
    mission.evidence.append(EvidenceRef(
        kind="deliverable",
        title="Communication Cockpit Briefing — listo para el usuario",
        data={"briefing": mission.output},
    ))

    # ── 8. REPORTE ───────────────────────────────────────────────────────────
    transition(mission, MissionStatus.GENERATING_REPORT, trigger="delivery_confirmed")
    mission.cost = CostRecord(
        input_tokens=1200,
        output_tokens=600,
        model_cost_usd=0.04,
        tool_cost_usd=0.0,
        duration_ms=3 * 60 * 1000,
        human_time_saved_hr=0.5,
    )
    mission.report = MissionReport(
        mission_id=mission.id,
        summary=(
            "Cockpit de comunicaciones ejecutado. "
            "4 canales leidos, pendientes estructurados, "
            "alertas de no-respuesta detectadas, briefing entregado."
        ),
        deliverable_description=(
            "Briefing consolidado con resumen por canal, "
            "pendientes priorizados y alertas de seguimiento."
        ),
        steps_completed=sum(1 for s in mission.plan.steps if s.status == StepStatus.COMPLETED),
        steps_total=len(mission.plan.steps),
        validation_result=mission.validation_result,
        cost=mission.cost,
        playbook_candidate=True,
        playbook_candidate_reason=(
            "Mision completamente repetible — mismo flujo diario o bajo demanda. "
            "Candidata a convertirse en playbook automatico programado."
        ),
    )

    # ── 9. MEMORIA ───────────────────────────────────────────────────────────
    transition(mission, MissionStatus.UPDATING_MEMORY, trigger="report_generated")
    mission.evidence.append(EvidenceRef(
        kind="memory_suggestion",
        title="Sugerencias de memoria post-mision",
        data={
            "recordar": [
                "usuario prefiere resumen de maximo 5 items por canal",
                "Gmail y Slack son canales prioritarios",
                "umbral de no-respuesta: 4 horas",
            ],
            "playbook_candidato": "communication-cockpit-daily-v1",
            "frecuencia_sugerida": "diaria a las 9am o bajo demanda",
            "conectores_requeridos_para_v1_real": [
                "WhatsApp Business API o MCP",
                "Slack MCP (disponible hoy)",
                "Gmail MCP (disponible hoy)",
                "Instagram Graph API",
            ],
        },
    ))

    transition(mission, MissionStatus.COMPLETED, trigger="memory_updated")
    return mission


# ── PLAN ─────────────────────────────────────────────────────────────────────

def _build_cockpit_plan() -> list[MissionStep]:
    return [
        MissionStep(
            order=1,
            description="Leer mensajes de WhatsApp (ultimas 4 horas)",
            executor="ExecutionSuboperator",
            required_tools=["whatsapp_connector"],
            permission_class=PermissionClass.INTERNAL_REVERSIBLE,
        ),
        MissionStep(
            order=2,
            description="Leer mensajes de Slack (canales autorizados)",
            executor="ExecutionSuboperator",
            required_tools=["slack_mcp"],
            permission_class=PermissionClass.INTERNAL_REVERSIBLE,
        ),
        MissionStep(
            order=3,
            description="Leer mensajes de Gmail (inbox, no spam)",
            executor="ExecutionSuboperator",
            required_tools=["gmail_mcp"],
            permission_class=PermissionClass.INTERNAL_REVERSIBLE,
        ),
        MissionStep(
            order=4,
            description="Leer DMs de Instagram",
            executor="ExecutionSuboperator",
            required_tools=["instagram_graph_api"],
            permission_class=PermissionClass.INTERNAL_REVERSIBLE,
        ),
        MissionStep(
            order=5,
            description="Detectar conversaciones sin respuesta por encima del umbral",
            executor="Orchestrator",
            required_tools=[],
            permission_class=PermissionClass.READ_DRAFT,
        ),
        MissionStep(
            order=6,
            description="Clasificar mensajes por urgencia y tipo (accion requerida / FYI / spam)",
            executor="Orchestrator",
            required_tools=[],
            permission_class=PermissionClass.READ_DRAFT,
        ),
        MissionStep(
            order=7,
            description="Generar resumen ejecutivo por canal",
            executor="Orchestrator",
            required_tools=[],
            permission_class=PermissionClass.READ_DRAFT,
        ),
        MissionStep(
            order=8,
            description="Estructurar lista de pendientes priorizados",
            executor="Orchestrator",
            required_tools=[],
            permission_class=PermissionClass.READ_DRAFT,
        ),
        MissionStep(
            order=9,
            description="Entregar briefing consolidado al usuario",
            executor="Orchestrator",
            required_tools=[],
            permission_class=PermissionClass.READ_DRAFT,
        ),
    ]


# ── EJECUCIÓN MOCK ────────────────────────────────────────────────────────────

def _execute_mock_cockpit(mission: Mission) -> dict[str, Any]:
    assert mission.plan is not None

    mock_data: dict[str, Any] = {
        "whatsapp": {
            "mensajes_nuevos": 12,
            "sin_respuesta": [
                {"de": "Carlos (cliente)", "mensaje": "Me mandas el contrato?", "hace": "5h", "urgencia": "alta"},
                {"de": "Maria (proveedor)", "mensaje": "Confirmamos para el jueves?", "hace": "3h", "urgencia": "media"},
            ],
            "fyi": 10,
        },
        "slack": {
            "mensajes_nuevos": 34,
            "sin_respuesta": [
                {"de": "@laura", "canal": "#producto", "mensaje": "Revisas el PR antes del standup?", "hace": "2h", "urgencia": "alta"},
            ],
            "fyi": 33,
        },
        "gmail": {
            "mensajes_nuevos": 8,
            "sin_respuesta": [
                {"de": "investor@vc.com", "asunto": "Follow-up call Oli", "hace": "6h", "urgencia": "critica"},
            ],
            "fyi": 7,
        },
        "instagram": {
            "mensajes_nuevos": 5,
            "sin_respuesta": [],
            "fyi": 5,
        },
    }

    briefing = {
        "resumen_ejecutivo": (
            "4 canales revisados. 4 conversaciones requieren tu respuesta hoy. "
            "1 es critica (email de investor). Tiempo estimado para responder todo: 20 min."
        ),
        "alertas_criticas": [
            {
                "canal": "Gmail",
                "de": "investor@vc.com",
                "asunto": "Follow-up call Oli",
                "sin_respuesta_hace": "6h",
                "urgencia": "CRITICA",
                "accion_sugerida": "Responder con disponibilidad esta semana",
            },
        ],
        "pendientes_por_canal": {
            "WhatsApp": [
                "Carlos (cliente) — contrato pendiente — 5h sin respuesta",
                "Maria (proveedor) — confirmar jueves — 3h sin respuesta",
            ],
            "Slack": [
                "@laura en #producto — revisar PR antes de standup — 2h sin respuesta",
            ],
            "Gmail": [
                "investor@vc.com — follow-up call — 6h sin respuesta",
            ],
            "Instagram": [],
        },
        "totales": {
            "mensajes_nuevos": 59,
            "requieren_accion": 4,
            "solo_fyi": 55,
            "canales_con_alertas": ["Gmail", "WhatsApp", "Slack"],
        },
        "nota_de_oli": (
            "No respondí nada. Ningún mensaje fue enviado. "
            "Esta es tu lista de pendientes — tú decides qué responder y cuándo. "
            "Si quieres que prepare borradores para alguno, dímelo."
        ),
    }

    for step in mission.plan.steps:
        step.status = StepStatus.EXECUTING
        if step.order == 1:
            step.output = mock_data["whatsapp"]
        elif step.order == 2:
            step.output = mock_data["slack"]
        elif step.order == 3:
            step.output = mock_data["gmail"]
        elif step.order == 4:
            step.output = mock_data["instagram"]
        elif step.order == 5:
            step.output = {"sin_respuesta_total": 4, "criticas": 1}
        elif step.order == 6:
            step.output = {"accion_requerida": 4, "fyi": 55}
        elif step.order == 7:
            step.output = {c: d.get("mensajes_nuevos", 0) for c, d in mock_data.items()}
        elif step.order == 8:
            step.output = briefing["pendientes_por_canal"]
        elif step.order == 9:
            step.output = {"entregado": True}
        step.status = StepStatus.COMPLETED

    mission.evidence.append(EvidenceRef(
        kind="execution",
        title="Datos mock de canales de comunicacion",
        data=mock_data,
    ))

    return {"mock_data": mock_data, "briefing": briefing}


# ── VALIDACIÓN ────────────────────────────────────────────────────────────────

def _validate_cockpit(mission: Mission, payload: dict[str, Any]) -> ValidationResult:
    briefing = payload["briefing"]
    pendientes = briefing["pendientes_por_canal"]
    totales = briefing["totales"]

    criteria = [
        {
            "criterion": "mensajes de 4 canales consolidados",
            "passed": len(pendientes) == 4,
            "evidence": f"{len(pendientes)} canales en el briefing",
        },
        {
            "criterion": "pendientes estructurados por canal",
            "passed": all(isinstance(v, list) for v in pendientes.values()),
            "evidence": "todos los canales tienen lista de pendientes",
        },
        {
            "criterion": "resumen ejecutivo presente",
            "passed": bool(briefing.get("resumen_ejecutivo")),
            "evidence": briefing.get("resumen_ejecutivo", "")[:60] + "...",
        },
        {
            "criterion": "alertas de no-respuesta detectadas",
            "passed": totales["requieren_accion"] > 0,
            "evidence": f"{totales['requieren_accion']} mensajes requieren accion",
        },
        {
            "criterion": "ningun mensaje enviado sin aprobacion",
            "passed": "No respondí nada" in briefing.get("nota_de_oli", ""),
            "evidence": "nota_de_oli confirma que Oli no actuó de forma autónoma",
        },
    ]
    passed = all(c["passed"] for c in criteria)
    result = ValidationResult(
        passed=passed,
        criteria_results=criteria,
        score=sum(1 for c in criteria if c["passed"]) / len(criteria),
        auto_repair_possible=False,
    )
    mission.evidence.append(EvidenceRef(
        kind="validation",
        title="Validacion — Communication Cockpit",
        data=result.model_dump(mode="json"),
    ))
    return result
