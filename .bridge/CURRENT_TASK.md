---
task_id: TASK-003
status: WAITING_FOR_LOCAL
owner: local_agent
created_by: claude
created_at: 2026-06-01T24:00Z
updated_at: 2026-06-01T24:00Z
---

## Misión

Instalar las dependencias de PostgresSaver y correr los 4 integration tests de checkpointing contra Postgres real. Verificar que checkpoint/resume funciona de verdad.

## Contexto relevante

Claude implementó:
- `packages/orchestrator/checkpointer.py` — factory que devuelve PostgresSaver si OLI_DATABASE_URL apunta a Postgres, MemorySaver si no. Lazy import: no falla sin el paquete.
- `packages/orchestrator/mission_graph.py` — refactorizado para usar el factory. Topología separada de checkpointer.
- `tests/test_postgres_checkpointer.py` — 6 unit tests (siempre corren) + 4 integration tests (se activan con Postgres).

Estado actual en tu Mac (después de TASK-002):
- Postgres 18 corriendo en Docker en `localhost:5432`
- `.env.local` tiene `OLI_MISSION_STORE=sqlalchemy` y `OLI_DATABASE_URL=postgresql+psycopg2://oli:oli@localhost:5432/oli`
- 51 tests pasan aquí (45 originales + 6 unit tests nuevos), 4 skipped esperando Postgres

PostgresSaver de LangGraph requiere dos paquetes que NO están en `pyproject.toml` todavía:
- `langgraph-checkpoint-postgres` — el saver oficial de LangGraph
- `psycopg[binary]` — psycopg3 (diferente a psycopg2, que ya tienes)

## Entregable esperado

1. Paquetes instalados en Mac
2. `python -m pytest tests/test_postgres_checkpointer.py -v` → 10 passed, 0 skipped
3. Los 4 integration tests verdes:
   - `test_checkpointer_returns_postgres_saver`
   - `test_mission_checkpoint_survives_graph_reinvocation`
   - `test_different_threads_have_isolated_checkpoints`
   - `test_graph_builds_with_postgres_checkpointer`
4. `python -m pytest` completo → 51 passed (o más), 0 skipped
5. Este archivo actualizado con `status: WAITING_FOR_CLAUDE` y resultado

## Criterio de completación

```bash
# 1. Instalar dependencias de PostgresSaver
pip install langgraph-checkpoint-postgres "psycopg[binary]"

# 2. Correr solo los tests de Postgres primero
python -m pytest tests/test_postgres_checkpointer.py -v

# Output esperado:
# TestCheckpointerFactory::test_returns_memory_saver_by_default PASSED
# TestCheckpointerFactory::test_returns_memory_saver_when_store_is_json PASSED
# TestCheckpointerFactory::test_psycopg3_url_conversion PASSED
# TestCheckpointerFactory::test_psycopg3_url_conversion_passthrough PASSED
# TestCheckpointerFactory::test_graph_builds_without_postgres PASSED
# TestCheckpointerFactory::test_graph_builds_with_memory_saver PASSED
# TestPostgresSaverIntegration::test_checkpointer_returns_postgres_saver PASSED
# TestPostgresSaverIntegration::test_mission_checkpoint_survives_graph_reinvocation PASSED
# TestPostgresSaverIntegration::test_different_threads_have_isolated_checkpoints PASSED
# TestPostgresSaverIntegration::test_graph_builds_with_postgres_checkpointer PASSED
# 10 passed

# 3. Correr suite completa
python -m pytest

# 4. Si todo verde, agregar las nuevas deps a pyproject.toml:
# En [project.dependencies] agregar:
#   "langgraph-checkpoint-postgres>=2.0",
#   "psycopg[binary]>=3.1",
```

Éxito = 10 passed en test_postgres_checkpointer.py + suite completa verde.

## Notas del agente anterior (Claude)

- El factory `get_checkpointer()` detecta Postgres automáticamente por variables de entorno. No hay cambio de código necesario en el Mac — solo instalar los paquetes.
- Si `langgraph-checkpoint-postgres` no encuentra la versión correcta, probar: `pip install "langgraph-checkpoint-postgres>=2.0"`.
- El test `test_mission_checkpoint_survives_graph_reinvocation` es el más importante: prueba que una misión completada persiste en Postgres y es recuperable. Si ese pasa, el checkpointing es real.
- Si algún integration test falla con error de conexión, verificar que el contenedor Docker sigue corriendo: `docker ps | grep oli-postgres`.
- Después de validar, agregar las dos nuevas deps a `pyproject.toml` y hacer push. Claude actualiza el REPO_MAP con el nuevo módulo checkpointer.
