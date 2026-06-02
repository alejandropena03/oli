# Oli — Git Bridge Protocol

Sistema de orquestación asíncrona entre dos agentes en dos máquinas distintas.
El repo de GitHub es el canal de comunicación. No hay coordinación en tiempo real.

---

## Arquitectura

```
[Laptop Corporativa]                [GitHub: alejandropena03/oli]          [Mac Personal]
Claude Code (músculo)  ──push──►   .bridge/ (archivos vivos)   ◄──pull──  Agente local
                       ◄──pull──                                ──push──►  (ejecutor)
```

**Claude Code (laptop corporativa):**
- Procesa prompts masivos, genera lógica compleja, escribe módulos, reescribe código.
- No puede instalar Docker, Postgres ni herramientas externas (política corporativa).
- Tokens ilimitados via cuenta corporativa.

**Agente local (Mac personal):**
- Ejecuta Docker, Postgres, pytest, migraciones, scripts.
- Valida que el código funcione en entorno real.
- No gasta tokens pesados en generación de código.
- Herramientas instaladas: Homebrew, Docker Desktop, VS Code, Python, Node.

---

## Estructura de archivos

```
.bridge/
├── README.md          ← este protocolo (no modificar sin consenso)
├── CURRENT_TASK.md    ← tarea activa: quién la tiene y qué hacer
├── HANDOFF_LOG.md     ← historial append-only de transfers
└── tasks/
    ├── TASK-001.md    ← archivada (inmutable una vez cerrada)
    └── ...
```

---

## Estados de CURRENT_TASK.md

```
WAITING_FOR_CLAUDE   → Claude está procesando. Agente local: solo pull, no toques nada.
WAITING_FOR_LOCAL    → Listo para ejecutar. Agente local: pull → ejecuta → valida → push.
IN_PROGRESS_LOCAL    → Agente local trabajando. Claude: espera.
DONE                 → Tarea cerrada. Claude archiva en tasks/ y crea la siguiente.
```

---

## Formato de CURRENT_TASK.md

```markdown
---
task_id: TASK-NNN
status: WAITING_FOR_LOCAL
owner: local_agent
created_by: claude
created_at: ISO8601
updated_at: ISO8601
---

## Misión
Descripción exacta de lo que hay que hacer.

## Contexto relevante
Archivos, paths, decisiones previas que el agente necesita saber.

## Entregable esperado
Qué debe existir cuando esta tarea termine.

## Criterio de completación
Comandos a correr y outputs esperados para declarar éxito.

## Notas del agente anterior
Lo que Claude o el agente local quiere que el otro sepa.
```

---

## Flujo de una iteración

**Paso 1 — Claude genera trabajo:**
1. Escribe código / schemas / módulos en el repo.
2. Crea/actualiza `CURRENT_TASK.md` con `status: WAITING_FOR_LOCAL`.
3. `git add -A && git commit && git push personal main`

**Paso 2 — Mac recibe la posta:**
```bash
git pull origin main
cat .bridge/CURRENT_TASK.md
# ejecuta: docker compose up, pytest, migration, etc.
```

**Paso 3 — Mac entrega resultado:**
1. Actualiza `CURRENT_TASK.md` → `status: WAITING_FOR_CLAUDE`.
2. Agrega notas del resultado en la sección correspondiente.
3. Opcionalmente crea `tasks/TASK-NNN-output.md` con outputs relevantes.
4. `git add -A && git commit -m "task(TASK-NNN): resultado local" && git push`

**Paso 4 — Claude recibe, archiva, genera siguiente tarea. Ciclo.**

---

## Reglas del protocolo

1. `CURRENT_TASK.md` siempre tiene una sola tarea activa.
2. `HANDOFF_LOG.md` es append-only — nunca se edita hacia atrás.
3. Una tarea archivada en `tasks/` es inmutable.
4. El agente que recibe la tarea no cambia el `task_id`.
5. Si hay un bloqueo, el agente que lo detecta escribe `status: WAITING_FOR_CLAUDE` con la razón en Notas.
6. Claude hace push a `personal` (remote del repo personal). El Mac hace push a `origin` (mismo repo).
7. Siempre hacer `git pull` antes de editar `.bridge/`.

---

## Setup inicial en el Mac

```bash
# Clonar el repo
git clone https://github.com/alejandropena03/oli.git
cd oli

# Verificar que el bridge está ahí
cat .bridge/CURRENT_TASK.md

# Seguir las instrucciones de la primera tarea
```

---

## Convenciones de commit

```
task(TASK-NNN): descripción breve    ← cuando se completa o actualiza una tarea
bridge: descripción                  ← cuando se actualiza el protocolo
```
