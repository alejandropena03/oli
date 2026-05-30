# 11 - Roadmap V0 to V5

## Roadmap philosophy

Do not publicly launch until Oli is meaningfully better than a weekend Claude Code agent.

But do expose V1-V4 privately to real users.

Private use is not launch. It is controlled reality.

## V0 - Mission Kernel Foundation

Goal:

> Define and implement the core mission system.

Build:

- repo structure
- FastAPI
- Postgres migrations
- mission state machine
- mission events
- tasks
- artifacts
- approvals
- validation reports
- mock executor
- basic validators
- minimal dashboard

Success:

- A mission can move through real states.
- Events are persisted.
- Artifacts are tracked.
- Validators can block delivery.
- No fake progress.

## V1 - Personal Oli for Founder

Goal:

> Oli helps the founder build Oli.

Build:

- local Linux/server deployment
- Ollama adapter
- Docker sandbox
- Claude Code/spec generation workflow
- memory items
- model profile manual setup
- basic security policy
- basic audit log

Mission classes:

- notes -> specs
- docs -> roadmap
- repo inspection -> fix plan
- task generation for Claude Code

Success:

- Founder uses Oli weekly/daily for real work.
- Oli remembers useful preferences.
- Oli produces artifacts that reduce build time.

## V2 - Onboarding + Persistent Memory + Multi-User Basics

Goal:

> Oli feels personal, can onboard a second user in the same organization, and company memory is shared across the team.

Build:

- onboarding wizard (account setup, tool connections, first mission — no hardware scan needed, runs on our infra)
- model registry (Oli-managed catalog, user selects within it)
- What Oli Knows panel
- memory edit/delete/archive
- privacy modes
- redaction gateway V1
- multi-user org basics: shared company memory across seats, separate user memory per seat
- org roles: owner and member (no full RBAC yet — that is V4)

Success:

- A second user (non-founder) can onboard without help from the founder.
- Company memory is visible and useful to all org members.
- Model routing decisions are logged and explainable.
- Memory improves output across sessions.

Note: "team server" infrastructure (RBAC, approval delegation, per-team playbooks) comes in V3-V4. V2 is multi-user basics on the same tenant, not a full team product.

## V3 - Cross-Tool Execution

Goal:

> Oli can complete real workflows across files, code, browser/API, and sandbox.

Build:

- OpenClaw adapter
- browser/API adapters
- n8n/script adapter
- approval queue
- more validators
- mission-class playbooks
- golden mission runner
- observability V1

Mission classes:

- repo inspection + patch preparation
- report automation
- CRM/lead research prep
- campaign drafts with approval gates

Success:

- Oli completes multi-step missions with evidence.
- Repairs common failures.
- External side effects are approval-gated.

## V4 - Self-Improving Execution OS

Goal:

> Oli converts repeated work into playbooks and improves from feedback.

Build:

- playbook engine
- playbook versioning
- after-action review
- eval-based regression tests
- routing improvements from benchmark history
- cost-quality dashboard
- team server alpha
- stronger credential broker

Success:

- Repeated missions get faster, cheaper, and safer.
- Oli proposes reusable automations.
- User trusts Oli with higher-value work.

## V5 - Serious Private Release Candidate

Goal:

> Oli is good enough that selected users would pay and not compare it to a weekend agent.

Build:

- polished setup flow
- stable dashboard
- mission feed
- approvals
- artifacts
- memory panel
- secure local/hybrid deployment
- 3-5 excellent mission classes
- pricing experiment
- onboarding docs
- export/delete data controls

Success:

- Paid private users complete real work.
- Measurable hours saved.
- Validation rate strong.
- Security/policy violations near zero.
- Users say Oli feels like continuity, not a chat.

## Do not build first

- overly polished Core Orb before real mission events
- generic marketplace of tools
- enterprise admin console before V4/V5
- autonomous external actions before approval system
- complex multi-agent architecture before mission kernel works
- model fine-tuning before evals and data rights are clear
