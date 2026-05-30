# State Machine — Mission

**Estado:** ✅ V1
**Fecha:** 2026-05-26

---

## Estados válidos (18)

```
idle
listening
intake_received
interpreting_intent
retrieving_context
classifying_permissions
planning
awaiting_approval
executing
validating
repairing
delivering
generating_report
updating_memory
completed
blocked
failed
cancelled
archived
```

---

## Transiciones

```
idle → listening                        [trigger: system_ready]
listening → intake_received             [trigger: user_input_received]
intake_received → interpreting_intent   [trigger: auto]
interpreting_intent → retrieving_context     [trigger: intent_clarified]
interpreting_intent → failed                 [trigger: intent_unresolvable]
retrieving_context → classifying_permissions [trigger: context_ready]
classifying_permissions → planning           [trigger: permissions_set]
planning → awaiting_approval            [trigger: plan_ready AND permission_class ≥ 2]
planning → executing                    [trigger: plan_ready AND permission_class < 2]
planning → failed                       [trigger: plan_unresolvable]
awaiting_approval → executing           [trigger: plan_approved]
awaiting_approval → cancelled           [trigger: plan_rejected]
executing → validating                  [trigger: all_steps_completed]
executing → repairing                   [trigger: step_failed AND repair_allowed]
executing → blocked                     [trigger: step_failed AND NOT repair_allowed]
executing → failed                      [trigger: critical_error]
repairing → executing                   [trigger: repair_successful]
repairing → blocked                     [trigger: repair_failed]
validating → delivering                 [trigger: validation_passed]
validating → repairing                  [trigger: validation_failed AND repair_allowed]
validating → failed                     [trigger: validation_failed AND NOT repair_allowed]
delivering → generating_report          [trigger: delivery_confirmed]
generating_report → updating_memory     [trigger: report_generated]
updating_memory → completed             [trigger: memory_updated]
completed → archived                    [trigger: archive_requested]
blocked → executing                     [trigger: human_unblocked]
blocked → cancelled                     [trigger: user_cancelled]
failed → archived                       [trigger: archive_requested]
cancelled → archived                    [trigger: archive_requested]
```

---

## Reglas inamovibles

1. Solo el Mission Kernel puede cambiar el estado de una misión
2. Los suboperadores reportan resultados — no cambian estado
3. Toda transición emite un evento de dominio
4. Las transiciones a `blocked` y `failed` requieren un `reason` documentado
5. `archived` es irreversible

---

## Datos requeridos por estado

| Estado | Datos requeridos para entrar |
|---|---|
| intake_received | raw_input, timestamp, source |
| interpreting_intent | raw_input |
| retrieving_context | interpreted_intent, clarifications[] |
| planning | context, permissions |
| awaiting_approval | plan, permission_class, cost_estimate |
| executing | approved_plan, tool_assignments |
| validating | step_outputs[], success_criteria |
| delivering | validated_output, evidence[] |
| completed | report, memory_updates[], cost_actual |
| blocked | block_reason, last_successful_step |
| failed | failure_reason, error_context |
