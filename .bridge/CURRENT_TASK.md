---
task_id: TASK-007
status: WAITING_FOR_CLAUDE
owner: claude
created_by: claude
created_at: 2026-06-02T07:00Z
updated_at: 2026-06-02T07:30Z
---

## Misión

Validar los 4 fixes del orchestrator V2 en entorno real y documentar si la petición del cockpit ahora termina `completed_partial`.

## Contexto

Claude cerró los 4 problemas reportados en TASK-006:

1. `connector_required` es ahora un field Pydantic real en `MissionStep` — visible en la respuesta serializada de la API
2. `COMPLETED_PARTIAL` es un nuevo estado en el kernel — misiones con conectores faltantes no son `failed`
3. Validación LLM tiene fallback local honesto — si el LLM no devuelve JSON, se evalúa con heurísticas reales
4. Cost tracking real — tokens y wall time medidos, no estimados a 0

## Lo que debes hacer

### Paso 1 — Actualizar y correr tests

```bash
cd ~/oli
git pull personal main
py -m pytest -v
```

Esperar ≥ 61 tests (57 anteriores + 4 nuevos en test_slice_001_mock.py).
Si alguno falla, documentar el error exacto.

### Paso 2 — Levantar API con OpenRouter

```bash
pkill -f uvicorn
cd ~/oli
python -m uvicorn apps.api.main:app --host 127.0.0.1 --port 8000 &
sleep 3
curl http://127.0.0.1:8000/models/status
```

### Paso 3 — Repetir petición del cockpit

```bash
curl -s -X POST http://127.0.0.1:8000/missions/research-brief \
  -H "Content-Type: application/json" \
  -d '{
    "raw_input": "Quiero un cockpit donde todas mis herramientas de comunicacion: WhatsApp, Slack, Gmail e Instagram me lean todos los mensajes, estructuren mis pendientes, me hagan resumenes y me recuerden cuando no haya respondido algo importante."
  }' | python -m json.tool > /tmp/task-007-mission.json

python -c "
import json
m = json.load(open('/tmp/task-007-mission.json'))
print('STATUS:', m['status'])
print('GOAL:', m['interpreted_intent']['goal'] if m['interpreted_intent'] else 'N/A')
print('STEPS total:', len(m['plan']['steps']) if m['plan'] else 0)
print()
if m['plan']:
    for s in m['plan']['steps']:
        print(f\"  Step {s['order']}: {s['status']} | connector_required={s.get('connector_required')} | {s['description'][:60]}\")
print()
print('VALIDATION score:', m['validation_result']['score'] if m['validation_result'] else 'N/A')
print('OUTPUT chars:', len(m.get('output','') or ''))
print('COST tokens in/out:', m['cost']['input_tokens'], '/', m['cost']['output_tokens'])
print('COST usd:', m['cost']['model_cost_usd'])
print('DURATION ms:', m['cost']['duration_ms'])
"
```

### Paso 4 — Documentar en .bridge/tasks/TASK-007-output.md

- Resultado de pytest (N passed)
- Status de la misión (esperado: `completed_partial`)
- `connector_required` visible en steps (esperado: whatsapp, slack, gmail, instagram)
- Score de validación (esperado: > 0)
- Cost tracking real (esperado: tokens > 0, cost_usd > 0)
- Evaluación honesta: ¿qué mejoró, qué falta?

## Criterio de éxito

- Tests: ≥ 61 pasando
- Status: `completed_partial` (no `failed`)
- `connector_required` visible y correcto en steps bloqueados
- Validation score > 0 (fallback local funcionó si el LLM no devolvió JSON)
- Cost tracking con números reales (no 0)
