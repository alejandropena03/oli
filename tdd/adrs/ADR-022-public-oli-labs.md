# ADR-022 - Public Oli Labs and Private Core Boundary

**Estado:** accepted
**Fecha:** 2026-05-31
**Deciders:** Alejandro Pena (founder)

---

## Contexto

Oli es un producto comercial con arquitectura, playbooks, routing, memory system y solution bank que pueden ser copiables si se publica el codigo completo.

Al mismo tiempo, Alejandro quiere que Oli funcione tambien como prueba publica de capacidad para roles de AI engineering, LLM systems, agent engineering, automation, model serving y post-training.

La pregunta es:

> Como mostrar excelencia tecnica sin regalar el producto?

---

## Decision

Oli separa formalmente:

1. **Private Oli Core**: producto comercial y moat.
2. **Public Oli Labs**: laboratorios publicos, reproducibles y sanitizados que demuestran habilidades tecnicas.

El core comercial permanece privado.

La capa publica se crea para:

- demostrar habilidades de AI engineering;
- atraer talento, usuarios tecnicos e inversion;
- generar credibilidad profesional;
- documentar decisiones tecnicas;
- permitir demos sin datos reales;
- mostrar rigor en evals, runtime, memory, security y fine-tuning.

---

## Public repository strategy

Se recomiendan repos publicos separados, no un mirror parcial caotico del core.

```text
oli-agent-evals
  - toy mission environments
  - golden datasets
  - graders
  - benchmark runner
  - eval reports

oli-runtime-lab
  - vLLM/OpenAI-compatible adapter demo
  - model router toy registry
  - latency/cost benchmarks
  - serving notes

oli-memory-lab
  - Postgres + pgvector demo
  - provenance-aware memory entries
  - retrieval reports
  - synthetic data only

oli-tool-security-lab
  - tool scopes
  - taint tracking fixtures
  - prompt injection tests
  - audit record demo

oli-posttraining-lab
  - synthetic dataset generation
  - SFT/LoRA experiments
  - eval before/after
  - failure analysis
```

These repos may later be grouped under an `oli-labs` GitHub organization or monorepo.

---

## What can be public

Allowed:

- architecture overviews;
- sanitized ADRs;
- generic schemas;
- toy mission classes;
- synthetic data;
- redacted traces;
- eval harnesses;
- model serving demos;
- fine-tuning notebooks;
- benchmark reports;
- blog/case-study markdown;
- screenshots and videos;
- small reusable libraries that do not expose moat.

---

## What must remain private

Not allowed by default:

- full Mission Kernel implementation if it becomes product moat;
- production orchestrator logic;
- commercial playbooks;
- solution bank;
- real user/company memory;
- customer traces;
- proprietary prompts;
- model routing heuristics tied to unit economics;
- pricing sensitivity models;
- credential broker production code;
- full tool connector implementations;
- deployment secrets or infra configs.

---

## Public/private interface

Public labs should use simplified contracts compatible with Oli concepts but not identical to production internals.

Example:

```text
Production MissionBlackBox
  -> full internal schema, private

Public TraceRecord
  -> reduced schema:
     mission_id
     task_type
     steps
     model_calls_summary
     tool_calls_summary
     validation_result
     cost_summary
     synthetic_artifacts
```

The public schema must be truthful enough to prove skill and abstract enough to protect the business.

---

## Why not publish the full product?

Publishing the full product too early creates avoidable risk:

- competitors can copy architecture and playbooks;
- prompts and routing logic can be cloned;
- user trust/security code can be misused if incomplete;
- the project becomes harder to commercialize;
- the repo may look unfinished if opened before product quality is ready.

The right signal is not "everything is open".

The right signal is:

> The commercial product is private, but the engineering claims are backed by public, reproducible labs.

---

## Consequences

### Positive

- Alejandro can show serious AI systems work publicly.
- Oli can keep commercial advantage private.
- Public repos become hiring/investor artifacts.
- Labs can be cited in interviews, portfolio, posts and demos.
- The discipline of public evals improves private Oli.

### Negative

- Requires maintaining public examples separately.
- Public code must avoid accidental leakage.
- Synthetic demos must be strong enough not to look fake.
- More documentation burden.

---

## Acceptance criteria

The public layer is successful when:

1. A hiring manager can understand Alejandro's AI engineering level in under 10 minutes.
2. A technical interviewer can run at least one lab locally.
3. The labs show evals, traces, model routing, memory or fine-tuning with measurable outputs.
4. No customer data, proprietary playbooks or private routing economics are exposed.
5. The public narrative points back to Oli without revealing Oli Core.

---

## References

- `tdd/domain/ai-engineering-skill-signal.md`
- `tdd/adrs/ADR-021-dedicated-oli-runtime.md`

