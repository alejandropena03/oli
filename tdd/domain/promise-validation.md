# Validación de la promesa de valor — "De intención a trabajo terminado"

**Fecha:** 2026-05-26
**Pregunta:** ¿Cómo exactamente la arquitectura propuesta cumple la promesa?
**Formato:** Demostración concreta — no teoría.

---

## La promesa tiene dos partes (del founder)

> **1. Ser capaz de hacer todo lo que un humano haría en un computador**
> **2. Orquestar el mejor cumplimiento de las misiones**

Este documento demuestra que ambas partes están cubiertas con la arquitectura actual.

---

## PARTE 1 — Todo lo que un humano haría en un computador

### El mapa completo de capacidades

```
UN HUMANO EN SU COMPUTADOR PUEDE:

  A. Leer y escribir archivos
  B. Ejecutar código y comandos
  C. Navegar la web y extraer información
  D. Interactuar con aplicaciones web
  E. Controlar el desktop (apps GUI)
  F. Comunicarse (email, mensajes, calendarios)
  G. Gestionar proyectos y notas
  H. Trabajar con datos y bases de datos
  I. Gestionar código y repos
  J. Manejar archivos multimedia
  K. Interactuar con servicios en la nube
  L. Automatizar tareas repetitivas
  M. Buscar información
  N. Hablar y escuchar (voz)
```

Ahora: ¿qué cubre cada capacidad con la arquitectura de Oli?

---

### A. Leer y escribir archivos

**MCP servers disponibles hoy:**
- `@modelcontextprotocol/server-filesystem` — oficial, file read/write/edit/list
- `fast-filesystem-mcp` — operaciones avanzadas
- `Paperless-MCP` — gestión de documentos

**En Oli:** ExecutionSuboperator → `linux_shell` (E2B/subprocess) o `filesystem_mcp`

```
"Oli, lee el contrato que dejé en Descargas y dime las cláusulas importantes"
→ filesystem MCP lee el archivo
→ MarketResearchSuboperator analiza
→ Oli entrega resumen con cláusulas
```

---

### B. Ejecutar código y comandos

**Stack de Oli (ADR-012):**
- V1-V2: subprocess local con allowlist de comandos
- V3+: E2B microVM — Linux completo con cualquier lenguaje

**Lo que puede ejecutar:**
```bash
python script.py          # Python
node app.js               # JavaScript/Node
bun run index.ts          # TypeScript/Bun
bash ./deploy.sh          # Shell scripts
git commit -m "..."       # Git
ffmpeg -i video.mp4 ...   # Multimedia
curl https://api.com      # HTTP
docker run imagen         # Containers
pip install / npm install # Packages
cron jobs                 # Tareas programadas
```

**MCP servers adicionales:**
- `code-executor` — ejecución segura de Python
- `code-sandbox-mcp` — Docker para code execution seguro
- `Docker` — gestión de containers
- `Kubernetes` — orquestación

```
"Oli, corre el script de análisis de datos que está en /scripts/weekly_analysis.py
 y mándame el reporte"
→ linux_shell ejecuta el script
→ Oli lee el output
→ ValidationSuboperator valida que el output tiene el formato correcto
→ Entrega el reporte
```

---

### C. Navegar la web y extraer información

**Stack de Oli (ADR-011):**
- Playwright MCP — scraping determinístico
- Stagehand v3 — extracción AI-híbrida con `extract(schema)`
- chrome-devtools-mcp — acceso al DOM y network

**MCP servers adicionales:**
- `Firecrawl` — web scraping a escala
- `Exa` — search engine para AIs
- `Tavily` — research con extracción
- `Perplexity` — research en tiempo real
- `Bright Data` — web data industrial
- `Apify` — 3,000+ scrapers pre-construidos
- `Jina Reader` — URL → Markdown limpio
- `SearXNG` — meta-búsqueda

```
"Oli, investiga los últimos 3 posts del blog de Anthropic y resume las novedades"
→ Jina Reader convierte URLs a texto
→ MarketResearchSuboperator analiza
→ Oli entrega resumen con fuentes
```

---

### D. Interactuar con aplicaciones web (formularios, clicks, flujos)

**Stack de Oli (ADR-011):**
- Stagehand `act()` — acción natural language en cualquier página
- Stagehand `agent()` — flujo multi-paso autónomo
- Playwright MCP — pasos determinísticos (login conocido, etc.)
- chrome-devtools-mcp — depuración y JavaScript execution

```
"Oli, publica este artículo en mi WordPress y ponle estas etiquetas"
→ Stagehand agent navega a WordPress
→ act("click en Nueva Entrada")
→ act("pega el contenido en el editor")
→ act("agrega las etiquetas X, Y, Z")
→ act("click en Publicar")
→ ValidationSuboperator verifica que el post está publicado
```

---

### E. Controlar el desktop — apps GUI sin API

**Stack de Oli (ADR-012):**
- ClawdCursor MCP — 97 tools, AT-SPI → OCR → screenshot
- computer-use-linux — Linux headless con Wayland

```
"Oli, abre el archivo .sketch que me mandaron y exporta las pantallas como PNG"
→ ClawdCursor detecta Sketch vía AT-SPI
→ act("File → Export")
→ act("selecciona todas las artboards")
→ act("Export PNG")
→ filesystem MCP copia los archivos al destino
```

---

### F. Comunicarse — email, mensajes, calendarios

**MCP servers disponibles:**
- `Gmail / Google Workspace` — email completo + Calendar + Drive + Docs + Sheets
- `Email MCP` — multi-proveedor (Gmail, Outlook, SMTP)
- `IMAP MCP` — lectura de email
- `Slack` — canales, mensajes, archivos
- `Discord` — server interaction
- `Telegram` — bot integration
- `Twilio` — SMS, WhatsApp programático
- `Mailgun` — email transaccional
- `Google Chat` — mensajería corporativa
- `CalDAV` — calendarios genéricos
- `Routine` — calendar + tasks + notes

```
"Oli, revisa mi email de hoy, identifica los urgentes y propón respuestas"
→ IMAP MCP lee el inbox
→ MarketResearchSuboperator clasifica por urgencia
→ Oli propone respuestas por email
→ permission_class 3 → founder aprueba antes de enviar
→ Email MCP envía las respuestas
```

---

### G. Gestionar proyectos y notas

**MCP servers disponibles:**
- `Notion` — oficial, páginas, databases, búsqueda
- `Obsidian` — vault local
- `Linear` — issues, proyectos, sprints
- `Jira` — issue tracking
- `Asana` — task management
- `Trello` — kanban
- `GitHub Projects` — via GitHub MCP
- `Airtable` — bases de datos visuales
- `Apple Notes` — notas nativas macOS
- `HackMD` — notas colaborativas

```
"Oli, crea una página en Notion con el resumen de la reunión de hoy, 
 organizada por decisiones tomadas y action items"
→ Oli genera el contenido estructurado
→ Notion MCP crea la página
→ Notion MCP llena las secciones
→ Oli confirma que está publicado
```

---

### H. Trabajar con datos y bases de datos

**MCP servers disponibles:**
- `PostgreSQL` — queries, schema, operaciones
- `MySQL` — base de datos relacional
- `SQLite` — local lightweight
- `MongoDB` — NoSQL
- `BigQuery` — analytics a escala
- `Supabase` — Postgres + auth + storage
- `Neon` — serverless Postgres
- `ClickHouse` — analytics column store
- `DuckDB` — análisis local
- `Elasticsearch` — búsqueda y analytics
- `Qdrant` / `Milvus` / `Chroma` — vector databases

```
"Oli, analiza la tabla de ventas de este mes y compárala con el mes anterior.
 Dime qué productos bajaron más de 20%"
→ PostgreSQL MCP ejecuta las queries
→ TechnicalArchitectSuboperator analiza los datos
→ Oli entrega el análisis con los productos identificados
```

---

### I. Gestionar código y repositorios

**MCP servers disponibles:**
- `GitHub` — oficial: repos, issues, PRs, actions, commits
- `Git` — operaciones de repo local
- `Semgrep` — análisis de seguridad en código
- `SonarQube` — calidad y seguridad
- `JetBrains` — IDE integration
- `VS Code` — editor integration
- `Postman` — API testing

```
"Oli, revisa los PRs abiertos de mi repo, identifica los que tienen conflictos
 y escribe un comentario explicando qué hay que resolver"
→ GitHub MCP lista los PRs
→ GitHub MCP lee el diff de cada uno
→ TechnicalArchitectSuboperator analiza conflictos
→ GitHub MCP posta los comentarios
→ permission_class 3 → founder aprueba antes de postear
```

---

### J. Multimedia — imágenes, video, audio, documentos

**MCP servers disponibles:**
- `ElevenLabs` — TTS de alta calidad
- `AllVoiceLab` — TTS + cloning de voz
- `VideoDB` — video editing y búsqueda
- `Mux` — video platform
- `Imagician` / `ImageSorcery` — edición de imágenes
- `PaddleOCR` — OCR y parsing de documentos
- `Mureka` — generación de música
- `Pollinations` — generación multimodal
- `AWS Nova Canvas` — generación de imágenes

**Via linux_shell (E2B):**
```bash
ffmpeg -i video.mp4 -ss 00:01:00 -t 30 clip.mp4  # cortar video
convert imagen.png -resize 50% thumbnail.png       # ImageMagick
whisper audio.mp3 --language es                    # transcripción
```

```
"Oli, transcribe el audio de la reunión de hoy y genera un resumen ejecutivo"
→ linux_shell ejecuta Whisper en el archivo de audio
→ Oli recibe la transcripción
→ Oli genera el resumen
→ Oli guarda en Notion (opcional)
```

---

### K. Servicios en la nube

**MCP servers disponibles:**
- `AWS` (Core, Bedrock, Cost Analysis, Documentation, Nova Canvas, CDK)
- `Google Cloud Run` — deploy
- `Cloudflare` — DNS, Workers, Pages
- `Supabase` — backend as a service
- `Render` — deploy de servicios
- `Stripe` — pagos
- `Square` / `PayPal` — pagos alternativos
- `Zapier` — 8,000+ apps via automations
- `Rube` / `Integration App` — 500+ SaaS apps

```
"Oli, despliega la nueva versión del landing a Cloudflare Pages"
→ Git MCP hace el commit del build
→ Cloudflare MCP triggea el deploy
→ ValidationSuboperator verifica que la URL responde 200
→ Oli confirma el deploy exitoso
```

---

### L. Automatizar tareas repetitivas → Playbooks

Esta es la capacidad más diferenciadora de Oli vs. cualquier otra herramienta:

```
Primer run → Oli ejecuta la misión manualmente
Oli detecta que es repetitiva → propone Playbook
Founder aprueba → Playbook guardado
Runs futuros → 1 utterance de voz → Oli ejecuta el playbook
```

**Ejemplos:**
```
"Oli, prepara el reporte semanal"
→ Playbook: weekly_report_v1
  Step 1: BigQuery → métricas de la semana
  Step 2: Google Sheets → actualiza dashboard
  Step 3: Oli genera el texto del reporte
  Step 4: Gmail MCP envía el reporte al equipo
  Tiempo: 8 min | Costo: $0.15 | Tiempo humano ahorrado: 2 hrs
```

---

### M. Búsqueda e investigación

**MCP servers disponibles:**
- `Exa` — search engine para AIs
- `Tavily` — research + extracción
- `Perplexity` — research en tiempo real
- `Brave Search` — búsqueda web
- `SearXNG` — meta-búsqueda privada
- `Firecrawl` — scraping profundo
- `Bright Data` — datos web industriales
- `Apify` — 3,000 scrapers pre-construidos

---

### N. Voz — hablar y escuchar (ADR-013)

**Stack de Oli:**
- Wake word "Oli" → OpenWakeWord (local, privado)
- STT → Whisper.cpp (local) o Whisper API
- TTS → ElevenLabs MCP o sistema
- Respuesta vía voz en el computador

```
Usuario (hablando): "Oli, ¿cuánto cuesta renovar el dominio de mi producto?"
→ Wake word detectado localmente
→ Whisper transcribe
→ Oli: google Domains MCP / web search
→ ElevenLabs TTS responde en voz
Tiempo total: ~8 segundos
```

---

## PARTE 2 — Orquestación del mejor cumplimiento de las misiones

Esto es lo que diferencia a Oli de "solo conectar MCP servers":

### El ciclo que ninguna otra herramienta tiene completo

```
1. INTAKE INTELIGENTE
   → Oli pregunta si hay ambigüedad (ADR-007)
   → Máximo 2 preguntas, con propósito explícito
   → Nunca asume — entiende primero

2. CONTEXTO PERSISTENTE
   → Memory Graph: sabe qué hiciste antes
   → Sabe tus preferencias, tu empresa, tu ICP
   → Recupera misiones similares para aprender de ellas

3. PLANIFICACIÓN
   → Orchestrator genera el plan completo antes de ejecutar
   → Permission classification antes de tocar nada
   → Cost estimate antes de aprobar

4. EJECUCIÓN RESILIENTE (ADR-006)
   → 3 intentos autónomos antes de escalar al founder
   → retry → herramienta alternativa → scope reducido
   → Solo escala cuando realmente no puede solo

5. VALIDACIÓN
   → ValidationSuboperator verifica contra success_criteria
   → No entrega hasta que los criterios se cumplan
   → Si falla: repair automático antes de escalar

6. EVIDENCIA
   → Todo queda registrado: tool calls, fuentes, screenshots
   → El founder puede auditar cada decisión

7. APRENDIZAJE
   → MemoryCuratorSuboperator actualiza memoria automáticamente
   → La tercera vez que haces lo mismo → propone Playbook
   → El Playbook mejora solo (Stagehand auto-caching)
```

### Por qué esto es diferente a usar los MCP servers directamente

```
Usuario con Claude Code (MCP servers directos):
  "Busca los competidores de mi producto"
  → Claude busca
  → Claude entrega texto
  → No recuerda qué dijiste la semana pasada
  → No sabe que prefieres tablas sobre bullets
  → No propone convertirlo en playbook
  → No valida que los criterios se cumplieron
  → No genera un reporte de costo/tiempo

Usuario con Oli:
  "Oli, investiga los competidores"
  → Oli: "¿Para qué lo necesitas — para el pitch deck o para la estrategia de pricing?"
  → Oli recupera: última vez busqué 3 competidores, el founder los rechazó porque faltó pricing
  → Oli planifica 6 pasos incluyendo pricing esta vez
  → Oli ejecuta, falla en un site con paywall, intenta alternativa solo
  → Oli valida que todos tienen pricing documentado
  → Oli entrega en el formato tabla que el founder prefiere
  → Oli propone Playbook: "competitor_research_v1"
  → Reporte: 12 min, $0.18, 3 hrs de trabajo humano ahorradas
```

---

## Mapa visual completo — la arquitectura que lo cubre todo

```
                         USUARIO
                    "Oli, [cualquier cosa]"
                           │
              ┌────────────┴────────────┐
              │ VOZ                     │ UI / texto
              │ OpenWakeWord → Whisper  │
              └────────────┬────────────┘
                           │
              ┌────────────▼────────────────────────────────────┐
              │            OLI MISSION KERNEL                   │
              │  Intake → Intent → Context → Plan → Execute     │
              │  Validate → Deliver → Report → Learn            │
              └──────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────────────────────┐
        │                  │                                  │
  FILESYSTEM          BROWSER / WEB               DESKTOP GUI
  ─────────────        ─────────────              ───────────────
  filesystem MCP       Playwright MCP             ClawdCursor MCP
  linux_shell/E2B      Stagehand v3               AT-SPI → OCR
  Git MCP              chrome-devtools            computer-use-linux
  Paperless MCP        Firecrawl, Exa, Tavily
  Docker MCP
        │                  │                                  │
  COMUNICACIÓN         PRODUCTIVIDAD              DATOS
  ─────────────        ─────────────              ───────────────
  Gmail/Google WS      Notion MCP                 PostgreSQL MCP
  Slack MCP            Linear MCP                 BigQuery MCP
  Email MCP            Jira MCP                   MongoDB MCP
  Twilio MCP           Asana MCP                  Supabase MCP
  ElevenLabs MCP       Obsidian MCP               Qdrant/Chroma
  Calendar MCP         GitHub MCP                 DuckDB MCP
        │                  │                                  │
  CLOUD / INFRA        MULTIMEDIA                 AUTOMATIZACIÓN
  ─────────────        ─────────────              ───────────────
  AWS MCPs             VideoDB MCP                Zapier MCP
  Cloudflare MCP       ElevenLabs MCP             Make MCP
  Render MCP           ImageSorcery MCP           Rube (500+ apps)
  Stripe MCP           PaddleOCR MCP              Playbooks de Oli
  Supabase MCP         Whisper (shell)
```

---

## La cuenta final

**Herramientas conectadas por protocolo:**
- MCP servers oficiales: ~70 producción-ready
- MCP community servers: 500+
- Via linux_shell (E2B): cualquier CLI, cualquier lenguaje, cualquier paquete
- Via ClawdCursor: cualquier app GUI con accessibility API
- Via Stagehand/Playwright: cualquier web
- Via Zapier/Rube MCP: 8,000+ apps adicionales

**Total efectivo: cualquier cosa que tenga una interfaz digital.**

**Lo que Oli agrega encima de todo esto:**
Memoria persistente + planificación + validación + playbooks + voz + evidencia + reporting.

Sin eso, son solo herramientas. Con eso, es un operador que trabaja.
