# Stack Decision — Oli

**Fecha:** 2026-05-26
**Fuente:** 01_CANONICAL_STACK.md + ADR-005 + ADR-010
**Estado:** Definitivo

---

## Stack completo

| Capa | Tecnología | Rol | Versión de entrada |
|---|---|---|---|
| OS | Ubuntu Server 24.04 LTS | Base del servidor | V0 |
| Backend API | Python 3.12 + FastAPI | API principal de Oli | V0 |
| Orquestación de agentes | LangGraph | Mission graph, state, checkpoints, human-in-the-loop | V0 |
| Base de datos | PostgreSQL 16 + pgvector | Estado + memoria semántica (una sola DB) | V0 |
| Cache / eventos | **Valkey** (fork Redis, Linux Foundation) | Mission feed en tiempo real → dashboard | V1 |
| Artifacts | **SeaweedFS** (MinIO archivado Feb 2026) | Archivos, reportes, audio, logs | V0 |
| Modelos locales | Ollama → LocalAI → vLLM/SGLang | Runtime LLMs (Tier 1 y 2) — LocalAI como abstracción | V0 (Ollama) / V2 (vLLM) |
| Modelos cloud | Anthropic SDK + OpenAI SDK | Tier 3, fallback, privacy override | V0 (mock) / V1 (real) |
| Code sandbox | Docker | Ejecución aislada de código, sin acceso al host | V0 |
| Automatizaciones | n8n + scripts Python | Flujos SaaS complejos (n8n) + lógica crítica (scripts) | V1 |
| Frontend | Next.js 15 + TypeScript + Tailwind | Dashboard + Mission Control + TV view | V1 |
| Realtime | SSE → WebSockets | Mission feed al browser | V0 (SSE) / V3 (WS) |
| Testing | pytest + vitest + Playwright | Backend / frontend / e2e | V0 |
| Seguridad estática | semgrep + trivy | Code + container scanning en CI | V1 |
| Observabilidad | OpenTelemetry + Grafana + Loki | Logs, traces, métricas | V2 |
| Orquestación durable | Temporal | Long-running missions avanzadas | V3+ (si se necesita) |

---

## Stack V0 — solo lo necesario para que el Mission Kernel corra

```
✅ FastAPI                     — API
✅ PostgreSQL + SQLAlchemy     — Estado de misiones
✅ LangGraph                   — Mission graph
✅ Ollama adapter              — Modelos locales (mock si no hay GPU)
✅ Mock premium adapter        — Claude/GPT simulado en V0
✅ MinIO local                 — Artifacts básicos
✅ Docker sandbox              — Code execution
✅ pytest                      — Tests
❌ Redis                       — Agrega en V1
❌ pgvector                    — Activa en V1 (RAG real)
❌ Next.js dashboard           — Agrega en V1 (V0 = CLI básico)
❌ vLLM                        — Agrega en V2
❌ Observabilidad completa     — Agrega en V2
❌ Temporal                    — Evalúa en V3
```

---

## Estructura de directorios del repositorio

```
oli/
├── apps/
│   ├── api/                    ← FastAPI (routes, auth, session, endpoints)
│   └── worker/                 ← Background mission worker (LangGraph runner)
│
├── packages/
│   ├── mission_kernel/         ← State machine, policy, event emission, validation gates
│   ├── orchestrator/           ← LangGraph nodes: planner, router, repair, human-in-loop
│   ├── executors/              ← Adapters: browser, shell, API, n8n, Docker sandbox
│   ├── model_router/           ← Local/premium selection, tier logic, benchmarking
│   ├── memory/                 ← Memory graph, RAG retrieval, write policies
│   ├── security/               ← Permissions, credential broker, audit log
│   └── validation/             ← Validators, eval runner, evidence capture
│
├── frontend/
│   └── dashboard/              ← Next.js (Mission Control, TV view, approval queue)
│
├── tdd/                        ← Fuente de verdad técnica (este directorio)
├── brand/                      ← Sistema de marca
├── bitacora/                   ← Log de sesiones
└── docker-compose.yml          ← Postgres + Redis + MinIO + Ollama en local
```

---

## Decisiones técnicas clave

| Decisión | Elección | ADR |
|---|---|---|
| Lenguaje backend | Python 3.12 | ADR-005 |
| Framework API | FastAPI | ADR-005 |
| Orquestación de agentes | LangGraph | ADR-010 |
| Framework de agentes (NO elegido) | ~~Mastra~~, ~~CrewAI~~, ~~LangChain~~ | ADR-010 |
| Base de datos | PostgreSQL + pgvector | ADR-010 |
| RAG | pgvector (dentro de Postgres) | ADR-003 |
| Modelos locales | Ollama (V0) → vLLM (V2+) | ADR-016 |
| Model routing | Tier 1 local / Tier 2 mediano / Tier 3 frontier | ADR-016 |
| GPU strategy | On-demand por nosotros, suscripción fija para el usuario | ADR-016 |
| Sandbox de código | Docker | ADR-002 |
| Browser automation | Stagehand v3 + Playwright MCP | ADR-011 |
| Desktop GUI | ClawdCursor MCP | ADR-012 |
| Auth y credenciales | Brokered credentials + OS Keychain | ADR-014 |
| UI nativa | Next.js (web app) + Electron wrapper opcional | ADR-015 |
| Permisos | 5 clases (0-4) | ADR-004 |
| Memoria | 4 capas con RAG desde V0 | ADR-003 |
| Clarificación | Sin límite fijo, inferencia primero | ADR-007 |
| Troubleshooting | Ciclo de diagnóstico real | ADR-006 |

---

## Lo que NO está en el stack y por qué

| Tecnología | Por qué no |
|---|---|
| TypeScript backend | Python es el ecosistema de IA — LangGraph, Ollama, todos son Python-first |
| Mastra | Excelente para TS, pero Oli usa Python — LangGraph tiene más durable execution |
| ChromaDB | Reemplazado por pgvector — una sola DB para todo |
| SQLite | Solo para prototipo individual — Postgres desde V0 |
| **MinIO** | **Archivado en GitHub Feb 2026 (confirmado)** — reemplazado por SeaweedFS (32k stars, Apache 2.0) |
| **Redis** | Licencia comercial 2024 — reemplazado por Valkey (Linux Foundation, drop-in, 8% más rápido) |
| Zapier | Nunca — wrappers de wrappers. n8n o API directa |
| Computer Use API (Anthropic) | Claude-only, viola model-agnostic. ClawdCursor es el reemplazo |
| OpenClaw como dependencia dura | CVEs críticos, inestable. Voz via NativeVoiceAdapter |

---

## Validación state of the art — 2026-05-27

Datos verificados directamente vía GitHub MCP:

| Tecnología | Stars GitHub | Estado | Verificado |
|---|---|---|---|
| pgvector | 21,501 ⭐ | ✅ Activo (updated ayer) | ✓ |
| SeaweedFS | 32,530 ⭐ | ✅ Activo | ✓ |
| RustFS (alternativa a SeaweedFS) | 28,050 ⭐ | ✅ Activo | ✓ |
| QwenLM/Qwen3 | 27,263 ⭐ | ✅ Activo | ✓ |
| **minio/minio** | **61,013 ⭐** | **🔴 archived: true** | ✓ |
| LangGraph | parte de langchain-ai | ✅ v1.0, producción | ✓ |
