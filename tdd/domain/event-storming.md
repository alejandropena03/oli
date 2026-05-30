# Event Storming — Oli

**Estado:** ✅ V3 — Decisiones fundacionales del founder aplicadas
**Fecha:** 2026-05-26
**Metodología:** Event Storming (Alberto Brandolini)
**Scope:** Todos los flujos del sistema — feliz, alternativo, degradado, edge cases

---

## Leyenda

| Símbolo | Elemento | Descripción |
|---|---|---|
| 🟠 | Evento de dominio | Algo que ocurrió (pasado) |
| 🔵 | Comando | Acción que dispara un evento |
| 🟡 | Agregado | Entidad que mantiene estado y acepta comandos |
| 🟣 | Política | Regla automática: evento → comando (sin intervención humana) |
| 🟢 | Vista / Read Model | Proyección de estado para el usuario u otro módulo |
| 🔴 | Hotspot | Duda, conflicto o riesgo abierto pendiente de resolver |
| 👤 | Actor externo | Quién dispara el comando (founder, sistema, timer) |

---

## 1. FLUJO PRINCIPAL — Misión de punta a punta

### 1.1 Intake y comprensión

```
👤 Founder
  CMD: CreateMission(raw_input, source)
    ↓
🟠 MissionCreated
  — id generado
  — status: intake_received
  — timestamp: T+0
    ↓
🟢 VISTA: Mission apareció en lista del usuario (estado: recibida)
    ↓
🟣 POLÍTICA: MissionCreated → InterpretIntent (automático)
  CMD: InterpretIntent(mission_id, raw_input, user_context)
    ↓
  [LLM call: interpretar intención]
    ↓
  ¿Intención clara?
  ├── SÍ →
  │   🟠 IntentInterpreted
  │     — interpreted_goal
  │     — success_criteria[]
  │     — output_format
  │     — clarifications_needed: []
  │
  └── NO — intención ambigua →
      🟠 ClarificationNeeded
        — ambiguity_description
        — clarification_questions[]
        ↓
      🟢 VISTA: Oli pregunta al founder (máx 2 preguntas)
        ↓
      👤 Founder responde
      CMD: ProvideClarification(answers[])
        ↓
      🟠 ClarificationProvided
        ↓
      🟣 POLÍTICA: ClarificationProvided → InterpretIntent (reintento con contexto)
```

### 1.2 Contexto y permisos

```
🟠 IntentInterpreted
  ↓
🟣 POLÍTICA: IntentInterpreted → RetrieveContext (automático)
  CMD: RetrieveContext(mission_id, interpreted_intent)
    ↓
  [Memory Graph: user_memory + company_memory + mission_memory relevante]
    ↓
🟠 ContextRetrieved
  — user_preferences{}
  — company_context{}
  — relevant_past_missions[]
  — applicable_playbooks[]
    ↓
🟣 POLÍTICA: ContextRetrieved → ClassifyPermissions (automático)
  CMD: ClassifyPermissions(mission_id, plan_preview)
    ↓
🟠 PermissionsClassified
  — permission_class: 0|1|2|3|4
  — actions_requiring_approval[]
  — estimated_cost{}
```

### 1.3 Planificación

```
🟠 PermissionsClassified
  ↓
🟣 POLÍTICA: PermissionsClassified → CreatePlan (automático)
  CMD: CreatePlan(mission_id, intent, context, permissions)
    ↓
  [Orchestrator + LLM: genera plan detallado]
    ↓
🟠 PlanCreated
  — steps[]: [{id, type, suboperator, params, permission_class, reversible, estimated_duration}]
  — total_permission_class: max(steps.permission_class)
  — cost_estimate: {tokens, usd, human_time_saved_hr}
    ↓
  ¿permission_class ≥ 2?
  ├── SÍ →
  │   🟣 POLÍTICA: PlanCreated (class≥2) → RequestApproval
  │   CMD: RequestApproval(mission_id, plan_summary, cost_estimate, actions_preview)
  │     ↓
  │   🟠 ApprovalRequested
  │     ↓
  │   🟢 VISTA: Decision Queue — el founder ve qué hará Oli y cuánto costará
  │     ↓
  │   👤 Founder decide
  │   ├── Aprueba →
  │   │   CMD: ApprovePlan(mission_id, approved_by)
  │   │   🟠 PlanApproved
  │   │
  │   ├── Rechaza →
  │   │   CMD: RejectPlan(mission_id, rejection_reason)
  │   │   🟠 PlanRejected
  │   │   🟠 MissionCancelled
  │   │
  │   └── Modifica el plan →
  │       CMD: RequestPlanRevision(mission_id, revision_notes)
  │       🟠 PlanRevisionRequested
  │       🟣 POLÍTICA: PlanRevisionRequested → CreatePlan (replanificar con notas)
  │
  └── NO (class 0-1) →
      🟠 PlanAutoApproved
      [sigue a ejecución sin intervención]
```

### 1.4 Ejecución

```
🟠 PlanApproved | PlanAutoApproved
  ↓
🟣 POLÍTICA: Plan*Approved → ExecuteStep (primer step)
  CMD: ExecuteStep(mission_id, step_id)
    ↓
  [Tool Router → Suboperator correcto]
    ↓
  ¿Step exitoso?
  ├── SÍ →
  │   🟠 StepExecuted
  │     — step_id, output, duration_ms, cost
  │     ↓
  │   🟢 VISTA: Mission progress bar avanza
  │     ↓
  │   ¿Hay más steps?
  │   ├── SÍ → 🟣 POLÍTICA: StepExecuted → ExecuteStep (siguiente step)
  │   └── NO → 🟠 AllStepsCompleted → ir a validación
  │
  └── NO (step falla) →
      🟠 StepFailed
        — step_id, error_type, error_message, repair_attempts: 0
        ↓
      ¿error_type = permission_denied?
      ├── SÍ → [ver sección 5.3 — Permiso denegado en runtime]
      │
      ¿error_type ≠ permission_denied?
      └── SÍ →
          🟣 POLÍTICA: StepFailed → AttemptRepair (ADR-006: Oli intenta solo primero)

          [CICLO DE REPARACIÓN AUTÓNOMA — hasta 3 intentos antes de escalar]

          Intento 1: retry exacto
            ↓
          ¿exitoso? → StepRepaired → continúa
          ¿falla? →
          Intento 2: herramienta alternativa / enfoque alternativo
            ↓
          ¿exitoso? → StepRepaired → continúa
          ¿falla? →
          Intento 3: scope reducido (hace menos, entrega parcial)
            ↓
          ¿exitoso? →
          │   🟠 StepRepairedWithReducedScope
          │   🟢 VISTA: Oli informa qué pudo y qué no pudo hacer en ese step
          │   → continúa al siguiente step
          ¿falla? →

          [AGOTADOS 3 INTENTOS — ahora sí escala al founder]
          🟠 RepairExhausted
            — step_id, attempts[]: [{strategy, outcome}] × 3
            ↓
          CMD: BlockMission(mission_id, step_id, block_reason, repair_history)
          🟠 MissionBlocked
          🟢 VISTA: Founder ve exactamente qué intentó Oli, por qué falló cada vez, y qué necesita para continuar
              ↓
          👤 Founder decide
          ├── Da información o autoriza alternativa →
          │   CMD: UnblockMission(mission_id, resolution)
          │   🟠 MissionUnblocked
          │   🟣 POLÍTICA: MissionUnblocked → ExecuteStep (desde step fallido con resolución)
          │
          └── Cancela →
              CMD: CancelMission(mission_id)
              🟠 MissionCancelled
```

### 1.5 Validación

```
🟠 AllStepsCompleted
  ↓
🟣 POLÍTICA: AllStepsCompleted → ValidateOutput
  CMD: ValidateOutput(mission_id, all_outputs[], success_criteria[])
    ↓
  [ValidationSuboperator: verifica output contra success_criteria]
    ↓
  ¿Validación pasa?
  ├── SÍ →
  │   🟠 OutputValidated
  │     — validation_score, criteria_met[], evidence_refs[]
  │     ↓
  │   → ir a entrega
  │
  └── NO →
      🟠 ValidationFailed
        — failed_criteria[]
        — failure_reason
        ↓
      ¿auto_repair_allowed AND repair_possible?
      ├── SÍ →
      │   🟣 POLÍTICA: ValidationFailed (repairable) → RepairStep
      │   [Repara el output específico que falló]
      │   → regresa a ValidateOutput
      │   (max 2 repair cycles antes de escalar)
      │
      └── NO →
          🟠 ValidationEscalated
          🟢 VISTA: Founder ve qué criterio falló y por qué
          👤 Founder decide
          ├── Acepta output de todas formas →
          │   CMD: AcceptWithWarning(mission_id, acknowledgement)
          │   🟠 OutputAcceptedWithWarning
          │   → ir a entrega
          │
          └── Cancela →
              🟠 MissionFailed(reason: validation_rejected)
```

### 1.6 Entrega, reporte y memoria

```
🟠 OutputValidated | OutputAcceptedWithWarning
  ↓
CMD: DeliverMission(mission_id)
  ↓
🟠 MissionDelivered
  — output_artifact_refs[]
  — delivery_timestamp
🟢 VISTA: Evidence Drawer — founder ve el output + evidencia completa
  ↓
🟣 POLÍTICA: MissionDelivered → GenerateReport (siempre)
CMD: GenerateReport(mission_id)
  ↓
🟠 ReportGenerated
  — duration_total_ms
  — cost_actual {tokens, usd}
  — human_time_saved_hr (estimado)
  — steps_completed / steps_total
  — validation_result
  — repair_cycles
  — playbook_candidate: bool
🟢 VISTA: Mission Report — resumen ejecutivo para el founder
  ↓
🟣 POLÍTICA: ReportGenerated → WriteMemory (ADR-009: automático, sin aprobación)
CMD: WriteMemoryUpdates(mission_id, updates[])
  ↓
🟠 MemoryAutoWritten
  — updates[]: [{layer, key, value, confidence, source_mission_id}]
  — visibles en "Recently Added" por 24h (founder puede editar/borrar, no necesita aprobar)
  ↓
🟣 POLÍTICA: ReportGenerated → EvaluatePlaybookCandidate
CMD: EvaluatePlaybookCandidate(mission_id)
  ↓
¿Es candidato?
├── SÍ →
│   🟠 PlaybookCandidateIdentified
│   CMD: ProposePlaybook(template_draft)
│   🟠 PlaybookProposed
│   🟢 VISTA: Founder ve propuesta de playbook — aprobar / rechazar / editar
│   👤 Founder aprueba →
│   CMD: ApprovePlaybook(playbook_id)
│   🟠 PlaybookApproved
│
└── NO → 🟠 NoPlaybookNeeded
  ↓
🟠 MissionCompleted
🟢 VISTA: Mission marcada como ✓ completada en lista
```

---

## 2. FLUJO ALTERNATIVO — Misión desde Playbook

```
👤 Founder
  CMD: CreateMissionFromPlaybook(playbook_id, overrides{})
    ↓
🟠 MissionCreatedFromPlaybook
  — plan pre-construido desde playbook
  — variables aplicadas (overrides)
    ↓
🟣 POLÍTICA: MissionCreatedFromPlaybook → ClassifyPermissions
  [se salta InterpretIntent y CreatePlan — ya está en el playbook]
    ↓
  [continúa flujo principal desde 1.3 PermissionsClassified]
```

---

## 3. FLUJO ALTERNATIVO — Misión interrumpida y reanudada

```
[Misión en estado: executing | validating | awaiting_approval]
  ↓
👤 Founder cierra la app / sesión termina
  ↓
🟣 POLÍTICA: SessionEnded (misión activa) → CheckpointMission
CMD: CheckpointMission(mission_id)
  ↓
🟠 MissionCheckpointed
  — current_step_id
  — completed_steps[]
  — partial_outputs{}
  — estado guardado en storage
    ↓
[Founder abre la app después]
  ↓
🟣 POLÍTICA: SessionStarted (missions_in_progress exists) → NotifyPendingMissions
  ↓
🟢 VISTA: Founder ve misiones en progreso con su estado
  ↓
👤 Founder decide reanudar
CMD: ResumeMission(mission_id)
  ↓
🟠 MissionResumed
  [carga checkpoint, retoma desde current_step_id]
  ↓
  [continúa flujo principal desde el punto de interrupción]
```

---

## 4. FLUJO — Misiones en paralelo
*(ADR-008: múltiples misiones activas, límite conservador = capacidad del modelo local)*

```
🟠 MissionCreated (misión A)
  ↓
[Mientras A está en executing...]
  ↓
👤 Founder crea misión B
CMD: CreateMission(raw_input_B)
  ↓
¿active_missions < max_concurrent?   (max_concurrent = min(3, model_capacity))
├── SÍ →
│   🟠 MissionCreated (misión B)
│   [A y B corren en paralelo — ciclos independientes]
│   🟢 VISTA: Founder ve ambas misiones con su estado real
│
└── NO — límite alcanzado →
    🟠 MissionQueued (misión B)
    🟢 VISTA: "Oli ya tiene 3 misiones activas — B empieza cuando haya capacidad"
    🟣 POLÍTICA: MissionCompleted (A) → ActivateNextQueued → B pasa a intake_received

[Conflicto de recursos — dos misiones necesitan escribir a la misma clave de memoria]
🟠 MemoryWriteConflictDetected
🟣 POLÍTICA: MemoryWriteConflictDetected → QueueMemoryWrite (FIFO)
  [La segunda escritura espera — no se pierde]
```

---

## 5. FLUJOS DE DEGRADACIÓN — Fallas del sistema

### 5.1 Modelo de IA falla o timeout

```
[Durante InterpretIntent | CreatePlan | ValidateOutput]
  ↓
🟠 ModelCallFailed
  — provider, model, error_type: timeout|rate_limit|api_error
  — retry_count
    ↓
¿retry_count < model_max_retries?
├── SÍ →
│   🟣 POLÍTICA: ModelCallFailed (retryable) → RetryModelCall
│   [espera exponential backoff]
│   → reintenta la misma operación
│
└── NO →
    ¿hay modelo fallback configurado?
    ├── SÍ →
    │   🟠 ModelFallbackActivated
    │   [usa modelo alternativo — puede ser menos capaz]
    │   🟢 VISTA: Oli informa al founder que usó modelo fallback
    │
    └── NO →
        🟠 ModelCallExhausted
        🟠 MissionBlocked(reason: model_unavailable)
        🟢 VISTA: Founder ve bloqueo con instrucciones de qué hacer
```

### 5.2 Herramienta externa falla

```
[Durante ExecuteStep — tool_type: api_call | browser | filesystem]
  ↓
🟠 ToolCallFailed
  — tool_type, error: network|auth|rate_limit|not_found
    ↓
¿tool_type = filesystem AND error = not_found?
└── 🟠 StepFailed(error_type: resource_missing)
    → flujo de repair con alternativa

¿tool_type = api_call AND error = rate_limit?
└── 🟣 POLÍTICA: → RetryWithBackoff
    🟠 ToolRetried | ToolRetryExhausted

¿tool_type = api_call AND error = auth?
└── 🟠 CredentialError
    🟢 VISTA: Founder ve que necesita re-autorizar herramienta X
    👤 Founder re-autoriza
    CMD: RetryAfterReauth(step_id)
    → regresa a ExecuteStep
```

### 5.3 Permiso denegado en runtime

```
[Durante ExecuteStep — acción requiere permiso que no fue anticipado]
  ↓
🟠 PermissionDeniedAtRuntime
  — action_attempted
  — permission_required
  — permission_current
    ↓
🟣 POLÍTICA: PermissionDeniedAtRuntime → EscalatePermission
CMD: EscalatePermission(mission_id, step_id, permission_needed, reason)
  ↓
🟠 PermissionEscalationRequested
🟢 VISTA: Oli explica qué quiere hacer y por qué necesita más permiso
  ↓
👤 Founder
├── Otorga permiso →
│   CMD: GrantEscalatedPermission(permission_class)
│   🟠 PermissionGranted
│   → regresa a ExecuteStep con permiso actualizado
│
└── Deniega →
    CMD: DenyEscalatedPermission
    🟠 PermissionDenied
    🟣 POLÍTICA: PermissionDenied → AttemptAlternativeStep
    ¿hay step alternativo sin ese permiso?
    ├── SÍ → ejecuta alternativa
    └── NO → MissionBlocked
```

---

## 6. EVENTOS DEL SISTEMA DE MEMORIA
*(ADR-009: escritura automática — el founder edita después, no aprueba antes)*

```
🟣 POLÍTICA: MissionCompleted → MemoryCuratorSuboperator evalúa qué guardar
  ↓
CMD: WriteMemoryUpdates(updates[])
  ↓
🟠 MemoryAutoWritten
  — updates[]: [{layer, key, value, confidence, source_mission_id}]
  — visibles en "Recently Added" por 24h para revisión opcional del founder
  [Oli decide y guarda — sin fricción, sin aprobación previa]

---

[Declaración explícita del founder — prioridad máxima, nunca sobreescrita por inferencia]
👤 Founder
CMD: RecordExplicitMemory(layer, key, value)
  ↓
🟠 ExplicitMemoryRecorded
  — sobreescribe cualquier inferencia anterior sobre la misma clave

---

[Founder edita una memoria (desde Memory Panel)]
👤 Founder
CMD: EditMemoryEntry(entry_id, new_value, reason)
  ↓
🟠 MemoryEntryEdited
  — previous_value guardado en historial auditable

---

[Founder borra una memoria]
👤 Founder
CMD: DeleteMemoryEntry(entry_id)
  ↓
🟠 MemoryEntryDeleted
  [soft delete — permanece en audit log]

---

[Founder pregunta por qué Oli recuerda algo]
👤 Founder
CMD: ExplainMemory(entry_id)
  ↓
🟠 MemoryExplained
🟢 VISTA: Oli muestra — source_mission_id, patrón observado, confianza, timestamp
```

---

## 7. EVENTOS DEL SISTEMA DE PLAYBOOKS

```
🟠 PlaybookApproved
  — playbook_id, template, variables[], steps[]
  ↓
🟠 PlaybookAvailable
🟢 VISTA: Playbook aparece en biblioteca del founder

[Founder ejecuta playbook]
CMD: CreateMissionFromPlaybook(playbook_id, variable_overrides{})
  ↓
🟠 PlaybookExecuted
  — execution_id, variables_used, mission_id

[Playbook falla en ejecución]
🟠 PlaybookExecutionFailed
  — step_id, failure_reason
  ↓
🟣 POLÍTICA: PlaybookExecutionFailed → FlagPlaybookForReview
🟠 PlaybookFlaggedForReview
🟢 VISTA: Oli sugiere actualizar el playbook

👤 Founder actualiza playbook
CMD: UpdatePlaybook(playbook_id, changes, version++)
🟠 PlaybookUpdated(version: N+1)

👤 Founder depreca playbook
CMD: DeprecatePlaybook(playbook_id, reason)
🟠 PlaybookDeprecated
```

---

## 8. EVENTOS DE PERFIL Y ONBOARDING

```
[Primera vez que el founder abre Oli]
CMD: InitializeUserProfile(name, role, company_context{})
  ↓
🟠 UserProfileCreated
  ↓
CMD: InitializeCompanyContext(product_thesis, icp, stack, team_size)
  ↓
🟠 CompanyContextInitialized
  ↓
🟠 OliReadyForMissions
🟢 VISTA: Oli listo — muestra primera misión sugerida basada en contexto
```

---

## 9. AGREGADOS — DEFINICIÓN COMPLETA

### Mission
**Responsabilidad:** Ciclo de vida completo de una unidad de trabajo

**Estado interno:**
```
id:                   uuid
status:               MissionStatus (18 estados)
source:               'chat' | 'playbook' | 'api' | 'scheduled'
raw_input:            string
interpreted_intent:   InterpretedIntent | null
context:              MissionContext | null
plan:                 MissionStep[] | null
current_step_index:   number
permission_class:     0|1|2|3|4
approvals:            ApprovalRecord[]
step_results:         StepResult[]
validation_result:    ValidationResult | null
output:               MissionOutput | null
evidence:             EvidenceRef[]
report:               MissionReport | null
cost:                 CostRecord
repair_cycles:        number
checkpoint:           Checkpoint | null
created_at:           timestamp
completed_at:         timestamp | null
playbook_id:          uuid | null  (si vino de playbook)
```

**Invariantes:**
- Solo el Mission Kernel puede cambiar `status`
- `permission_class` nunca baja durante ejecución (solo puede escalar)
- `repair_cycles` tiene un máximo configurable (default: 3)
- Toda transición de estado genera exactamente un evento de dominio

---

### User
**Responsabilidad:** Identidad, preferencias y memoria personal del founder

**Estado interno:**
```
id:                   uuid
name:                 string
role:                 string
preferences:          UserPreferences
memory_entries:       MemoryEntry[]
correction_log:       CorrectionRecord[]
auto_approve_memory:  boolean
permission_threshold: 0|1|2|3|4  (auto-aprueba hasta esta clase)
created_at:           timestamp
```

---

### Company
**Responsabilidad:** Contexto organizacional persistente

**Estado interno:**
```
id:                   uuid
product_thesis:       string
icp:                  ICPDefinition
positioning:          string
roadmap:              RoadmapEntry[]
stack:                TechStack
competitors:          CompetitorEntry[]
decisions:            DecisionRecord[]
facts:                CompanyFact[]
updated_at:           timestamp
```

---

### Playbook
**Responsabilidad:** Template reutilizable de misión

**Estado interno:**
```
id:                   uuid
name:                 string
trigger_pattern:      string  (natural language pattern)
version:              number
status:               'proposed' | 'approved' | 'deprecated'
steps:                PlaybookStep[]
variables:            PlaybookVariable[]
origin_mission_id:    uuid
execution_count:      number
success_rate:         number
avg_cost_usd:         number
avg_duration_ms:      number
created_at:           timestamp
updated_at:           timestamp
```

---

## 10. POLÍTICAS — TABLA COMPLETA

| # | Evento disparador | Condición | Comando automático | Actor |
|---|---|---|---|---|
| P01 | MissionCreated | siempre | InterpretIntent | Sistema |
| P02 | IntentInterpreted | siempre | RetrieveContext | Sistema |
| P03 | ClarificationProvided | siempre | InterpretIntent | Sistema |
| P04 | ContextRetrieved | siempre | ClassifyPermissions | Sistema |
| P05 | PermissionsClassified | siempre | CreatePlan | Sistema |
| P06 | PlanCreated | permission_class ≥ 2 | RequestApproval | Sistema |
| P07 | PlanCreated | permission_class < 2 | AutoApprovePlan | Sistema |
| P08 | PlanApproved \| PlanAutoApproved | siempre | ExecuteStep(first) | Sistema |
| P09 | StepExecuted | more_steps_remain | ExecuteStep(next) | Sistema |
| P10 | StepExecuted | no_more_steps | AllStepsCompleted | Sistema |
| P11 | AllStepsCompleted | siempre | ValidateOutput | Sistema |
| P12 | StepFailed | error ≠ permission_denied, attempt < 3 | AttemptRepair (autónomo) | Sistema |
| P13 | StepFailed | attempt ≥ 3 (reparaciones agotadas) | BlockMission | Sistema |
| P14 | StepFailed | error = permission_denied | EscalatePermission | Sistema |
| P15 | ValidationFailed | repairable AND repair_cycles < max | RepairStep | Sistema |
| P16 | ValidationFailed | NOT repairable OR cycles ≥ max | ValidationEscalated | Sistema |
| P17 | OutputValidated \| OutputAcceptedWithWarning | siempre | DeliverMission | Sistema |
| P18 | MissionDelivered | siempre | GenerateReport | Sistema |
| P19 | ReportGenerated | siempre | WriteMemoryUpdates (automático) | Sistema |
| P20 | ReportGenerated | siempre | EvaluatePlaybookCandidate | Sistema |
| P21 | PlaybookCandidateIdentified | siempre | ProposePlaybook | Sistema |
| P22 | ModelCallFailed | retry < model_max | RetryModelCall | Sistema |
| P23 | ModelCallFailed | retry ≥ model_max AND fallback_exists | ActivateModelFallback | Sistema |
| P24 | ModelCallFailed | retry ≥ model_max AND no_fallback | BlockMission | Sistema |
| P25 | SessionEnded | active_missions_exist | CheckpointMission | Sistema |
| P26 | PlaybookExecutionFailed | siempre | FlagPlaybookForReview | Sistema |
| P27 | PlanRevisionRequested | siempre | CreatePlan (con notas) | Sistema |
| P28 | MissionUnblocked | siempre | ExecuteStep (desde bloqueado) | Sistema |

---

## 11. VISTAS (READ MODELS) — TABLA COMPLETA

| Vista | Quién la ve | Qué muestra | Cuándo se actualiza |
|---|---|---|---|
| Mission List | Founder | Todas las misiones con estado, progreso | Cada evento de misión |
| Mission Progress | Founder | Steps completados, step actual, % | StepExecuted, StepFailed |
| Decision Queue | Founder | Misiones esperando aprobación | ApprovalRequested |
| Evidence Drawer | Founder | Output + sources + audit trail | MissionDelivered |
| Mission Report | Founder | Resumen ejecutivo post-misión | ReportGenerated |
| Memory Panel | Founder | Qué sabe Oli del usuario y empresa | MemoryUpdated |
| Memory Review | Founder | Sugerencias de memoria pendientes | MemoryUpdatesSuggested |
| Playbook Library | Founder | Playbooks disponibles | PlaybookApproved, PlaybookUpdated |
| Playbook Proposal | Founder | Propuesta de nuevo playbook | PlaybookProposed |
| Block Screen | Founder | Qué bloqueó la misión + cómo resolverlo | MissionBlocked |
| Permission Request | Founder | Qué quiere hacer Oli + por qué | ApprovalRequested, PermissionEscalationRequested |
| Cost Dashboard | Founder | Costo total de sesión y por misión | Cada MissionCompleted |

---

## 12. HOTSPOTS ABIERTOS 🔴

| # | Hotspot | Impacto | Estado |
|---|---|---|---|
| H01 | ¿Límite de misiones paralelas? | Alto | ✅ RESUELTO — ADR-008: min(3, model_capacity), cola FIFO |
| H02 | ¿Conflicto de escritura en memoria simultánea? | Alto | ✅ RESUELTO — ADR-008: QueueMemoryWrite FIFO |
| H03 | ¿Cómo se detecta candidato a playbook? | Medio | 🔴 ABIERTO — propuesta: frecuencia ≥ 3 + similitud semántica |
| H04 | ¿Cómo se implementa CheckpointMission en V0? | Alto | 🔴 ABIERTO — propuesta: JSON serializado por misión en disco |
| H05 | ¿Qué modelo para ClarificationNeeded vs. InterpretIntent? | Bajo V0 | 🟡 PROPUESTO — Haiku para detección, Sonnet para interpretación |
| H06 | ¿Cuántos repair_cycles antes de escalar? | Medio | ✅ RESUELTO — ADR-006: 3 intentos con estrategias distintas |
| H07 | ¿Cómo se calcula human_time_saved_hr? | Bajo V0 | 🟡 PROPUESTO — lookup por tipo de misión, editable por founder |
| H08 | ¿MemoryCuratorSuboperator dentro del ciclo o asíncrono? | Medio | 🟡 PROPUESTO — asíncrono post-completion para no bloquear entrega |
| H09 | ¿Cómo se versiona el plan cuando el founder pide revisión? | Medio | 🔴 ABIERTO — propuesta: plan_version++ con historial |
| H10 | ¿Qué pasa si el modelo cae durante misión activa? | Alto | 🔴 ABIERTO — propuesta: checkpoint auto + notificación |
| H11 | ¿Cuántas preguntas de clarificación máximo por ronda? | Medio | ✅ RESUELTO — ADR-007: máximo 2 preguntas por ronda |
| H12 | ¿Qué pasa si tras 2 rondas de clarificación el intent sigue ambiguo? | Bajo V0 | 🔴 ABIERTO — propuesta: escalar a founder para decidir cómo proceder |

---

## 13. RESUMEN DE EVENTOS — CATÁLOGO COMPLETO

### Mission events (31)
```
MissionCreated, MissionCreatedFromPlaybook
ClarificationNeeded, ClarificationProvided
IntentInterpreted
ContextRetrieved
PermissionsClassified
PlanCreated, PlanRevisionRequested
ApprovalRequested, PlanApproved, PlanAutoApproved, PlanRejected
StepExecuted, StepFailed, StepRepaired, RepairFailed
AllStepsCompleted
PermissionEscalationRequested, PermissionGranted, PermissionDenied, PermissionEscalationRequired
ToolCallFailed, ToolRetried, ToolRetryExhausted, CredentialError
ModelCallFailed, ModelFallbackActivated, ModelCallExhausted
MissionBlocked, MissionUnblocked
OutputValidated, ValidationFailed, ValidationEscalated, OutputAcceptedWithWarning
MissionDelivered
ReportGenerated
MemoryUpdatesSuggested, MemoryUpdated
PlaybookCandidateIdentified, NoPlaybookNeeded
MissionCompleted, MissionFailed, MissionCancelled
MissionCheckpointed, MissionResumed
```

### Memory events (6)
```
ExplicitMemoryRecorded, InferredMemorySuggested
MemoryEntryEdited, MemoryEntryDeleted
UserProfileCreated, CompanyContextInitialized
```

### Playbook events (6)
```
PlaybookProposed, PlaybookApproved, PlaybookExecuted
PlaybookUpdated, PlaybookDeprecated, PlaybookFlaggedForReview
```

### System events (3)
```
OliReadyForMissions
SessionEnded
PermissionDeniedAtRuntime
```

**Total: 46 eventos de dominio**
