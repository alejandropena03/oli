# 13 - Diagrams

## High-level architecture

```mermaid
flowchart TD
  U[User] --> UI[Oli Interface Layer]
  UI --> API[Oli API - FastAPI]
  API --> MK[Mission Kernel]
  MK --> MEM[Memory Graph]
  MK --> SEC[Security and Permission Service]
  MK --> ORCH[LangGraph Orchestrator]
  ORCH --> ROUTER[Executor Router]
  ROUTER --> OC[OpenClaw Adapter]
  ROUTER --> SB[Docker Sandbox]
  ROUTER --> BAPI[Browser/API Adapters]
  ROUTER --> N8N[n8n/Scripts]
  ROUTER --> MR[Model Router]
  MR --> LOCAL[Local Models - Ollama/vLLM]
  MR --> PREM[Premium Model Providers]
  OC --> EV[Evidence Store]
  SB --> EV
  BAPI --> EV
  N8N --> EV
  LOCAL --> EV
  PREM --> EV
  EV --> VAL[Validation Layer]
  VAL --> MK
  MK --> ART[Artifact Store - MinIO/S3]
  MK --> DB[(Postgres + pgvector)]
  MK --> REDIS[(Redis Events)]
  REDIS --> DASH[Mission Control Dashboard]
```

## Setup and model selection

```mermaid
flowchart TD
  START[User starts setup] --> DEPLOY[Choose deployment profile]
  DEPLOY --> SCAN[Hardware scan with permission]
  SCAN --> PRIV[Choose privacy mode]
  PRIV --> MISS[Choose mission profile]
  MISS --> BUDGET[Set budget policy]
  BUDGET --> PLAN[Oli creates ModelSetupPlan]
  PLAN --> APPROVE{User approves?}
  APPROVE -->|no| EDIT[User edits choices]
  EDIT --> PLAN
  APPROVE -->|yes| INSTALL[Install/configure runtimes and models]
  INSTALL --> BENCH[Run benchmarks]
  BENCH --> PROFILE[Save ModelProfile]
  PROFILE --> READY[Oli ready for missions]
```

## Mission state machine

```mermaid
stateDiagram-v2
  [*] --> created
  created --> intake_normalized
  intake_normalized --> context_retrieved
  context_retrieved --> classified
  classified --> planned
  planned --> awaiting_approval: policy requires approval
  planned --> executing: policy allows
  awaiting_approval --> executing: approved
  awaiting_approval --> cancelled: rejected
  executing --> validating
  executing --> failed: unrecoverable executor failure
  validating --> delivering: validators pass
  validating --> repairing: validators fail and attempts remain
  validating --> partially_delivered: partial acceptable
  repairing --> executing
  repairing --> failed: attempts exhausted
  delivering --> delivered
  delivered --> memory_reviewed
  partially_delivered --> memory_reviewed
  failed --> memory_reviewed
  memory_reviewed --> archived
  archived --> [*]
```

## Model routing

```mermaid
flowchart TD
  T[Task] --> POLICY[Model Policy]
  POLICY --> PRIV[Privacy Mode]
  PRIV --> SENS[Data Sensitivity]
  SENS --> DET{Deterministic possible?}
  DET -->|yes| NOMODEL[No model]
  DET -->|no| LOCALOK{Local model suitable?}
  LOCALOK -->|yes| LOCAL[Use local model]
  LOCALOK -->|no| PREMOK{Premium allowed?}
  PREMOK -->|yes| REDACT[Redact/summarize if needed]
  REDACT --> PREMIUM[Use premium model]
  PREMOK -->|no| ASK[Ask user or fail honestly]
  LOCAL --> VAL[Validate]
  PREMIUM --> VAL
  NOMODEL --> VAL
  VAL --> PASS{Pass?}
  PASS -->|yes| DONE[Return to Mission Kernel]
  PASS -->|no| REPAIR[Retry/repair/escalate by policy]
```

## Security gating

```mermaid
flowchart TD
  ACTION[Planned action] --> CLASS[Classify risk class]
  CLASS --> DATA[Classify data sensitivity]
  DATA --> SIDE[External side effect?]
  SIDE --> REV[Reversible?]
  REV --> POLICY[Permission Policy]
  POLICY --> DEC{Decision}
  DEC -->|allow| EXEC[Execute]
  DEC -->|approval| APPROVAL[Ask user]
  DEC -->|block| BLOCK[Block]
  APPROVAL -->|approved| EXEC
  APPROVAL -->|rejected| BLOCK
  EXEC --> AUDIT[Audit log]
  BLOCK --> AUDIT
```

## Memory and self-improvement loop

```mermaid
flowchart LR
  MISSION[Mission] --> EXEC[Execution]
  EXEC --> VAL[Validation]
  VAL --> FEED[User feedback]
  FEED --> CAND[Memory candidates]
  CAND --> POLICY[Memory write policy]
  POLICY --> MEM[Memory Graph]
  MEM --> RET[Future retrieval]
  RET --> PLAN[Better planning]
  PLAN --> PLAY[Playbook updates]
  PLAY --> MISSION
```

## Oli/executor boundary

```mermaid
flowchart TD
  USER[User] --> OLI[Oli]
  OLI --> STATE[Mission State]
  OLI --> POLICY[Policies and Approvals]
  OLI --> MEMORY[Official Memory]
  OLI --> FINAL[Final Response]
  OLI --> EXEC[Executors]
  EXEC --> OC[OpenClaw]
  EXEC --> DOCKER[Docker]
  EXEC --> BROWSER[Browser/API]
  EXEC --> MODELS[Local/Premium Models]
  OC --> RESULT[Structured Results]
  DOCKER --> RESULT
  BROWSER --> RESULT
  MODELS --> RESULT
  RESULT --> OLI
```
