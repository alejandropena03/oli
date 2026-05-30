# Vertical Slice 002 — Sales Automation System

**Estado:** ✅ En papel
**Fecha:** 2026-05-26
**Pregunta:** ¿Puede Oli construir un sistema completo (no solo ejecutar una tarea) de punta a punta?

---

## Por qué este slice es diferente al 001

Slice-001 era una misión de *investigación y entrega de texto* — permiso clase 0, sin herramientas externas, sin construcción de sistemas.

Slice-002 es una misión de *construcción real*:
- Involucra múltiples servicios externos (HubSpot, n8n, Slack)
- Requiere permisos clase 2 y 3
- Produce artefactos que persisten (workflows, configs, código)
- Necesita validación con tests reales
- Tiene fases secuenciales con dependencias entre sí

Si la arquitectura soporta esto, soporta la mayoría de lo que Oli necesitará en V3+.

---

## La misión

**Intención del usuario (voz):**
> "Oli, crea un sistema de automatización de ventas para mi empresa.
> Vendemos software B2B a empresas medianas.
> Necesito captura de leads desde el sitio, calificación automática,
> seguimiento por email y alertas al equipo cuando hay un lead caliente."

**Source:** `voice_local` (el founder lo dijo por voz)

---

## FASE 1 — INTAKE Y CLARIFICACIÓN

### LangGraph: nodo `interpret_intent`

El modelo local (Tier 1) intenta interpretar la intención.
Confianza inicial: 0.62 — hay ambigüedad en "calificación automática" y en qué CRM usan.

**Resultado: `ClarificationNeeded` → interrupt `human_clarification`**

Oli pregunta (2 preguntas, ambas necesarias — sin ellas el plan sería incorrecto):

```
"Antes de armar el sistema, necesito dos cosas:
 1. ¿Qué CRM usas actualmente — HubSpot, Notion, Salesforce, u otro?
 2. ¿Tienes n8n o Make corriendo, o construimos los flujos desde cero?"
```

**Founder responde:** "HubSpot. Tenemos n8n."

### Nodo `interpret_intent` (segunda pasada con clarificación)

```python
InterpretedIntent(
    goal="build_sales_automation_system",
    success_criteria=[
        "formulario de captura funcional en el sitio",
        "lead score calculado automáticamente (0-100)",
        "contacto creado en HubSpot con score y datos",
        "email sequence activada para leads score > 50",
        "alerta Slack para leads score > 80",
        "5/5 tests de validación pasados"
    ],
    output_format="sistema funcional + documentación + tests",
    scope=Scope(
        in_scope=["formulario HTML", "n8n workflow", "HubSpot config", "Slack alerts"],
        out_of_scope=["integración con el sitio (eso lo hace el founder)", "email copywriting"]
    ),
    confidence=0.94
)
```

---

## FASE 2 — CONTEXTO Y PERMISOS

### Nodo `retrieve_context` → Memory Graph (RAG)

Query semántica: "sales automation B2B HubSpot n8n"

**Resultados del vector store:**
```
Company memory:
  - producto: software B2B para empresas medianas
  - ICP: empresas 50-500 personas, sector tech/ops
  - stack actual: HubSpot + n8n (confirmado en clarificación)

User memory:
  - founder prefiere documentación concisa
  - ha rechazado antes outputs sin tests
  - horario: trabajo 9am-7pm

Mission memory:
  - no hay misiones similares previas
  - playbook "sales_automation" no existe aún
```

### Nodo `classify_permissions`

```python
PermissionsClassified(
    actions=[
        Action("crear formulario HTML",           class_=1),  # archivo local, reversible
        Action("crear workflow n8n via API",       class_=2),  # consume recursos de n8n
        Action("configurar HubSpot properties",   class_=2),  # modifica CRM
        Action("crear HubSpot email sequence",    class_=2),  # modifica CRM
        Action("configurar Slack notifications",  class_=3),  # comunicación externa
        Action("enviar test leads a HubSpot",     class_=2),  # datos reales al CRM
    ],
    total_permission_class=3,  # máximo del plan
    requires_approval=True
)
```

---

## FASE 3 — PLANIFICACIÓN

### Nodo `create_plan` → Orchestrator + Claude Sonnet (Tier 3)

*Aquí se usa Sonnet porque el diseño de arquitectura de un sistema complejo es Tier 3.*

**TechnicalArchitectSuboperator** es invocado como sub-grafo:
- Evalúa 2 alternativas: n8n nativo vs. Python script + n8n
- Recomienda: n8n nativo (el founder ya lo conoce, más mantenible)
- Identifica riesgos: rate limits de HubSpot API, GDPR en el email sequence

**Plan generado:**

```
Módulo A — Captura (permission: 1)
  Step A1: Generar formulario HTML+JS con campos de calificación
  Step A2: Crear webhook endpoint en n8n para recibir submissions

Módulo B — Scoring (permission: 2)
  Step B1: Construir nodo n8n que llama LLM para score 0-100
  Step B2: Definir reglas: empresa_size + sector_match + cargo → score

Módulo C — CRM (permission: 2)
  Step C1: Crear custom properties en HubSpot (lead_score, automation_source)
  Step C2: Configurar pipeline stage "Automation Qualified"
  Step C3: Conectar n8n → HubSpot API

Módulo D — Email Sequence (permission: 2)
  Step D1: Crear sequence en HubSpot (5 emails, 14 días)
  Step D2: Configurar trigger: score > 50 AND source = automation

Módulo E — Alertas (permission: 3) ← APPROVAL GATE
  Step E1: Configurar Slack webhook
  Step E2: Nodo n8n: si score > 80 → mensaje al canal #ventas

Módulo F — Tests y documentación (permission: 0)
  Step F1: Enviar 3 leads de prueba (alto score, bajo score, borde)
  Step F2: Verificar resultados esperados
  Step F3: Generar documentación del sistema
```

**Estimado:**
```
Duración: ~22 minutos
Costo tokens: ~$0.35 (Sonnet para arquitectura + Haiku para steps de ejecución)
Costo GPU: ~$0.15 (5 min de Tier 1 para scoring logic)
Costo total: ~$0.50
Horas humanas equivalentes: ~14-16 horas
```

### APPROVAL GATE — `human_approval` interrupt

Oli muestra la ruta visible:
```
/oli ruta propuesta — Sistema de automatización de ventas

Voy a construir 6 módulos. Los primeros 4 los ejecuto solo.
Para el Módulo E (alertas Slack) necesito tu aprobación porque
envía mensajes al canal #ventas de tu equipo.

Herramientas: n8n API, HubSpot API, Slack API
Datos que salen del entorno local: configuración de HubSpot y n8n
Costo estimado: ~$0.50 en modelos
Punto de aprobación: antes del Módulo E
Duración estimada: ~22 minutos

¿Arranco?
```

**Founder aprueba.** → Grafo reanuda.

---

## FASE 4 — EJECUCIÓN

### ExecutionSuboperator ejecuta step a step

**Módulo A — Formulario (linux_shell + filesystem MCP)**
```python
# Step A1: genera formulario
result = linux_shell.execute("""
python3 -c "
import jinja2
template = get_template('lead_form.html.j2')
output = template.render(fields=['nombre', 'empresa', 'cargo', 'tamaño_empresa', 'email'])
write_file('/tmp/oli_output/lead_form.html', output)
"
""")
# resultado: archivo HTML generado en /tmp/oli_output/
```

**Módulo B — Scoring workflow (n8n API directa)**
```python
# Step B1: crea workflow de scoring en n8n
result = n8n_api.create_workflow({
    "name": "oli_lead_scoring",
    "nodes": [
        {"type": "webhook", "name": "Recibe lead"},
        {"type": "function", "name": "Calcula score",
         "code": SCORING_LOGIC},  # generado por LLM
        {"type": "if", "name": "Bifurca por score"},
    ]
})
# resultado: workflow_id guardado en evidence store
```

**Módulo C — HubSpot (HubSpot API directa)**
```python
# Step C1: crea custom properties
hubspot_api.create_property("lead_score", "number")
hubspot_api.create_property("automation_source", "string")
# Step C2: actualiza pipeline
hubspot_api.create_pipeline_stage("Automation Qualified")
# resultado: properties y stage creados, IDs guardados
```

**→ Approval gate Módulo E → founder aprueba por segunda vez**

**Módulo E — Slack (Slack API directa, permission 3)**
```python
result = slack_api.configure_notification(
    channel="#ventas",
    trigger="lead_score > 80",
    message_template="🔥 Lead caliente: {nombre} de {empresa} (score: {score})"
)
```

---

## FASE 5 — TROUBLESHOOTING (ejemplo de fallo real)

Durante Step C3, el webhook de n8n → HubSpot falla:

```
Error: HubSpot API rate limit exceeded (429)
```

**Nodo `troubleshoot` diagnostica:**

```
Tipo: transient (rate limit, no error de lógica)
Estrategia 1: retry con backoff exponencial (1s, 4s, 16s)
  → Intento 1 (1s): falla
  → Intento 2 (4s): falla
  → Intento 3 (16s): éxito ✓

Resuelto solo. El founder no fue notificado.
Audit trail: registra los 3 intentos con timestamps y razón.
```

---

## FASE 6 — VALIDACIÓN

### ValidationSuboperator ejecuta 5 tests reales

```python
tests = [
    Test(
        name="lead_alto_score_llega_a_hubspot",
        action="enviar lead con empresa_size=200, cargo=CTO",
        expected=["contact creado en HubSpot", "score >= 80", "alerta Slack enviada"],
        result=PASS  # ✅
    ),
    Test(
        name="lead_bajo_score_no_activa_sequence",
        action="enviar lead con empresa_size=5, cargo=asistente",
        expected=["contact creado", "score <= 30", "NO email sequence activada"],
        result=PASS  # ✅
    ),
    Test(
        name="lead_borde_score_50_activa_sequence",
        action="enviar lead con score exactamente 51",
        expected=["email sequence activada", "NO alerta Slack"],
        result=PASS  # ✅
    ),
    Test(
        name="datos_llegan_completos_a_hubspot",
        action="verificar todas las properties en el contact creado",
        expected=["lead_score presente", "automation_source = 'oli_form'"],
        result=PASS  # ✅
    ),
    Test(
        name="webhook_rechaza_datos_invalidos",
        action="enviar submission sin email",
        expected=["n8n retorna 400", "no contact creado en HubSpot"],
        result=PASS  # ✅
    ),
]
# ValidationResult: 5/5 PASS, score=1.0
```

---

## FASE 7 — ENTREGA Y COMPROBANTE

```
/oli comprobante — Sistema de automatización de ventas

Entregado:
  ✓ /tmp/oli_output/lead_form.html — formulario listo para pegar en el sitio
  ✓ n8n workflow "oli_lead_scoring" — activo y testeado (ID: wf_8821)
  ✓ HubSpot: properties + pipeline stage + email sequence configurados
  ✓ Slack: alertas activas en #ventas para leads score > 80
  ✓ /tmp/oli_output/docs/sistema_ventas.md — documentación completa

Supuestos: ninguno (todo fue clarificado al inicio)

Costo real:
  Tokens: $0.38 (Sonnet: $0.28 / Haiku: $0.07 / Local: $0.03)
  GPU: $0.12 (6 min de Tier 1)
  Total: $0.50

Horas humanas ahorradas: ~15 horas
Tests: 5/5 pasados

Revisión humana necesaria:
  → El formulario HTML necesita ser pegado en el sitio por el founder
  → Revisar el copy de los 5 emails de la sequence (Oli los dejó como plantilla)

Playbook candidate: SÍ
  Nombre sugerido: sales_automation_b2b_v1
  Próxima empresa similar: ~8 minutos con el playbook vs. 22 minutos hoy
```

---

## GAPS IDENTIFICADOS EN LA ARQUITECTURA

Al trazar este slice, aparecen 4 gaps que el TDD actual no cubre completamente:

### Gap 1 — Manejo de credenciales de terceros durante la construcción
**Problema:** En Step C1 (HubSpot) y Step E1 (Slack), Oli necesita tokens que pueden no estar en el vault todavía.
**Lo que pasa:** Oli detecta que la credencial falta → lanza el OAuth flow de HubSpot → el founder autoriza → continúa.
**Veredicto:** ✅ Cubierto por ADR-014. El flujo está definido.

### Gap 2 — Estado de artefactos generados
**Problema:** Los archivos en `/tmp/oli_output/` son temporales. ¿Dónde persisten los artefactos?
**Lo que pasa:** El Evidence Store guarda la referencia, pero el archivo en sí se pierde si el sistema se reinicia.
**Veredicto:** 🔴 **Gap real** — necesita ADR. MinIO para artifacts es la solución (está en el stack pero no especificado cuándo entra).

### Gap 3 — Tests que modifican datos reales
**Problema:** Los 5 tests del Módulo F envían leads reales a HubSpot. En producción, eso crea contacts basura.
**Propuesta:** Sandbox environment en HubSpot para tests, o flag `test_mode=true` que usa un pipeline separado.
**Veredicto:** 🔴 **Gap real** — necesita definirse antes del build.

### Gap 4 — Handoff de artefactos al founder
**Problema:** El formulario HTML generado necesita llegar al founder de alguna forma. "En `/tmp/oli_output/`" no es una UX aceptable.
**Propuesta:** Oli abre la carpeta en el finder/explorador, o la muestra en el Evidence Drawer de la UI.
**Veredicto:** 🟡 **Diseño pendiente** — no bloquea V0 pero bloquea V2.

---

## MÓDULOS DEL TDD USADOS

| Módulo | Cómo se usa en este slice |
|---|---|
| Mission Kernel + LangGraph | Orquesta las 7 fases, mantiene estado, hace checkpoints |
| TechnicalArchitectSuboperator | Evalúa n8n vs. Python script, identifica riesgos |
| ExecutionSuboperator | Ejecuta API calls, genera archivos, configura servicios |
| ValidationSuboperator | Corre los 5 tests reales |
| MemoryCuratorSuboperator | Guarda el stack del founder, propone playbook |
| Permission Service | Gate en Módulo E (clase 3), approval flow |
| Memory Graph + RAG | Recupera contexto del founder antes del plan |
| Evidence Store | Guarda artefactos, IDs de workflows, resultados de tests |
| Cost Tracker | Registra tokens por modelo, tiempo de GPU |
| Playbook Engine | Detecta candidato, propone nombre |
| Model Router | Sonnet para arquitectura (Tier 3), Haiku para steps (Tier 2), Local para scoring (Tier 1) |
| Troubleshoot node | Resuelve rate limit de HubSpot sin escalar al founder |
| Auth / Credential Broker | OAuth flow para HubSpot y Slack si no están en vault |

**Conclusión:** La arquitectura actual soporta este slice completamente, excepto los 2 gaps marcados en rojo.
