# ADR-013 — Integración con OpenClaw: presencia local de Oli

**Estado:** accepted
**Fecha:** 2026-05-26
**Deciders:** Alejandro Peña (founder) — decisión explícita
**Principio:** Oli no compite con herramientas que resuelven bien su dominio — las integra.
**Versión:** 3 — arquitectura corregida tras research de riesgos reales de OpenClaw.

---

## Contexto

La visión del founder es clara:
> **"El usuario dice 'Oli' y Oli está ahí — escucha, responde, ejecuta."**

Eso no es una notificación en WhatsApp. Es presencia local. Es un asistente que vive
en el computador, siempre escuchando, que responde con voz y que puede hacer cosas reales.

Construir eso from scratch implica:
- Wake word detection (Porcupine / OpenWakeWord)
- VAD (Voice Activity Detection) con thresholds configurables
- STT local (Whisper.cpp) o en la nube (OpenAI Whisper API)
- TTS (ElevenLabs, sistema, local)
- Pipeline de audio cross-platform (macOS, Linux, Windows)
- Permisos de micrófono, accesibilidad, input monitoring por OS

**OpenClaw ya tiene todo esto construido, mantenido por 361K+ contributors.**

OpenClaw es la **capa de presencia local de Oli** — el sistema que hace que Oli viva
en el computador del usuario sin que tenga que abrir ninguna app.

---

## Qué tiene OpenClaw que Oli necesita (Mayo 2026)

### 1. Voice Wake — el núcleo de la presencia

```
Pipeline de voz de OpenClaw:
  1. Wake word detection local (Porcupine o OpenWakeWord)
     → Escucha continuamente sin enviar audio a la nube
     → Wake word configurable: "Oli", "Hey Oli", lo que quiera el usuario
     → Sensibilidad ajustable (0.0 - 1.0)

  2. VAD Recording (Voice Activity Detection)
     → Detecta cuándo el usuario terminó de hablar
     → Graba solo la utterance relevante

  3. STT (Speech-to-Text)
     → Opción local: Whisper.cpp (privacidad total)
     → Opción cloud: OpenAI Whisper API (más rápido)
     → Soporte multi-idioma (español incluido)

  4. Procesamiento → Oli (via MCP)
     → El texto transcrito llega a Oli como raw_input de misión
     → source: "voice_local"

  5. TTS (Text-to-Speech)
     → ElevenLabs (voz natural, configurable)
     → Sistema TTS (fallback gratuito)
     → La respuesta de Oli se lee en voz alta
```

### 2. 26 Tools built-in que Oli hereda

OpenClaw no es solo mensajería. Tiene **26 tools** que Oli puede usar directamente:

| Categoría | Tools | Lo que Oli puede hacer |
|---|---|---|
| **Filesystem** | read, write, edit | Leer/escribir archivos del usuario |
| **Shell** | bash, process | Ejecutar comandos en el OS del usuario |
| **Browser** | browser | Controlar Chrome — click, fill, screenshot, CDP attach |
| **Scheduling** | cron | Misiones programadas ("todos los lunes a las 8am") |
| **Events** | webhooks, Gmail Pub/Sub | Reaccionar a eventos externos |
| **Sesiones** | sessions_list, sessions_history | Ver historial de conversaciones |
| **Canvas** | canvas | Workspace visual con A2UI controls |
| **Canales** | 23+ platforms | WhatsApp, Telegram, Slack, Discord, Signal... |

### 3. 13,700+ Skills en ClawHub

OpenClaw tiene un ecosistema de skills que Oli puede invocar:
- **Obsidian, Notion, Apple Notes, Bear** — gestión de notas
- **Google Workspace** (Gmail, Calendar, Drive, Docs, Sheets)
- **cron-backup** — backups automáticos
- **Lobster** — orquestación de workflows multi-agente
- Y 13,690+ más — cualquier integración que el usuario ya use

### 4. Lobster — orquestación de workflows

OpenClaw tiene su propio motor de orquestación multi-agente llamado **Lobster**:
- Multi-step, multi-agent automations
- Sub-agent delegation
- Cada step puede correr bajo un agente diferente con herramientas distintas

Oli no compite con esto — lo usa como executor cuando la misión lo requiere.

---

## Decisión: OpenClaw como capa de presencia local de Oli

### Arquitectura de integración

```
┌─────────────────────────────────────────────────────────────────┐
│                   USUARIO EN SU COMPUTADOR                     │
│                                                                 │
│   "Oli, investiga los competidores de X"                       │
│         ↓ (voz)                                                 │
└─────────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                    OPENCLAW                                     │
│  Presencia local — siempre activo en el computador             │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Wake word: "Oli" → VAD → Whisper STT → texto            │   │
│  └──────────────────────────────┬──────────────────────────┘   │
│                                 │                               │
│  ┌──────────────────────────────▼──────────────────────────┐   │
│  │ 26 Tools: filesystem, shell, browser, cron, webhooks    │   │
│  │ 13,700+ Skills: Notion, Gmail, Calendar, Drive...       │   │
│  │ Lobster: workflows multi-step                           │   │
│  └──────────────────────────────┬──────────────────────────┘   │
│                                 │ MCP                           │
└────────────────────────────────-┼───────────────────────────────┘
                                  │
┌─────────────────────────────────▼───────────────────────────────┐
│                       OLI MISSION KERNEL                        │
│                                                                 │
│  raw_input: "investiga los competidores de X"                  │
│  source: "voice_local"                                          │
│                                                                 │
│  → InterpretIntent                                              │
│  → RetrieveContext (Memory Graph)                               │
│  → CreatePlan                                                   │
│  → Execute (usa tools de OpenClaw via MCP cuando necesita)     │
│  → Validate                                                     │
│  → Deliver                                                      │
│         │                                                       │
│         └── resultado → OpenClaw → TTS → voz al usuario        │
└─────────────────────────────────────────────────────────────────┘
```

### Qué hace OpenClaw vs. qué hace Oli

| Responsabilidad | OpenClaw | Oli |
|---|---|---|
| Escuchar la wakeword | ✅ | — |
| STT (voz → texto) | ✅ | — |
| TTS (texto → voz) | ✅ | — |
| Acceso a filesystem, shell, browser | ✅ (tools) | vía OpenClaw MCP |
| Skills de terceros (Notion, Gmail...) | ✅ (13,700+) | vía OpenClaw MCP |
| Misiones programadas (cron) | ✅ | puede triggear via OpenClaw |
| **Ciclo de vida de la misión** | — | ✅ |
| **Memory Graph** | — | ✅ |
| **Validación de outputs** | — | ✅ |
| **Permission model** | — | ✅ |
| **Playbooks** | — | ✅ |
| **Evidence + reporting** | — | ✅ |

**OpenClaw es el sistema nervioso periférico de Oli — percepción y acción.**
**Oli es el cerebro — razonamiento, memoria, misiones, validación.**

---

## El wake word es "Oli"

Configuración en OpenClaw:

```json
{
  "voicewake": {
    "engine": "openwakeword",
    "keyword": "oli",
    "sensitivity": 0.7,
    "stt": {
      "engine": "whisper",
      "model": "medium",
      "local": true,
      "language": "es"
    },
    "tts": {
      "engine": "elevenlabs",
      "voice_id": "oli_voice_id",
      "fallback": "system"
    }
  }
}
```

El usuario puede entrenar el wake word con OpenWakeWord para que responda
específicamente a **su voz** diciendo "Oli" — no a cualquiera que lo diga.

---

## Casos de uso concretos

### 1. Misión por voz desde el escritorio
```
Usuario (trabajando): "Oli, prepara un resumen del documento que acabo de editar"
    ↓ OpenClaw detecta wakeword → STT
    ↓ Oli recibe: {source: "voice_local", raw_input: "prepara un resumen..."}
    ↓ Oli: RetrieveContext → ve que hay un archivo .docx recién modificado
    ↓ Oli lee el archivo (via OpenClaw filesystem tool) → genera resumen
    ↓ OpenClaw TTS: "Listo. El resumen tiene 3 puntos clave: ..."
```

### 2. Consulta rápida mientras trabaja
```
Usuario: "Oli, ¿cuánto va a costar la misión de investigación que dejé corriendo?"
    ↓ Oli: RetrieveContext → Mission en estado executing
    ↓ Oli: "Va en el step 3 de 5. Costo estimado $0.08. Termina en ~4 minutos."
    ↓ OpenClaw TTS responde en voz
    [El usuario nunca abrió la UI de Oli]
```

### 3. Aprobación de plan por voz
```
Oli: (TTS) "Preparé el plan para tu misión de hoy. 6 pasos, 15 minutos, $0.15.
     Incluye enviar un email a tu cliente. ¿Apruebo?"
Usuario: "Sí, adelante"
    ↓ OpenClaw STT → Oli CMD: ApprovePlan
    ↓ Misión continúa sin que el founder toque el teclado
```

### 4. Misión por voz + herramientas de OpenClaw
```
Usuario: "Oli, agrega al Notion de proyectos que terminé el diseño de la marca"
    ↓ Oli crea misión → plan: [usar Notion skill de OpenClaw]
    ↓ Oli invoca: openclaw_skill("notion", {action: "add_entry", ...})
    ↓ OpenClaw ejecuta la Notion skill
    ↓ Oli valida → "Listo, agregado al Notion"
    ↓ TTS responde
```

### 5. Oli como asistente de fondo
```
Cron (via OpenClaw): 9:00 AM todos los días
    → Oli Mission: "prepara el brief del día — tareas pendientes, emails importantes, calendario"
    → Oli ejecuta en background mientras el usuario prepara el café
    → TTS: "Buenos días. Tienes 3 reuniones, 2 emails urgentes, y la misión de ayer
            entregó el análisis de competidores. ¿Lo reviso ahora?"
```

---

## Permission classes de las acciones de OpenClaw

| Acción | Clase | Razón |
|---|---|---|
| Escuchar wakeword + STT | 0 | Solo lectura — audio procesado localmente |
| TTS (responder en voz) | 0 | Read/draft — output propio de Oli |
| Usar filesystem tool de OpenClaw | 0-1 | Según si lee (0) o escribe (1) |
| Usar browser tool de OpenClaw | 0-2 | Según si navega (0) o interactúa (2) |
| Usar skills de terceros (Notion, Gmail) | 1-3 | Según impacto de la acción |
| Enviar comunicación por canal | 3 | Comunicación externa |
| Acciones destructivas via shell | 4 | Siempre confirmación explícita |

**Regla crítica:** El permission model de Oli rige sobre todas las acciones de OpenClaw.
OpenClaw no puede ejecutar nada que Oli no haya autorizado según sus clases de permiso.
OpenClaw es el ejecutor — Oli es el que decide qué se puede ejecutar.

---

## Stack técnico de la integración

```
OpenClaw (Node.js, TypeScript, local)
  ↓ expone MCP server
Tool Router de Oli
  ↓ consume como MCP client
Mission Kernel / ExecutionSuboperator
```

**Configuración mínima V1:**
```typescript
// En tool-registry.ts
{
  name: "openclaw_execute",
  transport: "mcp",
  mcp_config: { server_name: "openclaw", tool_name: "execute" },
  permission_class: 1, // default — sube según la acción
},
{
  name: "openclaw_speak",
  transport: "mcp",
  mcp_config: { server_name: "openclaw", tool_name: "tts_speak" },
  permission_class: 0,
},
{
  name: "openclaw_skill",
  transport: "mcp",
  mcp_config: { server_name: "openclaw", tool_name: "skill_invoke" },
  permission_class: 1, // varía por skill
}
```

---

## Versión de disponibilidad

| Versión | Capacidades de OpenClaw en Oli |
|---|---|
| **V0** | No — foco en Mission Kernel core |
| **V1** | Wake word "Oli" → texto → Mission Kernel → TTS respuesta |
| **V2** | + Filesystem y shell via OpenClaw tools. Oli puede leer/escribir archivos por voz |
| **V3** | + Browser tool. + Skills de ClawHub (Notion, Gmail, Calendar, Drive) |
| **V4+** | + Cron missions. + Lobster workflows. + Multi-canal completo |

---

## Por qué no construir esto en Oli from scratch

| Componente | Tiempo de build propio | Con OpenClaw |
|---|---|---|
| Wake word detection cross-platform | 3-4 semanas | 0 — ya existe |
| STT pipeline (Whisper local + cloud) | 2 semanas | 0 — ya existe |
| TTS con ElevenLabs + fallback | 1 semana | 0 — ya existe |
| 13,700+ Skills (Notion, Gmail, etc.) | Nunca | 0 — ya existe |
| Mantenimiento de integraciones | Permanente | Comunidad de 361K |

**Total ahorrado:** meses de desarrollo en componentes que no son el diferenciador de Oli.
El diferenciador de Oli es el Mission Kernel, la memoria, la validación y los playbooks —
no el pipeline de audio.

---

## Riesgos reales de OpenClaw (investigados Mayo 2026)

### Inestabilidad documentada
- **Abril 2026**: actualización 2026.4.26 rompió Discord, Telegram, WhatsApp y automaciones
  de miles de usuarios simultáneamente — sin migration guide, sin rollback fácil
- **Marzo 2026**: 13 releases en un mes con 9 CVEs. Ritmo de cambio muy alto
- El team reconoció el problema — están "haciendo el core más pequeño" (señal positiva
  pero indica que la arquitectura actual tiene problemas de acoplamiento)

### Vulnerabilidades de seguridad documentadas
- 40,214 instancias expuestas en internet con autenticación débil (Feb 2026)
- **CVE-2026-32922**: un API call → control total + RCE — "más severo en la historia de OpenClaw"
- CVE-2026-24763: command injection
- CVE-2026-26322: SSRF
- CVE-2026-26329: path traversal → lectura de archivos locales
- CVE-2026-30741: prompt injection → RCE
- **ClawHavoc campaign**: 824 skills maliciosos en ClawHub robando wallets y passwords

### Conclusión de riesgo
OpenClaw tiene un modelo de seguridad débil (full host access por defecto) y una historia
reciente de vulnerabilidades críticas. **Oli NO puede depender de OpenClaw para funcionar.**

---

## La regla de oro: Oli funciona solo. OpenClaw es opcional.

```
❌ MAL — dependencia dura:
   Oli requiere OpenClaw → si OpenClaw rompe, Oli rompe

✅ BIEN — integración opcional via interfaz abstracta:
   Oli tiene su propia VoiceInterface
   OpenClaw implementa esa interfaz si está instalado
   Cualquier alternativa puede implementar la misma interfaz
   Sin OpenClaw, Oli funciona via UI directa
```

---

## Arquitectura corregida: VoiceInterface abstracta

Oli define su propia interfaz de presencia local. OpenClaw es una implementación posible,
no la única:

```typescript
// Contrato que cualquier proveedor de voz debe implementar
interface OliVoiceInterface {
  // Activación
  startListening(): Promise<void>
  stopListening(): Promise<void>

  // STT
  onWakeWord(callback: (utterance: string) => void): void

  // TTS
  speak(text: string, options?: SpeakOptions): Promise<void>

  // Herramientas del OS (filesystem, shell, browser)
  getToolRegistry(): ToolDefinition[]
  executeTool(name: string, params: unknown): Promise<unknown>
}

// Implementaciones posibles:
class OpenClawAdapter implements OliVoiceInterface { ... }    // Si tiene OpenClaw
class NativeVoiceAdapter implements OliVoiceInterface { ... } // Sin dependencias externas
class MockVoiceAdapter implements OliVoiceInterface { ... }   // V0/testing
```

### Implementaciones por proveedor

| Proveedor | Cuándo usar | Riesgo |
|---|---|---|
| **OpenClawAdapter** | Usuario ya tiene OpenClaw instalado | Medio — monitorear CVEs |
| **NativeVoiceAdapter** | Sin dependencias externas — Oli lo construye | Bajo — controlado |
| **clawd-voice** | Si OpenClaw falla, alternativa directa mismo stack | Bajo |
| **MockVoiceAdapter** | V0 y testing | Cero |

### NativeVoiceAdapter — lo que Oli construye propio (V2)

No es construir todo from scratch. Es un adapter mínimo con componentes estables:

```
Wake word:  OpenWakeWord (Python, MIT, estable, sin las vulnerabilidades de OpenClaw)
            o Porcupine (Picovoice, production-grade, local)
STT:        Whisper.cpp (C++, MIT, local, sin API externa requerida)
TTS:        ElevenLabs API directa (sin pasar por OpenClaw)
            o Kokoro TTS (open source, local)
Tools:      MCP servers directos (filesystem MCP, shell MCP) — sin OpenClaw como proxy
```

Esto es 2-3 semanas de trabajo versus los meses que implicaría construir todo.
Y elimina la dependencia de un proyecto con historial reciente de CVEs críticos.

---

## Mitigación de riesgos

| Riesgo | Mitigación |
|---|---|
| OpenClaw 2026.4.26-style breakage | OliVoiceInterface absorbe el cambio. Solo se actualiza el adapter. |
| CVE en OpenClaw → RCE en machine del usuario | NativeVoiceAdapter como default. OpenClaw como opt-in para usuarios que ya lo usan. |
| Skills maliciosos de ClawHub | Oli nunca ejecuta skills de ClawHub sin validación. Solo usa tools via MCP con permission model de Oli. |
| OpenClaw desaparece | clawd-voice + NativeVoiceAdapter están listos. |
| El usuario no quiere OpenClaw | Oli funciona perfectamente via UI directa. Voz es enhancement, no requisito. |

---

## Referencias

- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [Voice Wake docs](https://docs.openclaw.ai/nodes/voicewake)
- [clawd-voice](https://github.com/joetomasone/clawd-voice)
- [voiceclaw plugin](https://github.com/muin-company/voiceclaw)
- [OpenClaw Skills](https://docs.openclaw.ai/tools/skills)
- [OpenWakeWord](https://github.com/dscripka/openWakeWord)
