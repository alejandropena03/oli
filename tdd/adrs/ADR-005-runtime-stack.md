# ADR-005 — Runtime y stack canónico

**Estado:** accepted
**Fecha:** 2026-05-26
**Fuente:** 01_CANONICAL_STACK.md (documento fundacional del proyecto)
**Decisión:** Python + FastAPI + LangGraph

---

## Contexto

El stack define el lenguaje, el framework de orquestación de agentes, la base de datos,
el servidor, el runtime de modelos locales y el frontend. Esta decisión afecta absolutamente
todo lo que viene después — no se cambia sin una razón muy sólida.

---

## Decisión: Python + LangGraph + FastAPI

### Por qué Python (no TypeScript)

Python es el lenguaje correcto para un sistema de agentes de IA en 2026:

- Ecosistema ML/AI más maduro: LangGraph, LangChain, Ollama, vLLM, transformers, chromadb — todos son Python-first
- LangGraph (el framework de orquestación elegido) es Python-native
- Ollama SDK, vLLM, PyTorch, HuggingFace — todos Python
- La comunidad de agentes de IA construye en Python
- FastAPI es el estándar de producción para APIs Python en 2026

TypeScript tiene mejor DX para frontends — por eso el dashboard usa Next.js.
El backend usa Python porque es donde vive el ecosistema de IA.

### Por qué LangGraph (no Mastra, no LangChain, no CrewAI)

LangGraph es el framework correcto para Oli porque Oli tiene misiones complejas y largas:

| Característica | LangGraph | Mastra | CrewAI |
|---|---|---|---|
| Checkpointing (resume tras crash) | ✅ Nativo | ❌ | ❌ |
| Human-in-the-loop interrupts | ✅ Diseñado para esto | ⚠️ Manual | ⚠️ |
| Workflows no-lineales complejos | ✅ Graph-based | ⚠️ | ⚠️ |
| Estado persistente entre pasos | ✅ Durable | ⚠️ | ❌ |
| Observabilidad producción (LangSmith) | ✅ Node-by-node | ⚠️ | ⚠️ |
| Misiones de horas de duración | ✅ | ❌ | ❌ |
| Python-native | ✅ | ❌ (TS) | ✅ |

Mastra es mejor si el stack fuera TypeScript. Pero el stack es Python.
CrewAI no tiene durable execution — una misión larga que se interrumpe se pierde.
LangGraph fue diseñado exactamente para el problema de Oli: misiones con estado, aprobaciones humanas, reparación de fallos, y checkpoints.

### El stack completo

```
OS:             Ubuntu Server 24.04 LTS
Backend:        Python 3.12 + FastAPI
Orquestación:   LangGraph (mission graph, state, checkpoints)
DB:             PostgreSQL 16 + pgvector (estado + memoria semántica)
Cache/eventos:  Valkey (fork open source de Redis, Linux Foundation — 8% más rápido, 20% menos RAM)
Artifacts:      SeaweedFS (MinIO archivado Feb 2026 — SeaweedFS: 32k stars, Apache 2.0, S3-compatible)
Modelos local:  Ollama (V0-V1, macOS/dev) → LocalAI abstraction → vLLM o SGLang (V2+, producción)
Sandbox código: Docker (ejecución aislada, sin acceso al host por defecto)
Automatización: n8n (flujos SaaS complejos) + scripts Python (lógica crítica)
Frontend:       Next.js 15 + TypeScript + Tailwind (dashboard, mission control)
Realtime:       Server-Sent Events (SSE) en V0 → WebSockets en V3+
Testing:        pytest (backend) + vitest (frontend) + Playwright (e2e)
Seguridad:      semgrep + trivy (CI/CD)
Observabilidad: OpenTelemetry + Grafana + Loki (logs, traces, métricas)
```

---

## V0 — Stack simplificado (solo lo necesario)

```
FastAPI                     ← API principal
PostgreSQL + SQLAlchemy     ← Estado de misiones
LangGraph                   ← Orquestación de misiones
Ollama adapter              ← Modelos locales (mock si no hay GPU)
Mock premium adapter        ← Claude/GPT (solo cuando se necesita)
MinIO local                 ← Artifacts básicos
Docker sandbox              ← Code execution aislado
Next.js minimal             ← Dashboard básico
pytest                      ← Tests
```

Excluidos en V0 (se agregan después):
- Redis (se agrega en V1 cuando el dashboard necesita realtime)
- pgvector (se activa en V1 cuando hay RAG real)
- vLLM (se agrega en V2 cuando hay concurrencia real)
- Temporal (se evalúa en V3 si LangGraph checkpoints no son suficientes)
- Observabilidad completa (Grafana, Loki) → V2+

---

## Estructura de módulos Python

```
apps/
  api/                    ← FastAPI routes, auth, session
  worker/                 ← Background mission worker

packages/
  mission_kernel/         ← State machine, policy, event emission
  orchestrator/           ← LangGraph nodes, planner, router, repair
  executors/              ← Tool adapters (browser, shell, API, n8n)
  model_router/           ← Local/premium model selection logic
  memory/                 ← Memory graph, retrieval, write policies
  security/               ← Permissions, credential broker, audit
  validation/             ← Validators, eval runner, evidence

frontend/
  dashboard/              ← Next.js (mission control, TV view)
```

---

## Consecuencias

- El backend es Python — el founder necesita saber o aprender Python para trabajar en el core
- LangGraph tiene una curva de aprendizaje más alta que Mastra, pero es más robusto para producción
- Postgres + pgvector es una sola base de datos para todo — estado estructurado Y semántico
- Docker sandbox desde V0 — la ejecución de código nunca toca el host directamente
- La simplicidad de V0 es intencional — cada componente se agrega solo cuando agrega valor real
