# State-of-the-art discovery y recomendaciones no flojas para Oli

Fecha: 2026-05-31
Rol: Codex como consultor estrategico/auditor

## Veredicto

Este pendiente es macro.

`Model Intelligence` es solo un caso particular. La capacidad completa que Oli necesita es:

```text
State-of-the-Art Discovery Engine
  -> evidence retrieval
  -> source quality ranking
  -> option generation
  -> benchmark/currentness check
  -> buildability check
  -> cost/sustainability check
  -> risk/privacy/security check
  -> decision memo
  -> execution route
```

Oli no debe "recomendar lo que recuerda". Tampoco debe "buscar en web y resumir lo primero". Debe construir una recomendacion defendible, actual y accionable.

## Problema que resuelve

La mayoria de agentes hacen recomendaciones flojas por cuatro razones:

1. Usan conocimiento viejo.
2. Buscan superficialmente.
3. No distinguen fuente primaria de blog/SEO.
4. No convierten opciones en decision ejecutable.

Para Oli, eso rompe el pilar "construimos con excelencia".

Si el usuario pregunta:

```text
Que modelo instalo?
Que stack uso?
Que MCP conviene?
Que servicio cloud contrato?
Como automatizo esto?
Que herramienta AI-first deberia usar?
```

Oli debe responder con:

- fuentes actuales;
- alternativas reales;
- tradeoffs;
- costo;
- fit con el usuario/tier/runtime;
- riesgo;
- recomendacion;
- siguiente accion.

## Decision central

Oli debe canonizar una mission class:

```text
state_of_art_decision_memo
```

No es "research brief". Es una decision operacional.

Output:

```text
Decision memo + recommended action + evidence pack + update policy
```

## Extension: open-source leverage

Una parte especifica de este motor debe ser:

```text
open_source_agent_leverage_review
```

No basta con saber "que existe". Oli debe revisar las apps y agentes con traccion real, especialmente las listadas en OpenRouter Apps, para extraer patrones ya probados por el mercado.

La regla es:

```text
No copiar producto.
Extraer arquitectura, contratos, seguridad, UX operacional, distribucion y eval patterns.
Adaptar solo lo que mejora la tesis de Oli.
```

Documento relacionado:

```text
20_openrouter_apps_leverage_y_extraccion_open_source_2026-05-31.md
```

## Fuentes: no todas valen igual

### Tier A - Fuentes primarias

Usar cuando existan:

- docs oficiales;
- API docs;
- model cards;
- technical reports;
- release notes;
- GitHub repo oficial;
- pricing oficial;
- benchmark paper con metodologia;
- changelog oficial;
- security advisories;
- status pages.

Ejemplos verificados:

- OpenRouter Models API publica metadata de modelos: context length, pricing, architecture, provider details y supported parameters.
- Hugging Face documenta leaderboards/eval results y model cards.
- vLLM documenta OpenAI-compatible serving, LoRA, quantization y tool calling.
- Ollama documenta context length configurable y hardware support.

### Tier B - Fuentes agregadoras confiables

Usar como señales, no como verdad unica:

- LMArena/Arena para preferencia humana;
- Artificial Analysis para calidad/costo/velocidad/contexto;
- OpenRouter Rankings para uso real y tool-call usage;
- Hugging Face community/eval leaderboards;
- BenchLM/WhatLLM/LLM Stats si la metodologia es visible.

### Tier C - Comunidad y experiencia

Util para detectar problemas reales:

- Reddit;
- Discord;
- Hacker News;
- issues GitHub;
- posts de practitioners;
- benchmarks independientes.

Regla:

```text
Comunidad detecta problemas; no canoniza decisiones.
```

### Tier D - Blogs SEO / comparativas dudosas

Solo sirven para descubrir nombres, nunca para decidir.

Riesgo:

- AI-generated content;
- affiliate bias;
- informacion vieja;
- claims sin metodologia;
- malware/ads en busquedas de herramientas.

## Source Quality Score

Cada fuente recuperada debe recibir:

```yaml
source_quality:
  source_type: official_docs | technical_report | benchmark | leaderboard | github | pricing | community | seo_blog
  authority: 0.0-1.0
  freshness: 0.0-1.0
  methodology_clarity: 0.0-1.0
  relevance_to_decision: 0.0-1.0
  bias_risk: 0.0-1.0
  citation_confidence: 0.0-1.0
```

Regla:

```text
Una recomendacion fuerte requiere al menos 2 fuentes Tier A/B
o 1 fuente Tier A + benchmark propio de Oli.
```

## Workflow de discovery

### 1. Classify Decision

Clasificar la decision:

```text
model_selection
tool_selection
cloud_service_selection
architecture_pattern
automation_strategy
security_policy
pricing/vendor_decision
ai_first_workflow_recommendation
```

### 2. Define Evaluation Criteria

Antes de buscar, Oli define criterios.

Ejemplo para modelo local:

```text
quality, context_effective, vram_fit, latency, license, cost, tool_use, structured_outputs
```

Ejemplo para herramienta SaaS:

```text
capabilities, API quality, pricing, lock-in, security, reliability, integration cost
```

Ejemplo para cloud/service broker:

```text
total cost, support burden, uptime, data residency, operational complexity, margin impact
```

### 3. Retrieve Evidence

Usar varias herramientas/fuentes:

- web search general;
- official docs search;
- GitHub search;
- model/vendor APIs;
- benchmark APIs/leaderboards;
- pricing pages;
- community issue search;
- internal Oli memory/solution bank;
- prior mission traces.

### 4. Filter and Rank Sources

Eliminar:

- duplicados;
- contenido sin fecha;
- claims sin fuente;
- SEO comparativo sin metodologia;
- fuente vieja cuando hay docs nuevos;
- fuente no oficial para pricing/licencia si existe fuente oficial.

### 5. Generate Options

Crear 2-5 opciones reales:

```text
Recommended
Strong alternative
Low-cost alternative
High-control/self-hosted alternative
Do-nothing/keep-current
```

### 6. Score Options

Cada opcion recibe scoring ponderado:

```yaml
option_score:
  quality: number
  fit_to_user: number
  buildability: number
  cost: number
  latency: number
  security_privacy: number
  maintainability: number
  reversibility: number
  strategic_moat: number
```

### 7. Buildability Check

Pregunta dura:

```text
Podemos construir/instalar/operar esto con el runtime, presupuesto y permisos actuales?
```

Incluye:

- hardware;
- engineering effort;
- dependencies;
- ops burden;
- support risk;
- time to first value;
- migration complexity.

### 8. Sustainability / Margin Check

Para Oli como producto:

- GPU minutes;
- API cost;
- storage cost;
- support burden;
- vendor risk;
- overage model;
- gross margin impact.

### 9. Risk Check

Revisar:

- licencia;
- privacidad;
- seguridad;
- prompt injection surface;
- data residency;
- vendor lock-in;
- reputational risk;
- failure mode.

### 10. Decision Memo

Output obligatorio:

```markdown
# Decision Memo

## Verdict
...

## Recommended Option
...

## Why
...

## Alternatives Considered
...

## Evidence
...

## Cost / Effort
...

## Risks
...

## Reversibility
...

## Next Action
...

## Recheck Date
...
```

## Recomendaciones no flojas: criterios

Una recomendacion de Oli es floja si:

- no cita fuentes;
- no tiene fecha;
- no compara alternativas;
- no explica tradeoffs;
- no revisa costo;
- no revisa implementabilidad;
- no revisa riesgo;
- no dice que hacer despues;
- recomienda lo popular sin fit;
- usa "best" sin definir para que.

Una recomendacion de Oli es fuerte si:

- define el objetivo;
- pondera criterios;
- separa hechos de inferencias;
- dice incertidumbre;
- ofrece decision y ruta;
- deja evidencia;
- tiene fecha de revalidacion.

## Arquitectura propuesta

```text
User asks for recommendation
  -> DecisionClassifier
  -> CriteriaBuilder
  -> SourcePlanner
  -> EvidenceRetriever
  -> SourceRanker
  -> OptionGenerator
  -> OptionScorer
  -> BuildabilityChecker
  -> RiskChecker
  -> DecisionMemoWriter
  -> Validator
  -> Mission Black Box
```

Esto puede ser single-agent o subagent workflow segun complejidad.

Para decisiones simples:

```text
single_agent_with_tools + validator
```

Para decisiones tecnicas importantes:

```text
manager_with_specialists_as_tools:
  - researcher
  - technical_architect
  - cost_checker
  - risk_checker
  - validator
```

## MCP/tool layer recomendada

No crear un solo "research MCP" generico. Crear tools por fuente/capacidad:

```text
source_search.web(query, filters)
source_search.official_docs(query, domains)
source_search.github_repo(query)
source_search.github_issues(repo, query)
model_intelligence.recommend_model(...)
pricing.fetch_vendor_pricing(vendor)
benchmark.fetch_leaderboard(source, category)
cloud_advisor.estimate_cost(service, region, usage)
license_checker.check(repo_or_model)
security_advisor.check_known_risks(package_or_service)
```

El Orchestrator decide que tools usar segun decision class.

## Relacion con Model Intelligence

`Model Intelligence Service` es un submodulo de este macro-sistema.

```text
State-of-the-Art Discovery Engine
  includes Model Intelligence
  includes Tool/Vendor Intelligence
  includes Cloud/Infra Intelligence
  includes Security/License Intelligence
  includes Buildability/Cost Intelligence
```

## Relacion con Oli Labs

Public lab recomendado:

```text
oli-state-of-art-advisor-lab
```

Demo:

- input: "Choose a local model for coding agent on RTX 4090"
- input: "Choose search API for agentic research"
- input: "Choose deployment option for n8n automation"

Output:

- evidence pack;
- ranked options;
- decision memo;
- cost/risk analysis;
- recheck date.

No revelar:

- private routing economics;
- vendor discounts;
- customer traces;
- proprietary playbooks.

## Que canonizar en TDD

Crear:

```text
tdd/adrs/ADR-025-state-of-art-discovery-and-decision-memos.md
tdd/domain/state-of-art-discovery.md
tdd/schemas/decision_memo.ts
tdd/domain/state-of-art-evals.md
```

Conectar con:

```text
tdd/domain/subagent-engineering.md
tdd/domain/model-intelligence.md
tdd/domain/tools-catalog.md
tdd/domain/oli-constitution.md
tdd/domain/mission-flows.md
```

## Eval plan

Fixtures:

- model selection;
- search API selection;
- cloud service selection;
- build-vs-buy decision;
- security-sensitive tool recommendation;
- frontend framework/library recommendation;
- automation workflow recommendation.

Metricas:

- source quality;
- freshness;
- alternative coverage;
- correctness;
- buildability;
- cost realism;
- risk coverage;
- actionability;
- human preference;
- later outcome tracking.

## Riesgos

1. Search APIs devuelven contenido SEO/AI-generated.
2. Citations pueden ser insuficientes o mal atribuidas.
3. Rankings externos no reflejan el caso de uso de Oli.
4. El sistema puede recomendar cambios demasiado frecuentes.
5. Vendor APIs pueden cambiar pricing/licencias.
6. "State of the art" puede volverse excusa para sobrecomplicar.

## Regla de control

```text
Oli recommends excellence, then lands it to constraints.
No recommendation is accepted until it passes buildability and risk checks.
```

## Siguiente decision

El siguiente paquete TDD no deberia ser otro subcaso.

Debe ser:

```text
ADR-025 + domain/state-of-art-discovery + decision_memo schema + eval plan
```

Despues, `ADR-024 Model Intelligence` puede colgar como submodulo especializado.
