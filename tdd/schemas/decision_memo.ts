/**
 * OLI - Decision Memo Schema
 *
 * Canonical output for state-of-the-art discovery missions.
 * See ADR-025 and tdd/domain/state-of-art-discovery.md.
 */

import { z } from "zod"

export const DecisionClass = z.enum([
  "model_selection",
  "tool_selection",
  "cloud_service_selection",
  "architecture_pattern",
  "automation_strategy",
  "security_policy",
  "pricing_vendor_decision",
  "ai_first_workflow_recommendation",
  "build_vs_buy",
])
export type DecisionClass = z.infer<typeof DecisionClass>

export const SourceTier = z.enum(["A_primary", "B_trusted_aggregator", "C_community", "D_low_authority"])
export type SourceTier = z.infer<typeof SourceTier>

export const SourceQuality = z.object({
  source_id: z.string(),
  url: z.string().url().optional(),
  title: z.string(),
  source_type: z.enum([
    "official_docs",
    "api_docs",
    "technical_report",
    "model_card",
    "benchmark",
    "leaderboard",
    "github",
    "pricing",
    "security_advisory",
    "community",
    "seo_blog",
    "internal_oli_eval",
    "internal_memory",
  ]),
  tier: SourceTier,
  authority: z.number().min(0).max(1),
  freshness: z.number().min(0).max(1),
  methodology_clarity: z.number().min(0).max(1),
  relevance_to_decision: z.number().min(0).max(1),
  bias_risk: z.number().min(0).max(1),
  citation_confidence: z.number().min(0).max(1),
  retrieved_at: z.string().datetime(),
})
export type SourceQuality = z.infer<typeof SourceQuality>

export const DecisionCriteria = z.object({
  id: z.string(),
  label: z.string(),
  weight: z.number().min(0).max(1),
  reason: z.string(),
})
export type DecisionCriteria = z.infer<typeof DecisionCriteria>

export const OptionScore = z.object({
  quality: z.number().min(0).max(1),
  fit_to_user: z.number().min(0).max(1),
  buildability: z.number().min(0).max(1),
  cost: z.number().min(0).max(1),
  latency: z.number().min(0).max(1),
  security_privacy: z.number().min(0).max(1),
  maintainability: z.number().min(0).max(1),
  reversibility: z.number().min(0).max(1),
  strategic_moat: z.number().min(0).max(1),
  weighted_total: z.number().min(0).max(1),
})
export type OptionScore = z.infer<typeof OptionScore>

export const DecisionOption = z.object({
  option_id: z.string(),
  name: z.string(),
  category: z.enum(["recommended", "strong_alternative", "low_cost", "high_control", "keep_current", "rejected"]),
  summary: z.string(),
  pros: z.array(z.string()).default([]),
  cons: z.array(z.string()).default([]),
  score: OptionScore,
  evidence_refs: z.array(z.string()).default([]),
})
export type DecisionOption = z.infer<typeof DecisionOption>

export const BuildabilityReport = z.object({
  feasible_now: z.boolean(),
  required_capabilities: z.array(z.string()).default([]),
  blockers: z.array(z.string()).default([]),
  engineering_effort: z.enum(["low", "medium", "high", "unknown"]),
  ops_burden: z.enum(["low", "medium", "high", "unknown"]),
  time_to_first_value: z.enum(["same_day", "days", "weeks", "months", "unknown"]),
  notes: z.string().optional(),
})
export type BuildabilityReport = z.infer<typeof BuildabilityReport>

export const RiskReport = z.object({
  license_risk: z.enum(["low", "medium", "high", "unknown"]),
  privacy_risk: z.enum(["low", "medium", "high", "unknown"]),
  security_risk: z.enum(["low", "medium", "high", "unknown"]),
  vendor_lock_in: z.enum(["low", "medium", "high", "unknown"]),
  margin_risk: z.enum(["low", "medium", "high", "unknown"]),
  failure_modes: z.array(z.string()).default([]),
  mitigations: z.array(z.string()).default([]),
})
export type RiskReport = z.infer<typeof RiskReport>

export const StateOfArtDecisionMemo = z.object({
  decision_id: z.string().uuid(),
  mission_id: z.string().uuid().optional(),
  decision_class: DecisionClass,
  question: z.string(),
  verdict: z.enum(["recommend", "recommend_with_caveats", "provisional", "do_not_recommend", "needs_more_research"]),
  recommended_option_id: z.string().optional(),
  criteria: z.array(DecisionCriteria).min(1),
  sources: z.array(SourceQuality).min(1),
  options: z.array(DecisionOption).min(2),
  buildability: BuildabilityReport,
  risk: RiskReport,
  facts: z.array(z.string()).default([]),
  inferences: z.array(z.string()).default([]),
  assumptions: z.array(z.string()).default([]),
  unsupported_claims: z.array(z.string()).default([]),
  next_action: z.string(),
  recheck_date: z.string(), // YYYY-MM-DD
  generated_at: z.string().datetime(),
})
export type StateOfArtDecisionMemo = z.infer<typeof StateOfArtDecisionMemo>

