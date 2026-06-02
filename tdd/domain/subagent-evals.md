# Subagent Evals

**Estado:** eval plan
**Fecha:** 2026-05-31
**ADR:** `tdd/adrs/ADR-023-subagent-engineering-contracts.md`

---

## Purpose

Subagent engineering is only valuable if it beats simpler baselines.

This document defines how Oli evaluates whether a mission class should use a single agent, specialists-as-tools, pipeline, fan-out, generator-validator, or deeper decomposition.

Rule:

```text
No multi-agent topology is accepted unless it improves quality, security, latency or cost
without unacceptable regression in the others.
```

---

## Baseline

Every mission class must start with a baseline:

```text
single_agent_with_tools
```

The baseline receives:

- same raw input;
- same allowed tools;
- same permission ceiling;
- same output contract;
- same validation criteria.

Candidate topologies are compared against this baseline.

---

## First Eval Target

Mission class:

```text
founder_notes_to_claude_code_spec
```

Baseline:

```text
single_agent_with_tools
```

Candidate:

```text
manager_with_specialists_as_tools
  - planner
  - technical_spec_writer
  - technical_spec_validator
```

Optional later candidate:

```text
sequential_pipeline
  raw_notes -> mission_spec -> implementation_spec -> validation_report -> repaired_spec
```

---

## Fixture Set v0

Create at least 20 fixtures before implementation:

| Fixture Type | Count | Purpose |
|---|---:|---|
| Clean founder notes | 5 | Basic conversion to spec. |
| Ambiguous notes | 5 | Tests open questions and assumptions. |
| Notes that imply feature creep | 3 | Tests V0 freeze / scope protection. |
| Notes with repo constraints | 3 | Tests use of limited repo context. |
| Contradictory notes | 2 | Tests conflict detection. |
| Bad/adversarial instruction | 2 | Tests permission and context boundaries. |

Each fixture includes:

- raw notes;
- optional context refs;
- expected output requirements;
- blocking criteria;
- non-blocking criteria;
- forbidden behavior;
- expected topology recommendation.

---

## Metrics

### Quality

- validation pass rate;
- blocking criteria pass rate;
- number of unresolved blocking questions;
- implementation readiness score;
- human preference score;
- repair cycles needed.

### Security / Permission

- permission ceiling respected;
- forbidden tools avoided;
- no product execution when task is TDD-only;
- sensitive context excluded from context packets;
- no unapproved external actions.

### Cost

- tokens in/out;
- model cost;
- tool calls;
- wall time;
- cost per accepted spec.

### Latency

- p50/p95 completion time;
- fan-out overhead;
- repair loop overhead.

### Context Quality

- relevant context included;
- irrelevant context excluded;
- each included item has reason;
- each memory has confidence;
- packet reproducible from trace.

### User Experience

- unnecessary questions;
- clarity of assumptions;
- clarity of next action;
- no generic assistant fluff;
- final answer has owner-ready format.

---

## Acceptance Threshold v0

A candidate topology is accepted for a mission class if:

```text
blocking criteria pass rate improves by >= 15%
OR repair cycles decrease by >= 25%
OR implementation readiness improves by >= 20%
OR cost decreases by >= 20% at equal quality
OR latency decreases by >= 20% at equal quality
```

And:

```text
permission/security regressions = 0
critical hallucinated sources/actions = 0
unapproved external actions = 0
```

For early V0/V1, quality and security dominate cost.

---

## Evaluation Report

Each eval run must produce:

```yaml
eval_report:
  eval_id: uuid
  mission_class_id: founder_notes_to_claude_code_spec
  baseline_topology: single_agent_with_tools
  candidate_topology: manager_with_specialists_as_tools
  fixture_count: 20
  metrics:
    validation_pass_rate:
      baseline: 0.65
      candidate: 0.82
    blocking_criteria_pass_rate:
      baseline: 0.70
      candidate: 0.90
    avg_cost_usd:
      baseline: 0.08
      candidate: 0.12
    avg_latency_seconds:
      baseline: 35
      candidate: 54
    permission_regressions:
      baseline: 0
      candidate: 0
  verdict: accepted_with_cost_tradeoff
  reason: Candidate improves blocking criteria enough to justify extra cost for this mission class.
  failure_analysis:
    - Candidate still asks unnecessary clarifying questions in 2 fixtures.
  next_actions:
    - Improve planner rules for ambiguity handling.
```

---

## Human Review

LLM-as-judge can help, but cannot be the only judge for early mission classes.

Human review is required for:

- implementation readiness;
- taste/clarity;
- whether open questions are actually necessary;
- whether spec is useful for Claude Code.

---

## Regression Policy

Once accepted, a topology becomes part of the mission class contract.

It must be re-evaluated when:

- prompts change;
- model router changes;
- a new base model/provider is introduced;
- context packet builder changes;
- mission class output contract changes;
- validation schema changes.

