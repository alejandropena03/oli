# Repo Map — Oli

Guía de navegación para agentes. Antes de buscar un archivo, consulta este mapa.
Actualizar cuando se agreguen archivos o carpetas relevantes.

---

## Raíz

| Archivo | Qué contiene | Cuándo leerlo |
|---|---|---|
| `CLAUDE.md` | Startup protocol de Claude Code | Claude al arrancar |
| `AGENTS.md` | Startup protocol de DeepSeek/opencode | DeepSeek al arrancar |
| `.env.example` | Variables de entorno documentadas | Al configurar entorno local |
| `pyproject.toml` | Dependencias Python y config pytest | Al instalar o agregar deps |
| `openrouter_docs.txt` | Índice de docs de OpenRouter | Al trabajar con modelos/routing |

---

## .bridge/

Canal de comunicación entre agentes. Leer SIEMPRE al arrancar.

| Archivo | Qué contiene |
|---|---|
| `CURRENT_TASK.md` | Tarea activa — quién la tiene, qué hacer, criterio de éxito |
| `HANDOFF_LOG.md` | Historial de transfers entre agentes (append-only) |
| `PENDIENTES.md` | Sistema compartido de pendientes con prioridades |
| `BITACORA.md` | Log de progreso por sesión — qué se hizo, qué sigue |
| `README.md` | Protocolo completo del bridge |
| `tasks/` | Tareas archivadas e inmutables una vez cerradas |

---

## tdd/ — Fuente de verdad técnica

**Regla: el código implementa lo que está aquí, no al revés.**

| Archivo/Carpeta | Qué contiene | Cuándo leerlo |
|---|---|---|
| `tdd/README.md` | Estado de todos los artefactos TDD, stack definitivo | Al arrancar cualquier tarea técnica |
| `tdd/adrs/README.md` | Lista de todos los ADRs con estado | Al tomar decisiones de arquitectura |
| `tdd/stack/stack-decision.md` | Stack completo justificado | Al agregar dependencias o cambiar infra |

### tdd/adrs/ — Architecture Decision Records

| ADR | Decisión |
|---|---|
| ADR-001 | Model strategy — model-agnostic, routing dinámico |
| ADR-002 | Execution sandbox — Docker, progresivo |
| ADR-003 | Memoria infinita con RAG — pgvector desde V0 |
| ADR-004 | Permission model — 5 clases 0-4 |
| ADR-005 | Runtime stack — Python + FastAPI + LangGraph |
| ADR-006 | Troubleshooting — diagnóstico real, no reintentos ciegos |
| ADR-007 | Clarificación de intención — inferencia primero |
| ADR-008 | Misiones paralelas — Mission Queue Manager |
| ADR-009 | Memoria auto-write — Oli guarda, founder edita |
| ADR-010 | LangGraph architecture — grafo, nodos, checkpoints |
| ADR-011 | Browser strategy — Stagehand + Playwright + CDP |
| ADR-012 | Desktop execution — ClawdCursor + E2B |
| ADR-013 | OpenClaw integration — opt-in |
| ADR-014 | Auth & credentials — brokered, OS Keychain, OAuth PKCE |
| ADR-015 | UI nativa — Next.js + Electron |
| ADR-016 | Model routing + GPU strategy — 3 tiers on-demand |
| ADR-018 | Multi-user y trabajo en equipo |
| ADR-021 | Dedicated Oli Runtime — instancia dedicada por tenant |
| ADR-022 | Public Oli Labs — core privado / labs públicos |
| ADR-023 | Subagent Engineering Contracts — single orchestrator por defecto |
| ADR-025 | State-of-Art Discovery — decision memos con source quality |

### tdd/domain/ — Especificaciones de dominio

| Archivo | Qué contiene |
|---|---|
| `oli-constitution.md` | **LA CONSTITUCIÓN** — 14 pilares en 3 niveles. Leer antes de cualquier decisión de producto |
| `system-prompts.md` | Prompt raíz de Oli + 5 suboperadores |
| `event-storming.md` | 46 eventos, 28 políticas — V3 |
| `state-machine.md` | 18 estados de misión y transiciones |
| `langgraph-mission-graph.md` | Cómo LangGraph implementa la state machine |
| `mission-flows.md` | 3 flujos reales de punta a punta |
| `tools-catalog.md` | 10 herramientas núcleo con ejemplos |
| `connectivity-map.md` | Jerarquía de decisión de conectividad |
| `subagent-engineering.md` | MissionClass, AgentTaskContract, ContextPacket, TopologyDecision |
| `subagent-evals.md` | Eval plan para topologías de subagentes |
| `state-of-art-discovery.md` | Spec del discovery engine con source quality |
| `state-of-art-evals.md` | Evals de recomendaciones no flojas |
| `setup-wizard-spec.md` | Setup wizard — 5 pasos, 4 perfiles hardware |

### tdd/schemas/ — Contratos de datos (TypeScript como especificación)

| Schema | Qué define |
|---|---|
| `mission.ts` | Agregado principal — 18 estados, plan, repair, evidence |
| `memory.ts` | 3 capas de memoria, MemoryGraph interface |
| `tool.ts` | 14 transports, permissions, configs |
| `playbook.ts` | Playbook, variables, steps |
| `suboperator.ts` | 8 suboperadores, contratos de output |
| `subagent_contracts.ts` | MissionClass, AgentTaskContract, ContextPacket, AgentTaskResult, ValidatorContract, TopologyDecision |
| `decision_memo.ts` | StateOfArtDecisionMemo — source quality, options, buildability, risk |

---

## packages/ — Código Python del core

| Módulo | Qué hace | Archivos clave |
|---|---|---|
| `mission_kernel/` | Estados, transiciones, permisos, eventos | `mission_state.py`, `state_machine.py`, `policies.py` |
| `orchestrator/` | LangGraph graph, nodos, routing, misiones | `mission_graph.py`, `nodes.py`, `router.py`, `weekly_client_report.py`, `draft_outreach.py`, `slice_001_research_brief.py` |
| `mission_store/` | Persistencia JSON y SQLAlchemy | `json_store.py`, `sqlalchemy_store.py`, `factory.py` |
| `model_router/` | Routing de modelos por tier y privacy mode | `router.py`, `status.py` |
| `orchestrator/model_adapter.py` | Adaptadores: development, Ollama, OpenAI-compatible, webhook, fallback | — |
| `config/` | Loader de variables de entorno | `env.py` |

---

## apps/ — API

| Archivo | Qué hace |
|---|---|
| `apps/api/main.py` | FastAPI app — endpoints raíz y health |
| `apps/api/missions.py` | Endpoints de misiones, eventos, evidencia, approve/reject |
| `apps/api/models.py` | Pydantic models de request/response |

**Endpoints disponibles:**
- `GET /health`
- `GET /missions`
- `POST /missions/research-brief`
- `POST /missions/weekly-client-report`
- `POST /missions/draft-outreach`
- `GET /missions/{id}`, `/events`, `/evidence`, `/report`
- `POST /missions/{id}/approve`, `/reject`
- `GET /models/status`, `POST /models/test`

---

## tests/

| Archivo | Qué testea |
|---|---|
| `test_mission_kernel.py` | Estados, transiciones, permisos |
| `test_api_v0.py` | Endpoints FastAPI |
| `test_draft_outreach.py` | Misión clase 3 con approval gate |
| `test_weekly_client_report.py` | Misión ICP agencias |
| `test_langgraph_mission_graph.py` | Grafo LangGraph |
| `test_model_router_tiers.py` | Routing por tier y privacy |
| `test_mission_store.py` | JSON store y SQLAlchemy store |
| `test_slice_001_mock.py` | Research brief end-to-end mockeado |
| `test_v0_acceptance.py` | Contrato vivo de V0 |
| `test_model_adapter.py`, `test_model_router_status.py`, `test_env_config.py`, `test_configure_openrouter_key.py` | Infra y config |

**Correr todos:** `python -m pytest` — debe dar 45 passed.

---

## scripts/

| Script | Qué hace |
|---|---|
| `run_api.ps1` | Levanta uvicorn desde cualquier carpeta |
| `restart_api.ps1` | Mata proceso y reinicia |
| `configure_openrouter_key.py` | GUI para configurar OpenRouter key |
| `test_openrouter_model.py` | Prueba un modelo vía OpenRouter |

---

## Consultor Estrategico Codex/ — Memoria estratégica

Documentos de análisis y decisiones del proyecto. No es código — es contexto.

| Subcarpeta | Qué contiene |
|---|---|
| `00_contexto/` | Estado vivo del proyecto, tracking estratégico, cierres de sesión |
| `01_auditorias/` | Auditoría V0 post-incidente, prompt engineering |
| `02_estrategia_producto/` | ICP, runtime brief, skill signal profesional |
| `03_runtime_y_arquitectura/` | Runtime SSH, dedicated runtime, memoria SOTA |
| `04_subagents/` | Subagent engineering SOTA con fuentes primarias |
| `05_research_stack/` | Discovery SOTA, OpenRouter, leverage open source, research_stack_v0 |
| `06_fine_tuning/` | Fine-tuning serio: análisis completo, pipeline recomendado |
| `07_presentaciones/` | HTMLs de pitch y presentaciones |
| `08_assets/` | Imágenes y assets |
| `99_archivo/` | Material superado, sin borrar |

**Archivos clave para contexto rápido:**
- `00_contexto/03_tracking_estrategico.md` — decisiones, riesgos, próximos pasos
- `00_contexto/05_estado_v0_implementacion.md` — qué está implementado exactamente
- `01_auditorias/12_auditoria_v0_post_incidente_2026-05-31.md` — auditoría técnica completa

---

## brand/

Assets de marca. No tocar salvo trabajo de UI/brand.
`dist/` tiene logos, favicons, heroes y social assets listos para producción.

---

## .agents/

Skills configuradas para agentes. `skills/lookml-modeling-guidelines/` — no relevante para Oli core.

---

## Variables de entorno (`.env.local`)

```
OLI_MISSION_STORE=sqlalchemy          # o "json" para dev sin Postgres
OLI_DATABASE_URL=postgresql+psycopg2://oli:oli@localhost:5432/oli
OPENROUTER_API_KEY=sk-or-...
OLI_MODEL_PROVIDER=openai_compatible  # o "development", "ollama"
OLI_DEFAULT_MODEL=openrouter/quasar-alpha
```
