# Sesión 02 — 2026-05-26

## Contexto
El founder revisó los contenidos visuales de sesión 1. Primera sesión post-brand enfocada en preparar el terreno técnico. Luego se ejecutó el Event Storming completo con decisiones fundacionales del founder.

## Qué se hizo

### Parte 1 — Estructura TDD
- Inventario completo del estado del proyecto
- Validación de la lectura del founder sobre las 2 capacidades core de Oli
- Decisiones: Mission Kernel primero, Linux server sandbox después, pre-dev antes de código
- Creación de estructura completa `tdd/`, `bitacora/`, `playbooks/`
- ADRs 001-005: modelo, sandbox, memoria, permisos, runtime
- Event Storming V1, State Machine V1, Slice-001 en papel

### Parte 2 — Event Storming con founder

**4 decisiones fundacionales del producto:**

| # | Pregunta | Decisión | ADR |
|---|---|---|---|
| 1 | Bloqueo de misión | Oli intenta 3 alternativas solo antes de escalar al founder | ADR-006 |
| 2 | Clarificación de intención | Preguntar SIEMPRE antes de ejecutar — de entender bien depende todo | ADR-007 |
| 3 | Misiones en paralelo | Múltiples activas, límite conservador = capacidad del modelo local | ADR-008 |
| 4 | Escritura de memoria | Automática — founder edita después, no aprueba antes | ADR-009 |

### Artefactos creados
| Artefacto | Archivo | Estado |
|---|---|---|
| Estructura TDD completa | `tdd/` | ✅ |
| Event Storming V3 (con decisiones founder) | `tdd/domain/event-storming.md` | ✅ |
| State Machine V1 | `tdd/domain/state-machine.md` | ✅ |
| ADR-001 Model Strategy | `tdd/adrs/ADR-001-model-strategy.md` | ✅ |
| ADR-002 Execution Sandbox | `tdd/adrs/ADR-002-execution-sandbox.md` | ✅ |
| ADR-003 Memory Storage | `tdd/adrs/ADR-003-memory-storage.md` | ✅ |
| ADR-004 Permission Model | `tdd/adrs/ADR-004-permission-model.md` | ✅ |
| ADR-005 Runtime | `tdd/adrs/ADR-005-runtime.md` | ✅ |
| ADR-006 Mission Blocking | `tdd/adrs/ADR-006-mission-blocking-strategy.md` | ✅ |
| ADR-007 Intent Clarification | `tdd/adrs/ADR-007-intent-clarification.md` | ✅ |
| ADR-008 Parallel Missions | `tdd/adrs/ADR-008-parallel-missions.md` | ✅ |
| ADR-009 Memory Auto-Write | `tdd/adrs/ADR-009-memory-auto-write.md` | ✅ |
| Vertical Slice 001 | `tdd/slices/slice-001-research-brief.md` | ✅ |
| Stack Decision V0 | `tdd/stack/stack-decision.md` | ✅ |
| Skill /oli actualizada | `~/.claude/skills/oli/SKILL.md` | ✅ |

## Estado al final de sesión 02
| Área | Estado |
|---|---|
| Marca | ✅ Completa |
| Skill /oli | ✅ Actualizada con protocolo TDD |
| Event Storming | ✅ V3 — completo con decisiones founder |
| State Machine | ✅ V1 (18 estados) |
| ADRs | ✅ 9 ADRs (001-009) |
| Slice-001 en papel | ✅ Research Brief |
| Stack Decision | ✅ V0 definido |
| Hotspots resueltos | ✅ H01, H02, H06, H11 — 4 de 12 |
| Schemas TypeScript | 🔲 Próximo paso |
| Mission Kernel V0 | 🔲 Pendiente |

## Próximo paso
Schemas TypeScript en `tdd/schemas/` → resolver hotspots abiertos (H03, H04, H09, H10, H12) → iniciar build V0
