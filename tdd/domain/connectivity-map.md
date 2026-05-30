# Mapa de conectividad de Oli — Cómo se conecta al mundo

**Fecha:** 2026-05-26
**Principio:** Oli elige el método más eficiente para cada conexión.
**No hay una sola estrategia — hay una jerarquía de decisión.**

---

## La jerarquía de decisión de conectividad

Antes de conectar cualquier herramienta, el Tool Router aplica esta lógica:

```
¿Cómo me conecto a X de la forma más eficiente?

  1. ¿Hay una API directa simple y estable?
     → Script Python / TypeScript directo (más rápido, sin intermediarios)
     → Ejemplo: Notion API, Slack API, GitHub API, Linear API

  2. ¿La tarea es compleja, multi-paso o necesita orquestación visual?
     → n8n (cuando el usuario ya tiene flujos ahí, o para flujos complejos pre-construidos)
     → Webhook trigger de n8n desde Oli

  3. ¿Hay un MCP server oficial y bien mantenido?
     → MCP client directo (para herramientas que exponen MCP de calidad)
     → Ejemplo: GitHub MCP oficial, Playwright MCP, filesystem MCP

  4. ¿Necesita GUI / browser / desktop?
     → Stagehand + Playwright (web)
     → ClawdCursor (desktop GUI)

  5. ¿Necesita shell / código / sistema?
     → linux_shell en E2B / subprocess

  Nunca: Zapier. Nunca: abstracciones que añaden latencia y costo sin valor.
```

---

## Las 4 vías de conectividad de Oli

### VÍA 1 — API directa (la más eficiente — default cuando existe)

Oli habla directamente con la API del servicio. Sin intermediarios, sin MCP de terceros,
sin Zapier. Un script Python o TypeScript que hace exactamente lo que se necesita.

**Cuándo:** La API del servicio es estable, bien documentada, y la tarea es acotada.

**Ejemplos:**
```python
# Notion — crear una página
import httpx
response = httpx.post(
    "https://api.notion.com/v1/pages",
    headers={"Authorization": f"Bearer {NOTION_TOKEN}"},
    json={"parent": {"database_id": DB_ID}, "properties": {...}}
)

# Slack — enviar mensaje
httpx.post("https://slack.com/api/chat.postMessage",
    json={"channel": "#general", "text": "Misión completada ✓"})

# Linear — crear issue
httpx.post("https://api.linear.app/graphql",
    json={"query": "mutation { issueCreate(input: {...}) { issue { id } } }"})

# GitHub — crear PR
httpx.post(f"https://api.github.com/repos/{repo}/pulls",
    json={"title": "...", "head": "branch", "base": "main"})
```

**Herramientas con API directa que Oli usa:**
| Herramienta | API | Para qué |
|---|---|---|
| Notion | REST | Páginas, databases, búsqueda |
| Slack | Web API | Mensajes, canales, archivos |
| GitHub | REST + GraphQL | Repos, PRs, issues, actions |
| Linear | GraphQL | Issues, proyectos, sprints |
| Gmail | Google API | Email, labels, threads |
| Google Calendar | Google API | Eventos, disponibilidad |
| Google Drive | Google API | Archivos, carpetas, permisos |
| Airtable | REST | Tablas, registros, vistas |
| Stripe | REST | Pagos, clientes, suscripciones |
| Jira | REST | Issues, sprints, boards |
| Asana | REST | Tasks, proyectos |
| HubSpot | REST | CRM, deals, contacts |
| Figma | REST | Archivos, componentes |
| Vercel | REST | Deploys, proyectos |
| Cloudflare | REST | DNS, Workers, Pages |
| OpenAI | REST | Modelos, embeddings |
| Anthropic | SDK | Claude (ya integrado) |
| Twilio | REST | SMS, WhatsApp, voz |
| Sendgrid | REST | Email transaccional |
| Supabase | REST + SDK | DB, auth, storage |
| AWS | SDK | Toda la plataforma |

**Cómo Oli gestiona las credenciales:**
```typescript
// secrets.ts — nunca en código, siempre en variables de entorno o secret store
const credentials = {
  notion: process.env.NOTION_TOKEN,
  slack: process.env.SLACK_BOT_TOKEN,
  github: process.env.GITHUB_TOKEN,
  // ...
}
// En V3+: Secrets MCP server (HashiCorp Vault, AWS Secrets Manager)
// El usuario conecta sus credenciales una vez — Oli las usa cuando necesita
```

---

### VÍA 2 — n8n (cuando ya existe el flujo o es complejo)

n8n es una herramienta legítima para flujos complejos con muchos nodos visuales,
lógica condicional compleja, o cuando el usuario ya tiene flujos construidos.

**Cuándo usa Oli n8n:**
- El usuario ya tiene flujos en n8n que funcionan → Oli los triggea via webhook
- El flujo involucra 10+ servicios con lógica compleja → n8n es más eficiente que construirlo
- El flujo necesita mantenimiento visual por el usuario → n8n tiene mejor UI para eso

**Cuándo NO usa Oli n8n:**
- Para cosas simples que un API call resuelve en 3 líneas
- Cuando añade latencia innecesaria (n8n → webhook → servicio vs. API directa)
- Cuando crea una dependencia de infra que el usuario tiene que mantener

**Cómo se integra:**
```typescript
// Oli triggea un flujo de n8n via webhook
const n8nTool = tool(
  "n8n_trigger",
  "Triggea un workflow de n8n via webhook",
  {
    webhook_url: z.string().url(),
    payload: z.record(z.unknown()),
  },
  async ({ webhook_url, payload }) => {
    const response = await fetch(webhook_url, {
      method: "POST",
      body: JSON.stringify(payload)
    })
    return await response.json()
  }
)

// También: Oli puede leer el output de un flujo de n8n
// También: n8n puede trigear misiones en Oli via webhook
```

**Casos de uso donde n8n tiene sentido:**
```
- Sincronización bidireccional CRM ↔ Notion (ya que n8n tiene nodos nativos)
- ETL complejo de múltiples fuentes de datos
- Flujos de aprobación multi-persona con lógica condicional
- Integraciones legacy que requieren transformación compleja de datos
```

---

### VÍA 3 — MCP server (para herramientas que lo exponen bien)

MCP es el protocolo estándar — pero no todos los MCP servers de terceros son buenos.
Oli usa MCP cuando el server es oficial, bien mantenido, y agrega valor real.

**MCP servers que Oli usa (curados, producción-ready):**

| MCP Server | Organización | Por qué MCP y no API directa |
|---|---|---|
| `@playwright/mcp` | Microsoft (oficial) | Playwright requiere control de browser — MCP es la interfaz natural |
| `stagehand-mcp` | Browserbase | Stagehand tiene lógica AI interna que va más allá de un API call |
| `chrome-devtools-mcp` | Google (oficial) | CDP es complejo — el MCP server lo abstrae bien |
| `@modelcontextprotocol/server-filesystem` | Anthropic (oficial) | Control de acceso configurable que un script directo no tiene |
| `@modelcontextprotocol/server-memory` | Anthropic (oficial) | Knowledge graph persistente — es una implementación completa |
| `@modelcontextprotocol/server-fetch` | Anthropic (oficial) | Fetch + conversión a Markdown optimizado para LLM |
| `clawdcursor` | AmrDab | Desktop GUI — requiere IPC con el OS, MCP es la interfaz correcta |
| `computer-use-linux` | agent-sh | Control de Linux headless — igual que arriba |
| `github-mcp` | GitHub (oficial) | GitHub lo mantiene — confiable |
| `exa-mcp` | Exa | Search API con lógica específica de Exa |
| `firecrawl-mcp` | Firecrawl | Scraping con rate limiting y gestión de sesiones |

**Criterio para elegir MCP vs. API directa:**
```
Usar MCP cuando:
  ✅ La organización que mantiene el servicio mantiene el MCP server
  ✅ El MCP server hace más que wrappear el API (añade lógica, manejo de estado)
  ✅ El protocolo MCP es más natural para esa categoría (browser, filesystem, desktop)

No usar MCP cuando:
  ❌ El MCP server es un wrapper delgado de una API REST simple
  ❌ El MCP server lo mantiene un tercero random — puede desaparecer
  ❌ Una llamada directa al API es más rápida y confiable
```

---

### VÍA 4 — linux_shell / E2B (para todo lo demás)

Cuando no hay API, no hay MCP server bueno, no hay n8n — hay una shell.
Un Linux completo puede hacer cualquier cosa que tenga una interfaz de línea de comandos.

```bash
# Transcripción de audio
whisper meeting.mp3 --language es --output_format txt

# Procesamiento de video
ffmpeg -i raw_video.mp4 -vf "scale=1280:720" -c:a copy output.mp4

# Web scraping básico
curl -s https://example.com | python -c "import sys,bs4; ..."

# Análisis de datos
python -c "import pandas as pd; df = pd.read_csv('data.csv'); print(df.describe())"

# Git operations complejas
git log --oneline --since="1 week ago" | head -20

# Cualquier CLI instalable
npm install -g lighthouse && lighthouse https://miproducto.com

# Scripts propios del usuario
python ~/scripts/weekly_report.py --format=markdown
```

**E2B en V3+:** El usuario tiene un Linux persistente. Oli puede instalar herramientas,
mantener estado entre misiones, y tener el entorno configurado exactamente como el usuario necesita.

---

## Mapa completo: "¿Sería todo?"

La respuesta honesta: **con estas 4 vías, sí — cualquier cosa con interfaz digital.**

Pero hay 3 cosas que faltan en el diseño actual y son críticas:

### Gap 1 — Auth y credenciales (el problema más importante)

**El problema:** El usuario tiene 20 servicios con credenciales distintas.
¿Cómo Oli las gestiona sin que el founder tenga que pasarle tokens manualmente cada vez?

**La solución correcta:**

```
V1-V2: .env file con variables de entorno
  → Simple, el founder técnico lo entiende
  → No ideal para founders no técnicos

V3+: Secrets Manager integrado en Oli
  → UI de configuración: "Conecta tu Notion" → OAuth flow
  → Oli guarda el token de forma segura
  → El usuario conecta servicios como conectaría una app normal
  → Renovación automática de tokens OAuth

Implementación:
  @modelcontextprotocol/server-secrets (Anthropic oficial) para V1
  OAuth2 flow propio de Oli para V3+
```

### Gap 2 — Descubrimiento de herramientas

**El problema:** El usuario no sabe qué herramientas tiene Oli disponibles.

**La solución:**

```
Tool Registry UI (en la UI de Oli):
  ├── Conectadas y activas ✅
  ├── Disponibles para conectar (con OAuth flow) 🔗
  └── Sugeridas según el tipo de trabajo del usuario 💡

Oli también puede sugerir: "Para esta misión necesitarías conectar Notion.
¿Lo conecto ahora? [Sí / No]"
```

### Gap 3 — El usuario no técnico vs. el técnico

**El problema:** Ambos deben poder usar Oli desde V1.

**La solución:**

```
Founder técnico:
  → Configura MCP servers via config.json (como Claude Code hoy)
  → Pasa credenciales via .env
  → Puede escribir scripts Python propios que Oli ejecuta
  → Acceso completo a linux_shell en E2B

Founder no técnico:
  → UI de onboarding: "¿Qué usas?" → selecciona Notion, Slack, Gmail
  → OAuth flows para conectar cada servicio
  → Oli sugiere qué conectar según las misiones que crea
  → Nunca ve un MCP server, un token, o una línea de código
```

---

## El stack completo de conectividad — definitivo

```
┌─────────────────────────────────────────────────────────────────────┐
│                    TOOL ROUTER DE OLI                               │
│                                                                     │
│  Para cada acción, elige en este orden de eficiencia:              │
│                                                                     │
│  1. API directa (script TS/Python)     → más rápido, más control  │
│  2. n8n webhook                        → flujos ya existentes      │
│  3. MCP server oficial                 → cuando añade valor real   │
│  4. linux_shell / E2B                  → cualquier CLI             │
│  5. Stagehand / Playwright             → cualquier web             │
│  6. ClawdCursor                        → cualquier GUI             │
│                                                                     │
│  NUNCA: Zapier. NUNCA: wrappers de wrappers de wrappers.          │
└─────────────────────────────────────────────────────────────────────┘

                    CREDENCIALES
                    ───────────
                    V1: .env / config.json
                    V3+: OAuth UI + Secrets Manager
                    Regla: el usuario conecta una vez, Oli las usa siempre

                    PARA AMBOS PERFILES
                    ──────────────────
                    Técnico: config.json + .env + E2B shell
                    No técnico: UI de onboarding + OAuth flows
```

---

## ¿Sería todo?

**Sí, con un matiz:** el límite de Oli no es qué herramientas puede conectar —
puede conectar cualquier cosa con interfaz digital.

El límite real es la **configuración inicial** — el usuario tiene que conectar sus servicios.
Y eso es un problema de UX de onboarding, no de capacidad técnica.

La misión de V3 es que conectar una herramienta sea tan fácil como en cualquier app:
"Conecta tu Notion" → click → OAuth → listo. Oli la usa en misiones sin más configuración.
