# Model Intelligence y state-of-the-art discovery para Oli

Fecha: 2026-05-31
Rol: Codex como consultor estrategico/auditor

## Veredicto

Oli no debe decidir "que modelo instalar" con una lista fija.

Oli debe tener una capacidad permanente:

```text
Model Intelligence Service
  + source connectors
  + model registry
  + hardware fit estimator
  + local benchmark runner
  + tier policy
  + rollout/rollback
```

El "llm-advisor MCP" es una buena interfaz para esa capacidad, pero no debe ser la fuente de verdad. La fuente de verdad debe ser un registry interno versionado que combina fuentes externas, benchmarks propios y costo real por tier.

## Correccion a la intuicion inicial

La pregunta correcta no es:

```text
Que modelo open-source local es mejor hoy?
```

La pregunta correcta es:

```text
Para cada tier, hardware, privacy mode, mission class y role,
que modelo/adaptador/runtime maximiza calidad, costo, latencia, contexto efectivo,
licencia y confiabilidad operativa?
```

Eso cambia todo.

## Por que esto importa para Oli

Model selection es parte del moat:

- reduce costo por mision;
- mejora margen;
- evita depender de APIs frontier;
- mantiene a usuarios en el mejor modelo disponible;
- permite upgrades sin que el usuario piense en modelos;
- alimenta Model Router;
- puede convertirse en ventaja publica de Oli Labs;
- refuerza "construimos con excelencia".

Si Oli se queda con modelos fijos del TDD, envejece en semanas.

## Evaluacion de la propuesta "llm-advisor MCP"

La idea es correcta, pero incompleta.

### Lo bueno

- Codex/Oli razona mejor con datos estructurados.
- Un MCP permite consultar estado actual sin depender de memoria vieja.
- Las decisiones de modelo necesitan cruzar benchmarks, contexto, hardware, licencia y costo.
- Seria muy valioso para mantenimiento automatico de runtimes.

### Lo que falta

No basta con APIs externas:

- rankings externos son ruidosos;
- benchmarks pueden estar contaminados;
- context window declarada no equivale a contexto efectivo;
- "popular en OpenRouter" no significa "mejor para Oli";
- Hugging Face metadata puede estar incompleta;
- algunas fuentes tipo blogs/SEO agregan ruido;
- modelos locales deben probarse en el hardware real con el runtime real.

Conclusion:

```text
llm-advisor debe recomendar candidatos.
BenchmarkRunner de Oli debe decidir promocion real.
```

## Fuentes que Oli debe consultar

### Tier 1 - Fuentes fuertes

Usar como señales primarias:

- OpenRouter Models API: metadata, context length, pricing, supported parameters, tool/structured output support.
- OpenRouter Rankings: uso real y tool-call usage dentro del ecosistema OpenRouter.
- Hugging Face Hub/API: model cards, license, downloads, eval results, model metadata.
- LMArena/Arena: preferencia humana, incluyendo ranking de code/document cuando aplique.
- Artificial Analysis: calidad/costo/velocidad/contexto cuando este disponible.
- Model technical reports y model cards oficiales.
- vLLM docs/runtime support: serving, quantization, LoRA, tool calling, OpenAI-compatible API.
- Ollama docs/library: solo para dev/local/simple mode, no runtime canonico de produccion.

### Tier 2 - Fuentes utiles pero no autoridad

Usar como señales secundarias:

- BenchLM;
- WhatLLM;
- LLM Stats;
- community leaderboards;
- Reddit/LocalLLaMA;
- blog posts comparativos.

Regla:

```text
Una fuente secundaria nunca promociona un modelo por si sola.
Solo dispara investigacion o benchmark.
```

### Fuentes a tratar con cuidado

- posts con `utm_source=chatgpt.com`;
- rankings sin metodologia clara;
- paginas SEO;
- claims de contexto extremo sin hardware/runtime;
- claims de "best coding model" sin version exacta y benchmark reproducible.

## Datos que debe guardar el Model Registry

El ADR-016 ya define un buen inicio, pero debe ampliarse.

Campos recomendados:

```yaml
model_registry_entry:
  model_id: string
  canonical_name: string
  provider: ollama | vllm | openrouter | anthropic | openai | google | custom
  family: qwen | llama | deepseek | kimi | gemma | mistral | glm | other
  modality:
    - text
    - vision
    - embeddings
  open_weight: boolean
  license:
    name: string
    commercial_allowed: boolean | unknown
    restrictions: string[]
    source_url: string
  context:
    advertised_tokens: number | null
    provider_context_tokens: number | null
    effective_context_tokens_by_runtime:
      ollama: number | null
      vllm: number | null
    context_reliability_score: number
  capabilities:
    tool_calling: low | medium | high | unknown
    structured_outputs: low | medium | high | unknown
    coding: number | null
    reasoning: number | null
    long_context: number | null
    multilingual: number | null
    data_analysis: number | null
    agentic_reliability: number | null
  hardware_fit:
    min_vram_gb_by_quant:
      q4: number | null
      q5: number | null
      q8: number | null
      fp16: number | null
    recommended_runtime: vllm | ollama | llama_cpp | tgi | other
    tested_gpu_profiles:
      - rtx_4090_24gb
      - a6000_48gb
      - h100_80gb
  performance:
    tokens_per_sec: number | null
    prefill_tokens_per_sec: number | null
    p50_latency_ms: number | null
    p95_latency_ms: number | null
    max_concurrency_tested: number | null
  economics:
    local_gpu_cost_per_1m_tokens_estimate: number | null
    api_input_cost_per_1m: number | null
    api_output_cost_per_1m: number | null
  source_signals:
    openrouter_rank: number | null
    openrouter_usage_share: number | null
    arena_score: number | null
    artificial_analysis_score: number | null
    hf_downloads_30d: number | null
    hf_likes: number | null
  oli_benchmarks:
    intent_classification: number | null
    structured_json_output: number | null
    tool_call_formatting: number | null
    memory_extraction: number | null
    short_coding_task: number | null
    repo_reasoning: number | null
    long_context_retrieval: number | null
    validation_repair: number | null
    mission_trace_summary: number | null
  status: discovered | candidate | installed | benchmarked | canary | promoted | disabled | deprecated
  last_refreshed_at: datetime
  last_benchmarked_at: datetime | null
```

## Roles de modelo para Oli

No seleccionar por "mejor modelo general". Seleccionar por rol:

- `FAST_LOCAL`: clasificacion, routing, extraccion simple.
- `MAIN_LOCAL`: planning, reportes, coding ligero, sintesis.
- `LONG_CONTEXT_LOCAL`: analisis largo cuando el hardware lo soporte.
- `CODING_LOCAL`: repo reasoning, specs, patches simples.
- `JUDGE_LOCAL`: validation barata cuando no hay riesgo alto.
- `EMBEDDING`: memoria semantica.
- `VISION`: screenshots/docs.
- `PREMIUM_REASONING`: decisiones criticas.
- `PREMIUM_CODING`: coding de alta precision.
- `PREMIUM_LONG_CONTEXT`: cuando contexto local efectivo no alcanza.

## Criterio por tier

### Starter - RTX 4090 clase, 24GB

Objetivo:

- buen modelo local principal;
- contexto efectivo moderado;
- buen costo;
- fallback premium cuando la mision lo justifique.

No prometer 1M local. En 24GB, el contexto largo real se paga en KV cache, prefill lento y degradacion.

### Pro - A6000 clase, 48GB

Objetivo:

- modelo local mas fuerte;
- mejor contexto efectivo;
- mejor coding/reasoning local;
- mas concurrencia;
- menos fallback premium.

### Team - H100 clase, 80GB

Objetivo:

- mejor open-weight disponible por rol;
- serving serio con vLLM;
- LoRA adapters cuando existan;
- mayor contexto efectivo;
- benchmark/canary mas frecuente.

## Context window: regla importante

Contexto declarado no es contexto util.

Oli debe medir:

- advertised context;
- provider/runtime enforced context;
- KV cache memory cost;
- prefill latency;
- retrieval accuracy en contexto largo;
- calidad al final del contexto;
- costo por mision;
- si RAG/context packets resuelven mejor que meter 1M tokens.

Regla:

```text
Para agentes, contexto efectivo + retrieval + context engineering
vale mas que contexto maximo declarado.
```

Una API gratuita con 1M contexto sirve para pruebas, no como pilar de producto. Puede cambiar, tener limites, routing opaco, privacidad incierta o desaparecer.

## Workflow recomendado

### 1. Discovery diario

Recolectar metadata:

- OpenRouter models API;
- OpenRouter rankings;
- Hugging Face Hub/model cards;
- Arena leaderboard;
- Artificial Analysis;
- vLLM/Ollama/runtime compatibility;
- model release feeds.

Salida:

```text
new_model_candidates
model_updates
license_changes
deprecations
price_changes
context_changes
```

### 2. Scoring semanal

Actualizar candidate score por rol:

```text
role_score = weighted external signals + fit filters
```

Ejemplo para `CODING_LOCAL`:

```text
repo_reasoning expected 30%
coding benchmark signals 25%
context effective 20%
vram fit 15%
license/commercial 10%
```

Ejemplo para `AGENTIC_MAIN_LOCAL`:

```text
tool/structured outputs 25%
context effective 25%
Oli mission evals 25%
latency/cost 15%
license/privacy 10%
```

### 3. Benchmark interno

Solo candidatos top pasan a benchmark en hardware real:

- RTX 4090 profile;
- A6000 profile;
- H100 profile.

Benchmarks Oli:

- intent classification;
- structured JSON;
- tool call formatting;
- context packet following;
- memory extraction;
- repo reasoning;
- mission trace summary;
- validation/repair;
- long-context retrieval;
- latency/cost.

### 4. Canary

Instalar en un runtime no critico o en subset de misiones:

- 5-10% de misiones internas/sinteticas;
- comparar contra modelo promovido actual;
- capturar regressions.

### 5. Promotion

Promocionar por rol y tier:

```text
Starter MAIN_LOCAL -> model A
Pro MAIN_LOCAL -> model B
Team MAIN_LOCAL -> model C
Team LONG_CONTEXT_LOCAL -> model D
```

### 6. Rollback

Cada modelo promovido debe tener:

- previous model;
- reason promoted;
- eval delta;
- known failures;
- rollback trigger.

## Cadencia recomendada

```text
Daily: discovery metadata
Weekly: score refresh + candidate shortlist
Monthly: benchmark top candidates
Quarterly: tier model refresh
Ad hoc: urgent update for security, license, pricing, or major model release
```

Trimestral para usuarios es sensato. Internamente Oli puede descubrir diario, pero no debe cambiar el modelo del usuario cada dia. Eso rompe reproducibilidad.

## MCP / tool interface recomendada

Nombre:

```text
model-intelligence
```

Herramientas:

```text
list_model_candidates(role, tier, privacy_mode)
get_model_metadata(model_id)
get_model_benchmarks(model_id)
get_model_context_profile(model_id, runtime, hardware_profile)
get_model_license(model_id)
estimate_hardware_fit(model_id, hardware_profile, quantization, context_tokens)
recommend_model(role, tier, mission_class, privacy_mode)
compare_models(model_ids, role, tier)
explain_model_decision(decision_id)
```

Importante:

```text
El MCP no decide solo.
El MCP expone datos y recomendaciones.
El Model Router decide en runtime bajo policy.
```

## TDD que deberia crearse

Recomendacion:

1. Crear ADR:

```text
tdd/adrs/ADR-024-model-intelligence-and-runtime-model-selection.md
```

2. Crear domain spec:

```text
tdd/domain/model-intelligence.md
```

3. Extender schema:

```text
tdd/schemas/model_registry.ts
```

4. Crear eval plan:

```text
tdd/domain/model-selection-evals.md
```

5. Actualizar:

```text
tdd/adrs/ADR-016-model-routing-gpu-strategy.md
tdd/domain/setup-wizard-spec.md
tdd/stack/stack-decision.md
```

## Decision recomendada

Canonizar este pendiente como:

```text
Model Intelligence and Runtime Model Selection
```

No como "llm-advisor MCP" solamente.

El MCP es una interfaz. La capacidad real es:

```text
Oli siempre sabe que modelos existen,
que caben en cada tier,
que licencia tienen,
como rinden en sus propias misiones,
y cuando conviene actualizar el runtime del usuario.
```

## Fuentes verificadas

- OpenRouter Models API documenta metadata por modelo: `context_length`, pricing, architecture, supported parameters y provider details.
- OpenRouter Rankings dice que combina benchmarks y uso real de millones de usuarios en OpenRouter.
- Hugging Face Leaderboards/Evaluations separa eval results, community leaderboards y Open LLM Leaderboard como proyecto curado para evaluar modelos open-source.
- Arena/LMArena expone rankings por Text, Code, Vision y Document basados en preferencia/votaciones.
- vLLM docs confirman OpenAI-compatible serving, APIs de chat/completions y soporte de features como LoRA/quantization/tool calling.
- Ollama docs confirman que context length es configurable y dependiente de memoria/runtime, por lo que no basta con leer el nombre del modelo.

