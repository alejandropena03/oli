# Oli Market Research Suboperator — Mission Spec

**Version:** 0.1  
**Status:** Foundation document — awaiting live research execution  
**Owner:** Oli Execution OS  
**Last updated:** 2026-05-25

---

## Purpose

This document defines the reusable `MarketResearchSuboperator` mission that Oli can invoke to understand its true target market, ICP segments, buyer personas, competitive landscape, and wedge strategy.

This is not a marketing document. This is a research mission spec — structured so Oli can execute it, validate it, and update it as evidence accumulates.

---

## Research Questions (Required)

The mission must answer all of the following:

1. Who is Oli's real target customer?
2. Which ICP segments have the strongest pain with current execution tools?
3. Which ICPs have budget and authority to buy?
4. What do they already use, and why?
5. What do they hate about those tools?
6. What would they pay for Oli, and why?
7. What security and privacy constraints matter to each segment?
8. Which workflows are most broken and most painful?
9. Which wedge use case should Oli start with?
10. How should Oli price early access?
11. Which acquisition channels should Oli test first?
12. What objections will buyers have?

---

## Methodology

### Phase 1 — Secondary Research (automated, browsing-based)
- Use web search and public sources to find:
  - Forum discussions (Reddit, Hacker News, IndieHackers, Twitter/X)
  - Job listings that reveal workflow pain
  - Competitor pricing pages and feature lists
  - Product reviews (G2, Capterra, ProductHunt)
  - Analyst reports and VC investment theses
  - LinkedIn profiles of likely buyers

### Phase 2 — Synthesis and Hypothesis Formation
- Cluster findings into ICP segments
- Score each segment on: pain intensity, budget, adoption speed, security complexity, sales difficulty, strategic fit
- Generate buyer personas with evidence backing
- Separate confirmed facts from inferred estimates from open hypotheses

### Phase 3 — Interview Design
- Generate discovery questions, WTP probes, and landing page copy hypotheses
- Design A/B test structures for landing page validation

### Phase 4 — Continuous Update
- Each time Oli completes a sales or user call, feed structured notes back into this mission
- MemoryCuratorSuboperator manages version tracking

---

## Output Template

> If live browsing is not available at research time, all finding sections below should be marked as: **[PENDING LIVE RESEARCH]**

---

# Oli Market Research Report

**Executed by:** MarketResearchSuboperator  
**Synthesized by:** Oli  
**Date:** [execution date]  
**Browsing available:** [yes / no]  
**Sources collected:** [count]

---

## 1. Executive Recommendation

| Field | Value |
|---|---|
| Primary ICP | [PENDING LIVE RESEARCH] |
| Secondary ICP | [PENDING LIVE RESEARCH] |
| Expansion ICP | [PENDING LIVE RESEARCH] |
| Recommended wedge | [PENDING LIVE RESEARCH] |
| Recommended first paid offer | [PENDING LIVE RESEARCH] |
| Confidence level | [PENDING LIVE RESEARCH] |
| Top unresolved assumptions | [PENDING LIVE RESEARCH] |

---

## 2. ICP Segments Compared

| Segment | Pain intensity (1-10) | Budget (1-10) | Adoption speed (1-10) | Security complexity (1-10) | Sales difficulty (1-10) | Strategic fit (1-10) | Composite score |
|---|---:|---:|---:|---:|---:|---:|---:|
| AI-first founders / builders | [PLR] | [PLR] | [PLR] | [PLR] | [PLR] | [PLR] | [PLR] |
| Solo operators / high-leverage solopreneurs | [PLR] | [PLR] | [PLR] | [PLR] | [PLR] | [PLR] | [PLR] |
| Small teams and agencies, 2-20 people | [PLR] | [PLR] | [PLR] | [PLR] | [PLR] | [PLR] | [PLR] |
| Operations teams in 50-500 person companies | [PLR] | [PLR] | [PLR] | [PLR] | [PLR] | [PLR] | [PLR] |
| Technical teams using Claude Code / Cursor / local models | [PLR] | [PLR] | [PLR] | [PLR] | [PLR] | [PLR] | [PLR] |
| Automation-heavy teams (Zapier, Make, n8n, Airtable, Notion, HubSpot, Slack, Google Workspace) | [PLR] | [PLR] | [PLR] | [PLR] | [PLR] | [PLR] | [PLR] |

*[PLR] = Pending Live Research*

---

## 3. Buyer Personas

> [PENDING LIVE RESEARCH — complete one block per persona after research phase 1]

**Persona template:**

```
Job title:
Company size:
Current workflow:
Core pain:
Existing tools:
Budget owner:
Likely budget range:
Objections to Oli:
Security concerns:
Buying trigger:
Success metric:
Message that resonates:
```

---

## 4. Budget and Willingness to Pay

> [PENDING LIVE RESEARCH]

Format when completed:

For each segment, separate findings into:
- **Confirmed evidence** — sourced from public pricing data, job listings, or stated WTP in forums/interviews
- **Inferred estimate** — reasoned from adjacent tool pricing and segment size
- **Hypothesis needing validation** — assumption requiring direct buyer interview

---

## 5. Competitive Landscape

| Competitor | What they do well | What they don't solve | How Oli differs | Why Oli can win |
|---|---|---|---|---|
| ChatGPT / OpenAI Agents | [PLR] | [PLR] | [PLR] | [PLR] |
| Claude / Claude Code / Computer Use | [PLR] | [PLR] | [PLR] | [PLR] |
| Google agentic products (Gemini, Workspace agents) | [PLR] | [PLR] | [PLR] | [PLR] |
| Devin / Cognition | [PLR] | [PLR] | [PLR] | [PLR] |
| Lindy | [PLR] | [PLR] | [PLR] | [PLR] |
| Manus-like agents | [PLR] | [PLR] | [PLR] | [PLR] |
| Genspark-like agents | [PLR] | [PLR] | [PLR] | [PLR] |
| Zapier / Make / n8n | [PLR] | [PLR] | [PLR] | [PLR] |
| Cursor / Windsurf / local agentic coding | [PLR] | [PLR] | [PLR] | [PLR] |
| Virtual assistant / automation agencies | [PLR] | [PLR] | [PLR] | [PLR] |

### Oli's Structural Differentiation (hypothesis — to be validated)

- Local-first / hybrid: user controls where data lives
- Model-agnostic: user chooses their model and runtime
- Privacy-preserving by architecture: Oli doesn't train on private data
- Execution-oriented, not chat-oriented: de intención a trabajo terminado
- Auditable: every action logged, every memory traceable
- Shared capability ecosystem without shared private data

---

## 6. Wedge Recommendations

> [PENDING LIVE RESEARCH — rank after segment scoring is complete]

**Wedge template (complete for each candidate):**

```
Mission type:
Target user:
Why it's painful:
Why current tools fail:
Why Oli can be 10x better:
Required integrations:
Required security level:
Pricing hypothesis:
Validation experiment:
```

---

## 7. Interview and Validation Plan

### Discovery Questions (20)

> [PENDING LIVE RESEARCH — generate from persona research]

Seed questions (to expand):
1. Walk me through your ideal workday — what does "done" look like?
2. What is the task you dread most every week?
3. When did you last delegate something to an AI tool? What happened?
4. What tool do you use most for coordinating work across apps?
5. If you had one more hour per day, what would you use it for?

### Willingness to Pay Questions (10)

> [PENDING LIVE RESEARCH]

Seed questions:
1. What tools do you currently pay for to save time?
2. What's the most you've paid for a productivity tool?
3. If Oli saved you 5 hours per week, what is that worth to you?

### Security / Privacy Questions (10)

> [PENDING LIVE RESEARCH]

Seed questions:
1. What data can you NOT send to a third-party AI tool under any circumstances?
2. Has a privacy concern ever stopped you from using an AI tool?
3. Would local processing matter to you? Would you pay more for it?

### Demo Reactions to Test (5)

> [PENDING LIVE RESEARCH]

### Landing Page Messages to A/B Test (5)

> [PENDING LIVE RESEARCH]

---

## 8. Evidence and Sources

> All factual claims in the final research report must be listed here with their source.
> No source = the claim must be marked as a hypothesis.

| Claim | Source | Date | Confidence |
|---|---|---|---|
| [PLR] | [PLR] | [PLR] | [PLR] |

---

## Suboperator Output Contract

When the MarketResearchSuboperator completes this mission, it must return:

```json
{
  "suboperator": "MarketResearchSuboperator",
  "task_id": "market-research-v0.1",
  "status": "complete | partial | blocked",
  "output": {
    "executive_recommendation": {},
    "icp_segments": [],
    "buyer_personas": [],
    "competitive_landscape": [],
    "wedge_recommendations": [],
    "interview_plan": {}
  },
  "evidence": ["list of URLs or source references"],
  "uncertainty_flags": ["list of unverified claims"],
  "recommendations": ["top 3-5 actionable next steps for Oli"],
  "needs_human_approval": true,
  "escalation_reason": null
}
```

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 0.1 | 2026-05-25 | Initial spec created — awaiting live research execution |

---
*This document is maintained by the Oli Execution OS. Updates require MemoryCuratorSuboperator review and Oli approval.*
