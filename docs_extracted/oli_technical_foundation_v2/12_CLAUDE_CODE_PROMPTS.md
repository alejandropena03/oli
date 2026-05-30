# 12 - Claude Code Prompts

## Prompt 0 - Start correctly

```text
You are building Oli, not Jarvis.

Read first:
- docs/OLI_MASTER_SPEC.md
- docs/technical/README.md
- docs/technical/00_TECHNICAL_THESIS.md
- docs/technical/01_CANONICAL_STACK.md
- docs/technical/04_MISSION_KERNEL_TECH_SPEC.md
- docs/technical/06_SECURITY_PRIVACY_AND_DATA_PROTECTION.md

Your task is to create an implementation plan for V0 Mission Kernel Foundation.

Do not build a chatbot.
Do not build decorative UI first.
Do not hardcode one model provider.
Do not let executors write memory or deliver to the user.
Do not claim mission completion without validation.

Output:
- proposed monorepo tree
- backend modules
- database tables
- API endpoints
- mission state machine plan
- validation plan
- security gates for V0
- exact first coding tasks
```

## Prompt 1 - Repo bootstrap

```text
Bootstrap the Oli monorepo for V0.

Use:
- Python FastAPI backend
- Postgres
- Alembic migrations
- Pydantic models
- pytest
- Next.js TypeScript frontend skeleton

Create:
- apps/api
- apps/dashboard
- packages/mission_kernel
- packages/orchestrator
- packages/executors
- packages/model_router
- packages/memory
- packages/security
- packages/validation
- docker-compose.yml for local development

Rules:
- Product name is Oli everywhere.
- No Jarvis names except in migration notes.
- Add healthcheck endpoint.
- Add test command.
```

## Prompt 2 - Mission database and state machine

```text
Implement the V0 Mission Kernel database and state machine.

Read docs/technical/04_MISSION_KERNEL_TECH_SPEC.md and docs/technical/09_DATA_MODEL_AND_SCHEMAS.md.

Implement:
- missions
- mission_tasks
- mission_events
- artifacts
- approvals
- validation_reports
- audit_logs

Implement mission statuses:
created, intake_normalized, context_retrieved, classified, planned, awaiting_approval, executing, validating, repairing, delivering, delivered, partially_delivered, failed, cancelled, memory_reviewed, archived.

Rules:
- Every transition emits mission_event.
- Invalid transitions raise typed error.
- Cannot deliver without validation pass or explicit partial delivery.
- Approval-required missions cannot execute before approval.

Add tests.
```

## Prompt 3 - Executor adapter and sandbox

```text
Implement executor adapter interfaces for Oli.

Read docs/technical/05_EXECUTION_RUNTIME_AND_TOOLING.md.

Implement:
- ExecutorAdapter protocol
- ExecutorRequest schema
- ExecutorResult schema
- MockExecutorAdapter
- DockerSandboxExecutor minimal implementation or stub with testable boundary
- executor call logging

Rules:
- Executors cannot mark mission delivered.
- Executors cannot write official memory.
- Executors receive scoped workspace and tool policy.
- No network in sandbox by default.
- No host filesystem access beyond workspace.

Add tests.
```

## Prompt 4 - Model routing V0

```text
Implement Oli Model Router V0.

Read docs/technical/03_SETUP_WIZARD_AND_MODEL_SELECTION.md.

Implement:
- ModelRegistry schema
- ModelProfile schema
- ModelPolicy schema
- ModelRouter class
- LocalModelClient interface
- Ollama client stub/implementation
- PremiumModelClient interface stub
- route simulation endpoint
- model_calls table usage

Rules:
- Do not hardcode one model.
- User can select model profile.
- Default is local-first.
- Premium calls require policy allowance.
- Sensitive data cannot route to premium in Local Only mode.

Add tests for routing decisions.
```

## Prompt 5 - Security V0

```text
Implement Oli Security V0.

Read docs/technical/06_SECURITY_PRIVACY_AND_DATA_PROTECTION.md.

Implement:
- RiskClass enum 0-5
- Sensitivity enum
- PrivacyMode enum
- PermissionPolicy schema
- policy decision function
- approval requirement function
- audit log write helper
- redaction helper stub

Rules:
- Class 4 and 5 always require approval.
- Local Only privacy mode blocks premium model calls.
- Secret sensitivity is never sent to models.
- Every external side effect requires policy decision.

Add tests.
```

## Prompt 6 - Memory V0/V1

```text
Implement Oli Memory V0.

Read docs/technical/07_MEMORY_PERSONALIZATION_SELF_IMPROVEMENT.md.

Implement:
- memory_items table
- explicit memory write endpoint
- memory search endpoint
- memory retrieval function for mission planning
- memory candidate object after mission completion

Rules:
- Memory must have source, confidence, and sensitivity.
- Inferred memory cannot be high confidence by default.
- Executors cannot write memory directly.
- User can archive/delete memory.

Add tests.
```

## Prompt 7 - Validation and golden missions

```text
Implement validation and golden mission runner.

Read docs/technical/08_VALIDATION_EVALS_OBSERVABILITY.md.

Implement validators:
- artifact_exists
- output_contract_markdown
- no_external_side_effects
- local_only_model_policy
- prompt_injection_untrusted_content

Implement golden mission YAML format and runner.

Add initial golden missions:
1. spec generation
2. external email requires approval
3. prompt injection document is ignored as instruction
4. local-only confidential summary does not call premium
5. failed code test triggers repair
```

## Prompt 8 - Setup wizard V1 skeleton

```text
Build the setup wizard skeleton.

Read docs/technical/03_SETUP_WIZARD_AND_MODEL_SELECTION.md.

Backend:
- endpoints for hardware scan placeholder
- model registry
- model setup plan
- model install plan
- route simulation

Frontend:
- deployment profile selection
- privacy mode selection
- mission profile selection
- budget policy selection
- recommended setup summary

Rules:
- User remains free to choose models.
- Oli recommendation explains tradeoffs.
- No heavy model install without approval.
```

## Prompt 9 - Dashboard V0

```text
Build minimal Oli dashboard.

Screens:
- command input
- mission list
- selected mission detail
- mission feed from real mission_events
- approval queue
- artifacts list
- validation status
- model routing summary

Rules:
- No fake Orb states.
- UI states must be backed by backend mission status/events.
- Use Oli naming only.
```

## Prompt 10 - Jarvis rename guard

```text
Add a repo check that fails if forbidden Jarvis naming appears in source paths, UI strings, API names, or product docs.

Allowed:
- historical migration docs
- comments explicitly explaining legacy rename

Forbidden:
- user-facing product copy
- API route names
- class names
- package names
- dashboard labels
```
