# TASK-004 — Output hardcodeado de Claude (referencia para comparación)

Este output fue escrito a mano por Claude en Python. No pasó por el Mission Kernel real.
No tiene valor como demo — solo sirve como punto de comparación.

## Lo que Claude inventó

**Plan (hardcodeado):** 9 pasos con permisos por paso
**Datos:** Carlos, Maria, investor@vc.com — inventados
**Briefing:** "4 canales revisados. 4 conversaciones requieren tu respuesta."
**Validación:** 5/5 criterios pasados — contra datos que él mismo fabricó
**Evidencia:** 8 registros — simulados, no guardados en Postgres

## El problema

Claude escribió código Python que simula lo que Oli haría.
Eso no es una demo — es teatro. El Mission Kernel no procesó nada.
El modelo no intervino. Postgres no guardó nada.

## Por qué se eliminó

Porque la demo real es: petición HTTP → Oli la procesa → Mission Kernel corre →
resultado guardado en Postgres → tú ves el output real.

Eso es lo que DeepSeek va a ejecutar en TASK-004.
