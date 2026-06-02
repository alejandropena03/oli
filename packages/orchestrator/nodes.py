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
    MissionStatus,
    PermissionClass,
    StepStatus,
)
from packages.mission_kernel.policies import max_permission_class
from packages.mission_kernel.state_machine import transition
from packages.model_router import ModelRouter, TaskType, get_model_status
from packages.orchestrator.model_adapter import ModelAdapter
from packages.orchestrator.weekly_client_report import (
    DEFAULT_WEEKLY_REPORT_DATA,
    _build_weekly_report_plan,
    _execute_weekly_report,
    _validate_weekly_report,
)


MissionGraphState = dict[str, Any]


def _mission(state: MissionGraphState) -> Mission:
    return state["mission"]


def _model(state: MissionGraphState) -> ModelAdapter:
    model = state.get("model")
    if model is None:
        router = ModelRouter(provider=get_model_status().provider)
        model, decision = router.get_adapter(TaskType.REPORT_GENERATION)
        state["model_routing_decision"] = decision
    return model


def _performance_data(state: MissionGraphState) -> dict[str, Any]:
    return state.get("performance_data") or DEFAULT_WEEKLY_REPORT_DATA


def interpret_intent_node(state: MissionGraphState) -> MissionGraphState:
    mission = _mission(state)
    transition(mission, MissionStatus.INTERPRETING_INTENT, trigger="langgraph.interpret_intent")
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
    state["intent_clear"] = True
    return state


def retrieve_context_node(state: MissionGraphState) -> MissionGraphState:
    mission = _mission(state)
    data = _performance_data(state)
    transition(mission, MissionStatus.RETRIEVING_CONTEXT, trigger="langgraph.intent_clarified")
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
    return state


def classify_permissions_node(state: MissionGraphState) -> MissionGraphState:
    mission = _mission(state)
    transition(mission, MissionStatus.CLASSIFYING_PERMISSIONS, trigger="langgraph.context_ready")
    steps = _build_weekly_report_plan()
    mission.permission_class = max_permission_class(steps)
    state["candidate_steps"] = steps
    return state


def create_plan_node(state: MissionGraphState) -> MissionGraphState:
    mission = _mission(state)
    transition(mission, MissionStatus.PLANNING, trigger="langgraph.permissions_set")
    steps = state.get("candidate_steps") or _build_weekly_report_plan()
    mission.plan = MissionPlan(
        steps=steps,
        total_permission_class=mission.permission_class or PermissionClass.READ_DRAFT,
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
    return state


def human_approval_node(state: MissionGraphState) -> MissionGraphState:
    mission = _mission(state)
    transition(mission, MissionStatus.AWAITING_APPROVAL, trigger="langgraph.approval_required")
    state["approval_required"] = True
    return state


def execute_step_node(state: MissionGraphState) -> MissionGraphState:
    mission = _mission(state)
    if mission.status == MissionStatus.PLANNING:
        transition(mission, MissionStatus.EXECUTING, trigger="langgraph.plan_ready")
    elif mission.status == MissionStatus.AWAITING_APPROVAL:
        transition(mission, MissionStatus.EXECUTING, trigger="langgraph.approved")

    payload = _execute_weekly_report(mission, _performance_data(state), _model(state))
    decision = state.get("model_routing_decision")
    if decision is not None:
        mission.evidence.append(
            EvidenceRef(
                kind="model_routing",
                title="Decision de Model Router para reporte semanal",
                data=decision.model_dump(mode="json"),
            )
        )
    state["payload"] = payload
    state["all_steps_done"] = True
    state["step_failed"] = False
    return state


def troubleshoot_node(state: MissionGraphState) -> MissionGraphState:
    mission = _mission(state)
    transition(
        mission,
        MissionStatus.BLOCKED,
        trigger="langgraph.repair_unavailable",
        reason=str(state.get("last_error") or "No repair strategy available in V0.1"),
    )
    state["repair_succeeded"] = False
    return state


def validate_output_node(state: MissionGraphState) -> MissionGraphState:
    mission = _mission(state)
    transition(mission, MissionStatus.VALIDATING, trigger="langgraph.all_steps_completed")
    mission.validation_result = _validate_weekly_report(mission, state["payload"])
    if not mission.validation_result.passed:
        transition(
            mission,
            MissionStatus.FAILED,
            trigger="langgraph.validation_failed",
            reason="weekly-client-report failed success criteria",
        )
    state["validation_passed"] = mission.validation_result.passed
    return state


def deliver_node(state: MissionGraphState) -> MissionGraphState:
    mission = _mission(state)
    if mission.status == MissionStatus.FAILED:
        return state
    transition(mission, MissionStatus.DELIVERING, trigger="langgraph.validation_passed")
    mission.output = state["payload"]["report"]
    mission.evidence.append(
        EvidenceRef(
            kind="deliverable",
            title="Reporte semanal listo para cliente",
            data={"report": mission.output},
        )
    )
    return state


def generate_report_node(state: MissionGraphState) -> MissionGraphState:
    mission = _mission(state)
    if mission.status == MissionStatus.FAILED:
        return state
    transition(mission, MissionStatus.GENERATING_REPORT, trigger="langgraph.delivery_confirmed")
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
    return state


def update_memory_node(state: MissionGraphState) -> MissionGraphState:
    mission = _mission(state)
    if mission.status == MissionStatus.FAILED:
        return state
    transition(mission, MissionStatus.UPDATING_MEMORY, trigger="langgraph.report_generated")
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
    transition(mission, MissionStatus.COMPLETED, trigger="langgraph.memory_updated")
    return state


def route_after_plan(state: MissionGraphState) -> str:
    mission = _mission(state)
    if mission.permission_class is not None and mission.permission_class >= PermissionClass.RESOURCE_CONSUMING:
        return "human_approval"
    return "execute_step"


def route_after_execution(state: MissionGraphState) -> str:
    if state.get("all_steps_done"):
        return "validate_output"
    if state.get("step_failed"):
        return "troubleshoot"
    return "execute_step"


def route_after_validation(state: MissionGraphState) -> str:
    return "deliver" if state.get("validation_passed") else "end"
