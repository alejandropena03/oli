# ADR-012 — Estrategia de ejecución desktop y OS completo

**Estado:** accepted
**Fecha:** 2026-05-26
**Deciders:** Alejandro Peña (founder) — decisión explícita tras diagnóstico
**Corrige:** ADR-011 sobredependía en Computer Use API (Claude-only)

---

## Contexto

La promesa de Oli incluye:
> **"Ser capaz de hacer todo lo que un humano haría en un computador."**

ADR-011 cubría browser automation (Playwright/Stagehand/CDP). Pero quedaba un hueco:
¿cómo Oli controla el desktop completo — apps GUI, filesystem, procesos, todo — de forma
**model-agnostic**?

El problema con Computer Use API de Anthropic:
- **Claude-only** — viola ADR-001 (model-agnostic)
- **Requiere container de Anthropic** — no es "tu Linux"
- **No escala** — latencia alta, costo por screenshot

La solución está en entender correctamente **qué significa "hacer todo en un computador"**:
- El 90% no requiere "ver" el desktop — requiere una **shell en Linux**
- El 8% requiere GUI — se resuelve con **ClawdCursor** (MCP, model-agnostic, Linux Wayland)
- El 2% es browser — ya cubierto en ADR-011

---

## Research (Mayo 2026)

### ClawdCursor — el estándar model-agnostic para desktop GUI

**GitHub:** [AmrDab/clawdcursor](https://github.com/AmrDab/clawdcursor)
**Estado:** Producción — v0.8.8, activamente mantenido

Características clave:
- **Model-agnostic**: Claude, GPT, Gemini, Llama, Kimi, Ollama — cualquier modelo
- **OS-agnostic**: Windows 10/11, macOS 12+, Linux X11, **Linux Wayland**
- **MCP nativo**: stdio MCP para editors + HTTP MCP daemon en 127.0.0.1:3847
- **97 tools granulares** O 6 compound tools (estilo Computer Use para compatibilidad)
- **Blind-first pipeline** — 12x más barato que vision-only:
  ```
  1. Accessibility tree (AT-SPI en Linux) → gratis, estructurado
  2. OCR sobre región                     → barato
  3. Screenshot parcial                   → medio
  4. Vision LLM completo                  → solo si todo lo anterior falla
  ```
- **Safety gate**: toda tool call pasa por un gate de seguridad antes de tocar el desktop
- **Local-only**: corre en el machine del usuario, sin cloud de Anthropic

### computer-use-linux — para Linux headless/server

**GitHub:** [agent-sh/computer-use-linux](https://github.com/agent-sh/computer-use-linux)
**Implementación:** Rust, MCP, model-agnostic

Capas técnicas en Linux:
```
Accessibility:  AT-SPI (crate atspi)         → semantic element targeting
Windowing:      GNOME Shell / KWin / Hyprland / i3 IPC → window management
Input:          Wayland portals RemoteDesktop → ydotool/uinput fallback
Screenshots:    GNOME Shell DBus + freedesktop portal alternatives
```

**Importante para Wayland:** xdotool se rompe en Wayland (mayoría de Linux 2026).
La solución correcta es `ydotool` + Wayland portals. computer-use-linux ya lo maneja.

### E2B / Daytona — el "Linux completo" para el 90%

No es sobre "ver el desktop" — es sobre tener un **Linux real con shell**:

```bash
# Lo que E2B/Daytona provee — un Linux completo ejecutable:
$ python script.py           # código
$ curl https://api.com       # HTTP
$ git clone repo && cd repo  # git
$ ffmpeg -i input output     # multimedia
$ chromium --headless        # browser headless
$ apt install cualquier-cosa # instalación de paquetes
$ cat / write / grep / sed   # filesystem
$ systemctl / cron / jobs    # procesos
```

**E2B**: Firecracker microVM, 150ms cold start, hardware isolation, 88% Fortune 100
**Daytona**: Docker containers, 27ms cold start, persistent workspaces

Para Oli V3+, el founder tiene un **Linux personal persistente** donde Oli puede instalar herramientas, mantener estado entre misiones, y ejecutar cualquier proceso.

---

## Decisión: Stack de ejecución desktop por capa

```
┌─────────────────────────────────────────────────────────────────────┐
│  LO QUE PUEDE HACER UN HUMANO EN UN COMPUTADOR                     │
│                                                                     │
│  90% — SHELL / CLI / PROCESOS                                       │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  E2B microVM (V3+) o subprocess local (V1-V2)               │  │
│  │  Cualquier comando Linux, cualquier lenguaje, cualquier API  │  │
│  │  Model-agnostic — el modelo da instrucciones en shell        │  │
│  │  Costo: muy bajo (cómputo local/microVM)                     │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  8% — GUI DE APLICACIONES DESKTOP (sin API ni CLI)                  │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  ClawdCursor (MCP, model-agnostic)                          │  │
│  │  AT-SPI → OCR → screenshot (escalante, 12x más barato)      │  │
│  │  Windows / macOS / Linux X11 / Linux Wayland                │  │
│  │  97 tools granulares vía MCP                                 │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  2% — WEB BROWSER                                                   │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Playwright MCP + Stagehand + chrome-devtools-mcp           │  │
│  │  (ver ADR-011)                                               │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

### Stack por versión de Oli

| Versión | Desktop/OS execution | Capacidad |
|---|---|---|
| **V0** | Mock | Simula toda ejecución |
| **V1** | Subprocess local con allowlist | Shell básico en el machine del usuario |
| **V2** | Subprocess + ClawdCursor (local) | Shell + GUI apps locales |
| **V3** | E2B microVM + ClawdCursor | Linux completo aislado + GUI |
| **V4+** | E2B persistente (Linux personal de Oli) + ClawdCursor | Linux persistente entre misiones, cualquier herramienta |

### El "Linux personal de Oli" (V4+)

Esta es la visión correcta de lo que el founder describió:

```
Oli V4+ tiene un E2B workspace persistente:
  ├── Herramientas instaladas por Oli para el founder
  ├── Estado persistente entre misiones (archivos, configs, credenciales seguras)
  ├── Python env con librerías del founder
  ├── Node/Bun env
  ├── Git repos clonados
  ├── Scripts y automaciones de Oli
  └── Chromium headless para scraping sin GUI

ClawdCursor conecta el Linux a las apps GUI cuando es necesario.
```

---

## Por qué Computer Use API pasa a ser "opción del usuario", no core

| Criterio | Computer Use API | ClawdCursor + Linux shell |
|---|---|---|
| Model-agnostic | ❌ Claude-only | ✅ Cualquier modelo |
| Local-first | ❌ Container Anthropic | ✅ Tu máquina |
| Costo por acción | Alto (screenshots completos) | Bajo (accessibility first, 12x más barato) |
| Linux Wayland | ⚠️ Depende del container | ✅ Soporte nativo |
| Sin internet | ❌ Requiere API | ✅ 100% local |
| ADR-001 compliant | ❌ Viola model-agnostic | ✅ Cumple |

**Computer Use API queda disponible** como opción si el usuario tiene Claude como modelo y quiere usarla para casos específicos. Pero no es la estrategia core de Oli.

---

## OpenClaw — qué es y por qué no es lo que Oli usa

OpenClaw (361K+ stars) es un framework de **agente personal local** con inbox multi-canal (WhatsApp, Slack, Telegram, etc.) y ejecución de tareas. Es más un **competidor de Oli** que una herramienta que Oli consume.

Oli no usa OpenClaw — Oli es la alternativa con mejor arquitectura de misiones, memoria y validación.

**Lo que Oli sí toma del ecosistema OpenClaw:** la idea de que el agente vive localmente y tiene acceso real al sistema. Eso es ADR-010 + esta ADR.

---

## Implicaciones en los schemas

El `ToolTransport` en `tool.ts` se actualiza:

```typescript
// Reemplaza "computer_use" como primario:
"clawdcursor_mcp"     // ClawdCursor — GUI desktop, model-agnostic, MCP
"linux_shell"         // E2B / subprocess / shell directo
"computer_use"        // Computer Use API — queda como opción, no como primario
```

El `ExecutionSuboperator` tiene acceso completo a estos transports.
La selección sigue el orden de costo: shell → accessibility → OCR → screenshot → vision.

---

## Consecuencias

**Positivo:**
- Oli cumple la promesa "todo lo que un humano haría" sin depender de Anthropic para ello
- ClawdCursor es 12x más barato que Computer Use por su pipeline blind-first
- E2B provee el Linux completo que el founder imaginó — con persistencia en V4+
- Stack 100% model-agnostic — Oli puede correr con Ollama local en una máquina sin internet
- Wayland funciona — la mayoría de Linux 2026 usa Wayland, xdotool no funciona ahí

**Negativo:**
- ClawdCursor requiere acceso al display del usuario (X11/Wayland) — no es headless por defecto en V2
- E2B tiene costo de cómputo en V3+ (aunque bajo)
- Setup más complejo que "usar el API de Anthropic"

**Riesgo gestionado:**
- Si ClawdCursor deja de mantenerse: computer-use-linux (Rust, alternativa directa) + Computer Use API como fallback

---

## Referencias

- [ClawdCursor GitHub](https://github.com/AmrDab/clawdcursor)
- [computer-use-linux GitHub](https://github.com/agent-sh/computer-use-linux)
- [E2B vs Daytona comparison](https://www.zenml.io/blog/e2b-vs-daytona)
- [Linux AI Agent Desktop Automation 2026](https://fazm.ai/blog/agentic-infrastructure-landscape-2026-linux-desktop-gui)
- [OpenClaw architecture](https://bibek-poudel.medium.com/how-openclaw-works-understanding-ai-agents-through-a-real-architecture-5d59cc7a4764)
