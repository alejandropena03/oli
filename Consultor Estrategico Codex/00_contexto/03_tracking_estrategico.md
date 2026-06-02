# Tracking estrategico Codex - Oli

Fecha inicial: 2026-05-30

## Estado actual

Oli ya no esta solo en pre-build documental. Existe un V0 tecnico ejecutable en modo desarrollo:
- Mission Kernel minimo.
- API FastAPI.
- Misiones `research-brief`, `draft-outreach`, `weekly-client-report`.
- Permisos y approval gate.
- Evidencia/eventos/reportes.
- Persistencia JSON local y SQLAlchemy opcional.
- LangGraph con MemorySaver en desarrollo.
- Adaptadores de modelo: development, Ollama, OpenAI-compatible, webhook, fallback.
- OpenRouter configurado con `openrouter/owl-alpha` y prueba real exitosa.
- Suite actual: `py -m pytest` -> 45 passed.

## Decisiones/observaciones registradas

1. Codex queda como consultor estrategico en este workspace.
2. Codex puede leer todo el repo, pero solo escribe dentro de `Consultor Estrategico Codex` salvo instruccion explicita.
3. Claude Code ya hizo push por git SSH local a `git@github.com:apenaosorio_meli/oli.git`.
4. El conector MCP de GitHub de Codex no ve el repo por permisos/Enterprise/SSO, pero git local por SSH funciona con permisos elevados.
5. Skills instaladas para futuras sesiones:
   - define-goal
   - pdf
   - security-best-practices
   - security-threat-model
   - notion-research-documentation
6. Alejandro dio luz verde para empezar desarrollo, con restriccion de que Codex puede leer todo el repo pero solo escribir dentro de `Consultor Estrategico Codex` por ahora.
7. Codex confirma que el repo define como primer desarrollo canonico el Build V0: Mission Kernel, empezando por `pyproject.toml`, `packages/mission_kernel/`, `packages/orchestrator/`, `apps/api/` y `tests/test_slice_001.py`.
8. Codex recomienda que el primer commit real sea aun mas pequeno: `pyproject.toml`, `mission_state.py`, `state_machine.py`, `policies.py` y `tests/test_mission_kernel.py`.
9. Alejandro autorizo ejecutar el inicio de V0. Codex creo el primer Mission Kernel en Python, un orquestador mock para `research-brief-v1` y tests de kernel + slice-001.
10. Verificacion inicial: `py -m pytest` paso con 7 tests. Se desactivo el cache de pytest en `pyproject.toml` para evitar warnings de escritura de `.pytest_cache` en este entorno.
11. Codex amplio V0 con API minima FastAPI:
   - `apps/api/main.py`
   - `apps/api/missions.py`
   - `POST /missions/research-brief`
   - `GET /missions/{mission_id}`
   - `GET /health`
12. FastAPI fue instalado en el entorno local del usuario con `py -m pip install fastapi`.
13. Verificacion despues de API: `py -m pytest` paso con 9 tests.
14. Se intento levantar `uvicorn apps.api.main:app --host 127.0.0.1 --port 8000`; el proceso fue interrumpido manualmente por Alejandro antes de cerrar la verificacion del servidor. Retomar despues comprobando si hay proceso vivo o puerto ocupado.
15. Alejandro intento correr uvicorn desde `C:\windows\system32` y fallo con `ModuleNotFoundError: No module named 'apps'`. Causa: Python no tenia el repo en el import path porque el comando no se ejecuto desde la raiz de `oli`.
16. Codex verifico que usando `--app-dir C:\Users\apenaosorio\Desktop\oli` la app importa correctamente. El puerto 8000 ya estaba ocupado por un servidor vivo.
17. Verificacion API viva:
   - `GET http://127.0.0.1:8000/health` respondio `{"status":"ok"}`.
   - `POST http://127.0.0.1:8000/missions/research-brief` respondio una mision `completed`, goal `competitor_research_brief`, `playbook_candidate=True`.
18. Codex agrego `scripts/run_api.ps1` para lanzar la API desde cualquier carpeta sin depender del working directory.
19. Se agrego pantalla raiz `/` para ejecutar una mision desde navegador, pero no se considera producto final.
20. Se agrego persistencia local JSON en `runtime/missions.json`.
21. Se agregaron endpoints de eventos, evidencia, reporte, approval y reject.
22. Se agrego `draft-outreach` para probar permission class 3 y human approval.
23. Se agrego `weekly-client-report-v1`, mision orientada al ICP elegido: agencias y teams.
24. Se agrego `test_v0_acceptance.py` como contrato vivo de V0.
25. Se agrego `.env.example`, loader de `.env.local`, configurador GUI de OpenRouter y model router status.
26. Se probo OpenRouter con `openrouter/owl-alpha`; respuesta: `oli_openrouter_ok`.
27. Se probo `weekly-client-report` con modelo real via OpenRouter; resultado completed, validation true, provider usado `openai_compatible`.
28. Se implemento LangGraph minimo siguiendo `tdd/domain/langgraph-mission-graph.md` y `ADR-010`:
   - `packages/orchestrator/nodes.py`
   - `packages/orchestrator/mission_graph.py`
   - `packages/orchestrator/router.py`
   - `POST /missions/weekly-client-report` ahora usa `run_weekly_client_report_graph_v1`.
29. Se agregaron tests especificos de LangGraph:
   - `tests/test_langgraph_mission_graph.py`
   - Valida que el grafo compile, ejecute y preserve el flujo de estados del TDD.
30. Verificacion despues de LangGraph: `py -m pytest` -> 37 passed.
31. Se implemento Model Router minimo segun ADR-016:
   - `packages/model_router/router.py`
   - `TaskType`
   - `ModelRole`
   - `PrivacyMode`
   - `RoutingTier`
   - `RoutingDecision`
   - `ModelRouter`
32. El nodo LangGraph de reporte ahora registra evidencia `model_routing` para que la decision de modelo quede auditada por mision.
33. Se resolvio un ciclo de imports entre `model_router` y `orchestrator` moviendo imports de adaptadores a carga lazy.
34. Verificacion despues de Model Router: `py -m pytest` -> 42 passed.
35. Se implemento persistencia SQLAlchemy compatible con la interfaz actual:
   - `packages/mission_store/sqlalchemy_store.py`
   - `packages/mission_store/factory.py`
   - `.env.example` documenta `OLI_MISSION_STORE` y `OLI_DATABASE_URL`.
36. Se agregaron dependencias canonicas del TDD para persistencia:
   - `sqlalchemy`
   - `psycopg2-binary`
37. Se agrego `MemorySaver` de LangGraph en desarrollo para preparar checkpointing.
38. Se corrigio el estado del grafo para no guardar objetos no serializables como adapters de modelo. Esto es requisito real para checkpoints.
39. Verificacion despues de SQLAlchemy + MemorySaver: `py -m pytest` -> 45 passed.
40. Se intento instalar PostgreSQL local via `winget`:
   - `docker` no estaba instalado.
   - `psql` no estaba instalado.
   - `winget` si estaba disponible.
   - `winget search PostgreSQL` mostro paquetes oficiales PostgreSQL 16, 17 y 18.
   - Codex eligio PostgreSQL 16 por alineacion literal con el TDD, pero Alejandro corrigio que para state-of-the-art debio proponerse PostgreSQL 18 como opcion principal.
   - `winget install --id PostgreSQL.PostgreSQL.16` descargo el instalador oficial, pero la instalacion fue cancelada/bloqueada por permisos de administrador del PC corporativo.
41. Decision de cierre de sesion:
   - No seguir desarrollando features hasta resolver la base de datos local/remota.
   - Registrar que Postgres local en este computador no quedo instalado.
   - Recomendacion futura: usar PostgreSQL 18 si se prioriza state-of-the-art; mantener compatibilidad SQLAlchemy para Postgres 16+ si se prioriza TDD estricto.
42. Incidente 2026-05-31:
   - Alejandro detecto que un chat nuevo de Codex arranco sin contexto automatico suficiente.
   - Causa raiz: existia memoria en `Consultor Estrategico Codex`, pero no habia un `AGENTS.md` fuerte desde el inicio de la sesion.
   - Impacto: otro Codex construyo V0 antes de que este consultor validara el proceso completo.
   - Mitigacion: se creo `AGENTS.md` y luego se endurecio con startup protocol obligatorio.
43. Auditoria post-incidente:
   - Archivo: `12_auditoria_v0_post_incidente_2026-05-31.md`.
   - Resultado tecnico: `py -m pytest` -> 45 passed.
   - Veredicto: V0.3 es defendible como base de desarrollo, no producto final.
   - Decision: congelar features nuevas hasta resolver Postgres/PostgresSaver/evals/guardrails.
44. Analisis de prompt engineering para Codex:
   - Archivo: `13_prompt_engineering_codex_ux_2026-05-31.md`.
   - Decision: mejorar UX de Codex con boot minimo obligatorio, carga condicional por tema, modos de trabajo y formatos de respuesta.
   - `AGENTS.md` actualizado para reducir friccion y reforzar que Codex es consultor/auditor por defecto.
45. Direccion runtime/modelos locales:
   - Alejandro aclaro que la vision no es simplemente "Oli cloud sin terminal del usuario".
   - La vision correcta a revisar/canonizar es: cada usuario percibe una instancia Oli propia, con compute/runtime asignado segun tier, normalmente en infraestructura gestionada o aprovisionada por Oli, conectable por SSH/terminal Linux y capaz de actuar como extension operacional del entorno digital del usuario.
   - Esa instancia puede correr modelos open-source detras; para el usuario el producto sigue siendo Oli, no "un modelo".
   - Implicacion: Ollama no debe ser runtime canonico si se busca excelencia/produccion; puede quedar para dev/local simple. vLLM debe evaluarse como runtime principal para serving gestionado de modelos open-weight.
   - El TDD hoy mezcla local-first, managed/on-demand y presencia local. Pendiente: crear o actualizar una ADR que defina con precision los modos: managed user runtime, local/on-prem/power-user, desktop bridge, customer cloud.
46. Pendiente estrategico: farming/onboarding de uso en Oli.
   - Alejandro quiere revisar como Oli debe maximizar adopcion progresiva en la vida/trabajo del usuario desde el onboarding.
   - Concepto: Oli no solo conecta herramientas; detecta oportunidades de automatizacion/simple leverage, sugiere habitos AI-first, incrementa uso por etapas y convierte tareas simples en misiones/playbooks.
   - Pendiente: decidir si esto entra en la Constitucion como principio de "onboarding/farming responsable" con limites de permiso, valor medible y no-spam/no-dark-pattern.
47. ADR-021 creada:
   - Archivo: `tdd/adrs/ADR-021-dedicated-oli-runtime.md`.
   - Decision: Oli adopta Dedicated Oli Runtime como arquitectura canonica: instancia operacional dedicada por usuario/equipo con memoria, terminal/sandbox, compute asignado, herramientas conectadas, permisos, evidencia y modelos detras de Oli.
   - Esta ADR corrige la ambiguedad entre SaaS puro, local-first y GPU on-demand.
48. Pendiente estrategico: fine-tuning serio.
   - Alejandro quiere analizar un proceso serio de fine-tuning para Oli, no solo como feature comercial sino como demostracion tecnica personal.
   - Pendiente: definir que datos se pueden usar, que tareas justifican fine-tuning vs RAG/prompting/evals, que modelos open-weight convienen, que pipeline muestra excelencia y que riesgos legales/privacidad existen.
49. Pendiente estrategico: posicionamiento profesional AI de Alejandro.
   - Alejandro quiere usar Oli como su primer gran proyecto para aspirar a roles muy bien pagos en AI, incluyendo OpenAI, Anthropic u otras empresas top.
   - Pendiente: analizar que habilidades debe evidenciar el repo para roles tipo LLM developer, AI engineer, agent engineer, automation engineer, infra/model-serving engineer o applied AI product engineer.
50. Documento de skill signal creado:
   - Archivo: `tdd/domain/ai-engineering-skill-signal.md`.
   - Define matriz de skills que Oli debe demostrar: agent orchestration, evals, mission traces, RAG/memoria, model routing, vLLM, fine-tuning, tool security, sandboxing, observability y product judgment.
   - Propone orden: eval harness, mission black box, memory lab, tool security, vLLM adapter, fine-tuning lab, public case studies.
51. ADR-022 creada:
   - Archivo: `tdd/adrs/ADR-022-public-oli-labs.md`.
   - Decision: mantener Oli Core privado y crear una capa publica `Oli Labs` con repos/labs reproducibles y sanitizados para demostrar capacidad tecnica sin regalar el producto.
52. Pendiente estrategico: AI-first transformation research/advisor.
   - Alejandro observa que las AIs actuales no hacen bien el research para volver al usuario mas AI-first ni generan analisis accionables de "como puedo hacer esto yo".
   - Oli debe poder analizar el trabajo/vida digital del usuario y proponer rutas concretas para delegar, automatizar, conectar herramientas, crear playbooks y mejorar habitos AI-first.
   - Pendiente: definir mission-class o modulo de "AI-first audit" con recomendaciones priorizadas, ROI, dificultad, permisos y primeros pasos.
53. Pendiente estrategico: subagent engineering como ventaja.
   - Alejandro observa que ni Claude Code usa subagentes de forma realmente optimizada en tareas complejas.
   - Oli debe aprender a dividir tareas complejas en subagentes/subtareas con paquetes de contexto, outputs esperados, validadores, merge strategy y presupuesto.
   - Pendiente: crear especificacion de Agent Task Contract, Context Packet, Scheduler, Validator y Synthesizer para maximizar output sin teatro multiagente.
54. Pendiente estrategico: state-of-the-art discovery y recomendaciones no flojas.
   - Oli no debe recomendar solo lo conocido o promedio; debe buscar state-of-the-art aplicable, validar si el usuario/Oli lo puede construir, explicar tradeoffs y proponer herramientas AI-first que aumenten autonomia.
   - Ejemplo: si el usuario quiere una web, Oli no solo genera codigo; guia dominio, DNS, Cloudflare, deploy, analytics, email, CI, costos, seguridad y trucos de developer cuando hagan sentido.
   - Pendiente: definir protocolo de research actual, ranking de opciones, buildability check, cost/sustainability check y decision memo por recomendacion.
55. Pendiente estrategico: Oli como cloud/service broker responsable.
   - Como Oli tambien podria operar infraestructura para el usuario, debe recomendar/provisionar servicios cloud cuando sea eficiente y sostenible.
   - Ejemplo: para n8n puede proponer un servidor pequeno dedicado si sale mejor que pagar suscripcion; no debe usar la GPU del usuario/runtime para cargas baratas si afecta sostenibilidad.
   - Pendiente: definir catalogo de servicios gestionables, reglas de costo/margen/sostenibilidad, limites de soporte, provisioning playbooks y evidence/cost report para que el usuario no necesite saber infraestructura.
56. Cierre de sesion 2026-05-31:
   - Archivo: `14_cierre_sesion_2026-05-31_fine_tuning_next.md`.
   - Correccion: Codex repitio el tema de carrera/posicionamiento cuando ya estaba documentado. No repetir en la siguiente sesion.
   - Proximo tema: fine-tuning serio para Oli.
   - Punto de partida: decidir que tareas justifican fine-tuning, que queda en RAG/prompting/evals/router, que dataset se puede construir y como mostrarlo en Oli Labs.
57. Analisis de fine-tuning serio creado:
   - Archivo: `15_fine_tuning_serio_oli_2026-05-31.md`.
   - Correccion posterior de Alejandro: no reducir fine-tuning a Oli Labs. Analizarlo para todo el TDD/Core y luego decidir que se muestra publicamente.
   - Veredicto: fine-tuning no debe usarse para conocimiento privado cambiante ni personalidad generica de Oli.
   - Uso correcto: conducta operacional repetible y medible, costo/latencia, aprendizaje privado del sistema conectado a traces/evals/playbooks/router/solution bank, y demostracion publica seria de post-training.
   - Primer lab publico recomendado: `Permission Policy Adapter`, un fine-tune LoRA/QLoRA para clasificar y explicar riesgo/permisos de acciones digitales.
   - Stack recomendado: Unsloth para primer LoRA/QLoRA, Hugging Face TRL al madurar SFT/DPO/GRPO, vLLM para serving de LoRA adapters con API compatible OpenAI.
   - Regla: no entrenar antes de tener baseline/evals/dataset versionado.
58. Analisis state-of-the-art de subagent engineering creado:
   - Archivo: `16_subagent_engineering_state_of_art_2026-05-31.md`.
   - Fuentes revisadas: OpenAI Agents SDK, OpenAI evals, Anthropic multi-agent research/context engineering/managed agents, LangGraph/LangChain, Google ADK, Microsoft Agent Framework/Conductor y papers 2026.
   - Veredicto: Oli no debe adoptar multi-agent por defecto; debe adoptar subagent engineering medible.
   - Criterio: un subagente solo existe si mejora calidad, seguridad, latencia o costo y tiene objetivo, contexto, tools/restricciones, output schema, validator y razon medible.
   - Recomendacion: default single orchestrator + tools; subir a manager + specialists-as-tools; luego workflows deterministas + evaluator loops; parallel fan-out para research; jerarquia solo para misiones largas.
   - Contratos v0 agregados al documento: `Mission Class`, `Agent Task Contract`, `Context Packet`, `Agent Task Result`, `Validator Contract`, `Topology Selector Rules`.
   - Mission class de prueba recomendada: `Founder notes -> Claude Code-ready spec`.
   - Ruta para volverlo TDD formal: crear `ADR-023-subagent-engineering-contracts.md`, `tdd/domain/subagent-engineering.md`, `tdd/schemas/subagent_contracts.ts` y `tdd/domain/subagent-evals.md`.
59. Paquete TDD minimo de subagent engineering creado:
   - `tdd/adrs/ADR-023-subagent-engineering-contracts.md`
   - `tdd/domain/subagent-engineering.md`
   - `tdd/schemas/subagent_contracts.ts`
   - `tdd/domain/subagent-evals.md`
   - Alcance: documental/schema TDD, no runtime product code.
   - Decision canonizada: Oli usa subagent engineering contractual; multi-agent no es default.
   - Cierre de consistencia: `tdd/schemas/index.ts`, `tdd/README.md` y `tdd/adrs/README.md` actualizados para exponer ADR-023 y `subagent_contracts.ts`.
   - Decision de encaje: `suboperator.ts` no se depreca. Queda como interfaz de worker ejecutable; `subagent_contracts.ts` queda como capa superior de contrato/audit/eval. El Orchestrator podra compilar `AgentTaskContract + ContextPacket` a `SuboperatorTask`.
60. Analisis de Model Intelligence y state-of-the-art discovery creado:
   - Archivo: `17_model_intelligence_state_of_art_discovery_2026-05-31.md`.
   - Veredicto: Oli no debe decidir modelos por lista fija; debe tener `Model Intelligence Service` con source connectors, model registry, hardware fit estimator, benchmark runner, tier policy y rollout/rollback.
   - El concepto de `llm-advisor MCP` es correcto como interfaz, pero no como fuente de verdad. La promocion real debe depender de benchmarks propios de Oli en hardware real.
   - Fuentes fuertes: OpenRouter Models API/Rankings, Hugging Face Hub/Eval Results/model cards, Arena/LMArena, Artificial Analysis, model cards/technical reports, vLLM docs, Ollama docs para dev/local.
   - Fuentes secundarias: BenchLM, WhatLLM, LLM Stats, Reddit, blogs comparativos. No deben promocionar modelos por si solas.
   - Decision recomendada: crear `ADR-024-model-intelligence-and-runtime-model-selection.md`, `tdd/domain/model-intelligence.md`, `tdd/schemas/model_registry.ts` y `tdd/domain/model-selection-evals.md`.
61. Analisis macro de state-of-the-art discovery y recomendaciones no flojas creado:
   - Archivo: `18_state_of_art_discovery_recommendations_2026-05-31.md`.
   - Veredicto: Model Intelligence es un subcaso. La capacidad macro debe ser `State-of-the-Art Discovery Engine`.
   - Workflow: DecisionClassifier -> CriteriaBuilder -> SourcePlanner -> EvidenceRetriever -> SourceRanker -> OptionGenerator -> OptionScorer -> BuildabilityChecker -> RiskChecker -> DecisionMemoWriter -> Validator -> Mission Black Box.
   - Regla: Oli recomienda excelencia y luego la aterriza a restricciones; ninguna recomendacion pasa sin buildability/risk checks.
   - TDD recomendado: `ADR-025-state-of-art-discovery-and-decision-memos.md`, `tdd/domain/state-of-art-discovery.md`, `tdd/schemas/decision_memo.ts`, `tdd/domain/state-of-art-evals.md`.
   - Nota: `ADR-024 Model Intelligence` debe colgar como submodulo especializado de ADR-025, no reemplazarlo.
62. Paquete TDD macro de state-of-the-art discovery creado:
   - `tdd/adrs/ADR-025-state-of-art-discovery-and-decision-memos.md`
   - `tdd/domain/state-of-art-discovery.md`
   - `tdd/domain/state-of-art-evals.md`
   - `tdd/schemas/decision_memo.ts`
   - `tdd/schemas/index.ts`, `tdd/README.md` y `tdd/adrs/README.md` actualizados.
   - Decision canonizada: Oli produce `StateOfArtDecisionMemo` con source quality, alternatives, buildability, risk, next action y recheck date.
63. Revision profunda de Hermes Agent creada:
   - Archivo: `19_revision_hermes_agent_nous_2026-05-31.md`.
   - Veredicto: Hermes confirma varias tesis de Oli: dedicated runtime, gateway multicanal, memoria/skills, subagentes aislados, sandboxing, provider routing, cron, MCP/plugins, trajectories y seguridad.
   - Riesgo: Hermes ya ocupa parte del espacio "agent that lives with you and grows"; Oli debe diferenciarse por Mission Kernel, evidence trail, permission classes, decision memos, playbooks por org/cliente, model intelligence y enfoque business/team/agencies.
   - Implicaciones: incorporar como futuras notas TDD `execute_code` vs subagents, filesystem rollback, prompt assembly layers stable/context/volatile, skills-like progressive disclosure con validation, y tool security mas fuerte (SSRF, MCP env filtering, hardline blocklist, credential passthrough allowlist).
64. Analisis de leverage desde OpenRouter Apps y agentes open source creado:
   - Archivo: `20_openrouter_apps_leverage_y_extraccion_open_source_2026-05-31.md`.
   - Se agrego `openrouter_docs.txt` en la raiz del repo con el indice correcto de documentacion de OpenRouter desde `https://openrouter.ai/docs/llms.txt`.
   - Decision: OpenRouter Apps debe usarse como senal de demanda real para priorizar que agentes/repos revisar, no como benchmark de calidad.
   - Mission class propuesta: `open_source_agent_leverage_review`.
   - Regla: no copiar productos; extraer arquitectura, contratos, UX operacional, seguridad, distribucion y eval patterns.
   - Apps/repos priorizados: Hermes, OpenClaw, Kilo Code, OpenCode, referencias cerradas como Claude Code/Cursor/Codex CLI, y herramientas de memoria tipo Pieces.
   - Proximo paso recomendado: hacer dos reviews reales de codigo/docs antes de canonizar `tdd/domain/open-source-leverage.md`.
65. Primer `open_source_agent_leverage_review` completo creado:
   - Archivo: `21_open_source_agent_leverage_review_v1_2026-05-31.md`.
   - Veredicto: la investigacion competitiva anterior fue incompleta; OpenRouter Apps debe ser parte obligatoria del discovery recurrente.
   - Analizados: Claude Agent SDK, Claude Managed Agents, OpenCode, Kilo Code, Hermes y OpenClaw.
   - Decision: usar Claude Agent SDK como delegate premium; OpenCode como benchmark/local delegate candidato; Kilo como benchmark de workflow dev/team; Hermes como benchmark de runtime/skills/security; OpenClaw como benchmark de channel gateway con riesgo alto.
   - Estimacion de ahorro: 50-70% en coding delegate premium con Claude Agent SDK; 25-40% en local coding tool loop con OpenCode patterns; 30-40% en channel gateway con OpenClaw patterns; 20-35% en runtime/skills/security design con Hermes/Kilo/OpenRouter.
   - TDD validation: encaja con ADR-001, ADR-016, ADR-019, ADR-020, ADR-021, ADR-023 y ADR-025. ADR-020 debe endurecerse con SSRF, gateway auth, egress policy, env filtering, plugin signing/trust y supply-chain checks.
   - Siguiente spike recomendado: comparar `Claude Agent SDK delegate` vs `OpenCode-like local delegate` en una tarea de repo pequena con patch, tests, evidence y Mission Black Box.
66. Probe v0 de State-of-the-Art Discovery creado:
   - Archivo: `22_state_of_art_discovery_probe_v0_2026-05-31.md`.
   - Veredicto: el problema no fue solo no conocer Hermes; el discovery aun no existe como sistema medible.
   - Herramientas probadas: OpenRouter docs index local, OpenRouter Apps via web, App Attribution docs, GitHub repo metadata parcial, `rg` contra TDD local.
   - Resultado: OpenRouter Apps funciona como senal de uso; GitHub API requiere conector mas robusto; TDD local necesita retrieval formal; ADR-013 OpenClaw esta bloqueado por permisos.
   - Se definieron contratos minimos: `SourceConnector`, `EvidenceRecord`, `DiscoveryRun`.
   - Evals propuestos: agent usage discovery, coding delegate choice, agent security risk.
   - Decision: no canonizar mas TDD hasta crear un harness minimo `state_of_art_discovery_probe_v0` que produzca evidence records, decision memo, sources_failed y recheck_date.

## Riesgos principales

1. Pre-build paralysis: demasiada documentacion antes de producto real.
2. Multiagente como complejidad prematura.
3. ICP amplio.
4. Surface area tecnica demasiado grande para V0.
5. Pricing sensible al routing real y costo por mision.
6. Memoria sin gobernanza podria volverse ruido o riesgo de privacidad.

## Recomendacion actual de Codex

No saltar a V1 todavia.

LangGraph minimo, Model Router minimo y SQLAlchemy store ya entraron. La siguiente decision tecnica grande debe ser una sola:
1. Postgres real + PostgresSaver para checkpoints persistentes, o
2. Setup wizard/runtime local para Ollama y GPU.

Recomendacion actualizada por Alejandro: parar aqui hasta tener Postgres corriendo. En PC corporativo, instalacion local requiere admin. Proxima opcion practica: Postgres gratuito remoto o instalar en el computador propio cuando lo compre.

## Preguntas pendientes para Alejandro

1. Quiere que Codex sea solo consultor o tambien auditor formal de Claude Code?

Auditor formal de claude code
2. Cual debe ser el primer cliente imaginario/real para Oli: founder, agencia, RevOps, product/eng ops?

Agencias y teams
3. El primer playbook debe ser research brief, reporte semanal o automatizacion de ventas?
4. Que nivel de honestidad quiere en scoring: conservador tipo inversor, o constructor optimista con riesgos marcados?

tu trabajo es ser critico

5. Debemos crear una rutina semanal de "review estrategico de Oli"?

Si, deberias manejar la misma constitution de oli.

## Proximo buen paso

Cuando Alejandro o Claude retomen:
1. Leer `AGENTS.md`.
2. Si la continuacion es estrategica, leer `14_cierre_sesion_2026-05-31_fine_tuning_next.md`.
3. Leer contexto condicional segun el modo:
   - estrategia/auditoria: `12_auditoria_v0_post_incidente_2026-05-31.md`;
   - prompt/UX: `13_prompt_engineering_codex_ux_2026-05-31.md`;
   - ejecucion V0: `05_estado_v0_implementacion.md`.
4. Ejecutar `py -m pytest` antes de declarar salud tecnica.
5. Resolver Postgres:
   - opcion A: PostgreSQL 18 local en computador propio/admin;
   - opcion B: Postgres gratuito remoto;
   - opcion C: Postgres en GPU/servidor alquilado cuando exista acceso SSH.
6. Con Postgres disponible, configurar `OLI_MISSION_STORE=sqlalchemy` y `OLI_DATABASE_URL`.
7. Despues conectar `PostgresSaver`.
8. Mantener `tests/test_v0_acceptance.py`, `tests/test_langgraph_mission_graph.py` y `tests/test_model_router_tiers.py` verdes.
9. Para fine-tuning serio, empezar por decidir si se acepta el primer lab recomendado: `Permission Policy Adapter`.
10. Si se acepta, el siguiente paso es especificar dataset schema, eval harness y baseline antes de entrenar.

67. Analisis de State of the Art para sistema de Research creado:
   - Archivo: `23_research_system_apis_state_of_art_2026-05-31.md`.
   - Veredicto: El "web fetch" basico es obsoleto debido a anti-bots y SPAs. Oli debe usar herramientas AI-native.
   - Opciones SOTA detectadas: Firecrawl (Scrape+Crawl cloud/self-hosted), Tavily (Search optimizado para RAG), Jina Reader (Conversor rapido URL->Markdown), Crawl4AI (Libreria local open-source para extraccion), y DuckDuckGo (Gratis/Fallback).
   - Decision recomendada: Oli no debe tener una unica tool de busqueda, sino un `Research Subsystem` con tiers (Zero-cost, AI-native, Local-heavy, Especializado). Integrar Jina Reader y DuckDuckGo como base cero-friccion, y Crawl4AI o Firecrawl para el runtime dedicado.

68. Research Stack v0 organizado en subcarpeta:
   - Carpeta: `Consultor Estrategico Codex/research_stack_v0/`.
   - Archivos creados: `README.md`, `01_connector_registry.md`, `02_research_workflow.md`, `03_evals_and_test_plan.md`, `04_build_plan.md`.
   - Decision: V0 no necesita una sola herramienta de busqueda; necesita conectores preestablecidos por categoria: web/search, docs reader, GitHub, OpenRouter, Hugging Face, benchmarks, papers, security y TDD/memoria.
   - Conectores base recomendados: Brave/Tavily/Exa, Jina Reader, Firecrawl/Crawl4AI, DuckDuckGo/SearXNG, GitHub, OpenRouter, Hugging Face, Artificial Analysis/LMArena, Semantic Scholar/arXiv/OpenAlex, NVD/GitHub Advisories, TDD/Mission Black Box.
   - Suficiencia V0: el stack es suficiente si pasa tres pruebas: coding delegate choice, model selection by tier y high-impact tool security risk.

69. Validacion SOTA de runtime/app PC/SSH y memoria creada:
   - Archivo: `24_runtime_ssh_memory_sota_validation_2026-05-31.md`.
   - Probes conectados en `research_stack_v0/scripts/`: `probe_research_connectors.py` y `model_second_reader_probe.py`.
   - Resultado conectores: 8/9 OK; fallo `semantic_scholar_search` por HTTP 429. Funcionaron OpenRouter docs, GitHub Hermes/OpenCode/Kilo, Hugging Face, arXiv, OpenAlex y NVD.
   - Modelo via OpenRouter: primer intento cayo a development adapter; segundo intento con red permitida produjo segunda lectura real. El proceso fallo solo al imprimir por encoding Windows, pero el output quedo guardado.
   - Veredicto runtime/SSH: direccion correcta, no launch-ready. Score ejecutivo 5/10. Falta session recording, command policy, sandbox hardening, egress policy y approval UX.
   - Veredicto memoria: mejor que RAG generico, pero no SOTA completa. Score ejecutivo 6/10. Falta jerarquia de memoria, temporal graph, write-time reconciliation, memory evals y data classification.
