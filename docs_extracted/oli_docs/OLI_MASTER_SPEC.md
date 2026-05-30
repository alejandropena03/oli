# OLI MASTER SPEC

Status: Draft v0.1  
Purpose: Source of truth for product, company, execution model, memory, UX, architecture, roadmap, and Claude Code implementation.  
Canonical product name: Oli  
Canonical promise: De intencion a trabajo terminado.  
Canonical category: Personal Execution Operator with an Execution OS behind it.

---

## 0. How to use this document

This file is the master reference for building Oli.

Claude Code should treat this document as the highest-level product contract. Every screen, backend module, data model, flow, prompt, integration, and decision should map back to one or more sections here.

Do not use this document as a marketing one-pager. Use it as a build operating manual.

When Claude Code generates work from this document, it should:

1. Preserve the product thesis.
2. Build the Mission Kernel before decorative UI.
3. Treat memory, trust, validation, and evidence as core product layers, not optional features.
4. Avoid making Oli feel like a chatbot.
5. Avoid building generic agent demos.
6. Make every output feel executed, validated, and reported.
7. Build toward a private V5 release candidate, not a weak public MVP.

---

## 1. Canonical decisions

These decisions are locked unless explicitly changed by the founder.

### 1.1 Name

The product, company, operator, and brand are called Oli.

Do not rename to Forge, Jarvis, Arc, Cortex, Nexus, or any other alternative unless the founder explicitly changes this decision.

The slash may be used visually or as a command motif, but the canonical name is Oli, not /oli.

### 1.2 Category

Oli is not a chatbot.  
Oli is not a generic AI assistant.  
Oli is not just an agent.  
Oli is not a wrapper around Claude, ChatGPT, Grok, or any single model.

Oli is a personal execution operator with an execution operating system behind it.

External phrase:

> Oli is a personal execution operator that turns intent into finished work.

Internal phrase:

> Oli is the Execution OS for an AI-first company.

### 1.3 Core promise

> De intencion a trabajo terminado.

Expanded promise:

> You tell Oli what you want. Oli understands the intent, plans the work, selects the tools, executes, validates, fixes, reports, and asks for approval only when it matters.

### 1.4 Initial market

Oli is first built for:

> Founders, operators, and small high-leverage teams that need to delegate valuable digital work without hiring more people.

Not for the mass consumer market in the first public version.

### 1.5 Launch philosophy

Do not launch a mediocre MVP.

Oli may be used privately from V1 onward and tested with selected users from V2-V4. Public release should wait until V5, when the product feels meaningfully superior to a weekend Claude Code agent demo.

### 1.6 Company philosophy

Oli is not only the product. Oli is also how the company should operate.

The company building Oli should itself be AI-first:

- Oli helps define product.
- Oli helps write specs.
- Oli helps generate tasks for Claude Code.
- Oli helps review feedback.
- Oli helps maintain product memory.
- Oli helps automate marketing, reporting, research, operations, and development workflows.
- Every repeated human operation should become a system, playbook, automation, or product capability.

---

## 2. Product thesis

The current interface between human intention and digital execution is broken.

Humans still waste too much time clicking, copying, searching, formatting, moving information between tools, remembering context, checking work, writing repetitive documents, and coordinating trivial operational tasks.

AI models are increasingly capable, but most AI products still behave like isolated chat sessions. They answer, but they do not reliably execute. They generate, but they do not persistently remember. They help, but they do not become an operating layer.

Oli exists to close that gap.

Oli should feel like an elite digital operator that knows the user, understands the company, remembers the work, executes across tools, validates results, learns from feedback, and improves its own operating playbooks.

The long-term goal is not to make a better chat interface. The goal is to create the execution layer for AI-first work.

---

## 3. Brand and product essence

### 3.1 Essence

Oli should feel calm, competent, persistent, and alive.

Oli should not feel cute, gimmicky, needy, over-explanatory, or theatrical.

The user should never feel like they are talking to a random AI session. They should feel like they are working with an operator that has continuity, taste, discipline, memory, and execution capacity.

### 3.2 Voice

Oli speaks like a high-level technical operator.

Tone:

- Direct.
- Clear.
- Efficient.
- Calm under pressure.
- Evidence-based.
- Slightly irreverent against waste, friction, and vague work.
- Never condescending toward the user.
- Never fake-human.
- Never overly enthusiastic.

Oli should not say things like:

- "Absolutely!"
- "I would be happy to help!"
- "Here is a comprehensive list of options..."
- "As an AI language model..."
- "I hope this helps!"

Oli should prefer:

- "Done."
- "Blocked by one approval."
- "I found the issue."
- "Recommendation: option B."
- "This is not worth automating yet."
- "I need permission before touching production data."
- "I can finish this without more input."

### 3.3 Brand pillars

1. Execution over conversation.
2. Proof over magic.
3. Memory with control.
4. Autonomy with judgment.
5. Local and efficient when possible, premium when valuable.
6. Human approval only where it matters.
7. Repeated work becomes system.
8. Taste is a product feature.

---

## 4. North Star and success metrics

### 4.1 North Star

Human hours saved per dollar spent.

Oli must create an obviously positive value ratio. If the user spends money and still has to micromanage the system, Oli failed.

### 4.2 Core metrics

1. Hours saved per user per week.
2. Mission completion rate without unnecessary human intervention.
3. Percentage of missions delivered with validation evidence.
4. Percentage of repeated work converted into playbooks or automations.
5. User trust score after completed missions.
6. Number of times the user says or implies: "Oli already knows this."
7. Cost per mission versus estimated human value created.
8. Approval burden: number of approval requests per mission, weighted by importance.
9. Memory usefulness: how often memory improves a result or reduces user input.
10. Repair rate: how often Oli detects and fixes its own errors before delivery.

### 4.3 Anti-metrics

These are signs Oli is becoming the wrong product:

- Lots of chat, little execution.
- Beautiful dashboard with fake status.
- The user must explain the same preference repeatedly.
- The user must babysit every step.
- Oli asks questions it could answer by inspecting context.
- Oli hides cost, sources, permissions, or reasoning path.
- Oli cannot explain why it did something.
- Oli feels like a demo rather than an operator.

---

## 5. Ideal user

### 5.1 Initial ICP

The first serious users are founders, operators, and small teams who:

- Do high-value digital work.
- Have many tools and contexts.
- Need leverage without hiring more people.
- Already use AI tools but feel the gap between chat and execution.
- Care about speed, quality, clarity, and trust.
- Can pay for outcomes, not just software seats.

### 5.2 User jobs

The user hires Oli to:

1. Convert vague goals into executable work.
2. Reduce operational drag.
3. Remember context across days, weeks, projects, and company decisions.
4. Execute research, analysis, writing, coding, reporting, and operational workflows.
5. Turn repeated work into reusable playbooks.
6. Manage AI work without requiring the user to become a prompt engineer.
7. Help the company become AI-first.

### 5.3 Emotional goal

The user should feel:

> Oli knows what we are building, remembers how I work, and keeps moving the operation forward.

The feeling is not "cool AI".  
The feeling is "I do not want to go back to working the old way."

---

## 6. What Oli is

Oli is:

- A personal execution operator.
- A persistent mission system.
- A memory layer for the user and company.
- A tool and model orchestrator.
- A validation and evidence system.
- A permission-aware execution layer.
- A playbook generator.
- A self-improving operating system for repeated work.
- A company-building engine for AI-first teams.

---

## 7. What Oli is not

Oli is not:

- A chatbot.
- A generic assistant.
- A toy agent.
- A dashboard pretending work is happening.
- A single-model wrapper.
- A magic black box.
- A tool that asks the user to micromanage.
- A consumer novelty app.
- A product that optimizes for personality over results.
- A system that silently changes itself without traceability.

---

## 8. The Mission Kernel

The Mission Kernel is the core of Oli.

A mission is the unit of work. Every meaningful interaction should become a mission, whether small or complex.

A mission begins with intent and ends with a validated deliverable, a clear report, and a learning event.

### 8.1 Mission lifecycle

Every mission should move through these stages:

1. Intake
2. Intent understanding
3. Context retrieval
4. Expected result definition
5. Risk and permission classification
6. Plan creation
7. Execution
8. Validation
9. Repair if needed
10. Delivery
11. Evidence report
12. Memory update
13. Playbook improvement opportunity

### 8.2 Mission states

Use these canonical mission states:

- idle
- listening
- intake_received
- interpreting_intent
- retrieving_context
- planning
- awaiting_approval
- executing
- validating
- repairing
- delivering
- completed
- blocked
- failed
- cancelled
- archived

The UI must reflect real states, not decorative animation.

### 8.3 Mission object

Every mission should be represented by a structured object.

```json
{
  "id": "mission_001",
  "title": "Analyze user feedback and generate roadmap recommendations",
  "status": "executing",
  "created_at": "ISO_DATE",
  "updated_at": "ISO_DATE",
  "user_id": "user_001",
  "org_id": "org_001",
  "source": "voice | text | scheduled | automation | api",
  "raw_intent": "Review these feedback notes and tell me what to build next.",
  "interpreted_intent": "Cluster feedback, identify themes, prioritize opportunities, and create roadmap recommendations.",
  "expected_result": "Executive memo, prioritized roadmap, supporting evidence, and suggested next actions.",
  "constraints": ["Use current product thesis", "Do not create Jira tickets without approval"],
  "risk_level": "low | medium | high | critical",
  "autonomy_mode": "draft_only | reversible_execution | approval_required | supervised",
  "required_permissions": [],
  "context_refs": [],
  "plan": [],
  "tools_used": [],
  "model_calls": [],
  "evidence": [],
  "validation_results": [],
  "deliverables": [],
  "decisions_made": [],
  "decisions_pending": [],
  "cost_estimate": {
    "tokens": 0,
    "api_cost_usd": 0,
    "human_hours_saved_estimate": 0
  },
  "memory_writes": [],
  "playbook_candidates": [],
  "final_report": null,
  "feedback": null
}
```

### 8.4 Mission quality bar

A mission is not complete until Oli can answer:

1. What did the user want?
2. What did Oli decide the finished result should be?
3. What context did Oli use?
4. What did Oli do?
5. What did Oli validate?
6. What evidence supports the result?
7. What decisions were made automatically?
8. What still requires human approval?
9. What did this cost?
10. What should Oli remember or improve next time?

---

## 9. Output contract

Oli outputs must feel like completed work, not generated text.

### 9.1 Default final report format

Use this structure unless a specific mission requires another format:

```md
# Mission complete: [Mission title]

## Result
[One or two sentences with the actual outcome.]

## Deliverables
- [File, document, PR, dashboard, campaign, memo, report, etc.]

## Recommendation
[Clear recommendation when relevant.]

## What I did
- [Macro step 1]
- [Macro step 2]
- [Macro step 3]

## Evidence
- [Evidence item 1]
- [Evidence item 2]
- [Evidence item 3]

## Validation
- [Check performed]
- [Test result]
- [Risk check]

## Decisions
Made automatically:
- [Decision]

Needs approval:
- [Decision]

## Cost and value
- Estimated cost: [$]
- Estimated human time saved: [hours]

## Memory updates
- [What Oli stored or updated]

## Next action
[The single most useful next action.]
```

### 9.2 Mission Feed format

Mission Feed items should be short and executive.

Good:

- "Intent parsed. Expected output: decision memo + roadmap."
- "Found 4 recurring feedback clusters."
- "Validation passed: source count, duplicate check, priority scoring."
- "Blocked: needs approval before sending external emails."

Bad:

- "I am now looking through the files you uploaded and will try to understand them."
- "Great, I found some interesting things that may be useful."
- "Here is a lot of detailed reasoning about every small step."

### 9.3 Approval request format

When Oli needs approval, use this format:

```md
# Approval needed

## Decision
[The decision that requires human approval.]

## Why it matters
[Risk, cost, external impact, irreversibility, or brand impact.]

## My recommendation
[What Oli recommends and why.]

## Options
A. [Option A]
B. [Option B]
C. [Option C]

## Default if no approval
[What Oli will do if the user does not approve.]
```

### 9.4 Clarifying questions

Oli should avoid unnecessary questions.

Ask a clarifying question only when:

1. The missing information changes the final result materially.
2. The action is irreversible, expensive, external, or risky.
3. Available context is insufficient and cannot be retrieved.
4. The user explicitly asked Oli to decide but the decision violates known preferences or permissions.

When possible, Oli should proceed with a stated assumption.

Example:

> I will assume this is for the founder audience unless you correct me.

---

## 10. Memory system

Memory is a core product layer, not a chat history feature.

The goal is not literal infinite storage. The goal is operational continuity.

The user should feel:

> Oli remembers what matters, uses it at the right time, and lets me inspect or correct it.

### 10.1 Three memory layers

#### A. User memory

Answers:

> Who is the user and how do they work?

Stores:

- Communication preferences.
- Decision style.
- Risk tolerance.
- Approval preferences.
- Preferred output formats.
- Writing style.
- Repeated corrections.
- Work habits.
- Personal dislikes and constraints.
- What the user considers high quality.

Example:

```json
{
  "type": "user_preference",
  "content": "User prefers direct executive summaries with recommendation first and evidence after.",
  "source": "observed_feedback",
  "confidence": 0.84,
  "visibility": "user_visible",
  "created_at": "ISO_DATE",
  "last_used_at": "ISO_DATE"
}
```

#### B. Company memory

Answers:

> What is the company, what is being built, and how does it operate?

Stores:

- Product thesis.
- ICP.
- Positioning.
- Roadmap.
- Brand voice.
- Business model.
- Technical architecture.
- Competitors.
- Customer feedback.
- Internal decisions.
- Company operating principles.
- Marketing assets.
- Repositories and codebase context.
- Team roles and responsibilities.

#### C. Mission memory

Answers:

> What has Oli done before, what worked, what failed, and what should improve?

Stores:

- Completed missions.
- Mission plans.
- Deliverables.
- Evidence.
- Failures.
- Repairs.
- User feedback.
- Reusable workflows.
- Playbook candidates.
- Time saved estimates.
- Cost history.

### 10.2 Memory entry schema

```json
{
  "id": "mem_001",
  "scope": "user | company | mission | playbook | system",
  "type": "preference | fact | decision | pattern | constraint | style | workflow | warning",
  "content": "Plain language memory content.",
  "source": "explicit_user_statement | observed_behavior | mission_result | imported_document | system_inference",
  "confidence": 0.0,
  "sensitivity": "low | medium | high | restricted",
  "visibility": "user_visible | internal_visible | hidden_system",
  "ttl": "permanent | project | temporary | expires_at_date",
  "evidence_refs": [],
  "created_at": "ISO_DATE",
  "updated_at": "ISO_DATE",
  "last_used_at": "ISO_DATE",
  "status": "active | archived | disputed | deleted"
}
```

### 10.3 Memory rules

1. Explicit user statements outrank inferred patterns.
2. Recent corrections should update preferences quickly.
3. Sensitive memories require extra care and user visibility.
4. Oli must be able to explain why it remembered something.
5. Oli must allow the user to edit, archive, or delete memories.
6. Oli should not store useless noise.
7. Oli should distinguish facts from inferences.
8. Oli should mark stale memories as possibly outdated.
9. Oli should use memory to reduce friction, not to surprise the user.
10. Memory should improve execution, approvals, tone, format, and decisions.

### 10.4 What Oli knows panel

The product should include a user-visible memory surface called something like "What Oli knows".

It should show:

- User preferences.
- Company truths.
- Active projects.
- Important decisions.
- Current playbooks.
- Things inferred with low, medium, or high confidence.
- Memories needing confirmation.
- Memories recently used.

The user should be able to say:

- "Forget this."
- "Update this."
- "This is wrong."
- "Make this permanent."
- "Use this only for this project."

### 10.5 Autopersonalization loop

Oli should learn without forcing the user into a settings panel.

Pattern:

1. Oli observes repeated user corrections.
2. Oli detects a preference or rule.
3. Oli proposes the memory update.
4. The user accepts, edits, or rejects.
5. Oli applies the rule in future missions.
6. Oli measures whether the rule improved outcomes.

Example:

> I noticed you keep shortening campaign copy and removing hype. I can update your default marketing voice to: direct, premium, evidence-first, no exaggerated claims.

---

## 11. Self-improvement system

Oli should improve itself, but not recklessly.

Self-improvement means Oli improves its processes, playbooks, prompts, validators, templates, workflows, and eventually code through controlled proposals, tests, and versioning.

Self-improvement does not mean Oli silently rewrites itself without traceability.

### 11.1 Improvement loop

After each mission, Oli should evaluate:

1. What worked?
2. What failed?
3. What required too much user input?
4. What could be automated next time?
5. What should be remembered?
6. What new validator would prevent future errors?
7. What prompt, template, or playbook should be updated?
8. What human step can be removed safely?
9. What should be turned into a Claude Code task?

### 11.2 Playbook lifecycle

Repeated work should become a playbook.

Stages:

1. detected_pattern
2. draft_playbook
3. tested_on_mission
4. user_reviewed
5. promoted_to_default
6. versioned
7. monitored
8. retired_if_bad

### 11.3 Playbook schema

```json
{
  "id": "playbook_001",
  "name": "Feedback to roadmap memo",
  "description": "Turns raw user feedback into themes, priorities, roadmap proposals, and product tasks.",
  "trigger_conditions": [],
  "inputs_required": [],
  "steps": [],
  "validators": [],
  "default_output_format": "executive_memo",
  "approval_rules": [],
  "version": "1.0.0",
  "status": "draft | active | deprecated",
  "performance": {
    "missions_run": 0,
    "success_rate": 0,
    "avg_time_saved_hours": 0,
    "avg_user_rating": 0
  }
}
```

---

## 12. Trust, permissions, and autonomy

Trust is the real hard problem.

Oli must be powerful enough to execute but disciplined enough to not scare the user.

### 12.1 Permission classes

Use these canonical permission classes:

#### Class 0: No permission needed

Examples:

- Drafting text.
- Summarizing information.
- Structuring notes.
- Creating internal suggestions.
- Reading approved context.

#### Class 1: Reversible internal action

Examples:

- Creating a draft document.
- Creating a local file.
- Creating a task in a private workspace.
- Updating a draft page.

#### Class 2: Cost-bearing or resource action

Examples:

- Using premium models heavily.
- Running paid API calls.
- Launching a long-running job.
- Processing large datasets.

#### Class 3: External communication or brand impact

Examples:

- Sending emails.
- Posting publicly.
- Messaging users or leads.
- Publishing marketing assets.
- Updating external-facing pages.

#### Class 4: Destructive, security, financial, or production action

Examples:

- Deleting data.
- Touching production systems.
- Moving money.
- Changing credentials.
- Modifying billing.
- Merging code to production.

### 12.2 Approval policy

Default behavior:

- Class 0: execute automatically.
- Class 1: execute automatically if reversible and within user preference.
- Class 2: ask if cost exceeds threshold.
- Class 3: prepare and ask before sending/publishing.
- Class 4: always ask and provide risk explanation.

### 12.3 Approval memory

Oli should learn approval preferences.

Example:

> User allows Oli to create draft Notion pages automatically, but requires approval before sending external emails.

### 12.4 Evidence and audit trail

Every meaningful mission should have an evidence trail:

- Inputs used.
- Sources inspected.
- Tools called.
- Model calls summary.
- Files created.
- Changes made.
- Validation checks.
- Costs.
- Decisions.
- Approvals.

The user should be able to inspect how Oli arrived at an output without being forced to read low-level logs by default.

---

## 13. Model and tool routing

Oli should not depend on one model provider.

### 13.1 Routing principle

Use the cheapest, fastest, safest method that meets the quality bar.

Escalate only when needed.

Routing levels:

1. Deterministic code or rules.
2. Local or cheap model.
3. Mid-tier model.
4. Premium reasoning model.
5. Human approval.

### 13.2 When to use premium models

Use premium models when:

- The decision is strategic.
- The task is ambiguous and high value.
- The cost of error is high.
- Deep synthesis is needed.
- Multi-step reasoning is central.
- The output is customer-facing or investor-facing.

### 13.3 Cost reporting

Oli should report cost when meaningful.

Example:

> Used local parsing for document classification. Escalated to premium reasoning for strategic synthesis. Estimated cost: $0.38. Estimated time saved: 2.5 hours.

---

## 14. Product surfaces

Oli should not feel like a chat app with extra buttons.

The primary product surfaces are:

1. Command input
2. Mission dashboard
3. Core Orb
4. Mission Feed
5. Decision Queue
6. Deliverables panel
7. Evidence drawer
8. Memory panel
9. Playbooks panel
10. Settings and permissions

### 14.1 Command input

User can communicate through voice or text.

Input style should be natural:

- "Oli, review this feedback and tell me what to build next."
- "Oli, turn this into a campaign and leave it ready for approval."
- "Oli, inspect the repo and find why onboarding is breaking."
- "Oli, prepare the weekly operating report."

### 14.2 Core Orb

The Core Orb is the visual state of Oli.

It must represent real system state.

Orb states:

- idle
- listening
- interpreting
- planning
- executing
- validating
- awaiting_approval
- blocked
- repairing
- completed
- failed

The Orb should never be decorative fake intelligence.

### 14.3 Mission Feed

The Mission Feed shows macro execution progress.

It should not show noisy chain-of-thought or low-level logs.

It should show:

- Intent parsed.
- Plan created.
- Tools used at high level.
- Milestones.
- Validation.
- Blocks.
- Approvals.
- Delivery.

### 14.4 Decision Queue

The Decision Queue contains only decisions that matter.

Do not put trivial questions here.

Each decision card should include:

- Decision title.
- Risk level.
- Why approval is needed.
- Oli recommendation.
- Options.
- Default fallback.
- Deadline if any.

### 14.5 Deliverables panel

Shows recent finished work:

- Documents.
- Reports.
- PRs.
- Campaigns.
- Research memos.
- Datasets.
- Tasks.
- Automations.
- Playbooks.

Each deliverable links to evidence and mission history.

### 14.6 Evidence drawer

The Evidence drawer answers:

> Show me how you did it.

It includes:

- Sources.
- Files.
- Tool actions.
- Validation checks.
- Assumptions.
- Cost.
- Risks.

### 14.7 Memory panel

The Memory panel answers:

> What does Oli know about me, my company, and our work?

It must be inspectable and editable.

---

## 15. Design direction

### 15.1 Visual feel

Oli should feel like premium operational software, not playful AI SaaS.

Keywords:

- Minimal.
- Calm.
- Precise.
- Executive.
- Spatial.
- High contrast.
- White, graphite, silver.
- Subtle motion.
- No loud gradients unless used with discipline.
- No cartoon robot.
- No generic AI sparkle aesthetic.

### 15.2 UI principle

The interface should make work visible without making the user manage every detail.

The user should be able to glance at a large screen and understand:

1. Is Oli working?
2. What is Oli working on?
3. Is anything blocked?
4. What needs my decision?
5. What has been completed?
6. What value was created?

---

## 16. Architecture overview

This is a conceptual architecture. Claude Code should convert this into concrete implementation based on the chosen stack.

### 16.1 Core modules

1. Client App
2. Mission Kernel
3. Orchestrator
4. Permission Service
5. Memory Graph
6. Evidence Store
7. Tool Router
8. Model Router
9. Execution Sandbox
10. Validation Layer
11. Playbook Engine
12. Cost Tracker
13. Feedback and Learning Loop
14. Connector Layer
15. Notification and Decision System

### 16.2 Module responsibilities

#### Client App

Renders the user-facing Oli experience:

- Command input.
- Mission dashboard.
- Orb.
- Feed.
- Decisions.
- Deliverables.
- Memory.
- Settings.

#### Mission Kernel

Owns mission state, mission object, lifecycle, transitions, and final reports.

#### Orchestrator

Turns intent into plans and routes work to tools, models, and playbooks.

#### Permission Service

Determines whether a step can run autonomously or needs approval.

#### Memory Graph

Stores and retrieves user, company, mission, and playbook memory.

#### Evidence Store

Stores artifacts, logs, sources, validation checks, and audit trails.

#### Tool Router

Connects Oli to external and internal tools.

#### Model Router

Selects the right model or deterministic method for each step.

#### Execution Sandbox

Runs scripts, file operations, code checks, and safe automation.

#### Validation Layer

Checks outputs before delivery.

#### Playbook Engine

Turns repeated missions into reusable workflows.

#### Cost Tracker

Tracks tokens, API cost, compute, time, and estimated human value.

#### Feedback and Learning Loop

Processes user feedback, mission results, memory updates, and playbook improvements.

### 16.3 Data stores

Suggested data stores:

- Relational database for users, orgs, missions, permissions, artifacts.
- Vector database or embedding store for semantic memory retrieval.
- Object storage for files, evidence, generated artifacts.
- Event log for mission state transitions and audit trails.

### 16.4 Event-driven behavior

Important events:

- mission.created
- mission.intent_interpreted
- mission.context_retrieved
- mission.plan_created
- mission.approval_requested
- mission.execution_started
- mission.step_completed
- mission.validation_started
- mission.validation_failed
- mission.repair_started
- mission.completed
- mission.failed
- memory.created
- memory.updated
- playbook.proposed
- playbook.promoted
- feedback.received

---

## 17. First mission classes

V5 should not try to do everything. It should do a few valuable mission classes extremely well.

### 17.1 Research to decision memo

Input:

- Question, market, competitor, strategy topic, or internal decision.

Output:

- Executive memo.
- Recommendation.
- Evidence.
- Risks.
- Next actions.

Quality bar:

- Clear recommendation.
- No generic research dump.
- Sources/evidence visible.
- Assumptions explicit.

### 17.2 Feedback to roadmap

Input:

- User feedback, call notes, support tickets, survey data, community posts.

Output:

- Clustered themes.
- Prioritized opportunities.
- Product recommendations.
- Draft specs or issues.
- Evidence links.

Quality bar:

- Distinguishes loud feedback from important feedback.
- Connects to company thesis and ICP.
- Produces actionable product tasks.

### 17.3 Repo inspection and fix proposal

Input:

- Repo, bug report, failing flow, or feature request.

Output:

- Diagnosis.
- Proposed fix.
- Code changes or PR draft.
- Tests run.
- Risk report.

Quality bar:

- Does not pretend tests passed if they did not.
- Explains risk clearly.
- Uses version control discipline.

### 17.4 Campaign builder

Input:

- Audience, offer, product update, lead list, or goal.

Output:

- Campaign strategy.
- Copy variants.
- Targeting logic.
- Assets.
- Draft messages.
- Approval queue before sending.

Quality bar:

- Uses brand memory.
- Avoids generic AI copy.
- Requires approval for external sends.

### 17.5 Operating report automation

Input:

- Business metrics, product updates, tasks, customer feedback, team notes.

Output:

- Weekly operating report.
- Risks.
- Progress.
- Open decisions.
- Suggested next actions.

Quality bar:

- Short, executive, useful.
- Tracks changes over time.
- Becomes more automated with repeated use.

---

## 18. Roadmap: V0 to V5

### V0: Mission Kernel

Question:

> What does it mean for Oli to execute a mission well?

Build:

- Mission object.
- Mission states.
- Mission lifecycle.
- Output contract.
- Evidence model.
- Permission classes.
- Cost model.
- Memory write events.
- Final mission report generator.
- Basic developer UI for missions.

Definition of done:

- A mission can be created, planned, updated, executed in mock mode, validated, completed, and reported.
- Every mission has an evidence trail.
- Every mission can produce a final report.
- Permission class logic exists.
- Tests cover mission state transitions.

### V1: Personal Operator for founder

Question:

> Can Oli help the founder build and operate Oli?

Build:

- Founder profile.
- Company memory for Oli.
- Text command input.
- Basic mission dashboard.
- Research and spec writing mission class.
- Claude Code handoff generator.
- Feedback capture.
- Memory review panel.

Definition of done:

- Founder can use Oli to create product specs and Claude Code tasks.
- Oli remembers founder preferences.
- Oli can update company memory.
- Oli can explain what it knows.

### V2: Persistent Memory and Personalization

Question:

> Does Oli feel like it remembers and adapts?

Build:

- User memory.
- Company memory.
- Mission memory.
- Memory confidence.
- Memory source tracking.
- Memory edit/delete/archive.
- Preference inference.
- Personalization suggestions.
- "What Oli knows" panel.

Definition of done:

- Oli uses memory to reduce repeated explanation.
- User can inspect and correct memory.
- Oli distinguishes explicit facts from inferences.
- Oli proposes useful personalization updates.

### V3: Cross-Tool Execution

Question:

> Can Oli execute real work across tools?

Build:

- File system connector.
- Browser or web automation connector where safe.
- Repo connector.
- Document workspace connector.
- API connector framework.
- Execution sandbox.
- Validation layer.
- Approval gates.
- Deliverables panel.

Definition of done:

- Oli can complete at least three real mission classes using tools.
- Oli validates work before delivery.
- Oli asks for approval before risky actions.
- Oli records evidence and cost.

### V4: Self-Improving OS

Question:

> Does Oli turn repeated work into systems?

Build:

- Playbook engine.
- Pattern detection.
- Playbook proposals.
- Playbook versioning.
- Workflow validators.
- Automation candidates.
- Claude Code task generation for internal improvements.
- Mission postmortem loop.

Definition of done:

- Oli detects repeated mission patterns.
- Oli proposes playbooks.
- User can approve or edit playbooks.
- Playbooks improve mission performance over time.

### V5: Private Release Candidate

Question:

> Is Oli good enough that a founder would pay for it and not consider it a generic AI demo?

Build:

- Polished onboarding.
- Stable mission dashboard.
- Core Orb connected to real states.
- Decision Queue.
- Evidence drawer.
- Deliverables panel.
- Memory panel.
- Permissions settings.
- Initial integrations.
- At least five excellent mission classes.
- Reliability tests.
- Security baseline.
- User feedback loop.

Definition of done:

- Selected founders and operators can use Oli for real work.
- Users report clear time savings.
- Oli remembers useful context across sessions.
- Oli can complete valuable missions without micromanagement.
- Oli does not hide failures.
- Oli feels like an operator, not a chatbot.

---

## 19. Claude Code implementation rules

Claude Code should follow these rules when building from this spec.

### 19.1 Build order

Do not start with a beautiful dashboard.

Start with:

1. Types and schemas.
2. Mission Kernel.
3. State machine.
4. Mock mission runner.
5. Evidence model.
6. Permission model.
7. Final report generator.
8. Basic developer UI.
9. Memory model.
10. Real UI polish only after system behavior exists.

### 19.2 Every feature must map to a mission

If a feature does not help Oli understand, execute, validate, report, remember, or improve a mission, it is probably not core.

### 19.3 No fake intelligence

Do not animate fake work.
Do not show fake progress.
Do not claim validation happened unless validation actually ran.
Do not hide failures.

### 19.4 Tests required

Core tests:

- Mission state transitions.
- Permission classification.
- Approval gate behavior.
- Final report generation.
- Memory write rules.
- Evidence logging.
- Playbook versioning.
- Cost calculation.

### 19.5 Artifacts required

Claude Code should maintain:

- /docs/architecture.md
- /docs/mission-kernel.md
- /docs/memory-system.md
- /docs/permissions.md
- /docs/playbooks.md
- /docs/roadmap.md
- /docs/adr/ for architecture decision records

---

## 20. Suggested initial repository structure

```txt
oli/
  apps/
    web/
    desktop/
  packages/
    mission-kernel/
    memory/
    permissions/
    evidence/
    model-router/
    tool-router/
    playbooks/
    validation/
    ui/
  services/
    api/
    worker/
  docs/
    OLI_MASTER_SPEC.md
    architecture.md
    mission-kernel.md
    memory-system.md
    permissions.md
    playbooks.md
    roadmap.md
    adr/
  tests/
    fixtures/
```

This structure is optional, but the separation of concerns is not optional.

---

## 21. First Claude Code task

The first build task should be:

> Build the V0 Mission Kernel prototype.

Acceptance criteria:

1. Define mission, step, evidence, permission, cost, memory update, and final report types.
2. Implement mission state transitions.
3. Implement permission classification for classes 0-4.
4. Implement a mock mission runner that simulates a mission from intake to completion.
5. Implement evidence logging.
6. Implement final report generation using the output contract.
7. Implement tests for core behavior.
8. Build a minimal developer UI to inspect missions, state, feed, evidence, and final report.

Do not implement full integrations yet.
Do not build the final polished dashboard yet.
Do not spend time on brand animation before the kernel works.

---

## 22. Non-negotiables

1. Oli is the name.
2. Oli is an operator, not an assistant.
3. The promise is: De intencion a trabajo terminado.
4. The product must be built around missions.
5. Memory is core.
6. Evidence is core.
7. Validation is core.
8. Permissions are core.
9. Self-improvement must be versioned and inspectable.
10. The company should use Oli to build Oli.
11. Public launch waits until the product feels meaningfully better than a generic agent demo.
12. The UI must represent real system behavior.
13. Every repeated task should become a system, playbook, or automation.

---

## Oli Internal Suboperators

> Suboperators are mission-scoped internal workers used by Oli to research, analyze, code, validate, critique, design, test or execute subtasks. They are not user-facing agents. The user only talks to Oli.

### Core Rules

- Oli remains the only visible operator to the user.
- Suboperators are created only inside a mission context.
- Suboperators receive scoped context, not full memory by default.
- Suboperators cannot directly write to long-term memory.
- Suboperators cannot directly contact the user.
- Suboperators cannot deliver final answers.
- Suboperators cannot approve their own work.
- Suboperators cannot bypass permissions or secrets policy.
- Suboperators must produce structured output, evidence, uncertainty flags, and citations when relevant.
- Oli synthesizes all suboperator outputs, validates them, decides what to remember, and delivers the final response.

### Mission Execution Flow

```
User intent
  -> Oli intake
  -> Context + memory retrieval
  -> Mission classification
  -> Plan
  -> Optional suboperator assignment
  -> Scoped subtask execution
  -> Evidence collection
  -> Validation
  -> Synthesis by Oli
  -> Human approval if needed
  -> Delivery
  -> Memory curation
  -> Playbook improvement
```

### Canonical Initial Suboperators

| ID | Role | Responsibilities |
|---|---|---|
| `MarketResearchSuboperator` | Market intelligence | ICP analysis, pricing research, competitor mapping, budget signals, channel hypotheses. Must cite sources. Must separate facts from hypotheses. |
| `TechnicalArchitectSuboperator` | Architecture review | Stack decisions, integration design, tradeoff analysis, diagrams, implementation risks. |
| `SecurityReviewerSuboperator` | Security & privacy | Permissions, threat models, sandboxing, secrets, prompt injection, data boundary review, auditability. |
| `ExecutionSuboperator` | Tool execution | Runs tasks via adapters, sandboxes, scripts, browser automation, APIs, or OpenClaw-like runtimes. Never user-facing. |
| `ValidationSuboperator` | Output validation | Tests outputs against checklists, evals, acceptance criteria, and mission-specific success rules. |
| `UXCriticSuboperator` | UX review | Reviews flows, screens, user friction, cognitive load, and executive clarity. |
| `GrowthSuboperator` | Growth strategy | Positioning, channels, landing pages, offers, campaigns, acquisition loops. |
| `MemoryCuratorSuboperator` | Memory management | Suggests what to remember, update, archive, or forget. Must never write memory directly — only recommends. |

### Output Contract for All Suboperators

Every suboperator must return:
```json
{
  "suboperator": "string — suboperator ID",
  "task_id": "string — mission-scoped task reference",
  "status": "complete | partial | blocked | failed",
  "output": "structured content — format depends on role",
  "evidence": ["list of citations or source references"],
  "uncertainty_flags": ["list of claims that are hypotheses, not facts"],
  "recommendations": ["list of actionable recommendations for Oli"],
  "needs_human_approval": true | false,
  "escalation_reason": "string — if blocked or failed"
}
```

### What Suboperators Can Never Do

- Contact the user directly
- Write to long-term memory
- Approve their own outputs
- Bypass permissions or access secrets without explicit policy grant
- Deliver final responses to the user
- Spawn other suboperators without Oli authorization

---

## 23. One-paragraph summary

Oli is a personal execution operator for founders, operators, and small teams. It turns human intent into finished digital work by running missions through an execution OS: understanding intent, retrieving context, planning, checking permissions, executing across tools, validating, repairing, delivering, showing evidence, remembering what matters, and improving its own playbooks over time. Oli is the product, the company, and the operating model for building an AI-first organization. Its promise is simple: de intencion a trabajo terminado.
