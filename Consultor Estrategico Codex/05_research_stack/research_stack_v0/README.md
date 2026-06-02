# Research Stack v0 para Oli

Fecha: 2026-05-31

## Veredicto

Para V0, el stack de research de Oli debe venir preestablecido con conectores suficientes para investigar decisiones actuales sin depender de memoria vieja ni de una sola busqueda web.

No es "un buscador". Es un subsistema:

```text
Research request
  -> clasificar pregunta
  -> elegir fuentes
  -> buscar y leer
  -> guardar evidencia
  -> puntuar fuentes
  -> validar contra TDD/memoria
  -> escribir decision memo
  -> definir recheck date
```

## Archivos

- `01_connector_registry.md` - conectores base y para que sirve cada uno.
- `02_research_workflow.md` - como Oli decide donde buscar y como produce evidencia.
- `03_evals_and_test_plan.md` - pruebas para saber si el research funciona.
- `04_build_plan.md` - que construir primero y que dejar para despues.

## Stack base recomendado

1. Web search y lectura web: Brave, Tavily, Exa, Jina Reader, Firecrawl, Crawl4AI, DuckDuckGo/SearXNG.
2. Codigo y open source: GitHub API, GitHub search/issues/releases, GitHub Security Advisories.
3. Modelos y agentes: OpenRouter, Hugging Face Hub, Artificial Analysis, LMArena/Arena.
4. Papers y literatura tecnica: Semantic Scholar, arXiv, OpenAlex.
5. Seguridad: NVD/CVE, GitHub Advisories, vendor security blogs, papers de seguridad.
6. Contexto interno: TDD local, memoria de Oli, decisiones previas, Mission Black Box.

## Regla central

Cada fuente tiene un rol. Ninguna fuente decide sola.

```text
OpenRouter Apps -> uso real
GitHub -> codigo, actividad, licencia, issues
Docs oficiales -> comportamiento esperado
Benchmarks -> capacidad comparativa
Papers -> frontera tecnica
Security feeds -> riesgos
TDD/memoria -> fit con Oli
```

## Suficiencia

Este stack es suficiente para V0 si cada decision importante consulta al menos dos tipos de fuente y produce evidencia trazable.

No es suficiente si:

- solo se consulta web search;
- no se consulta fuente oficial;
- no se revisa licencia/codigo para open source;
- no se valida contra el TDD;
- no se guarda que fuentes fallaron.

