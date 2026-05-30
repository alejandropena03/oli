# Claude Code Start Here

You are building **Oli**, not Jarvis.

Oli is a personal execution operator backed by a local-first Execution OS.

Canonical promise:

> De intención a trabajo terminado.

## Read first

Read these files in order:

1. `docs/OLI_MASTER_SPEC.md`
2. `docs/technical/README.md`
3. `docs/technical/00_TECHNICAL_THESIS.md`
4. `docs/technical/01_CANONICAL_STACK.md`
5. `docs/technical/02_LOCAL_FIRST_PRODUCT_ARCHITECTURE.md`
6. `docs/technical/03_SETUP_WIZARD_AND_MODEL_SELECTION.md`
7. `docs/technical/04_MISSION_KERNEL_TECH_SPEC.md`
8. `docs/technical/06_SECURITY_PRIVACY_AND_DATA_PROTECTION.md`

## Your first job

Create a concrete implementation plan for **V0 Mission Kernel Foundation**.

Do not build the full app in one pass.

## Non-negotiable rules

- Product name is Oli everywhere.
- No chatbot-first architecture.
- No fake dashboard progress.
- No hardcoded model provider.
- The user is free to choose local/premium models.
- Oli recommends model setup based on hardware, privacy, mission type, and budget.
- Executors cannot write official memory.
- Executors cannot deliver final user responses.
- No mission is delivered without validation or explicit partial-delivery status.
- Security, permissions, and audit logging are required from V0.

## Output required

Return:

1. Monorepo structure.
2. Backend module map.
3. Database tables.
4. API endpoints.
5. Mission state machine implementation plan.
6. Model routing V0 implementation plan.
7. Security V0 implementation plan.
8. Test/eval plan.
9. Exact first coding tasks in order.

## Build order

1. Repo bootstrap.
2. Mission database and state machine.
3. Mission events and artifact tracking.
4. Approvals and permission policy.
5. Validation reports and validators.
6. Mock executor.
7. Docker sandbox stub/minimal.
8. Model profile/router skeleton.
9. Memory items minimal.
10. Minimal dashboard from real mission events.
