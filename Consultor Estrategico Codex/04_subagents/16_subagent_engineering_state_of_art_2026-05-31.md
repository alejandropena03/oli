# Subagent engineering para Oli - state of the art y analisis first principles

Fecha: 2026-05-31
Rol: Codex como consultor estrategico/auditor

## Veredicto

Oli no debe adoptar "multi-agent" como arquitectura por defecto.

Debe adoptar **subagent engineering medible**: delegacion especializada solo cuando mejora una de cuatro variables:

1. calidad;
2. seguridad;
3. latencia;
4. costo.

El state of the art actual converge en una idea: el centro no son los agentes; es el **contexto correcto para la unidad correcta de trabajo**, con trazas, evals, verificadores y limites de herramientas.

## Lo ultimo observado

### OpenAI Agents SDK

OpenAI distingue dos patrones principales:

- **agents as tools**: un manager mantiene control y llama especialistas como herramientas.
- **handoffs**: un agente transfiere la conversacion a un especialista.

Tambien recomienda orquestar por codigo cuando se busca determinismo, costo/latencia predecible, structured outputs, loops evaluator-worker y paralelismo.

Implicacion para Oli:

```text
Oli debe preferir manager + specialists-as-tools para misiones auditables.
Handoffs solo cuando el especialista debe hablar directamente con el usuario.
```

### Anthropic Research / Engineering

Anthropic reporta que multi-agent gana especialmente en:

- context isolation;
- parallel execution;
- specialization.

Su sistema de research usa lead agent + subagents paralelos. Los subagents exploran con contextos propios y devuelven resúmenes comprimidos al lead. Tambien enfatizan context engineering como sucesor de prompt engineering.

Implicacion para Oli:

```text
Subagentes valen cuando comprimen trabajo exploratorio y evitan contaminar el contexto del orchestrator.
```

### LangGraph / LangChain

LangGraph pone el foco en:

- agentes como nodos;
- supervisor;
- handoffs;
- subgraphs;
- state updates;
- context engineering.

Su documentacion dice directamente que el centro de multi-agent design es decidir que informacion ve cada agente.

Implicacion para Oli:

```text
El Context Packet es tan importante como el agent role.
Sin Context Packet, los subagentes son prompts sueltos.
```

### Google ADK

Google ADK documenta patrones canonicos:

- coordinator/dispatcher;
- sequential pipeline;
- parallel fan-out/gather;
- hierarchical decomposition;
- review/critique;
- iterative refinement;
- human-in-the-loop.

Implicacion para Oli:

```text
Oli debe elegir topologia por mission class, no por preferencia de framework.
```

### Microsoft Agent Framework

Microsoft Agent Framework trae patrones integrados de orchestrations y una tendencia clara hacia topology control, workflows, observability, lifecycle y production primitives. Microsoft tambien esta empujando orquestacion deterministica para multi-agent workflows.

Implicacion para Oli:

```text
La direccion productiva es mezclar workflows declarativos/deterministicos con agentes especializados, no dejar todo al LLM.
```

### Papers 2026 y señal academica

Los trabajos recientes apuntan a:

- task-adaptive orchestration;
- plan-execute-verify-replan;
- seleccion dinamica entre topologias: parallel, sequential, hierarchical, hybrid;
- verificacion como mecanismo central de calidad.

Implicacion para Oli:

```text
El diferencial no es tener subagentes. Es seleccionar y verificar la topologia adecuada por tarea.
```

## First principles para Oli

Oli promete convertir intencion en trabajo terminado.

Eso exige resolver cinco problemas:

1. **Interpretar intencion**: que quiere realmente el usuario.
2. **Dividir trabajo**: que partes son independientes, especializadas, riesgosas o verificables.
3. **Ejecutar con permisos**: que acciones pueden hacerse, con que herramientas y bajo que scope.
4. **Validar resultado**: quien verifica que el output cumple criterios.
5. **Aprender**: que se vuelve memoria, playbook, eval o training example.

Subagentes solo son utiles si ayudan en alguno de esos problemas.

## Regla dura

```text
Un subagente solo existe si tiene:
- objetivo propio;
- contexto propio;
- tools propias o restricciones propias;
- output schema propio;
- validator propio;
- razon medible para existir.
```

Si falta alguno, probablemente es solo un prompt mas.

## Topologias candidatas para Oli

### 1. Single agent + tools

Uso:

- tareas simples;
- baja ambiguedad;
- poco riesgo;
- salida corta;
- no hay necesidad de verificacion independiente.

Ejemplo:

- resumir una nota;
- generar checklist;
- clasificar una mision simple.

### 2. Manager + agents-as-tools

Uso:

- Oli debe mantener una sola voz;
- specialists no deben hablar al usuario;
- el orchestrator sintetiza;
- hay varias perspectivas.

Ejemplo:

- founder notes -> spec;
- market research + technical assessment + risk review;
- reportes semanales con varias fuentes.

### 3. Sequential pipeline

Uso:

- cada paso depende del anterior;
- se puede validar entre pasos;
- hay artefactos intermedios.

Ejemplo:

- raw notes -> MissionSpec -> plan -> execution tasks -> validation report.

### 4. Parallel fan-out / gather

Uso:

- tareas independientes;
- research amplio;
- comparaciones;
- reducir latencia.

Ejemplo:

- investigar 5 competidores;
- analizar 3 estrategias de pricing;
- revisar varios documentos.

### 5. Generator-critic / verify-repair

Uso:

- outputs importantes;
- alta ambiguedad;
- riesgo de errores sutiles.

Ejemplo:

- outreach draft antes de aprobacion;
- arquitectura tecnica;
- decision memo;
- reporte de cliente.

### 6. Hierarchical decomposition

Uso:

- misiones largas;
- multiples workstreams;
- necesidad de checkpoints.

Ejemplo:

- AI-first audit de una empresa;
- build plan completo para onboarding de equipo;
- due diligence operacional.

No usar en V0 salvo como lab/simulacion.

### 7. Handoff user-facing

Uso:

- especialista debe hablar con el usuario;
- cambio claro de modo;
- conversacion multi-turn especializada.

Ejemplo:

- "modo tecnico";
- "modo legal/compliance" futuro;
- "modo onboarding".

Riesgo:

- voz inconsistente;
- perdida de control del orchestrator;
- permisos mas dificiles de auditar.

## Componentes que Oli debe predesarrollar

### Agent Task Contract

Define la unidad minima de delegacion:

- task_id;
- mission_id;
- role;
- objective;
- non_goals;
- input context;
- allowed tools;
- permission ceiling;
- expected output schema;
- success criteria;
- token/time/cost budget;
- failure modes;
- evidence requirements.

### Context Packet

Define que ve cada subagente:

- mission summary;
- relevant memory;
- source excerpts;
- constraints;
- prior outputs;
- forbidden context;
- provenance;
- confidence;
- max tokens.

### Agent Task Result

Define que devuelve:

- answer/artifact;
- evidence refs;
- assumptions;
- confidence;
- unresolved questions;
- tool calls summary;
- cost/latency;
- validation hooks;
- suggested memory/playbook updates.

### Scheduler / Topology Selector

Decide:

- single-agent vs multi-agent;
- parallel vs sequential;
- model per subtask;
- when to stop;
- when to escalate.

### Validator / Verifier

No debe ser el mismo agente que genero el output.

Valida:

- schema;
- factuality against evidence;
- permission compliance;
- success criteria;
- missing critical info;
- hallucinated sources/actions.

### Synthesizer

Combina outputs parciales sin perder:

- contradicciones;
- incertidumbre;
- evidencia;
- costos;
- decisiones pendientes.

## Que debe evitar Oli

1. Subagentes permanentes para todo.
2. Shared context gigante entre todos.
3. Especialistas sin schema.
4. Supervisor que solo reenvia mensajes.
5. Validator que opina pero no comprueba.
6. Handoffs user-facing prematuros.
7. Loops sin budget ni stop condition.
8. Multi-agent sin eval baseline contra single-agent.

## Decision recomendada para Oli

Oli debe canonizar:

```text
Default: single orchestrator + tools.
Upgrade 1: manager + specialists-as-tools.
Upgrade 2: deterministic workflow + evaluator loops.
Upgrade 3: parallel fan-out for research.
Upgrade 4: hierarchical multi-agent only for long-horizon missions.
```

Esto preserva el caracter de Oli: operador de ejecucion, no comite.

## Primer analisis/prototipo recomendado

No construir un swarm.

Diseñar primero:

```text
Agent Task Contract v0
Context Packet v0
Agent Task Result v0
Topology Selector rules v0
```

Mission class de prueba:

```text
Founder notes -> Claude Code-ready spec
```

Por que:

- ya esta en el TDD como primera mission class recomendada;
- ayuda directamente a construir Oli;
- permite evaluar si Claude Code puede implementar;
- requiere interpretar, estructurar, validar y entregar;
- puede mostrar subagent engineering sin tocar herramientas externas riesgosas.

## Contratos v0 propuestos

Estos contratos no son todavia codigo. Son la forma minima de volver solido el diseño antes de meterlo al TDD y despues al desarrollo.

### 1. Mission Class

Una `Mission Class` es un tipo repetible de trabajo que Oli sabe interpretar, ejecutar, validar y eventualmente convertir en playbook.

No es una mision individual. Es la plantilla operacional.

Ejemplo:

```text
Mission individual:
"Convierte estas notas sucias sobre pricing en un spec para Claude Code."

Mission class:
founder_notes_to_claude_code_spec
```

Contrato:

```yaml
mission_class:
  id: founder_notes_to_claude_code_spec
  title: Founder notes -> Claude Code-ready spec
  description: Convert rough founder notes into an implementation-ready spec.
  primary_icp:
    - founder_builder
    - product_engineering_ops
  input_contract:
    required:
      - raw_notes
    optional:
      - repo_context
      - relevant_docs
      - constraints
      - target_files
      - existing_decisions
  output_contract:
    artifacts:
      - implementation_spec
      - open_questions
      - risk_notes
      - validation_checklist
    format: markdown
  permission_ceiling: class_1
  default_topology: manager_with_specialists_as_tools
  success_criteria:
    - spec_has_clear_goal
    - spec_has_non_goals
    - spec_has_implementation_scope
    - spec_has_acceptance_tests
    - spec_has_risks_and_assumptions
    - claude_code_can_execute_with_minimal_questions
  playbook_candidate_rule:
    repeated_use_threshold: 3
    requires_user_confirmation: true
```

Campos obligatorios para cualquier mission class:

- `id`;
- `input_contract`;
- `output_contract`;
- `permission_ceiling`;
- `default_topology`;
- `success_criteria`;
- `validation_strategy`;
- `playbook_candidate_rule`.

### 2. Agent Task Contract

Un `Agent Task Contract` es la orden formal que el Orchestrator entrega a un subagente o especialista.

El subagente no recibe "haz esto" en texto libre. Recibe un contrato con limites.

Contrato:

```yaml
agent_task_contract:
  task_id: uuid
  mission_id: uuid
  mission_class_id: founder_notes_to_claude_code_spec
  role: technical_spec_writer
  objective: Produce an implementation-ready spec from rough notes.
  non_goals:
    - do_not_write_code
    - do_not_modify_files
    - do_not_invent_missing_product_decisions
  inputs:
    context_packet_id: uuid
  allowed_tools:
    - read_repo_files
    - search_repo
  forbidden_tools:
    - write_files
    - run_commands
    - external_network
  permission_ceiling: class_1
  expected_output_schema: technical_spec_v0
  success_criteria:
    - identifies_goal
    - identifies_scope
    - identifies_non_goals
    - maps_notes_to_files_or_modules_if_possible
    - lists_acceptance_tests
    - marks_open_questions_explicitly
  budgets:
    max_tokens: 8000
    max_wall_time_seconds: 180
    max_tool_calls: 12
  evidence_requirements:
    - cite_relevant_input_note_ids
    - cite_repo_files_if_used
  failure_policy:
    on_missing_context: return_blocked_with_specific_question
    on_conflicting_context: return_conflict_report
    on_tool_failure: return_partial_with_error
```

Regla:

```text
Si un subagente no puede recibir un Agent Task Contract claro,
la tarea no esta lista para delegarse.
```

### 3. Context Packet

Un `Context Packet` define exactamente que informacion ve un subagente.

Este es probablemente el contrato mas importante. Sin context packet, Oli termina metiendo todo el historial en cada agente y pierde costo, claridad y privacidad.

Contrato:

```yaml
context_packet:
  context_packet_id: uuid
  mission_id: uuid
  intended_role: technical_spec_writer
  summary:
    user_intent: Convert rough notes into implementation-ready spec.
    mission_class_id: founder_notes_to_claude_code_spec
  source_inputs:
    - id: note_001
      type: user_note
      content_ref: runtime_artifact_ref
      trust_level: user_provided
  retrieved_memory:
    - id: mem_123
      layer: project
      reason_included: Existing decision about V0 feature freeze.
      confidence: high
      content_ref: memory_ref
  repo_context:
    - path: tdd/domain/oli-constitution.md
      reason_included: Defines product character and operating principles.
      excerpt_ref: excerpt_ref
  constraints:
    - no_product_code_changes
    - respect_v0_feature_freeze
    - output_must_be_claude_code_ready
  forbidden_context:
    - unrelated_private_user_documents
    - raw_credentials
    - full_repo_dump
  provenance:
    generated_by: orchestrator
    generated_at: iso_timestamp
  token_budget:
    max_context_tokens: 12000
```

Reglas:

- Cada item incluido debe tener `reason_included`.
- Cada memoria debe tener `confidence`.
- Cada fuente debe tener `trust_level`.
- Contexto prohibido debe declararse cuando sea relevante.
- El packet debe ser reproducible desde mission trace.

### 4. Agent Task Result

Un `Agent Task Result` es el output estructurado que vuelve al Orchestrator.

Contrato:

```yaml
agent_task_result:
  task_id: uuid
  mission_id: uuid
  role: technical_spec_writer
  status: completed # completed | partial | blocked | failed
  output:
    artifact_type: technical_spec_v0
    artifact_ref: runtime_artifact_ref
  assumptions:
    - assumption: No production UI exists yet.
      confidence: medium
      evidence_ref: repo_search_result
  open_questions:
    - question: Should this spec target V0 or V1?
      blocking: false
  risks:
    - risk: Spec may imply new product feature despite V0 freeze.
      severity: high
      mitigation: Mark as TDD-only until unfreeze.
  evidence_refs:
    - note_001
    - tdd/domain/oli-constitution.md
  tool_calls_summary:
    count: 4
    failures: 0
  cost_summary:
    tokens_in: 6000
    tokens_out: 1800
    wall_time_seconds: 42
  confidence: 0.78
  suggested_next_steps:
    - Run validator against acceptance checklist.
  memory_suggestions:
    - key: preferred_spec_format
      value: Veredicto, scope, files, tests, risks, open questions.
      confidence: medium
      reason: Repeated format preference observed.
  playbook_signal:
    candidate: true
    reason: Repeated mission class with stable input/output.
```

Regla:

```text
El Orchestrator no sintetiza outputs libres.
Sintetiza Agent Task Results con evidencia, supuestos, riesgos y costo.
```

### 5. Validator Contract

El validator no evalua "si suena bien". Evalua contra criterios.

Contrato:

```yaml
validator_contract:
  validation_id: uuid
  mission_id: uuid
  target_task_id: uuid
  validator_role: technical_spec_validator
  validation_type:
    - schema_validation
    - success_criteria_validation
    - permission_validation
    - evidence_validation
  criteria:
    - id: spec_has_clear_goal
      blocking: true
    - id: spec_has_acceptance_tests
      blocking: true
    - id: no_unapproved_product_execution
      blocking: true
    - id: open_questions_marked
      blocking: false
  output_schema: validation_report_v0
```

Resultado:

```yaml
validation_report:
  validation_id: uuid
  overall_passed: false
  score: 0.75
  criteria_results:
    - criterion_id: spec_has_clear_goal
      passed: true
      evidence_ref: artifact_section_goal
    - criterion_id: spec_has_acceptance_tests
      passed: false
      evidence_ref: artifact_section_tests
      failure_reason: Tests are described as vague manual review, not acceptance checks.
      blocking: true
  repair_possible: true
  repair_instruction: Add concrete acceptance tests tied to expected files/behavior.
```

Regla:

```text
El validator debe poder fallar el output aunque el texto sea bonito.
```

### 6. Topology Selector Rules v0

El `Topology Selector` decide si una mision usa single-agent, specialists, pipeline, fan-out o verify-repair.

Inputs:

```yaml
topology_selector_input:
  mission_class_id: string
  complexity: low | medium | high
  risk_class: class_0 | class_1 | class_2 | class_3 | class_4
  ambiguity: low | medium | high
  requires_external_tools: boolean
  requires_parallel_research: boolean
  requires_independent_validation: boolean
  latency_sensitivity: low | medium | high
  cost_sensitivity: low | medium | high
```

Reglas iniciales:

```text
Si complexity=low y risk_class<=class_1:
  usar single_agent_with_tools.

Si requiere independent_validation:
  usar generator_validator.

Si requiere parallel_research y las subtareas son independientes:
  usar parallel_fanout_gather.

Si risk_class>=class_3:
  usar workflow con ruta visible + approval gate + validator.

Si ambiguity=high:
  primero usar planner/specifier, no executor.

Si latency_sensitivity=high:
  preferir single_agent o parallel_fanout, evitar sequential profundo.

Si cost_sensitivity=high:
  usar modelo barato/local para subclasificacion y modelo fuerte solo para sintesis/validacion critica.
```

Salida:

```yaml
topology_decision:
  topology: manager_with_specialists_as_tools
  reason: Mission requires spec generation and independent validation, but no direct external action.
  agents:
    - mission_planner
    - technical_spec_writer
    - technical_spec_validator
  model_routing:
    planner: strong_reasoning
    writer: balanced
    validator: strong_reasoning
  expected_cost_tier: medium
  approval_required: false
```

## Roles canonicos v0

No todos estos se implementan ya. Son roles canonicos para disenar contratos y evals.

### Orchestrator

Responsable de:

- interpretar intencion;
- seleccionar mission class;
- construir context packets;
- decidir topologia;
- coordinar tasks;
- sintetizar resultado final;
- mantener una sola voz ante el usuario.

### Planner / Specifier

Responsable de convertir input ambiguo en MissionSpec o plan ejecutable.

### Researcher

Responsable de investigar con fuentes, fechas, confianza y gaps.

### Technical Architect

Responsable de opciones tecnicas, tradeoffs, riesgos y ADR candidates.

### Execution Operator

Responsable de acciones concretas bajo permisos.

### Validator

Responsable de validar contra success criteria y evidencia.

### Memory Curator

Responsable de sugerir memoria, no escribirla directamente.

### Playbook Curator

Responsable de detectar si una mision repetida puede volverse playbook.

### Synthesizer

Responsable de convertir resultados parciales en entregable final claro, trazable y con contradicciones preservadas.

## Ejemplo completo: Founder notes -> Claude Code-ready spec

### Entrada

```text
"Quiero que Oli tenga un endpoint para convertir notas en specs para Claude Code.
No quiero que toque producto todavia, pero quiero el diseño listo."
```

### Mission class detectada

```text
founder_notes_to_claude_code_spec
```

### Topology decision

```yaml
topology: manager_with_specialists_as_tools
reason: Ambiguous founder notes need structuring and independent validation, but no external side effects.
agents:
  - planner
  - technical_spec_writer
  - validator
```

### Tasks

```text
Task 1 - Planner:
  Convertir notas en MissionSpec preliminar.

Task 2 - TechnicalSpecWriter:
  Convertir MissionSpec en spec implementable.

Task 3 - Validator:
  Verificar si Claude Code puede implementar con preguntas minimas.

Task 4 - Orchestrator/Synthesizer:
  Entregar spec final, riesgos, preguntas abiertas y next action.
```

### Output esperado

```markdown
# Spec: Founder notes to Claude Code-ready spec

## Goal
...

## Non-goals
...

## Proposed files
...

## API / contracts
...

## Acceptance tests
...

## Risks
...

## Open questions
...
```

### Validation

El validator falla si:

- no hay tests;
- no hay non-goals;
- se propone tocar producto pese al freeze;
- no se marca permiso;
- no queda claro que Claude Code debe construir.

## Ruta para volverlo TDD formal

Este documento todavia es consultoria/arquitectura. Para agregarlo formalmente al TDD, el proceso correcto es:

### Fase 1 - Consolidar decision

Crear ADR:

```text
tdd/adrs/ADR-023-subagent-engineering-contracts.md
```

Contenido:

- decision: Oli adopta subagent engineering contractual, no multi-agent por defecto;
- fuentes state-of-the-art;
- topologias permitidas;
- regla de existencia de subagentes;
- consecuencias para LangGraph, Model Router, evals y Mission Black Box.

Acceptance criterion:

```text
Un lector debe entender cuando Oli usa single-agent, specialists-as-tools,
pipeline, fan-out, validator loop o jerarquia.
```

### Fase 2 - Crear spec de dominio

Crear:

```text
tdd/domain/subagent-engineering.md
```

Contenido:

- definicion de Mission Class;
- Agent Task Contract;
- Context Packet;
- Agent Task Result;
- Validator Contract;
- Topology Selector;
- roles canonicos;
- ejemplos por mission class.

Acceptance criterion:

```text
El documento debe permitir implementar schemas sin volver a decidir la arquitectura.
```

### Fase 3 - Crear schemas

Crear o extender:

```text
tdd/schemas/agent_task_contract.ts
tdd/schemas/context_packet.ts
tdd/schemas/agent_task_result.ts
tdd/schemas/topology_decision.ts
```

O, si se prefiere mantener menos archivos:

```text
tdd/schemas/subagent_contracts.ts
```

Acceptance criterion:

```text
Los contratos deben ser validables con Zod y compatibles con Mission,
Evidence, Tool y Suboperator schemas existentes.
```

### Fase 4 - Conectar con mission flows

Actualizar:

```text
tdd/domain/mission-flows.md
tdd/slices/slice-001-*.md
tdd/slices/slice-002-*.md
```

Contenido:

- donde se genera Context Packet;
- donde se crean Agent Task Contracts;
- donde se guardan Agent Task Results;
- donde entra Validator;
- donde se registra evidence.

Acceptance criterion:

```text
Cada mission flow debe mostrar si usa single-agent, specialist-as-tool,
pipeline o validator loop.
```

### Fase 5 - Definir evals antes de implementacion

Crear:

```text
tdd/domain/subagent-evals.md
```

Contenido:

- baseline single-agent;
- candidate multi-agent topology;
- metricas: quality, cost, latency, tool failures, validation pass rate, unnecessary questions;
- fixtures para founder_notes_to_claude_code_spec.

Acceptance criterion:

```text
No se acepta una topologia multi-agent si no supera baseline single-agent
en al menos una metrica importante sin degradar seguridad/costo de forma inaceptable.
```

### Fase 6 - Implementacion posterior

Solo despues de ADR + domain spec + schemas + eval plan:

```text
packages/orchestrator/task_contracts.py
packages/orchestrator/context_packets.py
packages/orchestrator/task_results.py
packages/orchestrator/topology_selector.py
packages/orchestrator/validators.py
```

Tests:

```text
tests/test_subagent_contracts.py
tests/test_context_packet_builder.py
tests/test_topology_selector.py
tests/test_founder_notes_to_spec_eval.py
```

Acceptance criterion:

```text
El primer flujo debe demostrar que Oli puede generar un spec listo para Claude Code,
validarlo contra criterios y registrar evidence sin tocar producto real.
```

## Siguiente iteracion recomendada

La siguiente iteracion no debe implementar codigo.

Debe producir el paquete TDD minimo:

1. `ADR-023-subagent-engineering-contracts.md`
2. `tdd/domain/subagent-engineering.md`
3. borrador de `tdd/schemas/subagent_contracts.ts`
4. borrador de `tdd/domain/subagent-evals.md`

Despues de eso, se puede decidir si se implementa un primer slice.

## Fuentes usadas

- OpenAI Agents SDK - Agent Orchestration: https://openai.github.io/openai-agents-js/guides/multi-agent/
- OpenAI Agents SDK - Handoffs: https://openai.github.io/openai-agents-python/handoffs/
- OpenAI Evaluation Best Practices: https://platform.openai.com/docs/guides/evaluation-best-practices
- OpenAI Agent Evals: https://platform.openai.com/docs/guides/agent-evals
- Anthropic Engineering - How we built our multi-agent research system: https://www.anthropic.com/engineering/built-multi-agent-research-system
- Anthropic Engineering - Effective context engineering for AI agents: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Anthropic Engineering - Scaling Managed Agents: https://www.anthropic.com/engineering/managed-agents
- LangGraph multi-agent docs: https://langchain-ai.github.io/langgraph/tutorials/multi_agent/multi-agent-collaboration/
- LangChain handoffs docs: https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs
- Google ADK multi-agent docs: https://google.github.io/adk-docs/agents/multi-agents/
- Microsoft Agent Framework orchestrations: https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/
- Microsoft Open Source - Conductor deterministic orchestration: https://opensource.microsoft.com/blog/2026/05/14/conductor-deterministic-orchestration-for-multi-agent-ai-workflows/
