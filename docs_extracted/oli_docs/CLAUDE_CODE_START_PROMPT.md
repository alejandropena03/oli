# CLAUDE CODE START PROMPT FOR OLI

Paste this into Claude Code at the root of the Oli repo.

---

Read `docs/OLI_MASTER_SPEC.md` completely before writing code.

Treat it as the source of truth for product, architecture, behavior, UX, and roadmap.

We are building Oli: a personal execution operator with an Execution OS behind it.

Canonical promise: De intencion a trabajo terminado.

Do not build a generic chatbot. Do not build a decorative dashboard first. Build the V0 Mission Kernel.

Your first objective:

Build a working V0 Mission Kernel prototype.

Required deliverables:

1. Core types/schemas for:
   - Mission
   - MissionState
   - MissionStep
   - EvidenceItem
   - PermissionClass
   - ApprovalRequest
   - CostEstimate
   - MemoryWrite
   - FinalReport

2. Mission state machine with these states:
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

3. Permission classifier for classes 0-4:
   - Class 0: no permission needed
   - Class 1: reversible internal action
   - Class 2: cost-bearing or resource action
   - Class 3: external communication or brand impact
   - Class 4: destructive, security, financial, or production action

4. Mock mission runner:
   - Accept a raw user intent.
   - Create a mission object.
   - Interpret intent.
   - Create a plan.
   - Log feed events.
   - Simulate execution.
   - Simulate validation.
   - Generate evidence.
   - Generate final report.
   - Add memory write candidates.

5. Minimal developer UI:
   - Create mission.
   - See mission state.
   - See Mission Feed.
   - See evidence.
   - See permission status.
   - See final report.

6. Tests:
   - Mission state transitions.
   - Permission classification.
   - Evidence logging.
   - Final report generation.
   - Mock mission completion.

Constraints:

- No fake validation claims.
- No external integrations in this task.
- No polished Orb animation yet.
- No overbuilt settings page.
- Keep the architecture modular so V1-V5 can be built on top.

Before coding, produce:

1. A short implementation plan.
2. Proposed file structure.
3. Any assumptions.

Then implement.
