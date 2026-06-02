"""Tests del orchestrator LLM-first via slice_001.

El orchestrator hardcodeado fue reemplazado. Estos tests validan el contrato
real del nuevo orchestrator con el MockModelAdapter — sin dependencias de red.

El MockModelAdapter devuelve "[mock-model] <prompt>", lo que provoca que el
LLM-first orchestrator falle en parse de JSON (intención) y en validación.
Ese comportamiento es honesto: sin modelo real, el output es degradado pero
auditable. Los tests verifican el contrato de pipeline, no el contenido.
"""
from packages.mission_kernel.mission_state import MissionStatus
from packages.orchestrator import run_research_brief_v1
from packages.orchestrator.model_adapter import MockModelAdapter


def test_slice_001_pipeline_runs_end_to_end():
    """El pipeline completa todos los estados hasta COMPLETED o FAILED — nunca cuelga."""
    mission = run_research_brief_v1(model=MockModelAdapter())

    assert mission.status in {MissionStatus.COMPLETED, MissionStatus.FAILED}
    assert mission.interpreted_intent is not None
    assert mission.plan is not None
    assert len(mission.plan.steps) >= 1


def test_slice_001_leaves_auditable_trace():
    """La misión siempre produce evidencia rastreable independientemente del resultado."""
    mission = run_research_brief_v1(model=MockModelAdapter())

    event_statuses = [e.to_status for e in mission.events]
    # Estos estados siempre ocurren antes del resultado
    for expected in [
        MissionStatus.INTAKE_RECEIVED,
        MissionStatus.INTERPRETING_INTENT,
        MissionStatus.RETRIEVING_CONTEXT,
        MissionStatus.CLASSIFYING_PERMISSIONS,
        MissionStatus.PLANNING,
        MissionStatus.EXECUTING,
        MissionStatus.VALIDATING,
    ]:
        assert expected in event_statuses, f"Estado {expected} no encontrado en el trace"

    evidence_kinds = {item.kind for item in mission.evidence}
    # Estos evidence kinds siempre deben estar presentes
    assert "intent_interpretation" in evidence_kinds
    assert "context" in evidence_kinds
    assert "plan" in evidence_kinds


def test_slice_001_intent_interpretation_is_auditable():
    """La interpretación de intención es rastreable — sin importar si el parse falló."""
    mission = run_research_brief_v1(model=MockModelAdapter())

    intent_evidence = next(
        (e for e in mission.evidence if e.kind == "intent_interpretation"), None
    )
    assert intent_evidence is not None
    assert "raw_input" in intent_evidence.data
    assert intent_evidence.data["raw_input"] != ""


def test_slice_001_custom_input_flows_through():
    """El raw_input del usuario llega al orchestrator y queda en evidencia."""
    custom = "Analiza el mercado de herramientas de productividad para startups."
    mission = run_research_brief_v1(raw_input=custom, model=MockModelAdapter())

    assert mission.raw_input == custom
    intent_evidence = next(
        (e for e in mission.evidence if e.kind == "intent_interpretation"), None
    )
    assert intent_evidence is not None
    assert intent_evidence.data["raw_input"] == custom
