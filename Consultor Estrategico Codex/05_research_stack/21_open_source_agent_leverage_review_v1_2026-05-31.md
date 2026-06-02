# Open-source Agent Leverage Review v1

Fecha: 2026-05-31
Rol: Codex como consultor estrategico/auditor

## Veredicto

La investigacion competitiva anterior fue incompleta.

Si Hermes, OpenRouter Apps y el ranking de agentes con uso real no estaban en el loop de discovery, entonces el proceso de "state-of-the-art" no era suficientemente bueno. No significa que la tesis de Oli este mal. Significa que el metodo de investigacion necesita una capa mas dura:

```text
No solo buscar frameworks conocidos.
Buscar que agentes se estan usando en volumen real.
Revisar su codigo/docs/licencia/seguridad.
Extraer patrones.
Validar contra TDD.
Decidir build/buy/adapt/delegate.
```

OpenRouter Apps debe convertirse en una fuente recurrente de leverage discovery.

## Fuentes usadas

- OpenRouter Apps: `https://openrouter.ai/apps`
- OpenRouter docs index local: `openrouter_docs.txt` desde `https://openrouter.ai/docs/llms.txt`
- OpenRouter Models/API docs: `https://openrouter.ai/docs/guides/overview/models`
- Claude Agent SDK: `https://platform.claude.com/docs/en/agent-sdk/quickstart`
- Claude Managed Agents: `https://platform.claude.com/docs/en/managed-agents/quickstart`
- Hermes Agent: `https://hermes-agent.nousresearch.com/`
- OpenClaw docs: `https://docs.openclaw.ai/`
- OpenCode: `https://dev.opencode.ai/` y `https://github.com/opencode-ai/opencode`
- Kilo Code: `https://kilo.ai/docs/getting-started`, `https://kilo.ai/open`, `https://github.com/Kilo-Org/kilocode`
- OpenClaw security survey: `https://arxiv.org/abs/2605.25435`
- OpenClaw security incident reporting: TechRadar/Oasis coverage, 2026-03

Nota: intente leer `tdd/adrs/ADR-013-openclaw-integration.md`, pero el entorno devolvio `Acceso denegado`. El analisis TDD se apoya en los ADRs y dominios visibles por `rg`: ADR-001, ADR-016, ADR-019, ADR-020, ADR-021, ADR-023, ADR-025, schemas y domain docs.

## Tesis del review

Oli no debe construir todo desde cero.

Pero tampoco debe convertirse en wrapper de OpenCode, Kilo, Claude Agent SDK, Hermes u OpenClaw.

La arquitectura correcta es:

```text
Oli Mission Kernel
  -> decide mision, permisos, evidencia, memoria, playbook, costo y validacion
  -> delega a agentes/runtimes cuando conviene
  -> extrae patrones open source cuando reducen riesgo/tiempo
  -> no cede la supervision del trabajo
```

Oli debe usar herramientas externas como operadores subordinados, no como cerebro.

## Ranking de leverage

| Candidato | Tipo | Leverage para Oli | Riesgo | Decision |
|---|---|---:|---:|---|
| Claude Agent SDK | SDK oficial de agente/coding | Muy alto para delegacion de coding y tool loop | Vendor lock-in/API cost | Usar como delegate premium, no core unico |
| Claude Managed Agents | Sandbox cloud/managed sessions | Alto para aprender contrato runtime/sandbox/events | Beta/vendor lock-in | Referencia, no base default |
| OpenCode | Open-source coding agent terminal | Alto para tool contracts, patch loop, TUI/CLI, LSP, provider abstraction | Dominio dev-only, privacidad/telemetry a validar | Extraer patrones; posible delegate local |
| Kilo Code | Agentic engineering platform | Alto para multi-surface, roles Architect/Code/Debug/Review, BYOK, team dashboard | Plataforma amplia, posible competencia dev-first | Extraer UX/workflow; no adoptar entero |
| Hermes | Persistent personal agent runtime | Alto para runtime, skills, prompt layers, sandboxing, checkpoints, subagents | Compite narrativamente con "agent that grows" | Benchmark arquitectonico |
| OpenClaw | Self-hosted multi-channel gateway | Alto para channels, gateway, mobile/web control, personal agent UX | Seguridad/supply chain/licencia GitHub no clara | Extraer gateway patterns; no integrar sin hardening |

## Que vale la pena traer

### 1. De Claude Agent SDK

Traer:

- agentic loop probado;
- streaming de eventos;
- tool execution semantics;
- `allowed_tools`;
- permission modes;
- MCP server integration;
- sesiones para coding;
- uso como delegado para tareas de repo donde Claude ya tiene ventaja.

Por que importa:

El TDD ya define `AgentRouter` con `CLAUDE_CODE_DELEGATE` y `CODEX_DELEGATE` en ADR-016. Claude Agent SDK encaja exactamente ahi: herramienta premium delegada, no reemplazo de Oli.

Ahorro estimado:

- 50-70% del esfuerzo de construir un coding delegate premium desde cero.
- 20-30% del esfuerzo de tool loop para coding, porque Oli aun debe envolver permisos, evidencia, Mission Black Box, costos y memory writes.

No traer:

- dependencia exclusiva de Anthropic;
- login/rate limits de claude.ai dentro de Oli sin aprobacion de Anthropic;
- `bypassPermissions` salvo sandbox CI completamente aislado.

Decision:

```text
Adopt as delegate, wrap with Oli permissions/evidence.
```

### 2. De Claude Managed Agents

Traer como referencia:

- contrato `Agent / Environment / Session / Events`;
- sandbox administrado o self-hosted;
- streaming de tool use;
- session lifecycle.

Esto valida ADR-021 Dedicated Oli Runtime.

Ahorro estimado:

- No ahorra desarrollo directo si Oli quiere runtime propio.
- Ahorra diseno: 2-4 semanas de arquitectura al darnos un contrato claro para runtime sessions.

Decision:

```text
Use as reference architecture and possible premium execution backend later.
```

### 3. De OpenCode

Traer:

- tool catalog de coding: `glob`, `grep`, `ls`, `view`, `write`, `edit`, `patch`, `diagnostics`, `bash`, `fetch`, `sourcegraph`, `agent`;
- permission dialog UX: allow, allow for session, deny;
- LSP diagnostics as first-class tool;
- custom commands as markdown prompts;
- provider abstraction, including self-hosted OpenAI-compatible endpoint;
- TUI/session ergonomics;
- local CLI as power-user surface.

Por que importa:

Oli necesita Product/Engineering Ops, repo inspection, PR prep, bug-to-fix-plan. OpenCode ya tiene patrones para el 60-70% de esa surface tecnica.

Ahorro estimado:

- Si se usa como delegate local: 40-60% de ahorro para coding agent workflows V1/V2.
- Si solo se extraen patrones: 20-30% de ahorro en diseno/implementacion de tool loop, patching y CLI UX.

Decision:

```text
Reimplement/adapt patterns. Evaluate delegate mode after security review.
```

No traer:

- su producto completo;
- su UX dev-first como cara principal de Oli;
- tool permissions sin mapear a `PermissionClass`;
- web/remote UI sin privacy review.

### 4. De Kilo Code

Traer:

- roles/modes: Architect, Code, Debug, Review;
- session continuity across IDE/CLI/cloud/mobile;
- BYOK como promesa de no lock-in;
- team dashboard/adoption analytics;
- multi-surface product thinking;
- MCP server marketplace discovery;
- code review/triage/autofix agent patterns.

Por que importa:

Kilo muestra que el mercado esta premiando plataformas de agentic engineering, no solo CLIs. Oli no debe limitarse al "lab" o al developer terminal; debe conservar founders, teams y agencias.

Ahorro estimado:

- 15-25% de ahorro conceptual para roles y workflow design.
- 30-40% de ahorro para futuras superficies dev/team si se toma Kilo como benchmark UX.
- Bajo ahorro directo de codigo, porque Oli tiene otro dominio y Kilo es plataforma dev-first.

Decision:

```text
Use as benchmark for Product/Engineering Ops and team surfaces.
```

No traer:

- modelo de producto centrado en IDE como default;
- "500+ models" como narrativa principal de Oli;
- marketplace sin supply-chain policy.

### 5. De Hermes

Traer:

- prompt layers `stable/context/volatile`;
- skills/procedural memory;
- subagents isolated/fresh context;
- sandbox and dangerous command approval;
- provider routing;
- trajectories/checkpoints/rollback;
- scheduled automations;
- MCP/plugins with credential filtering.

Por que importa:

Hermes es el benchmark mas cercano al runtime "agent that grows". Oli debe diferenciarse por mission governance, no por tener otro runtime persistente.

Ahorro estimado:

- 20-35% de ahorro en diseno de runtime/skills/subagents/security.
- 10-15% de ahorro directo de codigo salvo que se haga inspeccion profunda de modulos reutilizables.

Decision:

```text
Use as runtime benchmark. Extract design patterns only for now.
```

### 6. De OpenClaw

Traer:

- channel gateway;
- per-sender/per-workspace sessions;
- web control UI;
- mobile nodes / remote message surfaces;
- onboarding service daemon;
- channel allowlists and mention rules;
- multi-agent routing by sender/workspace.

Por que importa:

Oli necesita eventually vivir donde trabaja el usuario: Slack, email, browser, repo, docs. OpenClaw ya prueba que "message your agent from anywhere" tiene demanda.

Ahorro estimado:

- 30-50% de ahorro de diseno para channel gateway y service daemon.
- 10-20% de ahorro real de implementacion si se reimplementa con seguridad propia.
- No recomiendo integrar directo sin security audit.

Decision:

```text
Extract gateway/session/onboarding patterns. Reject direct integration for now.
```

Riesgo:

OpenClaw es exactamente el tipo de sistema que amplifica superficie de ataque: persistent memory + multi-channel + high privilege + skills/plugins. La literatura reciente sobre OpenClaw menciona amenazas como skill poisoning, cognitive manipulation, cascading failures y supply-chain vulnerabilities. Eso refuerza ADR-020.

## Claude Agent SDK vs OpenCode

Esta comparacion es clave.

| Criterio | Claude Agent SDK | OpenCode |
|---|---|---|
| Naturaleza | SDK oficial/proprietary-backed | Open-source coding agent |
| Mejor uso para Oli | Delegate premium de coding/agentic tasks | Local/dev delegate o fuente de patrones |
| Modelo | Claude-first | Multi-provider/self-hosted |
| Tool loop | Resuelto por SDK | Visible y modificable |
| Permisos | `allowed_tools`, permission modes | Permission dialog y session allow/deny |
| MCP | Integrado | Soportado, con mismo modelo de permisos |
| LSP/diagnostics | No es su diferenciador principal | Fuerte para coding agent |
| Vendor risk | Alto | Bajo-medio |
| Código reusable | Bajo, depende de SDK | Alto, MIT en repo oficial segun GitHub |
| Calidad frontier | Alta con Claude | Depende del modelo/provider |
| Fit V0/V1 Oli | Alto como delegado puntual | Alto como benchmark, medio como delegate |

Conclusion:

```text
Claude Agent SDK = mejor para no reconstruir un agente de codigo premium.
OpenCode = mejor para aprender/extraer el diseno de un agente de codigo controlable.
```

Oli deberia soportar ambos como rutas distintas:

```text
AgentRouter:
  if mission_step requires premium repo repair:
      ClaudeAgentSDKDelegate
  if mission_step is local/dev workflow and privacy/cost matters:
      OpenCodeLikeLocalDelegate or OliCodingOperator
```

## Cuanto desarrollo se ahorraria Oli

Estimacion realista, no marketing:

| Area | Si se construye desde cero | Con leverage open source/SDK | Ahorro estimado |
|---|---:|---:|---:|
| Coding delegate premium | 6-10 semanas | 2-4 semanas con Claude Agent SDK wrapper | 50-70% |
| Local coding tool loop | 8-12 semanas | 5-8 semanas extrayendo OpenCode patterns | 25-40% |
| CLI/TUI dev surface | 6-8 semanas | 3-5 semanas usando OpenCode patterns | 30-45% |
| Channel gateway | 10-16 semanas | 6-10 semanas con OpenClaw patterns | 30-40% |
| Runtime sessions/events | 6-10 semanas | 4-6 semanas tomando Claude Managed Agents/Hermes contracts | 25-35% |
| Tool security | 8-12 semanas | 6-9 semanas con Hermes/OpenClaw incident patterns + ADR-020 | 15-30% |
| Skills/playbooks | 8-12 semanas | 5-8 semanas con Hermes/Kilo/OpenClaw patterns | 25-35% |
| Model/provider gateway | 6-8 semanas | 4-6 semanas con OpenRouter/Kilo/OpenCode patterns | 20-35% |

Pero el Mission Kernel, Evidence Trail, Permission Classes, Mission Black Box, org memory, playbook governance y pricing/routing economics no se pueden "traer" de afuera. Eso es Oli.

## Validacion contra TDD

### ADR-001 Model Strategy

Encaja.

El TDD dice model-agnostic. OpenCode/Kilo/OpenRouter refuerzan que no hay que casarse con un modelo. Claude Agent SDK se acepta como premium delegate, no como vendor lock-in.

### ADR-016 Model Routing / Agent Router

Encaja y debe expandirse.

ADR-016 ya contempla `CLAUDE_CODE_DELEGATE` y `CODEX_DELEGATE`. Debe agregarse explicitamente:

```text
OPEN_CODE_LOCAL_DELEGATE
KILO_DEV_WORKFLOW_REFERENCE
CHANNEL_GATEWAY_REFERENCE
```

No como producto final, sino como rutas/patrones de leverage.

### ADR-019 Mission Black Box

Encaja.

Cualquier delegate externo debe devolver:

- prompt/task;
- tool calls;
- files touched;
- patch/diff;
- commands run;
- model used;
- cost;
- validation result;
- artifacts;
- permission decisions.

Sin eso, se rechaza. Oli no puede delegar a una caja negra sin caja negra propia.

### ADR-020 Tool Security

Encaja, pero se queda corto frente a OpenClaw/Hermes.

Agregar en futura iteracion:

- SSRF protection;
- local gateway auth hardening;
- network egress policy;
- plugin/skill signing or trust levels;
- MCP env var filtering;
- credential passthrough allowlist;
- command blocklist + dangerous command confirmation;
- supply-chain review para skills/plugins;
- browser-origin attack checks.

### ADR-021 Dedicated Oli Runtime

Encaja fuerte.

Hermes, OpenClaw y Claude Managed Agents validan que runtime dedicado/sandbox/session es el camino. Pero Oli debe ser:

```text
mission-governed runtime
```

No solo:

```text
persistent personal agent runtime
```

### ADR-023 Subagent Engineering

Encaja.

OpenCode tiene `agent` como tool para subtasks. Hermes usa subagents aislados. Kilo usa roles/modes. Todo valida la decision de "specialists-as-tools", pero tambien confirma la regla:

```text
No multi-agent por defecto.
Usar roles solo cuando hay contrato, validacion y ahorro real.
```

### ADR-025 State-of-the-Art Discovery

Necesita extension formal.

`open_source_agent_leverage_review` debe ser subclase de decision memo:

```text
state_of_art_decision_memo
  -> open_source_agent_leverage_review
```

Output:

- repo/app;
- usage signal;
- source quality;
- license;
- architecture map;
- reusable patterns;
- risks;
- TDD fit;
- build/adapt/delegate/reject;
- next spike.

## Que mejora con estas opciones open source

### Mejoras concretas

1. Menos invencion prematura
   - Oli aprende de agentes que ya tienen uso real.

2. Mejor security posture
   - OpenClaw muestra que agentes con permisos reales fallan por gateway, plugins, memoria y autonomia.

3. Mejor runtime contract
   - Claude Managed Agents y Hermes dan un lenguaje claro: agent, environment, session, events, tools, sandbox, checkpoints.

4. Mejor developer workflow
   - OpenCode/Kilo dan patrones para repo inspection, patching, diagnostics y sessions.

5. Mejor routing/product economics
   - OpenRouter/Kilo/OpenCode refuerzan BYOK, provider abstraction, self-hosted endpoints y model selection dinamico.

6. Mejor product intuition
   - Kilo y OpenClaw muestran que multi-surface importa: IDE, CLI, Slack, mobile, browser, control UI.

## Que NO mejora

No resuelve:

- ICP;
- pricing;
- Mission Kernel;
- permission classes;
- evidence trail;
- org memory;
- playbook governance;
- Oli-to-Oli solution bank;
- trust del usuario;
- monetizacion en agencias/teams;
- evals de misiones de negocio.

Por eso Oli no debe volverse "OpenCode plus memory" ni "OpenClaw para empresas".

## Recomendacion ejecutiva

### Camino recomendado

1. Adoptar Claude Agent SDK como delegate premium para coding/repo tasks.
2. Usar OpenCode como benchmark y posible local coding delegate.
3. Usar Kilo como benchmark de workflow dev/team, no como core.
4. Usar Hermes como benchmark de runtime/skills/security.
5. Usar OpenClaw como benchmark de channel gateway, pero tratarlo como riesgo alto de seguridad.
6. Crear `open_source_agent_leverage_review` como proceso recurrente dentro de ADR-025.

### Primer spike recomendado

No empezar con OpenClaw.

Empieza por coding delegate porque es acotado, medible y encaja con V0/V1:

```text
Spike: Claude Agent SDK delegate vs OpenCode-like local delegate

Input:
  repo pequeno con bug real

Outputs:
  fix plan
  patch
  tests run
  evidence report
  cost/model/tool trace

Comparar:
  quality
  latency
  permission compliance
  patch cleanliness
  ease of wrapping
  Mission Black Box completeness
```

Resultado esperado:

```text
Claude Agent SDK gana calidad/velocidad en premium.
OpenCode gana transparencia/control/costo.
Oli gana si puede elegir segun mission/tier/privacy.
```

## Decision final

Traer:

- Claude Agent SDK as delegate.
- OpenCode tool/pattern model.
- Kilo workflow concepts.
- Hermes runtime/security/skills patterns.
- OpenClaw channel gateway patterns.
- OpenRouter Apps as recurring market signal.

No traer:

- un runtime externo como cerebro;
- autonomy sin permission classes;
- marketplaces sin supply-chain policy;
- agent UIs que no muestren evidencia;
- model routing decidido por popularidad.

La frase canonica:

> Oli no compite construyendo cada pieza desde cero. Oli compite integrando, gobernando y mejorando las mejores piezas disponibles bajo un Mission Kernel con memoria, permisos, evidencia, playbooks y decision quality.

