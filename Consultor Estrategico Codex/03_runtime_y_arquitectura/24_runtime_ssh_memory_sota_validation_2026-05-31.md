# Validacion SOTA: runtime/app PC/SSH y memoria de Oli

Fecha: 2026-05-31
Rol: Codex como consultor estrategico/auditor

## Veredicto

El modelo de Oli de `App PC / Desktop Bridge -> Mission API -> Dedicated Oli Runtime -> terminal/sandbox Linux -> SSH controlado` esta alineado conceptualmente con el state of the art, pero no esta suficientemente especificado para ser seguro.

La memoria de Oli esta mejor que RAG generico y tiene bases fuertes: Postgres, pgvector, memoria estructurada, provenance, Mission Black Box, After Action Review, playbooks y control del usuario. Frente al SOTA 2026 le faltan tres cosas para poder decir "nivel alto": jerarquia explicita de memoria, temporal knowledge graph y evals de memoria.

Decision ejecutiva:

```text
Runtime/SSH: alineado, pero no lanzable sin session recording + command policy.
Memoria: buena base, no SOTA completa todavia.
```

## Que se probo

Se ejecuto:

```text
Consultor Estrategico Codex/research_stack_v0/scripts/probe_research_connectors.py
```

Output:

```text
Consultor Estrategico Codex/research_stack_v0/probe_outputs/connector_probe_2026-05-31.json
```

Resultado:

```text
8 conectores OK
1 conector fallo: semantic_scholar_search -> HTTP 429
```

Tambien se ejecuto:

```text
Consultor Estrategico Codex/research_stack_v0/scripts/model_second_reader_probe.py
```

Output:

```text
Consultor Estrategico Codex/research_stack_v0/probe_outputs/model_second_reader_2026-05-31.md
```

Nota: el primer intento sin red elevada cayo al `development-model`. El segundo intento con red permitida produjo una respuesta real via OpenRouter y el archivo quedo escrito; el proceso fallo solo al imprimir por encoding Windows `cp1252`.

## Que saco de cada herramienta

| Herramienta | Resultado | Que aporto | Limitacion |
|---|---|---|---|
| OpenRouter docs index | OK | Indice oficial `llms.txt`; docs de modelos, apps, routing y app attribution | No da ranking de apps por si solo |
| GitHub Hermes | OK | Repo vivo, MIT, runtime/skills/subagents benchmark | Stars/issues no son calidad |
| GitHub OpenCode | OK | Coding agent terminal, MIT, referencia para patch/tool loop | Requiere review de codigo antes de integrar |
| GitHub Kilo Code | OK | Benchmark dev/team, roles y multi-surface workflow | Dev-first; no debe arrastrar a Oli |
| Hugging Face | OK | Modelos open-weight, metadata, downloads/likes | Downloads no son calidad; falta licencia/hardware fit |
| arXiv | OK | Literatura reciente de agent memory | Preprints no son prueba final |
| Semantic Scholar | FAIL 429 | Conector deseable | Necesita rate limits/API key/fallback |
| OpenAlex | OK | Encontro `Zep: A Temporal Knowledge Graph Architecture for Agent Memory` | Hay ruido semantico |
| NVD/CVE | OK | CVEs por keyword alrededor de Claude Code/coding agents | Keyword search requiere filtrado |
| Modelo via OpenRouter | OK en segundo intento | Segundo lector: runtime/SSH 5/10, memoria 6/10 | No navega; razona sobre facts dados |

## Validacion 1: App PC + SSH / Terminal

### Estado Oli

ADR-021 define Dedicated Oli Runtime, Desktop Bridge, SSH como canal setup/admin/power-user/debug y terminal execution pasando por Mission Step, Permission Policy, Tool/Terminal Scope, Credential Broker, Execution Environment y Audit Log.

### Comparacion SOTA

Fuentes usadas:

- Claude Code Desktop/Remote: desktop app + remote sessions + terminal/file editor.
- Cloudflare Browser SSH: browser-rendered SSH terminal con Zero Trust.
- Tailscale: identity-based private connectivity.
- Teleport: SSH access con audit log y session recording.
- NVD/CVE y security research: agentic terminal trae riesgos de RCE, exfiltracion, approval bypass, prompt injection, SSRF y command execution risk.

### Score

```text
6/10 como arquitectura conceptual.
4/10 como launch-ready security.
Score ejecutivo: 5/10.
```

### Lo que esta bien

- Separar Desktop Bridge de core brain.
- Tratar SSH como canal controlado, no como acceso libre.
- Mantener Mission Kernel como supervisor.
- Requerir audit/evidence para terminal.
- No exponer credenciales al modelo.
- Dedicated Runtime por tenant encaja con Claude Code/Managed Agents/Hermes.

### Gaps criticos

1. Falta session recording granular estilo Teleport.
2. Falta command-level policy: allowlist/denylist, dangerous command approval, network egress policy, file write scope, shell command classifier.
3. Falta sandbox real especificado: container boundary, filesystem mounts, seccomp/namespaces/AppArmor, no-root, ephemeral workspaces.
4. Falta threat model del runtime: SSH keys, OAuth tokens, API keys, repo secrets, prompt injection from repo/docs, exfiltration via curl/dns/http.
5. Falta remote approval UX para comandos de alto riesgo.

### Recomendacion runtime

Mantener la vision:

```text
Desktop Bridge + Dedicated Runtime + controlled terminal
```

pero no construir terminal/SSH productivo sin:

- session recording;
- command policy;
- credential broker;
- network egress control;
- sandbox hardening;
- approval UX;
- Mission Black Box completo.

## Validacion 2: Memoria de Oli

### Estado Oli

ADR-003 y `memory.ts` definen Postgres + pgvector, user/company/mission memory, confidence, source, status, reason, source mission IDs, history, tags, expires_at. ADR-019 agrega Mission Black Box, MissionMemoryPackage, After Action Review, playbooks y Cross-Agent Memory Capture. ADR-021 dice que cada mision recibe solo contexto relevante, permitido y trazable.

### Comparacion SOTA

Fuentes usadas:

- Letta: core memory en contexto + archival memory on-demand + context hierarchy.
- Zep/Graphiti: temporal knowledge graph para conversaciones y business data cambiante.
- Mem0: vector + graph memory, entity/relationship extraction.
- OpenAlex/arXiv: tendencia hacia temporal graph memory y memory evals.

### Score

```text
7/10 como arquitectura de producto.
5/10 como SOTA tecnico de memoria.
Score ejecutivo: 6/10.
```

### Lo que esta bien

- No es RAG plano.
- Tiene provenance y explicabilidad.
- Tiene capas user/company/mission.
- Tiene mission memory vinculada a outcomes.
- Tiene Mission Black Box y AAR.
- Tiene control de usuario: ver, editar, borrar, exportar.
- Tiene playbooks como salida operacional de memoria.

Esto es fuerte. Es mas producto-real que muchas librerias de memoria.

### Gaps criticos

1. Falta jerarquia explicita:

```text
working memory
core memory
archival memory
episodic/mission memory
procedural/playbook memory
semantic/document memory
```

2. Falta temporal graph:

```text
entidades
relaciones
valid_from / valid_to
supersedes
contradicts
observed_in_mission
confidence over time
```

3. Falta write-time reconciliation:

- crear;
- actualizar;
- supersede;
- contradiccion;
- merge;
- bajar confianza;
- pedir revision.

4. Falta memory eval harness:

- recall precision;
- outdated memory detection;
- contradiction detection;
- preference stability;
- mission improvement by memory;
- hallucinated memory prevention.

5. Falta privacy/data classification:

- personal;
- company;
- client;
- secret;
- public;
- derived-generalizable;
- non-exportable to solution bank.

## Decision final

### Runtime/app PC/SSH

```text
Decision: mantener direccion, endurecer seguridad antes de construir.
Estado: conceptualmente correcto, no launch-ready.
```

Construir primero:

1. TerminalCommandPolicy.
2. SessionRecording/AuditEvent model.
3. NetworkEgressPolicy.
4. Approval UX para comandos peligrosos.
5. Sandbox spec.

### Memoria

```text
Decision: buena base, no SOTA completa.
Estado: producto fuerte, memory engine incompleto.
```

Construir primero:

1. Memory hierarchy document.
2. Temporal graph schema.
3. Memory write reconciliation policy.
4. Memory evals.
5. Data classification for memory and solution bank.

## Implicacion para TDD

Crear o actualizar:

```text
tdd/adrs/ADR-026-runtime-terminal-access-and-session-recording.md
tdd/domain/terminal-command-policy.md
tdd/domain/memory-hierarchy-and-temporal-graph.md
tdd/domain/memory-evals.md
tdd/schemas/terminal_session.ts
tdd/schemas/memory_graph.ts
```

No recomiendo escribirlos todavia sin una decision corta de prioridad. La conclusion esta clara; ahora toca decidir si endurecemos runtime/SSH primero o memoria primero.

