# Auditoria V0 post-incidente

Fecha: 2026-05-31
Auditor: Codex como consultor estrategico
Motivo: Alejandro detecto que un chat nuevo de Codex arranco sin contexto suficiente y construyo V0.

## Veredicto

El V0 construido por el otro Codex no esta roto. La suite actual pasa:

```text
py -m pytest
45 passed
```

Pero el proceso que llevo a ese V0 si fue defectuoso: Codex no tenia un protocolo raiz cargado desde el inicio. La carpeta `Consultor Estrategico Codex` existia, pero sin `AGENTS.md` fuerte el siguiente chat podia ignorarla. Ese fue el fallo de sistema.

Veredicto tecnico:

- V0.3 es una base de desarrollo defendible.
- No es producto final.
- No debe avanzar a mas features hasta resolver persistencia real, checkpointing durable, evals y guardrails.

## Validacion contra lineamientos de Alejandro

### 1. Codex como consultor estrategico

Estado: parcialmente incumplido por proceso.

El otro Codex actuo como builder. Segun el tracking, Alejandro autorizo iniciar V0, por lo que la ejecucion puede estar permitida. El problema es que el arranque no garantizo lectura de contexto estrategico antes de ejecutar.

Correccion aplicada:

- Se creo `AGENTS.md` en raiz.
- Esta auditoria recomienda endurecerlo para obligar a leer contexto y generar un startup brief antes de tocar codigo.

### 2. Leer repo y respetar TDD

Estado: mayormente cumplido.

El orden construido coincide con `tdd/README.md`:

- `pyproject.toml`
- `packages/mission_kernel`
- `packages/orchestrator`
- `apps/api`
- `tests`

El Mission Kernel implementa estados, transiciones, permisos y eventos. La API expone misiones. Hay tests de acceptance.

### 3. Oli como supervisor, no agente suelto

Estado: cumplido en arquitectura minima.

Lo construido mantiene la idea de Mission Kernel + Orchestrator + suboperadores nominales. No es un agente autonomo suelto.

Limitacion:

- Los suboperadores aun son nombres en steps, no subgrafos reales independientes.
- `weekly-client-report` usa un grafo LangGraph minimo, no un sistema multiagente completo.

### 4. Audit ready

Estado: parcialmente cumplido.

Bien:

- Cada mision tiene eventos.
- Hay evidence refs.
- Hay report.
- Hay aprobaciones registradas.
- El model routing queda como evidencia en `weekly-client-report`.

Falta:

- No hay audit log inmutable.
- No hay tool calls/resultados con schema completo.
- No hay replay real.
- No hay costos reales del proveedor, solo estimados/simulados en varias rutas.

### 5. Permisos y aprobaciones

Estado: base correcta, con una tension a resolver.

Bien:

- `draft-outreach` clase 3 queda en `awaiting_approval`.
- La accion externa no se envia realmente en V0.
- Al aprobar se registra evidencia y se simula el punto de envio.

Tension:

- `policies.py` aprueba desde clase 2 (`RESOURCE_CONSUMING`), alineado con ADR-004.
- La Constitucion dice en un punto "clase 3+" como regla de parada.

Decision recomendada:

- Mantener ADR-004 como fuente tecnica: clase 2 requiere aprobacion al menos la primera vez por tipo; clase 3 y 4 siempre.
- Agregar politica configurable por usuario antes de V1.

### 6. Excelencia/state-of-the-art

Estado: mixto.

Bien:

- FastAPI + LangGraph + SQLAlchemy + Pydantic es coherente con el TDD.
- Se agrego Model Router y adapters, preparando local/API.
- Se probo OpenRouter.

Fallo relevante:

- Intento de instalar PostgreSQL 16 por lectura literal del TDD sin presentar primero la opcion state-of-the-art disponible: PostgreSQL 18. Alejandro corrigio esto correctamente.

Decision recomendada:

- `AGENTS.md` debe exigir que, ante tension entre TDD viejo y state-of-the-art actual, Codex presente ambas opciones con tradeoff antes de ejecutar.

### 7. No sobre-expandir V0

Estado: parcialmente incumplido.

El plan inicial recomendaba empezar pequeno: kernel + slice-001. El V0 termino incluyendo:

- API
- root HTML
- 3 mission classes
- JSON store
- SQLAlchemy store
- OpenRouter setup
- Model Router
- LangGraph
- scripts de runtime

Esto no es necesariamente malo, pero si es mas ancho que el primer corte recomendado.

Riesgo:

- Seguir agregando features antes de endurecer la columna vertebral.

Decision recomendada:

- Congelar features.
- Resolver Postgres + PostgresSaver + evals.

## Validacion tecnica por modulo

### Mission Kernel

Estado: bueno para V0.

Fortalezas:

- Estados principales implementados.
- Transiciones invalidas rechazadas.
- `failed` y `blocked` requieren reason.
- Eventos registrados.

Gaps:

- No implementa todos los campos del schema TS.
- `MissionSource` no incluye canales OpenClaw.
- `StepStatus` no incluye `repairing`, `repaired`, `repaired_partial`.
- No hay repair attempts por step.
- No hay tool calls/tool results dentro de steps.
- `CostRecord` esta simplificado frente al schema.

### Orchestrator

Estado: util para V0, no suficiente para V1.

Fortalezas:

- `research-brief-v1` cierra ciclo completo mock.
- `weekly-client-report-v1` apunta al ICP correcto: agencias y teams.
- `draft-outreach` prueba permiso clase 3 sin side effect real.

Gaps:

- Research no hace web real ni fuentes reales.
- Weekly report usa datos simulados.
- Suboperadores son estructuras nominales, no workers/grafos propios.
- No hay fault injection ni retries reales.

### LangGraph

Estado: minimo correcto.

Fortalezas:

- Grafo compila.
- Flujo de estados coincide con TDD para weekly report.
- Usa MemorySaver en desarrollo.

Gaps:

- No hay `PostgresSaver`.
- No hay interrupts reales persistentes.
- `human_approval_node` existe, pero no esta probado como pausa durable de LangGraph.
- No hay reanudacion tras reinicio.

### API

Estado: adecuada para V0 tecnico.

Fortalezas:

- Health.
- Crear/listar/get misiones.
- Eventos/evidencia/reporte.
- Approve/reject.
- Model status/test.

Gaps:

- No hay auth.
- No hay usuario/tenant.
- No hay SSE/realtime.
- No hay idempotency keys.
- Store global `_STORE` en import-time, suficiente para dev pero no ideal.

### Persistencia

Estado: dev-only.

Fortalezas:

- JSON store simple.
- SQLAlchemy store preparado.

Gaps:

- No hay Postgres real.
- No hay migraciones.
- No hay audit tables separadas.
- No hay pgvector.
- No hay transacciones alrededor de mission/event/evidence como unidades separadas.

### Model Router

Estado: buen stub auditable.

Fortalezas:

- Tiers por task.
- Privacy modes.
- Evidencia de routing.

Gaps:

- No hay registry persistente.
- No hay benchmark runner.
- No hay cost tracker real.
- Fallback puede ocultar fallas del proveedor si el usuario no revisa evidencia.

## Riesgos principales ahora

1. Confundir "45 tests passing" con producto listo.
2. Seguir ampliando mission classes antes de Postgres/checkpointing.
3. Usar datos simulados y creer que el moat ya fue probado.
4. No tener evals formales para calidad del output.
5. No tener tool guardrails reales antes de conectar herramientas externas.
6. No resolver la tension TDD literal vs state-of-the-art actualizado.
7. Que Codex/Claude sigan trabajando sin leer contexto raiz.

## Decision de control

Desde este punto:

- Ningun Codex debe tocar codigo de producto sin leer `AGENTS.md`.
- Ningun Codex debe tocar codigo de producto sin generar primero un startup brief.
- Ningun Codex debe avanzar features nuevas sin actualizar tracking.
- Para decisiones dependientes de versiones actuales, Codex debe verificar estado actual y presentar tradeoffs.

## Proxima accion recomendada

Actualizar `AGENTS.md` con:

1. Startup protocol obligatorio.
2. Regla de modo por defecto: consultor/auditor.
3. Regla de no ejecucion si no hay contexto.
4. Regla de congelamiento V0.
5. Estado actual del V0.
6. Comando de verificacion obligatorio: `py -m pytest`.
7. Fuentes de verdad a leer.

