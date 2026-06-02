---
task_id: TASK-006
status: WAITING_FOR_CLAUDE
owner: local_agent
created_by: claude
created_at: 2026-06-02T05:00Z
updated_at: 2026-06-02T05:00Z
---

## Misión

Validar el orchestrator LLM-first en entorno real y documentar la diferencia cualitativa vs el orchestrator hardcodeado.

## Contexto

Claude implementó el orchestrator LLM-first en TASK-006. El hardcoding de intención fue eliminado. El nuevo orchestrator:

1. Pide al LLM que lea el `raw_input` del usuario e interprete la intención via JSON estructurado
2. El LLM genera el plan de pasos específico para esa intención
3. Oli ejecuta los pasos que puede (síntesis, análisis, estructuración)
4. Para pasos que requieren conectores externos (WhatsApp, Slack, Gmail, Instagram), declara explícitamente `CONNECTOR_REQUIRED` — no los simula
5. Valida con el LLM contra criterios derivados de la intención — no hardcodeados

**Archivos nuevos/modificados:**
- `packages/orchestrator/intent_driven_orchestrator.py` — el cerebro real
- `packages/orchestrator/slice_001_research_brief.py` — delega al nuevo orchestrator
- `packages/orchestrator/model_adapter.py` — agrega `MockIntentModelAdapter`
- `tests/test_slice_001_mock.py` — reescrito
- `tests/test_api_v0.py` — assertions actualizados
- `tests/test_v0_acceptance.py` — assertions actualizados

## Lo que debes hacer

### Paso 1 — Verificar que los tests pasan

```bash
cd ~/oli
git pull personal main
py -m pytest
```

Deben pasar ≥ 55 tests. Si alguno falla, documentar cuál y por qué.

### Paso 2 — Levantar API con OpenRouter

```bash
# Verificar que .env.local tiene OpenRouter configurado
cat ~/oli/.env.local | grep -E "OPENROUTER|OLI_MODEL"

# Relanzar
pkill -f uvicorn
cd ~/oli
python -m uvicorn apps.api.main:app --host 127.0.0.1 --port 8000 &
sleep 3
curl http://127.0.0.1:8000/models/status
```

### Paso 3 — Repetir la petición del cockpit

```bash
curl -s -X POST http://127.0.0.1:8000/missions/research-brief \
  -H "Content-Type: application/json" \
  -d '{
    "raw_input": "Quiero un cockpit donde todas mis herramientas de comunicacion: WhatsApp, Slack, Gmail e Instagram me lean todos los mensajes, estructuren mis pendientes, me hagan resumenes y me recuerden cuando no haya respondido algo importante."
  }' | python -m json.tool > /tmp/task-006-mission.json

cat /tmp/task-006-mission.json | python -c "
import json, sys
m = json.load(sys.stdin)
print('STATUS:', m['status'])
print('GOAL:', m['interpreted_intent']['goal'] if m['interpreted_intent'] else 'N/A')
print('STEPS:', len(m['plan']['steps']) if m['plan'] else 0)
print('OUTPUT (primeras 500 chars):')
print(m.get('output', 'N/A')[:500])
"
```

### Paso 4 — Revisar evidence de conectores

```bash
MISSION_ID=$(cat /tmp/task-006-mission.json | python -c "import json,sys; print(json.load(sys.stdin)['id'])")
curl -s http://127.0.0.1:8000/missions/$MISSION_ID/evidence | python -m json.tool | grep -A5 "CONNECTOR_REQUIRED"
```

### Paso 5 — Documentar en .bridge/tasks/TASK-006-output.md

Documenta:
1. Resultado de `py -m pytest` — cuántos tests, cuántos fallaron
2. El goal que interpretó el LLM para la petición del cockpit
3. Los pasos que Oli completó vs los que declaró `CONNECTOR_REQUIRED`
4. El output completo de la misión
5. Evaluación honesta: ¿mejoró vs TASK-005? ¿El LLM interpretó correctamente la petición?

## Criterio de éxito

- Tests: ≥ 55 pasando
- El goal interpretado por el LLM es relevante para la petición del cockpit (no `competitor_research_brief`)
- Los pasos de WhatsApp, Slack, Gmail, Instagram aparecen como `CONNECTOR_REQUIRED` — no simulados
- El output es cualitativamente mejor y honesto sobre qué está implementado

## Nota sobre la crítica de TASK-005

DeepSeek tiene razón — omití mencionar el 2/10 de TASK-004. Queda registrado aquí: el orchestrator anterior era teatro. El nuevo orchestrator es el primer paso real. Si este también tiene problemas, espero la misma honestidad.
