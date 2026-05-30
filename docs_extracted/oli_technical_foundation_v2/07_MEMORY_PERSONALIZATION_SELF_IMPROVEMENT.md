# 07 - Memory, Personalization, and Self-Improvement

## Purpose

Oli should not feel like a chat session.

Oli should feel like continuity.

The user should feel:

> Oli knows how I work, what we are building, what happened before, what I trust it to do, and how to improve the next mission.

## Memory types

### 1. User Memory

Answers:

> How does this person work?

Includes:

- communication style
- preferred output format
- decision style
- approval preferences
- risk tolerance
- recurring corrections
- working hours/preferences
- sensitive areas

### 2. Company Memory

Answers:

> What is this company and how does it operate?

Includes:

- vision
- product
- ICP
- positioning
- roadmap
- pricing
- competitors
- brand voice
- assets
- repositories
- stack
- docs
- metrics
- active projects

### 3. Mission Memory

Answers:

> What has Oli done and learned?

Includes:

- mission objective
- plan
- tools used
- models used
- artifacts
- failures
- repairs
- validation result
- user feedback
- follow-up actions

### 4. Decision Memory

Answers:

> What decisions were made and why?

Includes:

- decision
- alternatives
- rationale
- date
- owner
- consequences
- reversal conditions

### 5. Playbook Memory

Answers:

> What repeated workflow can be reused?

Includes:

- trigger
- steps
- tools
- validators
- approvals
- expected artifacts
- known failure modes
- version history

## Memory item schema

```json
{
  "id": "mem_001",
  "scope": "user|organization|project|mission",
  "type": "preference|fact|decision|playbook|lesson|style|policy",
  "title": "User prefers executive summaries first",
  "content": "When delivering strategic analysis, start with recommendation and rationale before details.",
  "source_type": "explicit_user|mission_feedback|inference|document|system",
  "source_id": "mission_001",
  "confidence": 0.82,
  "sensitivity": "internal",
  "status": "active|stale|archived|disputed",
  "tags": ["style", "delivery"],
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

## Memory write policy

- Explicit user statements can become high-confidence memory.
- Inferred memory starts medium/low confidence.
- Untrusted docs cannot create high-confidence memory by themselves.
- Sensitive memory may require confirmation.
- Memory updates should be explainable.
- Memory can be edited, archived, or deleted by user.

## What Oli Knows panel

The product should include a user-visible memory surface:

- What Oli knows about me
- What Oli knows about the company
- What Oli learned from recent missions
- What Oli is unsure about
- What Oli wants confirmation on
- What Oli should forget

## Personalization engine

Oli should adapt:

- output length
- approval frequency
- preferred artifacts
- model routing preferences
- risk thresholds
- writing style
- mission planning depth
- evidence verbosity
- dashboard defaults

But personalization must not become invisible manipulation.

Oli should expose important changes:

```text
I noticed you usually reject long strategy memos and prefer a direct recommendation first. I can make that the default for future strategy outputs.
```

## Self-improvement loop

Oli should improve playbooks, validators, prompts, routing, and workflows.

Self-improvement does not mean uncontrolled self-modification.

Allowed improvement targets:

- playbook steps
- prompt templates
- validation criteria
- routing policies
- output templates
- mission classification rules
- automation proposals
- Claude Code task specs
- documentation

High-risk improvement targets:

- production code changes
- permission rules
- credential handling
- security policies

High-risk changes require approval, tests, and versioning.

## After Action Review

At the end of each mission, Oli should evaluate:

- Did it finish the objective?
- Which validators passed/failed?
- What user feedback occurred?
- What memory candidates were generated?
- What playbook can be improved?
- What should be a regression test?
- Was premium spend justified?
- What should be automated next time?

## Playbook versioning

Every playbook update should include:

```json
{
  "playbook_id": "pb_weekly_report",
  "from_version": "1.2",
  "to_version": "1.3",
  "change_summary": "Moved metrics table before narrative summary based on 3 user edits.",
  "evidence_missions": ["mission_102", "mission_119", "mission_131"],
  "requires_user_approval": false
}
```

## Moat from memory

Memory becomes defensible when it is:

- accurate
- useful during execution
- visible
- editable
- permissioned
- linked to outcomes
- converted into playbooks
- used to reduce future friction

## V0 build target

Implement:

- memory_items table
- source/confidence/sensitivity fields
- explicit memory write endpoint
- memory retrieval for mission planning
- memory candidates after mission completion
- no direct executor memory writes

V1/V2:

- What Oli Knows panel
- edit/delete/archive memory
- decision memory
- playbooks
- personalization suggestions

V3/V4:

- self-improving playbook engine
- eval-generated regression tests
- routing improvements from mission history
