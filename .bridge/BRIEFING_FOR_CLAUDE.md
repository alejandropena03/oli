# Briefing: DeepSeek (Local Agent) → Claude Code

Fecha: 2026-06-01
Emisor: DeepSeek corriendo en opencode (Mac personal de Alejandro)
Destinatario: Claude Code (laptop corporativa de Alejandro)

---

## 1. Quién soy y qué capacidades tengo

Soy DeepSeek ejecutándome dentro de **opencode** en el Mac personal de Alejandro.
No soy Codex. Codex está retirado. Alejandro ya no usará más ese rol.

### Stack técnico

| Capa | Qué soy |
|------|---------|
| Modelo | DeepSeek (contexto 1M, razonamiento denso, multilingüe) |
| CLI agéntico | opencode |
| Tools directas | bash, read, write, edit, glob, grep, websearch, webfetch, task (subagentes) |
| Extras | MCP servers, skills, plugins, permission system |
| Contexto de arranque | `AGENTS.md` (lo leo al inicio de cada sesión) |

### Lo que hago bien
- Razonamiento estratégico, análisis, auditoría, research
- Ejecución local (Docker, Postgres, pytest, scripts)
- Revisión de código generado por otros
- Mantener tracking de decisiones, riesgos y contexto
- Búsqueda web y de código
- Orquestación de subagentes para tareas paralelas

### Lo que NO hago bien (y ahí entras tú)
- Generación de código pesado (tú tienes Claude Opus 4.7 gratis por la empresa)
- Refactoring complejo multi-archivo
- Prompts masivos que requieren tokens ilimitados
- Lo que requiera la red corporativa

---

## 2. Lo que encontré en el repo

### 2.1 El bridge actual (.bridge/)

El protocolo existe y está bien pensando, pero tiene un **problema de dirección único**:
asume que solo Claude Code crea tareas y el agente local ejecuta.

**Yo también soy capaz de generar tareas para ti.** Alejandro puede hablarme a mí
(DeepSeek en Mac personal), yo puedo planificar, analizar, y luego delegarte
trabajo de código pesado. El bridge debe ser **bidireccional**.

### 2.2 No existe CLAUDE.md

No hay ningún archivo `CLAUDE.md` en el repo. Tú (Claude Code) lees ese archivo
al arrancar para saber contexto, igual que yo leo `AGENTS.md`. Sin ese archivo,
arrancas sin memoria del proyecto.

### 2.3 AGENTS.md aún habla de "Codex"

El archivo `AGENTS.md` está escrito para "Codex operating instructions for Oli".
Codex ya no existe. Ese archivo necesita reflejar la nueva realidad: dos agentes
(DeepSeek + opencode en Mac, Claude Code + Claude Opus 4.7 en corporativa).

**Alejandro me dijo que la responsabilidad de crear/editar ese archivo te la deja a ti.**
Es tuyo. Mejorarlo radicalmente.

### 2.4 Estructura de carpetas confusa

La carpeta `Consultor Estrategico Codex/` tiene contexto valioso pero:
- La identidad "Codex" está obsoleta
- Está mezclado: contexto vivo, auditorías, estrategia, research, fine-tuning, assets
- Alejandro pide limpiarlo: **fusionar lo de Codex con el resto del repo en una estructura clara**
- Los "pendientes" que Codex dejó en `03_tracking_estrategico.md` deben migrarse a un sistema de pendientes en el bridge

### 2.5 Sin sistema de pendientes compartido

Codex dejó decenas de decisiones y pendientes en `03_tracking_estrategico.md`.
Alejandro quiere que **cualquiera de los dos** pueda agregar un pendiente
y que quede registrado en algún lado accesible para ambos vía git.

### 2.6 Sin registro de conectores

Alejandro espera que yo (DeepSeek) vaya conectándome a servicios/herramientas
(MCP servers, APIs, skills) y que eso quede documentado en el bridge
para que tú también sepas a qué tengo acceso.

---

## 3. El modelo de trabajo que Alejandro quiere

```
[Habla con Alejandro]          [Habla con Alejandro]
       │                               │
       ▼                               ▼
  DeepSeek (Mac personal)      Claude Code (Corporativa)
  (opencode + tools)           (Claude Opus 4.7 + tokens ∞)
       │                               │
       └────────── git push/pull ──────┘
                      │
              .bridge/ (canal)
              AGENTS.md / CLAUDE.md (contexto alineado)
```

### Flujo correcto

1. Alejandro habla conmigo (DeepSeek) en Mac personal → strategizo, analizo, planifico
2. Yo creo una tarea en `.bridge/` → `status: WAITING_FOR_CLAUDE`
3. Hago commit y push
4. En corporativa, tú haces pull, ves la tarea, ejecutas (código pesado)
5. Pusheas de vuelta → `status: WAITING_FOR_LOCAL`
6. Yo hago pull, valido (pytest, revisión), cierro el ciclo

**Y viceversa**: Si tú detectas algo que necesita ejecución local, me pasas la tarea a mí.

---

## 4. Lo que necesito que hagas tú (Claude Code)

### 4.1 Crear CLAUDE.md (URGENTE)

Crea `CLAUDE.md` en la raíz del repo con:

- Tu rol: builder en laptop corporativa con Claude Opus 4.7
- Startup protocol obligatorio (como mi AGENTS.md)
- Contexto del proyecto Oli (V0.3, 45 tests, Postgres pendiente)
- Cómo leer el bridge al arrancar
- Mismo tono y estructura que AGENTS.md para que Alejandro no sienta diferencia
- División de trabajo: tú generas código, yo valido en local
- Regla de cierre de sesión: al terminar, dejar el repo estructurado con ruta clara

### 4.2 Actualizar AGENTS.md

Alejandro te deja a ti la responsabilidad de:
- Renombrar la identidad de "Codex" a "Local Agent (DeepSeek+opencode)"
- Actualizar el startup protocol para reflejar el modelo a 2 agentes
- Agregar sección sobre el bridge
- Mantener el tono crítico y directo que Alejandro valora

### 4.3 Rediseñar la estructura del bridge

El bridge actual es funcional pero minimalista. Necesita:

- **Bidirectional flow**: cualquier agente puede crear tareas
- **Pendientes system**: archivo `PENDIENTES.md` donde ambos agregamos items
- **Connector registry**: `CONNECTORS.md` documentando a qué servicios/herramientas tiene acceso cada agente
- **Session close protocol**: al finalizar cada sesión, ambos agentes dejan el repo en estado "listo" con ruta clara

### 4.4 Reestructurar carpeta Codex

`Consultor Estrategico Codex/` necesita:
- Fusionar el contexto útil en el bridge o en una estructura nueva
- Eliminar la identidad "Codex"
- Migrar los pendientes a `PENDIENTES.md`
- Mantener lo que sirve (auditorías, research, decisiones), descartar lo obsoleto

### 4.5 Alinear tono y formato

Alejandro dice: "no quiero sentir diferencia cuando hablo con uno y con el otro".
Necesitamos:

- Misma estructura de respuesta (Veredicto / Razón / Riesgo / Recomendación / Siguiente decisión)
- Mismo tono: crítico, directo, sin fluff
- Mismo sistema de contexto: startup protocol obligatorio
- Ambos leemos: `AGENTS.md` (yo) y `CLAUDE.md` (tú) — pero deben estar alineados

---

## 5. Resumen de acción inmediata

| # | Qué | Quién | Prioridad |
|---|-----|-------|-----------|
| 1 | Crear `CLAUDE.md` con startup protocol | Tú | Alta |
| 2 | Actualizar `AGENTS.md` (nueva identidad, bridge) | Tú | Alta |
| 3 | Crear sistema de pendientes (`PENDIENTES.md`) | Tú | Alta |
| 4 | Rediseñar bridge con flujo bidireccional | Tú | Alta |
| 5 | Reestructurar carpeta Codex | Tú | Media |
| 6 | Agregar connector registry | Tú (estructura) + Yo (llenar) | Media |
| 7 | Alinear tono/formato entre ambos | Ambos | Media |

---

## 6. Notas finales

- No tengo acceso a `CLAUDE.md` ni a las skills que tú usas para saber contexto previo. Eso es normal: son contextos diferentes. Pero debemos mantener la info alineada entre `AGENTS.md` y `CLAUDE.md`.
- El bridge funciona por git. Siempre hacer `git pull` antes de tocar `.bridge/`.
- Alejandro está en Mac personal con `gh` autenticado y el repo clonado. Ya puede hacer push/pull.
- Si algo no está claro, la regla es: **dejar una nota en `HANDOFF_LOG.md` y pasar la tarea de vuelta**.
- **Regla de oro**: al finalizar cada sesión, el repo debe quedar en estado "listo para el otro agente" con una ruta clara de lo que sigue.

---

Este archivo es mi briefing inicial. Una vez que hayas leído esto, actualiza
`CURRENT_TASK.md` con `status: WAITING_FOR_LOCAL` y las tareas que hayas completado
o iniciado. Yo validaré desde el Mac y cerraremos el ciclo.

— DeepSeek (vía opencode en Mac personal)
