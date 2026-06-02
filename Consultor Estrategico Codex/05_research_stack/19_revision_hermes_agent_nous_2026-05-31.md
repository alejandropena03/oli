# Revision Hermes Agent - Nous Research

Fecha: 2026-05-31
Rol: Codex como consultor estrategico/auditor
Objeto: https://hermes-agent.nousresearch.com/

## Veredicto

Hermes Agent es una señal state-of-the-art relevante para Oli.

No invalida la tesis de Oli. La confirma en varios puntos:

- agente persistente que vive en servidor/runtime;
- memoria y skills como loop de aprendizaje;
- multi-channel gateway;
- subagentes aislados;
- sandboxing real;
- provider/model routing;
- cron/automation;
- MCP/plugins;
- trajectory export para training;
- seguridad como capa visible.

Pero tambien muestra un riesgo claro para Oli:

```text
Si Oli se queda solo como TDD bonito + V0 tecnico,
Hermes ya ocupa parte del espacio "agent that lives with you and grows".
```

Oli debe diferenciarse por Mission Kernel, evidence trail, permission classes, decision memos, playbooks por org/cliente, model intelligence y enfoque producto/equipo/agencias. No por "un agente con tools".

## Que es Hermes Agent

Segun su home/docs, Hermes es un agente open source MIT que:

- vive en servidor, VPS, GPU cluster o serverless infrastructure;
- no esta atado al laptop;
- conversa por CLI y multiples plataformas;
- tiene memoria persistente;
- crea y mejora skills;
- delega subtareas a subagentes aislados;
- ejecuta tareas programaticas;
- usa backends local, Docker, SSH, Singularity, Modal y Daytona;
- soporta providers como Nous Portal, OpenRouter, OpenAI, Anthropic, Google y endpoints compatibles.

Repositorio verificado via GitHub API:

- repo: `NousResearch/hermes-agent`;
- creado: 2025-07-22;
- actualizado/pushed: 2026-05-31;
- licencia: MIT;
- lenguaje principal: Python;
- stars reportadas: ~174k;
- forks: ~29k;
- open issues: ~15k.

Nota critica: esos numeros son enormes para un repo relativamente reciente. Pueden reflejar traccion real, hype, imports, actividad automatizada o una mezcla. No basaria una decision solo en stars. Pero la actividad y la documentacion si justifican estudiarlo.

## Arquitectura observada

Hermes se organiza alrededor de un `AIAgent` central:

```text
Entry points
  CLI / Gateway / ACP / Batch / API / Python Library
    -> AIAgent
       -> Prompt Builder
       -> Provider Resolution
       -> Tool Dispatch
       -> Session Storage
       -> Tool Backends
```

Piezas importantes:

- prompt builder con tiers `stable`, `context`, `volatile`;
- provider resolution para multiples proveedores/API modes;
- tool registry con decenas de tools/toolsets;
- SQLite + FTS5 para sesiones;
- gateway de mensajeria con multiples plataformas;
- plugins;
- cron;
- ACP/editor integration;
- trajectory export.

Lectura para Oli:

```text
Hermes es agent-runtime-first.
Oli debe ser mission-supervisor-first.
```

Hermes parece optimizado para un agente general que vive contigo. Oli debe estar optimizado para misiones auditables, valor de negocio, permisos, playbooks y equipos.

## Puntos fuertes que Oli debe tomar en serio

### 1. Dedicated runtime real

Hermes ya comunica claramente:

```text
run it on a VPS/GPU cluster/serverless; talk from Telegram while it works elsewhere
```

Esto se parece mucho a ADR-021 de Oli. Buena noticia: confirma la direccion. Mala noticia: no es una idea rara; hay competencia visible.

Implicacion:

- ADR-021 esta bien.
- Oli debe acelerar la prueba de runtime dedicado.
- La narrativa "tu Oli vive en tu runtime" debe volverse producto, no solo documento.

### 2. Gateway multicanal

Hermes soporta muchas superficies: CLI, Telegram, Discord, Slack, WhatsApp, Signal, email, SMS, Matrix, etc.

Oli habia pensado OpenClaw/desktop bridge/canales. Hermes muestra que el multi-channel gateway es una ventaja fuerte porque el agente "vive donde tu trabajas".

Para Oli:

- no construir 20 canales temprano;
- si priorizar 1-2 canales que prueben valor: CLI/API + Telegram/Slack o WhatsApp segun ICP;
- mantener canal como capa de entrada, no como core.

### 3. Skills como procedural memory

Hermes tiene skills:

- `SKILL.md`;
- progressive disclosure;
- fallback por tools disponibles;
- required env vars/config;
- Skills Hub;
- agent-created skills;
- curator.

Esto toca directamente el moat de Oli: playbooks, solution bank y generalized solutions.

Lectura critica:

```text
Hermes skills = procedural memory portable.
Oli playbooks = procedural memory validada, auditable y orientada a negocio.
```

Oli debe aprender del formato de skills, pero no copiarlo sin mas. El diferenciador de Oli debe ser:

- playbook candidate detection;
- validation;
- permissions;
- evidence;
- cost;
- per-org calibration;
- solution bank sanitizada.

### 4. Subagentes aislados con contexto fresco

Hermes `delegate_task` crea child agents:

- contexto aislado;
- toolsets restringidos;
- terminal propia;
- solo resumen final entra al contexto padre;
- batch paralelo;
- nested delegation opt-in;
- limites de profundidad;
- monitoring `/agents`;
- costos/tokens/files touched por branch.

Esto confirma ADR-023 de Oli casi punto por punto.

Mejor practica observada:

```text
Subagents know nothing by default.
Parent must pass all required context.
```

Esto refuerza el `ContextPacket` de Oli. Tambien refuerza que Oli necesita UI/trace para ver subagentes, no solo logs ocultos.

### 5. execute_code para pipelines mecanicos

Hermes tiene `execute_code`: el agente escribe scripts Python que llaman tools via RPC. Solo stdout vuelve al LLM; resultados intermedios no entran al contexto.

Esto es importante.

Para Oli:

```text
No todo necesita subagente.
Si hay pipeline mecanico con loops/filtering, usar code execution con tool RPC.
Si hay juicio/razonamiento, usar subagente.
```

Esto deberia entrar como regla en ADR-023/subagent-evals futuro.

### 6. Seguridad mas avanzada que muchas demos

Hermes documenta:

- user authorization;
- dangerous command approval;
- hardline blocklist;
- YOLO mode con warning;
- Docker/Singularity/Modal isolation;
- MCP credential filtering;
- context file scanning;
- SSRF protection;
- website blocklist;
- env passthrough control;
- Tirith pre-exec scanning.

Oli ya tiene permisos en TDD, pero Hermes muestra que la barra esta subiendo. Oli necesita convertir ADR-020/tool security en implementacion real antes de conectar tools externas.

### 7. Prompt assembly y cache stability

Hermes separa prompt en tiers:

- stable;
- context;
- volatile.

Y usa frozen memory snapshots para preservar cache. Esto es muy relevante para Oli:

- AGENTS/context files como layer estable/semistable;
- memoria inyectada con control;
- no mutar prompt medio turno;
- context packets para subtareas.

Oli debe incorporar esta disciplina en prompt/runtime design.

### 8. Checkpoints y rollback

Hermes tiene snapshots con shadow git repo antes de writes/destructive commands, rollback por comando y caps de tamaño.

Oli ya tiene PostgresSaver/checkpoint pendiente, pero esto añade otra dimension:

```text
workflow checkpoint != filesystem rollback
```

Oli necesita ambos:

- mission checkpoint/resume;
- filesystem/artifact rollback para acciones del runtime.

## Donde Hermes parece mas debil que Oli podria ser

### 1. Mission governance

Hermes parece centrado en agent/session/tool execution. Oli esta diseñando mission classes, success criteria, validation reports, evidence drawer, permission classes y mission black box.

Oli puede ganar si convierte cada trabajo en unidad auditada con:

- mission intent;
- plan;
- permission class;
- evidence;
- validation;
- report;
- memory/playbook update.

### 2. Business/workflow orientation

Hermes es amplio: agent general para coding/research/admin. Oli tiene oportunidad de ser mas fuerte para:

- founders;
- equipos pequeños;
- agencias;
- reportes;
- client work;
- playbooks comerciales;
- team memory.

### 3. Decision memo layer

No vi en Hermes una capa equivalente a ADR-025:

```text
source quality + alternatives + buildability + risk + recheck date
```

Ese puede ser diferenciador real para Oli.

### 4. Model intelligence por tier/runtime

Hermes tiene provider switching y model catalog/provider routing. Oli esta diseñando Model Intelligence para decidir modelos por tier, runtime, hardware, evals y costo.

Si se hace bien, esto puede ser moat de producto/economia, no solo config.

### 5. Per-org solution bank

Hermes skills son portables/comunidad. Oli solution bank puede ser privado, derivado de misiones, sanitizado y orientado a workflows de negocio.

Eso sigue siendo diferenciador si se gobierna bien.

## Implicaciones directas para Oli

### Mantener

- Dedicated Oli Runtime.
- Mission Kernel como centro.
- Subagent contracts/context packets.
- State-of-the-art decision memos.
- Model Intelligence.
- Playbook/solution bank.
- Permission/evidence system.

### Endurecer

1. Tool security antes de tools reales.
2. Filesystem rollback junto a mission checkpointing.
3. Gateway/canal inicial.
4. Skills/playbooks como procedural memory.
5. Prompt assembly layers.
6. Runtime observability para subagents.

### No copiar

- No intentar soportar 20 canales temprano.
- No hacer "agent general que vive en Telegram" como posicionamiento principal.
- No dejar que skills auto-creadas escriban memoria/playbooks sin validation.
- No depender de agent-created skills sin governance.

## Riesgos para Oli

1. Hermes puede capturar mindshare tecnico rapido por ser MIT/open-source y muy completo.
2. Oli puede parecer menos impresionante si solo muestra V0 API/mock missions.
3. La frase "agent that grows with you" pisa parte del territorio narrativo de Oli.
4. Si Hermes skills + memory evolucionan rapido, la diferencia de Oli debe ser governance/evidence/business, no "aprende".
5. Seguridad de tools ya es mesa de entrada, no diferenciador opcional.

## Recomendacion

Crear un decision memo/TDD de comparativa:

```text
tdd/domain/competitor-hermes-agent-analysis.md
```

O mantenerlo por ahora en memoria consultor y extraer cambios puntuales:

1. Añadir a ADR-023 una nota: `execute_code`/scripted pipelines son alternativa a subagentes para tareas mecanicas.
2. Añadir a ADR-020/tool security: SSRF protection, MCP env filtering, hardline blocklist, credential passthrough allowlist.
3. Añadir a future ADR de runtime: filesystem rollback/shadow checkpoint.
4. Añadir a playbook/solution bank: skills-like progressive disclosure + curator, pero con validation/evidence.
5. Añadir a prompt engineering: stable/context/volatile prompt layers.

Mi recomendacion: no crear documento TDD de competitor todavia. Registrar aqui y traducir a cambios TDD cuando toquemos cada area.

## Fuentes

- Hermes home: https://hermes-agent.nousresearch.com/
- Hermes docs overview: https://hermes-agent.nousresearch.com/docs
- Hermes llms.txt: https://hermes-agent.nousresearch.com/docs/llms.txt
- Hermes architecture: https://hermes-agent.nousresearch.com/docs/developer-guide/architecture
- Hermes subagent delegation: https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation
- Hermes persistent memory: https://hermes-agent.nousresearch.com/docs/user-guide/features/memory
- Hermes skills system: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
- Hermes security: https://hermes-agent.nousresearch.com/docs/user-guide/security
- Hermes code execution: https://hermes-agent.nousresearch.com/docs/user-guide/features/code-execution
- Hermes checkpoints/rollback: https://hermes-agent.nousresearch.com/docs/user-guide/checkpoints-and-rollback
- Hermes prompt assembly: https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly
- GitHub API repo metadata: https://api.github.com/repos/NousResearch/hermes-agent

