# State-of-the-Art Discovery

**Estado:** canonical domain spec
**Fecha:** 2026-05-31
**ADR:** `tdd/adrs/ADR-025-state-of-art-discovery-and-decision-memos.md`

---

## Veredicto

Oli must not recommend from stale memory or shallow search.

For decisions that depend on current tools, models, APIs, infrastructure, pricing, security, benchmarks or market conditions, Oli produces a decision memo with evidence, alternatives, buildability, risk and a recheck date.

The canonical unit is:

```text
StateOfArtDecisionMemo
```

Not:

```text
"Here are some options..."
```

---

## Mission Class

Canonical mission class:

```text
state_of_art_decision_memo
```

Purpose:

```text
Turn a current/unstable decision into a ranked, evidence-backed, actionable recommendation.
```

Example user intents:

- "What local model should Oli install for Starter tier?"
- "Which search API should we use for AI research?"
- "Should we deploy n8n for the user or recommend SaaS?"
- "What is the current best stack for browser automation agents?"
- "Which vector DB/memory architecture should we use now?"

---

## Workflow

```text
DecisionClassifier
  -> CriteriaBuilder
  -> SourcePlanner
  -> EvidenceRetriever
  -> SourceRanker
  -> OptionGenerator
  -> OptionScorer
  -> BuildabilityChecker
  -> RiskChecker
  -> DecisionMemoWriter
  -> Validator
  -> Mission Black Box
```

### 1. DecisionClassifier

Classifies the decision:

```text
model_selection
tool_selection
cloud_service_selection
architecture_pattern
automation_strategy
security_policy
pricing_vendor_decision
ai_first_workflow_recommendation
build_vs_buy
```

### 2. CriteriaBuilder

Defines criteria before retrieval.

Examples:

Model selection:

```text
quality, effective_context, vram_fit, latency, license, cost, tool_use, structured_outputs
```

Tool/vendor selection:

```text
capabilities, API quality, pricing, lock-in, security, reliability, integration cost
```

Cloud/service broker:

```text
total cost, support burden, uptime, data residency, operational complexity, margin impact
```

### 3. SourcePlanner

Chooses source types by decision class:

- official docs;
- API docs;
- model cards;
- pricing pages;
- GitHub repos/issues;
- benchmark leaderboards;
- security advisories;
- community reports;
- internal Oli memory/solution bank;
- prior mission traces.

### 4. EvidenceRetriever

Retrieves evidence using available tools:

- web search;
- official docs search;
- GitHub search/issues;
- vendor APIs;
- benchmark APIs/leaderboards;
- pricing fetchers;
- internal memory;
- Oli benchmarks.

### 5. SourceRanker

Scores every source:

```yaml
source_quality:
  source_type: official_docs | technical_report | benchmark | leaderboard | github | pricing | community | seo_blog
  authority: 0.0-1.0
  freshness: 0.0-1.0
  methodology_clarity: 0.0-1.0
  relevance_to_decision: 0.0-1.0
  bias_risk: 0.0-1.0
  citation_confidence: 0.0-1.0
```

### 6. OptionGenerator

Generates 2-5 real options:

- recommended;
- strong alternative;
- low-cost alternative;
- high-control/self-hosted alternative;
- do-nothing/keep-current.

### 7. OptionScorer

Scores each option:

```yaml
option_score:
  quality: number
  fit_to_user: number
  buildability: number
  cost: number
  latency: number
  security_privacy: number
  maintainability: number
  reversibility: number
  strategic_moat: number
```

### 8. BuildabilityChecker

Checks whether Oli can realistically build, install or operate the option with current constraints:

- hardware;
- engineering effort;
- dependencies;
- ops burden;
- support risk;
- time to first value;
- migration complexity.

### 9. RiskChecker

Checks:

- license;
- privacy;
- security;
- prompt injection surface;
- data residency;
- vendor lock-in;
- reputational risk;
- failure modes.

### 10. DecisionMemoWriter

Produces final memo:

```markdown
# Decision Memo

## Verdict
...

## Recommended Option
...

## Why
...

## Alternatives Considered
...

## Evidence
...

## Cost / Effort
...

## Risks
...

## Reversibility
...

## Next Action
...

## Recheck Date
...
```

### 11. Validator

Fails the memo if:

- no current sources;
- no alternatives;
- no buildability check;
- no risk check;
- claims without evidence;
- source quality too weak;
- no next action;
- no recheck date.

---

## Recommendation Quality Rules

A recommendation is weak if it:

- lacks citations;
- lacks dates;
- compares no alternatives;
- ignores tradeoffs;
- ignores cost;
- ignores implementation fit;
- ignores risk;
- has no next action;
- recommends popularity without fit;
- says "best" without defining the goal.

A recommendation is strong if it:

- defines the decision class;
- defines criteria first;
- separates facts, inference and opinion;
- ranks source quality;
- compares options;
- checks buildability;
- checks risk;
- provides a concrete next action;
- sets a recheck date.

---

## Tool Layer

Recommended tool families:

```text
source_search.web(query, filters)
source_search.official_docs(query, domains)
source_search.github_repo(query)
source_search.github_issues(repo, query)
model_intelligence.recommend_model(...)
pricing.fetch_vendor_pricing(vendor)
benchmark.fetch_leaderboard(source, category)
cloud_advisor.estimate_cost(service, region, usage)
license_checker.check(repo_or_model)
security_advisor.check_known_risks(package_or_service)
```

Oli should not rely on a single generic search tool for important decisions.

---

## Source Requirements

Strong recommendation:

```text
>= 2 Tier A/B sources
OR
1 Tier A source + Oli benchmark/eval
```

If source quality is insufficient:

```text
verdict = provisional
```

Oli must say what would change confidence.

---

## Connection To Subagents

Simple decisions:

```text
single_agent_with_tools + validator
```

Complex decisions:

```text
manager_with_specialists_as_tools:
  - researcher
  - technical_architect
  - cost_checker
  - risk_checker
  - validator
```

Subagent contracts must follow ADR-023.

---

## Mission Black Box

Record:

- decision class;
- criteria;
- source plan;
- evidence refs;
- source quality scores;
- option scores;
- buildability report;
- risk report;
- final memo;
- validation report;
- recheck date.

---

## Public Lab

Public lab candidate:

```text
oli-state-of-art-advisor-lab
```

Safe demos:

- choose local model for coding agent on RTX 4090;
- choose search API for agentic research;
- choose deployment option for n8n automation;
- choose browser automation stack.

Public artifacts:

- synthetic decision memos;
- evidence packs;
- scoring scripts;
- eval reports.

Do not publish:

- private routing economics;
- vendor discounts;
- customer traces;
- proprietary playbooks;
- internal source weights if they become moat.

---

## Relationship To Model Intelligence

Model Intelligence is a specialized module inside State-of-the-Art Discovery.

```text
State-of-the-Art Discovery Engine
  includes Model Intelligence
  includes Tool/Vendor Intelligence
  includes Cloud/Infra Intelligence
  includes Security/License Intelligence
  includes Buildability/Cost Intelligence
```

Future TDD:

```text
ADR-024-model-intelligence-and-runtime-model-selection.md
tdd/domain/model-intelligence.md
tdd/schemas/model_registry.ts
tdd/domain/model-selection-evals.md
```

