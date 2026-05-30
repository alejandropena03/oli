# ADR-010 — Arquitectura de orquestación: LangGraph

**Estado:** accepted
**Fecha:** 2026-05-26
**Decisión:** LangGraph es el motor de orquestación de misiones de Oli

---

## Contexto

LangGraph es un framework de Python para construir agentes y workflows stateful como grafos.
En Oli, cada misión es un grafo de estados con nodos (acciones), edges (transiciones),
checkpoints (persistencia) y human-in-the-loop interrupts (approval gates).

La misión de Oli es exactamente el caso de uso para el que fue diseñado LangGraph.

---

## Cómo LangGraph mapea al Mission Kernel de Oli

### El grafo de una misión

```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.postgres import PostgresSaver

# El estado completo de una misión — persiste en Postgres
class MissionState(TypedDict):
    mission_id: str
    raw_input: str
    interpreted_intent: InterpretedIntent | None
    context: MissionContext | None
    plan: MissionPlan | None
    permission_class: int | None
    current_step_index: int
    step_results: list[StepResult]
    validation_result: ValidationResult | None
    output: Any | None
    evidence: list[EvidenceRef]
    report: MissionReport | None
    status: MissionStatus
    error: str | None

# El grafo de misión
builder = StateGraph(MissionState)

# Nodos — cada uno es una función Python
builder.add_node("interpret_intent",   interpret_intent_node)
builder.add_node("retrieve_context",   retrieve_context_node)
builder.add_node("classify_permissions", classify_permissions_node)
builder.add_node("create_plan",        create_plan_node)
builder.add_node("request_approval",   request_approval_node)  # human interrupt
builder.add_node("execute_step",       execute_step_node)
builder.add_node("troubleshoot",       troubleshoot_node)
builder.add_node("validate_output",    validate_output_node)
builder.add_node("deliver",            deliver_node)
builder.add_node("generate_report",    generate_report_node)
builder.add_node("update_memory",      update_memory_node)

# Edges — las transiciones
builder.set_entry_point("interpret_intent")
builder.add_edge("interpret_intent",     "retrieve_context")
builder.add_edge("retrieve_context",     "classify_permissions")
builder.add_edge("classify_permissions", "create_plan")

# Edge condicional — ¿necesita aprobación?
builder.add_conditional_edges(
    "create_plan",
    lambda state: "request_approval" if state["permission_class"] >= 2 else "execute_step",
    {"request_approval": "request_approval", "execute_step": "execute_step"}
)

# Approval gate — human interrupt
builder.add_edge("request_approval", "execute_step")  # continúa tras aprobación

# Execute con troubleshooting
builder.add_conditional_edges(
    "execute_step",
    route_after_execution,  # all_done → validate | step_failed → troubleshoot | blocked → END
    {"validate": "validate_output", "troubleshoot": "troubleshoot", "blocked": END}
)

builder.add_conditional_edges(
    "troubleshoot",
    lambda s: "execute_step" if s["repair_succeeded"] else "blocked",
    {"execute_step": "execute_step", "blocked": END}
)

# Checkpoint para persistencia — si el proceso se cae, la misión se puede reanudar
checkpointer = PostgresSaver.from_conn_string(POSTGRES_URL)
mission_graph = builder.compile(checkpointer=checkpointer)
```

### El human-in-the-loop — approval gates reales

LangGraph tiene soporte nativo para interrumpir el grafo y esperar input humano:

```python
# Configura el grafo para interrumpirse antes de nodos críticos
mission_graph = builder.compile(
    checkpointer=checkpointer,
    interrupt_before=["request_approval"]  # pausa aquí, espera aprobación
)

# El founder ve el plan y aprueba desde la UI
# Luego el worker reanuda desde el checkpoint
result = mission_graph.invoke(
    None,  # None = reanudar desde el último checkpoint
    config={"configurable": {"thread_id": mission_id}}
)
```

Esto es exactamente como funciona el `awaiting_approval` state de la Mission State Machine.

---

## Cómo el Model Router se integra en LangGraph

En cada nodo que necesita un LLM, el Model Router decide qué modelo usar:

```python
from packages.model_router import ModelRouter, TaskType

router = ModelRouter()

async def interpret_intent_node(state: MissionState) -> MissionState:
    # El router decide: ¿GPU local o API?
    model = router.get_model(TaskType.INTENT_INTERPRETATION)
    # Si hay GPU disponible y el modelo local es suficiente → local ($0)
    # Si no hay GPU o la tarea es muy compleja → API (Claude/GPT)
    
    result = await model.invoke(
        messages=[
            SystemMessage(content=INTERPRET_INTENT_PROMPT),
            HumanMessage(content=state["raw_input"])
        ]
    )
    return {"interpreted_intent": parse_intent(result)}
```

### Las tier decisions del Model Router

```python
class ModelRouter:
    def get_model(self, task: TaskType) -> BaseChatModel:
        
        # TIER 1 — modelo local siempre que pueda
        # Intent, clasificación, routing, queries de memoria
        if task in TIER_1_TASKS and self.gpu_available:
            return OllamaModel(model=self.tier1_model)  # $0
        
        # TIER 2 — modelo mediano, local si GPU potente, API si no
        # Planning, síntesis, redacción
        elif task in TIER_2_TASKS:
            if self.gpu_vram_gb >= 48:
                return OllamaModel(model=self.tier2_model)  # $0
            else:
                return AnthropicModel(model="claude-haiku-4-5")  # barato
        
        # TIER 3 — siempre API frontier
        # Arquitectura compleja, código profundo, análisis crítico
        elif task in TIER_3_TASKS:
            return AnthropicModel(model="claude-sonnet-4-6")
        
        # Privacy override — usuario eligió local_only
        elif self.privacy_mode == "local_only":
            return OllamaModel(model=self.best_available_local())

TIER_1_TASKS = {
    TaskType.INTENT_INTERPRETATION,
    TaskType.PERMISSION_CLASSIFICATION,
    TaskType.MEMORY_QUERY_GENERATION,
    TaskType.STEP_ROUTING,
    TaskType.BASIC_VALIDATION,
}

TIER_2_TASKS = {
    TaskType.PLAN_CREATION,
    TaskType.SYNTHESIS,
    TaskType.REPORT_GENERATION,
    TaskType.DRAFT_WRITING,
}

TIER_3_TASKS = {
    TaskType.COMPLEX_ARCHITECTURE,
    TaskType.DEEP_CODE_ANALYSIS,
    TaskType.CRITICAL_DECISION_SUPPORT,
}
```

---

## Cómo el troubleshooting se implementa en LangGraph

El nodo `troubleshoot` implementa el ciclo de diagnóstico real (ADR-006):

```python
async def troubleshoot_node(state: MissionState) -> MissionState:
    failed_step = state["step_results"][-1]
    error = failed_step.error
    
    # 1. Clasificar el error
    error_type = classify_error(error)
    
    # 2. Estrategia según tipo
    if error_type == "transient":
        strategy = RetryStrategy(backoff=[1, 4, 16])
    elif error_type == "auth":
        strategy = RefreshTokenStrategy()
    elif error_type == "tool_unavailable":
        strategy = AlternativeToolStrategy(tool_registry=TOOL_REGISTRY)
    elif error_type == "logic_error":
        strategy = ReplanStrategy(orchestrator=orchestrator)
    else:
        # No hay estrategia — bloquear y escalar
        return {**state, "status": "blocked", "error": format_block_context(state)}
    
    # 3. Intentar la estrategia
    result = await strategy.execute(failed_step, state)
    
    if result.success:
        # Volver a execute_step con el step corregido
        return {**state, "repair_succeeded": True, "current_step": result.corrected_step}
    else:
        # La estrategia falló — hay info nueva, ¿intentar otra?
        if strategy.has_alternative() and result.produced_new_info:
            return {**state, "repair_succeeded": False, "next_strategy": strategy.next()}
        else:
            return {**state, "status": "blocked", "error": format_block_context(state)}
```

---

## Suboperadores como nodos LangGraph especializados

Cada suboperador es un sub-grafo de LangGraph que el orquestador puede invocar:

```python
# MarketResearchSuboperator como sub-grafo
market_research_graph = build_market_research_graph()

async def execute_step_node(state: MissionState) -> MissionState:
    step = state["plan"].steps[state["current_step_index"]]
    
    # Rutear al suboperador correcto
    if step.executor == "MarketResearchSuboperator":
        result = await market_research_graph.ainvoke({
            "instruction": step.description,
            "tools": get_tools_for(step),
            "context": state["context"],
        })
    elif step.executor == "ExecutionSuboperator":
        result = await execution_graph.ainvoke(...)
    # ...etc
    
    return {**state, "step_results": [*state["step_results"], result]}
```

---

## Persistencia — por qué Postgres + pgvector (no ChromaDB)

Una sola base de datos para todo:

```
Postgres:
  - Estado de misiones (JSON en columnas tipadas)
  - Checkpoints de LangGraph (tabla nativa de langgraph-checkpoint-postgres)
  - Memoria estructurada (queries exactas)
  - Audit trail (inmutable)
  - Artifacts metadata

pgvector (extensión de Postgres):
  - Memoria semántica (embeddings de todo lo que Oli aprendió)
  - RAG retrieval (búsqueda por similitud)
  - Sin base de datos adicional — pgvector vive dentro de Postgres
```

ChromaDB es excelente para prototipos. Para producción, pgvector dentro de Postgres
elimina una dependencia y da consistencia transaccional entre el estado y los embeddings.

```sql
-- La extensión de pgvector se activa una vez
CREATE EXTENSION vector;

-- Tabla de memoria semántica
CREATE TABLE memory_entries (
    id UUID PRIMARY KEY,
    layer TEXT NOT NULL,  -- 'user' | 'company' | 'mission'
    key TEXT NOT NULL,
    value JSONB,
    embedding vector(768),  -- nomic-embed-text dimensions
    confidence FLOAT,
    source TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índice para búsqueda semántica rápida
CREATE INDEX ON memory_entries USING ivfflat (embedding vector_cosine_ops);

-- Query de RAG: recuperar lo relevante para una misión
SELECT key, value, 1 - (embedding <=> $1) AS similarity
FROM memory_entries
WHERE layer = ANY($2)
  AND confidence >= $3
ORDER BY embedding <=> $1
LIMIT $4;
```

---

## Consecuencias

**Positivo:**
- Misiones de horas no se pierden si el proceso se cae — LangGraph resume desde checkpoint
- Los approval gates son naturales en el grafo — no requieren lógica manual
- Una sola DB (Postgres + pgvector) para estado Y memoria semántica
- LangSmith para observabilidad completa en producción
- El troubleshooting real es un nodo del grafo — fácil de testear y mejorar

**Negativo:**
- LangGraph tiene curva de aprendizaje más alta que frameworks más simples
- Python requiere gestionar el entorno virtual, dependencias, etc.
- pgvector requiere activar la extensión en Postgres

**Riesgo gestionado:**
- Si en V3+ LangGraph no es suficiente para casos extremos → Temporal como complemento
  (pero LangGraph checkpointing debería ser suficiente para V0-V2)
