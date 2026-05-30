# ADR-009 — Escritura automática de memoria

**Estado:** accepted
**Fecha:** 2026-05-26
**Deciders:** Alejandro Peña (founder) — decisión explícita

---

## Contexto

Cuando Oli termina una misión y quiere recordar algo (preferencias detectadas, hechos del usuario, contexto de empresa), ¿pregunta antes de guardar o guarda automáticamente?

## Decisión

**Oli guarda en memoria automáticamente. El founder puede editar o borrar después.**

La fricción de "¿puedo recordar esto?" destruye la promesa de memoria persistente. Si el founder tiene que aprobar cada cosa que Oli recuerda, Oli se convierte en un sistema de notas, no en un operador que aprende.

## Alternativas consideradas

| Opción | Pros | Contras |
|---|---|---|
| **A — Guardar automático ✓** | Memoria fluida, Oli mejora solo | El founder debe confiar en que Oli recordará bien |
| B — Pedir aprobación | Control total | Fricción constante, mata el loop de aprendizaje |
| C — Solo lo explícito | Máximo control | Oli nunca mejora solo, requiere microgestión |

## Consecuencias

- **El MemoryCuratorSuboperator** escribe a memoria directamente tras MissionCompleted
- El founder tiene un **Memory Panel** donde puede ver todo lo que Oli sabe, editar o borrar
- Las memorias tienen **metadata de origen**: qué misión las generó, qué confianza tiene Oli, si es inferida o explícita
- Las declaraciones explícitas del founder **siempre** sobreescriben inferencias automáticas
- Oli debe poder **explicar por qué recuerda algo** cuando se le pregunta
- Las memorias auto-escritas tienen un período de 24h donde aparecen en un "recently added" visible — el founder puede revisarlas sin buscarlas

## Jerarquía de confianza en memoria

```
1. Declaración explícita del founder (mayor confianza — nunca se sobreescribe automáticamente)
2. Corrección del founder sobre inferencia anterior
3. Inferencia de alta confianza (patrón repetido ≥ 3 veces)
4. Inferencia de baja confianza (observación única)
```

## Lo que Oli recuerda automáticamente (ejemplos)

- Formato preferido de output (detectado por misiones anteriores)
- Herramientas que el founder usa
- Contexto actualizado del producto (competidores, decisiones tomadas en misiones)
- Tiempo estimado de valor creado por tipo de misión
- Qué tipos de misión el founder cancela o modifica frecuentemente
