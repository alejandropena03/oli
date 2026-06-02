# AI Engineering Skill Signal for Oli

**Fecha:** 2026-05-31
**Estado:** strategic target
**Owner:** Alejandro Pena

---

## Proposito

Oli no solo debe funcionar como producto comercial. Tambien debe servir como evidencia tecnica de alto nivel para roles de AI engineering, LLM developer, agent engineer, automation engineer, model serving engineer o applied AI product engineer.

El objetivo no es publicar todo el producto. El objetivo es que el proyecto demuestre, de forma verificable, que Alejandro puede construir sistemas de IA reales:

- medibles;
- seguros;
- trazables;
- con memoria;
- con tool use;
- con model routing;
- con evals;
- con serving de modelos open-weight;
- con loops de mejora;
- con criterio de producto.

---

## Principio

Un repo privado puede ser valioso, pero no prueba suficiente hacia afuera.

Oli debe separar:

```text
Private Oli Core
  - producto comercial
  - mission kernel completo
  - playbooks reales
  - routing propietario
  - solution bank
  - customer memory/runtime

Public Oli Labs
  - harnesses genericos
  - evaluaciones reproducibles
  - demos con datos sinteticos
  - adapters no sensibles
  - reports tecnicos
  - mini-entornos de agente
  - fine-tuning lab
```

La senal profesional debe venir de laboratorios publicos reproducibles, no de regalar el core.

---

## Skill matrix

| Skill | Estado actual en Oli | Gap | Propuesta que hace sentido |
|---|---|---|---|
| Agent orchestration | Parcial | Misiones aun poco reales por step | Agent eval harness con toy missions y traces |
| Stateful workflows | Parcial | Falta checkpoint durable real | PostgresSaver + resume demo |
| Human-in-the-loop | Parcial | Approval API existe, no durable graph interrupt | HITL durable en una mision con resume |
| Evals de agentes | Debil | No hay dataset ni graders | Golden mission dataset + regression runner |
| Tool use seguro | Fuerte en ADRs, debil en codigo | Falta enforcement | Tool scopes + audit + taint mini-implementation |
| RAG/memoria operacional | Fuerte en TDD, debil en codigo | Falta pgvector/retrieval | Memory lab con provenance, confidence y retrieval |
| Model routing | Parcial | Router estatico | Model registry + benchmark runner |
| vLLM/inference serving | No | Sin serving real | vLLM OpenAI-compatible adapter + latency/cost report |
| Fine-tuning/post-training | No | Sin pipeline | SFT/LoRA lab con eval antes/despues |
| Sandboxing/terminal | En TDD | Falta ejecucion aislada | Sandbox lab con command audit y filesystem scope |
| Observability | Parcial | Falta trace completo | Mission black box con model/tool/cost logs |
| Security/privacy | Fuerte en ADRs | Falta prueba ejecutable | Prompt injection fixture + taint policy demo |
| Product judgment | Fuerte | Falta narrativa publica verificable | Technical case studies y architecture docs sanitizados |

---

## Propuestas canonicas para fortalecer Oli

### 1. Oli Agent Eval Harness

Objetivo:

> Demostrar que Oli no solo ejecuta agentes, sino que los mide.

Debe incluir:

- misiones sinteticas;
- inputs esperados;
- graders deterministas cuando sea posible;
- LLM-as-judge solo cuando este justificado;
- metricas de success rate, costo, latencia, tool errors, validation pass/fail;
- comparacion entre single-agent, multi-step y multi-agent;
- regression suite.

### 2. Mission Black Box / Trace Viewer

Objetivo:

> Demostrar observabilidad de agentes.

Cada mision debe poder mostrar:

- raw intent;
- intent interpretado;
- contexto recuperado;
- plan;
- steps;
- model calls;
- tool calls;
- approval events;
- artifacts;
- validation report;
- cost report;
- failure/repair timeline.

Version publica:

- trazas redacted o sinteticas;
- UI simple o markdown report;
- no customer data.

### 3. vLLM Runtime Adapter

Objetivo:

> Demostrar que Oli puede correr modelos open-weight en infraestructura seria.

Debe probar:

- endpoint OpenAI-compatible;
- integracion con Model Router;
- benchmark de p50/p95 latency;
- throughput basico;
- costo estimado por mision;
- fallback a premium API solo cuando policy lo permite.

Ollama queda como dev/simple-local mode. vLLM queda como senal profesional de serving serio.

### 4. Memory and RAG Lab

Objetivo:

> Demostrar memoria operacional, no "chat with docs".

Debe incluir:

- Postgres + pgvector;
- memory entries con provenance;
- confidence;
- memory type;
- source mission;
- permission scope;
- retrieval por mission objective;
- reporte de por que cada memoria fue recuperada.

### 5. Fine-Tuning Lab

Objetivo:

> Demostrar criterio de post-training, no fine-tuning decorativo.

Debe responder:

- que tarea justifica fine-tuning;
- que baseline se compara: prompting/RAG/router;
- que dataset se usa;
- como se filtra o sintetiza;
- como se evalua antes/despues;
- que modelo open-weight se usa;
- que riesgos legales/privacidad existen;
- cuando NO conviene fine-tunear.

Primeras tareas candidatas:

- output schema reliability;
- mission classification;
- memory extraction;
- validation rubric following;
- repair suggestion formatting.

Tareas malas para primer fine-tuning:

- knowledge general;
- customer-specific facts;
- informacion temporal;
- contenido que cambia rapido;
- datos privados sin politica formal.

### 6. Tool Security Mini-Implementation

Objetivo:

> Demostrar que Oli entiende que agentes con herramientas son superficie de ataque.

Debe incluir:

- tool scopes;
- permission class;
- credential broker boundary;
- taint labels;
- audit record;
- fixture de prompt injection;
- tests donde contenido no confiable reduce permisos.

### 7. Public Technical Case Studies

Objetivo:

> Hacer visible el razonamiento tecnico sin abrir el core.

Temas recomendados:

- "Why mission traces matter for AI agents";
- "Evaluating agent workflows beyond final answers";
- "RAG memory is not enough: operational memory for agents";
- "Open-weight model routing with vLLM and premium fallback";
- "Tool security for AI operators";
- "When fine-tuning helps and when it is theater".

---

## Orden recomendado

No construir todo a la vez.

Orden de maximo impacto:

```text
1. Eval Harness
2. Mission Black Box / Trace Report
3. Memory + pgvector Lab
4. Tool Security Mini-Implementation
5. vLLM Runtime Adapter
6. Fine-Tuning Lab
7. Public Case Studies
```

Razon:

- Evals hacen que todo lo demas sea creible.
- Trace hace que los agentes sean auditables.
- Memory prueba el moat.
- Tool security diferencia a Oli de demos fragiles.
- vLLM demuestra infra.
- Fine-tuning impresiona solo si tiene evals.

---

## Public proof policy

Lo publico debe probar capacidad sin exponer ventaja comercial.

Publicar:

- harnesses genericos;
- toy datasets;
- synthetic traces;
- schemas reducidos;
- benchmark scripts;
- adapters no propietarios;
- notebooks de fine-tuning sintetico;
- reports tecnicos;
- videos/demo GIFs.

No publicar:

- Oli Core completo;
- playbooks comerciales;
- solution bank;
- prompts propietarios;
- datos reales;
- routing heuristics sensibles;
- unit economics internos;
- customer memory;
- conectores completos si crean ventaja.

---

## Definition of done

Oli esta bien posicionado como proyecto profesional cuando una persona externa puede ver repos publicos y entender:

1. Alejandro sabe construir agentes con estado.
2. Alejandro sabe evaluar agentes, no solo llamarlos.
3. Alejandro sabe manejar memoria/RAG con procedencia.
4. Alejandro sabe servir modelos open-weight y medir costo/latencia.
5. Alejandro sabe pensar seguridad de herramientas.
6. Alejandro sabe disenar feedback loops y fine-tuning con evals.
7. Alejandro sabe separar producto privado de evidencia publica.

