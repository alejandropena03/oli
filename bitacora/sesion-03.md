# Sesión 03 — 2026-05-26

## Contexto
Sesión de arquitectura profunda. El founder hizo la pregunta correcta: "demuéstrame cómo la arquitectura actual cumple la promesa". Se investigó el ecosistema completo, se diseñaron los schemas TypeScript, y se cerraron todos los gaps arquitecturales antes de escribir código.

---

## Research ejecutado (en vivo, Mayo 2026)

| Área | Hallazgo clave |
|---|---|
| MCP ecosystem | 5,800+ servers, estándar de facto, adoptado por OpenAI/Google/Microsoft/Linux Foundation |
| Mastra v1.0 | Mejor framework TypeScript para agentes, 22k+ stars, 9/10 DX |
| Browser AI | Stagehand v3 (TypeScript, CDP nativo, auto-caching), Playwright MCP, chrome-devtools-mcp |
| Desktop Linux | ClawdCursor (MCP, model-agnostic, AT-SPI→OCR, 12x más barato que Computer Use) |
| Desktop Linux headless | computer-use-linux (Rust, Wayland, AT-SPI, MCP) |
| Sandboxes | E2B (150ms Firecracker) vs Daytona (27ms Docker) |
| OpenClaw | 361K stars, voice wake + 26 tools + 13,700 skills PERO CVEs críticos, inestabilidad Apr 2026 |
| Auth | Brokered Credentials + PKCE + OS Keychain — estándar 2026 para agentes |
| Conectividad | Jerarquía: API directa → n8n → MCP → shell — nunca Zapier |

---

## Artefactos creados

| Artefacto | Descripción |
|---|---|
| `tdd/adrs/ADR-010` | Connectivity Architecture — MCP como protocolo, Mastra como framework |
| `tdd/adrs/ADR-011` | Browser Strategy — Playwright→Stagehand→CDP→ComputerUse |
| `tdd/adrs/ADR-012` | Desktop Execution — ClawdCursor + linux_shell/E2B (Computer Use degradado a opt-in) |
| `tdd/adrs/ADR-013` | OpenClaw Integration v3 — NativeVoiceAdapter (default) + OpenClawAdapter (opt-in) |
| `tdd/adrs/ADR-014` | Auth & Credentials — Brokered creds, OS Keychain, OAuth PKCE, onboarding automático |
| `tdd/schemas/tool.ts` | Schema completo: transport (14 tipos), permissions, configs browser/desktop/shell/voice |
| `tdd/schemas/mission.ts` | Agregado principal: 21 estados (incluyendo fuentes OpenClaw), plan, repair, evidence |
| `tdd/schemas/memory.ts` | 3 capas, MemoryEntry, MemoryGraph interface, claves canónicas USER/COMPANY |
| `tdd/schemas/playbook.ts` | Playbook, variables, steps, PlaybookEngine interface |
| `tdd/schemas/suboperator.ts` | 8 suboperadores, outputs específicos, registry completo con tools actualizados |
| `tdd/schemas/index.ts` | Entry point unificado |
| `tdd/domain/promise-validation.md` | Demostración concreta: 14 capacidades cubiertas, cada una con ejemplo real |
| `tdd/domain/connectivity-map.md` | Jerarquía de decisión (API→n8n→MCP→shell), 2 perfiles (técnico / no técnico) |

---

## Decisiones arquitecturales clave de la sesión

### Computer Use API → no es core
Computer Use es Claude-only → viola ADR-001 (model-agnostic). Degradado a opción del usuario. Reemplazado por ClawdCursor (model-agnostic, 12x más barato, Linux Wayland).

### OpenClaw → opt-in, nunca dependencia dura
CVE-2026-32922 (RCE con 1 API call), inestabilidad documentada en Apr 2026, 40K+ instancias expuestas. Solución: OliVoiceInterface abstracta. NativeVoiceAdapter como default (OpenWakeWord + Whisper.cpp + ElevenLabs directo). OpenClawAdapter disponible para quien ya lo usa.

### Deployment model aclarado
- **Local (siempre):** Credential Vault, OAuth flows, wake word, UI, Mission Kernel V0-V2
- **Servidor Linux/E2B (V3+):** ejecución de código pesado, browser headless, sandbox
- **Regla inamovible:** el vault de credenciales NUNCA va al servidor

### Auth: el onboarding lo hace Oli solo
1. Oli detecta que necesita un servicio → lanza OAuth PKCE flow → abre browser
2. Usuario da un click en el browser de autorización
3. Oli recibe el callback en localhost:3847 → intercambia code por token → guarda en OS Keychain
4. Misión continúa. El LLM nunca vio el token.

### Conectividad: jerarquía de eficiencia
1. API directa (Python/TS) — sin intermediarios
2. n8n webhook — para flujos ya existentes o muy complejos
3. MCP server oficial — solo cuando añade valor real
4. linux_shell/E2B — cualquier CLI
5. Stagehand/Playwright — cualquier web
6. ClawdCursor — cualquier GUI

### Sinergia clave: Stagehand auto-caching + Playbooks
Primera ejecución de un playbook con browser: paga el costo AI. Ejecuciones siguientes: Stagehand reutiliza el selector guardado → ~$0 tokens. Los playbooks de Oli mejoran solos con el uso.

---

## Estado al final de sesión 03

| Área | Estado |
|---|---|
| Marca | ✅ Completa |
| Skill /oli | ✅ Actualizada con stack completo de conectividad |
| Event Storming | ✅ V3 — con todas las decisiones del founder |
| State Machine | ✅ V1 — 18 estados |
| ADRs | ✅ 14 ADRs (001-014) |
| Slice-001 en papel | ✅ Research Brief |
| Stack Decision | ✅ V0 completo + conectividad + auth |
| Schemas TypeScript | ✅ 5 schemas completos |
| Connectivity Map | ✅ Jerarquía clara |
| Promise Validation | ✅ Demostrada con ejemplos reales |
| Auth & Credentials | ✅ Arquitectura completa |
| Mission Kernel V0 (código) | 🔲 **PRÓXIMO PASO** |

---

## Próximo paso — Build V0

Orden estricto, sin saltear:
1. `package.json` — Bun, @anthropic-ai/claude-agent-sdk, Mastra, Zod, keytar
2. `src/types/` — schemas a implementación
3. `src/kernel/state-machine.ts` — 18 estados
4. `src/kernel/mission-kernel.ts` — orquestador
5. `src/kernel/orchestrator.ts` — intent → plan
6. `src/permissions/permission-service.ts`
7. `tests/integration/slice-001.test.ts` — mock runner end-to-end
8. `src/evidence/evidence-store.ts`
9. `src/memory/memory-graph.ts` — JSON files V0
10. CLI básico — solo después de que todo lo anterior funcione
