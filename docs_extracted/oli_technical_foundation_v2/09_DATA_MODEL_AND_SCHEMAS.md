# 09 - Data Model and Schemas

## Purpose

This file gives Claude Code enough structure to implement V0 without inventing the data model.

## Core entities

### users

- id
- email nullable for local mode
- display_name
- role
- created_at
- updated_at

### organizations

- id
- name
- deployment_profile
- privacy_mode
- created_at
- updated_at

### memberships

- id
- user_id
- organization_id
- role

### missions

- id
- organization_id
- user_id
- title
- raw_intent
- normalized_objective
- mission_class
- status
- risk_class
- privacy_level
- approval_required
- model_policy_id
- tool_policy_id
- cost_budget_usd
- solution_derivable (bool, default false — flags whether this mission resolved a generalizable pattern eligible for the Oli solution bank; set by ValidationSuboperator post-delivery, never by the executor)
- created_at
- updated_at

### mission_tasks

- id
- mission_id
- title
- objective
- status
- executor_type
- risk_class
- attempt
- max_attempts
- created_at
- updated_at

### mission_events

- id
- mission_id
- task_id nullable
- event_type
- actor
- summary
- data_json
- created_at

### artifacts

- id
- mission_id
- task_id nullable
- name
- artifact_type
- storage_uri
- sha256
- provenance_json
- sensitivity
- created_at

### approvals

- id
- mission_id
- task_id nullable
- requested_action
- risk_class
- reason
- preview_artifact_id nullable
- status
- decided_by nullable
- decided_at nullable
- created_at

### validation_reports

- id
- mission_id
- task_id nullable
- validator
- status
- summary
- evidence_json
- created_at

### model_profiles

- id
- organization_id
- user_id nullable
- name
- privacy_mode
- default_fast_model_id
- default_main_model_id
- default_embedding_model_id
- default_premium_provider nullable
- allow_premium
- premium_approval_threshold_usd
- config_json
- created_at

### model_registry

- id
- provider
- display_name
- family
- roles_json
- local
- requires_gpu
- min_vram_gb nullable
- recommended_vram_gb nullable
- context_tokens_estimate nullable
- privacy_rating
- status
- metadata_json

### model_benchmarks

- id
- model_registry_id
- model_profile_id nullable
- organization_id
- benchmark_name
- score_json
- latency_ms nullable
- passed
- created_at

### model_calls

- id
- mission_id
- task_id nullable
- model_id
- provider
- local
- prompt_tokens nullable
- completion_tokens nullable
- latency_ms nullable
- estimated_cost_usd
- data_sensitivity
- redacted
- reason
- created_at

### tool_calls

- id
- mission_id
- task_id nullable
- tool_name
- executor_type
- risk_class
- input_summary
- output_summary
- status
- policy_decision_id nullable
- created_at

### memory_items

- id
- organization_id
- user_id nullable
- scope
- memory_type
- title
- content
- source_type
- source_id
- confidence
- sensitivity
- status
- tags_json
- created_at
- updated_at

### memory_links

- id
- source_memory_id
- target_memory_id
- relation_type
- created_at

### playbooks

- id
- organization_id
- name
- mission_class
- version
- status
- trigger_description
- steps_json
- validators_json
- approvals_json
- created_at
- updated_at

### policies

- id
- organization_id
- policy_type
- name
- config_json
- created_at
- updated_at

### audit_logs

- id
- organization_id
- user_id nullable
- mission_id nullable
- task_id nullable
- actor
- action
- permission_class
- data_sensitivity
- policy_decision
- approval_id nullable
- input_summary
- output_summary
- created_at

## Enum suggestions

### MissionStatus

```text
created
intake_normalized
context_retrieved
classified
planned
awaiting_approval
executing
validating
repairing
delivering
delivered
partially_delivered
failed
cancelled
memory_reviewed
archived
```

### RiskClass

```text
0_readonly_public
1_local_reversible
2_sensitive_or_external_read
3_external_reversible_write
4_external_irreversible
5_admin_security_boundary
```

### PrivacyMode

```text
local_only
hybrid_redacted
hybrid_approval
quality_first
custom
```

### Sensitivity

```text
public
internal
confidential
restricted
secret
```

## V0 implementation order

1. organizations/users minimal
2. missions
3. mission_events
4. mission_tasks
5. artifacts
6. approvals
7. validation_reports
8. model_profiles/model_calls
9. tool_calls
10. memory_items
11. audit_logs

## Database rules

- Use migrations.
- Use enums where practical.
- Store flexible policy/evidence data in JSONB.
- Keep mission state canonical in Postgres.
- Every event belongs to a mission.
- Every artifact has provenance.
- Every model/tool call is auditable.
