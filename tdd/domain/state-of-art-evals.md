# State-of-the-Art Discovery Evals

**Estado:** eval plan
**Fecha:** 2026-05-31
**ADR:** `tdd/adrs/ADR-025-state-of-art-discovery-and-decision-memos.md`

---

## Purpose

Oli must evaluate whether its recommendations are current, evidence-backed, actionable and not shallow.

This eval plan tests the `state_of_art_decision_memo` mission class.

---

## Fixture Categories

Create at least 30 fixtures:

| Category | Count | Example |
|---|---:|---|
| Model selection | 5 | Choose local model for RTX 4090 coding agent. |
| Tool/API selection | 5 | Choose search API for agentic research. |
| Cloud/service selection | 4 | Deploy n8n self-hosted vs SaaS. |
| Architecture pattern | 4 | Choose browser automation stack. |
| Build-vs-buy | 4 | Build internal CRM enrichment vs buy vendor. |
| Security-sensitive recommendation | 4 | Choose MCP tool for filesystem/browser access. |
| AI-first workflow recommendation | 4 | Recommend automation path for founder/team workflow. |

Each fixture includes:

- decision prompt;
- constraints;
- decision class;
- expected source types;
- required criteria;
- forbidden weak behaviors;
- acceptable options;
- risk hotspots;
- required next action.

---

## Metrics

### Evidence Quality

- source freshness;
- source authority;
- source diversity;
- primary-source coverage;
- citation correctness;
- methodology clarity.

### Recommendation Quality

- criteria defined before options;
- alternatives covered;
- tradeoffs explicit;
- verdict clear;
- next action concrete;
- recheck date present.

### Buildability

- hardware/runtime fit;
- implementation effort realism;
- dependency awareness;
- migration path;
- operational burden.

### Risk

- license risk identified;
- security risk identified;
- privacy risk identified;
- vendor lock-in;
- reversibility.

### Outcome Proxy

- human preference;
- expert review;
- later decision accuracy when rechecked;
- whether recommendation avoided known bad option.

---

## Acceptance Threshold v0

Decision memo passes if:

```text
primary_or_trusted_source_count >= 2
alternatives_count >= 2
buildability_check_present = true
risk_check_present = true
next_action_present = true
recheck_date_present = true
unsupported_critical_claims = 0
```

For high-impact technical decisions:

```text
source_quality_average >= 0.75
```

If evidence is weak, memo may pass only as:

```text
verdict = provisional
```

---

## Failure Modes To Test

Oli must fail or downgrade confidence when:

- sources are undated;
- only SEO blogs are found;
- pricing is not from official source;
- license claim is not verified;
- benchmark source lacks methodology;
- community reports conflict with official docs;
- option is strong technically but impossible under current hardware/tier;
- recommendation improves quality but breaks margin/security.

---

## Eval Report

Each run produces:

```yaml
eval_report:
  eval_id: uuid
  mission_class_id: state_of_art_decision_memo
  fixture_count: 30
  metrics:
    source_quality_avg: 0.82
    primary_source_coverage: 0.76
    alternatives_coverage: 0.91
    buildability_present_rate: 1.0
    risk_present_rate: 0.97
    unsupported_critical_claims: 0
    human_preference_score: 0.84
  verdict: passed
  failures:
    - fixture_id: tool_api_selection_003
      issue: Community source conflict was noted but not resolved.
  next_actions:
    - Improve conflict-resolution section in DecisionMemoWriter.
```

---

## Regression Policy

Re-run evals when:

- source tools change;
- search provider changes;
- decision memo schema changes;
- source scoring weights change;
- new decision class is added;
- model/router used for research changes.

