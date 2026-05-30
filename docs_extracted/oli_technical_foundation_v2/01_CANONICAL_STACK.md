# 01 - Canonical Stack

## Stack principle

The stack must be optimized for a local-first execution product, not just for one founder's personal machine.

The architecture must support:

- personal local server
- GPU workstation
- hybrid local/premium execution
- team deployments
- future managed/on-prem deployments
- user-selectable model stacks
- security and evidence from day one

## Canonical V0-V2 stack

| Layer | Choice | Role | Notes |
|---|---|---|---|
| OS | Ubuntu Server | Stable base for local/server deployment | Best default for Docker, GPUs, services. |
| Backend API | Python + FastAPI | Main Oli API | Python is strongest for agent tooling and model orchestration. |
| Agent graph | LangGraph | Mission-control graph | Planner, executor routing, validation, repair, memory loop. |
| Durable workflows | Start with Postgres/checkpoints; add Temporal | Long-running missions | Do not overcomplicate V0. Add Temporal when mission recovery requires it. |
| Executor runtime | OpenClaw adapter + internal adapters | Tool-using executor layer | Executor, not product brain. |
| Model serving | Ollama first, vLLM later | Local LLM runtime | Ollama for install simplicity; vLLM for throughput/concurrency. |
| Local models | User-selectable | Main local reasoning/coding/classification | Oli recommends based on hardware and missions. |
| Premium models | Provider abstraction | Hard reasoning / failure recovery | User API keys and policy controls. |
| Database | Postgres + pgvector | Canonical state + semantic retrieval | Missions, memory, events, artifacts, model calls, policies. ChromaDB descartado — pgvector hace el mismo trabajo sin base de datos separada. |
| Cache/events | Valkey | Live mission events | Fork de Redis mantenido por Linux Foundation. MinIO archivado Feb 2026 — no usar. |
| Artifact store | SeaweedFS | Reports, files, logs, builds, audio | MinIO archivado Feb 2026. SeaweedFS es el reemplazo activo S3-compatible. |
| Sandbox | ExecutionEnvironment abstraction (Docker V0-V2, E2B/Modal V3+) | Code execution and validation | Ver ADR-002. Docker para V0-V2; E2B para aislamiento fuerte en V3+. |
| Automation | n8n/scripts/adapters | Repeatable workflows | n8n for SaaS-style flows; scripts for versionable critical logic. |
| Frontend | Next.js + TypeScript + Tailwind | Dashboard and mission control | TV/dashboard + desktop control. |
| Realtime | SSE first, WebSockets later | Mission feed | SSE is enough for V0. |
| Testing | pytest, vitest, playwright | Backend/frontend/e2e validation | Required. |
| Security scanning | semgrep, trivy | Code/container checks | Required in CI. |
| Observability | OpenTelemetry + Grafana + Loki | Logs, traces, metrics | Local and team deployments. |

## V0 stack simplification

V0 should not start with every enterprise component.

Build V0 with:

- FastAPI
- Postgres
- SQLAlchemy/SQLModel + Alembic
- LangGraph
- Valkey optional or minimal (Redis fork — no usar Redis directamente)
- local filesystem o SeaweedFS para artifacts (no MinIO — archivado Feb 2026)
- Docker sandbox (ExecutionEnvironment abstraction — MockExecutor en V0)
- Ollama adapter
- mock premium adapter
- Next.js minimal dashboard
- pytest

Add later:

- Temporal
- vLLM
- advanced credential broker
- multi-user RBAC
- advanced observability
- on-prem installer

## Naming migration

All product-facing references must use Oli.

Legacy mappings:

| Old | New |
|---|---|
| Jarvis OS | Oli Execution OS |
| Jarvis | Oli |
| Jarvis Validator | Oli Validator |
| Jarvis Memory | Oli Memory Graph |
| Jarvis -> OpenClaw | Oli -> Executor Runtime |
| Dashboard TV | Oli Mission Control |

## Backend module boundaries

```text
apps/api
  - FastAPI routes
  - auth/session
  - mission endpoints
  - approval endpoints
  - memory endpoints

packages/mission_kernel
  - mission state machine
  - mission policy
  - event emission
  - validation gates

packages/orchestrator
  - LangGraph nodes
  - planner
  - router
  - repair loop

packages/executors
  - executor protocol
  - OpenClaw adapter
  - Docker sandbox
  - browser/API adapters
  - script/n8n adapters

packages/model_router
  - model registry
  - local clients
  - premium clients
  - routing policy
  - benchmarking

packages/memory
  - memory graph
  - retrieval
  - memory candidates
  - write policies

packages/security
  - permission policy
  - data classification
  - redaction
  - credential broker interfaces
  - audit log

packages/validation
  - validators
  - golden mission runner
  - eval reports
```

## Decision: Temporal

Temporal is valuable for long-running missions, retries, pausing, and recovery.

Do not make Temporal a blocker for V0.

Use this progression:

- V0: mission state in Postgres, workers, explicit retries.
- V2: add durable checkpoints for long missions.
- V3/V4: add Temporal when real mission complexity justifies it.

## Decision: OpenClaw

OpenClaw is allowed as an executor runtime.

Rules:

- OpenClaw is not user-facing.
- OpenClaw cannot write official memory.
- OpenClaw cannot mark missions delivered.
- OpenClaw receives scoped workspace and tool policy.
- OpenClaw returns structured result, artifacts, evidence, errors, and tool calls.

## Decision: model providers

The product must not depend on one provider.

The model router should support:

- local models via Ollama
- local high-throughput serving via vLLM later
- premium provider adapters
- user-supplied API keys
- provider-level privacy rules
- per-mission model policy

## Rule

If a component does not improve mission reliability, security, memory, validation, cost control, or user trust, it is not V0-critical.
