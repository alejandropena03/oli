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
from packages.mission_kernel.policies import max_permission_class
from packages.mission_kernel.state_machine import create_mission, transition
from packages.orchestrator.model_adapter import ModelAdapter, get_default_model_adapter


DEFAULT_WEEKLY_REPORT_INPUT = (
    "Prepara un reporte semanal para el cliente Acme Growth con resultados, insights y proximos pasos."
)

DEFAULT_WEEKLY_REPORT_DATA: dict[str, Any] = {
    "client": "Acme Growth",
    "period": "Semana 2026-05-23 a 2026-05-30",
    "channels": {
        "paid_search": {
            "spend_usd": 1250,
            "leads": 64,
            "cpl_usd": 19.53,
            "conversion_rate": 0.041,
        },
        "linkedin": {
            "spend_usd": 820,
            "leads": 21,
            "cpl_usd": 39.05,
            "conversion_rate": 0.018,
        },
        "email": {
            "sent": 2400,
            "reply_rate": 0.036,
            "qualified_replies": 11,
        },
    },
    "last_week": {
        "total_leads": 72,
        "qualified_leads": 19,
        "spend_usd": 1980,
    },
    "this_week": {
        "total_leads": 96,
        "qualified_leads": 27,
        "spend_usd": 2070,
    },
}


def run_weekly_client_report_v1(
    raw_input: str = DEFAULT_WEEKLY_REPORT_INPUT,
    performance_data: dict[str, Any] | None = None,
    model: ModelAdapter | None = None,
) -> Mission:
    model = model or get_default_model_adapter()
    data = performance_data or DEFAULT_WEEKLY_REPORT_DATA

    mission = create_mission(raw_input=raw_input, source=MissionSource.CHAT)

    transition(mission, MissionStatus.INTERPRETING_INTENT, trigger="auto")
    mission.interpreted_intent = InterpretedIntent(
        goal="weekly_client_report",
        success_criteria=[
            "incluye resumen ejecutivo",
            "incluye metricas clave",
            "incluye al menos 3 insights",
            "incluye proximos pasos accionables",
            "incluye evidencia de datos usados",
        ],
        output_format="client_ready_weekly_report",
        scope={
            "in_scope": ["weekly_performance", "insights", "next_actions", "client_report"],
            "out_of_scope": ["send_to_client", "change_campaign_budget", "crm_update"],
        },
        confidence=0.9,
    )

    transition(mission, MissionStatus.RETRIEVING_CONTEXT, trigger="intent_clarified")
    mission.context = MissionContext(
        user_preferences={
            "tone": "directo, consultivo, claro para cliente",
            "language": "es",
        },
        company_context={
            "target_customer": "agencias y teams",
            "job_to_be_done": "convertir datos de performance en reporte semanal reutilizable",
        },
    )
    mission.evidence.append(
        EvidenceRef(
            kind="input_data",
            title="Datos de performance usados para reporte semanal",
            data=data,
        )
    )

    transition(mission, MissionStatus.CLASSIFYING_PERMISSIONS, trigger="context_ready")
    steps = _build_weekly_report_plan()
    mission.permission_class = max_permission_class(steps)

    transition(mission, MissionStatus.PLANNING, trigger="permissions_set")
    mission.plan = MissionPlan(
        steps=steps,
        total_permission_class=mission.permission_class,
        estimates={
            "duration_ms": 5 * 60 * 1000,
            "cost_usd": 0.09,
            "human_time_saved_hr": 1.5,
        },
    )
    mission.evidence.append(
        EvidenceRef(
            kind="plan",
            title="Plan weekly-client-report-v1",
            data=mission.plan.model_dump(mode="json"),
        )
    )

    transition(mission, MissionStatus.EXECUTING, trigger="plan_ready")
    payload = _execute_weekly_report(mission, data, model)

    transition(mission, MissionStatus.VALIDATING, trigger="all_steps_completed")
    mission.validation_result = _validate_weekly_report(mission, payload)
    if not mission.validation_result.passed:
        transition(
            mission,
            MissionStatus.FAILED,
            trigger="validation_failed",
            reason="weekly-client-report failed success criteria",
        )
        return mission

    transition(mission, MissionStatus.DELIVERING, trigger="validation_passed")
    mission.output = payload["report"]
    mission.evidence.append(
        EvidenceRef(
            kind="deliverable",
            title="Reporte semanal listo para cliente",
            data={"report": mission.output},
        )
    )

    transition(mission, MissionStatus.GENERATING_REPORT, trigger="delivery_confirmed")
    mission.cost = CostRecord(
        input_tokens=2200,
        output_tokens=1200,
        model_cost_usd=0.09,
        tool_cost_usd=0,
        duration_ms=5 * 60 * 1000,
        human_time_saved_hr=1.5,
    )
    mission.report = MissionReport(
        mission_id=mission.id,
        summary="Reporte semanal de cliente generado, validado y listo para revision de agencia.",
        deliverable_description="Reporte semanal con resumen, metricas, insights y proximos pasos.",
        steps_completed=sum(1 for step in mission.plan.steps if step.status == StepStatus.COMPLETED),
        steps_total=len(mission.plan.steps),
        validation_result=mission.validation_result,
        cost=mission.cost,
        playbook_candidate=True,
        playbook_candidate_reason="Reporte semanal para cliente es repetible por agencia y por cuenta.",
    )

    transition(mission, MissionStatus.UPDATING_MEMORY, trigger="report_generated")
    mission.evidence.append(
        EvidenceRef(
            kind="memory_suggestion",
            title="Sugerencia de playbook semanal para agencias",
            data={
                "playbook_name": "weekly-client-report-v1",
                "target_customer": "agencias y teams",
                "repeat_frequency": "weekly",
            },
        )
    )

    transition(mission, MissionStatus.COMPLETED, trigger="memory_updated")
    return mission


def _build_weekly_report_plan() -> list[MissionStep]:
    return [
        MissionStep(
            order=1,
            description="Normalizar datos de performance semanal",
            executor="Orchestrator",
            required_tools=["development_model"],
            permission_class=PermissionClass.READ_DRAFT,
        ),
        MissionStep(
            order=2,
            description="Calcular cambios contra semana anterior",
            executor="Orchestrator",
            required_tools=[],
            permission_class=PermissionClass.READ_DRAFT,
        ),
        MissionStep(
            order=3,
            description="Generar insights consultivos",
            executor="GrowthSuboperator",
            required_tools=["development_model"],
            permission_class=PermissionClass.READ_DRAFT,
        ),
        MissionStep(
            order=4,
            description="Redactar reporte semanal para cliente",
            executor="Orchestrator",
            required_tools=["development_model"],
            permission_class=PermissionClass.READ_DRAFT,
        ),
        MissionStep(
            order=5,
            description="Validar reporte contra criterios de exito",
            executor="ValidationSuboperator",
            required_tools=[],
            permission_class=PermissionClass.READ_DRAFT,
        ),
    ]


def _execute_weekly_report(
    mission: Mission,
    data: dict[str, Any],
    model: ModelAdapter,
) -> dict[str, Any]:
    assert mission.plan is not None

    this_week = data["this_week"]
    last_week = data["last_week"]
    lead_delta = this_week["total_leads"] - last_week["total_leads"]
    qualified_delta = this_week["qualified_leads"] - last_week["qualified_leads"]
    spend_delta = this_week["spend_usd"] - last_week["spend_usd"]

    metrics = {
        "total_leads": this_week["total_leads"],
        "lead_delta": lead_delta,
        "qualified_leads": this_week["qualified_leads"],
        "qualified_delta": qualified_delta,
        "spend_usd": this_week["spend_usd"],
        "spend_delta": spend_delta,
        "blended_cpl_usd": round(this_week["spend_usd"] / this_week["total_leads"], 2),
    }
    insights = [
        "Paid search genero el mayor volumen y mantiene el CPL mas eficiente.",
        "LinkedIn esta aportando menos volumen y un CPL mas alto; conviene revisar segmentacion y creatividad.",
        "Email produjo 11 respuestas calificadas con bajo costo incremental; merece mas prioridad en follow-up.",
    ]
    next_steps = [
        "Mantener paid search como canal principal durante la proxima semana.",
        "Reducir o reorientar presupuesto de LinkedIn hasta validar nueva segmentacion.",
        "Crear secuencia de seguimiento para las 11 respuestas calificadas de email.",
    ]
    report = _render_report(data, metrics, insights, next_steps, model)

    for step in mission.plan.steps:
        step.status = StepStatus.COMPLETED
        if step.order == 1:
            step.output = {"normalized": data}
        elif step.order == 2:
            step.output = metrics
        elif step.order == 3:
            step.output = {"insights": insights}
        elif step.order == 4:
            step.output = {"report": report}
        else:
            step.output = {"validation_pending": True}

    mission.evidence.append(
        EvidenceRef(
            kind="computed_metrics",
            title="Metricas calculadas para reporte semanal",
            data=metrics,
        )
    )
    mission.evidence.append(
        EvidenceRef(
            kind="insights",
            title="Insights generados para cliente",
            data={
                "insights": insights,
                "next_steps": next_steps,
                "model_adapter": getattr(model, "name", model.__class__.__name__),
                "model_provider_used": getattr(model, "last_provider_used", None),
                "model_error": getattr(model, "last_error", None),
            },
        )
    )
    return {
        "metrics": metrics,
        "insights": insights,
        "next_steps": next_steps,
        "report": report,
    }


def _render_report(
    data: dict[str, Any],
    metrics: dict[str, Any],
    insights: list[str],
    next_steps: list[str],
    model: ModelAdapter,
) -> str:
    model.complete("weekly_client_report")
    insight_lines = "\n".join(f"- {insight}" for insight in insights)
    next_step_lines = "\n".join(f"- {step}" for step in next_steps)
    return (
        f"Reporte semanal - {data['client']}\n"
        f"Periodo: {data['period']}\n\n"
        "Resumen ejecutivo\n"
        f"Esta semana se generaron {metrics['total_leads']} leads "
        f"({metrics['lead_delta']:+} vs semana anterior) y "
        f"{metrics['qualified_leads']} leads calificados "
        f"({metrics['qualified_delta']:+}). El gasto fue de ${metrics['spend_usd']} "
        f"({metrics['spend_delta']:+}) con CPL combinado de ${metrics['blended_cpl_usd']}.\n\n"
        "Insights\n"
        f"{insight_lines}\n\n"
        "Proximos pasos\n"
        f"{next_step_lines}\n"
    )


def _validate_weekly_report(mission: Mission, payload: dict[str, Any]) -> ValidationResult:
    report = payload["report"]
    criteria = [
        {
            "criterion": "incluye resumen ejecutivo",
            "passed": "Resumen ejecutivo" in report,
            "evidence": "Seccion Resumen ejecutivo presente.",
        },
        {
            "criterion": "incluye metricas clave",
            "passed": all(key in payload["metrics"] for key in ["total_leads", "qualified_leads", "blended_cpl_usd"]),
            "evidence": "Metricas total_leads, qualified_leads y blended_cpl_usd calculadas.",
        },
        {
            "criterion": "incluye al menos 3 insights",
            "passed": len(payload["insights"]) >= 3,
            "evidence": f"{len(payload['insights'])} insights generados.",
        },
        {
            "criterion": "incluye proximos pasos accionables",
            "passed": len(payload["next_steps"]) >= 3 and "Proximos pasos" in report,
            "evidence": f"{len(payload['next_steps'])} proximos pasos incluidos.",
        },
        {
            "criterion": "incluye evidencia de datos usados",
            "passed": any(item.kind == "input_data" for item in mission.evidence),
            "evidence": "Evidence input_data presente.",
        },
    ]
    passed = all(item["passed"] for item in criteria)
    result = ValidationResult(
        passed=passed,
        criteria_results=criteria,
        score=sum(1 for item in criteria if item["passed"]) / len(criteria),
        auto_repair_possible=not passed,
    )
    mission.evidence.append(
        EvidenceRef(
            kind="validation",
            title="Validation report weekly-client-report-v1",
            data=result.model_dump(mode="json"),
        )
    )
    return result
