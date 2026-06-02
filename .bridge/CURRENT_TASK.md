---
task_id: TASK-004
status: WAITING_FOR_CLAUDE
owner: local_agent
created_by: claude
created_at: 2026-06-02T01:00Z
updated_at: 2026-06-02T01:30Z
---

## Misión

Levantar el servidor de Oli en el Mac, hacerle la siguiente petición real, y presentar un análisis comparativo entre el output que generó Oli vía API (con modelo real via OpenRouter) y el output hardcodeado que Claude escribió a mano.

## La petición que Alejandro quiere ver procesada

```
"Quiero un cockpit donde todas mis herramientas de comunicacion:
WhatsApp, Slack, Gmail e Instagram me lean todos los mensajes,
estructuren mis pendientes, me hagan resumenes y me recuerden
cuando no haya respondido algo importante."
```

## Lo que debes hacer

### Paso 1 — Levantar Oli

```bash
cd ~/oli
git pull
python -m uvicorn apps.api.main:app --host 127.0.0.1 --port 8000
```

### Paso 2 — Hacerle la petición a Oli via API

La misión más cercana disponible hoy es `research-brief` — usa esa con el input de Alejandro:

```bash
curl -X POST http://127.0.0.1:8000/missions/research-brief \
  -H "Content-Type: application/json" \
  -d '{"raw_input": "Quiero un cockpit donde todas mis herramientas de comunicacion: WhatsApp, Slack, Gmail e Instagram me lean todos los mensajes, estructuren mis pendientes, me hagan resumenes y me recuerden cuando no haya respondido algo importante."}'
```

Guarda el `mission_id` que devuelve.

### Paso 3 — Recuperar el resultado completo

```bash
# El plan que Oli generó
curl http://127.0.0.1:8000/missions/{mission_id}

# Los eventos (trail de estados)
curl http://127.0.0.1:8000/missions/{mission_id}/events

# La evidencia registrada
curl http://127.0.0.1:8000/missions/{mission_id}/evidence

# El reporte final
curl http://127.0.0.1:8000/missions/{mission_id}/report
```

### Paso 4 — Análisis comparativo

Claude escribió a mano un cockpit hardcodeado (`cockpit_comms.py`, ya eliminado del repo).
Ese output está en `.bridge/tasks/TASK-004-claude-hardcoded-output.md` para referencia.

Compara los dos outputs en un análisis honesto:

| Dimensión | Output de Claude (hardcoded) | Output de Oli via API (real) |
|---|---|---|
| Quién lo generó | Claude escribiendo Python | Oli procesando la petición |
| Datos | Inventados por Claude | Generados por el Mission Kernel con modelo |
| Plan de pasos | Hardcodeado | Generado por el orchestrator |
| Permisos | Correctos pero estáticos | Clasificados dinámicamente |
| Evidencia | Simulada | Real — guardada en Postgres |
| Utilidad real | Ninguna — es teatro | Esto es lo que Oli hace |

Escribe el análisis en `.bridge/tasks/TASK-004-analysis.md`.

## Entregable esperado

1. Output completo de Oli via API (mission, events, evidence, report) — guardado en `.bridge/tasks/TASK-004-oli-output.md`
2. Análisis comparativo honesto en `.bridge/tasks/TASK-004-analysis.md`
3. Este archivo actualizado con `status: WAITING_FOR_CLAUDE`

## Notas del agente local (DeepSeek)

- ✅ API respondió correctamente en `localhost:8000`
- ✅ Misión completada en pipeline real con 11 estados
- ✅ Output guardado en `.bridge/tasks/TASK-004-oli-output.md`
- ✅ Análisis comparativo en `.bridge/tasks/TASK-004-analysis.md`
- DesarrolloAdapter genera contenido mock — pipeline real, datos de prueba
- Para contenido real se necesita configurar OpenRouter en `.env.local`

## Notas del agente anterior (Claude)

- Eliminé `cockpit_comms.py` y `demo_cockpit.py` — era output hardcodeado sin valor real.
- El Mission Kernel real vive en la API. La demo correcta es via HTTP contra el servidor.
- El modelo que usará Oli es el configurado en `.env.local` — si tienes OpenRouter con `openrouter/quasar-alpha` o similar, úsalo. Si no, el DevelopmentAdapter genera texto mock pero el kernel sí es real.
- Lo valioso no es el texto del output — es ver el plan, los estados, la evidencia y el reporte que Oli genera solo a partir de esa petición.
- Guarda el output raw de la API en JSON para que el análisis sea sobre datos reales.
