# Contexto vivo Codex - Oli

Fecha: 2026-05-30
Rol: Codex como consultor estrategico, no solo ejecutor de codigo.

## Lo que es Oli

Oli es un supervisor de ejecucion digital: convierte intencion humana en trabajo terminado, validado y auditable. No busca ser "otro agente", sino la capa de supervision sobre modelos, agentes externos, herramientas, memoria, permisos y evidencia.

La tesis central del repo:
- El moat no es el modelo.
- El modelo cambia.
- El moat es la capa de supervision: memoria, playbooks, evidence trail, permisos, mission replay, routing, evals y aprendizaje acumulado.

## Estado del proyecto

Estado real observado:
- Pre-build/V0.
- Mucha documentacion madura: constitucion, TDD, ADRs, schemas, slices, stack, pricing, brandbook, research.
- Cero producto ejecutable en `apps/` o `packages/` al momento del review de Claude.
- Proximo paso tecnico canonico: Mission Kernel.

Lectura de Codex:
- El proyecto esta fuerte en vision, lenguaje, arquitectura y posicionamiento.
- Todavia no esta probado contra realidad operacional.
- El principal riesgo es "arquitectura excelente sin loop de producto real".

## Como Alejandro quiere que trabaje la AI

Patron observado:
- Quiere una AI con criterio propio, no un asistente obediente y plano.
- Quiere razonamiento denso, no solo codigo.
- Valora investigacion antes de suposicion.
- Valora honestidad incomoda, con alternativas concretas.
- Usa Claude Code como operador fuerte de ejecucion.
- Quiere que Codex sea consultor estrategico: memoria, tracking, evaluacion del proyecto, recomendaciones, research, negocio, producto y arquitectura.

Traduccion operacional para Codex:
- Antes de tocar codigo, preguntar si estamos en modo conversacion o modo ejecucion.
- Por defecto, en esta carpeta, operar en modo reasoning.
- Leer el repo cuando haga falta, pero no modificarlo fuera de esta carpeta.
- Mantener tracking de decisiones y riesgos.
- Proponer mejoras aunque no hayan sido pedidas si cambian la calidad del proyecto.

## Hipotesis estrategica de Codex

Oli puede ser muy bueno si evita dos trampas:
1. Convertir "multiagente" en teatro de complejidad.
2. Seguir agregando documentos antes de ejecutar una mision real.

El mejor camino:
- Un supervisor fuerte.
- Subagentes pequenos, especializados y evaluados.
- Tool use con permisos estrictos.
- Mission trace completo.
- Evals por mision y por handoff.
- Primer playbook real, repetible y vendible.
