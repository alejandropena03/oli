---
task_id: TASK-002
status: WAITING_FOR_LOCAL
owner: local_agent
created_by: claude
created_at: 2026-06-01T23:00Z
updated_at: 2026-06-01T23:00Z
---

## Misión

Validar el entorno local en el Mac: clonar repo, instalar dependencias, levantar Postgres 18 con Docker, correr los 45 tests y confirmar que todo está verde.

## Contexto relevante

- Repo: `github.com/alejandropena03/oli`
- Python 3.12, FastAPI, LangGraph, SQLAlchemy ya en `pyproject.toml`
- Store SQLAlchemy listo en `packages/mission_store/sqlalchemy_store.py`
- Variables a configurar en `.env.local` (ver `.env.example`)
- `.opencode/` debe agregarse al `.gitignore` antes del próximo push

## Entregable esperado

1. `.opencode/` agregado a `.gitignore`
2. Postgres 18 corriendo en Docker en el Mac
3. `.env.local` configurado con `OLI_MISSION_STORE=sqlalchemy` y `OLI_DATABASE_URL`
4. `python -m pytest` → 45 passed contra Postgres real
5. `GET http://127.0.0.1:8000/health` → `{"status": "ok"}`
6. Este archivo actualizado con `status: WAITING_FOR_CLAUDE` y resultado

## Criterio de completación

```bash
# 1. Agregar .opencode/ al .gitignore
echo ".opencode/" >> .gitignore

# 2. Levantar Postgres
docker run -d --name oli-postgres \
  -e POSTGRES_USER=oli -e POSTGRES_PASSWORD=oli -e POSTGRES_DB=oli \
  -p 5432:5432 postgres:18

# 3. Configurar .env.local
echo "OLI_MISSION_STORE=sqlalchemy" > .env.local
echo "OLI_DATABASE_URL=postgresql+psycopg2://oli:oli@localhost:5432/oli" >> .env.local

# 4. Instalar dependencias
pip install fastapi langgraph sqlalchemy psycopg2-binary pydantic python-dotenv pytest anyio httpx pytest-mock langsmith

# 5. Correr tests
python -m pytest

# 6. Levantar API y verificar
python -m uvicorn apps.api.main:app --host 127.0.0.1 --port 8000 &
curl http://127.0.0.1:8000/health
```

Éxito = 45 passed + health OK.

## Notas del agente anterior (Claude)

- Completé toda la reestructura del bridge: CLAUDE.md creado, AGENTS.md actualizado, PENDIENTES.md creado, bridge bidireccional documentado.
- El briefing de DeepSeek fue correcto en todos los puntos. Bien ejecutado.
- Si `psycopg2-binary` falla en Mac ARM: usar `psycopg[binary]` como alternativa.
- El store hace `create_all` automáticamente — no necesitas migraciones manuales para V0.
- Después de esta tarea, el siguiente paso es conectar PostgresSaver a LangGraph (eso lo hago yo desde aquí).
- Leer `.bridge/REPO_MAP.md` antes de explorar cualquier archivo del repo.
- Leer `.bridge/BITACORA.md` para ver qué hizo Claude en esta sesión.
