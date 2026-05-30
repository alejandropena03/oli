# 03 - Setup Wizard and Model Selection

## Purpose

Oli must not hardcode one local model, one premium provider, or one compute assumption.

Each user is free to decide what model stack they use. Oli's job is to make that choice simple, safe, and evidence-based.

## Setup principle

The user should feel:

> I own the system. Oli understands my hardware and privacy needs. Oli recommends the best setup, installs what I approve, benchmarks it, and explains the tradeoffs in plain language.

## Setup flow

### Step 1 - Deployment choice

Ask or infer:

- local machine
- Linux server
- GPU workstation
- cloud VM
- team server
- managed mode later

### Step 2 - Hardware scan

Collect, with explicit permission:

- OS
- CPU
- RAM
- GPU model
- GPU VRAM
- available disk
- Docker availability
- network access
- installed runtimes
- existing Ollama/vLLM installations

### Step 3 - Privacy posture

User chooses:

| Mode | Meaning |
|---|---|
| Local Only | No mission content goes to premium providers. |
| Hybrid Redacted | Sensitive content is redacted/summarized before premium use. |
| Hybrid Approval | Premium use allowed only with explicit approval on sensitive missions. |
| Quality First | Premium models allowed when Oli believes quality gain is worth it. |
| Custom | Advanced user-defined routing rules. |

### Step 4 - Mission profile

User selects likely mission classes:

- coding/repo work
- research/synthesis
- data analysis
- marketing/campaigns
- CRM/sales ops
- reporting
- document automation
- browser/OS operations
- personal/company memory

### Step 5 - Budget policy

User chooses:

- local-only budget
- premium monthly cap
- per-mission premium cap
- approval threshold
- fallback policy after local failures

### Step 6 - Model recommendation

Oli generates a `ModelSetupPlan`:

```json
{
  "recommended_profile": "local_gpu_hybrid",
  "privacy_mode": "hybrid_approval",
  "local_runtime": "ollama",
  "future_runtime": "vllm_when_needed",
  "models": {
    "fast_local": {
      "role": "classification, memory extraction, formatting",
      "candidate": "user_selected_fast_model"
    },
    "main_local": {
      "role": "coding, tool use, first-pass execution",
      "candidate": "user_selected_main_model"
    },
    "embedding": {
      "role": "memory retrieval",
      "candidate": "user_selected_embedding_model"
    },
    "premium": {
      "role": "hard reasoning and recovery",
      "provider": "user_selected_provider",
      "requires_approval_above_usd": 2.0
    }
  },
  "benchmark_required": true,
  "estimated_capabilities": [
    "local coding missions",
    "private document summarization",
    "local validation",
    "premium fallback for hard architecture"
  ],
  "limitations": [
    "vision tasks require additional model or premium provider",
    "very long context may require premium or vLLM upgrade"
  ]
}
```

## Model Registry

Oli should maintain a local `ModelRegistry`.

Fields:

```json
{
  "model_id": "string",
  "provider": "ollama|vllm|openai|anthropic|gemini|custom",
  "display_name": "string",
  "family": "string",
  "roles": ["fast", "coding", "reasoning", "embedding", "vision", "judge"],
  "local": true,
  "requires_gpu": true,
  "min_vram_gb": 24,
  "recommended_vram_gb": 48,
  "context_tokens_estimate": 64000,
  "tool_use_reliability": "unknown|low|medium|high",
  "privacy_rating": "local|external",
  "cost_model": "local_compute|api_per_token|unknown",
  "status": "candidate|installed|benchmarked|disabled",
  "benchmark_scores": {}
}
```

## User Model Choice

The model recommendation is not coercive.

User can:

- accept Oli recommendation
- choose another local model
- add custom model endpoint
- disable premium models
- use premium-only temporarily
- set different models per mission class

Oli must expose choices simply:

```text
Recommended for your machine:
- Fast local: small model for classification and memory extraction.
- Main local: larger coding/reasoning model for execution.
- Premium fallback: disabled by default for sensitive data unless you approve.

Why:
Your GPU can handle larger local coding tasks, but very long strategic synthesis may be better with a premium model.
```

## Preinstallation by Oli

When user approves, Oli can:

- install runtime dependencies
- pull selected local models
- configure Ollama/vLLM
- start services
- run health checks
- run benchmark missions
- save the resulting `ModelProfile`

Oli must not silently install heavy models or services without approval.

## Benchmarking

Before a model becomes canonical for a user, run:

- startup/load test
- short coding task
- repo reasoning task
- structured JSON output test
- tool-call formatting test
- memory extraction test
- summarization test
- latency test
- context stress test
- validation repair test

Store results in `model_benchmarks`.

## Routing policy

The model router uses:

- user preference
- privacy mode
- task type
- risk class
- context length
- validation history
- mission value
- local benchmark performance
- premium budget
- latency requirement

Never route sensitive data to premium providers unless policy allows.

## Model Router APIs

Suggested endpoints:

```text
GET  /setup/hardware
POST /setup/scan
GET  /models/registry
POST /models/install-plan
POST /models/install
POST /models/benchmark
GET  /models/profiles/current
PUT  /models/profiles/current
POST /models/route-simulation
```

## V0 implementation

V0 should implement:

- static model registry
- user model profile schema
- Ollama local client
- premium provider stub
- route simulation
- manual model selection
- model call logging

V1/V2 should add:

- hardware scan
- guided installer
- benchmark runner
- automatic recommendation
- privacy-aware routing

## Core rule

Oli is model-agnostic, but not model-indifferent.

It should recommend the best available model stack for the user's real environment and mission needs.
