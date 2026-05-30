# ADR-019 — Agent Memory & Mission Replay

**Estado:** accepted
**Fecha:** 2026-05-27
**Deciders:** Alejandro Peña (founder)

---

## Contexto

Claude Code no recuerda perfectamente entre proyectos. Codex tampoco funciona como sistema operativo personal. Los agentes externos tienen memoria de sesión, no memoria operacional.

Oli debe ser la **memoria persistente encima de todos los agentes**. Cada misión ejecutada — sin importar qué agente la ejecutó — alimenta una capa de memoria que mejora las misiones futuras.

La segunda parte del problema: una misión que funcionó debe poder reproducirse, auditarse, compararse y convertirse en playbook. Eso requiere que cada misión sea una "caja negra" completa con replay.

---

## Decisión

### 1. La misión como unidad de memoria

Cada misión completada produce automáticamente:

```python
@dataclass
class MissionMemoryPackage:
    """
    Producido al finalizar cada misión. Alimenta memoria, playbooks y solution bank.
    """
    mission_id: str
    mission_class: str
    objective_summary: str           # sin contenido privado — solo estructura
    plan_summary: list[str]          # pasos ejecutados como categorías, no contenido
    tools_used: list[str]            # nombres de herramientas
    agents_used: list[str]           # claude_code | codex | browser_use | local_model | etc.
    models_used: list[ModelCallSummary]
    validation_result: ValidationSummary
    failure_modes: list[str]         # categorías de fallo, no contenido
    repair_actions: list[str]        # qué se hizo para reparar
    total_cost_usd: float
    total_duration_seconds: int
    user_feedback: str | None
    memory_candidates: list[MemoryCandidate]  # sugerencias para memoria de usuario/empresa
    playbook_candidate: PlaybookCandidate | None
    solution_derivable: bool         # puede contribuir al Oli solution bank
```

### 2. Mission Replay

Cada misión tiene una caja negra completa que permite:
- **Reproducir:** re-ejecutar la misión con los mismos inputs
- **Auditar:** ver cada step, cada tool call, cada decisión de modelo, cada costo
- **Comparar:** comparar dos runs de la misma clase de misión
- **Convertir:** promover la misión a playbook si el resultado fue bueno

```python
@dataclass
class MissionBlackBox:
    mission_id: str
    # Inputs exactos
    raw_intent: str
    context_snapshot: dict          # estado de memoria al inicio de la misión
    # Ejecución completa
    events: list[MissionEvent]      # every state transition
    task_logs: list[TaskExecutionLog]
    tool_calls: list[ToolCallRecord]
    model_calls: list[ModelCallRecord]
    approval_events: list[ApprovalEvent]
    # Outputs
    artifacts: list[ArtifactRef]
    validation_reports: list[ValidationReport]
    delivery_summary: str
    # Costos
    total_tokens: int
    total_cost_usd: float
    total_gpu_minutes: float
    # Replay
    replay_compatible: bool         # True si todos los inputs pueden ser reproducidos
    replay_blocked_reason: str | None
```

### 3. Cross-Agent Memory

Cuando un agente externo (Claude Code, Codex, Browser Use) ejecuta trabajo delegado por Oli:

```python
class CrossAgentMemoryCapture:
    """
    Oli captura evidencia de lo que hizo el agente externo
    y decide qué entra en la memoria persistente.
    """
    def capture_from_claude_code(self, result: ClaudeCodeResult) -> list[MemoryCandidate]:
        # Qué archivos creó/modificó → artefactos
        # Qué decisiones de arquitectura tomó → decision memory candidates
        # Qué falló y cómo lo reparó → lesson memory candidates
        ...

    def capture_from_codex(self, result: CodexResult) -> list[MemoryCandidate]:
        ...

    def capture_from_browser_use(self, result: BrowserUseResult) -> list[MemoryCandidate]:
        # Qué selectores funcionaron → playbook candidates para browser steps
        ...
```

**Regla:** Los agentes externos no escriben memoria directamente. Retornan resultados estructurados. Oli decide qué entra en memoria.

### 4. After Action Review (AAR)

Al finalizar cada misión, el `MemoryCuratorSuboperator` ejecuta un AAR:

```python
class AfterActionReview:
    questions = [
        "¿Se completó el objetivo?",
        "¿Qué validadores pasaron/fallaron?",
        "¿Qué feedback dio el usuario?",
        "¿Qué memoria nueva se generó?",
        "¿Qué playbook se puede mejorar o crear?",
        "¿Qué debería ser un regression test?",
        "¿El spend de GPU/API fue justificado?",
        "¿Qué debería automatizarse la próxima vez?",
        "¿Esta misión puede contribuir al Oli solution bank?",
    ]
```

Los resultados del AAR generan `memory_candidates` — sugerencias que el usuario puede aprobar, rechazar o ignorar. **El MemoryCuratorSuboperator nunca escribe memoria directamente.**

### 5. Oli Solution Bank (por misión)

Cuando `solution_derivable: true`, el sistema puede derivar un artefacto generalizado:

- Solo estructura: pasos, tipos de herramientas, métricas de éxito, failure modes como categorías
- Nunca texto libre derivado del contenido del usuario
- Nunca identificadores, nombres, URLs específicas del usuario
- El artefacto es un repo/snippet en el banco privado de Olis

El campo `solution_derivable` en `missions` (ADR-002, schema 09) es la señal. El mecanismo de contribución al banco llega en V4+.

---

## Playbook Versioning

Cada vez que una misión mejora un playbook:

```python
@dataclass
class PlaybookUpdate:
    playbook_id: str
    from_version: str
    to_version: str
    change_summary: str
    evidence_missions: list[str]    # mission IDs que justifican el cambio
    requires_user_approval: bool    # true si el cambio afecta permisos o validadores
```

---

## Moat implicado

La memoria operacional de Oli no es RAG genérico sobre documentos. Es:
- Procedencia: cada memoria tiene una fuente (misión, feedback, documento)
- Outcomes: cada memoria está ligada a resultados reales
- Correcciones: las correcciones del usuario tienen mayor peso que las inferencias
- Playbooks: la memoria se convierte en workflows ejecutables
- Evidencia replayable: cada decisión puede ser auditada y reproducida

Eso no se copia exportando un JSON. El switching cost es real.

---

## V0 build target

Implementar:
- `mission_events` table con log completo
- `MissionBlackBox` básico (eventos + artifacts + model calls)
- `AfterActionReview` stub que genera `memory_candidates`
- `solution_derivable` flag en missions (ya en schema 09)

V1-V2:
- `CrossAgentMemoryCapture` para Claude Code
- Replay UI básica (ver eventos de una misión)
- `PlaybookCandidate` generado automáticamente después de 3 misiones del mismo tipo

V3-V4:
- Replay ejecutable (re-run con mismos inputs)
- Comparación entre runs
- Oli Solution Bank pipeline
