"""Intent-driven orchestrator — el cerebro real de Oli.

Reemplaza el orchestrator hardcodeado de slice_001. El LLM interpreta el
raw_input del usuario, genera el plan específico para esa intención, ejecuta
los pasos que puede con los recursos disponibles, y declara explícitamente
los pasos que requieren conectores externos aún no implementados.

Sin intención hardcodeada. Sin datos inventados. Sin teatro.
"""
from __future__ import annotations

import json
import textwrap
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


# ---------------------------------------------------------------------------
# Conectores disponibles en V0.4
# ---------------------------------------------------------------------------

AVAILABLE_CONNECTORS: set[str] = set()  # ninguno aún en V0.4

KNOWN_CONNECTORS: dict[str, str] = {
    "whatsapp": "WhatsApp Business API — leer/enviar mensajes",
    "slack": "Slack API — leer canales, threads, DMs",
    "gmail": "Gmail API — leer inbox, threads, etiquetas",
    "instagram": "Instagram Graph API — leer DMs y menciones",
    "telegram": "Telegram Bot API — leer mensajes",
    "notion": "Notion API — leer/escribir páginas y bases de datos",
    "calendar": "Google Calendar API — leer eventos y recordatorios",
    "linear": "Linear API — leer/crear issues",
}


# ---------------------------------------------------------------------------
# Prompts del sistema
# ---------------------------------------------------------------------------

_INTENT_SYSTEM = textwrap.dedent("""
Eres Oli, un operador de ejecución digital. Tu trabajo es interpretar con precisión
lo que el usuario quiere lograr y estructurar una misión ejecutable.

Cuando recibes un raw_input del usuario, debes responder ÚNICAMENTE con un JSON
válido con esta estructura exacta:

{
  "goal": "slug_corto_del_objetivo",
  "summary": "Una oración que describe qué quiere el usuario",
  "success_criteria": [
    "criterio 1 — observable y verificable",
    "criterio 2",
    "criterio 3"
  ],
  "output_format": "tipo_de_entregable",
  "required_connectors": ["nombre_conector_1", "nombre_conector_2"],
  "scope_in": ["qué está dentro del alcance"],
  "scope_out": ["qué está fuera del alcance"],
  "steps": [
    {
      "order": 1,
      "description": "Descripción del paso",
      "executor": "NombreSuboperador",
      "required_connector": null,
      "permission_class": 0
    }
  ],
  "confidence": 0.85
}

Reglas:
- required_connectors: lista los conectores externos que necesita la misión (whatsapp, slack, gmail, instagram, etc.)
- Para cada step, required_connector es null si Oli puede ejecutarlo con su capacidad actual (síntesis, análisis, estructuración, búsqueda en memoria), o el nombre del conector si necesita acceso externo
- permission_class: 0=READ_DRAFT, 1=INTERNAL_REVERSIBLE, 2=RESOURCE_CONSUMING, 3=EXTERNAL_BRAND_IMPACT, 4=DESTRUCTIVE_SENSITIVE
- Los pasos de análisis, síntesis y estructuración NO requieren conector — Oli los puede ejecutar ahora
- Los pasos de lectura de mensajes externos (WhatsApp, Slack, Gmail, Instagram) SÍ requieren conector
- Los pasos de envío de mensajes o acciones externas requieren permission_class >= 3
- Responde SOLO el JSON. Sin explicaciones. Sin markdown.
""").strip()

_EXECUTE_SYSTEM = textwrap.dedent("""
Eres Oli ejecutando un paso de una misión. Tienes acceso a tu capacidad de análisis
y síntesis, pero NO tienes acceso a sistemas externos (WhatsApp, Slack, Gmail, Instagram)
en esta versión.

El usuario pidió: {raw_input}

El objetivo de la misión es: {goal}

Tu tarea en este paso es: {step_description}

Ejecuta este paso con la información que tienes. Si el paso requiere datos de un
conector externo que no tienes, dilo explícitamente y describe qué harías con esos
datos cuando el conector esté disponible.

Responde directamente con el resultado del paso. Sin preámbulos.
""").strip()

_SYNTHESIS_SYSTEM = textwrap.dedent("""
Eres Oli sintetizando el output final de una misión.

El usuario pidió: {raw_input}
El objetivo: {goal}
Criterios de éxito: {criteria}

Tienes los resultados de los pasos ejecutados:
{step_results}

Pasos que requieren conectores externos aún no disponibles:
{blocked_steps}

Genera el entregable final de la misión. Debe:
1. Responder directamente lo que el usuario pidió
2. Incluir lo que Oli puede hacer AHORA con su capacidad actual
3. Para cada conector externo requerido, declarar explícitamente: "Para [funcionalidad], se necesita conectar [Conector]. Una vez conectado, Oli hará: [descripción específica]."
4. Ser honesto sobre qué está implementado y qué no

Responde directamente con el entregable. Sin preámbulos.
""").strip()

_VALIDATION_SYSTEM = textwrap.dedent("""
Eres un validador de outputs de misiones de Oli.

El usuario pidió: {raw_input}
Los criterios de éxito definidos: {criteria}
El output generado: {output}

Para cada criterio, evalúa si el output lo cumple. Responde ÚNICAMENTE con JSON:

{
  "criteria_results": [
    {
      "criterion": "texto del criterio",
      "passed": true,
      "evidence": "qué parte del output lo cumple o por qué falla"
    }
  ],
  "overall_passed": true,
  "score": 0.85,
  "notes": "observación general opcional"
}

Responde SOLO el JSON. Sin markdown.
""").strip()


# ---------------------------------------------------------------------------
# Orchestrator principal
# ---------------------------------------------------------------------------

def run_intent_driven_mission(
    raw_input: str,
    model: ModelAdapter | None = None,
) -> Mission:
    """Orchestrator LLM-first — interpreta la intención real del usuario."""
    model = model or get_default_model_adapter()
    mission = create_mission(raw_input=raw_input, source=MissionSource.CHAT)

    # ── 1. Interpretar intención ──────────────────────────────────────────
    transition(mission, MissionStatus.INTERPRETING_INTENT, trigger="auto")
    intent_data = _interpret_intent(raw_input, model)

    mission.interpreted_intent = InterpretedIntent(
        goal=intent_data["goal"],
        success_criteria=intent_data["success_criteria"],
        output_format=intent_data.get("output_format", "structured_report"),
        scope={
            "in_scope": intent_data.get("scope_in", []),
            "out_of_scope": intent_data.get("scope_out", []),
        },
        confidence=intent_data.get("confidence", 0.8),
    )
    mission.evidence.append(EvidenceRef(
        kind="intent_interpretation",
        title="Intención interpretada por LLM",
        data={
            "raw_input": raw_input,
            "interpreted": intent_data,
            "model_used": getattr(model, "name", model.__class__.__name__),
        },
    ))

    # ── 2. Recuperar contexto ─────────────────────────────────────────────
    transition(mission, MissionStatus.RETRIEVING_CONTEXT, trigger="intent_clarified")
    required_connectors = intent_data.get("required_connectors", [])
    available = [c for c in required_connectors if c in AVAILABLE_CONNECTORS]
    missing = [c for c in required_connectors if c not in AVAILABLE_CONNECTORS]

    mission.context = MissionContext(
        user_preferences={"language": "es", "style": "directo y ejecutable"},
        company_context={
            "product": "Oli",
            "version": "V0.4",
            "available_connectors": list(AVAILABLE_CONNECTORS) or ["ninguno en V0.4"],
            "missing_connectors": missing,
        },
    )
    mission.evidence.append(EvidenceRef(
        kind="context",
        title="Contexto de conectividad",
        data={
            "required_connectors": required_connectors,
            "available_in_v04": available,
            "missing_need_implementation": [
                {"connector": c, "description": KNOWN_CONNECTORS.get(c, c)}
                for c in missing
            ],
        },
    ))

    # ── 3. Construir plan desde intent_data ───────────────────────────────
    transition(mission, MissionStatus.CLASSIFYING_PERMISSIONS, trigger="context_ready")
    raw_steps = intent_data.get("steps", [])
    steps = _build_steps_from_llm(raw_steps, missing)
    total_permission = max_permission_class(steps)
    mission.permission_class = total_permission

    transition(mission, MissionStatus.PLANNING, trigger="permissions_set")
    mission.plan = MissionPlan(
        steps=steps,
        total_permission_class=total_permission,
        estimates={
            "duration_ms": len(steps) * 30_000,
            "cost_usd": round(len(steps) * 0.005, 3),
            "human_time_saved_hr": _estimate_time_saved(required_connectors),
        },
    )
    mission.evidence.append(EvidenceRef(
        kind="plan",
        title=f"Plan generado por LLM para: {intent_data['goal']}",
        data=mission.plan.model_dump(mode="json"),
    ))

    if plan_requires_approval(mission.plan):
        transition(mission, MissionStatus.AWAITING_APPROVAL, trigger="plan_ready")
        return mission

    # ── 4. Ejecutar pasos ─────────────────────────────────────────────────
    transition(mission, MissionStatus.EXECUTING, trigger="plan_ready")
    step_results: list[dict[str, Any]] = []
    blocked_steps: list[dict[str, Any]] = []

    for step in mission.plan.steps:
        step.status = StepStatus.EXECUTING
        connector_needed = getattr(step, "_connector_required", None)

        if connector_needed and connector_needed not in AVAILABLE_CONNECTORS:
            # Conector no disponible — declarar explícito, no simular
            step.status = StepStatus.BLOCKED
            result = {
                "step": step.order,
                "description": step.description,
                "status": "CONNECTOR_REQUIRED",
                "connector": connector_needed,
                "connector_description": KNOWN_CONNECTORS.get(connector_needed, connector_needed),
                "what_oli_will_do_when_connected": (
                    f"Cuando {connector_needed} esté conectado, Oli ejecutará: {step.description}"
                ),
            }
            blocked_steps.append(result)
            step.output = result
        else:
            # Oli puede ejecutar este paso con su capacidad actual
            prompt = _EXECUTE_SYSTEM.format(
                raw_input=raw_input,
                goal=intent_data["goal"],
                step_description=step.description,
            )
            output = model.complete(prompt)
            step.status = StepStatus.COMPLETED
            result = {
                "step": step.order,
                "description": step.description,
                "status": "COMPLETED",
                "output": output,
            }
            step_results.append(result)
            step.output = output

    # ── 5. Sintetizar output final ────────────────────────────────────────
    synthesis_prompt = _SYNTHESIS_SYSTEM.format(
        raw_input=raw_input,
        goal=intent_data["goal"],
        criteria="\n".join(f"- {c}" for c in intent_data["success_criteria"]),
        step_results=json.dumps(step_results, ensure_ascii=False, indent=2),
        blocked_steps=json.dumps(blocked_steps, ensure_ascii=False, indent=2),
    )
    final_output = model.complete(synthesis_prompt)

    # ── 6. Validar ────────────────────────────────────────────────────────
    transition(mission, MissionStatus.VALIDATING, trigger="all_steps_completed")
    validation_result = _validate_with_llm(
        raw_input=raw_input,
        criteria=intent_data["success_criteria"],
        output=final_output,
        model=model,
    )
    mission.validation_result = validation_result
    mission.evidence.append(EvidenceRef(
        kind="validation",
        title="Validación LLM del output final",
        data=validation_result.model_dump(mode="json"),
    ))

    if not mission.validation_result.passed:
        transition(
            mission,
            MissionStatus.FAILED,
            trigger="validation_failed",
            reason=f"score={mission.validation_result.score:.2f} — criterios no cumplidos",
        )
        mission.output = final_output  # preservar para debugging
        return mission

    # ── 7. Entregar ───────────────────────────────────────────────────────
    transition(mission, MissionStatus.DELIVERING, trigger="validation_passed")
    mission.output = final_output
    mission.evidence.append(EvidenceRef(
        kind="deliverable",
        title=f"Entregable: {intent_data['goal']}",
        data={
            "output": final_output,
            "steps_completed": len(step_results),
            "steps_blocked_connector_required": len(blocked_steps),
            "blocked_connectors": [b["connector"] for b in blocked_steps],
        },
    ))

    # ── 8. Reporte ────────────────────────────────────────────────────────
    transition(mission, MissionStatus.GENERATING_REPORT, trigger="delivery_confirmed")
    completed_count = sum(1 for s in mission.plan.steps if s.status == StepStatus.COMPLETED)
    blocked_count = sum(1 for s in mission.plan.steps if s.status == StepStatus.BLOCKED)

    mission.cost = CostRecord(
        input_tokens=_estimate_tokens(raw_input) + len(steps) * 200,
        output_tokens=_estimate_tokens(final_output),
        model_cost_usd=round(len(steps) * 0.005, 3),
        tool_cost_usd=0,
        duration_ms=len(steps) * 30_000,
        human_time_saved_hr=_estimate_time_saved(required_connectors),
    )

    connector_note = ""
    if blocked_steps:
        names = ", ".join(b["connector"] for b in blocked_steps)
        connector_note = f" {len(blocked_steps)} paso(s) requieren conectores externos aún no implementados: {names}."

    mission.report = MissionReport(
        mission_id=mission.id,
        summary=(
            f"Misión '{intent_data['goal']}' ejecutada. "
            f"{completed_count} paso(s) completados por Oli.{connector_note}"
        ),
        deliverable_description=intent_data.get("summary", intent_data["goal"]),
        steps_completed=completed_count,
        steps_total=len(mission.plan.steps),
        validation_result=mission.validation_result,
        cost=mission.cost,
        playbook_candidate=blocked_count == 0,
        playbook_candidate_reason=(
            "Misión completamente ejecutable por Oli — candidata a playbook."
            if blocked_count == 0
            else f"Requiere {len(missing)} conector(es) para ser completamente autónoma."
        ),
    )

    # ── 9. Memoria ────────────────────────────────────────────────────────
    transition(mission, MissionStatus.UPDATING_MEMORY, trigger="report_generated")
    mission.evidence.append(EvidenceRef(
        kind="memory_suggestion",
        title="Sugerencia de memoria",
        data={
            "mission_type": intent_data["goal"],
            "required_connectors": required_connectors,
            "missing_connectors": missing,
            "playbook_candidate": mission.report.playbook_candidate,
        },
    ))

    transition(mission, MissionStatus.COMPLETED, trigger="memory_updated")
    return mission


# ---------------------------------------------------------------------------
# Helpers de interpretación
# ---------------------------------------------------------------------------

def _interpret_intent(raw_input: str, model: ModelAdapter) -> dict[str, Any]:
    """Pide al LLM que interprete la intención y genere el plan inicial."""
    prompt = f"{_INTENT_SYSTEM}\n\nraw_input del usuario:\n{raw_input}"
    raw = model.complete(prompt)

    try:
        data = _extract_json(raw)
        # Validar campos mínimos
        if "goal" not in data or "success_criteria" not in data:
            raise ValueError("Respuesta del LLM sin campos requeridos")
        return data
    except Exception as exc:
        # Si el LLM no devuelve JSON válido, construir intent mínimo honesto
        return {
            "goal": "intent_parse_failed",
            "summary": raw_input[:200],
            "success_criteria": ["Oli interpreta correctamente la petición del usuario"],
            "output_format": "text",
            "required_connectors": [],
            "scope_in": [raw_input[:100]],
            "scope_out": [],
            "steps": [
                {
                    "order": 1,
                    "description": f"Analizar y responder: {raw_input[:200]}",
                    "executor": "Orchestrator",
                    "required_connector": None,
                    "permission_class": 0,
                }
            ],
            "confidence": 0.3,
            "_parse_error": str(exc),
            "_raw_llm_response": raw[:500],
        }


def _build_steps_from_llm(
    raw_steps: list[dict[str, Any]],
    missing_connectors: list[str],
) -> list[MissionStep]:
    """Convierte los pasos del LLM en MissionSteps con metadata de conectores."""
    if not raw_steps:
        return [MissionStep(
            order=1,
            description="Analizar la petición y generar respuesta",
            executor="Orchestrator",
            required_tools=[],
            permission_class=PermissionClass.READ_DRAFT,
        )]

    steps = []
    for raw in raw_steps:
        connector = raw.get("required_connector")
        pclass_int = raw.get("permission_class", 0)
        # Si el paso tiene conector externo faltante, elevar permission a mínimo class 1
        if connector and connector in missing_connectors:
            pclass_int = max(pclass_int, 1)

        step = MissionStep(
            order=raw.get("order", len(steps) + 1),
            description=raw.get("description", "paso sin descripción"),
            executor=raw.get("executor", "Orchestrator"),
            required_tools=[connector] if connector else [],
            permission_class=PermissionClass(min(pclass_int, 4)),
        )
        # Adjuntar metadata de conector para que el executor la use
        step.__dict__["_connector_required"] = connector
        steps.append(step)

    return steps


def _validate_with_llm(
    raw_input: str,
    criteria: list[str],
    output: str,
    model: ModelAdapter,
) -> ValidationResult:
    """Validación derivada de los criterios de la intención, no hardcodeada."""
    prompt = _VALIDATION_SYSTEM.format(
        raw_input=raw_input,
        criteria="\n".join(f"- {c}" for c in criteria),
        output=output[:2000],  # limitar para no exceder contexto
    )
    raw = model.complete(prompt)

    try:
        data = _extract_json(raw)
        criteria_results = data.get("criteria_results", [])
        passed = data.get("overall_passed", False)
        score = float(data.get("score", 0.0))
        return ValidationResult(
            passed=passed,
            criteria_results=criteria_results,
            score=score,
            auto_repair_possible=not passed,
        )
    except Exception:
        # Si el LLM no puede validar, no inventar que pasó — marcar con score bajo
        return ValidationResult(
            passed=False,
            criteria_results=[
                {
                    "criterion": c,
                    "passed": False,
                    "evidence": "Validación LLM no pudo parsear respuesta",
                }
                for c in criteria
            ],
            score=0.0,
            auto_repair_possible=True,
        )


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def _extract_json(text: str) -> dict[str, Any]:
    """Extrae el primer bloque JSON de un texto que puede tener markdown."""
    text = text.strip()
    # Remover bloques markdown ```json ... ```
    if "```" in text:
        start = text.find("```")
        end = text.rfind("```")
        if start != end:
            block = text[start:end]
            block = block.lstrip("`").lstrip("json").strip()
            text = block

    # Encontrar el primer { ... }
    brace_start = text.find("{")
    brace_end = text.rfind("}")
    if brace_start != -1 and brace_end != -1:
        text = text[brace_start:brace_end + 1]

    return json.loads(text)


def _estimate_tokens(text: str) -> int:
    return max(1, len(text.split()) * 4 // 3)


def _estimate_time_saved(required_connectors: list[str]) -> float:
    """Tiempo humano ahorrado estimado — más si hay conectores que Oli puede automatizar."""
    base = 0.5
    return round(base + len(required_connectors) * 0.5, 1)
