# Workflow de investigación: State of the Art

**Fecha:** 2026-05-26
**Propósito:** Cómo Oli investiga el estado del arte antes de construir algo técnico.
**Pilar que implementa:** "Construimos con excelencia" (Constitución, pilar 1)

---

## El problema

El conocimiento de entrenamiento de cualquier LLM tiene un corte.
Para Mayo 2026, ese corte puede tener 6-18 meses de retraso.
En el ecosistema de IA, 6 meses es una era completa.

Oli no puede confiar en lo que "sabe" para decisiones técnicas.
Tiene que verificar el estado actual antes de recomendar o construir.

---

## Las 5 fuentes del estado del arte

```
FUENTE              CICLO    LO QUE DA
──────────────────────────────────────────────────────────────────
GitHub trending     Diario   Qué se está construyendo y adoptando HOY
arXiv               Diario   Qué se está investigando — lo más nuevo
Exa / Tavily        Real-time Qué practitioners reales están publicando
npm / PyPI trending Semanal  Qué librerías están creciendo en uso
HN / Reddit         Diario   Qué adopta la comunidad real (signal real)
```

Ninguna fuente sola es suficiente.
La intersección de las 3 primeras = estado del arte real.

---

## Los MCP servers que habilitan este workflow

```python
RESEARCH_MCPS = {
    "github_official": "@github/github-mcp-server",
    # → buscar repos, ver README, comparar stars/actividad reciente

    "github_trending": "hetaoBackend/mcp-github-trending",
    # → repos trending por categoría y período (daily/weekly/monthly)

    "arxiv": "blazickjp/arxiv-mcp-server",
    # → papers recientes por tema, categoría, fecha

    "exa": "exa-labs/exa-mcp-server",
    # → search semántico en la web, ideal para "concepto" no keyword

    "tavily": "tavily-ai/tavily-mcp",
    # → search + extracción optimizado para LLMs, con fuentes

    "firecrawl": "mendableai/firecrawl-mcp-server",
    # → extrae contenido completo de páginas técnicas (docs, benchmarks)
}
```

---

## El workflow en 4 pasos

### Paso 1 — DETECTAR que la tarea requiere investigación

Trigger automático cuando:
- La tarea implica elegir una tecnología, librería o herramienta
- La tarea implica implementar algo con una "mejor práctica"
- El contexto menciona algo que tiene versiones o evoluciona rápido
- La última vez que Oli "sabe" algo de ese tema tiene > 3 meses de antigüedad en memoria

```python
def requires_state_of_art_research(task: str, context: MissionContext) -> bool:
    triggers = [
        "implementa", "construye", "elige", "mejor forma", "más reciente",
        "cómo hacer", "qué usar para", "state of the art", "best practice"
    ]
    # + verificar si la memoria tiene información reciente sobre el tema
    memory_freshness = context.get_topic_freshness(extract_topic(task))
    return any(t in task.lower() for t in triggers) or memory_freshness > 90  # días
```

### Paso 2 — LANZAR research en paralelo (3 threads simultáneos)

```python
async def research_state_of_art(topic: str) -> ResearchResult:

    # Thread A: GitHub — qué se está construyendo
    github_task = asyncio.create_task(
        github_trending_mcp.search({
            "query": topic,
            "period": "weekly",
            "min_stars": 500,
            "language": relevant_language
        })
    )

    # Thread B: arXiv — qué se está investigando
    arxiv_task = asyncio.create_task(
        arxiv_mcp.search({
            "query": topic,
            "date_from": "3 months ago",
            "sort_by": "citations",
            "max_results": 5
        })
    )

    # Thread C: Web — qué practioners reales dicen
    web_task = asyncio.create_task(
        exa_mcp.search({
            "query": f"{topic} best practice 2026",
            "num_results": 8,
            "include_domains": ["dev.to", "substack.com", "engineering blogs"],
            "date_from": "6 months ago"
        })
    )

    github_results, arxiv_results, web_results = await asyncio.gather(
        github_task, arxiv_task, web_task
    )

    return ResearchResult(
        github=github_results,
        arxiv=arxiv_results,
        web=web_results,
        researched_at=datetime.now()
    )
```

### Paso 3 — SINTETIZAR en < 30 segundos

El TechnicalArchitectSuboperator sintetiza los hallazgos:

```
Input: ResearchResult (GitHub + arXiv + Web)
Output:
  current_best: "La mejor opción actual es X por [razón con evidencia]"
  emerging: "Y está ganando tracción — no es mainstream aún pero vale vigilar"
  deprecated: "Z era estándar hasta hace 6 meses, ya no se recomienda porque..."
  sources: [lista de fuentes con fecha]
  confidence: high | medium | low
  freshness: "información de los últimos N días"
```

### Paso 4 — DECIDIR y documentar

```
SI la investigación confirma la decisión existente:
  → Continúa con la tarea
  → Actualiza Memory: "verificado [fecha]: X sigue siendo el estado del arte"

SI la investigación cambia la decisión:
  → Propone al founder: "Encontré que cambió el estado del arte. 
    Antes: [lo que teníamos]. Ahora: [lo nuevo]. 
    Recomiendo actualizar el TDD y usar el nuevo enfoque. ¿Confirmas?"
  → Si el founder confirma → actualiza el ADR correspondiente
  → Ejecuta con el enfoque nuevo
```

---

## Ejemplo real: Ollama vs vLLM (prueba ejecutada 2026-05-26)

Esta es la primera ejecución real del workflow para validar el TDD.

**Pregunta:** ¿Sigue siendo correcto el ADR-005 que dice "Ollama V0-V2, vLLM V3+"?

**Resultado de la investigación:**

| Aspecto | Lo que el TDD asumía | Lo que la investigación encontró |
|---|---|---|
| Brecha de rendimiento | vLLM es "más rápido" | 19x diferencia en throughput pico. Para equipo (ADR-018), Ollama se queda corto antes |
| Alternativas | Solo Ollama y vLLM | **SGLang** emergió — comparable a vLLM, más simple de operar |
| Abstracción | No mencionado | **LocalAI** puede abstraer ambos — Oli llama a un API, LocalAI decide el runtime |
| macOS support | No mencionado | **vLLM es Linux-only** — el founder que desarrolla en Mac necesita Ollama siempre |

**Decisión actualizada:**

```
DESARROLLO (Mac):
  Ollama → inamovible, única opción en macOS/Apple Silicon

PRODUCCIÓN V0-V1 (single user / equipo pequeño):
  Ollama → suficiente para < 5 usuarios simultáneos

PRODUCCIÓN V2+ (equipo real, múltiples usuarios simultáneos):
  vLLM O SGLang → throughput real
  Recomendación: evaluar SGLang primero (más simple, benchmarks comparables)

ABSTRACCIÓN (recomendación nueva):
  LocalAI como capa de API unificada
  → Oli llama a LocalAI (OpenAI-compatible API)
  → LocalAI decide el backend según la carga
  → Cambiar de Ollama a vLLM no requiere cambiar código de Oli
```

**ADR afectado:** ADR-005 — se agrega LocalAI como capa de abstracción recomendada.
**Hotspot resuelto:** Oli en macOS siempre usa Ollama para desarrollo local.

---

## La skill y el workflow

La skill `/oli` por sí sola **no puede ejecutar este workflow** sin los MCP servers de investigación conectados.

Cuando los MCP servers estén disponibles:
- La skill sabe cuándo activar el workflow (trigger detection)
- La skill sabe qué fuentes consultar (los 5 MCPs)
- La skill sabe cómo sintetizar (TechnicalArchitectSuboperator)
- La skill sabe cómo documentar el hallazgo (actualizar ADR + Memory)

Sin los MCPs: la skill responde con conocimiento de entrenamiento marcando explícitamente:
`[REQUIERE VERIFICACIÓN — este dato tiene potencialmente > 3 meses de antigüedad]`

---

## Frecuencia de re-investigación

| Tipo de dato | Re-investigar cada |
|---|---|
| Versiones de librerías | Antes de cada build que toque esa librería |
| Benchmarks de rendimiento | Cada 3 meses |
| Mejores prácticas de arquitectura | Cada 6 meses |
| Herramientas del ecosistema | Cuando alguien menciona algo nuevo |
| Precios de APIs/GPU | Antes de cada decisión de pricing |
