# LangGraph Mission Graph — Oli

**Fecha:** 2026-05-26
**Propósito:** Describir cómo los 18 estados de la State Machine se implementan como nodos y edges en LangGraph.

---

## Mapeo State Machine → LangGraph

```
STATE MACHINE (abstracto)     →    LANGGRAPH (implementación)
─────────────────────────────────────────────────────────────
idle                          →    Estado inicial del grafo
listening                     →    API endpoint recibe el input
intake_received               →    Entry point del grafo
interpreting_intent           →    Nodo: interpret_intent
clarifying                    →    Interrupt: human_clarification
retrieving_context            →    Nodo: retrieve_context
classifying_permissions       →    Nodo: classify_permissions
planning                      →    Nodo: create_plan
awaiting_approval             →    Interrupt: human_approval
executing                     →    Nodo: execute_step (loop)
repairing                     →    Nodo: troubleshoot
validating                    →    Nodo: validate_output
delivering                    →    Nodo: deliver
generating_report             →    Nodo: generate_report
updating_memory               →    Nodo: update_memory
completed                     →    END (success)
blocked                       →    END (blocked) + notificación
failed                        →    END (failed) + notificación
cancelled                     →    END (cancelled)
archived                      →    DB operation post-END
```

---

## El grafo completo

```
                    [ENTRY]
                       │
                       ▼
              [interpret_intent]
                  /          \
          ambiguous?         clear?
              │                │
      [human_clarification]    │
         (interrupt)           │
              │                │
              └────────────────┘
                       │
                       ▼
             [retrieve_context]
                       │
                       ▼
          [classify_permissions]
                       │
                       ▼
               [create_plan]
                  /          \
          class >= 2?       class < 2?
              │                │
      [human_approval]         │
         (interrupt)           │
         /       \             │
    approved?  rejected?       │
        │          │           │
        │      [END:cancelled] │
        └──────────────────────┘
                       │
                       ▼
               [execute_step] ◄──────────────┐
                  /    |    \                 │
          done?  fail? critical?             repair
            │      │      │                 succeeded
            │      │   [END:failed]          │
            │   [troubleshoot]───────────────┘
            │      │
            │   blocked?
            │      │
            │   [END:blocked]
            │
            ▼
       [validate_output]
          /          \
      passed?       failed?
         │               │
         │        auto_repair?
         │          /       \
         │       yes?        no?
         │         │           │
         │   [troubleshoot]  [human_escalation]
         │         │         (interrupt)
         │         └──────────┘
         │
         ▼
       [deliver]
          │
          ▼
    [generate_report]
          │
          ▼
    [update_memory]
          │
          ▼
       [END:completed]
```

---

## Los Human Interrupts — dónde Oli para y espera

LangGraph implementa los interrupts con `interrupt_before` en la compilación del grafo:

```python
graph = builder.compile(
    checkpointer=PostgresSaver(...),
    interrupt_before=[
        "human_clarification",  # cuando el intent es ambiguo
        "human_approval",       # cuando permission_class >= 2
        "human_escalation",     # cuando la validación falla y no hay auto-repair
    ]
)
```

Cuando el grafo llega a uno de estos nodos:
1. Guarda el estado completo en Postgres (checkpoint)
2. El proceso termina (no bloquea el worker)
3. El frontend recibe un evento SSE: "misión en espera de input"
4. El usuario ve la cola de aprobaciones en la UI
5. Cuando el usuario responde → el worker reanuda desde el checkpoint

Esto es lo que hace posible que Oli tenga misiones largas que sobreviven reinicios.

---

## El execution loop — cómo se itera por los steps

```python
async def execute_step_node(state: MissionState) -> MissionState:
    plan = state["plan"]
    idx = state["current_step_index"]
    
    if idx >= len(plan.steps):
        # Todos los steps completados → ir a validación
        return {**state, "all_steps_done": True}
    
    step = plan.steps[idx]
    
    # Verificar permiso antes de ejecutar
    if step.permission_class > state["user_permission_threshold"]:
        # Necesita aprobación específica para este step
        return {**state, "pending_approval": step}
    
    # Ejecutar via el executor correcto
    result = await executor_registry[step.executor].execute(step, state)
    
    if result.success:
        return {
            **state,
            "step_results": [*state["step_results"], result],
            "current_step_index": idx + 1,
            "step_failed": False,
        }
    else:
        return {
            **state,
            "step_results": [*state["step_results"], result],
            "step_failed": True,
            "last_error": result.error,
        }

def route_after_execution(state: MissionState) -> str:
    if state.get("all_steps_done"):
        return "validate_output"
    elif state.get("step_failed"):
        return "troubleshoot"
    elif state.get("pending_approval"):
        return "human_approval"
    else:
        return "execute_step"  # siguiente step
```

---

## Checkpointing — misiones que sobreviven reinicios

LangGraph guarda el estado completo en Postgres después de cada nodo:

```sql
-- Tabla creada automáticamente por langgraph-checkpoint-postgres
-- Cada fila es un checkpoint de un thread (misión)
CREATE TABLE checkpoints (
    thread_id    TEXT,
    checkpoint_id TEXT,
    parent_id    TEXT,
    type         TEXT,
    checkpoint   BYTEA,
    metadata     BYTEA,
    PRIMARY KEY (thread_id, checkpoint_id)
);
```

Si el worker se cae mientras ejecuta una misión:
1. El proceso se reinicia
2. El worker detecta las misiones en estado `executing` sin worker activo
3. Llama a `graph.invoke(None, config={"thread_id": mission_id})`
4. LangGraph carga el último checkpoint y continúa desde ahí

El usuario nunca ve que la misión se interrumpió.

---

## Observabilidad con LangSmith

Cada nodo del grafo genera un trace en LangSmith:

```python
from langsmith import traceable

@traceable(name="interpret_intent")
async def interpret_intent_node(state: MissionState) -> MissionState:
    # LangSmith captura:
    # - Input del nodo (state)
    # - LLM calls con tokens usados
    # - Output del nodo
    # - Tiempo de ejecución
    # - Errores si los hay
    ...
```

Esto da visibilidad completa por misión:
- ¿Qué nodo falló?
- ¿Cuántos tokens usó cada nodo?
- ¿Cuánto tardó cada step?
- ¿Qué modelo se usó en cada llamada?

---

## Suboperadores como sub-grafos

Cada suboperador es un grafo LangGraph independiente invocado desde el execution loop:

```python
# MarketResearchSuboperator — su propio grafo
market_research = StateGraph(MarketResearchState)
market_research.add_node("identify_sources",  identify_sources_node)
market_research.add_node("research_source",   research_source_node)  # loop
market_research.add_node("synthesize",        synthesize_node)
market_research.add_node("verify_sources",    verify_sources_node)
# ...
market_research_graph = market_research.compile()

# Se invoca desde el execution loop principal
result = await market_research_graph.ainvoke({
    "instruction": step.description,
    "tools": available_tools,
    "context": state["context"],
})
```

Los suboperadores NO tienen acceso al grafo principal — solo reciben su task y devuelven su resultado.
El grafo principal no sabe cómo el suboperador hace su trabajo — solo lee el resultado.
