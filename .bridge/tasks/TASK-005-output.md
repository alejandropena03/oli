# TASK-005 — Output con OpenRouter + owl-alpha

## Misión
**ID:** a7d25919-9fb2-436a-a8d1-2f0729833843
**Status:** failed (validación: 2/4 criteria)
**Modelo real usado:** Sí — vía OpenRouter (owl-alpha)
**Evidencia:** `model_adapter: "fallback"`, `model_provider_used: "openai_compatible"`

## ¿El modelo interpretó la petición del cockpit?
**NO.** El orchestrator de `research-brief` tiene la intención hardcodeada como `competitor_research_brief`. Ignoró completamente el `raw_input`: "Quiero un cockpit donde todas mis herramientas de comunicacion: WhatsApp, Slack, Gmail e Instagram..."

En lugar de eso, el pipeline:
1. Identificó competidores (Lindy, Dust, Claude Projects) — datos mock
2. Le pasó eso al modelo real para sintetizar
3. owl-alpha generó un brief detallado de 742 palabras sobre esos 3 competidores

## Qué produjo el modelo real
Un brief competitivo bien escrito sobre Lindy, Dust y Claude Projects, con:
- Análisis de cada competidor (features, strengths, weaknesses)
- Matriz comparativa
- Recomendaciones estratégicas para Oli

El texto no tiene nada que ver con WhatsApp, Slack, Gmail o Instagram. El modelo nunca recibió el input real.

## Diferencia con TASK-004 (mock)

| Aspecto | TASK-004 (DevelopmentAdapter) | TASK-005 (OpenRouter owl-alpha) |
|---|---|---|
| Output textual | 132 palabras genéricas | 742 palabras, bien estructurado |
| Calidad del texto | Baja — placeholder | Alta — análisis real |
| Relevancia al input | Ninguna | Ninguna (mismo problema) |
| Validación | Score 1.0 (pasó) | Score 0.5 (falló: 742 > 600) |
| Provider | `development_codex_authored` | `openai_compatible` (OpenRouter) |
| Pipeline | Mismo | Mismo |

## Conclusión
OpenRouter + owl-alpha funciona. El modelo produce texto de calidad. Pero el **orchestrator es el cuello de botella**: no pasa el input del usuario al modelo. Hasta que eso se arregle, Oli no puede responder a lo que Alejandro le pide.
