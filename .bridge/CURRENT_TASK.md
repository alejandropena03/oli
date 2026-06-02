---
task_id: TASK-005
status: WAITING_FOR_LOCAL
owner: local_agent
created_by: claude
created_at: 2026-06-02T02:00Z
updated_at: 2026-06-02T02:00Z
---

## Misión

Conectar OpenRouter al adaptador de modelo de Oli y repetir la petición del cockpit de comunicaciones para ver la diferencia entre contenido mock y contenido generado por un modelo real.

## Contexto relevante

En TASK-004 Oli procesó la petición correctamente (11 estados, Postgres, evidencia real) pero el output textual fue mock — el `DevelopmentModelAdapter` ignora el input y devuelve texto fijo.

El problema central: `research-brief` tiene la intención hardcodeada como `competitor_research_brief`. No importa qué le mandes — siempre responde con Lindy, Dust, Claude Projects.

Para que Oli interprete la petición real del usuario necesitamos:
1. Modelo real via OpenRouter conectado
2. Que el modelo lea el `raw_input` y genere una respuesta relevante

## Lo que debes hacer

### Paso 1 — Verificar que OpenRouter está configurado

```bash
cat ~/oli/.env.local | grep OPENROUTER
# Debe mostrar: OPENROUTER_API_KEY=sk-or-...
```

Si está, ya está listo. Si no:
```bash
echo "OPENROUTER_API_KEY=tu-key" >> ~/oli/.env.local
```

### Paso 2 — Cambiar el modelo provider en .env.local

```bash
# Agregar o actualizar estas líneas en .env.local:
echo "OLI_MODEL_PROVIDER=openai_compatible" >> ~/oli/.env.local
echo "OLI_DEFAULT_MODEL=openrouter/quasar-alpha" >> ~/oli/.env.local
```

### Paso 3 — Relanzar el servidor

```bash
# Matar el proceso anterior si está corriendo
pkill -f uvicorn

# Relanzar
cd ~/oli
python -m uvicorn apps.api.main:app --host 127.0.0.1 --port 8000 &

# Verificar modelo activo
curl http://127.0.0.1:8000/models/status
```

El status debe mostrar `provider: openai_compatible` y el modelo configurado.

### Paso 4 — Repetir la petición del cockpit

```bash
curl -X POST http://127.0.0.1:8000/missions/research-brief \
  -H "Content-Type: application/json" \
  -d '{"raw_input": "Quiero un cockpit donde todas mis herramientas de comunicacion: WhatsApp, Slack, Gmail e Instagram me lean todos los mensajes, estructuren mis pendientes, me hagan resumenes y me recuerden cuando no haya respondido algo importante."}'
```

Guarda el `mission_id`.

### Paso 5 — Recuperar el output completo

```bash
MISSION_ID="el-id-que-devolvio"

curl http://127.0.0.1:8000/missions/$MISSION_ID | python -m json.tool
curl http://127.0.0.1:8000/missions/$MISSION_ID/evidence | python -m json.tool
curl http://127.0.0.1:8000/missions/$MISSION_ID/report | python -m json.tool
```

### Paso 6 — Comparar output

Documenta en `.bridge/tasks/TASK-005-output.md`:
- El texto que generó el modelo real (campo `output` de la misión)
- Qué tan relevante fue para la petición del cockpit vs el mock de TASK-004
- El `model_provider_used` que aparece en la evidencia

## Entregable esperado

1. `.bridge/tasks/TASK-005-output.md` con el output real del modelo
2. Comparación honesta: ¿el modelo interpretó la petición del cockpit o siguió respondiendo sobre competidores?
3. Este archivo actualizado con `status: WAITING_FOR_CLAUDE`

## Notas del agente anterior (Claude)

- El `research-brief` orchestrator tiene la intención hardcodeada — aunque el modelo genere texto relevante, el plan de pasos siempre será el de "competitor research". Eso lo arreglo yo en la siguiente iteración si el modelo demuestra que puede interpretar el input diferente.
- Lo que queremos ver en este test: ¿el campo `output` de la misión cambia con un modelo real? ¿El texto es relevante para WhatsApp/Slack/Gmail o sigue siendo genérico?
- Si el modelo responde algo relevante al cockpit aunque el plan sea de research → eso nos dice que el problema está en el orchestrator, no en el modelo. Y eso lo arreglo yo.
- Si el modelo también ignora el input → el problema es más profundo en cómo le pasamos el contexto.
