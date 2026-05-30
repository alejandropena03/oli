# 02 - Local-First Product Architecture

## Purpose

Oli started as a personal local-first system. That is an advantage, but it must be productized.

The product should not force one deployment mode. It should guide the user into the simplest safe deployment that fits their hardware, privacy needs, and mission ambition.

## Deployment profiles

### Profile A - Solo Local Basic

For:

- individual founder
- laptop/desktop
- light missions
- high privacy
- low setup complexity

Characteristics:

- local Oli daemon or local Docker Compose
- small local model or premium-only with redaction
- local file access scoped to workspaces
- minimal integrations
- no team permissions

### Profile B - Local GPU Power User

For:

- founder/operator with Linux GPU server
- heavy coding/research/data missions
- desire to reduce premium model spend

Characteristics:

- Ubuntu Server
- Docker Compose
- Ollama initially
- vLLM later
- OpenClaw/executor runtime
- Docker sandbox
- Postgres + pgvector
- Redis
- MinIO
- local dashboard
- optional SSH/admin access

This is the founder's original strong configuration.

### Profile C - Hybrid Operator

For:

- users who want local privacy and premium quality when needed

Characteristics:

- local-first by default
- premium models allowed by policy
- redaction before premium calls
- user approval for sensitive external calls
- model routing based on mission risk/value

### Profile D - Team Server

For:

- small teams
- agencies
- operations teams
- startups with multiple users

Characteristics:

- central Oli server
- org memory
- user memory
- RBAC
- shared integrations
- approval queues
- audit logs
- per-user policy
- per-team playbooks

### Profile E - Future Managed/On-Prem

For:

- companies that want Oli but not self-managed infrastructure

Characteristics:

- managed cloud or customer VPC/on-prem
- stronger auth/SSO
- compliance reports
- tenant isolation
- centralized admin controls

Not V0.

## Product architecture

```text
User
  -> Oli Interface Layer
      - command input
      - voice later
      - dashboard
      - approval queue
  -> Oli API
      - missions
      - memory
      - approvals
      - artifacts
      - settings
  -> Mission Kernel
      - state machine
      - policy engine
      - validation gates
      - event stream
  -> Orchestrator
      - LangGraph
      - planner
      - executor router
      - repair loop
      - delivery formatter
  -> Runtime Layer
      - local models
      - premium models
      - OpenClaw
      - Docker sandbox
      - browser/API adapters
      - n8n/scripts
  -> Trust Layer
      - permissions
      - credential broker
      - redaction
      - audit log
      - evidence store
  -> Memory Layer
      - user memory
      - company memory
      - mission memory
      - playbooks
      - decision history
```

## SSH role

SSH should not be the normal product interface.

SSH is an operational/admin channel for:

- installing Oli on a Linux server
- restarting services
- inspecting logs
- applying updates
- running maintenance scripts
- connecting a user-owned server during setup

Oli itself should operate through APIs, workers, adapters, and permissioned execution.

If Oli controls a computer through OS-level agents, that control must still go through the Permission Service and Audit Log.

## Data ownership

Default assumption:

> The user's data belongs to the user and lives under the user's selected deployment and privacy policy.

Oli may store:

- mission records
- artifacts
- memory items
- logs
- model-call metadata
- tool-call metadata
- user preferences

But the user must be able to:

- inspect what Oli knows
- edit memories
- delete memories
- export data
- disable premium routing
- disable global learning
- set sensitive-data boundaries

## Local-first does not mean local-only

Local-only is a privacy mode.

Local-first is an architecture.

Oli can support:

- local-only missions
- local-first with premium fallback
- premium-only for users without local hardware
- hybrid routing by task
- team policies that define which data can leave the local environment

## Product rule

The user should never need to understand the full stack to get value.

The setup experience should translate technical complexity into simple choices:

- privacy level
- hardware available
- mission types
- monthly budget
- integrations
- autonomy level

Then Oli recommends a deployment and model profile.
