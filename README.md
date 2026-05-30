# /oli

> **Oli es el supervisor de ejecución digital que convierte intención humana en trabajo terminado, validado y auditable** — coordinando modelos locales, agentes externos, herramientas, memoria y permisos bajo un único operador que el usuario controla.

Marca operativa: `/oli` · Marca verbal: Oli

---

## Estado del proyecto

**Fase actual:** Pre-build (V0). Fundación técnica + marca + TDD completos. Próximo paso: implementar el Mission Kernel.

| Capa | Estado |
|---|---|
| Constitución de Oli (14 pilares) | ✅ v1.0 |
| Lenguaje de marca | ✅ v0.1 |
| Brandbook + assets | ✅ Generado por pipeline |
| Foundation técnica (13 docs) | ✅ Completa |
| TDD (17 ADRs, 5 schemas, 2 slices) | ✅ En papel |
| Pricing model | ✅ v6 (definitivo) |
| Market research | ✅ 2026-05-27 |
| Build V0 (Mission Kernel) | 🔜 Próximo |

---

## Estructura del repo

```
oli/
├── bitacora/                          → Sesiones de trabajo cronológicas (01-07)
├── brand/                             → Pipeline de marca (logos, brandbook, landing, social)
│   ├── tokens/                        → CSS tokens (colors, spacing, typography)
│   ├── logos/                         → SVGs de wordmark/icon en dark/light/mono
│   ├── brandbook/index.html           → Brandbook generado
│   ├── landing/index.html             → Landing page
│   └── scripts/                       → Build scripts (Node)
├── docs_extracted/                    → Foundation técnica V2 (13 docs) + research
│   ├── oli_technical_foundation_v2/   → 00_THESIS → 13_DIAGRAMS + DECISION_MEMO
│   └── oli_docs/                      → OLI_MASTER_SPEC + market research suboperator
├── playbooks/                         → Workflows reutilizables (vacío — primer candidato: research-brief-v1)
├── tdd/                               → Technical Design Document — fuente de verdad técnica
│   ├── adrs/                          → 17 Architecture Decision Records
│   ├── domain/                        → Constitución, event storming, state machine, system prompts, pricing v2-v6
│   ├── schemas/                       → Contratos de datos en TypeScript (se implementan en Pydantic)
│   ├── slices/                        → Misiones end-to-end en papel
│   └── stack/                         → Decisión de stack definitiva
├── oli_lenguaje_de_marca_v0_1.md      → Lenguaje de marca completo
└── _oli Brandbook by Pomelli.pdf      → Brandbook impreso de referencia
```

---

## Stack definitivo (resumen)

```
Backend:         Python 3.12 + FastAPI
Orquestación:    LangGraph (mission graph, state, checkpoints, HITL)
Base de datos:   PostgreSQL 16 + pgvector (estado + RAG en una sola DB)
Cache/Queue:     Valkey (no Redis)
Object storage:  SeaweedFS (no MinIO — archivado en 2026)
Modelos locales: Ollama (V0) → vLLM (V2+) — Qwen3 27B y 35B-A3B MoE
GPU strategy:    On-demand por detrás, suscripción fija para el usuario
Frontend:        Next.js 15 + TypeScript (dashboard, TV view)
Browser:         Stagehand v3 CDP-native + browser-use
Sandbox:         Docker (V0-V2) → E2B/ClawdCursor opcional (V3+)
```

Detalle: `tdd/stack/stack-decision.md`

---

## Pricing (V6)

| Tier | Precio | Seats | Créditos | Overage |
|---|---|---|---|---|
| Starter | $79/mes | 1 | 660 | $0.09/cr |
| Pro | $129/seat/mes | máx 3 | 1,100/seat (pool) | $0.08/cr |
| Team | $199/seat/mes | mín 4 | 1,500/seat (pool) | $0.08/cr |

1 crédito = 1 minuto de GPU activa. Detalle: `tdd/domain/pricing-model-v6.md`

---

## ICP por versión

```
V0-V1:   Founder / Builder  +  Product/Engineering Ops
V2-V3:   Equipos pequeños founder-led  +  Agencias/consultoras
V3-V4:   Growth/RevOps  +  Operaciones internas
V5+:     Empresas 50-200 con compliance
```

---

## Próximo paso: Build V0 — Mission Kernel

Orden estricto (de `tdd/README.md`):

1. `pyproject.toml` — fastapi, langgraph, sqlalchemy, psycopg2, ollama, pytest
2. `packages/mission_kernel/` — mission_state.py, state_machine.py (18 estados), policies.py
3. `packages/orchestrator/` — mission_graph.py, nodes.py, router.py
4. `apps/api/` — FastAPI app + endpoints de misiones
5. `tests/test_slice_001.py` — research brief end-to-end mockeado

---

## Reglas inamovibles del TDD

1. **Nunca borrar ADRs** — solo `deprecated` o `superseded`
2. **Los schemas son contratos** — si cambias un schema, actualizas todos los módulos que lo usan
3. **Los slices validan la arquitectura** — si no podés describir una misión end-to-end, la arquitectura está incompleta
4. **Toda decisión de tecnología tiene un ADR**

---

## Carácter

> Oli no es otro agente que usa herramientas. Es el supervisor que coordina agentes.
>
> El moat no es un modelo. El modelo va a cambiar. El moat es la capa de supervisión alrededor de todos los modelos y agentes.

Ver `tdd/domain/oli-constitution.md` — los 14 pilares en 3 niveles (Carácter, Operación, Producto).
