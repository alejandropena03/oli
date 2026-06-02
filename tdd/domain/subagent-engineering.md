# Subagent Engineering

**Estado:** canonical domain spec
**Fecha:** 2026-05-31
**ADR:** `tdd/adrs/ADR-023-subagent-engineering-contracts.md`

---

## Veredicto

Oli does not use multi-agent by default.

Oli uses contractual subagent engineering: subagents exist only when a mission class needs specialization, context isolation, parallelism, independent validation, risk separation, or measurable cost/latency improvement.

The unit of design is not "agent". The unit of design is:

```text
MissionClass -> TopologyDecision -> AgentTaskContract -> ContextPacket -> AgentTaskResult -> ValidationReport
```

---

## 1. What Is a Mission Class?

A `MissionClass` is a repeatable type of work Oli can interpret, execute, validate and potentially convert into a playbook.

It is not a single mission instance.

Example:

```text
Mission instance:
"Convert these rough pricing notes into a Claude Code-ready spec."

Mission class:
founder_notes_to_claude_code_spec
```

Canonical early mission classes:

```text
founder_notes_to_claude_code_spec
feedback_docs_to_roadmap_issues_specs
repo_inspection_to_fix_plan
recurring_client_report
sales_marketing_ops_preparation_not_sending
```

Every mission class must define:

- input contract;
- output contract;
- permission ceiling;
- default topology;
- success criteria;
- validation strategy;
- playbook candidate rule.

---

## 2. When Does a Mission Class Deserve Subagents?

A mission class deserves subagents only if subagents improve at least one:

- quality;
- security;
- latency;
- cost.

Strong signals:

- multiple independent sources;
- high ambiguity;
- need for specialist reasoning;
- need for independent validation;
- external tool risk;
- parallel research;
- high-value output;
- repeated workflow that may become a playbook.

Weak signals:

- "multi-agent sounds advanced";
- the output is just text;
- one strong model with tools can do it;
- no validator exists;
- no eval baseline exists.

Rule:

```text
If a subagent cannot receive a clear AgentTaskContract,
the work is not ready to be delegated.
```

---

## 3. Internal Contracts

### Relationship With Existing Suboperator Schema

The existing `tdd/schemas/suboperator.ts` remains valid.

It describes executable suboperators:

```text
SuboperatorTask -> SuboperatorInterface.execute() -> SuboperatorResult
```

ADR-023 adds a stricter orchestration layer above it:

```text
MissionClass
  -> TopologyDecision
  -> AgentTaskContract
  -> ContextPacket
  -> executable SuboperatorTask
  -> SuboperatorResult
  -> AgentTaskResult
  -> ValidationReport
```

Interpretation:

- `suboperator.ts` is the runtime worker interface.
- `subagent_contracts.ts` is the mission-level contract/audit/eval layer.
- The Orchestrator may compile an `AgentTaskContract + ContextPacket` into one or more `SuboperatorTask`s.
- The Mission Black Box records the higher-level contracts, not only raw suboperator calls.

Do not delete `suboperator.ts`. Deprecation is not justified yet. The next implementation decision is whether the Python runtime mirrors both layers or collapses them internally while preserving the TDD contracts.

### MissionClass

```yaml
mission_class:
  id: founder_notes_to_claude_code_spec
  title: Founder notes -> Claude Code-ready spec
  description: Convert rough founder notes into an implementation-ready spec.
  primary_icp:
    - founder_builder
    - product_engineering_ops
  input_contract:
    required:
      - raw_notes
    optional:
      - repo_context
      - relevant_docs
      - constraints
      - target_files
      - existing_decisions
  output_contract:
    artifacts:
      - implementation_spec
      - open_questions
      - risk_notes
      - validation_checklist
    format: markdown
  permission_ceiling: class_1
  default_topology: manager_with_specialists_as_tools
  success_criteria:
    - spec_has_clear_goal
    - spec_has_non_goals
    - spec_has_implementation_scope
    - spec_has_acceptance_tests
    - spec_has_risks_and_assumptions
    - claude_code_can_execute_with_minimal_questions
  validation_strategy:
    validator_role: technical_spec_validator
    required: true
  playbook_candidate_rule:
    repeated_use_threshold: 3
    requires_user_confirmation: true
```

### AgentTaskContract

```yaml
agent_task_contract:
  task_id: uuid
  mission_id: uuid
  mission_class_id: founder_notes_to_claude_code_spec
  role: technical_spec_writer
  objective: Produce an implementation-ready spec from rough notes.
  non_goals:
    - do_not_write_code
    - do_not_modify_files
    - do_not_invent_missing_product_decisions
  inputs:
    context_packet_id: uuid
  allowed_tools:
    - read_repo_files
    - search_repo
  forbidden_tools:
    - write_files
    - run_commands
    - external_network
  permission_ceiling: class_1
  expected_output_schema: technical_spec_v0
  success_criteria:
    - identifies_goal
    - identifies_scope
    - identifies_non_goals
    - maps_notes_to_files_or_modules_if_possible
    - lists_acceptance_tests
    - marks_open_questions_explicitly
  budgets:
    max_tokens: 8000
    max_wall_time_seconds: 180
    max_tool_calls: 12
  evidence_requirements:
    - cite_relevant_input_note_ids
    - cite_repo_files_if_used
  failure_policy:
    on_missing_context: return_blocked_with_specific_question
    on_conflicting_context: return_conflict_report
    on_tool_failure: return_partial_with_error
```

### ContextPacket

```yaml
context_packet:
  context_packet_id: uuid
  mission_id: uuid
  intended_role: technical_spec_writer
  summary:
    user_intent: Convert rough notes into implementation-ready spec.
    mission_class_id: founder_notes_to_claude_code_spec
  source_inputs:
    - id: note_001
      type: user_note
      content_ref: runtime_artifact_ref
      trust_level: user_provided
      reason_included: Primary user input.
  retrieved_memory:
    - id: mem_123
      layer: project
      reason_included: Existing decision about V0 feature freeze.
      confidence: high
      content_ref: memory_ref
  repo_context:
    - path: tdd/domain/oli-constitution.md
      reason_included: Defines product character and operating principles.
      excerpt_ref: excerpt_ref
  constraints:
    - no_product_code_changes
    - respect_v0_feature_freeze
    - output_must_be_claude_code_ready
  forbidden_context:
    - unrelated_private_user_documents
    - raw_credentials
    - full_repo_dump
  provenance:
    generated_by: orchestrator
    generated_at: iso_timestamp
  token_budget:
    max_context_tokens: 12000
```

Context rules:

- Every included item must have `reason_included`.
- Every memory must have `confidence`.
- Every source must have `trust_level`.
- Forbidden context must be declared when relevant.
- The packet must be reproducible from the mission trace.

### AgentTaskResult

```yaml
agent_task_result:
  task_id: uuid
  mission_id: uuid
  role: technical_spec_writer
  status: completed
  output:
    artifact_type: technical_spec_v0
    artifact_ref: runtime_artifact_ref
  assumptions:
    - assumption: No production UI exists yet.
      confidence: medium
      evidence_ref: repo_search_result
  open_questions:
    - question: Should this spec target V0 or V1?
      blocking: false
  risks:
    - risk: Spec may imply new product feature despite V0 freeze.
      severity: high
      mitigation: Mark as TDD-only until unfreeze.
  evidence_refs:
    - note_001
    - tdd/domain/oli-constitution.md
  tool_calls_summary:
    count: 4
    failures: 0
  cost_summary:
    tokens_in: 6000
    tokens_out: 1800
    wall_time_seconds: 42
  confidence: 0.78
  suggested_next_steps:
    - Run validator against acceptance checklist.
  memory_suggestions:
    - key: preferred_spec_format
      value: Verdict, scope, files, tests, risks, open questions.
      confidence: medium
      reason: Repeated format preference observed.
  playbook_signal:
    candidate: true
    reason: Repeated mission class with stable input/output.
```

### ValidatorContract and ValidationReport

```yaml
validator_contract:
  validation_id: uuid
  mission_id: uuid
  target_task_id: uuid
  validator_role: technical_spec_validator
  validation_type:
    - schema_validation
    - success_criteria_validation
    - permission_validation
    - evidence_validation
  criteria:
    - id: spec_has_clear_goal
      blocking: true
    - id: spec_has_acceptance_tests
      blocking: true
    - id: no_unapproved_product_execution
      blocking: true
    - id: open_questions_marked
      blocking: false
  output_schema: validation_report_v0
```

```yaml
validation_report:
  validation_id: uuid
  overall_passed: false
  score: 0.75
  criteria_results:
    - criterion_id: spec_has_clear_goal
      passed: true
      evidence_ref: artifact_section_goal
    - criterion_id: spec_has_acceptance_tests
      passed: false
      evidence_ref: artifact_section_tests
      failure_reason: Tests are vague manual review, not acceptance checks.
      blocking: true
  repair_possible: true
  repair_instruction: Add concrete acceptance tests tied to expected files/behavior.
```

Validator rule:

```text
The validator must be able to fail an output even if the prose is good.
```

---

## 4. Allowed Topologies

```text
single_agent_with_tools
manager_with_specialists_as_tools
sequential_pipeline
parallel_fanout_gather
generator_validator
hierarchical_decomposition
handoff_user_facing
```

Default:

```text
single_agent_with_tools
```

Upgrade only when justified by mission class, risk, complexity or eval evidence.

### Topology Selector Rules v0

```text
If complexity=low and risk_class<=class_1:
  use single_agent_with_tools.

If independent validation is required:
  use generator_validator.

If parallel research is required and subtasks are independent:
  use parallel_fanout_gather.

If risk_class>=class_3:
  use workflow with visible route + approval gate + validator.

If ambiguity=high:
  use planner/specifier before executor.

If latency_sensitivity=high:
  prefer single_agent or parallel_fanout; avoid deep sequential pipeline.

If cost_sensitivity=high:
  use cheaper/local models for classification and strong models only for synthesis or critical validation.
```

---

## 5. Canonical Roles

These are canonical roles, not necessarily separate runtime agents in V0.

| Role | Responsibility |
|---|---|
| Orchestrator | Interpret intent, select mission class, build context packets, choose topology, coordinate tasks, synthesize final answer. |
| Planner / Specifier | Convert ambiguous input into MissionSpec or executable plan. |
| Researcher | Produce sourced findings with dates, confidence and gaps. |
| Technical Architect | Evaluate technical options, tradeoffs, risks and ADR candidates. |
| Execution Operator | Execute concrete actions under permissions. |
| Validator | Validate outputs against success criteria and evidence. |
| Memory Curator | Suggest memory updates, never write directly. |
| Playbook Curator | Detect repeatable mission patterns. |
| Synthesizer | Combine partial results into a final deliverable with evidence, contradictions and uncertainty preserved. |

---

## 6. Partial Output Validation

An `AgentTaskResult` must be validated when:

- it feeds another task;
- it touches a blocking success criterion;
- it can affect external actions;
- it will be delivered to the user;
- it may update memory;
- it may become a playbook;
- it is used as a training/eval example.

Validation checks:

- schema validity;
- success criteria;
- evidence references;
- permission compliance;
- missing critical information;
- hallucinated sources/actions;
- contradiction with prior results;
- repairability.

---

## 7. Connection To Core Oli Systems

### LangGraph

LangGraph executes the selected topology:

- nodes may represent roles, validators or deterministic transforms;
- edges encode sequencing, fan-out/gather, repair loops and approval gates;
- graph state stores task contracts, context packet refs, task result refs and validation report refs.

### Model Router

Model Router selects model/adaptor per task:

- cheap/local model for low-risk classification;
- strong reasoning model for planning, validation and synthesis;
- privacy mode gates external providers;
- routing decision is evidence.

### Evals

Evals compare:

- single-agent baseline;
- candidate topology;
- model routing variants;
- validation strategies.

No multi-agent topology is accepted unless it beats baseline in at least one important metric without unacceptable regressions.

### Mission Black Box

Mission Black Box records:

- mission class;
- topology decision;
- context packets;
- agent task contracts;
- agent task results;
- validation reports;
- model routing decisions;
- tool calls;
- approvals;
- cost/latency;
- final synthesis.

### Memory and Playbooks

Memory Curator and Playbook Curator consume task results and validation reports. They do not write directly.

Memory/playbook updates require provenance and reason.

---

## 8. V0/V1 Scope And Deferrals

### Build in V0/V1

- Mission Class registry, even if static.
- `AgentTaskContract` v0.
- `ContextPacket` v0.
- `AgentTaskResult` v0.
- `ValidatorContract` v0.
- `TopologySelector` rules v0.
- First flow: `founder_notes_to_claude_code_spec`.
- Evals against single-agent baseline.

### Defer

- swarm behavior;
- deep hierarchy;
- user-facing handoffs;
- persistent autonomous subagents;
- automatic topology learning;
- fine-tuning subagents;
- external actions beyond existing permission gates;
- production UI for subagent traces.

---

## First Mission Class To Prove

```text
founder_notes_to_claude_code_spec
```

Reason:

- directly helps build Oli;
- high leverage for founder workflow;
- clear input/output;
- validation can check whether Claude Code can implement;
- low external risk;
- useful public lab candidate later.
