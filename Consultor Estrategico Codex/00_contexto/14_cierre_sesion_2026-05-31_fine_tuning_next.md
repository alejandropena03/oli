# Cierre de sesion - 2026-05-31

## Estado de cierre

Esta sesion se cerro despues de ordenar la arquitectura estrategica de Oli alrededor de:

- Dedicated Oli Runtime.
- Oli Core privado.
- Oli Labs publico/sanitizado.
- Skill signal profesional para Alejandro.
- Pendientes estrategicos de fine-tuning, subagent engineering, AI-first transformation, state-of-the-art discovery y cloud/service broker.

## Correccion importante

Codex repitio el pendiente de posicionamiento profesional cuando Alejandro ya habia pedido avanzar. En la siguiente sesion no se debe volver a empezar por carrera.

La carrera/skill signal ya quedo documentada en:

- `tdd/domain/ai-engineering-skill-signal.md`
- `tdd/adrs/ADR-022-public-oli-labs.md`

## Artefactos creados o actualizados

1. `tdd/adrs/ADR-021-dedicated-oli-runtime.md`
   - Canoniza Dedicated Oli Runtime como arquitectura principal.
   - Aclara que el usuario habla con Oli, no con el modelo.
   - Define managed runtime, BYOC, local/on-prem/power-user y desktop bridge.

2. `tdd/domain/ai-engineering-skill-signal.md`
   - Define las skills que Oli debe demostrar para posicionar a Alejandro como AI engineer / LLM developer / agent engineer.
   - Propone labs publicos sin revelar Oli Core.

3. `tdd/adrs/ADR-022-public-oli-labs.md`
   - Define frontera entre Private Oli Core y Public Oli Labs.
   - Recomienda repos publicos sanitizados: evals, runtime, memory, tool security, post-training.

4. `Consultor Estrategico Codex/03_tracking_estrategico.md`
   - Actualizado con decisiones 45-55.
   - Incluye pendientes nuevos y decisiones cerradas.

## Pendientes vivos

Orden recomendado para continuar:

1. Fine-tuning serio.
2. Subagent engineering.
3. State-of-the-art discovery.
4. AI-first transformation advisor.
5. Cloud/service broker responsable.
6. Farming/onboarding responsable.
7. Postgres/PostgresSaver/evals/guardrails cuando se vuelva a ejecucion tecnica.

## Proximo inicio recomendado

Cuando Alejandro continue en otra sesion, el siguiente tema debe ser:

> Fine-tuning serio para Oli.

No volver a explicar el plan de carrera salvo que Alejandro lo pida.

Preguntas guia para la proxima sesion:

1. Para que tareas de Oli si tiene sentido fine-tuning?
2. Que tareas deben seguir siendo RAG/prompting/evals/model routing?
3. Que dataset se puede construir sin usar datos privados?
4. Que pipeline demostraria nivel serio: SFT, LoRA/QLoRA, DPO, evals antes/despues, model registry?
5. Como conectar fine-tuning con Oli Labs sin regalar el core?

## Recordatorio de estado tecnico

V0.3 tecnico existe, pero sigue congelado para nuevas features hasta resolver:

- Postgres real.
- PostgresSaver.
- checkpoint/resume durable.
- evals formales.
- tool guardrails.

No llamar V0 producto terminado.

