# Oli — Technical Design Document (TDD)

Este directorio es la fuente de verdad técnica del proyecto.
**El código implementa lo que está aquí — no al revés.**

---

## Reglas inamovibles

1. **Nunca borrar ADRs** — solo se pueden marcar como `deprecated` o `superseded`
2. **Los schemas son contratos** — si cambias un schema, actualizas todos los módulos que lo usan
3. **Los slices validan la arquitectura** — si no puedes describir una misión de punta a punta, la arquitectura está incompleta
4. **Toda decisión de tecnología tiene un ADR** — no se elige stack sin documentar el porqué

---

## Stack definitivo (resumen ejecutivo)

```
Backend:         Python 3.12 + FastAPI
Orquestación:    LangGraph (mission graph, state, checkpoints, human-in-the-loop)
Base de datos:   PostgreSQL 16 + pgvector (estado + RAG en una sola DB)
Modelos locales: Ollama (V0) → vLLM (V2+)
GPU strategy:    On-demand por detrás, suscripción fija para el usuario
Frontend:        Next.js 15 + TypeScript (dashboard, TV view)
```

Ver [stack/stack-decision.md](stack/stack-decision.md) para el detalle completo.

---

## Estructura

```
tdd/
├── README.md                   → Este archivo
├── adrs/                       → Architecture Decision Records (17 ADRs)
├── domain/
│   ├── oli-constitution.md     → LA CONSTITUCIÓN — 14 pilares en 3 niveles (v1.0)
│   ├── system-prompts.md       → Prompt raíz + prompts de suboperadores + microcopy
│   ├── event-storming.md       → 46 eventos, 28 políticas — V3
│   ├── state-machine.md        → 18 estados de misión
│   ├── langgraph-mission-graph.md → Cómo LangGraph implementa la state machine
│   ├── mission-flows.md        → 3 flujos de punta a punta
│   ├── tools-catalog.md        → 10 herramientas núcleo con ejemplos
│   ├── promise-validation.md   → Demostración de la promesa
│   ├── connectivity-map.md     → Jerarquía de decisión de conectividad
│   ├── state-of-art-discovery.md → Decision memos actuales con evidencia y buildability
│   ├── state-of-art-evals.md     → Evals de recomendaciones no flojas
│   ├── subagent-engineering.md   → MissionClass, AgentTaskContract, ContextPacket, TopologyDecision
│   ├── subagent-evals.md         → Eval plan para topologías de subagentes
│   └── setup-wizard-spec.md    → Instalación y configuración de hardware
├── schemas/                    → Contratos de datos (TypeScript como especificación)
│   ├── mission.ts              → Agregado principal — 18 estados, plan, repair, evidence
│   ├── memory.ts               → 3 capas de memoria, MemoryGraph interface
│   ├── tool.ts                 → 14 transports, permissions, configs
│   ├── playbook.ts             → Playbook, variables, steps
│   ├── suboperator.ts          → 8 suboperadores, contratos de output
│   ├── subagent_contracts.ts   → MissionClass, ContextPacket, TaskResult, TopologyDecision
│   └── decision_memo.ts        → State-of-the-art decision memo contract
├── slices/
│   ├── slice-001-research-brief.md → Misión simple end-to-end en papel
│   └── slice-002-sales-automation.md → Misión compleja con construcción de sistema
└── stack/
    └── stack-decision.md       → Stack completo con justificación
```

**Nota sobre schemas:** Los archivos `.ts` son la especificación de contratos de datos.
La implementación real será en Python (Pydantic models). Los schemas TS documentan
la estructura — no son el código de producción.

---

## Estado actual de artefactos

### Domain Model
| Artefacto | Estado | Notas |
|---|---|---|
| **Constitución de Oli** | ✅ v1.0 | 14 pilares en 3 niveles — el carácter de Oli |
| **System Prompts** | ✅ completo | Prompt raíz + 5 suboperadores + microcopy |
| Event Storming | ✅ V3 | 46 eventos, 28 políticas, 12 hotspots |
| State Machine | ✅ V1 | 18 estados, 30 transiciones |
| LangGraph Mission Graph | ✅ completo | Mapeo state machine → grafo Python con código |
| Mission Flows | ✅ completo | 3 flujos reales demostrados |
| Tools Catalog | ✅ completo | 10 núcleo + opcionales con ejemplos |
| Slice-001: Research Brief | ✅ en papel | Misión simple end-to-end |
| Slice-002: Sales Automation | ✅ en papel | Misión compleja — 2 gaps identificados |
| Setup Wizard | ✅ completo | 5 pasos, 4 perfiles de hardware |
| Promise Validation | ✅ completo | Cada capacidad demostrada |
| AI Engineering Skill Signal | moved | Movido a Consultor Estrategico Codex/02_estrategia_producto/ — es estratégico, no TDD core |
| Subagent Engineering | ✅ accepted | Contratos, topologias y roles canonicos (ADR-023) |
| Subagent Evals | eval plan | Baseline single-agent vs topologias candidatas |
| State-of-Art Discovery | ✅ accepted | Decision memos con evidencia, source quality, buildability y risk checks |
| State-of-Art Evals | eval plan | Evalua frescura, fuentes, alternativas, buildability y accionabilidad |

### ADRs — Architecture Decision Records
| ADR | Título | Estado |
|---|---|---|
| 001 | Model strategy (model-agnostic, routing dinámico) | ✅ accepted |
| 002 | Execution sandbox (Docker, progresivo) | ✅ accepted |
| 003 | Memoria infinita con RAG (pgvector desde V0) | ✅ accepted |
| 004 | Permission model (5 clases 0-4) | ✅ accepted |
| **018** | **Multi-user y trabajo en equipo** | ✅ accepted |
| 005 | Runtime stack (Python + FastAPI + LangGraph) | ✅ accepted |
| 006 | Troubleshooting real (diagnóstico, no reintentos ciegos) | ✅ accepted |
| 007 | Clarificación de intención (sin límite fijo, inferencia primero) | ✅ accepted |
| 008 | Misiones paralelas (Mission Queue Manager) | ✅ accepted |
| 009 | Memoria auto-write (Oli guarda, founder edita) | ✅ accepted |
| 010 | LangGraph architecture (grafo, nodos, checkpoints) | ✅ accepted |
| 011 | Browser strategy (Stagehand + Playwright + CDP) | ✅ accepted |
| 012 | Desktop execution (ClawdCursor + E2B) | ✅ accepted |
| 013 | OpenClaw integration (opt-in, no dependencia dura) | ✅ accepted |
| 014 | Auth & credentials (brokered, OS Keychain, OAuth PKCE) | ✅ accepted |
| 015 | UI nativa (Next.js + Electron wrapper, TV via HDMI/Cast) | ✅ accepted |
| 016 | Model routing + GPU strategy (on-demand, 3 tiers) | ✅ accepted |
| 021 | Dedicated Oli Runtime y entorno de ejecucion del usuario | ✅ accepted |
| 022 | Public Oli Labs y frontera private core/public proof | ✅ accepted |
| 023 | Subagent engineering contracts | ✅ accepted |
| 025 | State-of-the-art discovery and decision memos | ✅ accepted |

### Schemas (especificación de contratos)
| Schema | Estado | Nota |
|---|---|---|
| mission.ts | ✅ completo | Se implementa como Pydantic en Python |
| memory.ts | ✅ completo | ídem |
| tool.ts | ✅ completo | ídem |
| playbook.ts | ✅ completo | ídem |
| suboperator.ts | ✅ completo | ídem |
| subagent_contracts.ts | ✅ v0 | Capa contractual superior para MissionClass, ContextPacket, AgentTaskResult y TopologyDecision |
| decision_memo.ts | ✅ v0 | Contrato para recomendaciones actuales y auditables |

### Stack
| Artefacto | Estado |
|---|---|
| Stack decision completo | ✅ definitivo |
| Estructura de directorios | ✅ definida |

---

## Pendiente antes del build

| Item | Prioridad | Descripción |
|---|---|---|
| Slice-002 | Alta | Segunda misión end-to-end en papel (sistema de ventas) |
| Pricing formal | Alta | Investigación de mercado → 3 tiers con precios reales |
| System prompts | Alta | Prompt raíz de Oli + prompts de cada suboperador |
| Setup wizard spec | Media | Cómo Oli detecta GPU y configura modelos |
| Claude Code en tools-catalog | Media | Agregar Claude Code como herramienta de desarrollo |
| ADR-016 — Pricing tier values | Media | Los precios reales (post investigación de mercado) |

---

## Próximo paso: Build V0

Orden estricto — nunca saltear:

```
1. pyproject.toml / requirements.txt
   Dependencias: fastapi, langgraph, sqlalchemy, psycopg2, ollama, pytest

2. packages/mission_kernel/
   - mission_state.py    (Pydantic models de MissionState)
   - state_machine.py    (18 estados, transiciones válidas)
   - policies.py         (reglas: quién puede hacer qué)

3. packages/orchestrator/
   - mission_graph.py    (LangGraph graph builder)
   - nodes.py            (cada nodo del grafo)
   - router.py           (conditional edges)

4. apps/api/
   - main.py             (FastAPI app)
   - missions.py         (endpoints: create, get, approve)

5. tests/
   - test_slice_001.py   (Research brief de punta a punta, todo mockeado)
```
