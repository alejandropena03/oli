# Vertical Slice 001 — Research Brief Mission

**Estado:** ✅ En papel
**Fecha:** 2026-05-26
**Pregunta:** ¿Puede Oli ejecutar esta misión de punta a punta con la arquitectura actual?

---

## La misión

**Intención del usuario:**
> "Investiga los 3 principales competidores de Oli y dame un brief de 1 página con sus fortalezas, debilidades y el gap que Oli puede explotar."

**Por qué esta misión como slice-001:**
- Representativa del trabajo real del founder en esta etapa
- Requiere todos los módulos del Mission Kernel
- No requiere ejecución de código ni filesystem (permiso clase 0)
- Output verificable manualmente
- Primera candidata a playbook reutilizable

---

## Flujo completo

### 1. Intake
```
raw_input: "Investiga los 3 principales competidores de Oli..."
timestamp: T+0
source: founder_chat
```

### 2. Interpretar intención
```json
{
  "goal": "competitor_research_brief",
  "scope": "top_3_competitors",
  "output_format": "1-page_brief",
  "success_criteria": [
    "fortalezas identificadas por competidor",
    "debilidades identificadas por competidor",
    "gap_exploitable definido"
  ]
}
```

### 3. Recuperar contexto
```
User memory:    founder prefiere resúmenes ejecutivos, sin listas > 5 ítems
Company memory: Oli = execution operator, ICP = founders/operadores, pricing = $149/seat
Mission memory: sin misiones similares previas
```

### 4. Clasificar permisos
```
Acciones requeridas:
  - Web research:    permission_class = 0 (read only)
  - Generate text:   permission_class = 0
Total: permission_class = 0 → NO se requiere aprobación
```

### 5. Crear plan
```
Step 1: Identificar top 3 competidores (MarketResearchSuboperator)
Step 2: Research Lindy (MarketResearchSuboperator)
Step 3: Research Dust (MarketResearchSuboperator)
Step 4: Research Claude Projects (MarketResearchSuboperator)
Step 5: Sintetizar en formato brief (Oli / Orchestrator)
Step 6: Validar contra success_criteria (ValidationSuboperator)
Step 7: Entregar
```

### 6. Ejecutar (mock en V0)
```
Step 1 output: ["Lindy", "Dust", "Claude Projects"]
Step 2-4 output: {
  Lindy:           { strengths: [...], weaknesses: [...], positioning: "..." },
  Dust:            { strengths: [...], weaknesses: [...], positioning: "..." },
  ClaudeProjects:  { strengths: [...], weaknesses: [...], positioning: "..." }
}
Step 5 output: [brief 1 página]
```

### 7. Validar
```
✅ fortalezas identificadas (3 × 3+)
✅ debilidades identificadas (3 × 2+)
✅ gap_exploitable definido
✅ formato 1 página (< 600 palabras)
```

### 8. Reporte de misión
```json
{
  "duration_min": 8,
  "cost_usd": 0.12,
  "human_time_saved_hr": 2,
  "steps_completed": "7/7",
  "validation": "passed",
  "playbook_candidate": true,
  "playbook_name": "research-brief-v1"
}
```

### 9. Actualizar memoria
```
Mission memory: tipo=research_brief, playbook_candidate=true
Company memory: competidores actualizado con nueva info
```

---

## Módulos usados

| Módulo | Rol |
|---|---|
| Mission Kernel | Orquesta ciclo completo |
| Orchestrator | Intent → plan |
| Permission Service | Determina: no aprobación necesaria |
| Memory Graph | Recupera preferencias y contexto |
| MarketResearchSuboperator | Ejecuta research |
| ValidationSuboperator | Valida criterios |
| Evidence Store | Guarda steps y fuentes |
| Cost Tracker | Registra tokens y tiempo |
| Playbook Engine | Propone playbook candidate |

---

## Gaps identificados en arquitectura

- ✅ Todos los módulos necesarios están definidos
- 🔴 ¿Cómo se pasan resultados entre suboperadores? ¿Qué formato tiene el output de MarketResearchSuboperator?
- 🔴 ¿El Orchestrator puede subdividir pasos dinámicamente?
- 🔴 ¿Cómo se detecta automáticamente un playbook candidate?
