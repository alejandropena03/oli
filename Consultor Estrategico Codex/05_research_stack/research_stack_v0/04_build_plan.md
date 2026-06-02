# 04 - Build Plan

## Veredicto

No construir todo de una vez.

Primero construir el harness que permite probar si el research encuentra evidencia buena.

## Fase 0 - Manual but structured

Estado: ahora.

Hacer con Codex/humano:

- usar fuentes manualmente;
- llenar evidence pack;
- producir decision memo;
- registrar sources_failed.

Objetivo:

- aprender que fuentes faltan;
- definir contratos;
- crear eval fixtures.

## Fase 1 - Local harness

Construir scripts/adapters simples:

```text
research_stack_v0/
  connectors/
    web_search_stub
    github_api
    openrouter_docs
    tdd_reader
  schemas/
    evidence_record
    discovery_run
  evals/
    agent_usage_discovery
    coding_delegate_choice
```

Prioridad:

1. TDD reader.
2. OpenRouter docs/apps reader.
3. GitHub repo metadata reader.
4. Web search adapter.
5. Evidence pack writer.

No requiere Postgres al inicio. Puede escribir JSON/Markdown.

## Fase 2 - External APIs

Conectar:

- Brave o Tavily para search;
- Jina Reader para URL to Markdown;
- GitHub API;
- OpenRouter Models/Docs;
- Hugging Face Hub;
- Semantic Scholar/arXiv.

Output:

```text
DiscoveryRun.json
EvidencePack.md
DecisionMemo.md
```

## Fase 3 - Dedicated Runtime

Cuando exista runtime serio:

- Crawl4AI local;
- Firecrawl self-hosted o cloud;
- SearXNG si conviene privacy/costo;
- cache de fuentes;
- rate limit;
- source freshness scheduler.

## Fase 4 - Integration with Mission Kernel

Integrar con:

- Mission Black Box;
- memory;
- permission classes;
- Model Router;
- evals;
- playbook detection.

## Primera prueba contigo

Pregunta:

```text
Que herramientas open-source/SDK debe usar Oli para delegar coding tasks?
```

Oli Research Stack debe:

1. Consultar OpenRouter Apps.
2. Consultar GitHub.
3. Consultar docs oficiales de Claude Agent SDK, OpenCode y Kilo.
4. Consultar TDD ADR-016, ADR-020, ADR-021, ADR-023.
5. Producir evidence pack.
6. Producir recommendation.
7. Marcar que falta ejecutar spike.

## Segunda prueba

Pregunta:

```text
Que modelos locales convienen hoy para Starter/Pro/Team?
```

Debe:

1. Consultar OpenRouter Models.
2. Consultar Hugging Face.
3. Consultar benchmarks.
4. Consultar vLLM/Ollama.
5. Validar contra ADR-016.
6. No dar lista fija sin recheck.

## Tercera prueba

Pregunta:

```text
Que riesgos impiden conectar herramientas externas de alto impacto en V0?
```

Debe:

1. Consultar ADR-020.
2. Consultar security advisories/papers.
3. Revisar OpenClaw/Hermes-like risks.
4. Proponer mitigaciones.
5. Definir no-go conditions.

## Decision de suficiencia

El stack es suficiente para V0 si pasa las tres pruebas.

Si falla:

- si no encuentra fuentes: agregar connector;
- si encuentra fuentes malas: mejorar source ranking;
- si no decide bien: mejorar judge/rubric;
- si contradice TDD sin explicarlo: mejorar TDD validator.

