/**
 * OLI - Subagent Engineering Contracts
 *
 * These schemas formalize ADR-023. They do not replace the older
 * SuboperatorTask/SuboperatorResult immediately; they define the stricter
 * contract layer that future orchestrator code should move toward.
 */

import { z } from "zod"
import { PermissionClass } from "./tool"

export const MissionClassId = z.string().min(3)
export type MissionClassId = z.infer<typeof MissionClassId>

export const CanonicalSubagentRole = z.enum([
  "orchestrator",
  "planner",
  "specifier",
  "researcher",
  "technical_architect",
  "execution_operator",
  "validator",
  "memory_curator",
  "playbook_curator",
  "synthesizer",
])
export type CanonicalSubagentRole = z.infer<typeof CanonicalSubagentRole>

export const TopologyKind = z.enum([
  "single_agent_with_tools",
  "manager_with_specialists_as_tools",
  "sequential_pipeline",
  "parallel_fanout_gather",
  "generator_validator",
  "hierarchical_decomposition",
  "handoff_user_facing",
])
export type TopologyKind = z.infer<typeof TopologyKind>

export const Sensitivity = z.enum(["low", "medium", "high"])
export type Sensitivity = z.infer<typeof Sensitivity>

export const MissionClass = z.object({
  id: MissionClassId,
  title: z.string().min(3),
  description: z.string().min(10),
  primary_icp: z.array(z.string()).default([]),
  input_contract: z.object({
    required: z.array(z.string()),
    optional: z.array(z.string()).default([]),
  }),
  output_contract: z.object({
    artifacts: z.array(z.string()),
    format: z.string(),
  }),
  permission_ceiling: PermissionClass,
  default_topology: TopologyKind,
  success_criteria: z.array(z.string()).min(1),
  validation_strategy: z.object({
    validator_role: z.string(),
    required: z.boolean().default(true),
  }),
  playbook_candidate_rule: z.object({
    repeated_use_threshold: z.number().int().positive().default(3),
    requires_user_confirmation: z.boolean().default(true),
  }),
})
export type MissionClass = z.infer<typeof MissionClass>

export const AgentTaskContract = z.object({
  task_id: z.string().uuid(),
  mission_id: z.string().uuid(),
  mission_class_id: MissionClassId,
  role: z.string(),
  objective: z.string().min(10),
  non_goals: z.array(z.string()).default([]),
  inputs: z.object({
    context_packet_id: z.string().uuid(),
  }),
  allowed_tools: z.array(z.string()).default([]),
  forbidden_tools: z.array(z.string()).default([]),
  permission_ceiling: PermissionClass,
  expected_output_schema: z.string(),
  success_criteria: z.array(z.string()).min(1),
  budgets: z.object({
    max_tokens: z.number().int().positive().optional(),
    max_wall_time_seconds: z.number().int().positive().optional(),
    max_tool_calls: z.number().int().nonnegative().optional(),
  }).default({}),
  evidence_requirements: z.array(z.string()).default([]),
  failure_policy: z.object({
    on_missing_context: z.string(),
    on_conflicting_context: z.string(),
    on_tool_failure: z.string(),
  }),
})
export type AgentTaskContract = z.infer<typeof AgentTaskContract>

export const ContextSource = z.object({
  id: z.string(),
  type: z.string(),
  content_ref: z.string(),
  trust_level: z.enum(["system", "user_provided", "retrieved_memory", "repo", "web", "tool_output", "untrusted"]),
  reason_included: z.string().min(3),
})
export type ContextSource = z.infer<typeof ContextSource>

export const RetrievedMemoryRef = z.object({
  id: z.string(),
  layer: z.enum(["user", "company", "project", "mission", "playbook"]),
  reason_included: z.string().min(3),
  confidence: z.enum(["low", "medium", "high"]),
  content_ref: z.string(),
})
export type RetrievedMemoryRef = z.infer<typeof RetrievedMemoryRef>

export const RepoContextRef = z.object({
  path: z.string(),
  reason_included: z.string().min(3),
  excerpt_ref: z.string().optional(),
})
export type RepoContextRef = z.infer<typeof RepoContextRef>

export const ContextPacket = z.object({
  context_packet_id: z.string().uuid(),
  mission_id: z.string().uuid(),
  intended_role: z.string(),
  summary: z.object({
    user_intent: z.string(),
    mission_class_id: MissionClassId,
  }),
  source_inputs: z.array(ContextSource).default([]),
  retrieved_memory: z.array(RetrievedMemoryRef).default([]),
  repo_context: z.array(RepoContextRef).default([]),
  constraints: z.array(z.string()).default([]),
  forbidden_context: z.array(z.string()).default([]),
  provenance: z.object({
    generated_by: z.string(),
    generated_at: z.string().datetime(),
  }),
  token_budget: z.object({
    max_context_tokens: z.number().int().positive(),
  }),
})
export type ContextPacket = z.infer<typeof ContextPacket>

export const TaskStatus = z.enum(["completed", "partial", "blocked", "failed"])
export type TaskStatus = z.infer<typeof TaskStatus>

export const AgentTaskResult = z.object({
  task_id: z.string().uuid(),
  mission_id: z.string().uuid(),
  role: z.string(),
  status: TaskStatus,
  output: z.object({
    artifact_type: z.string(),
    artifact_ref: z.string(),
  }).optional(),
  assumptions: z.array(z.object({
    assumption: z.string(),
    confidence: z.enum(["low", "medium", "high"]),
    evidence_ref: z.string().optional(),
  })).default([]),
  open_questions: z.array(z.object({
    question: z.string(),
    blocking: z.boolean().default(false),
  })).default([]),
  risks: z.array(z.object({
    risk: z.string(),
    severity: z.enum(["low", "medium", "high"]),
    mitigation: z.string().optional(),
  })).default([]),
  evidence_refs: z.array(z.string()).default([]),
  tool_calls_summary: z.object({
    count: z.number().int().nonnegative(),
    failures: z.number().int().nonnegative(),
  }).default({ count: 0, failures: 0 }),
  cost_summary: z.object({
    tokens_in: z.number().int().nonnegative().default(0),
    tokens_out: z.number().int().nonnegative().default(0),
    wall_time_seconds: z.number().nonnegative().default(0),
  }).default({ tokens_in: 0, tokens_out: 0, wall_time_seconds: 0 }),
  confidence: z.number().min(0).max(1),
  suggested_next_steps: z.array(z.string()).default([]),
  memory_suggestions: z.array(z.object({
    key: z.string(),
    value: z.unknown(),
    confidence: z.enum(["low", "medium", "high"]),
    reason: z.string(),
  })).default([]),
  playbook_signal: z.object({
    candidate: z.boolean(),
    reason: z.string().optional(),
  }).default({ candidate: false }),
})
export type AgentTaskResult = z.infer<typeof AgentTaskResult>

export const ValidatorContract = z.object({
  validation_id: z.string().uuid(),
  mission_id: z.string().uuid(),
  target_task_id: z.string().uuid(),
  validator_role: z.string(),
  validation_type: z.array(z.enum([
    "schema_validation",
    "success_criteria_validation",
    "permission_validation",
    "evidence_validation",
  ])).min(1),
  criteria: z.array(z.object({
    id: z.string(),
    blocking: z.boolean().default(false),
  })).min(1),
  output_schema: z.string(),
})
export type ValidatorContract = z.infer<typeof ValidatorContract>

export const ValidationReport = z.object({
  validation_id: z.string().uuid(),
  overall_passed: z.boolean(),
  score: z.number().min(0).max(1),
  criteria_results: z.array(z.object({
    criterion_id: z.string(),
    passed: z.boolean(),
    evidence_ref: z.string().optional(),
    failure_reason: z.string().optional(),
    blocking: z.boolean().default(false),
  })),
  repair_possible: z.boolean(),
  repair_instruction: z.string().optional(),
})
export type ValidationReport = z.infer<typeof ValidationReport>

export const TopologySelectorInput = z.object({
  mission_class_id: MissionClassId,
  complexity: Sensitivity,
  risk_class: PermissionClass,
  ambiguity: Sensitivity,
  requires_external_tools: z.boolean(),
  requires_parallel_research: z.boolean(),
  requires_independent_validation: z.boolean(),
  latency_sensitivity: Sensitivity,
  cost_sensitivity: Sensitivity,
})
export type TopologySelectorInput = z.infer<typeof TopologySelectorInput>

export const TopologyDecision = z.object({
  topology: TopologyKind,
  reason: z.string().min(10),
  agents: z.array(z.string()).default([]),
  model_routing: z.record(z.string(), z.string()).default({}),
  expected_cost_tier: z.enum(["low", "medium", "high"]),
  approval_required: z.boolean(),
})
export type TopologyDecision = z.infer<typeof TopologyDecision>

