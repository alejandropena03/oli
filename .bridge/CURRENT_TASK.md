---
task_id: TASK-001
status: WAITING_FOR_LOCAL
owner: local_agent
created_by: claude
created_at: 2026-06-01T22:00Z
updated_at: 2026-06-01T22:00Z
---

## Misión

Levantar Postgres 18 con Docker en el Mac personal, conectarlo al proyecto Oli y verificar que los 45 tests pasen contra una base de datos real.

## Contexto relevante

El proyecto ya tiene todo preparado para Postgres:
- `packages/mission_store/sqlalchemy_store.py` — store SQLAlchemy listo
- `packages/mission_store/factory.py` — factory que lee `OLI_MISSION_STORE` y `OLI_DATABASE_URL`
- `.env.example` — documenta las variables de entorno necesarias
- `pyproject.toml` — dependencias ya incluyen `sqlalchemy` y `psycopg2-binary`

Variables de entorno que necesitas configurar (crea un archivo `.env.local` en la raíz):
```
OLI_MISSION_STORE=sqlalchemy
OLI_DATABASE_URL=postgresql+psycopg2://oli:oli@localhost:5432/oli
OPENROUTER_API_KEY=<tu key si la tienes, opcional para los tests>
```

El agente local a usar es OpenCode (o cualquier CLI agéntico disponible en el Mac).
El modelo no importa para esta tarea — es ejecución pura, no generación de código.

## Entregable esperado

1. Postgres 18 corriendo como contenedor Docker en el Mac.
2. Base de datos `oli` creada con usuario `oli`.
3. Tablas creadas automáticamente por SQLAlchemy (el store hace `create_all` en startup).
4. `py -m pytest` pasando los 45 tests con `OLI_MISSION_STORE=sqlalchemy` activo.
5. Este archivo actualizado con `status: WAITING_FOR_CLAUDE` y el resultado.

## Criterio de completación

Ejecutar en orden:

```bash
# 1. Clonar repo (si no está clonado)
git clone https://github.com/alejandropena03/oli.git
cd oli

# 2. Levantar Postgres 18 con Docker
docker run -d \
  --name oli-postgres \
  -e POSTGRES_USER=oli \
  -e POSTGRES_PASSWORD=oli \
  -e POSTGRES_DB=oli \
  -p 5432:5432 \
  postgres:18

# 3. Esperar ~5 segundos y verificar que está corriendo
docker ps | grep oli-postgres

# 4. Instalar dependencias Python
pip install -e ".[dev]"
# o si no tiene pyproject extras:
pip install fastapi langgraph sqlalchemy psycopg2-binary pydantic python-dotenv pytest anyio httpx pytest-mock

# 5. Crear .env.local
echo "OLI_MISSION_STORE=sqlalchemy" >> .env.local
echo "OLI_DATABASE_URL=postgresql+psycopg2://oli:oli@localhost:5432/oli" >> .env.local

# 6. Correr tests
py -m pytest
# o en Mac:
python -m pytest

# Output esperado: 45 passed
```

Éxito = `45 passed` (o más si los tests SQLAlchemy adicionales se activan).

## Notas del agente anterior (Claude)

- El proyecto ya fue auditado. V0.3 es estable. No agregar features — solo conectar Postgres.
- Si `psycopg2-binary` falla en Mac ARM (M1/M2/M3), usar `psycopg2` puro o `psycopg[binary]`.
- Si el puerto 5432 está ocupado, cambiar a 5433 y actualizar `OLI_DATABASE_URL` en consecuencia.
- El store hace `create_all` automáticamente — no necesitas correr migraciones manuales para V0.
- Si algún test falla por SQLAlchemy (no por código nuevo), reportar el error exacto en las notas.
- Postgres 18 es la versión state-of-art según auditoría 2026-05-31. El TDD dice 16 pero se decidió usar 18.
- Una vez que los tests pasen, también intentar levantar la API: `python -m uvicorn apps.api.main:app --host 127.0.0.1 --port 8000` y hacer un `GET /health`.
