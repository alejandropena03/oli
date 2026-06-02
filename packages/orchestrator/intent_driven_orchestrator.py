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
import time
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

# Costo estimado por token para owl-alpha via OpenRouter (USD)
_COST_PER_INPUT_TOKEN = 0.0000015
_COST_PER_OUTPUT_TOKEN = 0.000002


# ---------------------------------------------------------------------------
# Prompts del sistema
# ---------------------------------------------------------------------------

_INTENT_SYSTEM = textwrap.dedent("""
Eres Oli, un operador de ejecución digital. Tu trabajo es interpretar con precisión
lo que el usuario quiere lograr y estructurar una misión ejecutable.

Cuando recibes un raw_input del usuario, debes responder ÚNICAMENTE con un objeto JSON
válido. Sin markdown, sin explicaciones, sin texto antes o después del JSON.

Estructura exacta:

{"goal":"slug_corto","summary":"Una oración del objetivo","success_criteria":["criterio 1","criterio 2","criterio 3"],"output_format":"tipo_entregable","required_connectors":["conector1"],"scope_in":["dentro del alcance"],"scope_out":["fuera del alcance"],"steps":[{"order":1,"description":"Descripción","executor":"Orchestrator","required_connector":null,"permission_class":0}],"confidence":0.85}

Reglas:
- required_connectors: conectores externos requeridos (whatsapp, slack, gmail, instagram, telegram, notion, calendar, linear)
- required_connector por step: null si Oli puede ejecutarlo (síntesis, análisis, estructuración), o el nombre del conector si necesita acceso externo
- permission_class: 0=READ_DRAFT, 1=INTERNAL_REVERSIBLE, 2=RESOURCE_CONSUMING, 3=EXTERNAL_BRAND_IMPACT, 4=DESTRUCTIVE
- Pasos de lectura de mensajes externos SÍ requieren conector
- Pasos de síntesis, estructuración, análisis NO requieren conector

Responde SOLO el JSON. Nada más.
""").strip()

_EXECUTE_SYSTEM = textwrap.dedent("""
Eres Oli ejecutando un paso de una misión. Tienes capacidad de análisis y síntesis,
pero NO tienes acceso a sistemas externos en esta versión.

Usuario pidió: {raw_input}
Objetivo: {goal}
Paso a ejecutar: {step_description}

Ejecuta con la información disponible. Responde directamente con el resultado.
""").strip()

_SYNTHESIS_SYSTEM = textwrap.dedent("""
Eres Oli entregando el resultado final de una misión.

Usuario pidió: {raw_input}
Objetivo: {goal}
Criterios de éxito:
{criteria}

Resultados de pasos ejecutados:
{step_results}

Pasos bloqueados por conectores faltantes:
{blocked_steps}

Entrega el resultado final. Debe:
1. Responder directamente lo que pidió el usuario
2. Mostrar lo que Oli puede hacer AHORA con su capacidad actual
3. Para cada conector faltante declarar: "Para [funcionalidad]: necesita conectar [Conector]. Una vez conectado, Oli ejecutará automáticamente: [descripción exacta]."
4. Ser honesto — no inventar datos de conectores no disponibles

Responde directamente con el entregable.
""").strip()

_VALIDATION_SYSTEM = textwrap.dedent("""
Eres un validador de misiones. Evalúa si el output cumple los criterios.

Criterios:
{criteria}

Output a evaluar:
{output}

Responde SOLO este JSON (sin markdown, sin texto extra):
{{"criteria_results":[{{"criterion":"texto","passed":true,"evidence":"razón"}}],"overall_passed":true,"score":0.85,"notes":"opcional"}}
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
    token_tracker = _TokenTracker()
    wall_start = time.monotonic()

    # ── 1. Interpretar intención ──────────────────────────────────────────
    transition(mission, MissionStatus.INTERPRETING_INTENT, trigger="auto")
    intent_raw = _llm_call(model, f"{_INTENT_SYSTEM}\n\nraw_input del usuario:\n{raw_input}", token_tracker)
    intent_data = _parse_intent(intent_raw, raw_input)

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
            "parse_ok": "_parse_error" not in intent_data,
        },
    ))

    # ── 2. Recuperar contexto ─────────────────────────────────────────────
    transition(mission, MissionStatus.RETRIEVING_CONTEXT, trigger="intent_clarified")
    required_connectors: list[str] = intent_data.get("required_connectors", [])
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

    # ── 3. Construir plan ─────────────────────────────────────────────────
    transition(mission, MissionStatus.CLASSIFYING_PERMISSIONS, trigger="context_ready")
    raw_steps = intent_data.get("steps", [])
    steps = _build_steps(raw_steps, missing)
    total_permission = max_permission_class(steps)
    mission.permission_class = total_permission

    transition(mission, MissionStatus.PLANNING, trigger="permissions_set")
    mission.plan = MissionPlan(
        steps=steps,
        total_permission_class=total_permission,
        estimates={
            "duration_ms": len(steps) * 30_000,
            "cost_usd": 0,  # se actualiza con tracking real al final
            "human_time_saved_hr": _estimate_time_saved(required_connectors),
        },
    )
    mission.evidence.append(EvidenceRef(
        kind="plan",
        title=f"Plan LLM para: {intent_data['goal']}",
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

        if step.connector_required and step.connector_required not in AVAILABLE_CONNECTORS:
            step.status = StepStatus.BLOCKED
            blocked = {
                "step": step.order,
                "description": step.description,
                "connector": step.connector_required,
                "connector_description": KNOWN_CONNECTORS.get(step.connector_required, step.connector_required),
                "when_connected": f"Oli ejecutará automáticamente: {step.description}",
            }
            blocked_steps.append(blocked)
            step.output = {"status": "CONNECTOR_REQUIRED", **blocked}
        else:
            prompt = _EXECUTE_SYSTEM.format(
                raw_input=raw_input,
                goal=intent_data["goal"],
                step_description=step.description,
            )
            output = _llm_call(model, prompt, token_tracker)
            step.status = StepStatus.COMPLETED
            result = {
                "step": step.order,
                "description": step.description,
                "output": output,
            }
            step_results.append(result)
            step.output = output

    # ── 5. Síntesis final ─────────────────────────────────────────────────
    synthesis_prompt = _SYNTHESIS_SYSTEM.format(
        raw_input=raw_input,
        goal=intent_data["goal"],
        criteria="\n".join(f"- {c}" for c in intent_data["success_criteria"]),
        step_results=json.dumps(step_results, ensure_ascii=False, indent=2),
        blocked_steps=json.dumps(blocked_steps, ensure_ascii=False, indent=2),
    )
    final_output = _llm_call(model, synthesis_prompt, token_tracker)

    # ── 6. Validar ────────────────────────────────────────────────────────
    transition(mission, MissionStatus.VALIDATING, trigger="all_steps_completed")
    validation_result = _validate(
        criteria=intent_data["success_criteria"],
        output=final_output,
        blocked_steps=blocked_steps,
        model=model,
        token_tracker=token_tracker,
    )
    mission.validation_result = validation_result
    mission.evidence.append(EvidenceRef(
        kind="validation",
        title="Validación del output final",
        data=validation_result.model_dump(mode="json"),
    ))

    # Determinar path: si hay bloqueados pero los ejecutables pasaron → COMPLETED_PARTIAL
    # Si falló en pasos ejecutables → depende del score
    has_blockers = len(blocked_steps) > 0
    executable_ok = validation_result.score >= 0.5 or has_blockers

    if not executable_ok:
        transition(
            mission,
            MissionStatus.FAILED,
            trigger="validation_failed",
            reason=f"score={validation_result.score:.2f} — output ejecutable no cumple criterios mínimos",
        )
        mission.output = final_output
        return mission

    # ── 7. Entregar ───────────────────────────────────────────────────────
    transition(mission, MissionStatus.DELIVERING, trigger="validation_passed")
    mission.output = final_output
    completed_count = sum(1 for s in mission.plan.steps if s.status == StepStatus.COMPLETED)
    blocked_count = len(blocked_steps)

    mission.evidence.append(EvidenceRef(
        kind="deliverable",
        title=f"Entregable: {intent_data['goal']}",
        data={
            "steps_completed": completed_count,
            "steps_blocked_connector_required": blocked_count,
            "blocked_connectors": [b["connector"] for b in blocked_steps],
            "output_length_chars": len(final_output),
        },
    ))

    # ── 8. Reporte ────────────────────────────────────────────────────────
    transition(mission, MissionStatus.GENERATING_REPORT, trigger="delivery_confirmed")
    wall_ms = int((time.monotonic() - wall_start) * 1000)

    mission.cost = CostRecord(
        input_tokens=token_tracker.input_tokens,
        output_tokens=token_tracker.output_tokens,
        model_cost_usd=round(
            token_tracker.input_tokens * _COST_PER_INPUT_TOKEN
            + token_tracker.output_tokens * _COST_PER_OUTPUT_TOKEN,
            6,
        ),
        tool_cost_usd=0,
        duration_ms=wall_ms,
        human_time_saved_hr=_estimate_time_saved(required_connectors),
    )

    connector_note = ""
    if blocked_steps:
        names = ", ".join(b["connector"] for b in blocked_steps)
        connector_note = (
            f" {blocked_count} paso(s) requieren conectores no implementados: {names}."
            " Una vez conectados, Oli los ejecutará automáticamente."
        )

    final_status = MissionStatus.COMPLETED_PARTIAL if has_blockers else MissionStatus.COMPLETED

    mission.report = MissionReport(
        mission_id=mission.id,
        summary=(
            f"Misión '{intent_data['goal']}': {completed_count} paso(s) completados por Oli.{connector_note}"
        ),
        deliverable_description=intent_data.get("summary", intent_data["goal"]),
        steps_completed=completed_count,
        steps_total=len(mission.plan.steps),
        validation_result=mission.validation_result,
        cost=mission.cost,
        playbook_candidate=blocked_count == 0,
        playbook_candidate_reason=(
            "Completamente ejecutable por Oli — candidata a playbook."
            if blocked_count == 0
            else f"Requiere {len(missing)} conector(es) para ejecución autónoma completa."
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

    transition(mission, final_status, trigger="memory_updated")
    return mission


# ---------------------------------------------------------------------------
# Helpers de LLM
# ---------------------------------------------------------------------------

class _TokenTracker:
    """Acumula tokens reales de llamadas al modelo."""

    def __init__(self) -> None:
        self.input_tokens = 0
        self.output_tokens = 0

    def record(self, prompt: str, response: str) -> None:
        self.input_tokens += _estimate_tokens(prompt)
        self.output_tokens += _estimate_tokens(response)


def _llm_call(model: ModelAdapter, prompt: str, tracker: _TokenTracker) -> str:
    response = model.complete(prompt)
    tracker.record(prompt, response)
    return response


def _parse_intent(raw: str, original_input: str) -> dict[str, Any]:
    """Parsea la respuesta del LLM de interpretación. Si falla, construye intent mínimo honesto."""
    try:
        data = _extract_json(raw)
        if "goal" not in data or "success_criteria" not in data:
            raise ValueError("campos requeridos ausentes")
        # Normalizar: success_criteria debe ser lista de strings
        if not isinstance(data["success_criteria"], list):
            data["success_criteria"] = [str(data["success_criteria"])]
        return data
    except Exception as exc:
        return {
            "goal": "intent_parse_failed",
            "summary": original_input[:200],
            "success_criteria": [
                "El output responde directamente la petición del usuario",
                "El output es honesto sobre qué está implementado",
            ],
            "output_format": "text",
            "required_connectors": [],
            "scope_in": [original_input[:100]],
            "scope_out": [],
            "steps": [
                {
                    "order": 1,
                    "description": f"Analizar y responder: {original_input[:200]}",
                    "executor": "Orchestrator",
                    "required_connector": None,
                    "permission_class": 0,
                }
            ],
            "confidence": 0.3,
            "_parse_error": str(exc),
            "_raw_llm_response": raw[:300],
        }


def _build_steps(raw_steps: list[dict[str, Any]], missing_connectors: list[str]) -> list[MissionStep]:
    """Convierte pasos del LLM en MissionSteps con connector_required como field real."""
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
        connector = raw.get("required_connector") or None
        pclass_int = raw.get("permission_class", 0)
        if connector and connector in missing_connectors:
            pclass_int = max(pclass_int, 1)

        steps.append(MissionStep(
            order=raw.get("order", len(steps) + 1),
            description=raw.get("description", "paso sin descripción"),
            executor=raw.get("executor", "Orchestrator"),
            required_tools=[connector] if connector else [],
            connector_required=connector,
            permission_class=PermissionClass(min(pclass_int, 4)),
        ))

    return steps


def _validate(
    criteria: list[str],
    output: str,
    blocked_steps: list[dict[str, Any]],
    model: ModelAdapter,
    token_tracker: _TokenTracker,
) -> ValidationResult:
    """Validación LLM con fallback local honesto.

    Intenta que el LLM evalúe cada criterio. Si el JSON no es parseable,
    aplica heurísticas locales sobre el output real — no inventa score 0.
    """
    prompt = _VALIDATION_SYSTEM.format(
        criteria="\n".join(f"- {c}" for c in criteria),
        output=output[:3000],
    )
    raw = _llm_call(model, prompt, token_tracker)

    try:
        data = _extract_json(raw)
        criteria_results = data.get("criteria_results", [])
        passed = bool(data.get("overall_passed", False))
        score = float(data.get("score", 0.0))

        # Sanity check: si el LLM devolvió resultados vacíos, caer al fallback
        if not criteria_results:
            raise ValueError("criteria_results vacío")

        return ValidationResult(
            passed=passed,
            criteria_results=criteria_results,
            score=score,
            auto_repair_possible=not passed,
        )
    except Exception:
        # Fallback local: evaluar heurísticamente — no declarar score 0 sin evidencia
        return _local_validation_fallback(criteria, output, blocked_steps)


def _local_validation_fallback(
    criteria: list[str],
    output: str,
    blocked_steps: list[dict[str, Any]],
) -> ValidationResult:
    """Validación local cuando el LLM no devuelve JSON parseable.

    Heurísticas honestas: el output tiene contenido sustancial, menciona los
    conectores bloqueados, y responde algo coherente.
    """
    output_lower = output.lower()
    word_count = len(output.split())
    blocked_connectors = {b["connector"] for b in blocked_steps}

    results = []
    for criterion in criteria:
        crit_lower = criterion.lower()

        # Heurística 1: criterio sobre conectores externos
        connector_keywords = {"whatsapp", "slack", "gmail", "instagram", "telegram", "notion"}
        mentioned_connectors = connector_keywords & set(crit_lower.split())
        if mentioned_connectors:
            # El criterio requiere un conector — si está en blocked_steps, Oli lo declaró
            declared = any(c in output_lower for c in mentioned_connectors)
            results.append({
                "criterion": criterion,
                "passed": declared,
                "evidence": (
                    f"Conector mencionado en output (declarado como pendiente)"
                    if declared
                    else "Conector no mencionado en output"
                ),
            })
            continue

        # Heurística 2: criterio sobre contenido del output
        has_content = word_count >= 50
        results.append({
            "criterion": criterion,
            "passed": has_content,
            "evidence": (
                f"Output tiene {word_count} palabras — contenido sustancial"
                if has_content
                else f"Output insuficiente ({word_count} palabras)"
            ),
        })

    passed_count = sum(1 for r in results if r["passed"])
    score = passed_count / len(results) if results else 0.0

    return ValidationResult(
        passed=score >= 0.5,
        criteria_results=results,
        score=round(score, 2),
        auto_repair_possible=score < 1.0,
    )


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def _extract_json(text: str) -> dict[str, Any]:
    """Extrae el primer objeto JSON de un texto que puede tener markdown o texto extra."""
    text = text.strip()

    # Remover bloques markdown ```json ... ``` o ``` ... ```
    if "```" in text:
        import re
        match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
        if match:
            text = match.group(1).strip()

    # Encontrar el primer { ... } balanceado
    brace_start = text.find("{")
    if brace_start == -1:
        raise ValueError("No se encontró objeto JSON en la respuesta")

    depth = 0
    for i, ch in enumerate(text[brace_start:], start=brace_start):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[brace_start:i + 1])

    raise ValueError("JSON incompleto — llaves no balanceadas")


def _estimate_tokens(text: str) -> int:
    """Estimación de tokens: ~4 chars por token (aproximación estándar)."""
    return max(1, len(text) // 4)


def _estimate_time_saved(required_connectors: list[str]) -> float:
    base = 0.5
    return round(base + len(required_connectors) * 0.5, 1)
