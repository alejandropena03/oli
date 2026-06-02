# Estado V0 implementacion

Fecha: 2026-05-30
Autor: Codex
Estado: V0.3 tecnico aceptable en modo desarrollo, no producto final

## Veredicto

V0 ya no esta en papel. Existe un nucleo ejecutable con API, Mission Kernel, misiones de prueba, permisos, evidencia, reportes, persistencia simple, SQLAlchemy store, adaptadores de modelo, LangGraph minimo con MemorySaver, Model Router minimo y pruebas automatizadas.

Sesion cerrada por decision de Alejandro: no continuar con mas features hasta tener Postgres corriendo.

Resultado actual de verificacion:

```text
py -m pytest
45 passed
```

## Que se implemento

### Mission Kernel

- `packages/mission_kernel/mission_state.py`
- `packages/mission_kernel/state_machine.py`
- `packages/mission_kernel/policies.py`

Capacidades:

- Crear misiones desde texto.
- Validar transiciones de estado.
- Rechazar transiciones invalidas.
- Exigir `reason` para `failed` y `blocked`.
- Detectar estados activos, terminales y que requieren humano.
- Manejar clases de permiso 0-4.

### API FastAPI

- `apps/api/main.py`
- `apps/api/missions.py`
- `apps/api/models.py`

Endpoints principales:

```text
GET  /
GET  /health
GET  /missions
POST /missions/research-brief
POST /missions/weekly-client-report
POST /missions/draft-outreach
GET  /missions/{mission_id}
GET  /missions/{mission_id}/events
GET  /missions/{mission_id}/evidence
GET  /missions/{mission_id}/report
POST /missions/{mission_id}/approve
POST /missions/{mission_id}/reject
GET  /models/status
POST /models/test
```

### Misiones implementadas

1. `research-brief-v1`
   - Informe corto de investigacion.
   - Permiso clase 0.
   - Corre solo.
   - Genera evidencia, validacion, reporte y playbook candidate.

2. `draft-outreach`
   - Borrador de contacto comercial.
   - Permiso clase 3.
   - Se detiene en `awaiting_approval`.
   - Al aprobar, simula accion externa sin enviar nada real.
   - Cierra con evidencia de aprobacion y accion externa simulada.

3. `weekly-client-report-v1`
   - Reporte semanal para cliente de agencia/team.
   - Usa datos simulados de performance.
   - Calcula metricas, insights y proximos pasos.
   - Genera reporte validado y evidencia.
   - Es la mision mas cercana al ICP elegido: agencias y teams.
   - Ahora corre mediante LangGraph en el endpoint principal.

### LangGraph

- `packages/orchestrator/nodes.py`
- `packages/orchestrator/mission_graph.py`
- `packages/orchestrator/router.py`

Capacidades:

- Grafo minimo para `weekly-client-report-v1`.
- Nodos alineados con el TDD:
  - `interpret_intent`
  - `retrieve_context`
  - `classify_permissions`
  - `create_plan`
  - `human_approval`
  - `execute_step`
  - `troubleshoot`
  - `validate_output`
  - `deliver`
  - `generate_report`
  - `update_memory`
- Edges condicionales para approval y ejecucion.
- Tests dedicados en `tests/test_langgraph_mission_graph.py`.

Limitacion consciente:

- Todavia no hay checkpointer Postgres ni interrupts reales persistentes. El grafo usa `MemorySaver` en desarrollo, pero las misiones largas aun no sobreviven reinicios como exige la version final del TDD.
- El estado del grafo ya fue limpiado para ser serializable; no guarda adapters de modelo vivos.

### Persistencia

- `packages/mission_store/json_store.py`
- `packages/mission_store/sqlalchemy_store.py`
- `packages/mission_store/factory.py`

Persistencia local simple en:

```text
runtime/missions.json
```

Tambien existe store SQLAlchemy compatible con:

```text
OLI_MISSION_STORE=sqlalchemy
OLI_DATABASE_URL=sqlite:///runtime/oli-dev.db
OLI_DATABASE_URL=postgresql+psycopg2://oli:oli@localhost:5432/oli
```

No hay Postgres corriendo todavia en este entorno. La interfaz ya esta preparada para Postgres.

Intento de instalacion local:

- `docker` no estaba disponible.
- `psql` no estaba disponible.
- `winget` si estaba disponible.
- `winget search PostgreSQL` mostro PostgreSQL 16, 17 y 18.
- Codex intento PostgreSQL 16 por alineacion literal con el TDD, pero Alejandro corrigio que si se busca state-of-the-art la opcion correcta a proponer era PostgreSQL 18.
- La instalacion local fue bloqueada/cancelada por permisos de administrador del computador corporativo.
- Resultado: Postgres no quedo instalado ni corriendo.

### Modelos

- `packages/orchestrator/model_adapter.py`
- `packages/model_router/status.py`
- `packages/config/env.py`
- `.env.example`
- `scripts/configure_openrouter_key.py`
- `scripts/test_openrouter_model.py`

Adaptadores:

- `DevelopmentModelAdapter`
- `OllamaModelAdapter`
- `OpenAICompatibleModelAdapter`
- `WebhookModelAdapter`
- `FallbackModelAdapter`

Estado actual:

- OpenRouter fue configurado por `.env.local`.
- Modelo probado exitosamente: `openrouter/owl-alpha`.
- Prueba real devolvio `oli_openrouter_ok`.
- Una mision `weekly-client-report` corrio con `model_provider_used=openai_compatible`.
- Hay fallback a desarrollo si el proveedor falla.

### Model Router

- `packages/model_router/router.py`

Capacidades:

- `TaskType` alineado con ADR-010/ADR-016.
- `ModelRole` por rol, no por nombre de modelo.
- `PrivacyMode`:
  - `local_only`
  - `hybrid`
  - `cloud_ok`
- `RoutingTier`:
  - Tier 1 fast local
  - Tier 2 main local
  - Tier 3 frontier API
  - development fallback
  - blocked
- `RoutingDecision` auditable.
- El LangGraph semanal registra evidencia `model_routing`.

Limitacion consciente:

- Todavia no existe Model Registry persistente ni BenchmarkRunner. El router decide por reglas minimas y deja preparada la interfaz.

### Scripts

- `scripts/run_api.ps1`
- `scripts/restart_api.ps1`
- `scripts/configure_openrouter_key.py`
- `scripts/test_openrouter_model.py`

Nota: hubo problemas operativos con procesos `uvicorn` en Windows. La forma mas estable por ahora:

```powershell
cd C:\Users\apenaosorio\Desktop\oli
py -m uvicorn apps.api.main:app --host 127.0.0.1 --port 8000 --app-dir .
```

## Que NO esta implementado aun

- Postgres corriendo como servicio real.
- PostgresSaver conectado a LangGraph.
- pgvector/memoria semantica.
- Worker separado.
- SSE/realtime feed.
- Docker sandbox.
- SeaweedFS/artifact store real.
- Model Registry completo con benchmark runner.
- UI Next.js.
- Browser/desktop tools reales.
- Evals formales con dataset.

## Evaluacion contra TDD V0

El TDD decia:

```text
1. pyproject.toml / requirements
2. packages/mission_kernel
3. packages/orchestrator
4. apps/api
5. tests/test_slice_001.py
```

Estado:

- Cumplido en version minima.
- Se agrego mas que el minimo: approvals, model router, weekly report, persistencia simple.
- LangGraph minimo ya se cumplio para `weekly-client-report-v1`.
- Model Router minimo ya se cumplio.
- SQLAlchemy store minimo ya se cumplio.
- No se cumplio todavia Postgres corriendo, PostgresSaver, pgvector ni Ollama como runtime canonico.

## Veredicto de Codex

V0.3 tecnico: logrado y defendible como base de desarrollo.

No diria "V0 producto terminado". Diria:

```text
V0.0 Mission Kernel + API + Model Adapter esta completo.
V0.1 LangGraph minimo esta completo para la primera mision de agencia/team.
V0.2 Model Router minimo esta completo y auditable por mision.
V0.3 SQLAlchemy store y MemorySaver estan completos en modo desarrollo.
V0.4 debe integrar PostgresSaver si hay Postgres disponible, o execution loop real por step si no hay infraestructura.
```

## Siguiente recomendacion

Orden recomendado:

1. Mantener `tests/test_v0_acceptance.py` y `tests/test_langgraph_mission_graph.py` como contrato vivo.
2. Mantener `tests/test_model_router_tiers.py` como contrato vivo de ADR-016.
3. No seguir con nuevas features hasta resolver Postgres.
4. Preferir PostgreSQL 18 si se busca state-of-the-art; mantener SQLAlchemy compatible con PostgreSQL 16+.
5. Cuando haya Postgres, configurar:

```text
OLI_MISSION_STORE=sqlalchemy
OLI_DATABASE_URL=postgresql+psycopg2://...
```

6. Despues conectar `PostgresSaver`.
7. Despues crear evals para las 3 mission-class.
8. Despues pensar en V1 UI/Next.js.

No recomiendo saltar a V1 todavia.
