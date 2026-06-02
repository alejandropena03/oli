# Bitácora de sesiones — Oli Bridge

Cada agente escribe una entrada al cerrar sesión. Formato fijo. Append-only.

## Formato

```
### [FECHA] — [AGENTE] — Sesión N

**Qué se hizo:**
- item 1
- item 2

**Estado al cierre:**
- Tests: X passed
- Task activa: TASK-NNN (status)
- Repo: commit SHA o "pendiente"

**Qué no se pudo / quedó bloqueado:**
- item o "nada"

**Qué sigue (para el otro agente):**
- acción concreta
```

---

### 2026-06-01 — Claude Code — Sesión 1

**Qué se hizo:**
- Auditoría completa del trabajo de Codex (2026-05-30/31)
- Reorganización de Consultor Estrategico Codex/ en 11 subcarpetas
- Commit del V0.3 completo (105 archivos, 45 tests pasando)
- Push a github.com/alejandropena03/oli
- Sistema bridge creado: README, CURRENT_TASK, HANDOFF_LOG, PENDIENTES
- CLAUDE.md creado (startup protocol para Claude Code)
- AGENTS.md actualizado (identidad DeepSeek, bridge bidireccional)
- REPO_MAP.md creado (mini-RAG del repo)
- Constitución de Oli incorporada a ambos MDs

**Estado al cierre:**
- Tests: 45 passed (MemorySaver, sin Postgres real)
- Task activa: TASK-002 — WAITING_FOR_LOCAL (DeepSeek)
- Repo: commit cbd5efa + pendiente commit de esta sesión

**Qué no se pudo / quedó bloqueado:**
- Postgres: bloqueado en laptop corporativa (política de seguridad)
- PostgresSaver: pendiente Postgres
- .opencode/ en .gitignore: lo hace DeepSeek en TASK-002

**Qué sigue (para DeepSeek):**
- git pull
- Ejecutar TASK-002: Docker + Postgres 18 + pytest + health check
- Agregar .opencode/ al .gitignore antes del push

---

### 2026-06-01 — DeepSeek via opencode — Sesión 1

**Qué se hizo:**
- TASK-002 completada: entorno Mac personal validado
- Postgres 18 levantado con Docker Desktop en Mac
- `.env.local` configurado con OLI_MISSION_STORE=sqlalchemy + OLI_DATABASE_URL
- Python 3.12.13 via pyenv + dependencias instaladas
- `.opencode/` agregado a `.gitignore`
- `python -m pytest`: 45/45 passed contra Postgres real
- API levantada en localhost:8000 → health OK
- Fix: tkinter import movido a lazy en `scripts/configure_openrouter_key.py`

**Estado al cierre:**
- Tests: 45 passed (contra Postgres real via SQLAlchemy)
- Task activa: TASK-002 — WAITING_FOR_CLAUDE (Claude)
- Repo: pendiente commit de DeepSeek

**Qué no se pudo / quedó bloqueado:**
- Nada. Todo completado.

**Qué sigue (para Claude):**
- git pull
- Conectar PostgresSaver de LangGraph a Postgres real
- Probar checkpoint/resume con PostgresSaver

---

### 2026-06-01 — Claude Code — Sesión 2

**Qué se hizo:**
- Implementado `packages/orchestrator/checkpointer.py`: factory que devuelve PostgresSaver (Postgres disponible) o MemorySaver (dev). Lazy import — no falla sin el paquete.
- Refactorizado `packages/orchestrator/mission_graph.py`: topología separada del checkpointer, `build_weekly_report_graph()` usa el factory automáticamente.
- Creado `tests/test_postgres_checkpointer.py`: 6 unit tests (siempre corren) + 4 integration tests (se activan con Postgres en env). Tests cubren: factory logic, URL conversion, checkpoint/resume, thread isolation.
- Suite local: 51 passed, 4 skipped (integration tests esperan Mac con Postgres).
- Actualizado bridge: PENDIENTES.md, CURRENT_TASK.md (TASK-003), HANDOFF_LOG.md, BITACORA.md.

**Estado al cierre:**
- Tests: 51 passed, 4 skipped (aquí) — 55 passed esperados en Mac con Postgres
- Task activa: TASK-003 — WAITING_FOR_LOCAL (DeepSeek)
- Repo: pendiente commit de esta sesión

**Qué no se pudo / quedó bloqueado:**
- Correr integration tests: requieren `langgraph-checkpoint-postgres` y `psycopg[binary]` — solo en Mac con Postgres.

**Qué sigue (para DeepSeek):**
- git pull
- pip install langgraph-checkpoint-postgres "psycopg[binary]"
- python -m pytest tests/test_postgres_checkpointer.py -v → 10 passed
- python -m pytest → suite completa verde
- Agregar deps a pyproject.toml y hacer push

---

### 2026-06-02 — DeepSeek via opencode — Sesión 2

**Qué se hizo:**
- TASK-003 completada: PostgresSaver validado contra Postgres real
- `langgraph-checkpoint-postgres` + `psycopg[binary]` instalados
- `python -m pytest`: **55/55 passed** (6 nuevos unit + 4 integration tests)
- Dependencias agregadas a `pyproject.toml`
- Fix: tests de integración corregidos — PostgresSaver usa `__root__` en channel_values
- Bridge actualizado: CURRENT_TASK.md → WAITING_FOR_CLAUDE, HANDOFF_LOG, BITACORA

**Estado al cierre:**
- Tests: 55 passed (contra Postgres real + PostgresSaver checkpointing)
- Task activa: TASK-003 — WAITING_FOR_CLAUDE (Claude)
- Repo: pendiente commit de DeepSeek

**Qué no se pudo / quedó bloqueado:**
- Nada. PostgresSaver checkpointing funciona end-to-end.

**Qué sigue (para Claude):**
- Revisar fix en tests de integración (__root__ wrapper)
- Próximo paso según PENDIENTES: evals formales o tool guardrails
