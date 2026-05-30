# Sesión 04 — 2026-05-26

## Contexto
Sesión de corrección y consolidación. Se descubrió que el TDD de sesiones anteriores había ignorado documentación fundacional que ya existía (`docs_extracted/oli_technical_foundation_v2/`), llevando a decisiones de stack incorrectas (TypeScript/Mastra vs. Python/LangGraph). Se corrigió todo.

---

## El problema que se encontró

En sesiones 02-03 se construyó el TDD sobre:
- TypeScript + Bun (ADR-005 anterior)
- Mastra como framework de agentes (ADR-010 anterior)
- ChromaDB + SQLite como bases de datos

**El problema:** el `01_CANONICAL_STACK.md` que existía desde el inicio ya había decidido:
- Python + FastAPI
- LangGraph
- PostgreSQL + pgvector

Los ADRs anteriores contradecían los documentos fundacionales del proyecto. Se corrigieron.

---

## Decisiones confirmadas por el founder

| Decisión | Respuesta |
|---|---|
| Framework de orquestación | **LangGraph** (Python, durable, battle-tested) |
| Modelo de GPU | On-demand por detrás, suscripción fija para el usuario |
| Competencia primaria | Hacer lo mismo con APIs premium directas (Claude/GPT) |
| Investigación de mercado | Después de tener el TDD completo |
| Orden | TDD primero, luego market research, luego build |

---

## Artefactos creados / corregidos

| Artefacto | Acción |
|---|---|
| ADR-005 (TypeScript/Bun) | ❌ Eliminado — reemplazado |
| ADR-005-runtime-stack.md | ✅ Creado — Python + FastAPI + LangGraph |
| ADR-010 (Mastra/MCP) | ❌ Eliminado — reemplazado |
| ADR-010-langgraph-architecture.md | ✅ Creado — LangGraph completo con código Python real |
| ADR-016 (model routing simple) | ❌ Eliminado — reemplazado |
| ADR-016-model-routing-gpu-strategy.md | ✅ Creado — GPU on-demand, 3 tiers, modelo de negocio |
| ADR-017 (Mastra-specific) | ❌ Eliminado |
| domain/langgraph-mission-graph.md | ✅ Creado — mapeo state machine → LangGraph con código |
| stack/stack-decision.md | ✅ Reescrito — stack correcto con justificación |
| tdd/README.md | ✅ Actualizado — estado real, pendientes |

---

## Lo que reveló la auditoría de docs

El `docs_extracted/oli_technical_foundation_v2/` tiene 15 documentos fundacionales que no se habían leído en sesiones anteriores:

- `10_ICP_MOAT_AND_BUSINESS_MODEL.md` — ICP, moat, 4 modelos de pricing, data flywheel
- `01_CANONICAL_STACK.md` — Stack Python + LangGraph (el correcto)
- `00_TECHNICAL_THESIS.md` — Tesis técnica del producto
- `DECISION_MEMO_FOR_FOUNDER.md` — Decisiones clave ya tomadas

**Lección:** Siempre leer los docs fundacionales antes de tomar decisiones de arquitectura.

---

## Estado del TDD al cierre de sesión 04

| Área | Estado |
|---|---|
| Stack | ✅ Correcto — Python + LangGraph + Postgres |
| 16 ADRs | ✅ Todos coherentes con el stack correcto |
| LangGraph mission graph | ✅ Completo con código Python |
| Model routing + GPU | ✅ On-demand, 3 tiers, modelo de negocio |
| Schemas | ✅ 5 schemas (especificación en TS, implementación en Python) |
| Domain model | ✅ Event storming, state machine, flows |
| Tools catalog | ✅ 10 núcleo con ejemplos |
| System prompts de Oli | 🔲 Pendiente |
| Setup wizard spec | 🔲 Pendiente |
| Pricing formal (valores reales) | 🔲 Post investigación de mercado |
| Mission Kernel V0 (código) | 🔲 Próximo paso |

## Próximos pasos en orden

1. Completar items pendientes del TDD (system prompts, setup wizard)
2. Investigación de mercado (competencia, precios, ICP validado)
3. Build V0: pyproject.toml → mission_kernel → orchestrator → API → test slice-001
