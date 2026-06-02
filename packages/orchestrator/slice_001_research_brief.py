"""slice_001_research_brief — delegated to intent_driven_orchestrator.

El orchestrator hardcodeado fue reemplazado. Esta interfaz se mantiene para
compatibilidad con la API y tests existentes, pero ahora delega al orchestrator
LLM-first que interpreta el raw_input real del usuario.
"""
from __future__ import annotations

from packages.mission_kernel.mission_state import Mission
from packages.orchestrator.intent_driven_orchestrator import run_intent_driven_mission
from packages.orchestrator.model_adapter import ModelAdapter


SLICE_001_INPUT = (
    "Investiga los 3 principales competidores de Oli y dame un brief de 1 pagina "
    "con sus fortalezas, debilidades y el gap que Oli puede explotar."
)


def run_research_brief_v1(
    raw_input: str = SLICE_001_INPUT,
    model: ModelAdapter | None = None,
) -> Mission:
    return run_intent_driven_mission(raw_input=raw_input, model=model)
