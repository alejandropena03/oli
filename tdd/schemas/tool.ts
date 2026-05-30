/**
 * OLI — Tool Schema
 *
 * Define cómo Oli conoce, valida y ejecuta herramientas.
 * Toda herramienta que Oli puede usar — MCP server, subprocess, API, browser —
 * tiene esta forma. El Tool Router usa estos schemas para decidir qué tool
 * usar, con qué permiso, y cómo fallar con gracia.
 *
 * Patrón: Zod como source of truth → TypeScript types derivados.
 * Compatible con @anthropic-ai/claude-agent-sdk tool() pattern.
 *
 * @see ADR-010 — Connectivity Architecture
 * @see ADR-004 — Permission Model
 */

import { z } from "zod"

// ─────────────────────────────────────────────────────────────────────────────
// ENUMS & CONSTANTS
// ─────────────────────────────────────────────────────────────────────────────

export const ToolTransport = z.enum([
  // ── Protocolo base ─────────────────────────────────────────────────────────
  "mcp",              // MCP server genérico (protocolo estándar — preferido para todo)
  "mock",             // Mock para V0 — retorna outputs predefinidos

  // ── Shell / OS (ADR-012: el 90% de "hacer todo en un computador") ──────────
  "subprocess",       // Shell local con allowlist — V1-V2
  "linux_shell",      // E2B microVM o Daytona — Linux completo aislado — V3+
  "http",             // API REST directa

  // ── Desktop GUI — model-agnostic (ADR-012) ─────────────────────────────────
  "clawdcursor_mcp",  // ClawdCursor — MCP, model-agnostic, Windows/macOS/Linux X11+Wayland
                      // Blind-first: AT-SPI → OCR → screenshot (12x más barato que vision)
                      // 97 tools granulares — apps GUI sin CLI

  // ── Browser web (ADR-011) ──────────────────────────────────────────────────
  "playwright_mcp",   // @playwright/mcp — determinístico, <100ms, $0. Para el 80% conocido.
  "stagehand",        // Stagehand v3 — AI-híbrido, act/extract/observe/agent. Para el 20% dinámico.
  "cdp_mcp",          // chrome-devtools-mcp — Google oficial. CDP: console, network, perf, debug.

  // ── Sandboxes de ejecución (ADR-002) ──────────────────────────────────────
  "e2b",              // E2B Firecracker microVM — 150ms cold start, hardware isolation
  "daytona",          // Daytona Docker container — 27ms cold start, persistent workspaces

  // ── Voz / presencia local (ADR-013) ───────────────────────────────────────
  "voice_native",     // NativeVoiceAdapter — OpenWakeWord + Whisper.cpp + ElevenLabs directo
                      // Sin dependencias externas. Default de Oli. Bajo riesgo.
  "voice_openclaw",   // OpenClawAdapter — si el usuario ya tiene OpenClaw instalado (opt-in)
                      // Mayor superficie de ataque. Requiere monitoreo de CVEs.

  // ── Computer Use — opción de usuario, no core (ADR-012) ───────────────────
  "computer_use",     // Anthropic Computer Use API — Claude-only, requiere container Anthropic
                      // NO es la estrategia primaria. Disponible si el usuario elige Claude
                      // y quiere esta opción específica. ClawdCursor es el reemplazo.
])
export type ToolTransport = z.infer<typeof ToolTransport>

export const ToolCategory = z.enum([
  "filesystem",   // Leer/escribir archivos y directorios
  "shell",        // Ejecutar comandos, scripts, procesos
  "browser",      // Automatización web — Playwright (determinístico) o Stagehand (AI-híbrido)
  "desktop",      // Control de desktop completo — Computer Use API (cualquier app)
  "code",         // Ejecutar código — Python, JS, bash, etc.
  "api",          // Llamadas a APIs externas
  "memory",       // Operaciones en el Memory Graph
  "communication",// Email, Slack, calendar, mensajería — incluye OpenClaw (ADR-013)
  "search",       // Búsqueda web, bases de datos, documentos
  "data",         // Transformación, análisis, visualización de datos
  "ai",           // Llamadas a otros modelos o agentes
])
export type ToolCategory = z.infer<typeof ToolCategory>

export const PermissionClass = z.union([
  z.literal(0), // Read/Draft — sin side effects externos
  z.literal(1), // Internal reversible — acciones locales reversibles
  z.literal(2), // Resource consuming — costo real o uso de recursos
  z.literal(3), // External/brand impact — comunicación o publicación
  z.literal(4), // Destructive/sensitive — datos, producción, finanzas
])
export type PermissionClass = z.infer<typeof PermissionClass>

export const ToolAvailability = z.enum([
  "available",    // Tool lista para usar
  "unavailable",  // MCP server caído o no configurado
  "requires_auth",// Necesita credenciales que no están configuradas
  "sandbox_only", // Solo disponible en sandbox (E2B/Daytona), no local
  "mock",         // Solo modo mock disponible (V0)
])
export type ToolAvailability = z.infer<typeof ToolAvailability>

// ─────────────────────────────────────────────────────────────────────────────
// TOOL ANNOTATIONS
// Metadatos que el modelo usa para decidir cuándo y cómo usar el tool.
// Compatible con Anthropic tool annotations spec.
// ─────────────────────────────────────────────────────────────────────────────

export const ToolAnnotations = z.object({
  /** Si true, el tool solo lee — no modifica estado externo */
  readOnlyHint: z.boolean().default(false),

  /** Si true, el tool puede interactuar con el mundo abierto (web, APIs externas) */
  openWorldHint: z.boolean().default(false),

  /** Si true, la acción NO puede deshacerse */
  destructiveHint: z.boolean().default(false),

  /** Si true, llamar este tool múltiples veces con los mismos params es seguro */
  idempotentHint: z.boolean().default(false),

  /**
   * Si true, Oli debe mostrar al founder exactamente lo que va a hacer
   * antes de ejecutar, incluso si permission_class lo permite automáticamente
   */
  requiresExplicitConfirmation: z.boolean().default(false),
})
export type ToolAnnotations = z.infer<typeof ToolAnnotations>

// ─────────────────────────────────────────────────────────────────────────────
// TOOL FALLBACK
// Qué hace Oli si el tool primario no está disponible
// ─────────────────────────────────────────────────────────────────────────────

export const ToolFallback = z.object({
  /** Nombre del tool alternativo */
  tool_name: z.string(),

  /** Descripción de qué se pierde usando el fallback */
  degradation_note: z.string(),

  /** Si el fallback también falla, ¿bloqueamos la misión? */
  block_if_unavailable: z.boolean().default(false),
})
export type ToolFallback = z.infer<typeof ToolFallback>

// ─────────────────────────────────────────────────────────────────────────────
// TOOL DEFINITION
// El contrato completo de una herramienta en Oli.
// ─────────────────────────────────────────────────────────────────────────────

export const ToolDefinition = z.object({
  /** Identificador único — usado para referenciar en Mission steps */
  name: z.string().regex(/^[a-z][a-z0-9_]*$/, "snake_case requerido"),

  /** Descripción que ve el modelo — debe ser precisa y accionable */
  description: z.string().min(10),

  /** Categoría funcional — para routing y UI */
  category: ToolCategory,

  /** Cómo se transporta la llamada al tool */
  transport: ToolTransport,

  /**
   * Schema Zod del input — source of truth.
   * Se convierte a JSON Schema para el modelo y se usa en validación runtime.
   * Compatible con Anthropic claude-agent-sdk tool() pattern.
   */
  input_schema: z.instanceof(z.ZodType).describe("Zod schema del input"),

  /**
   * Schema Zod del output — permite validar lo que retorna el tool.
   * El ValidationSuboperator usa esto para verificar outputs.
   */
  output_schema: z.instanceof(z.ZodType).describe("Zod schema del output"),

  /** Clase de permiso requerida para ejecutar este tool */
  permission_class: PermissionClass,

  /** Si la acción puede deshacerse — afecta el repair strategy */
  reversible: z.boolean(),

  /**
   * Tiempo estimado de ejecución — usado para UI y timeout config.
   * El Mission Kernel usa esto para decidir si mostrar progress.
   */
  estimated_duration_ms: z.object({
    min: z.number().int().nonnegative(),
    typical: z.number().int().nonnegative(),
    max: z.number().int().nonnegative(),
  }),

  /** Costo estimado en USD si aplica (APIs pagas, compute, etc.) */
  estimated_cost_usd: z.number().nonnegative().optional(),

  /** Metadatos para el modelo sobre cómo usar el tool */
  annotations: ToolAnnotations,

  /**
   * Si transport = "mcp": configuración del MCP server
   */
  mcp_config: z.object({
    server_name: z.string(),
    tool_name: z.string(),   // nombre en el MCP server (puede diferir de name)
  }).optional(),

  /**
   * Si transport = "subprocess": configuración de shell
   */
  subprocess_config: z.object({
    command_template: z.string(),  // ej: "cat {path}"
    allowed_commands: z.array(z.string()),
    working_directory: z.string().optional(),
    timeout_ms: z.number().int().positive().default(30000),
    environment: z.record(z.string()).optional(),
  }).optional(),

  /**
   * Si transport = "linux_shell": configuración de shell en E2B/Daytona (ADR-012)
   * Para el 90% de "hacer todo en un computador" — no requiere GUI.
   * V1-V2: subprocess local | V3+: E2B microVM o Daytona container
   */
  linux_shell_config: z.object({
    provider: z.enum(["subprocess", "e2b", "daytona"]),

    // El comando a ejecutar — puede ser bash, python, node, cualquier CLI
    command: z.string(),

    // Para subprocess: allowlist de comandos permitidos
    allowed_commands: z.array(z.string()).optional(),

    // Para E2B/Daytona: si usar sandbox nuevo o reutilizar uno existente (V4+ persistente)
    sandbox_id: z.string().optional(),       // null = crear nuevo
    persist_sandbox: z.boolean().default(false), // true = sandbox persistente entre misiones

    // Timeout, working dir, env vars
    timeout_ms: z.number().int().positive().default(60000),
    working_directory: z.string().optional(),
    environment: z.record(z.string()).optional(),

    // Si el comando puede tener side effects irreversibles
    reversible: z.boolean().default(false),
  }).optional(),

  /**
   * Si transport = "clawdcursor_mcp": configuración de ClawdCursor (ADR-012)
   * Para GUI de apps desktop sin CLI. Model-agnostic, MCP nativo.
   * Pipeline blind-first: AT-SPI → OCR → screenshot → vision (12x más barato que Computer Use)
   */
  clawdcursor_config: z.object({
    /**
     * Modo de percepción — ClawdCursor escala automáticamente,
     * pero se puede forzar para casos específicos.
     */
    perception_mode: z.enum([
      "auto",         // Escala automáticamente: AT-SPI → OCR → screenshot → vision
      "accessibility",// Solo AT-SPI (más barato, solo si la app lo soporta)
      "ocr",          // OCR sobre región específica
      "screenshot",   // Screenshot completo (más caro)
    ]).default("auto"),

    /**
     * Compound tool (estilo Computer Use) o granular (97 tools específicos)
     */
    tool_mode: z.enum(["compound", "granular"]).default("compound"),

    // La acción específica a ejecutar
    action: z.enum([
      // Compound tools (computer, accessibility, window, system, browser, task)
      "computer",        // Acción general de computadora
      "accessibility",   // Inspección de accessibility tree
      "window",          // Gestión de ventanas
      "system",          // Operaciones de sistema
      // Granulares más comunes
      "click",
      "type",
      "screenshot",
      "get_accessibility_tree",
      "focus_window",
      "scroll",
      "drag",
      "key_combination",
    ]),

    // Instrucción en lenguaje natural (para compound tools)
    instruction: z.string().optional(),

    // Para acciones granulares: target, coordenadas, texto, etc.
    target: z.string().optional(),
    coordinates: z.object({ x: z.number(), y: z.number() }).optional(),
    text: z.string().optional(),

    timeout_ms: z.number().int().positive().default(30000),
  }).optional(),

  /**
   * Si transport = "playwright_mcp": configuración de Playwright MCP
   * Para pasos determinísticos donde el selector ya es conocido (playbooks establecidos).
   * Velocidad: <100ms | Costo: $0.00 | Confiabilidad: ~98%
   */
  playwright_config: z.object({
    selector: z.string().optional(),     // CSS/role/text selector — si se conoce
    action: z.enum([
      "navigate", "click", "fill", "screenshot",
      "accessibility_snapshot", "wait_for",
    ]),
    headless: z.boolean().default(true),
  }).optional(),

  /**
   * Si transport = "stagehand": configuración de Stagehand v3 (Browserbase)
   * Para pasos que requieren comprensión AI del DOM.
   * Velocidad: 1-3s (act/extract) | 5-30s (agent) | Auto-cache en ejecuciones subsiguientes
   * (ADR-011: auto-caching — segunda ejecución del mismo playbook ~$0.00 tokens)
   */
  stagehand_config: z.object({
    primitive: z.enum(["act", "extract", "observe", "agent"]),

    // Para act: instrucción en lenguaje natural
    instruction: z.string().optional(),

    // Para extract: el Zod schema del dato a extraer (serializado como JSON schema)
    extract_schema: z.record(z.unknown()).optional(),

    // Para agent: la tarea autónoma completa
    agent_task: z.string().optional(),

    // Si usar Browserbase managed (V4+) o Playwright local (V1-V3)
    use_browserbase: z.boolean().default(false),

    // Auto-cache: Stagehand guarda selectores exitosos para reutilizar sin LLM
    // true = comportamiento normal (recomendado para playbooks)
    enable_cache: z.boolean().default(true),

    timeout_ms: z.number().int().positive().default(30000),
  }).optional(),

  /**
   * Si transport = "cdp_mcp": configuración de Chrome DevTools MCP (Google oficial)
   * Para inspección profunda: console, network, performance, debugging.
   * 29 tools disponibles vía CDP.
   */
  cdp_config: z.object({
    tool: z.enum([
      "navigate_page", "screenshot", "click", "type", "scroll",
      "list_console_messages", "list_network_requests",
      "performance_start_trace", "performance_stop_trace",
      "get_lighthouse_report", "execute_javascript",
      "get_dom_snapshot",
    ]),
    url: z.string().optional(),
  }).optional(),

  /**
   * Si transport = "computer_use": configuración de Computer Use API
   * ESCAPE HATCH — para cuando ninguna otra opción funciona.
   * Cubre cualquier app desktop, no solo browser.
   */
  computer_use_config: z.object({
    model: z.string().default("claude-sonnet-4-6"),
    display_width: z.number().int().default(1280),
    display_height: z.number().int().default(800),
    requires_container: z.boolean().default(true),
  }).optional(),

  /**
   * Si transport = "e2b" | "daytona": configuración de sandbox
   */
  sandbox_config: z.object({
    provider: z.enum(["e2b", "daytona"]),
    template: z.string(),           // imagen base del sandbox
    timeout_ms: z.number().int().positive().default(60000),
    persist_between_steps: z.boolean().default(false),
    network_access: z.boolean().default(false),
  }).optional(),

  /** Qué hacer si este tool no está disponible */
  fallbacks: z.array(ToolFallback).default([]),

  /** Estrategias de repair cuando este tool falla (ADR-006) */
  repair_strategies: z.array(z.enum([
    "retry",                // Reintento exacto
    "alternative_tool",     // Usar un tool alternativo del mismo tipo
    "alternative_approach", // Replantear el step con otro enfoque
    "reduce_scope",         // Hacer menos — entregar parcial
  ])).default(["retry", "alternative_tool"]),

  /** Si true, el tool está disponible en esta instalación */
  availability: ToolAvailability.default("available"),
})
export type ToolDefinition = z.infer<typeof ToolDefinition>

// ─────────────────────────────────────────────────────────────────────────────
// TOOL CALL
// Una instancia de uso de un tool en el contexto de una mission step.
// ─────────────────────────────────────────────────────────────────────────────

export const ToolCall = z.object({
  /** ID único de esta llamada */
  id: z.string().uuid(),

  /** Nombre del tool — debe existir en el Tool Router */
  tool_name: z.string(),

  /** Input validado contra input_schema del tool */
  input: z.record(z.unknown()),

  /** ID de la misión que origina esta llamada */
  mission_id: z.string().uuid(),

  /** ID del step que origina esta llamada */
  step_id: z.string().uuid(),

  /** Timestamp de inicio */
  started_at: z.string().datetime(),
})
export type ToolCall = z.infer<typeof ToolCall>

// ─────────────────────────────────────────────────────────────────────────────
// TOOL RESULT
// El resultado de ejecutar un tool — éxito o falla.
// ─────────────────────────────────────────────────────────────────────────────

export const ToolResult = z.discriminatedUnion("success", [
  z.object({
    success: z.literal(true),
    tool_call_id: z.string().uuid(),
    output: z.unknown(),   // Validado contra output_schema del tool
    duration_ms: z.number().int().nonnegative(),
    cost_usd: z.number().nonnegative().optional(),
    transport_used: ToolTransport,
    completed_at: z.string().datetime(),
  }),
  z.object({
    success: z.literal(false),
    tool_call_id: z.string().uuid(),
    error_type: z.enum([
      "tool_not_found",
      "validation_error",      // Input no pasó schema validation
      "permission_denied",     // permission_class insuficiente
      "transport_error",       // MCP server caído, subprocess falla, etc.
      "timeout",
      "sandbox_error",         // E2B/Daytona falla
      "auth_required",         // Credenciales no configuradas
      "resource_not_found",    // Archivo/URL/entidad no existe
      "rate_limited",          // API rate limit
      "unknown",
    ]),
    error_message: z.string(),
    retryable: z.boolean(),
    duration_ms: z.number().int().nonnegative(),
    failed_at: z.string().datetime(),
  }),
])
export type ToolResult = z.infer<typeof ToolResult>

// ─────────────────────────────────────────────────────────────────────────────
// TOOL REGISTRY
// El catálogo de todos los tools disponibles en esta instalación de Oli.
// El Tool Router lee de aquí para decidir qué tools ofrecer al modelo.
// ─────────────────────────────────────────────────────────────────────────────

export const ToolRegistry = z.object({
  /** Versión del registry — para cache invalidation */
  version: z.string(),

  /** Cuándo se escanearon los MCP servers */
  last_scanned_at: z.string().datetime(),

  /** Todos los tools disponibles */
  tools: z.record(z.string(), ToolDefinition),

  /** MCP servers conocidos y su estado */
  mcp_servers: z.record(z.string(), z.object({
    name: z.string(),
    status: z.enum(["connected", "disconnected", "error"]),
    tools_count: z.number().int().nonnegative(),
    last_ping_at: z.string().datetime().optional(),
  })),
})
export type ToolRegistry = z.infer<typeof ToolRegistry>
