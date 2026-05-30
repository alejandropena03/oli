# Sesión 05 — 2026-05-26

## Contexto
Cierre del TDD + diseño del workflow de investigación state of the art + prueba real de la skill.

## Artefactos completados

| Artefacto | Descripción |
|---|---|
| `tdd/slices/slice-002-sales-automation-system.md` | Misión compleja end-to-end. Reveló 2 gaps reales: persistencia de artefactos (MinIO entra antes) + sandbox mode para tests |
| `tdd/adrs/ADR-018-multi-user-team.md` | Soporte de equipos desde V1: 4 roles, memoria personal vs. empresa, misiones asignables, playbooks de equipo |
| `tdd/domain/setup-wizard-spec.md` | 5 pasos de instalación, 4 perfiles de hardware, GPU cloud transparente |
| `tdd/domain/oli-constitution.md` | La Constitución — 14 pilares en 3 niveles (Carácter / Operación / Producto) |
| `tdd/domain/system-prompts.md` | Prompt raíz + 5 suboperadores + microcopy |
| `tdd/domain/research-workflow.md` | Workflow completo de state of the art con MCPs + prueba real |

## Correcciones aplicadas

**Pilar "Ejecución sobre conversación":**
No significa actuar sin pensar. Significa que el resultado es trabajo terminado. El razonamiento profundo es obligatorio — la velocidad viene de que el razonamiento es eficiente, no de saltárselo.

**Pilares de Oli restructurados:**
De lista desordenada de 11 a Constitución formal de 14 pilares en 3 niveles (modelo Anthropic).

**Voz de Oli:**
"Sin ego, sin personalidad forzada" era incorrecto. Oli tiene carácter: directo, filoso, con humor seco contra la fricción. "Una terminal que se compró un traje bueno."

## Investigación real ejecutada: Ollama vs vLLM

Primera ejecución del workflow de state of the art sobre una decisión real del TDD.

**Hallazgos que cambiaron el TDD:**
- Brecha real: 19x throughput (vLLM vs Ollama en pico). Para equipo, Ollama se queda corto antes de V3
- SGLang: alternativa a vLLM no mencionada — comparable en throughput, más simple
- LocalAI: capa de abstracción que permite cambiar backend sin tocar código de Oli
- vLLM es Linux-only: el founder que desarrolla en Mac necesita Ollama siempre

**ADR actualizado:** ADR-005 — Ollama (dev/Mac) → LocalAI abstraction → vLLM o SGLang (producción V2+)

## Estado del TDD — COMPLETO

| Área | Estado |
|---|---|
| 18 ADRs | ✅ Todos coherentes con Python + LangGraph |
| Constitución de Oli (14 pilares) | ✅ v1.0 |
| System prompts | ✅ Raíz + 5 suboperadores |
| 2 slices en papel | ✅ Simple (research) + Complejo (sistema de ventas) |
| Multi-user desde V1 | ✅ ADR-018 |
| Setup wizard | ✅ 4 perfiles de hardware |
| Research workflow | ✅ Con MCPs + primera prueba real |

## Próximo paso
Investigación de mercado: competencia con precios reales, ICP validado, 3 tiers de pricing.
