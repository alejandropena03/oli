"""Tests del orchestrator LLM-first via slice_001.

El orchestrator hardcodeado fue reemplazado. Estos tests validan el contrato
real del nuevo orchestrator con el MockModelAdapter — sin dependencias de red.

El MockModelAdapter devuelve "[mock-model] <prompt>", lo que provoca que el
LLM-first orchestrator falle en parse de JSON (intención) y en validación.
Ese comportamiento es honesto: sin modelo real, el output es degradado pero
auditable. Los tests verifican el contrato de pipeline, no el contenido.
"""
from packages.mission_kernel.mission_state import MissionStatus, StepStatus
from packages.orchestrator import run_research_brief_v1
from packages.orchestrator.model_adapter import MockIntentModelAdapter, MockModelAdapter


def test_slice_001_pipeline_runs_end_to_end():
    """El pipeline completa todos los estados — nunca cuelga."""
    mission = run_research_brief_v1(model=MockModelAdapter())

    assert mission.status in {
        MissionStatus.COMPLETED,
        MissionStatus.COMPLETED_PARTIAL,
        MissionStatus.FAILED,
    }
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


def test_slice_001_with_mock_intent_completes():
    """Con MockIntentModelAdapter el pipeline completa — no hay conectores requeridos."""
    mission = run_research_brief_v1(model=MockIntentModelAdapter())

    assert mission.status == MissionStatus.COMPLETED
    assert mission.validation_result is not None
    assert mission.validation_result.passed
    assert mission.report is not None
    assert mission.cost.input_tokens > 0
    assert mission.cost.model_cost_usd > 0


def test_slice_001_connector_required_field_is_serializable():
    """connector_required es un field real del schema — visible en serialización."""
    mission = run_research_brief_v1(model=MockIntentModelAdapter())

    assert mission.plan is not None
    for step in mission.plan.steps:
        # El field existe y es serializable — None o string, nunca KeyError
        step_dict = step.model_dump(mode="json")
        assert "connector_required" in step_dict


def test_slice_001_completed_partial_status_for_connector_missions():
    """Misiones con conectores faltantes terminan COMPLETED_PARTIAL, no FAILED."""
    from packages.orchestrator.model_adapter import MockIntentModelAdapter as Base

    class MockWithConnectors(Base):
        """MockIntentModelAdapter que simula una misión con conectores externos."""
        _INTENT_RESPONSE = """{
  "goal": "cockpit_test",
  "summary": "Cockpit con conectores externos",
  "success_criteria": ["conectar whatsapp", "mostrar mensajes"],
  "output_format": "cockpit",
  "required_connectors": ["whatsapp"],
  "scope_in": ["mensajes"],
  "scope_out": [],
  "steps": [
    {"order": 1, "description": "Leer WhatsApp", "executor": "Orchestrator",
     "required_connector": "whatsapp", "permission_class": 1},
    {"order": 2, "description": "Sintetizar resumen", "executor": "Orchestrator",
     "required_connector": null, "permission_class": 0}
  ],
  "confidence": 0.9
}"""

    mission = run_research_brief_v1(model=MockWithConnectors())

    assert mission.status == MissionStatus.COMPLETED_PARTIAL
    assert mission.plan is not None
    blocked = [s for s in mission.plan.steps if s.status == StepStatus.BLOCKED]
    completed = [s for s in mission.plan.steps if s.status == StepStatus.COMPLETED]
    assert len(blocked) == 1
    assert len(completed) == 1
    assert blocked[0].connector_required == "whatsapp"
    assert blocked[0].output is not None
    assert blocked[0].output.get("status") == "CONNECTOR_REQUIRED"
