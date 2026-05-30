# 10 - ICP, Moat, and Business Model

## ICP definition

### ICP paraguas

> Personas o equipos con alto volumen de trabajo digital, contexto fragmentado y necesidad de convertir intención en entregables terminados.

### ICP prioritario

> Founders y equipos pequeños de empresas AI-first / tech-enabled que necesitan más ejecución sin contratar más headcount.

### ICPs secundarios

Agencias, consultores, growth/revops, operaciones internas, product/engineering ops.

### Regla estratégica

Oli puede aceptar varios tipos de cliente. Pero el producto, la landing, los demos y las primeras misiones deben optimizarse para los que más rápido prueban valor.

> "Oli no es una herramienta de automatización. Es un operador de ejecución. Automatiza solo cuando una misión merece convertirse en sistema."

---

## ICP detallado por segmento

### ICP 1: Founder / Builder

Características:
- Founder solo o equipo de 2-10
- Usa IA todos los días
- Tiene demasiadas ideas, decisiones, documentos, research y tareas
- No quiere otro chatbot; quiere alguien que avance trabajo
- Tolera producto beta si siente leverage real
- Puede pagar $79-$299/mes si ahorra tiempo claro

Jobs-to-be-done:
- Convertir ideas en specs, memos, issues, planes y entregables
- Investigar mercado, competidores, pricing, tecnología
- Revisar repos, preparar fixes, generar tareas para devs
- Mantener memoria de decisiones y contexto de empresa

Mensaje: "Dile a Oli qué quieres terminado. Oli convierte intención en research, specs, decisiones y ejecución."

Riesgo: muchos founders técnicos pueden construir algo parecido. Pueden amar el producto pero pagar poco o churnear si no se vuelve hábito.

**Prioridad: Alta para V0-V2. Media como mercado grande.**

---

### ICP 2: Equipos Pequeños / Founder-Led Companies

Características:
- Empresas de 5-50 personas
- Tienen trabajo digital repetido pero no procesos maduros
- Usan Slack, Notion, Google Workspace, HubSpot, Linear, GitHub, Sheets
- Hay una persona "operadora" que conecta todo manualmente
- Les duele contratar más gente para tareas de coordinación

Jobs-to-be-done:
- Preparar reportes semanales
- Convertir reuniones/notas en decisiones y tareas
- Revisar métricas, feedback y documentos
- Coordinar entregables entre herramientas
- Hacer seguimiento sin perseguir personas

Mensaje: "Oli ayuda a equipos pequeños a terminar más trabajo sin añadir más coordinación."

Riesgo: requieren onboarding, permisos, conectores y confianza. Si el producto falla, afecta procesos reales.

**Prioridad: Muy alta para monetización.**

---

### ICP 3: Agencias y Consultoras

Características:
- Agencias de marketing, desarrollo, contenido, research, automatización o growth
- Manejan múltiples clientes
- Repiten procesos parecidos con variaciones
- Tienen presión de margen
- Les importa entregar más rápido sin bajar calidad

Jobs-to-be-done:
- Research por cliente
- Reportes mensuales/semanales
- Preparar campañas, briefs, assets y propuestas
- Convertir aprendizajes de un cliente en procesos reutilizables
- Mantener memoria por cliente/proyecto

Mensaje: "Convierte trabajo de cliente en misiones repetibles, auditables y listas para entregar."

Por qué es fuerte: dolor económico directo (horas facturables), pueden pagar más si mejora margen, los playbooks por cliente son muy defensibles.

Riesgo: pueden pedir demasiada personalización. Si Oli toca entregables externos, exige control de calidad alto.

**Prioridad: Muy alta para pilotos pagados.**

---

### ICP 4: Growth / RevOps / Sales Ops

Características:
- Equipos de 2-15 dentro de startups o empresas pequeñas
- Viven entre CRM, email, LinkedIn, Sheets, enrichment, dashboards
- Mucho trabajo repetitivo pero también criterio humano
- Necesitan aprobación antes de acciones externas

Jobs-to-be-done:
- Investigar cuentas/leads
- Enriquecer CRM
- Preparar secuencias y follow-ups
- Analizar pipeline
- Generar reportes y alertas
- Preparar campañas, no necesariamente enviarlas

Mensaje: "Oli prepara el trabajo comercial pesado y deja las decisiones listas para aprobar."

Riesgo: datos sensibles, riesgo de spam si se ejecuta mal, mercado lleno de herramientas verticales.

**Prioridad: Alta, pero después de permisos/evidencia sólidos.**

---

### ICP 5: Operaciones Internas / Admin Ops

Características:
- Pequeñas empresas con procesos administrativos manuales
- Mucho Google Workspace, PDFs, facturas, calendarios, reportes, formularios
- Usuarios menos técnicos
- Dolor real, pero menor tolerancia a configuración técnica

Jobs-to-be-done:
- Organizar documentos
- Preparar reportes
- Revisar facturas/contratos
- Actualizar bases de datos
- Coordinar calendarios, tareas y aprobaciones

Mensaje: "Oli convierte instrucciones normales en trabajo administrativo terminado, con permisos y evidencia."

Riesgo: requiere UX muy pulida, soporte alto, menor disposición a lidiar con betas.

**Prioridad: Media. Mejor para V3+.**

---

### ICP 6: Product / Engineering Ops

Características:
- Equipos pequeños de producto/engineering
- Mucho contexto en GitHub, Linear, Notion, Slack
- Necesitan convertir bugs, feedback y decisiones en specs/tickets/PR plans
- Valoran trazabilidad y tests

Jobs-to-be-done:
- Feedback to roadmap
- Bug report to diagnosis
- Spec to implementation plan
- Meeting notes to issues
- PR review summaries
- Release notes

Mensaje: "Oli convierte contexto disperso de producto e ingeniería en trabajo listo para ejecutar."

Riesgo: compite parcialmente con Cursor, Claude Code, Linear AI, GitHub Copilot. Debe integrarse bien con workflows dev.

**Prioridad: Alta para fundador/dev-first, media para ventas amplias.**

---

## Priorización por versión

```text
V0-V1:   Founder / Builder  +  Product/Engineering Ops
V2-V3:   Equipos pequeños founder-led  +  Agencias/consultoras
V3-V4:   Growth/RevOps  +  Operaciones internas
V5+:     Empresas pequeñas más formales, 50-200 con compliance
```

## Ranking comercial

1. Agencias/consultoras — ROI claro, repetición, pagan si sube el margen
2. Equipos pequeños founder-led — mercado amplio, dolor real, buen encaje
3. Founder/builders — excelente para producto y comunidad, no necesariamente el mejor revenue
4. Product/Engineering Ops — fuerte si Oli demuestra ejecución técnica real
5. Growth/RevOps — buen dinero, más riesgo por datos y acciones externas
6. Admin/Ops interno — enorme mercado, exige producto más maduro

---

## Wedge criteria

Una misión class es buena si tiene:

- repeated pain
- clear input/output
- measurable time savings
- deterministic or semi-deterministic validation
- high enough value to justify setup
- low enough catastrophic risk for early versions
- ability to become a playbook

## Recommended first mission classes

### 1. Founder notes → Claude Code-ready specs
- directly helps build Oli
- high leverage
- easy to validate by whether Claude Code can implement
- aligns with current workflow

### 2. Feedback/documents → roadmap/issues/specs
- high-value operational transformation
- repeatable
- produces artifacts
- memory improves over time

### 3. Repo inspection → fix plan / PR preparation
- strong fit for local coding models
- validation through tests
- clear evidence

### 4. Recurring report automation
- strong for small teams/ops
- clear saved hours
- repeatable
- dashboard/evidence useful

### 5. Sales/marketing ops preparation, not sending
- valuable, repeatable, can be approval-gated
- avoids early external-action risk

---

## Moat thesis

Oli's moat is not the base model.

Oli's moat is the compound system around execution:

1. Long-term user/company/mission memory that is expensive to rebuild elsewhere.
2. Oli-managed compute — the user does not own or manage infrastructure.
3. Model routing based on real benchmarks and mission history.
4. Validated playbooks for recurring workflows, calibrated to each org.
5. Permission and evidence system users trust.
6. Secure execution in isolated tenants on our infrastructure.
7. Mission-class-specific evals and validators.
8. Oli-to-Oli solution bank — private repo network that accumulates generalized solutions.

The switching cost is not just "export data." It is losing accumulated memory, playbooks, routing intelligence, and access to the solution bank.

## Oli-to-Oli learning

Each Oli operates in isolation per organization. No user data or content is shared between organizations.

However: when an Oli resolves a type of mission, it can derive a generalized solution — a repo, a script, a template, a pattern — with no user content. These artifacts accumulate in a private solution bank shared only between Olis, not between organizations.

Over time, this bank is incorporated into the model directly (fine-tuning or RAG), making each new Oli faster and more capable from day one.

Rules:
- Only structure and code are contributed — never text derived from user content.
- The user never sees or approves this (it is a platform-level operation post-mission).
- Nothing from this bank is exposed to other organizations' users.
- This is a proprietary moat, not an open-source resource.

## Data flywheel (per organization)

```text
Mission executed
  → evidence captured
  → validation result stored
  → user feedback captured
  → memory updated
  → playbook improved
  → model routing improved
  → future mission cheaper/safer/faster
  → user delegates more important work
  → [optionally] generalized solution contributed to Oli solution bank
```

## Onboarding model

Hybrid:
- Starter and Pro: self-serve — sign up, connect tools, run first mission
- Team: done-with-you — Oli team configures first workflows, sets up playbooks, trains the team

## Privacy-preserving learning (PAUSED)

Decision deferred. No compliance framework defined yet. Does not block V0-V3 build.

When revisited: the principle is that only generalized structure and code can leave an organization's context — never user content, never summarized text derived from user content.

## Pricing model V6 (definitivo — 2026-05-27)

Ver documento completo con unit economics, sensibilidad y política de control: `tdd/domain/pricing-model-v6.md`

| Tier | Precio | Seats | Créditos incluidos | Overage | Narrativa |
|---|---|---|---|---|---|
| Starter | $79/mes | 1 | 660/mes | $0.09/cr | Individuo — founder solo, power user |
| Pro | $129/seat/mes | máx 3 | 1,100/seat (pool) | $0.08/cr | Mini-equipo — cofounders, agencia pequeña |
| Team | $199/seat/mes | mín 4 | 1,500/seat (pool) | $0.08/cr | Organización — equipo formal, empresa pequeña |

Gross margins estimados: Starter ~70% | Pro ~79% | Team ~81%

## Strategic rule

Founders are not the whole market.

Founders are the proving ground.

Small teams, agencies, and operations teams are where the business hardens.
