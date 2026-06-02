# Revision orquestada por subagentes - Oli

Fecha: 2026-05-30
Autor/orquestador: Codex
Scope: analisis de estado, ICP, arquitectura, diferenciacion y direccion visual. No modifica archivos de producto.

## Veredicto ejecutivo

Oli tiene una base V0.3 real y defendible, pero todavia no es producto. El repo ya contiene una tesis fuerte: de intencion a trabajo terminado, con permisos, evidencia, validacion, memoria y playbooks. Lo construido demuestra el Mission Kernel y un primer LangGraph, pero falta la columna vertebral: Postgres real, PostgresSaver, memoria con pgvector, HITL durable, seguridad de herramientas y evals.

El pitch anterior que hablaba de "empresas SaaS con agentes" no sirve porque aplana el ICP. El repo define un paraguas mas amplio, pero el wedge comercial real para pilotos pagados es:

> Agencias/consultoras y equipos pequenos founder-led que repiten entregables digitales por cliente o por operacion interna, sufren presion de margen y necesitan convertir trabajo recurrente en misiones auditables y playbooks.

Founders/builders siguen siendo proving ground. Agencias, consultoras y teams pequenos son donde el negocio se endurece.

## Hallazgos por subagente

### 1. ICP / GTM

El ICP paraguas segun repo:

- Personas o equipos con alto volumen de trabajo digital.
- Contexto fragmentado.
- Necesidad de convertir intencion en entregables terminados.

ICP prioritario documentado:

- Founders y equipos pequenos de empresas AI-first / tech-enabled.

Lectura critica:

- El ICP "oficial" sigue amplio.
- El ranking comercial favorece agencias/consultoras por ROI claro, repeticion y margen.
- La mision `weekly-client-report-v1` ya apunta a "agencias y teams".

Recomendacion:

- Pitch y demo principal deben enfocarse en reportes semanales auditados, research verificable y outreach draft con approval.
- No vender "Oli hace todo".
- Vender "Oli convierte trabajo recurrente de cliente en misiones ejecutables, auditables y reutilizables".

### 2. Arquitectura / state-of-the-art

Bien orientado:

- LangGraph es la decision correcta para workflows stateful.
- Postgres + pgvector como una sola base para estado y memoria sigue siendo fuerte.
- Mission Kernel, permisos, evidencia y acceptance tests son buena base.
- OpenAI-compatible adapter prepara camino a vLLM, Ollama y proveedores compatibles.

Gaps criticos:

- No hay checkpointing durable real: solo MemorySaver.
- No hay human-in-the-loop durable dentro de LangGraph.
- No existe memoria/RAG real.
- SQLAlchemy existe, pero no hay Postgres corriendo, migraciones, audit tables ni pgvector.
- Model Router es estatico, no registry/benchmark-driven.
- No hay evals operacionales ni adversariales.
- Seguridad de tools esta en ADRs, no en codigo.

State-of-the-art pendiente:

- Actualizar canon de Postgres 16 a Postgres 18 recomendado, compatible con 16+.
- Resolver contradiccion pgvector V0 vs V1.
- Planear `psycopg` v3/pooling/migraciones para produccion futura.
- Antes de fine-tuning: recolectar misiones, replay y evals.

### 3. Innovacion / diferenciacion

Tesis:

> Oli no gana por ser otro agente. Gana por ser un operador con memoria, comprobantes y playbooks para trabajo digital repetido.

Innovaciones de mayor leverage:

1. Comprobante de mision.
2. Mission Black Box / replay basico.
3. Validacion por criterios de exito.
4. Reporte semanal auditado para cliente.
5. Memoria por cliente/proyecto.
6. Playbook candidate automatico.
7. Approval gates por impacto.
8. Cost-quality routing visible.
9. After Action Review operativo.
10. Evidence Drawer por entregable.
11. Handoff listo para cliente.
12. Comparacion entre runs.

Riesgo principal:

- La vision "execution OS" es enorme. V0 se puede diluir si no se enfoca en una mission-class vendible.

### 4. Direccion visual / presentacion

Principios visuales:

- Caja de cristal ejecutiva: rutas, costos, permisos y evidencia visibles.
- TechLuxe operativo: void, graphite, plata, porcelana y cyan electrico.
- Slash como sistema: comando, separador, cursor y progreso.
- Una slide, una idea dominante.
- No SaaS generico, no gradiente morado, no robot, no consola hacker.

Componentes recomendados:

- Ruta propuesta.
- Comprobante de ejecucion.
- Mission timeline.
- Permission matrix.
- Cost router.
- Evidence drawer.
- Executive metric tiles.

## Plan de revision al 30 de mayo de 2026

### Decision 1: ICP y wedge

Decision recomendada:

- Wedge comercial: agencias/consultoras y teams pequenos.
- Proving ground: founder/builder.
- Mision demo principal: weekly client report auditado.

### Decision 2: Estado tecnico

Estado:

- V0.3 tecnico.
- 45 tests passing.
- No producto todavia.

Bloqueo:

- Postgres real no corre en este equipo por permisos admin.

### Decision 3: State-of-the-art

Actualizar TDD:

- PostgreSQL 18 recomendado.
- Compatibilidad PostgreSQL 16+.
- pgvector desde V0 si memoria es parte del moat.

### Decision 4: Proximo build cuando haya DB

1. Postgres 18.
2. Migraciones.
3. PostgresSaver.
4. HITL durable.
5. Memory entries + pgvector.
6. Security/tool audit stub.
7. Evals/replay.

### Decision 5: Que no construir aun

- UI grande.
- Multi-user completo.
- Marketplace MCP abierto.
- Fine-tuning.
- Kubernetes/Ray.
- Temporal.

## Pitch corregido de 1 minuto

Oli no es otro chatbot ni un dashboard mas. Oli es un operador de ejecucion para agencias, consultoras y equipos pequenos que repiten trabajo digital valioso entre clientes, herramientas y entregables.

Le dices el resultado: prepara el reporte semanal del cliente, convierte estas notas en propuesta, investiga estos competidores o arma un draft de outreach. Oli entiende la mision, recupera contexto, arma un plan, clasifica permisos, ejecuta, valida el entregable y deja un comprobante: que hizo, con que datos, cuanto costo, que asumio y que requiere aprobacion humana.

La diferencia es que Oli aprende del trabajo real. Si haces el mismo reporte varias veces, no lo trata como tarea manual eterna: lo propone como playbook. Si corriges el tono de un cliente, lo recuerda. Si hay impacto externo, pide aprobacion. Si algo falla, queda trazado.

Los dashboards muestran informacion. Los CRMs guardan registros. Los chatbots responden. Oli termina trabajo, deja evidencia y mejora el siguiente run.
