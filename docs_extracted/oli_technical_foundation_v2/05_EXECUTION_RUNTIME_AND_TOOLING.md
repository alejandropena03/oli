# 05 - Execution Runtime and Tooling

## Purpose

Oli must be the brain, supervisor, memory owner, policy owner, validator, and final voice.

Executors are hands.

Executors can be powerful, but they must remain bounded.

## Oli como supervisor/orquestador — no como agente más

Oli no es un agente que compite con Claude Code, Codex o Browser Use.
Oli es el supervisor que los coordina, les delega trabajo, captura su evidencia y mantiene la memoria entre ellos.

```
Oli (supervisor)
  ├── Claude Code        → coding, repo work, specs (delegado como herramienta)
  ├── Codex              → code completion, inline fixes (delegado como herramienta)
  ├── Browser Use        → browser tasks autónomas completas
  ├── Stagehand          → browser steps dentro de misiones
  ├── ExecutionEnvironment → código, scripts, CLI (Docker V0-V2, E2B V3+)
  ├── Local model        → intent, classification, memory, formatting
  ├── Premium API        → hard reasoning, recovery, high-stakes output
  └── Human approval     → permission gates, escalación
```

Cada agente externo retorna resultados estructurados. Oli decide qué entra en memoria, qué es evidencia, y qué entrega al usuario. **El usuario nunca habla directamente con Claude Code ni con Codex — habla con Oli.**

## Executor types

| Executor | Role |
|---|---|
| ExecutionEnvironment | Code execution, tests, validation, data scripts. Abstracción sobre Docker (V0-V2) y E2B/Modal (V3+). Ver ADR-002. |
| Claude Code adapter | Coding missions, repo work, spec generation. Oli delega y captura evidencia. |
| Codex adapter | Code completion, inline fixes. Oli delega y captura evidencia. |
| Browser Use adapter | Browser tasks autónomas completas. Python-native, compatible con stack. |
| Stagehand/Playwright adapter | Browser steps dentro de misiones. CDP-native, híbrido AI+determinístico. |
| n8n/script adapter | Repeatable workflows and automation. |
| Local model adapter | Direct local LLM tasks via Ollama/vLLM. |
| Premium model adapter | Hard reasoning, synthesis, fallback via provider API. |
| OS agent adapter (V3+) | Controlled computer actions via ClawdCursor o Computer Use API. |

## Boundary rule

Executors return structured results.

Oli decides whether those results are acceptable.

Executors cannot:

- speak directly to user
- mark mission delivered
- write official memory
- bypass permission policy
- access credentials outside scope
- access filesystem outside workspace
- send external communications without approval

## Executor request

```json
{
  "mission_id": "mission_001",
  "task_id": "task_001",
  "objective": "Generate Python script and tests.",
  "workspace": "/workspaces/mission_001/task_001",
  "inputs": [
    {"artifact_id": "artifact_input_csv", "path": "leads.csv"}
  ],
  "model_policy": {
    "local_first": true,
    "allowed_models": ["user_main_local", "user_fast_local"],
    "allow_premium": false,
    "max_cost_usd": 0.0
  },
  "tool_policy": {
    "filesystem_scope": "workspace_only",
    "allow_shell": true,
    "shell_scope": "sandbox_only",
    "allow_network": false,
    "allow_external_actions": false,
    "allow_delete": false
  },
  "expected_outputs": ["main.py", "tests/test_main.py", "README.md"],
  "timeout_seconds": 600
}
```

## Executor result

```json
{
  "mission_id": "mission_001",
  "task_id": "task_001",
  "status": "succeeded|failed|partial",
  "summary": "Created script and tests.",
  "artifacts": [
    {"path": "main.py", "type": "code", "sha256": "..."}
  ],
  "tool_calls": [],
  "model_calls": [],
  "evidence": [],
  "errors": [],
  "recommendations": []
}
```

## Docker sandbox requirements

Default:

- no host filesystem access
- workspace mount only
- no Docker socket
- no privileged containers
- no network unless policy allows
- CPU/memory/time limits
- ephemeral containers
- read-only base image where possible
- capture stdout/stderr
- store logs as artifacts

## SSH role

SSH is permitted as an installation/admin/maintenance channel, especially for the founder's Linux server.

Do not expose raw SSH as normal mission execution until the policy layer is mature.

When OS-level execution is later added:

- every command must be tied to mission/task/policy
- dry-run when possible
- workspace-only by default
- no destructive commands without approval
- full audit log

## Browser/API execution

Browser/API tools should be treated as higher risk than local file operations because they can create external side effects.

Policy must distinguish:

- external read
- external draft creation
- external send/commit/publish/deploy
- irreversible action

## n8n/scripts

Use n8n for:

- repeatable SaaS workflows
- low-code integrations
- internal automation prototypes

Use versioned scripts for:

- critical transformations
- testable business logic
- data validation
- code generation workflows

## OpenClaw adapter

OpenClaw can be integrated as a general executor.

Adapter responsibilities:

- convert Oli task to OpenClaw-compatible request
- inject only scoped tools and workspace
- pass model policy
- capture all outputs
- normalize result
- return structured evidence
- never expose OpenClaw directly to user

## V0 build target

Implement:

- `ExecutionEnvironment` protocol (ver ADR-002 para contrato completo)
- `MockExecutionEnvironment`
- `DockerSandboxEnvironment` minimal
- `ClaudeCodeAdapter` stub (recibe task, retorna ExecutionResult estructurado)
- executor request/result schemas
- tool policy enforcement at adapter boundary
- executor call logging con `ToolCallAuditRecord` (ver ADR-020)
- tests

## Trust Firewall

Antes de ejecutar cualquier herramienta, Oli muestra al usuario (cuando el risk_class lo requiere):
- Qué dato sale del contexto del usuario
- Qué modelo se usará
- Qué herramienta se invocará
- Qué permiso requiere
- Qué queda local vs qué va a una API externa

Esto no es UX decorativa. Es el mecanismo que hace que el usuario confíe en Oli con trabajo de mayor valor.
