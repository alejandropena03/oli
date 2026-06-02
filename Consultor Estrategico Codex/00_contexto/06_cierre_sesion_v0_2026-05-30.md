# Cierre de sesion V0 - 2026-05-30

## Estado final

Se detiene el desarrollo por decision de Alejandro hasta tener Postgres corriendo.

La base tecnica actual queda asi:

- Mission Kernel minimo.
- API FastAPI.
- Misiones `research-brief`, `draft-outreach`, `weekly-client-report`.
- Approval gate para acciones de impacto externo.
- Evidencia, eventos y reportes por mision.
- Persistencia JSON local.
- Store SQLAlchemy opcional.
- LangGraph para `weekly-client-report`.
- LangGraph `MemorySaver` en desarrollo.
- Model Router minimo por tiers.
- Adaptadores de modelo development, Ollama, OpenAI-compatible, webhook y fallback.
- OpenRouter probado con `openrouter/owl-alpha`.

Ultima verificacion completa:

```text
py -m pytest
45 passed
```

## Postgres

No quedo corriendo Postgres.

Se detecto:

- `docker`: no instalado.
- `psql`: no instalado.
- `winget`: disponible.

`winget search PostgreSQL` mostro paquetes oficiales:

- PostgreSQL 16
- PostgreSQL 17
- PostgreSQL 18

Codex intento PostgreSQL 16 porque el TDD menciona PostgreSQL 16. Alejandro corrigio que si la prioridad es state-of-the-art, Codex debio presentar PostgreSQL 18 como la opcion principal. Correccion aceptada.

Intento realizado:

```text
winget install --id PostgreSQL.PostgreSQL.16 --exact --accept-package-agreements --accept-source-agreements
```

Resultado:

- El instalador oficial se descargo.
- La instalacion fue cancelada/bloqueada por permisos de administrador del computador corporativo.
- No hay Postgres local instalado.

## Decision estrategica

No continuar con mas features hasta resolver Postgres.

Opciones futuras:

1. PostgreSQL 18 local en computador propio o con permisos admin.
2. Postgres gratuito remoto.
3. Postgres en servidor/GPU alquilado cuando exista acceso SSH.

Cuando Postgres este disponible, configurar:

```text
OLI_MISSION_STORE=sqlalchemy
OLI_DATABASE_URL=postgresql+psycopg2://...
```

Despues de eso:

1. Validar conexion real con `py -m pytest`.
2. Conectar `PostgresSaver` de LangGraph.
3. Probar que una mision pueda checkpoint/reanudar.

## Nota critica de Codex

La decision tecnica no debe confundirse:

- Si seguimos el TDD literalmente: PostgreSQL 16.
- Si seguimos state-of-the-art disponible hoy por `winget`: PostgreSQL 18.

Para Oli como producto AI-first, la recomendacion futura debe presentar ambas opciones con tradeoff, no escoger silenciosamente una.
