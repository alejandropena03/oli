# Catálogo de herramientas de Oli

**Fecha:** 2026-05-26
**Propósito:** Definir cuáles son las herramientas mínimas sin las que Oli no puede cumplir su promesa, con un ejemplo concreto de qué hace cada una posible.

---

## HERRAMIENTAS NÚCLEO — Sin estas no hay producto

Estas son las que Oli necesita desde V0-V1 para cumplir la promesa básica. El usuario no puede prescindir de ellas.

---

### 1. ChromaDB (vector store local)
**Por qué es núcleo:** Sin esto, Oli no tiene memoria. Cada misión empieza desde cero.
**Qué hace:** Guarda todo lo que Oli aprende como embeddings. Recupera lo relevante para cada misión.

**Ejemplo concreto:**
```
Founder: "Oli, escríbele a María sobre la reunión"
         ↓
Sin ChromaDB: Oli no sabe quién es María.

Con ChromaDB: Oli recupera en <100ms:
  - María Rodríguez, CMO de Acme Corp
  - Última reunión: hace 2 semanas, habló de presupuesto Q3
  - Tono de comunicación preferido: formal, directo
  - Su email: m.rodriguez@acme.com
  
  → Oli escribe el email correcto sin preguntar nada.
```

---

### 2. Filesystem MCP (leer/escribir archivos)
**Por qué es núcleo:** El 80% del trabajo de un humano en un computador involucra archivos.
**Qué hace:** Oli puede leer, crear, editar, mover y organizar archivos en el computador del usuario.

**Ejemplo concreto:**
```
"Oli, analiza el contrato que está en mi Descargas"
→ filesystem MCP lee el PDF
→ Oli extrae cláusulas importantes
→ Crea un resumen en /Documents/Contratos/acme_resumen.md
```

---

### 3. Linux shell / subprocess
**Por qué es núcleo:** Cualquier cosa que no tiene API ni MCP, tiene CLI.
**Qué hace:** Oli ejecuta comandos reales en el sistema operativo.

**Ejemplo concreto:**
```
"Oli, convierte todos los videos de esta carpeta a MP4"
→ linux_shell ejecuta:
  for f in *.mov; do ffmpeg -i "$f" "${f%.mov}.mp4"; done
→ 47 videos convertidos en 3 minutos
→ Oli informa: "Listo. 47 videos convertidos. Total: 12.3GB → 8.1GB"
```

---

### 4. Web search + fetch (Exa o Tavily)
**Por qué es núcleo:** La información del mundo vive en la web. Sin esto, Oli no puede investigar.
**Qué hace:** Busca en la web y extrae contenido de páginas con comprensión semántica.

**Ejemplo concreto:**
```
"Oli, ¿cuál es el pricing actual de Notion?"
→ Exa busca "Notion pricing 2026"
→ fetch extrae la página de precios
→ Oli responde: "Notion tiene 3 planes: Free ($0), Plus ($10/mes), Business ($18/mes)..."
→ Fuente: notion.so/pricing — verificado hoy
```

---

### 5. Email — Gmail API o IMAP/SMTP
**Por qué es núcleo:** El email es el canal de comunicación de trabajo más usado.
**Qué hace:** Leer inbox, clasificar, redactar, enviar. Con aprobación del founder antes de enviar (clase 3).

**Ejemplo concreto:**
```
"Oli, revisa mi email y respóndele a los clientes que llevan más de 24h esperando"
→ IMAP lee inbox → identifica 3 emails sin respuesta > 24h
→ Redacta respuestas personalizadas con contexto de cada contacto (de ChromaDB)
→ Muestra los 3 borradores al founder
→ Founder aprueba → Gmail API envía
```

---

### 6. Calendar (Google Calendar API)
**Por qué es núcleo:** Agenda = tiempo = el recurso más valioso del founder.
**Qué hace:** Leer disponibilidad, crear eventos, proponer horarios, recordatorios.

**Ejemplo concreto:**
```
"Oli, agenda una reunión con Juan esta semana"
→ Calendar API: verifica disponibilidad del founder y de Juan (si tiene acceso)
→ Propone: "Jueves 3pm o viernes 10am. ¿Cuál prefieres?"
→ Founder: "Jueves" → crea evento + Google Meet link + envía invitación a Juan
```

---

### 7. GitHub API
**Por qué es núcleo:** Para founders técnicos, el código es donde vive el producto.
**Qué hace:** Leer repos, crear issues, revisar PRs, hacer commits, gestionar releases.

**Ejemplo concreto:**
```
"Oli, revisa los PRs abiertos y dime cuáles tienen conflictos"
→ GitHub API lista todos los PRs abiertos
→ Para cada uno: lee el diff, detecta archivos en conflicto
→ Responde: "3 PRs tienen conflictos: PR #47 (auth.ts), PR #52 (api/users.ts)..."
→ "¿Quieres que comente en cada uno qué hay que resolver?"
```

---

### 8. Playwright MCP (browser automation)
**Por qué es núcleo:** Hay miles de servicios que solo tienen interfaz web, sin API.
**Qué hace:** Navega páginas, hace clicks, llena formularios, extrae datos.

**Ejemplo concreto:**
```
"Oli, sube este artículo a mi WordPress"
→ Playwright navega a /wp-admin/post-new.php
→ Pega el contenido en el editor
→ Configura categorías y tags
→ Click en "Publicar"
→ Verifica que el post está en línea y retorna la URL
```

---

### 9. Whisper (STT — Speech to Text)
**Por qué es núcleo:** La voz es la interfaz más natural. Sin esto no hay wakeword.
**Qué hace:** Convierte audio a texto con precisión alta en español e inglés.

**Ejemplo concreto:**
```
Founder (hablando): "Oli, ¿cuánto costó la misión de esta mañana?"
→ Whisper.cpp transcribe en ~300ms (local)
→ Oli consulta Mission Memory
→ ElevenLabs responde en voz: "La misión de research de esta mañana costó $0.18 y tomó 11 minutos"
```

---

### 10. ElevenLabs TTS (Text to Speech)
**Por qué es núcleo:** Si Oli escucha por voz, también debe responder por voz.
**Qué hace:** Convierte texto a audio con voz natural configurada por el usuario.

**Ejemplo concreto:**
```
Misión bloqueada mientras el founder está en reunión →
→ Oli detecta momento apropiado (entre reuniones, según Calendar)
→ ElevenLabs: "Tengo un problema con la tarea de deploy. El servidor no responde. ¿Quieres que lo reintente en 30 minutos o lo escalo ahora?"
→ Founder responde verbalmente → Whisper capta → Oli actúa
```

---

## HERRAMIENTAS DE SEGUNDA CAPA — Muy importantes, el usuario las elige

Estas herramientas son necesarias según el flujo de trabajo del usuario. No todas son requeridas por todos, pero la mayoría de founders las usarán.

---

### 11. Notion API
**Cuándo:** El founder usa Notion para gestión de proyectos, notas o wiki.

**Ejemplo:**
```
"Oli, actualiza el roadmap de Notion con la decisión que tomamos hoy"
→ Notion API busca la página del roadmap
→ Agrega la entrada con fecha, decisión y contexto
→ "Agregado. ¿Quieres que también lo anote en la bitácora de decisiones?"
```

---

### 12. Slack API
**Cuándo:** El equipo usa Slack.

**Ejemplo:**
```
"Oli, avísale al equipo que el deploy de hoy se pospone"
→ Slack API: mensaje en #engineering
→ "El deploy de hoy (v2.3.1) se pospone a mañana 9am. Motivo: tests de integración fallando. /oli"
→ Clase 3 → el founder aprueba el mensaje antes de enviarlo
```

---

### 13. Linear / Jira API
**Cuándo:** El equipo usa Linear o Jira para gestión de tareas.

**Ejemplo:**
```
"Oli, crea los issues para el sprint de la próxima semana basándote en el roadmap"
→ Notion API lee el roadmap (feature prioritizadas)
→ Linear API crea un issue por feature con estimación y descripción
→ "Creé 8 issues en el sprint. ¿Quieres asignarlos o los dejo sin asignar?"
```

---

### 14. n8n (webhook trigger)
**Cuándo:** El usuario ya tiene flujos en n8n o necesita automatizaciones complejas multi-servicio.

**Ejemplo:**
```
"Oli, cuando llegue un lead nuevo de HubSpot, notifícame y crea el deal en Linear"
→ Oli crea el trigger en n8n via webhook
→ n8n maneja la sincronización HubSpot → Linear
→ Oli recibe el webhook de notificación y avisa al founder
```

---

### 15. OpenClaw (voz + canales) — opt-in
**Cuándo:** El usuario quiere usar WhatsApp, Telegram u otros canales para dar misiones a Oli.

**Ejemplo:**
```
Founder desde WhatsApp: "Oli, ¿cuántas misiones tengo activas?"
→ OpenClaw recibe → pasa a Oli
→ Oli: "Tienes 2 activas: el reporte semanal (70% completo) y el deploy de Cloudflare (esperando aprobación)"
→ OpenClaw entrega la respuesta en WhatsApp
```

---

## HERRAMIENTAS OPCIONALES — El usuario decide si las necesita

Estas se agregan según el tipo de trabajo del usuario. Oli las sugiere cuando detecta que serían útiles.

| Herramienta | Para qué | Cuándo sugerirla |
|---|---|---|
| Google Sheets API | Análisis de datos, dashboards | Cuando el founder trabaja con spreadsheets |
| HubSpot API | CRM, deals, contactos | Cuando hay proceso de ventas estructurado |
| Stripe API | Pagos, suscripciones, métricas | Cuando hay SaaS con revenue |
| Cloudflare API | DNS, Workers, Pages, deploys | Cuando el producto usa Cloudflare |
| Docker / K8s | Containers, deploys | Para founders técnicos con infra propia |
| BigQuery / PostgreSQL | Analytics, queries a datos | Cuando hay base de datos relevante |
| Figma API | Diseño, assets, componentes | Para founders que trabajan con diseñadores |
| Twilio API | SMS, WhatsApp programático | Para comunicación masiva o alertas |
| ClawdCursor (desktop GUI) | Apps sin API ni CLI | Cuando Oli necesita controlar el desktop |

---

## La regla de extensión

El catálogo de herramientas opcionales es abierto e ilimitado. Si una herramienta tiene:
- Una API REST documentada → Oli puede conectarse directamente
- Un MCP server oficial → Oli lo consume via Tool Router
- Solo CLI → Oli la usa via linux_shell
- Solo interfaz web → Stagehand o Playwright
- Solo GUI de escritorio → ClawdCursor

**El usuario nunca está limitado por lo que Oli "soporta nativamente". Si existe una interfaz digital, Oli puede usarla.**
