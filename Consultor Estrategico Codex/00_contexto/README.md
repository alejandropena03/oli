# Consultor Estrategico Codex — Índice

Este espacio es la memoria estratégica y operativa de Codex como consultor de Oli.
Reorganizado: 2026-06-01.

## Estructura

```
00_contexto/             — Contexto vivo, protocolo, tracking, cierres de sesión, estado V0
01_auditorias/           — Auditorías de V0, post-incidente, reviews técnicos
02_estrategia_producto/  — ICP, runtime brief, skill signal, UX de ventas
03_runtime_y_arquitectura/ — Runtime SSH, dedicated runtime, memoria SOTA
04_subagents/            — Subagent engineering SOTA y contratos
05_research_stack/       — State-of-art discovery, OpenRouter, leverage open source, research_stack_v0
06_fine_tuning/          — Fine-tuning serio: análisis, pipeline, labs
07_presentaciones/       — HTMLs de presentación y pitch decks
08_assets/               — Imágenes y assets usados por documentos
09_probes_y_outputs/     — Outputs de probes y scripts (uso futuro)
99_archivo/              — Material antiguo o superado, sin borrar
```

## Reglas de uso

- Codex puede leer todo el repo para entender Oli.
- Codex solo crea o edita archivos dentro de esta carpeta salvo instrucción explícita de Alejandro.
- Rol principal: razonamiento — estrategia, producto, arquitectura, research, decisiones y tracking.
- Rol secundario: ejecución — solo cuando Alejandro lo pida claramente.

## Archivos clave de inicio de sesión

1. `00_contexto/00_contexto_vivo_codex.md` — qué es Oli y cómo trabaja Alejandro
2. `00_contexto/03_tracking_estrategico.md` — estado actual, decisiones, riesgos, próximos pasos
3. `01_auditorias/12_auditoria_v0_post_incidente_2026-05-31.md` — auditoría técnica del V0
4. `00_contexto/05_estado_v0_implementacion.md` — qué está implementado en V0

## Estado del proyecto (2026-06-01)

- V0.3 técnico: ✅ 45 tests pasando, API funcional, LangGraph, Model Router, SQLAlchemy store
- TDD: ✅ extendido — ADR-021, 022, 023, 025 + 5 domain docs + 2 schemas nuevos
- Postgres: ❌ pendiente — solucionable en Mac personal con Docker Desktop
- PostgresSaver: ❌ pendiente Postgres
- pgvector: ❌ pendiente Postgres
- Evals formales: ❌ solo en papel
- Commit del trabajo: ✅ commiteado 2026-06-01

## Próximo paso canónico

Mac personal con Docker Desktop:
1. docker run postgres:18
2. Configurar OLI_DATABASE_URL
3. Conectar PostgresSaver a LangGraph
4. py -m pytest verde contra Postgres real
5. Después: evals formales, tool guardrails, V1
