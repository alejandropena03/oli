# State-of-the-Art Discovery Probe v0

Fecha: 2026-05-31
Rol: Codex como consultor estrategico/auditor

## Veredicto

El problema no fue solo no conocer Hermes.

El problema real es que el discovery de Oli todavia no existe como sistema. Existe como:

```text
usuario exige investigacion
  -> Codex navega/busca manualmente
  -> Codex sintetiza
  -> se guarda un memo
```

Eso no es suficiente para Oli.

Oli necesita:

```text
source registry
  -> source connectors
  -> evidence extraction
  -> freshness scoring
  -> source quality ranking
  -> decision memo
  -> recheck schedule
  -> evals contra fallos conocidos
```

Si Oli va a vender "decisiones state-of-the-art", debe poder demostrar que busca mejor que un humano con prisa.

## Objetivo del probe

Probar si podemos responder tres preguntas con evidencia, no con intuicion:

1. Que agentes/apps tienen uso real hoy?
2. Que podemos extraer de ellos para Oli?
3. Que riesgos recientes cambian la recomendacion?

Este probe no busca construir producto. Busca validar el workflow que despues Oli debe automatizar.

## Herramientas/fuentes probadas

### 1. OpenRouter docs index

Estado: funciona.

Se descargo:

```text
https://openrouter.ai/docs/llms.txt
```

Archivo local:

```text
openrouter_docs.txt
```

Uso:

- descubrir paginas oficiales relevantes;
- ubicar docs de routing, app attribution, model routing, coding agents;
- servir como indice local para futuras sesiones.

Limitacion:

- no contiene ranking de apps;
- no reemplaza `https://openrouter.ai/apps`.

### 2. OpenRouter Apps via web search/open

Estado: funciona parcialmente.

Hallazgos confirmados por busqueda web:

- OpenRouter Apps se describe como ranking de apps/agentes que optan por usage tracking.
- Hermes aparece como app/agente de alto volumen.
- OpenClaw, Kilo Code y Claude Code aparecen como agentes relevantes en la pagina de apps.
- La pagina de OpenRouter Spawn tambien lista OpenClaw, Kilo Code y otros agentes como herramientas relevantes.

Dato de prueba capturado:

```text
Hermes: ~9.9T tokens
OpenClaw: ~6.25T tokens
Kilo Code: ~4.76T tokens
Claude Code: ~2.23T tokens
```

Nota:

Estos valores son senal de uso, no prueba de calidad.

### 3. OpenRouter App Attribution

Estado: funciona.

Uso:

- explica por que las apps aparecen en rankings;
- valida que el ranking depende de apps que se atribuyen con headers;
- importante para interpretar sesgo de seleccion.

Implicacion:

OpenRouter Apps no muestra "todo el mercado"; muestra apps que optan por atribucion o integracion visible.

### 4. GitHub public repo metadata

Estado: parcial.

Funciono:

- Hermes via GitHub API.

Fallo/parcial:

- Algunas aperturas directas a `api.github.com` fueron bloqueadas por la herramienta web salvo URLs ya vistas en busqueda.
- La busqueda web si encontro repos de OpenCode, Kilo Code y OpenHands.

Dato Hermes capturado previamente:

```text
repo: NousResearch/hermes-agent
license: MIT
language: Python
created_at: 2025-07-22
updated/pushed: 2026-05-31
stars: ~174k
forks: ~29k
open issues: ~15k
```

Nota critica:

Los numeros publicos de GitHub pueden estar inflados o ser anomalos. No se decide por stars.

### 5. Repo/TDD local search

Estado: funciona.

Se uso `rg` para validar contra:

- ADR-001 Model Strategy
- ADR-016 Model Routing / Agent Router
- ADR-019 Mission Black Box
- ADR-020 Tool Security
- ADR-021 Dedicated Oli Runtime
- ADR-023 Subagent Engineering
- ADR-025 State-of-the-Art Discovery

Fallo:

- `tdd/adrs/ADR-013-openclaw-integration.md` devolvio `Acceso denegado` incluso con intento elevado.

Implicacion:

Hay que revisar permisos del archivo si se va a usar como fuente canonica.

## Resultado del probe

### Pregunta 1: Que agentes/apps tienen uso real?

Respuesta v0:

OpenRouter Apps debe ser fuente obligatoria para detectar agentes con uso real. En este probe emergieron:

- Hermes;
- OpenClaw;
- Kilo Code;
- Claude Code;
- OpenCode;
- Pieces;
- Cursor/Codex/Gemini CLI/Windsurf/Devin como referencias de categoria.

Conclusion:

Nuestro discovery anterior no debio depender solo de frameworks conocidos. Debio consultar:

```text
OpenRouter Apps
GitHub repos/activity
official docs
security reports
benchmarks/evals
community pain signals
```

### Pregunta 2: Que podemos extraer?

Respuesta v0:

No se extrae producto. Se extraen patrones:

- runtime sessions;
- tool loop;
- permission modes;
- prompt layers;
- coding patch loop;
- LSP diagnostics;
- channel gateway;
- skills/playbooks;
- sandbox/checkpointing;
- provider abstraction;
- app attribution/usage telemetry;
- security controls.

Estos patrones se mapearon en:

```text
21_open_source_agent_leverage_review_v1_2026-05-31.md
```

### Pregunta 3: Que riesgos recientes cambian la recomendacion?

Respuesta v0:

OpenClaw-like systems elevan riesgo por:

- multi-channel gateway;
- memoria persistente;
- skills/plugins;
- acciones reales;
- credenciales;
- autonomia creciente;
- usuarios no tecnicos.

Eso obliga a endurecer ADR-020 antes de conectar herramientas de impacto externo.

## Workflow correcto para Oli

```text
User asks a current technical decision
  -> DecisionClassifier
  -> SourcePlanner
  -> SourceRegistry lookup
  -> EvidenceRetriever
       - OpenRouter Apps
       - OpenRouter docs
       - GitHub API
       - official docs
       - papers/security advisories
       - benchmarks
       - community signals
  -> EvidenceNormalizer
  -> SourceQualityScorer
  -> OptionGenerator
  -> TDDValidator
  -> RiskChecker
  -> Cost/BuildabilityChecker
  -> DecisionMemoWriter
  -> RecheckScheduler
```

## Contrato minimo

### SourceConnector

```ts
type SourceConnector = {
  id: string
  source_type:
    | "official_docs"
    | "usage_ranking"
    | "github_repo"
    | "benchmark"
    | "paper"
    | "security_advisory"
    | "community_signal"
  freshness_policy_days: number
  trust_tier: "A" | "B" | "C" | "D"
  fetch(query: DiscoveryQuery): Promise<EvidenceRecord[]>
}
```

### EvidenceRecord

```ts
type EvidenceRecord = {
  source_id: string
  url: string
  title: string
  captured_at: string
  published_at?: string
  claim: string
  evidence_type:
    | "fact"
    | "usage_signal"
    | "benchmark"
    | "security_risk"
    | "license"
    | "implementation_detail"
    | "community_report"
  confidence: "high" | "medium" | "low"
  limitations: string[]
}
```

### DiscoveryRun

```ts
type DiscoveryRun = {
  id: string
  question: string
  decision_type: string
  sources_planned: string[]
  sources_used: string[]
  sources_failed: { source_id: string; reason: string }[]
  evidence_records: EvidenceRecord[]
  options: DecisionOption[]
  tdd_validation: TDDValidation
  recommendation: DecisionRecommendation
  recheck_date: string
}
```

## Evals para saber si funciona

Crear fixtures donde ya sabemos que el discovery deberia encontrar ciertas cosas.

### Eval 1: Agent usage discovery

Pregunta:

```text
Que agentes de IA open/source o developer agents tienen uso real alto actualmente?
```

Debe encontrar:

- OpenRouter Apps;
- Hermes;
- OpenClaw;
- Kilo Code;
- Claude Code;
- OpenCode;
- al menos una limitacion del ranking.

Falla si:

- solo menciona LangGraph/CrewAI/AutoGen;
- no usa fuentes de demanda real;
- no separa uso de calidad.

### Eval 2: Coding delegate choice

Pregunta:

```text
Que conviene para Oli: Claude Agent SDK o OpenCode?
```

Debe responder:

- Claude Agent SDK como delegate premium;
- OpenCode como benchmark/local delegate/pattern source;
- no vendor lock-in;
- Mission Black Box obligatorio;
- PermissionClass obligatorio.

Falla si:

- recomienda uno universalmente;
- ignora costo/privacidad;
- no valida contra TDD.

### Eval 3: Agent security risk

Pregunta:

```text
Que riesgos actuales tienen agentes multi-channel con tools y memoria persistente?
```

Debe encontrar:

- prompt injection;
- SSRF/network abuse;
- credential leakage;
- plugin/skill poisoning;
- supply-chain risk;
- memory poisoning;
- approval bypass;
- command execution risk.

Falla si:

- solo dice "usar sandbox";
- no conecta riesgos a permisos/evidence/audit.

## Spike comparativo recomendado

### Hipotesis

Oli puede ahorrar desarrollo si delega coding premium a Claude Agent SDK y usa OpenCode como delegate local/patron, siempre que ambos pasen por un contrato comun.

### Fixture

```text
Repo: modulo pequeno de Oli o repo sandbox
Task: bug/fix de 1-3 archivos
Expected: tests pasan y se genera diff
Permission ceiling: class_1 o class_2 segun si modifica archivos
```

### Rutas

```text
Route A: Claude Agent SDK delegate
Route B: OpenCode-like local delegate
```

### Output obligatorio

```text
DelegateRunReport:
  - task
  - input context
  - model/provider
  - tools used
  - files read
  - files modified
  - commands run
  - diff
  - tests
  - cost
  - latency
  - permission decisions
  - failures
  - final recommendation
```

### Scoring

| Dimension | Weight |
|---|---:|
| Patch correctness | 30% |
| Test pass | 20% |
| Evidence completeness | 15% |
| Permission compliance | 15% |
| Cost/latency | 10% |
| Ease of integration | 10% |

### Decision rule

```text
Si Claude gana calidad pero pierde costo/control:
  usarlo como Tier 3 premium delegate.

Si OpenCode gana control/costo pero pierde calidad:
  usarlo como local delegate o pattern source.

Si ambos fallan evidence/permissions:
  no integrar; primero construir Delegate Contract.
```

## Que herramientas faltan conectar

Minimo:

1. GitHub API connector
   - repo metadata;
   - releases;
   - commits;
   - issues;
   - license;
   - file tree.

2. OpenRouter connector
   - docs index;
   - app attribution docs;
   - apps/rankings page extraction;
   - models API;
   - pricing/context/tool support.

3. Paper/security connector
   - arXiv;
   - GitHub Security Advisories;
   - vendor security blogs;
   - CVE/NVD when applicable.

4. Benchmark connector
   - LMArena;
   - Artificial Analysis;
   - SWE-bench/LiveCodeBench when relevant;
   - provider official model cards.

5. Local TDD connector
   - ADR retrieval;
   - domain docs retrieval;
   - schema retrieval;
   - "does this conflict with TDD?" validator.

## Decision recomendada

No avanzar a mas TDD todavia.

Primero hacer el harness minimo:

```text
state_of_art_discovery_probe_v0
```

Debe producir:

- `DiscoveryRun`;
- `EvidenceRecord[]`;
- `DecisionMemo`;
- `sources_failed`;
- `recheck_date`.

Luego correrlo con los tres evals anteriores.

Si pasa, se canoniza:

```text
tdd/domain/open-source-leverage.md
tdd/schemas/leverage_review.ts
```

Si no pasa, se corrige el discovery antes de prometerlo como capacidad de Oli.

## Conclusion

La mejora no es "buscar mejor una vez".

La mejora es que Oli tenga una disciplina:

```text
current source discovery
  + evidence pack
  + TDD validation
  + risk/buildability check
  + evals
  + recheck schedule
```

Sin eso, Oli recomendaria como cualquier chatbot. Con eso, Oli empieza a comportarse como operador serio.

