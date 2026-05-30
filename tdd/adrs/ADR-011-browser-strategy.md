# ADR-011 — Estrategia de browser para ejecución web y desktop

**Estado:** accepted — v3 actualizado 2026-05-27 (stack Python confirmado)
**Fecha:** 2026-05-26
**Deciders:** Alejandro Peña (founder) + research exhaustivo del ecosistema
**Research base:** Mayo 2026 — datos verificados con GitHub MCP

---

## Contexto

Uno de los dos pilares de la promesa de Oli es:
> **"Ser capaz de hacer todo lo que un humano haría en un computador."**

Para cumplir esta promesa, Oli necesita una estrategia de browser y desktop automation que sea:
- Confiable en producción (no experimental)
- Compatible con el stack Python + FastAPI + LangGraph (ADR-005)
- Compatible con MCP (ADR-010: MCP como protocolo de conectividad)
- Escalable desde V1 (mock + web básico) hasta V4+ (control total de desktop)
- Con costo de ejecución razonable por misión

**Nota de migración:** Las versiones anteriores de este ADR decían "TypeScript-native" porque el stack original era TypeScript/Bun. El stack definitivo es Python (ADR-005 v2). Todas las referencias a "TypeScript-only" o "Python incompatible" en este doc quedaron obsoletas con ese cambio.

El ecosistema de browser para IA en 2026 es radicalmente diferente al de 2024. Esta ADR documenta el estado real y las decisiones basadas en él.

---

## Landscape del ecosistema (Mayo 2026)

### Las 5 capas del stack de browser para IA

```
Capa 5 — DESKTOP COMPLETO
  Anthropic Computer Use API (computer-use-2025-11-24)
  → Claude ve screenshots del desktop, controla mouse/teclado
  → Cualquier app, no solo browser
  → Corre en container dedicado
  → Escape hatch final: si nada más funciona, esto funciona

Capa 4 — BROWSER AUTÓNOMO (agente completo)
  Browser Use (Python, 95,876 stars — verificado GitHub 2026-05-27)
  → LLM controla el browser completo como agente autónomo
  → Multi-tab, memoria, razonamiento cross-site
  → Python-only ← compatible con backend Python de Oli (ADR-005)
  → 2-5s por acción, $0.02-0.30 por tarea
  → NOTA: con backend Python, Browser Use es viable como subagente interno

Capa 3 — BROWSER HÍBRIDO AI+DETERMINÍSTICO (★ elección principal)
  Stagehand v3 (TypeScript, Browserbase, 3,359 stars MCP server — verificado GitHub)
  → ⚠️ CAMBIO ARQUITECTURAL v3: dropped Playwright dependency, ahora CDP-native
  → Ya NO es "built on Playwright" — v3 habla directamente a CDP (44% más rápido)
  → Playwright sigue siendo integrable (docs.stagehand.dev/v3/integrations/playwright)
    pero ya no es una dependencia — es un driver opcional
  → Tres primitivas AI: act(), extract(), observe()
  → Una primitiva autónoma: agent()
  → Auto-caching: cuando un act() tiene éxito, guarda el selector
    y lo reutiliza sin llamar al modelo en runs futuros
  → TypeScript/JavaScript — sin conflict con backend Python (son capas distintas)
  → 1-3s por acción AI, <100ms para pasos determinísticos

Capa 2 — BROWSER DETERMINÍSTICO (alta velocidad, cero LLM)
  Playwright (TypeScript, Microsoft, 70K+ stars)
  → Chromium + Firefox + WebKit
  → <100ms por acción, ~$0.00 por tarea
  → Requiere selectores explícitos — se rompe cuando UI cambia
  → Tasa de éxito: ~98% en páginas conocidas, ~0% en páginas nuevas
  → Ideal para el 80% de pasos predecibles en un playbook

Capa 1 — PROTOCOLO BASE
  Chrome DevTools Protocol (CDP)
  → El protocolo que todos usan por debajo
  → chrome-devtools-mcp (Google oficial, v0.21, Sep 2025)
    29 tools: input, navigation, performance, network, debug, emulation
  → Playwright MCP (Microsoft oficial)
    Accesibility tree snapshots — ~200 tokens vs miles con screenshots
    4x más barato que Computer Use en tokens
  → WebMCP (experimental — Chrome 146 Canary)
    Páginas web como MCP servers nativos — spec en borrador, 2027+
```

### Benchmarks reales (WebVoyager benchmark, 586 tareas)

| Herramienta | Modelo | Tasa de éxito | Velocidad/acción | Costo/tarea |
|---|---|---|---|---|
| Playwright (determinístico) | N/A | ~98% (páginas conocidas) | <100ms | $0.00 |
| Stagehand agent | Claude Sonnet | ~75% | 1-3s | $0.002-0.02 |
| Browser Use | Claude Opus | ~78% | 2-5s | $0.02-0.30 |
| Browser Use | GPT-4.1 | ~72% | 2-5s | $0.02-0.30 |
| Computer Use API | Claude Sonnet | ~85%* | 3-8s | $0.05-0.50 |

*estimado — benchmark oficial de Computer Use no publicado aún

### Por qué Stagehand es la elección para Oli

1. **CDP nativo en v3** — habla directamente al browser sin capas intermedias. Más rápido y más confiable.
2. **Arquitectura híbrida** — el insight clave de 2026: el 80% de pasos en un playbook son predecibles (Playwright determinístico), el 20% requieren AI (Stagehand act/extract). Stagehand es ambos.
3. **Auto-caching** — la primera vez Stagehand invoca el modelo, la segunda usa el selector guardado. En playbooks que se ejecutan repetidamente, el costo AI baja dramáticamente.
4. **MCP compatible** — Stagehand puede exponerse como MCP server para que Oli lo consuma via Tool Router.
5. **Consumible desde Python** — Stagehand corre como proceso separado o via MCP. El backend Python de Oli lo llama a través del Tool Router, no lo importa directamente. Sin bloqueadores de integración.

### Revisión: Browser Use como subagente interno (confirmado — stack Python)

**Browser Use es Python-native. Con el stack Python definitivo de Oli (ADR-005), es perfectamente compatible sin adaptadores.**

Datos de GitHub verificados: **95,876 stars** (casi 2x más que el dato anterior de "50K+").
Browser Use es el proyecto de browser automation para IA más popular del ecosistema.

Evaluación actualizada:

| Criterio | Stagehand v3 | Browser Use |
|---|---|---|
| Lenguaje | TypeScript | Python (compatible con ADR-005) |
| Stars GitHub | 3,359 (MCP server) | **95,876** |
| Arquitectura | CDP nativo, AI quirúrgica | Agente autónomo completo |
| Mejor para | Acciones específicas dentro de misiones | Tasks de browser completamente autónomas |
| Costo/acción | $0.002-0.02 | $0.02-0.30 |

**Decisión revisada:**
- **Stagehand**: para acciones de browser embebidas dentro de misiones de Oli (act/extract/observe dentro de un step)
- **Browser Use**: para misiones donde el OBJETIVO COMPLETO es navegar/ejecutar en el browser — se invoca como subagente desde el ExecutionSuboperator
- No se elige uno o el otro — se usan los dos con criterios distintos

---

## Decisión: Stack de browser por capa y versión

### Principio arquitectural: Híbrido primero, AI cuando necesario

```
Para cada step de browser en una misión:

  ¿La página y el selector son conocidos (playbook establecido)?
  └── SÍ → Playwright determinístico
               Velocidad: <100ms | Costo: $0.00 | Confiabilidad: 98%

  ¿La acción necesita entender contexto pero la página es predecible?
  └── SÍ → Stagehand act() / extract() / observe()
               Velocidad: 1-3s | Costo: $0.002-0.02 | Confiabilidad: ~75%
               + auto-caching: segunda ejecución ~0 tokens

  ¿La tarea requiere razonamiento autónomo multi-página?
  └── SÍ → Stagehand agent()
               Velocidad: 5-30s | Costo: $0.02-0.10 | Confiabilidad: ~75%

  ¿El sitio bloquea automation o requiere JavaScript complejo?
  └── SÍ → chrome-devtools-mcp (Google oficial)
               Acceso completo CDP: console, network, performance, DOM

  ¿Nada de lo anterior funciona? ¿O es una app desktop, no web?
  └── SÍ → Computer Use API (escape hatch)
               Claude ve screenshot, controla mouse/teclado
               Velocidad: 3-8s | Costo: más alto | Cobertura: total
```

### Stack por versión de Oli

| Versión | Herramientas de browser | Capacidad |
|---|---|---|
| **V0** | Mock (ExecutionSuboperator) | Simula acciones de browser — valida arquitectura |
| **V1** | Playwright MCP (Microsoft oficial) | Web scraping determinístico, páginas conocidas |
| **V2** | Stagehand v3 + Playwright | Automatización AI-híbrida. Stagehand cuando la página es dinámica, Playwright cuando el selector es conocido |
| **V3** | V2 + chrome-devtools-mcp + Computer Use API | Cobertura completa: cualquier web + cualquier app desktop |
| **V4+** | V3 + Browserbase (managed) | Browsers en la nube, sesiones paralelas, sin infra propia |

---

## Arquitectura de integración en Oli

### Cómo el ExecutionSuboperator usa el stack

```python
# El ExecutionSuboperator recibe un BrowserAction
# El Tool Router selecciona la implementación correcta

@dataclass
class BrowserAction:
    type: Literal[
        "navigate",      # ir a una URL
        "click",         # click en elemento
        "fill",          # llenar formulario
        "extract",       # extraer datos estructurados
        "screenshot",    # capturar estado visual
        "observe",       # listar elementos accionables
        "agent_task",    # tarea autónoma multi-paso
    ]
    target: str | None = None        # selector o descripción natural
    schema: dict | None = None       # schema del dato a extraer
    instruction: str | None = None   # para agent_task en lenguaje natural
    url: str | None = None
    timeout_ms: int = 30_000

# El Tool Router selecciona la implementación:
#   navigate + URL conocida       → Playwright MCP
#   click + selector conocido     → Playwright MCP
#   click + descripción natural   → Stagehand act()
#   extract + schema              → Stagehand extract()
#   agent_task                    → Stagehand agent() o Browser Use
#   console/network/perf          → chrome-devtools-mcp
#   desktop app                   → Computer Use API (escape hatch)
```

### MCP servers de browser que Oli consume

```
V1:
  @playwright/mcp                → Playwright oficial (Microsoft)
    Tools: navigate, click, fill, screenshot, accessibility_snapshot

V2:
  stagehand-mcp                  → Stagehand (Browserbase)
    Tools: act, extract, observe, agent

V3:
  chrome-devtools-mcp            → Google oficial
    Tools: navigate_page, screenshot, list_console_messages,
           list_network_requests, performance_start_trace, ...29 total

V3 (escape hatch):
  computer-use via Anthropic SDK → No es MCP, es tool nativo
    Integrado directamente en el Model Router para Claude models
```

---

## Auto-caching y playbooks — la sinergia clave

Este es el detalle más importante para la economía de Oli:

```
Primera ejecución de un playbook que incluye step de browser:
  1. Stagehand act("click en el botón de exportar CSV")
  2. Stagehand llama al modelo → identifica selector → ejecuta → guarda
  3. Costo: ~$0.005-0.01 en tokens del modelo

Segunda y subsiguientes ejecuciones del mismo playbook:
  1. Stagehand auto-cache tiene el selector guardado
  2. Stagehand ejecuta el selector directamente (como Playwright)
  3. Si la UI cambió → Stagehand re-invoca el modelo, actualiza cache
  4. Costo: ~$0.00 tokens | velocidad: <100ms
```

Esto significa que los playbooks de Oli mejoran solos con el uso — el primer run paga el costo AI, los runs subsiguientes son casi gratuitos y más rápidos.

---

## Consideraciones de seguridad y privacidad

1. **Sandbox por misión** — el browser corre en contexto aislado, no en el perfil real del founder
2. **Credenciales** — Oli nunca guarda passwords. Usa el session store del browser para sesiones autorizadas previamente por el founder (permission_class ≥ 3 para sitios con login)
3. **Computer Use en container** — el Computer Use API siempre corre en container dedicado, nunca en la máquina del founder directamente
4. **Audit trail** — toda acción de browser genera un EvidenceRef (screenshot + selector + timestamp) en el Evidence Store de la misión
5. **Permission_class de browser actions**:

| Acción | Clase de permiso |
|---|---|
| navigate + read (scraping) | 0 — read only |
| form fill (datos públicos) | 1 — internal reversible |
| form fill + submit | 2 — resource consuming |
| login en nombre del founder | 3 — external impact |
| acciones en cuentas del founder con consecuencias | 4 — destructive |

---

## Alternativas consideradas y descartadas

| Opción | Por qué no |
|---|---|
| Browser Use como primario (standalone) | Poderoso pero autónomo — difícil de controlar dentro de una misión con permisos y evidencia. Mejor como subagente delegado para tasks completos de browser. |
| Selenium/WebDriver | Obsoleto para AI agents. Sin primitivas AI. |
| Puppeteer directo | CDP sin abstracción AI. Más trabajo, menos capacidad que Playwright. |
| OpenAI CUA (Computer-Using-Agent) | Cloud-only, locked a OpenAI. Incompatible con ADR-001 (model-agnostic). |
| WebMCP | Experimental — spec en borrador. Chrome 146 Canary only. No antes de 2027. |
| Skyvern | Bueno pero cloud-only managed service. Crea dependencia de proveedor. |

---

## Consecuencias

**Positivo:**
- Compatible con stack Python — Stagehand y Playwright MCP se consumen via Tool Router sin importar el lenguaje del caller
- Cobertura completa: web scraping → web automation → desktop completo
- Economía de playbooks: costo AI solo en la primera ejecución vía auto-caching
- Todos los browsers expuestos como MCP servers → el Tool Router los trata igual que cualquier otra herramienta
- Computer Use como escape hatch — literalmente nada en un computador escapa a Oli en V3+

**Negativo:**
- Stagehand requiere cuenta Browserbase para el runtime managed (tiene alternativa local via Playwright)
- Computer Use API requiere container dedicado — latencia de startup en cold start
- Las tasas de éxito AI (~75%) son menores que Playwright determinístico (~98%) — justifica la arquitectura híbrida

**Riesgo gestionado:**
- WebMCP (páginas como MCP servers nativos) podría cambiar el landscape en 2027 — la arquitectura de Oli es compatible porque ya usa MCP como protocolo base

---

## Referencias

- [Stagehand v3 Launch](https://www.browserbase.com/blog/stagehand-v3)
- [Chrome DevTools MCP — Google oficial](https://developer.chrome.com/blog/chrome-devtools-mcp)
- [Stagehand vs Browser Use vs Playwright 2026](https://www.nxcode.io/resources/news/stagehand-vs-browser-use-vs-playwright-ai-browser-automation-2026)
- [Playwright MCP — Microsoft](https://playwright.dev/)
- [Computer Use API — Anthropic](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)
- [Cloudflare Browser Run](https://blog.cloudflare.com/browser-run-for-ai-agents/)
- [WebMCP spec](https://www.arcade.dev/blog/web-mcp-alex-nahas-interview/)
