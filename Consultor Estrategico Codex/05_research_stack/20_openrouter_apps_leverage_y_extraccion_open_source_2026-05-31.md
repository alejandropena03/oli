# OpenRouter Apps leverage y extraccion open source para Oli

Fecha: 2026-05-31
Rol: Codex como consultor estrategico/auditor

## Veredicto

Alejandro tiene razon: OpenRouter Apps no debe usarse solo para mirar modelos. Es una fuente de demanda real sobre que agentes, IDE agents, runtimes y workflows estan procesando mas volumen en produccion.

La oportunidad para Oli no es copiar esas apps. La oportunidad es:

```text
OpenRouter Apps ranking
  -> identificar agentes con traccion real
  -> revisar codigo/documentacion/licencia
  -> extraer patrones reutilizables
  -> comparar contra la tesis de Oli
  -> adaptar solo lo que mejora Mission Kernel, runtime, seguridad, playbooks o UX
  -> validar con evals propias
```

Esto debe convertirse en una practica recurrente de leverage, no en una sesion puntual de curiosidad.

## Fuente local agregada

Se agrego en la raiz del repo:

```text
openrouter_docs.txt
```

Fuente:

```text
https://openrouter.ai/docs/llms.txt
```

Nota: el primer intento contra `https://openrouter.ai/llms.txt` devolvio HTML de error. La ruta correcta fue `https://openrouter.ai/docs/llms.txt`.

El archivo no lista las apps populares directamente; lista la documentacion tecnica de OpenRouter. Para apps y agentes, la fuente viva es:

```text
https://openrouter.ai/apps
```

## Por que OpenRouter Apps importa

OpenRouter Apps mide uso real por tokens procesados. No es benchmark de calidad, pero si es senal de mercado:

- que interfaces se usan;
- que agentes tienen traccion;
- que workflows consumen mucho contexto;
- que productos resuelven dolor suficientemente fuerte como para generar volumen;
- que proyectos open source merecen inspeccion prioritaria.

Esto complementa Benchmarks, Arena, Artificial Analysis, GitHub, papers, docs y repos.

Regla:

```text
OpenRouter Apps = senal de uso.
Benchmarks/evals = senal de capacidad.
Codigo/licencia = senal de extractibilidad.
Oli evals = decision final.
```

## Aplicaciones a estudiar primero

Primera lista por relevancia para Oli:

1. Hermes Agent
   - Ya revisado en `19_revision_hermes_agent_nous_2026-05-31.md`.
   - Extraible: runtime persistente, prompt layers, subagentes aislados, skills, sandboxing, checkpoints, gateway multicanal, provider routing.
   - Riesgo: ocupa narrativa de "agent that lives with you and grows".

2. OpenClaw
   - Relevante por adopcion, enfoque personal agent, canales, skills/plugins, accion sobre herramientas reales.
   - Extraible: channel gateway, skill marketplace mechanics, personal agent UX, local/self-hosted deployment, ecosystem leverage.
   - Riesgo: seguridad, supply chain, exceso de autonomia, permisos demasiado amplios.

3. Kilo Code
   - Relevante para developer workflows en IDE/CLI.
   - Extraible: sesiones de coding, parallel agents, team dashboard, BYOK/provider gateway, code review loops.
   - Riesgo: muy dev-first; Oli no debe quedar atrapado como "otro coding agent".

4. OpenCode
   - Relevante por terminal-native coding agent.
   - Extraible: tool loop de CLI, repo context handling, patch/edit loop, provider abstraction, install/distribution.
   - Riesgo: su dominio es narrower que Oli; util para Oli Labs y product/engineering ops, no como producto paraguas.

5. Claude Code, Cursor, Codex CLI
   - No todos son open source, pero son referencia de UX y expectativas.
   - Extraible: patrones de interaccion, plan/act/test loops, recovery, diff review, context ergonomics.
   - Riesgo: no confundir "agent de codigo" con Oli completo.

6. Pieces / memory-oriented tools
   - Relevante para memoria personal/developer context.
   - Extraible: context capture, local memory UX, search over working history.
   - Riesgo: memoria sin mission governance se vuelve ruido.

## Que se puede extraer

No se extrae "producto"; se extraen piezas:

### 1. Arquitectura

- runtime persistente;
- scheduler/cron;
- channel adapters;
- provider/model gateway;
- prompt assembly;
- tool registry;
- sandbox;
- checkpointing;
- plugin/skill loading;
- observability/traces.

### 2. Contratos

- formato de tool call;
- formato de task/subtask;
- formato de memory item;
- formato de skill/playbook;
- formato de approval;
- formato de trace/replay;
- formato de eval result.

### 3. UX operacional

- como el agente pide permisos;
- como muestra evidencia;
- como resume progreso;
- como maneja errores;
- como recupera una sesion;
- como muestra costos/model usage;
- como transforma una conversacion en accion.

### 4. Seguridad

- command allow/block lists;
- SSRF protection;
- credential filtering;
- env var passthrough allowlist;
- filesystem sandbox;
- plugin trust levels;
- network egress policy;
- human approval classes.

### 5. Distribucion

- install scripts;
- local runtime setup;
- Docker/VPS deployment;
- BYOK;
- model provider config;
- update channels;
- telemetry opt-in.

## Que NO se debe hacer

No copiar componentes por entusiasmo.

No traer una dependency pesada si solo necesitamos el patron.

No adoptar marketplaces/skills sin supply-chain policy.

No adoptar permisos estilo personal-agent para equipos/agencias sin evidence trail y approval classes.

No asumir que mucho uso en OpenRouter significa buena arquitectura.

No asumir que muchas stars significan madurez. Hermes ya mostro que los numeros publicos pueden ser impresionantes, pero Oli debe decidir por arquitectura, seguridad, licencia, fit y evals.

## Protocolo de extraccion

Para cada app candidata:

```text
1. Confirmar traccion
   - OpenRouter Apps
   - GitHub activity
   - comunidad/docs
   - issues recientes

2. Confirmar extractibilidad
   - licencia
   - lenguaje/stack
   - modularidad
   - dependencias
   - riesgo legal

3. Mapear arquitectura
   - runtime
   - tools
   - memory
   - prompts
   - subagents
   - security
   - observability

4. Mapear a Oli
   - Mission Kernel
   - Mission Black Box
   - permission classes
   - evidence trail
   - playbooks
   - Model Router
   - State-of-the-Art Decision Memo

5. Clasificar
   - copy? casi nunca
   - adapt?
   - reimplement pattern?
   - reject?
   - monitor?

6. Crear spike pequeno
   - una pieza aislada
   - sin tocar producto core congelado
   - con eval o test

7. Canonizar solo si pasa
   - ADR
   - TDD domain doc
   - schema si aplica
   - eval
```

## Matriz de extraccion

| Fuente | Extraer | Como entra en Oli | Prioridad |
|---|---|---|---|
| Hermes | prompt layers, skills, sandbox, checkpoints, subagents | runtime + playbooks + ADR-023 + tool security | Alta |
| OpenClaw | channel gateway, skill ecosystem, self-hosted runtime | future runtime/cloud/local + tool marketplace lessons | Alta |
| Kilo Code | IDE/CLI sessions, parallel coding agents, team dashboard | Product/Engineering Ops + Labs | Media-alta |
| OpenCode | terminal-native agent loop, patches, provider abstraction | Oli Labs + coding operator | Media |
| Pieces | memory capture/retrieval UX | semantic memory + user/org memory | Media |
| OpenRouter docs | routing, guardrails, caching, observability, app attribution | Model Intelligence + provider gateway + telemetry | Alta |

## Implicacion para Oli

Esto cambia el proceso estrategico:

Antes:

```text
Pensamos desde cero -> definimos TDD -> construimos.
```

Mejor:

```text
Tesis Oli
  -> buscar state-of-the-art y apps con traccion
  -> extraer patrones probados
  -> filtrar por seguridad/fit/licencia
  -> adaptar a Mission Kernel
  -> validar con evals
  -> canonizar en TDD
```

Esto no debilita la vision. La vuelve mas eficiente.

## Decision recomendada

Crear una mission class interna:

```text
open_source_agent_leverage_review
```

Output obligatorio:

```text
Leverage Memo
  - app/repo analizado
  - traccion
  - arquitectura
  - codigo reusable
  - patrones adaptables
  - riesgos
  - licencia
  - fit con Oli
  - recomendacion: adopt/adapt/reimplement/reject/monitor
  - proximo spike
```

Esto debe colgar de ADR-025 `State-of-the-Art Discovery`, no reemplazarlo.

## Siguiente paso recomendado

El siguiente pendiente no es escribir mas filosofia.

Es hacer una primera ronda de `open_source_agent_leverage_review` con tres objetivos:

1. Hermes Agent: ya revisado conceptualmente; falta mapear codigo/estructura si vamos a extraer patrones concretos.
2. OpenClaw: revisar repo/docs con foco en channel gateway, skills y seguridad.
3. OpenCode o Kilo Code: revisar repo/docs con foco en agent loop de codigo, patching, provider abstraction y sesiones.

Luego se crea un unico documento TDD:

```text
tdd/domain/open-source-leverage.md
```

Y, si hace falta:

```text
tdd/schemas/leverage_review.ts
```

Pero no antes de hacer al menos dos reviews reales. Canonizar demasiado pronto vuelve rigido un proceso que todavia esta aprendiendo.

