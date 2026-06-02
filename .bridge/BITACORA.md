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
