# ADR-006 — Estrategia de troubleshooting y recuperación de misión

**Estado:** accepted — v2 revisado tras feedback del founder
**Fecha:** 2026-05-26
**Deciders:** Alejandro Peña (founder)

---

## Contexto

La versión anterior decía "Oli intenta 3 veces antes de escalar". Esto era incorrecto — es una simplificación que no refleja cómo debe razonar un operador real ante un problema.

## Decisión revisada

**Cuando algo falla, Oli ejecuta un ciclo de troubleshooting real — no reintentos ciegos.**

El ciclo es:
1. **Diagnosticar** — ¿qué falló exactamente? ¿cuál es la causa raíz?
2. **Clasificar el error** — ¿es transitorio? ¿de permisos? ¿de datos? ¿de herramienta?
3. **Buscar solución** — según la clasificación, aplicar la estrategia correcta
4. **Ejecutar la solución**
5. **Verificar** — ¿se resolvió? Si no, repetir el ciclo con nueva información
6. **Escalar** cuando el ciclo no converge en solución

## Árbol de troubleshooting por tipo de error

```
ERROR DETECTADO
│
├── Transitorio (timeout, rate limit, flakiness)
│   └── Estrategia: retry con backoff exponencial
│       → 1s → 4s → 16s → si persiste: clasificar como no transitorio
│
├── Autenticación / permisos
│   └── Estrategia: verificar token, intentar refresh
│       → Si token expiró: renovar automáticamente (ADR-014)
│       → Si scope insuficiente: escalar con propuesta de solución
│
├── Recurso no encontrado (archivo, URL, entidad)
│   └── Estrategia: buscar alternativas
│       → ¿existe una ruta alternativa al mismo recurso?
│       → ¿se puede reconstruir el recurso desde otra fuente?
│       → ¿el scope reducido resuelve el problema?
│
├── Error de lógica / datos incorrectos
│   └── Estrategia: diagnóstico profundo
│       → Analizar qué datos causaron el error
│       → Verificar si el plan inicial asumió algo incorrecto
│       → Replantear el step con datos corregidos
│
├── Herramienta no disponible (MCP server caído, API down)
│   └── Estrategia: herramienta alternativa
│       → ¿existe otro MCP server que haga lo mismo?
│       → ¿se puede hacer via API directa en lugar de MCP?
│       → ¿via linux_shell se puede lograr el mismo resultado?
│
└── Error crítico sin solución conocida
    └── Escalar al founder con diagnóstico completo
```

## Lo que Oli presenta al founder cuando escala

Oli nunca escala sin contexto. Cuando escala, presenta:

```
Diagnóstico:
  Error: [descripción técnica del error]
  Causa identificada: [por qué ocurrió]

Lo que intenté:
  Intento 1: [estrategia] → [resultado]
  Intento 2: [estrategia] → [resultado]
  Intento N: [estrategia] → [resultado]

Por qué no pude resolverlo solo:
  [explicación honesta del límite encontrado]

Lo que necesito de ti para continuar:
  Opción A: [acción específica del founder] → resultado esperado
  Opción B: [alternativa] → resultado esperado
  Opción C: Cancelar este step y continuar sin él
```

## Sin límite fijo de intentos

No hay un número máximo de intentos establecido. El ciclo continúa mientras:
- Oli tenga nuevas estrategias que aplicar
- Cada intento produzca nueva información para la siguiente iteración
- El costo de continuar sea menor al costo de escalar

Escala cuando:
- El ciclo converge en el mismo error sin nueva información
- La solución requiere acceso o información que solo el founder tiene
- El costo de continuar supera el beneficio estimado

## Consecuencias

- Oli puede tardar más en escalar — esto es intencional y correcto
- El founder nunca recibe un bloqueo sin diagnóstico completo
- Con el tiempo, los patrones de error se guardan en Mission Memory y Oli aprende a resolverlos más rápido
