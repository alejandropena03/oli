# Oli Technical Foundation v2

Status: technical companion pack for `OLI_MASTER_SPEC.md`  
Canonical product/company name: **Oli**  
Canonical promise: **De intención a trabajo terminado**  
Canonical architecture: **Personal Execution Operator + Local-First Execution OS**  
Legacy name: Jarvis OS. Treat all Jarvis references as Oli.

## Why this v2 exists

The original master spec defines what Oli is as a product and company. The old Jarvis technical stack defined a strong personal/local setup. This v2 turns both into a buildable, productized technical foundation.

The key change:

> Oli is not a fixed SaaS that forces one model or one cloud. Oli is a local-first execution system where each user can choose their model stack, privacy mode, compute setup, and premium fallback policy. Oli guides the setup, benchmarks the options, recommends the best profile, and keeps the execution experience simple.

## Core decisions

- Oli is the user-facing operator.
- The Execution OS is the system behind Oli.
- The user may run Oli on a local Linux server, GPU workstation, cloud VM, or hybrid setup.
- The user chooses which models to use.
- Oli recommends and installs models based on hardware, mission types, privacy preferences, and budget.
- Oli owns mission state, memory, permissions, validation, evidence, and final response.
- Executors, local models, premium models, browsers, scripts, Docker containers, and workflow tools are replaceable components.
- Security, privacy, auditability, and permissioned autonomy are product primitives, not enterprise add-ons.

## Document map

| File | Purpose |
|---|---|
| `00_TECHNICAL_THESIS.md` | Direct thesis: why Oli can be more than a generic agent. |
| `01_CANONICAL_STACK.md` | Productized version of the Jarvis stack, now Oli. |
| `02_LOCAL_FIRST_PRODUCT_ARCHITECTURE.md` | How personal, hybrid, team, and future enterprise deployments work. |
| `03_SETUP_WIZARD_AND_MODEL_SELECTION.md` | How Oli guides each user into the right local/premium model stack. |
| `04_MISSION_KERNEL_TECH_SPEC.md` | Mission object, state machine, invariants, events, validators. |
| `05_EXECUTION_RUNTIME_AND_TOOLING.md` | OpenClaw/executor boundary, Docker sandbox, SSH role, tools. |
| `06_SECURITY_PRIVACY_AND_DATA_PROTECTION.md` | Security model, threat model, privacy modes, credential isolation. |
| `07_MEMORY_PERSONALIZATION_SELF_IMPROVEMENT.md` | Memory graph, personalization, self-improvement loops. |
| `08_VALIDATION_EVALS_OBSERVABILITY.md` | Golden missions, evals, validation, telemetry, reliability metrics. |
| `09_DATA_MODEL_AND_SCHEMAS.md` | Initial database entities and TypeScript/Python schema direction. |
| `10_ICP_MOAT_AND_BUSINESS_MODEL.md` | Founder + small company wedge, moat, pricing hypotheses. |
| `11_ROADMAP_V0_TO_V5.md` | Private build sequence up to serious release candidate. |
| `12_CLAUDE_CODE_PROMPTS.md` | Ready-to-paste implementation prompts for Claude Code. |
| `13_DIAGRAMS.md` | Mermaid diagrams for architecture, setup, routing, security, memory. |
| `CLAUDE_CODE_START_HERE.md` | Short command file for Claude Code to begin correctly. |

## How to use with Claude Code

1. Keep `OLI_MASTER_SPEC.md` as the product constitution.
2. Put this folder under `docs/technical/`.
3. Start Claude Code with `CLAUDE_CODE_START_HERE.md`.
4. Build V0 Mission Kernel before dashboard polish.
5. Build model routing as a policy layer, not as a hardcoded provider choice.
6. Build security, permissions, and evidence from the beginning.

## Non-negotiables

- No chatbot-first implementation.
- No fake Core Orb or fake mission progress.
- No executor can directly write official memory.
- No executor can deliver directly to the user.
- No mission can be marked delivered unless validators pass or Oli explicitly reports partial failure.
- No hardcoded model dependency.
- No hardcoded cloud dependency.
- No silent premium model calls with sensitive data.
- No broad credentials passed into untrusted execution environments.
- No promise of absolute security. The product promise is maximum practical user control, strong isolation, explicit policy, and auditability.
