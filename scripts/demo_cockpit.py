"""
Demo: Communication Cockpit Mission Kernel
Muestra el desglose completo de una mision real a traves del Mission Kernel de Oli.
Sin conectores reales — el kernel, los permisos, el plan y la evidencia son reales.

Correr desde la raiz del repo:
    python scripts/demo_cockpit.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from packages.config.env import load_env_file
load_env_file()

from packages.orchestrator.cockpit_comms import run_cockpit_comms_mission, COCKPIT_INPUT


def separator(title: str = "", char: str = "─", width: int = 70) -> None:
    if title:
        side = (width - len(title) - 2) // 2
        print(f"\n{'─' * side} {title} {'─' * side}")
    else:
        print("─" * width)


def main() -> None:
    print("\n" + "═" * 70)
    print("  OLI — MISSION KERNEL DEMO")
    print("  Communication Cockpit")
    print("═" * 70)

    print(f"\n📥 INPUT DEL USUARIO:\n\"{COCKPIT_INPUT}\"\n")

    print("Ejecutando Mission Kernel...\n")
    mission = run_cockpit_comms_mission()

    # ── ESTADO FINAL ─────────────────────────────────────────────────────────
    separator("ESTADO FINAL DE LA MISIÓN")
    print(f"  ID:      {mission.id}")
    print(f"  Estado:  {mission.status.upper()}")
    print(f"  Fuente:  {mission.source}")
    print(f"  Clase de permiso: {mission.permission_class.value} — {mission.permission_class.name}")

    # ── INTENCIÓN INTERPRETADA ────────────────────────────────────────────────
    separator("INTENCIÓN INTERPRETADA")
    intent = mission.interpreted_intent
    print(f"  Goal:       {intent.goal}")
    print(f"  Confianza:  {intent.confidence:.0%}")
    print(f"\n  Criterios de éxito ({len(intent.success_criteria)}):")
    for c in intent.success_criteria:
        print(f"    ✓ {c}")
    print(f"\n  En scope:")
    for s in intent.scope["in_scope"]:
        print(f"    → {s}")
    print(f"\n  Fuera de scope (Oli NO hará esto):")
    for s in intent.scope["out_of_scope"]:
        print(f"    ✗ {s}")

    # ── PLAN ──────────────────────────────────────────────────────────────────
    separator("PLAN DE EJECUCIÓN")
    plan = mission.plan
    print(f"  {len(plan.steps)} pasos | Clase máxima: {plan.total_permission_class.name}")
    print(f"  Estimado: {plan.estimates['duration_ms']/1000:.0f}s | "
          f"${plan.estimates['cost_usd']:.2f} | "
          f"{plan.estimates['human_time_saved_hr']}h ahorradas\n")
    for step in plan.steps:
        icon = "✅" if step.status.value == "completed" else "⏳"
        tools = f" [{', '.join(step.required_tools)}]" if step.required_tools else " [sin tools externas]"
        print(f"  {icon} Paso {step.order}: {step.description}")
        print(f"       Ejecutor: {step.executor}{tools}")
        print(f"       Permiso: clase {step.permission_class.value} ({step.permission_class.name})")

    # ── TRAIL DE ESTADOS ──────────────────────────────────────────────────────
    separator("TRAIL DE ESTADOS (audit log)")
    for i, event in enumerate(mission.events):
        arrow = "→" if i > 0 else " "
        print(f"  {arrow} {event.to_status:<30} [trigger: {event.trigger}]")

    # ── VALIDACIÓN ────────────────────────────────────────────────────────────
    separator("VALIDACIÓN")
    vr = mission.validation_result
    print(f"  Resultado: {'✅ PASSED' if vr.passed else '❌ FAILED'} | Score: {vr.score:.0%}\n")
    for c in vr.criteria_results:
        icon = "✅" if c["passed"] else "❌"
        print(f"  {icon} {c['criterion']}")
        print(f"       Evidencia: {c['evidence']}")

    # ── BRIEFING ENTREGADO ────────────────────────────────────────────────────
    separator("BRIEFING ENTREGADO AL USUARIO")
    briefing = mission.output
    print(f"\n  📋 {briefing['resumen_ejecutivo']}\n")

    if briefing["alertas_criticas"]:
        print("  🚨 ALERTAS CRÍTICAS:")
        for a in briefing["alertas_criticas"]:
            print(f"    [{a['urgencia']}] {a['canal']} — {a['de']}")
            print(f"    Asunto: {a['asunto']} — sin respuesta hace {a['sin_respuesta_hace']}")
            print(f"    Acción sugerida: {a['accion_sugerida']}\n")

    print("  📌 PENDIENTES POR CANAL:")
    for canal, items in briefing["pendientes_por_canal"].items():
        if items:
            print(f"\n    {canal}:")
            for item in items:
                print(f"      • {item}")
        else:
            print(f"\n    {canal}: sin pendientes")

    totales = briefing["totales"]
    print(f"\n  📊 TOTALES: {totales['mensajes_nuevos']} mensajes nuevos | "
          f"{totales['requieren_accion']} requieren acción | "
          f"{totales['solo_fyi']} solo FYI")

    print(f"\n  💬 NOTA DE OLI: {briefing['nota_de_oli']}")

    # ── REPORTE FINAL ─────────────────────────────────────────────────────────
    separator("REPORTE FINAL")
    report = mission.report
    print(f"  {report.summary}")
    print(f"\n  Pasos completados: {report.steps_completed}/{report.steps_total}")
    print(f"  Costo: ${report.cost.total_cost_usd:.2f}")
    print(f"  Tiempo humano ahorrado: {report.cost.human_time_saved_hr}h")
    print(f"\n  ♻️  Playbook candidato: {'SÍ' if report.playbook_candidate else 'NO'}")
    if report.playbook_candidate_reason:
        print(f"  Razón: {report.playbook_candidate_reason}")

    # ── EVIDENCIA ─────────────────────────────────────────────────────────────
    separator("EVIDENCIA REGISTRADA (audit trail)")
    print(f"  {len(mission.evidence)} registros de evidencia:\n")
    for ev in mission.evidence:
        print(f"  [{ev.kind}] {ev.title}")

    # ── CONECTORES PENDIENTES ──────────────────────────────────────────────────
    separator("CONECTORES REQUERIDOS PARA VERSIÓN REAL")
    conectores = [
        ("WhatsApp", "WhatsApp Business API o MCP", "V2", "no disponible como MCP oficial"),
        ("Slack", "Slack MCP oficial", "HOY", "✅ disponible — Claude Code lo tiene"),
        ("Gmail", "Gmail MCP oficial", "HOY", "✅ disponible — Claude Code lo tiene"),
        ("Instagram", "Instagram Graph API", "V2", "requiere Meta Business verification"),
    ]
    for canal, conector, version, nota in conectores:
        print(f"  {canal:<12} {conector:<35} [{version}] {nota}")

    separator()
    print(f"\n  Mission ID:  {mission.id}")
    print(f"  Status:      {mission.status.upper()}")
    print(f"  Eventos:     {len(mission.events)} transiciones registradas")
    print(f"  Evidencia:   {len(mission.evidence)} registros auditables")
    print("\n" + "═" * 70)
    print("  Esto es el Mission Kernel de Oli.")
    print("  Sin conectores reales hoy — con ellos, este briefing sería tuyo cada mañana.")
    print("═" * 70 + "\n")


if __name__ == "__main__":
    main()
