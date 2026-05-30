# Flujos detallados de misión — Oli

**Fecha:** 2026-05-26
**Propósito:** Describir con precisión cómo viaja una señal desde el usuario hasta el resultado.
Estos flujos son la prueba de que la arquitectura del TDD puede responder casos reales.

---

## FLUJO 1 — Voz end-to-end

El usuario dice "Oli" y espera una respuesta. Cada milisegundo importa.

```
USUARIO (dice "Oli, prepara el reporte de esta semana")
│
├─ CAPA LOCAL (máquina del usuario — siempre activo en background)
│  │
│  ├─ [1] OpenWakeWord escucha el micrófono continuamente
│  │       Modelo local ~40MB · <5ms latencia · nunca envía audio
│  │       Detecta "Oli" → activa grabación
│  │
│  ├─ [2] VAD (Voice Activity Detection)
│  │       Detecta cuándo el usuario terminó de hablar
│  │       Graba solo la utterance (~3 segundos)
│  │
│  ├─ [3] Whisper.cpp (local) o Whisper API
│  │       Transcribe audio → texto
│  │       Local: ~800ms en CPU / ~200ms en GPU local
│  │       API: ~300ms + latencia de red
│  │       Output: "prepara el reporte de esta semana"
│  │
│  └─ [4] Texto llega al Mission Kernel (local)
│
├─ MISSION KERNEL (local — V0-V2)
│  │
│  ├─ [5] CreateMission(raw_input, source: "voice_local")
│  │
│  ├─ [6] InterpretIntent → LLM call
│  │       Modelo: Claude Haiku (rápido, barato para intent)
│  │       Output: {goal: "weekly_report", success_criteria: [...]}
│  │
│  ├─ [7] RetrieveContext → Memory Graph
│  │       Lee: user_preferences, company_context, last_weekly_report
│  │       "el founder prefiere tablas, el reporte incluye ventas + métricas"
│  │
│  ├─ [8] ClassifyPermissions
│  │       read BigQuery: class 0 | write Sheets: class 1 | send email: class 3
│  │       Total plan: class 3 → requiere aprobación para el envío
│  │
│  ├─ [9] CreatePlan → Orchestrator + LLM
│  │       Step 1: BigQuery query (metrics)
│  │       Step 2: Google Sheets update
│  │       Step 3: Generate report text
│  │       Step 4: [APPROVAL GATE] Send email to team
│  │
│  └─ [10] TTS: "Listo el plan. Pasos 1-3 los hago solo.
│            Para el paso 4 (enviar al equipo) necesito tu ok.
│            Estimado: 8 min, $0.12. ¿Arranco?"
│
├─ USUARIO responde "Sí"
│
├─ EJECUCIÓN
│  │
│  ├─ [11] Step 1: BigQuery MCP / API directa
│  │        SQL query → métricas de la semana
│  │        ~2-5 segundos
│  │
│  ├─ [12] Step 2: Google Sheets API
│  │        Actualiza dashboard del founder
│  │        ~1-2 segundos
│  │
│  ├─ [13] Step 3: LLM call (Claude Sonnet)
│  │        Genera texto del reporte con datos reales
│  │        ~3-5 segundos
│  │
│  ├─ [14] ValidationSuboperator
│  │        ✅ métricas incluidas ✅ formato tabla ✅ < 500 palabras
│  │
│  ├─ [15] APPROVAL GATE — TTS al usuario:
│  │        "El reporte está listo. ¿Lo envío al equipo?"
│  │        Founder: "Sí"
│  │
│  └─ [16] Gmail API → envía el reporte
│
├─ ENTREGA
│  │
│  ├─ [17] TTS: "Listo. Reporte enviado. 7 minutos, $0.11."
│  │
│  ├─ [18] MemoryCurator actualiza Mission Memory
│  │        Guarda: weekly_report completado, formato aprobado, costo real
│  │
│  └─ [19] PlaybookEngine evalúa candidato
│           ≥ 3 ejecuciones similares → propone weekly_report_v1 playbook

TIEMPO TOTAL: ~9 minutos (mayoría en BigQuery + LLM)
TIEMPO HUMANO AHORRADO: ~2 horas
COSTO: ~$0.11
```

---

## FLUJO 2 — Sistema de automatización de ventas (misión compleja de construcción)

El usuario pide un *sistema*, no una tarea puntual. Oli no solo ejecuta — diseña, construye, prueba y entrega.

```
USUARIO: "Oli, crea un sistema de automatización de ventas para mi empresa.
          Vendemos software B2B a empresas medianas. Necesito:
          captura de leads desde el sitio, calificación automática,
          seguimiento por email, CRM actualizado y alertas al equipo."

─────────────────────────────────────────────────────────────────────
FASE 1 — ENTENDER (no asumir nunca)
─────────────────────────────────────────────────────────────────────

[1] ClarificationNeeded — Oli pregunta (máx 2):
    "¿Qué CRM usas actualmente? (HubSpot, Notion, otro, ninguno)"
    "¿Tienes n8n o Make configurado, o construimos todo desde cero?"

[2] Founder responde: "HubSpot. n8n ya tenemos."

─────────────────────────────────────────────────────────────────────
FASE 2 — INVESTIGAR (MarketResearchSuboperator + TechnicalArchitect)
─────────────────────────────────────────────────────────────────────

[3] MarketResearchSuboperator:
    - Investiga mejores prácticas de automatización B2B 2026
    - Benchmarks: tasa de conversión lead→demo con automation
    - Herramientas: HubSpot Workflows vs n8n vs custom
    - Fuentes: HubSpot blog, Gartner, G2 reviews
    Tiempo: ~4 min | Costo: ~$0.08

[4] TechnicalArchitectSuboperator:
    - Mapea el stack actual: HubSpot + n8n + sitio web del usuario
    - Diseña la arquitectura del sistema:
      Sitio web → formulario → n8n → HubSpot API → email sequences
    - Identifica riesgos: rate limits HubSpot, GDPR compliance
    - Propone 3 opciones con tradeoffs
    Tiempo: ~3 min | Costo: ~$0.06

─────────────────────────────────────────────────────────────────────
FASE 3 — PLANIFICAR
─────────────────────────────────────────────────────────────────────

[5] Orchestrator genera plan detallado:

    Módulo A: Captura de leads
      - Formulario en el sitio (HTML/JS) con campos de calificación
      - Webhook → n8n para procesamiento

    Módulo B: Calificación automática (scoring)
      - n8n workflow: recibe lead → LLM evalúa empresa → score 0-100
      - Reglas: empresa_size > 50 AND sector_match → score alto

    Módulo C: CRM (HubSpot)
      - HubSpot API: crear contact, deal, pipeline stage
      - Custom properties: lead_score, automation_source

    Módulo D: Email sequences
      - HubSpot Sequences: 5 emails en 14 días
      - Personalización con datos del lead

    Módulo E: Alertas al equipo
      - Score > 80: Slack DM al vendedor asignado
      - Deal sin actividad > 3 días: alerta automática

    permission_class máximo: 3 (envía emails + mensajes)
    → APPROVAL GATE: founder aprueba el plan completo

─────────────────────────────────────────────────────────────────────
FASE 4 — CONSTRUIR (ExecutionSuboperator)
─────────────────────────────────────────────────────────────────────

[6] Construir formulario de captura:
    linux_shell/E2B: genera HTML+JS → archivo en filesystem
    Tiempo: ~2 min

[7] Construir workflow n8n (Módulos A+B+C):
    n8n API: crear workflow via JSON
    Nodos: Webhook → Extract → LLM Score → HubSpot Create → Branch
    Tiempo: ~5 min

[8] Configurar HubSpot (Módulos C+D):
    HubSpot API directa:
    - Crear custom properties
    - Crear email sequence
    - Configurar pipeline stages
    Tiempo: ~4 min

[9] Configurar alertas Slack (Módulo E):
    Slack API: crear workflow de notificaciones
    Tiempo: ~2 min

─────────────────────────────────────────────────────────────────────
FASE 5 — PROBAR
─────────────────────────────────────────────────────────────────────

[10] ValidationSuboperator ejecuta tests:
     - Envía lead de prueba → verifica que llega a HubSpot
     - Verifica score calculation con lead ficticio
     - Verifica que email sequence se activa
     - Verifica que alerta Slack llega
     - Verifica que lead bajo score NO activa la secuencia

     Si falla algún test → RepairStep automático (hasta 3 intentos)

─────────────────────────────────────────────────────────────────────
FASE 6 — ENTREGAR
─────────────────────────────────────────────────────────────────────

[11] Oli entrega al founder:
     - URL del formulario de captura (para pegar en el sitio)
     - Link al workflow de n8n (ya activo)
     - Screenshot del pipeline en HubSpot
     - Documentación: cómo funciona cada módulo
     - Evidence: todos los tests pasados con evidencia

[12] Mission Report:
     Tiempo total: ~22 minutos
     Costo Oli: ~$0.45
     Costo humano equivalente: ~16 horas de desarrollo + configuración
     Tests: 5/5 pasados
     Playbook candidate: YES → "sales_automation_b2b_v1"

─────────────────────────────────────────────────────────────────────
LO QUE HACE POSIBLE ESTE FLUJO EN EL TDD:
─────────────────────────────────────────────────────────────────────
✅ MarketResearchSuboperator — investigación con fuentes
✅ TechnicalArchitectSuboperator — diseño de arquitectura
✅ ExecutionSuboperator — construye con API directa + n8n + linux_shell
✅ ValidationSuboperator — tests reales antes de entregar
✅ Mission Kernel — orquesta las fases en orden
✅ Permission model — approval gate en clase 3 antes de enviar emails
✅ Evidence Store — documenta todo el proceso
✅ Playbook Engine — convierte en sistema reutilizable
```

---

## FLUJO 3 — Asistente de WhatsApp con memoria contextual

```
CONTEXTO:
  OpenClaw conectado como canal de entrada (ADR-013)
  Oli recibe los mensajes de WhatsApp via OpenClaw MCP
  Memory Graph guarda contexto de cada contacto
  El founder ve todo en la app desktop de Oli

─────────────────────────────────────────────────────────────────────
CAPA DE INGESTA — Tiempo real, background
─────────────────────────────────────────────────────────────────────

[1] Mensaje nuevo en WhatsApp (Juan Pérez, cliente):
    "Hola! Tengo una pregunta sobre la propuesta que me mandaste"

[2] OpenClaw recibe → pasa a Oli vía MCP
    source: "openclaw_whatsapp"
    contact: "Juan Pérez | +57..."

[3] Oli consulta Memory Graph:
    Company memory: Juan = cliente potencial, propuesta enviada 3 días ago
    Mission memory: última misión con Juan = "send_proposal" hace 3 días
    User memory: founder responde clientes entre 9am-12pm
    Contact memory: Juan escribe corto, directo, responde rápido

─────────────────────────────────────────────────────────────────────
CONSTRUCCIÓN DE BITÁCORA
─────────────────────────────────────────────────────────────────────

[4] MemoryCuratorSuboperator actualiza contact thread:
    Thread Juan Pérez:
    ─ [hace 5 días] Founder envió propuesta por email
    ─ [hace 3 días] Oli ejecutó misión "send_proposal" → entregado
    ─ [hace 1 día]  Juan visto propuesta (apertura email detectada via Gmail API)
    ─ [HOY 10:23am] Juan pregunta sobre la propuesta → NUEVO MENSAJE

─────────────────────────────────────────────────────────────────────
RESPUESTA SUGERIDA
─────────────────────────────────────────────────────────────────────

[5] Oli genera respuesta sugerida:
    Contexto: Juan es directo, propuesta enviada hace 3 días,
              probablemente quiere aclarar precio o implementación

    Sugerencia: "Hola Juan! Claro, dime qué necesitas saber.
                 Si quieres, también podemos hacer una llamada
                 rápida de 20 min esta semana."

    Tono: casual-profesional (aprendido del patrón de conversación del founder)
    Permisos: class 0 (solo sugerencia, no envía)

─────────────────────────────────────────────────────────────────────
NOTIFICACIÓN AL FOUNDER
─────────────────────────────────────────────────────────────────────

[6] App desktop Oli muestra notificación:
    ┌─────────────────────────────────────────┐
    │ 💬 Juan Pérez — WhatsApp                │
    │ "Hola! Tengo una pregunta sobre la..."  │
    │                                         │
    │ Contexto: propuesta enviada hace 3 días │
    │ Última vez: vio el email ayer           │
    │                                         │
    │ Sugerencia de respuesta:                │
    │ "Hola Juan! Claro, dime qué necesitas..." │
    │                                         │
    │ [Enviar esta] [Editar] [Ignorar]        │
    └─────────────────────────────────────────┘

─────────────────────────────────────────────────────────────────────
RECORDATORIO INTELIGENTE
─────────────────────────────────────────────────────────────────────

[7] Si el founder no responde en X horas:
    → Oli envía alerta (voz o notificación):
    "Juan Pérez está esperando respuesta desde hace 4 horas.
     Preguntó sobre la propuesta. ¿Respondo con la sugerencia?"

[8] Founder dice "Sí" → class 3 → Oli envía via OpenClaw → WhatsApp

─────────────────────────────────────────────────────────────────────
AGENDA AUTOMÁTICA
─────────────────────────────────────────────────────────────────────

[9] Juan responde: "Me gustaría una llamada, ¿jueves?"

[10] Oli detecta intención de agendar:
     → Google Calendar API: verifica disponibilidad del founder el jueves
     → Encuentra slot libre: jueves 3pm
     → Sugerencia: "Perfecto, jueves 3pm te funciona?"

[11] Founder aprueba → Oli confirma con Juan → crea evento en Calendar
     Evento: "Call Juan Pérez - Propuesta" | Jueves 3pm | Link Meet generado

─────────────────────────────────────────────────────────────────────
LO QUE FALTABA EN EL TDD — GAPS IDENTIFICADOS:
─────────────────────────────────────────────────────────────────────
❌ Contact Memory — no estaba definida como sub-capa de Company Memory
   → Necesita: contact_id, thread_history, tone_profile, relationship_stage
❌ Proactive monitoring — Oli actúa en background sin que el founder inicie misión
   → Necesita: background_agent loop, event triggers (mensaje nuevo = crear misión)
❌ Respuesta sugerida como tipo de output — no estaba en ValidationSuboperator
   → Necesita: draft_suggestion como output_type de misión
```

