# ADR-021 - Dedicated Oli Runtime and User-Owned Execution Environment

**Estado:** accepted
**Fecha:** 2026-05-31
**Deciders:** Alejandro Pena (founder)

---

## Contexto

El TDD de Oli tenia una tension conceptual:

- Algunos documentos hablaban de `local-first`, GPU workstation, Ollama y ejecucion en la maquina del usuario.
- Otros documentos hablaban de GPU on-demand gestionada por Oli, runtime remoto, sandboxes, API y trabajo en background.
- La vision del founder no es "SaaS generico sin terminal" ni "instala un modelo local y arreglate".

La vision correcta es:

> Cada usuario u organizacion tiene un Oli propio: una instancia operacional dedicada, con memoria persistente, herramientas conectadas, permisos, terminal/sandbox Linux, compute asignado segun tier y modelos open-source/frontier ruteados por mision.

Para el usuario, el producto no es Qwen, Llama, Claude, GPT, vLLM u Ollama.

Para el usuario, el producto es Oli.

---

## Decision

Oli adopta el concepto de **Dedicated Oli Runtime** como arquitectura canonica.

Un Dedicated Oli Runtime es el entorno de ejecucion asignado a un usuario, equipo o tenant. Puede correr en infraestructura administrada por Oli, cloud del cliente, on-prem o modo local avanzado, pero conserva el mismo contrato de producto:

- Oli tiene memoria persistente del usuario/equipo.
- Oli ejecuta misiones en background.
- Oli usa modelos open-source cuando conviene y modelos frontier cuando se justifica.
- Oli tiene acceso a terminal/sandbox Linux bajo permisos.
- Oli conecta herramientas del usuario mediante credential broker.
- Oli captura evidencia, costos, tool calls, model calls y resultados.
- Oli convierte misiones repetidas en playbooks.
- Oli opera como extension del entorno digital del usuario, no como chatbot aislado.

La arquitectura canonica queda:

```text
User / Team
  -> Oli App / API / CLI / Desktop Bridge
  -> Oli Mission API
  -> Mission Kernel
  -> Policy + Permission Engine
  -> Dedicated Oli Runtime
       - tenant/user workspace
       - Postgres + pgvector memory
       - checkpointing and mission state
       - Linux terminal / sandbox
       - browser automation
       - tool connectors
       - credential broker boundary
       - model router
       - open-source model serving
       - premium model adapters
       - artifact store
       - audit log and evidence drawer
  -> Mission report, approvals, artifacts, memory updates
```

---

## Deployment modes

Oli must support multiple deployment modes, but they are not equal in product priority.

### Mode 1 - Oli Managed Dedicated Runtime

Default commercial mode.

- Oli provisions and manages runtime, storage, workers, GPU access and model serving.
- User does not administer infrastructure.
- User perceives a dedicated Oli with assigned compute and memory.
- Work runs in background.
- Best fit for founders, small teams, agencies and non-infrastructure users.

This is the default interpretation of "Oli gives the user their own AI".

### Mode 2 - Customer Cloud / BYOC

For advanced companies.

- Runtime runs in customer cloud/VPC.
- Oli provides control plane, runtime contract, updates and policy layer.
- Customer controls infrastructure boundary.
- Same mission/memory/evidence model.

### Mode 3 - Local / On-Prem / Power User

For technical users, privacy-heavy users and development.

- Runtime may run on a Linux workstation, local GPU server or on-prem machine.
- SSH can be used for setup, administration and power-user operation.
- User may connect local files, repos and tools directly.
- Same permission, memory and evidence rules apply.

This mode is important, but it is not the simplest commercial default.

### Mode 4 - Desktop Bridge

Companion mode, not the core brain.

- Exposes selected local files, browser sessions, OS keychain callbacks or local apps.
- Handles user approvals and local presence.
- Does not bypass Oli permissions.
- Does not give unrestricted filesystem access by default.

---

## SSH and terminal semantics

SSH is allowed, but it must be defined precisely.

SSH can be:

- a setup/admin channel for a user-owned or customer-owned runtime;
- a power-user interface for Linux-native users;
- an operational debugging channel;
- a way to connect Oli to a remote machine the user controls.

SSH is not:

- a permission bypass;
- an uncontrolled root shell for the LLM;
- a replacement for the Mission Kernel;
- a place where secrets are exposed to the model.

All terminal execution must pass through:

```text
Mission Step
  -> Permission Policy
  -> Tool/Terminal Scope
  -> Credential Broker if needed
  -> Execution Environment
  -> Audit Log + Evidence
```

---

## Model serving

The model behind Oli is an implementation detail.

For managed or serious GPU deployments:

- vLLM or equivalent high-throughput OpenAI-compatible serving should be preferred for open-weight models.
- Ollama can remain useful for local development, demos and simple personal deployments.
- The orchestrator should talk to model providers through a model-router abstraction, not directly to a specific runtime.

Recommended interpretation:

| Term | Canonical meaning |
|---|---|
| local model | model running inside the user's dedicated Oli runtime boundary |
| user GPU | compute assigned to the user's tier/runtime, not necessarily physical hardware owned by user |
| Oli model | role selected by Model Router, not a fixed model name |
| open-source model | open-weight model served by Oli runtime |

---

## Memory and context

Oli should not put "everything" into the LLM context.

Oli should build an operational memory system:

1. Index authorized sources.
2. Store documents, missions, decisions, preferences, tool results and artifacts with provenance.
3. Embed semantically useful chunks in pgvector.
4. Store structured facts and mission metadata in Postgres.
5. Retrieve only relevant context per mission.
6. Distinguish personal, company, project, mission and playbook memory.
7. Let the user inspect, edit, delete and export memory.

The principle:

> Oli may know a lot. Each mission should receive only what is relevant, permitted and traceable.

Unrestricted ingestion of "the whole computer" is rejected. It creates privacy, security, cost and memory-contamination risk.

---

## Onboarding curve

The intended user curve is:

```text
Create Oli runtime
  -> connect identity and basic workspace
  -> authorize selected files/repos/tools
  -> index relevant context
  -> run first low-risk missions
  -> show evidence and value
  -> suggest more integrations
  -> detect repeated work
  -> propose playbooks
  -> increase autonomy only with permission
  -> help the user/team become more AI-first
```

Onboarding is not just setup. It is the beginning of Oli's usage expansion loop.

Oli should progressively discover:

- what tools the user uses;
- what work repeats;
- what can be automated safely;
- what requires approval;
- what context should become memory;
- what habits would make the user or team more AI-first.

This will require a future product/constitution decision around responsible farming and onboarding.

---

## Permission boundaries

Oli must not interpret "user-owned runtime" as unlimited access.

Default rules:

1. No filesystem access without an explicit scope.
2. No credential access by the LLM; always use brokered credentials.
3. No external writes without permission class evaluation.
4. No hidden global learning from private content.
5. No silent premium routing in local-only/privacy mode.
6. No permanent memory writes without provenance and user-editability.
7. No tool connector without scope, audit and revocation path.

---

## Alternatives considered

| Option | Pros | Cons | Decision |
|---|---|---|---|
| Pure SaaS API with no dedicated runtime | Simple to explain and operate | Weakens "user-owned Oli", terminal, memory and compute moat | Rejected as full vision |
| Mandatory local GPU/Ollama install | Strong privacy and hacker appeal | Too much setup, not viable for mainstream users | Rejected as default |
| Premium APIs only | Fastest to build | Destroys cost thesis, weakens open-source leverage | Rejected as default |
| Unrestricted local computer access | Powerful | Security/privacy disaster, memory contamination | Rejected |
| Dedicated Oli Runtime | Preserves ownership, compute, memory, tools and product simplicity | More complex infra and permissions | Accepted |

---

## Consecuencias

### For product

- The user should feel they have "their Oli", not a generic chatbot.
- The UI/API should hide model complexity.
- Setup must explain runtime, memory, tools and permissions in human terms.
- The first missions should prove memory + execution + evidence, not just chat quality.

### For infrastructure

- Oli needs clear tenant/runtime boundaries.
- Postgres + pgvector remains core.
- vLLM or equivalent serving becomes more important than Ollama for serious runtime.
- Runtime provisioning, scheduling and cost accounting become product-critical.

### For security

- Tool scopes and credential broker are non-negotiable.
- SSH/terminal must be controlled by Mission Kernel and audit log.
- Memory ingestion must be permissioned and reversible.

### For business

- "Oli-managed compute" remains part of the moat.
- Pricing must account for GPU minutes, storage, embeddings, tool calls and premium API escapes.
- The switching cost is accumulated memory, playbooks, validated workflows and runtime integration.

---

## Required follow-up changes

This ADR supersedes ambiguous language in older documents that imply Ollama/local laptop is the default product architecture.

Documents to update later:

- `tdd/README.md`
- `tdd/stack/stack-decision.md`
- `tdd/domain/setup-wizard-spec.md`
- `tdd/adrs/ADR-016-model-routing-gpu-strategy.md`
- `tdd/adrs/ADR-012-desktop-execution-strategy.md`
- `docs_extracted/oli_technical_foundation_v2/01_CANONICAL_STACK.md`
- `docs_extracted/oli_technical_foundation_v2/02_LOCAL_FIRST_PRODUCT_ARCHITECTURE.md`

Acceptance criterion:

> A reader should understand that Oli can run local/on-prem, but the product promise is a dedicated Oli runtime per user/team with memory, tools, compute and permissions. The model is behind Oli. The user talks to Oli.

