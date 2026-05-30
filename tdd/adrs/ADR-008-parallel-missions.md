# ADR-008 — Misiones en paralelo

**Estado:** accepted
**Fecha:** 2026-05-26
**Deciders:** Alejandro Peña (founder) — decisión explícita

---

## Contexto

¿Cuántas misiones puede Oli correr simultáneamente? La respuesta afecta la arquitectura de concurrencia, el uso del modelo, la experiencia del founder y la estabilidad del sistema.

## Decisión

**Oli corre múltiples misiones en paralelo, limitado conservadoramente por la capacidad del modelo local.**

El límite no es arbitrario — es la capacidad real del runtime. En V0, esto significa probablemente 2-3 misiones activas con pasos en ejecución simultánea, con las demás en cola o en estado awaiting_approval.

## Alternativas consideradas

| Opción | Pros | Contras |
|---|---|---|
| A — Una a la vez | Simple, predecible | No refleja cómo trabaja un operador real |
| **B — Paralelo conservador ✓** | Refleja trabajo real del founder | Requiere gestión de concurrencia y recursos |
| C — Paralelo por tipo | Flexibilidad granular | Complejidad prematura |

## Consecuencias

- El sistema necesita un **Mission Queue Manager** — gestiona qué misiones están activas, cuáles en pausa, cuáles en cola
- El `max_concurrent_missions` es configurable — default conservador: `min(3, model_capacity)`
- Misiones en `awaiting_approval` y `blocked` no cuentan para el límite (no consumen modelo)
- Misiones en `executing` y `validating` sí cuentan
- Conflictos de recursos (dos misiones leen/escriben a la misma memoria) → cola de escritura FIFO

## Implementación

```typescript
interface MissionQueueManager {
  max_concurrent: number  // configurable, default: 3
  active: Mission[]       // executing | validating
  pending: Mission[]      // planning | awaiting_approval
  blocked: Mission[]      // blocked | awaiting human input
  
  canActivate(mission: Mission): boolean
  activate(mission_id: string): void
  pause(mission_id: string): void
  getResourceConflicts(mission_id: string): ResourceConflict[]
}
```

## Nota de producto

En la UI, el founder debe poder ver de un vistazo todas las misiones activas y su estado. La "Mission List" con estados reales (no animación) es la vista más importante del producto.
