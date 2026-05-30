# Decision Memo for Founder

## My position

Keep **Oli**.

Do not rename to Forge, Jarvis, Axion, or anything else right now.

The brand decision is settled enough to build: Oli is the operator; the Execution OS is the system behind it.

## The critique from Claude/Elon

It is directionally correct if Oli is a generic cloud AI agent.

It is incomplete because it underweights your strongest angle:

> user-owned local/hybrid execution + model freedom + secure orchestration + memory + validation.

That does not automatically create a moat, but it gives Oli a much better wedge than "chatbot with dashboard."

## The ICP decision

Both are valid:

1. Founders/operators/small teams are best for V1-V3 product shaping.
2. Operations teams in 50-500 person companies are likely stronger later monetization.

Do not choose one forever. Stage them.

## The technical decision

The Jarvis stack is a good founder/power-user stack:

- Ubuntu Server
- FastAPI
- LangGraph
- OpenClaw/executors
- local models via Ollama/vLLM
- Postgres + pgvector
- Redis
- MinIO
- Docker sandbox
- n8n/scripts
- Next.js dashboard
- testing/security/observability

But as a product, it must become configurable:

- user chooses models
- Oli recommends profiles
- Oli benchmarks hardware
- Oli handles installation where allowed
- privacy mode controls routing
- premium fallback is optional and policy-bound

## The security decision

Security must be elevated to core product identity.

Not "enterprise feature later."

Oli should be known for:

- local-first privacy
- model transparency
- permissioned autonomy
- strong sandboxing
- auditability
- memory visibility
- user data control

## What to build next

Build the technical foundation in this order:

1. Mission Kernel.
2. Security/permissions/audit.
3. Validation/evidence.
4. Model profile/router.
5. Memory.
6. Executor adapter.
7. Setup wizard.
8. Dashboard.

The dashboard should visualize truth, not simulate intelligence.
