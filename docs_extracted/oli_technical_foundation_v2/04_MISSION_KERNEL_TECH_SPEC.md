# 04 - Mission Kernel Technical Spec

## Purpose

The Mission Kernel is the core abstraction of Oli.

Everything begins as a mission.

A mission is not a chat message. It is a structured unit of work with objective, context, plan, permissions, tasks, execution, validation, evidence, artifacts, memory updates, and final report.

## Mission lifecycle

```text
created
  -> intake_normalized
  -> context_retrieved
  -> classified
  -> planned
  -> awaiting_approval? 
  -> executing
  -> validating
  -> repairing? 
  -> delivering
  -> delivered / partially_delivered / failed
  -> memory_reviewed
  -> archived
```

## Mission object

```json
{
  "id": "mission_001",
  "organization_id": "org_001",
  "user_id": "user_001",
  "title": "Prepare outbound campaign draft",
  "raw_intent": "Oli, find the best 50 leads from this CSV and prepare personalized emails.",
  "normalized_objective": "Rank leads, select top 50, generate personalized draft emails, and prepare approval packet.",
  "mission_class": "sales_ops_campaign_preparation",
  "status": "planned",
  "risk_class": 3,
  "privacy_level": "internal",
  "approval_required": true,
  "model_policy_id": "mp_001",
  "tool_policy_id": "tp_001",
  "expected_outputs": [
    "ranked_leads.csv",
    "email_drafts.md",
    "approval_summary.md"
  ],
  "validators": [
    "artifact_exists",
    "schema_valid",
    "no_external_send_without_approval"
  ],
  "cost_budget_usd": 5.0,
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

## Mission invariants

- A mission must have one canonical owner.
- Every state transition emits a `mission_event`.
- Every external action must be linked to a permission policy decision.
- Every artifact must have provenance.
- Every model call must be logged.
- Every tool call must be logged.
- Executors cannot mark missions delivered.
- Executors cannot write official memory.
- Final delivery is produced by Oli after validation.
- Partial delivery must be explicitly labeled as partial.

## Task object

```json
{
  "id": "task_001",
  "mission_id": "mission_001",
  "title": "Validate CSV and rank leads",
  "objective": "Clean lead CSV, validate email formats, score leads based on criteria.",
  "status": "executing",
  "executor": "docker_sandbox|openclaw|script|browser|api|model",
  "risk_class": 1,
  "attempt": 1,
  "max_attempts": 3,
  "input_artifacts": [],
  "output_artifacts": [],
  "validators": ["csv_schema_valid", "email_format_valid"],
  "created_at": "timestamp"
}
```

## Event object

```json
{
  "id": "event_001",
  "mission_id": "mission_001",
  "task_id": "task_001",
  "event_type": "task_started",
  "actor": "oli|executor|user|validator|system",
  "summary": "Started lead validation in Docker sandbox.",
  "data": {},
  "created_at": "timestamp"
}
```

## Approval object

```json
{
  "id": "approval_001",
  "mission_id": "mission_001",
  "requested_action": "Create 50 Gmail drafts using connected Gmail account.",
  "risk_class": 3,
  "reason": "External side effect in user's email account.",
  "preview_artifact_id": "artifact_email_preview",
  "options": ["approve", "edit", "reject"],
  "status": "pending",
  "expires_at": null
}
```

## Validation report

```json
{
  "id": "validation_001",
  "mission_id": "mission_001",
  "task_id": "task_001",
  "validator": "artifact_exists",
  "status": "passed|failed|warning",
  "summary": "All expected artifacts exist.",
  "evidence": {},
  "created_at": "timestamp"
}
```

## Output contract

A final mission report should include:

- status
- result
- artifacts
- evidence summary
- validations
- decisions made
- approvals needed
- cost/time summary when relevant
- risks or limitations
- memory updates proposed or committed
- next recommended action

Bad:

```text
Done.
```

Good:

```text
Mission completed.

Result:
- Ranked 312 leads.
- Selected top 50 based on company size, role match, and recent buying signals.
- Generated 50 personalized email drafts.

Validation:
- CSV schema passed.
- 48/50 emails passed format checks.
- 2 leads flagged for manual review.

Approval needed:
- I prepared drafts only. I did not send anything.

Artifacts:
- ranked_leads.csv
- email_drafts.md
- approval_summary.md
```

## Suboperator Integration in Mission Kernel

The Mission Kernel is responsible for:

1. **Spawning suboperators** — based on mission type, complexity, and available tools.
2. **Scope isolation** — each suboperator receives only the context relevant to its task; not full user memory.
3. **Output aggregation** — collecting structured outputs from all suboperators assigned to a mission.
4. **Synthesis routing** — passing aggregated outputs to Oli for final synthesis and delivery.
5. **Memory gate** — all memory write decisions go through Oli, never directly from suboperators.

### Suboperator Lifecycle

```
Mission starts
  -> Kernel classifies mission complexity
  -> If simple: Oli handles directly
  -> If complex: Kernel spawns required suboperators with scoped context
  -> Suboperators execute in parallel where safe
  -> Outputs collected
  -> ValidationSuboperator runs (if configured)
  -> Kernel passes all outputs to Oli
  -> Oli synthesizes
  -> If human approval needed: Oli presents summary and waits
  -> Oli delivers final answer
  -> MemoryCuratorSuboperator suggests what to store
  -> Oli reviews and approves memory writes
  -> Mission closed
```

### Mission Classification Rules

| Mission type | Suboperators typically assigned |
|---|---|
| Market research | MarketResearchSuboperator, ValidationSuboperator |
| Architecture decision | TechnicalArchitectSuboperator, SecurityReviewerSuboperator, ValidationSuboperator |
| Product build | ExecutionSuboperator, TechnicalArchitectSuboperator, UXCriticSuboperator, ValidationSuboperator |
| Security audit | SecurityReviewerSuboperator, ValidationSuboperator |
| Growth campaign | GrowthSuboperator, UXCriticSuboperator, ValidationSuboperator |
| Memory cleanup | MemoryCuratorSuboperator |
| Simple task | None (Oli handles directly) |

---

## V0 build target

Implement:

- mission schema
- task schema
- state machine
- mission events
- approval object
- artifact object
- validation report object
- basic validators
- API endpoints
- tests for state transitions
