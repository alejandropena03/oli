# ADR-007 — Estrategia de clarificación de intención

**Estado:** accepted — v2 revisado tras feedback del founder
**Fecha:** 2026-05-26
**Deciders:** Alejandro Peña (founder)

---

## Contexto

Cuando el founder escribe una intención, Oli necesita entenderla completamente antes de ejecutar. La versión anterior establecía un límite arbitrario de "máximo 2 preguntas" — esto era incorrecto.

## Decisión revisada

**Oli pregunta todo lo que necesite para no cometer errores costosos. No hay límite fijo.**

El criterio no es cuántas preguntas hace — es si tiene suficiente información para ejecutar correctamente. Un límite arbitrario de 2 preguntas lleva a Oli a asumir cosas que no debería asumir, y los humanos son malos optimizando sus propios prompts.

**Lo que sí tiene límite es la calidad de cada pregunta:**
- Cada pregunta debe ser necesaria — no puede ser algo que Oli puede inferir del contexto o de la memoria
- Cada pregunta debe tener un propósito explícito: "necesito saber X porque sin eso no puedo determinar Y"
- Oli nunca pregunta lo mismo dos veces en la misma misión
- Oli agrupa preguntas relacionadas para minimizar las rondas de interacción

## Principio de inferencia vs. pregunta

```
ANTES de preguntar, Oli verifica:
  1. ¿Está en la memoria del usuario? → usar directamente
  2. ¿Está en la memoria de la empresa? → usar directamente
  3. ¿Se puede inferir con alta confianza del contexto? → usar con nota
  4. ¿Si lo asumo mal, el costo de corrección es bajo? → asumir y notificar
  5. ¿Si lo asumo mal, el resultado es inutilizable? → preguntar

SOLO llega a preguntar si pasa el filtro 5.
```

## Ejemplo correcto vs. incorrecto

```
❌ MAL — pregunta lo que puede inferir:
  Founder: "Oli, prepara el reporte"
  Oli: "¿Qué tipo de reporte?" (la memoria dice que siempre hace el semanal de ventas)

✅ BIEN — usa la memoria, solo pregunta lo nuevo:
  Founder: "Oli, prepara el reporte para el pitch de mañana"
  Oli: "Entiendo — el reporte de ventas en formato ejecutivo para inversores.
        Necesito saber: ¿qué período cubre (este mes, Q1, YTD)?
        ¿A quién va dirigido específicamente?"
  [2 preguntas porque son nuevas y el resultado sería incorrecto sin ellas]
```

## Implicaciones en el schema

El objeto `InterpretedIntent` incluye:
- `clarifications_made`: las preguntas que Oli hizo y las respuestas
- `assumptions_made`: qué asumió Oli y con qué confianza
- `confidence`: 0-1 — si < 0.7 con memoria suficiente, Oli pregunta más

## Consecuencias

- Oli puede hacer muchas preguntas en misiones complejas y nuevas — esto es correcto
- Oli hace pocas preguntas en misiones repetidas — la memoria hace el trabajo
- El founder nunca tiene que repetir la misma preferencia más de una vez
- Con el tiempo, Oli pregunta cada vez menos porque conoce mejor al founder
