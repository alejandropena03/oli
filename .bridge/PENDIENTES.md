# Pendientes — Sistema compartido

Ambos agentes pueden agregar items. Formato: `- [ ] descripción — @quien — prioridad`.
Marcar completados con `- [x]`. No borrar items completados.

---

## Técnicos — V0 → V1

- [x] Conectar Postgres 18 real con Docker en Mac — @local_agent — DONE 2026-06-01
- [x] Conectar PostgresSaver de LangGraph (checkpointing real) — @claude — DONE 2026-06-01
- [x] Correr 4 integration tests de PostgresSaver contra Postgres real — @local_agent — DONE 2026-06-02
- [x] Instalar `langgraph-checkpoint-postgres` y `psycopg[binary]` en Mac — @local_agent — DONE 2026-06-02
- [ ] Crear evals formales para las 3 mission classes — @claude — pendiente validación Postgres
- [ ] Agregar tool guardrails reales antes de conectar herramientas externas — @claude — pendiente evals
- [ ] ADR-024: Model Intelligence (decidido, no escrito) — @claude — media
- [ ] ADR-026: Terminal/SSH Security (decidido, no escrito) — @claude — media
- [ ] Actualizar slices 001 y 002 para reflejar topología de subagentes (ADR-023) — @claude — baja

## Infraestructura — Bridge

- [x] Agregar `.opencode/` al `.gitignore` — @local_agent — DONE 2026-06-01
- [x] Probar flujo completo del bridge: tarea de Claude → ejecución Mac → validación — @ambos — DONE 2026-06-01
- [ ] Documentar conectores y tools disponibles en Mac — @local_agent — media

## Estrategia — Pendientes de Codex

- [ ] Decidir primer fine-tune lab: Permission Policy Adapter vs MissionSpec Normalizer — @alejandro — cuando V0 esté sólido
- [ ] Definir farming/onboarding loop en la Constitución de Oli — @claude — V1
- [ ] Crear mission-class: founder_notes_to_claude_code_spec (primera misión real con subagentes) — @claude — V1
- [ ] Revisitar memoria SOTA: jerarquía explícita, temporal graph, write-time reconciliation — @claude — V2
- [ ] Decidir si runtime/SSH entra en V2 o V3 — @alejandro — cuando Postgres esté listo

## Organización — Repo

- [x] Reorganizar Consultor Estrategico Codex/ en subcarpetas — @claude — DONE 2026-06-01
- [x] Crear sistema bridge bidireccional — @claude — DONE 2026-06-01
- [x] Crear CLAUDE.md — @claude — DONE 2026-06-01
- [x] Actualizar AGENTS.md con nueva identidad — @claude — DONE 2026-06-01
