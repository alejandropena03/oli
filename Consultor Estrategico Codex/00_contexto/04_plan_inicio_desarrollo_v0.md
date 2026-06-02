# Plan de inicio desarrollo V0 - Oli

Fecha: 2026-05-30
Autor: Codex como consultor estrategico
Estado: Recomendacion de arranque, sin modificar codigo fuente del producto

## Veredicto

Lo primero que debe desarrollarse es el Mission Kernel minimo.

El repo lo dice de forma explicita en `tdd/README.md`: el proximo paso de Build V0 tiene un orden estricto:

1. `pyproject.toml` / `requirements.txt`
2. `packages/mission_kernel/`
   - `mission_state.py`
   - `state_machine.py`
   - `policies.py`
3. `packages/orchestrator/`
   - `mission_graph.py`
   - `nodes.py`
   - `router.py`
4. `apps/api/`
   - `main.py`
   - `missions.py`
5. `tests/test_slice_001.py`

Mi recomendacion: no empezar por todo ese bloque completo. Empezar por una version aun mas pequena y verificable:

```text
Primer commit real:
- pyproject.toml
- packages/mission_kernel/mission_state.py
- packages/mission_kernel/state_machine.py
- packages/mission_kernel/policies.py
- tests/test_mission_kernel.py
```

Eso convierte a Oli de "arquitectura en papel" a "nucleo ejecutable".

## Por que esto es lo primero

Oli se define como un supervisor de ejecucion digital. Su unidad central no es un chat, una pagina web ni un agente suelto. Su unidad central es una mision.

Por eso, el primer objeto vivo del sistema debe ser:

```text
Mission
```

Y la primera capacidad viva debe ser:

```text
crear una mision -> avanzar estados validos -> rechazar transiciones invalidas
```

Si eso no existe, todo lo demas es decoracion: UI, agentes, memoria, herramientas, reportes y playbooks dependen de que el Mission Kernel gobierne el ciclo de vida.

## Primer objetivo tecnico

Construir un Mission Kernel que pueda:

1. Crear una mision desde `raw_input`.
2. Representar los estados principales definidos en `tdd/domain/state-machine.md`.
3. Validar transiciones permitidas.
4. Bloquear transiciones invalidas.
5. Determinar si una mision necesita input humano.
6. Determinar si una mision esta activa.
7. Determinar si una mision es terminal.
8. Calcular si un plan requiere aprobacion humana segun permission class.

## Alcance recomendado del primer build

### Incluir

- Python 3.12.
- Pydantic para contratos.
- Enum de estados.
- Modelo `Mission`.
- Modelo `InterpretedIntent` minimo.
- Modelo `MissionPlan` minimo.
- Modelo `MissionStep` minimo.
- `transition(mission, target_status, reason=None)`.
- Tests unitarios de transiciones.

### No incluir todavia

- FastAPI.
- LangGraph.
- Postgres.
- pgvector.
- Ollama.
- Browser automation.
- UI.
- Multi-user.
- Memoria persistente.
- Agentes reales.

La razon: el primer riesgo no es falta de infraestructura; es no tener un nucleo verificable.

## Test inicial que deberia existir

El primer test deberia probar algo asi:

```text
Dado un raw_input del founder
Cuando se crea una mision
Entonces queda en intake_received

Dado que la mision esta en intake_received
Cuando transiciona a interpreting_intent
Entonces la transicion es valida

Dado que la mision esta en intake_received
Cuando intenta transicionar directo a completed
Entonces falla con InvalidTransition
```

Ese test parece pequeno, pero cambia la naturaleza del proyecto: ya hay una autoridad ejecutable que protege el flujo de Oli.

## Primera vertical slice despues del kernel

Despues del Mission Kernel, la primera mission-class deberia ser `research-brief-v1`, basada en `tdd/slices/slice-001-research-brief.md`.

La version inicial debe ser mockeada:

```text
intake_received
-> interpreting_intent
-> retrieving_context
-> classifying_permissions
-> planning
-> executing
-> validating
-> delivering
-> generating_report
-> updating_memory
-> completed
```

El objetivo no es investigar perfecto todavia. El objetivo es probar que Oli puede:

- interpretar una intencion,
- construir un plan,
- ejecutar pasos,
- validar criterios,
- generar reporte,
- dejar evidencia,
- cerrar una mision.

## Criterio de exito de la primera semana

La primera semana termina bien si existe:

```text
pytest
```

y pasa al menos:

```text
tests/test_mission_kernel.py
tests/test_slice_001_mock.py
```

Con eso, Oli deja de ser solo documentacion y empieza a tener columna vertebral.

## Decision recomendada

Congelar por ahora:

- nuevos ADRs,
- nuevos documentos de estrategia,
- nuevas versiones de pricing,
- expansion de tools,
- multi-user,
- UI,
- growth automation.

Activar:

- Mission Kernel,
- test del flujo,
- slice-001 mockeado,
- trace minimo.

Regla operativa:

```text
Si una tarea no ayuda a ejecutar slice-001, no entra al sprint V0.0.
```

