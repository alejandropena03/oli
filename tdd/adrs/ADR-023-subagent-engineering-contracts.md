# ADR-023 - Subagent Engineering Contracts

**Estado:** accepted
**Fecha:** 2026-05-31
**Deciders:** Alejandro Pena (founder)

---

## Contexto

Oli promete convertir intencion humana en trabajo digital terminado, validado y auditable.

El TDD ya define suboperadores internos, Mission Kernel, validation, memory, playbooks, Model Router y Mission Black Box. Pero falta una decision mas precisa: cuando una mision debe ser ejecutada por un solo agente, cuando merece especialistas, que contexto recibe cada especialista, que devuelve, como se valida y como se registra.

El riesgo es adoptar "multi-agent" como estetica: varios agentes conversando, mucho texto, mas costo, mas latencia y menos claridad.

El state of the art revisado converge en otra direccion:

- OpenAI Agents SDK distingue `agents as tools` y `handoffs`.
- Anthropic enfatiza context isolation, parallel execution, specialization y context engineering.
- LangGraph/LangChain ponen el foco en supervisor, handoffs, subgraphs, state updates y contexto por agente.
- Google ADK documenta coordinator, sequential pipeline, parallel fan-out, hierarchical decomposition, critique/review y HITL.
- Microsoft Agent Framework/Conductor empuja workflows deterministas y topology control para sistemas multi-agent.

La conclusion: el centro no son los agentes. El centro es el contrato de trabajo, el paquete de contexto, la topologia y la validacion.

---

## Decision

Oli adopta **subagent engineering contractual**, no multi-agent por defecto.

Un subagente solo existe si tiene:

- objetivo propio;
- contexto propio;
- tools o restricciones propias;
- output schema propio;
- validator propio o validation hook;
- razon medible para existir.

La razon medible debe mejorar al menos una:

- calidad;
- seguridad;
- latencia;
- costo.

Por defecto, Oli usa:

```text
single orchestrator + tools
```

Solo sube complejidad cuando la mission class lo justifica:

```text
Upgrade 1: manager + specialists-as-tools
Upgrade 2: deterministic workflow + evaluator loops
Upgrade 3: parallel fan-out/gather for research
Upgrade 4: hierarchical multi-agent for long-horizon missions
```

Handoffs user-facing no son el default. Se permiten solo cuando un especialista debe hablar directamente con el usuario y el cambio de modo esta justificado.

---

## Canonical Contracts

Oli define estos contratos como capa formal entre Mission Kernel, Orchestrator, Model Router, LangGraph, validators y Mission Black Box:

1. `MissionClass`
2. `AgentTaskContract`
3. `ContextPacket`
4. `AgentTaskResult`
5. `ValidatorContract`
6. `ValidationReport`
7. `TopologySelectorInput`
8. `TopologyDecision`

Estos contratos se especifican en:

- `tdd/domain/subagent-engineering.md`
- `tdd/schemas/subagent_contracts.ts`

---

## Topologies Allowed

Oli permite estas topologias:

| Topology | Uso |
|---|---|
| `single_agent_with_tools` | Tareas simples, bajo riesgo, baja ambiguedad. |
| `manager_with_specialists_as_tools` | Oli mantiene una sola voz y llama especialistas internos. |
| `sequential_pipeline` | Cada paso depende del anterior y puede validarse. |
| `parallel_fanout_gather` | Subtareas independientes, research amplio, comparaciones. |
| `generator_validator` | Outputs importantes que requieren critica/verificacion independiente. |
| `hierarchical_decomposition` | Misiones largas con multiples workstreams. No V0 por defecto. |
| `handoff_user_facing` | Especialista conversa con usuario. Uso restringido. |

---

## Consequences

### Positive

- Evita teatro multi-agent.
- Hace auditable cada delegacion.
- Permite comparar topologias contra baseline single-agent.
- Conecta naturalmente con LangGraph, Model Router, evals y Mission Black Box.
- Permite context isolation y menor exposure de datos.
- Prepara datos limpios para future fine-tuning/post-training.

### Negative

- Mas diseno antes de implementar.
- Mas schemas y metadata.
- Requiere evals antes de justificar multi-agent.
- Puede parecer lento al inicio, pero reduce deuda arquitectonica.

---

## Acceptance Criteria

Esta ADR se considera aplicada cuando:

1. Existe `tdd/domain/subagent-engineering.md`.
2. Existe `tdd/schemas/subagent_contracts.ts`.
3. Existe `tdd/domain/subagent-evals.md`.
4. Una mission class puede declarar su default topology.
5. Cada subtask puede representarse como `AgentTaskContract`.
6. Cada subagente recibe un `ContextPacket`, no contexto libre.
7. Cada output parcial vuelve como `AgentTaskResult`.
8. Cada output critico puede validarse con `ValidatorContract`.
9. Mission Black Box puede registrar context packets, task contracts, results, validation reports, topology decisions y model routing decisions.
10. No se acepta una topologia multi-agent si no supera baseline single-agent en al menos una metrica importante sin degradar seguridad/costo de forma inaceptable.

---

## References

- `Consultor Estrategico Codex/16_subagent_engineering_state_of_art_2026-05-31.md`
- `tdd/domain/subagent-engineering.md`
- `tdd/domain/subagent-evals.md`
- OpenAI Agents SDK: https://openai.github.io/openai-agents-js/guides/multi-agent/
- OpenAI Agents SDK Handoffs: https://openai.github.io/openai-agents-python/handoffs/
- OpenAI Evaluation Best Practices: https://platform.openai.com/docs/guides/evaluation-best-practices
- Anthropic Engineering - Multi-agent research system: https://www.anthropic.com/engineering/built-multi-agent-research-system
- Anthropic Engineering - Context engineering: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- LangGraph multi-agent docs: https://langchain-ai.github.io/langgraph/tutorials/multi_agent/multi-agent-collaboration/
- Google ADK multi-agent docs: https://google.github.io/adk-docs/agents/multi-agents/
- Microsoft Agent Framework orchestrations: https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/

