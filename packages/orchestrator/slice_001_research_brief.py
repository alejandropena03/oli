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
from packages.orchestrator.model_adapter import ModelAdapter, get_default_model_adapter


SLICE_001_INPUT = (
    "Investiga los 3 principales competidores de Oli y dame un brief de 1 pagina "
    "con sus fortalezas, debilidades y el gap que Oli puede explotar."
)


def run_research_brief_v1(
    raw_input: str = SLICE_001_INPUT,
    model: ModelAdapter | None = None,
) -> Mission:
    model = model or get_default_model_adapter()
    mission = create_mission(raw_input=raw_input, source=MissionSource.CHAT)

    transition(mission, MissionStatus.INTERPRETING_INTENT, trigger="auto")
    mission.interpreted_intent = InterpretedIntent(
        goal="competitor_research_brief",
        success_criteria=[
            "fortalezas identificadas por competidor",
            "debilidades identificadas por competidor",
            "gap_exploitable definido",
            "brief menor a 600 palabras",
        ],
        output_format="1-page_brief",
        scope={
            "in_scope": ["top_3_competitors", "strengths", "weaknesses", "exploitable_gap"],
            "out_of_scope": ["pricing_deep_dive", "legal_review", "live_outreach"],
        },
        confidence=0.92,
    )

    transition(mission, MissionStatus.RETRIEVING_CONTEXT, trigger="intent_clarified")
    mission.context = MissionContext(
        user_preferences={
            "style": "executive",
            "max_list_items": 5,
            "language": "es",
        },
        company_context={
            "product": "Oli",
            "positioning": "supervisor de ejecucion digital sobre modelos, agentes, herramientas y memoria",
            "current_stage": "pre-build V0",
        },
    )
    mission.evidence.append(
        EvidenceRef(
            kind="context",
            title="Contexto recuperado para slice-001",
            data=mission.context.model_dump(mode="json"),
        )
    )

    transition(mission, MissionStatus.CLASSIFYING_PERMISSIONS, trigger="context_ready")
    steps = _build_research_plan()
    total_permission = max_permission_class(steps)
    mission.permission_class = total_permission

    transition(mission, MissionStatus.PLANNING, trigger="permissions_set")
    mission.plan = MissionPlan(
        steps=steps,
        total_permission_class=total_permission,
        estimates={
            "duration_ms": 8 * 60 * 1000,
            "cost_usd": 0.12,
            "human_time_saved_hr": 2,
        },
    )
    mission.evidence.append(
        EvidenceRef(
            kind="plan",
            title="Plan research-brief-v1",
            data=mission.plan.model_dump(mode="json"),
        )
    )

    if plan_requires_approval(mission.plan):
        transition(mission, MissionStatus.AWAITING_APPROVAL, trigger="plan_ready")
        return mission

    transition(mission, MissionStatus.EXECUTING, trigger="plan_ready")
    research_payload = _execute_mock_research(mission, model)

    transition(mission, MissionStatus.VALIDATING, trigger="all_steps_completed")
    mission.validation_result = _validate_research_brief(mission, research_payload)

    if not mission.validation_result.passed:
        transition(
            mission,
            MissionStatus.FAILED,
            trigger="validation_failed",
            reason="slice-001 mock output failed success criteria",
        )
        return mission

    transition(mission, MissionStatus.DELIVERING, trigger="validation_passed")
    mission.output = research_payload["brief"]
    mission.evidence.append(
        EvidenceRef(
            kind="deliverable",
            title="Brief competitivo V0",
            data={"brief": mission.output},
        )
    )

    transition(mission, MissionStatus.GENERATING_REPORT, trigger="delivery_confirmed")
    mission.cost = CostRecord(
        input_tokens=1800,
        output_tokens=900,
        model_cost_usd=0.12,
        tool_cost_usd=0,
        duration_ms=8 * 60 * 1000,
        human_time_saved_hr=2,
    )
    mission.report = MissionReport(
        mission_id=mission.id,
        summary="Research brief competitivo generado, validado y entregado en modo mock V0.",
        deliverable_description="Brief de una pagina sobre Lindy, Dust y Claude Projects.",
        steps_completed=sum(1 for step in mission.plan.steps if step.status == StepStatus.COMPLETED),
        steps_total=len(mission.plan.steps),
        validation_result=mission.validation_result,
        cost=mission.cost,
        playbook_candidate=True,
        playbook_candidate_reason="Estructura repetible: intake -> research -> synthesis -> validation -> report.",
    )

    transition(mission, MissionStatus.UPDATING_MEMORY, trigger="report_generated")
    mission.evidence.append(
        EvidenceRef(
            kind="memory_suggestion",
            title="Sugerencia de memoria",
            data={
                "mission_type": "research_brief",
                "playbook_candidate": True,
                "playbook_name": "research-brief-v1",
                "competitors": ["Lindy", "Dust", "Claude Projects"],
            },
        )
    )

    transition(mission, MissionStatus.COMPLETED, trigger="memory_updated")
    return mission


def _build_research_plan() -> list[MissionStep]:
    return [
        MissionStep(
            order=1,
            description="Identificar top 3 competidores de Oli",
            executor="MarketResearchSuboperator",
            required_tools=["mock_web_research"],
            permission_class=PermissionClass.READ_DRAFT,
        ),
        MissionStep(
            order=2,
            description="Research Lindy",
            executor="MarketResearchSuboperator",
            required_tools=["mock_web_research"],
            permission_class=PermissionClass.READ_DRAFT,
        ),
        MissionStep(
            order=3,
            description="Research Dust",
            executor="MarketResearchSuboperator",
            required_tools=["mock_web_research"],
            permission_class=PermissionClass.READ_DRAFT,
        ),
        MissionStep(
            order=4,
            description="Research Claude Projects",
            executor="MarketResearchSuboperator",
            required_tools=["mock_web_research"],
            permission_class=PermissionClass.READ_DRAFT,
        ),
        MissionStep(
            order=5,
            description="Sintetizar en formato brief",
            executor="Orchestrator",
            required_tools=["mock_model"],
            permission_class=PermissionClass.READ_DRAFT,
        ),
        MissionStep(
            order=6,
            description="Validar contra criterios de exito",
            executor="ValidationSuboperator",
            required_tools=[],
            permission_class=PermissionClass.READ_DRAFT,
        ),
        MissionStep(
            order=7,
            description="Entregar brief al founder",
            executor="Orchestrator",
            required_tools=[],
            permission_class=PermissionClass.READ_DRAFT,
        ),
    ]


def _execute_mock_research(mission: Mission, model: ModelAdapter) -> dict[str, Any]:
    assert mission.plan is not None
    competitors = {
        "Lindy": {
            "strengths": ["automatizacion SaaS madura", "UX simple", "integraciones de negocio"],
            "weaknesses": ["menos orientado a ejecucion local", "evidencia tecnica poco visible"],
            "positioning": "AI employees for business workflows",
        },
        "Dust": {
            "strengths": ["fuerte en equipos", "conectores empresariales", "base tecnica seria"],
            "weaknesses": ["mas knowledge-work que ejecucion total", "requiere madurez operativa"],
            "positioning": "AI assistants for teams and company knowledge",
        },
        "Claude Projects": {
            "strengths": ["calidad de razonamiento", "contexto documental", "adopcion amplia"],
            "weaknesses": ["no es supervisor multi-tool persistente", "poca auditoria operacional nativa"],
            "positioning": "workspace contextual para colaborar con Claude",
        },
    }
    brief = model.complete(
        "competitor_research_brief: synthesize Lindy, Dust and Claude Projects for Oli"
    )

    for step in mission.plan.steps:
        step.status = StepStatus.EXECUTING
        if step.order == 1:
            step.output = ["Lindy", "Dust", "Claude Projects"]
        elif step.order in {2, 3, 4}:
            name = step.description.removeprefix("Research ")
            step.output = competitors[name]
        elif step.order == 5:
            step.output = brief
        elif step.order == 6:
            step.output = {"validation_pending": True}
        else:
            step.output = {"delivered": True}
        step.status = StepStatus.COMPLETED

    mission.evidence.append(
        EvidenceRef(
            kind="mock_research",
            title="Resultados mock de competidores",
            data={
                "competitors": competitors,
                "model_adapter": getattr(model, "name", model.__class__.__name__),
                "model_provider_used": getattr(model, "last_provider_used", None),
                "model_error": getattr(model, "last_error", None),
            },
        )
    )
    return {"competitors": competitors, "brief": brief}


def _validate_research_brief(mission: Mission, payload: dict[str, Any]) -> ValidationResult:
    competitors = payload["competitors"]
    brief = payload["brief"]
    words = brief.split()
    criteria = [
        {
            "criterion": "fortalezas identificadas por competidor",
            "passed": all(len(item["strengths"]) >= 3 for item in competitors.values()),
            "evidence": "3 fortalezas por competidor",
        },
        {
            "criterion": "debilidades identificadas por competidor",
            "passed": all(len(item["weaknesses"]) >= 2 for item in competitors.values()),
            "evidence": "2 debilidades por competidor",
        },
        {
            "criterion": "gap_exploitable definido",
            "passed": "gap explotable" in brief and "supervisor de ejecucion" in brief,
            "evidence": "El brief formula el gap de Oli como supervisor de ejecucion.",
        },
        {
            "criterion": "brief menor a 600 palabras",
            "passed": len(words) < 600,
            "evidence": f"{len(words)} palabras",
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
            title="Validation report slice-001",
            data=result.model_dump(mode="json"),
        )
    )
    return result
