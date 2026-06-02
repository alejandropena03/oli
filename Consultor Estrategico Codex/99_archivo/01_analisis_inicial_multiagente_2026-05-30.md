 # Analisis inicial multiagente - Oli

Fecha: 2026-05-30
Preparado por: Codex como consultor estrategico
Uso: este es el primer analisis que debe responder/usar el siguiente chat de Codex cuando Alejandro pregunte por el estado de Oli como sistema multiagente.

## Veredicto corto

Oli esta conceptualmente muy bien internacionalizado contra el estado del arte multiagente: supervisor, suboperadores, permisos, memoria, mission graph, validation, evidence y playbooks estan en el lenguaje correcto de 2026.

Pero todavia no esta "bien desarrollado" como sistema multiagente en sentido productivo, porque esta en papel. La arquitectura es prometedora; la calidad real solo empieza cuando haya traces, evals, costos, errores, retries y resultados de misiones reales.

Mi veredicto:
- Vision multiagente: 8.5/10
- Diseño de orquestacion: 8/10
- Seguridad conceptual: 7.5/10
- Evaluabilidad actual: 5/10
- Producto real: 1/10, porque aun no hay V0 corriendo
- Potencial si se ejecuta bien: muy alto

## Lo que Oli ya tiene bien

1. Oli no se define como "un agente mas".

Esto es correcto. En 2026, la ventaja no esta en decir "tenemos agentes", sino en coordinar agentes, herramientas, memoria y permisos bajo una capa auditable.

2. Usa un patron supervisor/suboperadores.

El repo define suboperadores como:
- MarketResearchSuboperator
- TechnicalArchitectSuboperator
- ExecutionSuboperator
- ValidationSuboperator
- MemoryCuratorSuboperator

Eso encaja con el patron de "manager/orchestrator + specialists". OpenAI Agents SDK lo llama "agents as tools" cuando el manager mantiene control y llama especialistas para subtareas acotadas. Fuente: https://openai.github.io/openai-agents-python/multi_agent/

3. Tiene separacion de responsabilidades.

Cada suboperador tiene prompt y output estructurado. Eso es muy superior a un solo prompt gigante donde un agente intenta investigar, planear, ejecutar, validar y recordar al mismo tiempo.

4. Tiene human-in-the-loop y permisos como parte del core.

Oli entiende que acciones reales necesitan approval gates. Esto esta alineado con LangGraph y con practicas de agentes productivos: interrupts, checkpoints, resume, recovery y trazas.

5. Tiene validacion como suboperador, no como decoracion.

Esto es clave. El validation layer debe evaluar success criteria, no "si suena bien". El repo ya piensa en PASS/FAIL por criterio.

6. Tiene memoria y playbooks como flywheel.

La idea "trabajo repetido se convierte en sistema" es probablemente uno de los mejores pilares de Oli. Si se implementa bien, ahi vive mucho del moat.

## Lo que falta para estar al nivel state of the art

1. Evals antes de mas subagentes.

OpenAI recomienda que la decision de pasar de single-agent a multi-agent la guien evals, porque multiagente agrega no determinismo y complejidad. Fuente: https://platform.openai.com/docs/guides/evaluation-best-practices

Para Oli esto significa:
- No crear subagentes porque "suena pro".
- Crear subagentes solo cuando mejoren una metrica.
- Medir: calidad, costo, latencia, tool selection, handoff accuracy, factualidad, cumplimiento de permisos y tasa de reparacion.

2. Trace-based assurance.

El research 2026 sobre agentes insiste en que los fallos no son solo outputs incorrectos: tambien hay loops, role drift, propagacion de claims no soportados, fallos de herramientas y efectos externos. Fuente: https://arxiv.org/abs/2603.18096

Oli necesita desde V0:
- Message-action traces.
- Contratos por step.
- Replay deterministico cuando se pueda.
- Primer paso violado localizado.
- Fault injection basico: tool falla, memoria incompleta, browser no responde, API rate limit.

3. Tool guardrails, no solo agent guardrails.

OpenAI documenta que los guardrails de input/output no cubren todos los puntos en workflows con managers, handoffs o especialistas; para proteger tool calls se necesitan tool guardrails. Fuente: https://openai.github.io/openai-agents-python/guardrails/

Para Oli:
- Cada tool debe tener politica: quien puede llamarla, con que datos, bajo que permiso, con que redaction, con que rollback.
- Email, Slack, GitHub push, filesystem delete, deploy y pagos deben ser clase alta.

4. Economia de tokens y latencia.

Anthropic reporto que su sistema multiagente de research supero a un agente unico en tareas breadth-first, pero tambien que consume muchos mas tokens: agentes suelen usar aprox. 4x vs chat y multiagente aprox. 15x vs chat. Fuente: https://www.anthropic.com/engineering/multi-agent-research-system

Para Oli:
- Multiagente debe usarse cuando la mision vale el costo.
- Research complejo: si.
- Tareas lineales o pequeñas: no necesariamente.
- Coding con dependencias estrechas: cuidado, porque Anthropic tambien advierte que muchos coding tasks no son tan paralelizables.

5. Definir cuando NO usar multiagente.

Este punto es central.

Regla propuesta:
- Single agent + tools: tareas cortas, lineales, con bajo riesgo.
- Supervisor + specialists: tareas con fases claras y criterios distintos.
- Parallel subagents: research breadth-first, comparativas, auditorias, exploracion independiente.
- Handoff/swarm: solo cuando el siguiente paso depende mucho del resultado intermedio y se acepta menor predictibilidad.
- Code orchestration deterministico: permisos, billing, estado, retries, colas, contratos.

## State of the art aplicado a Oli

Estado del arte 2026, sintetizado:

1. Orquestacion explicita sobre autonomia libre.

Los sistemas fuertes no dejan a "un enjambre" improvisar todo. Usan grafo, supervisor, contratos, checkpoints y politicas.

2. Especialistas pequenos, no personajes.

Un buen subagente no es "el genio de marketing". Es una funcion operacional con input/output y success criteria.

3. Evaluacion por frontera de decision.

No basta evaluar el resultado final. Hay que evaluar:
- Interpretacion de intent.
- Recuperacion de contexto.
- Seleccion de herramienta.
- Argumentos de tool call.
- Handoff correcto.
- Cumplimiento de permisos.
- Reparacion correcta.
- Factualidad con fuentes.

4. Memoria con gobernanza.

Memoria sin control se vuelve contaminacion. Oli acierta al tener MemoryCurator. Hay que reforzarlo:
- Hecho vs inferencia.
- Confianza.
- TTL o revision.
- Fuente.
- Usuario puede editar/borrar.

5. Observabilidad como producto, no solo devtool.

Para Oli, audit trail no es log interno. Es parte del valor percibido: "mira lo que hice, por que, con que costo y que evidencia".

6. Human approval solo en puntos de impacto.

Demasiadas aprobaciones destruyen el producto. Muy pocas destruyen confianza. La clave es clase de permiso + reversibilidad + coste de error.

## Diagnostico honesto sobre Oli

Oli esta haciendo las preguntas correctas. Eso no es menor.

La arquitectura actual se parece mas a un producto serio que a la mayoria de demos de agentes:
- Tiene constitucion.
- Tiene mission kernel.
- Tiene state machine.
- Tiene permisos.
- Tiene suboperadores.
- Tiene validation.
- Tiene memory curator.
- Tiene playbook engine.
- Tiene pricing pensado por uso/costo.

El problema: aun no sabemos si funciona.

La pregunta correcta ya no es "esta bien diseñado?".
La pregunta correcta es:

"Cual es la mision minima que prueba que Oli convierte intencion en trabajo terminado, validado, auditable y repetible?"

Mi respuesta:

V0 debe probar solo una mission-class:
- Research brief verificable, o
- Reporte operativo semanal, o
- Automatizacion simple de ventas con stubs.

Yo elegiria `research-brief-v1` porque:
- Es naturalmente breadth-first.
- Justifica multiagente.
- Requiere fuentes.
- Permite validation.
- Permite evidence.
- Es vendible a founders/agencias.
- Puede correr sin permisos peligrosos.

## Best practices que Oli deberia seguir desde V0

1. Empezar con un grafo pequeno.

Propuesta V0:
- intake
- interpret_intent
- retrieve_context
- plan
- execute_research
- synthesize
- validate
- deliver
- update_memory_suggestions

2. Crear evals antes de crear mas tools.

Primer set:
- 20 prompts de research brief.
- 5 con informacion ambigua.
- 5 con datos temporales que requieren web.
- 5 con fuentes contradictorias.
- 5 con restricciones de formato/tono.

3. Mantener outputs estructurados.

Cada suboperador debe devolver JSON/schema validable, no prosa libre.

4. Guardar cada mision como trace.

Cada mision debe generar:
- input original
- intent interpretado
- contexto recuperado
- plan
- tool calls
- sources
- outputs intermedios
- validation report
- final deliverable
- costo
- memoria sugerida

5. Separar "trabajo" de "presentacion".

El subagente de research no debe escribir el reporte final. Produce hallazgos. El synthesizer/report writer arma el output.

6. No permitir que subagentes hablen con el usuario por defecto.

El Orchestrator debe ser la voz unica, salvo handoff explicito. Esto conserva tono, permisos y responsabilidad.

7. Cerrar loops.

Toda mision necesita limites:
- max steps
- max retries
- max cost
- max elapsed time
- stop conditions
- escalation condition

8. Medir costo por mision desde el dia 1.

Pricing V6 depende de que el routing real no destruya margen. Sin telemetria, el pricing es una hipotesis bonita.

9. Preferir herramientas pocas y confiables.

V0 deberia limitarse a:
- filesystem/read repo
- web search/fetch
- shell controlado
- Postgres/pgvector cuando exista
- browser basico solo si el use case lo exige

10. Convertir repeticion en playbook.

Cuando una mision se repite 3 veces con estructura similar:
- sugerir playbook
- versionarlo
- medir mejora contra ejecucion manual

## Recomendacion estrategica

Estamos desarrollando esto de la mejor forma en filosofia y arquitectura. Todavia no en ejecucion.

La mejor forma ahora es dejar de expandir la vision y construir un loop minimo medible:

1. Mission Kernel minimo.
2. Research brief playbook.
3. Trace completo.
4. Validation report.
5. Cost report.
6. Memory suggestions.
7. 20 evals.

Si eso funciona, Oli deja de ser una tesis excelente y empieza a ser un producto.

## Fuentes usadas

- Anthropic, "How we built our multi-agent research system", 2025: https://www.anthropic.com/engineering/multi-agent-research-system
- OpenAI Agents SDK, "Agent orchestration": https://openai.github.io/openai-agents-python/multi_agent/
- OpenAI Agents SDK, "Guardrails": https://openai.github.io/openai-agents-python/guardrails/
- OpenAI, "Evaluation best practices": https://platform.openai.com/docs/guides/evaluation-best-practices
- LangGraph TypeScript Guide, "How to Build Multi-Agent Systems", last reviewed 2026-04-07: https://langgraphjs.guide/multi-agent/
- arXiv 2601.13671, "The Orchestration of Multi-Agent Systems", 2026-01-20: https://arxiv.org/abs/2601.13671
- arXiv 2603.18096, "A Trace-Based Assurance Framework for Agentic AI Orchestration", 2026-03-18: https://arxiv.org/abs/2603.18096
- arXiv 2601.01743, "AI Agent Systems: Architectures, Applications, and Evaluation", 2026-01-05: https://arxiv.org/abs/2601.01743
