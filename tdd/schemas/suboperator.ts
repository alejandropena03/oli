/**
 * OLI — Suboperator Schema
 *
 * Los suboperadores son trabajadores internos de misión. Reglas inamovibles:
 * - El founder NUNCA los ve ni habla con ellos — solo habla con Oli
 * - NO contactan al usuario directamente
 * - NO escriben directo a memoria (solo el MemoryCuratorSuboperator sugiere)
 * - NO aprueban su propio trabajo
 * - NO bypassean permisos
 * - NO entregan respuestas finales
 * - Oli sintetiza todos sus outputs y entrega la respuesta final
 *
 * El contrato de un suboperador es simple: recibe un SuboperatorTask,
 * retorna un SuboperatorResult. El Mission Kernel orquesta el resto.
 *
 * @see SKILL.md — Sección "Suboperadores internos"
 * @see ADR-001 — Model Strategy (model-agnostic — cada suboperador puede usar el modelo óptimo)
 */

import { z } from "zod"
import { ToolCall, ToolResult } from "./tool"

// ─────────────────────────────────────────────────────────────────────────────
// SUBOPERATOR REGISTRY
// Los 8 suboperadores del sistema.
// ─────────────────────────────────────────────────────────────────────────────

export const SuboperatorName = z.enum([
  "MarketResearchSuboperator",
  "TechnicalArchitectSuboperator",
  "SecurityReviewerSuboperator",
  "ExecutionSuboperator",
  "ValidationSuboperator",
  "UXCriticSuboperator",
  "GrowthSuboperator",
  "MemoryCuratorSuboperator",
])
export type SuboperatorName = z.infer<typeof SuboperatorName>

// ─────────────────────────────────────────────────────────────────────────────
// SUBOPERATOR TASK
// Lo que el Orchestrator le da a un suboperador para procesar.
// ─────────────────────────────────────────────────────────────────────────────

export const SuboperatorTask = z.object({
  /** ID único de esta tarea */
  id: z.string().uuid(),

  /** Qué suboperador debe procesarla */
  suboperator: SuboperatorName,

  /** Misión a la que pertenece */
  mission_id: z.string().uuid(),

  /** Step de la misión que origina esta tarea */
  step_id: z.string().uuid(),

  /**
   * Instrucción específica para el suboperador.
   * El Orchestrator la genera en lenguaje natural, precisa y accionable.
   * Ejemplo: "Investiga Lindy.ai: identifica sus 3 principales fortalezas,
   *           2 debilidades y su posicionamiento de precio. Fuentes requeridas."
   */
  instruction: z.string().min(10),

  /**
   * Criterios que debe cumplir el output para que el ValidationSuboperator lo apruebe.
   * El suboperador debe conocer estos criterios — trabaja hacia ellos.
   */
  success_criteria: z.array(z.string()),

  /**
   * Contexto relevante del Memory Graph para esta tarea específica.
   * El Orchestrator filtra y pasa solo lo relevante — no el contexto completo.
   */
  context: z.record(z.string(), z.unknown()),

  /**
   * Tools disponibles para esta tarea.
   * El Orchestrator filtra según el tipo de suboperador y la tarea.
   */
  available_tools: z.array(z.string()),

  /**
   * Input de steps anteriores que este step necesita.
   * Key = step_id, Value = output de ese step.
   */
  prior_step_outputs: z.record(z.string(), z.unknown()),

  /**
   * Modelo a usar para esta tarea (ADR-001: model-agnostic).
   * El Model Router decide el default; el Orchestrator puede overridearlo.
   */
  model_config: z.object({
    provider: z.enum(["anthropic", "openai", "ollama", "gemini"]),
    model: z.string(),
    temperature: z.number().min(0).max(1),
    max_tokens: z.number().int().positive(),
  }),

  /**
   * Timeout para esta tarea.
   * Si el suboperador no responde en este tiempo, se trata como falla.
   */
  timeout_ms: z.number().int().positive().default(120000),

  created_at: z.string().datetime(),
})
export type SuboperatorTask = z.infer<typeof SuboperatorTask>

// ─────────────────────────────────────────────────────────────────────────────
// SUBOPERATOR RESULT
// Lo que el suboperador retorna al Mission Kernel.
// Discriminated union: success o failure — siempre uno de los dos.
// ─────────────────────────────────────────────────────────────────────────────

export const SuboperatorResult = z.discriminatedUnion("success", [
  // ── ÉXITO ──────────────────────────────────────────────────────────────────
  z.object({
    success: z.literal(true),

    task_id: z.string().uuid(),
    suboperator: SuboperatorName,
    mission_id: z.string().uuid(),
    step_id: z.string().uuid(),

    /**
     * El output principal — lo que el Orchestrator usa para síntesis.
     * Cada suboperador tiene su propia estructura de output (ver abajo).
     */
    output: z.unknown(),

    /**
     * Fuentes consultadas — requerido para MarketResearchSuboperator,
     * recomendado para todos.
     */
    sources: z.array(z.object({
      url: z.string().optional(),
      description: z.string(),
      retrieved_at: z.string().datetime().optional(),
    })).default([]),

    /**
     * Tool calls realizadas durante la ejecución.
     * El Evidence Store los indexa para el audit trail.
     */
    tool_calls_made: z.array(ToolCall),
    tool_results: z.array(ToolResult),

    /**
     * Confianza del suboperador en su output (0-1).
     * El ValidationSuboperator la usa como señal — no como validación.
     */
    confidence: z.number().min(0).max(1),

    /**
     * Si el suboperador encontró algo relevante que Oli debería recordar.
     * SOLO una sugerencia — el MemoryCuratorSuboperator decide qué guardar.
     * Regla inamovible: suboperadores nunca escriben directo a memoria.
     */
    memory_suggestions: z.array(z.object({
      layer: z.enum(["user", "company", "mission"]),
      key: z.string(),
      value: z.unknown(),
      reason: z.string(),
    })).default([]),

    /**
     * Notas para el Orchestrator — contexto que ayuda en síntesis.
     * No van al founder directamente.
     */
    notes_for_orchestrator: z.string().optional(),

    duration_ms: z.number().int().nonnegative(),
    completed_at: z.string().datetime(),
  }),

  // ── FALLA ──────────────────────────────────────────────────────────────────
  z.object({
    success: z.literal(false),

    task_id: z.string().uuid(),
    suboperator: SuboperatorName,
    mission_id: z.string().uuid(),
    step_id: z.string().uuid(),

    error_type: z.enum([
      "tool_failure",         // Tool que necesitaba no funcionó
      "model_failure",        // Llamada al modelo falló
      "timeout",              // Se agotó el tiempo
      "invalid_input",        // El input de la tarea no era válido
      "resource_not_found",   // Algo que necesitaba no existe
      "permission_insufficient", // Necesitaría más permiso para completar
      "partial_result",       // Completó parcialmente — retorna lo que pudo
      "unknown",
    ]),

    error_message: z.string(),

    /**
     * Si pudo hacer algo antes de fallar — el output parcial.
     * El Orchestrator decide si usarlo o descartar.
     */
    partial_output: z.unknown().optional(),

    /**
     * Si el suboperador cree que vale la pena reintentar
     * y con qué estrategia (alimenta el repair cycle de ADR-006)
     */
    retryable: z.boolean(),
    suggested_repair: z.enum([
      "retry",
      "alternative_tool",
      "alternative_approach",
      "reduce_scope",
      "escalate_to_founder",
    ]).optional(),

    tool_calls_made: z.array(ToolCall),
    tool_results: z.array(ToolResult),

    duration_ms: z.number().int().nonnegative(),
    failed_at: z.string().datetime(),
  }),
])
export type SuboperatorResult = z.infer<typeof SuboperatorResult>

// ─────────────────────────────────────────────────────────────────────────────
// OUTPUTS ESPECÍFICOS POR SUBOPERADOR
// Cada suboperador tiene una estructura de output conocida.
// El Orchestrator puede hacer type narrowing según el suboperador.
// ─────────────────────────────────────────────────────────────────────────────

/** MarketResearchSuboperator — análisis de mercado, competidores, ICP */
export const MarketResearchOutput = z.object({
  subjects_analyzed: z.array(z.string()),
  findings: z.array(z.object({
    subject: z.string(),
    strengths: z.array(z.string()),
    weaknesses: z.array(z.string()),
    positioning: z.string(),
    pricing: z.string().optional(),
    key_differentiators: z.array(z.string()),
  })),
  synthesis: z.string(),
  gap_identified: z.string().optional(),
  data_freshness: z.enum(["real_time", "recent", "stale", "unknown"]),
})
export type MarketResearchOutput = z.infer<typeof MarketResearchOutput>

/** TechnicalArchitectSuboperator — stack, integraciones, tradeoffs */
export const TechnicalArchitectOutput = z.object({
  recommendation: z.string(),
  options_evaluated: z.array(z.object({
    option: z.string(),
    pros: z.array(z.string()),
    cons: z.array(z.string()),
    effort_estimate: z.enum(["low", "medium", "high"]),
  })),
  risks: z.array(z.object({
    risk: z.string(),
    severity: z.enum(["low", "medium", "high"]),
    mitigation: z.string(),
  })),
  implementation_order: z.array(z.string()),
  adr_candidates: z.array(z.string()),  // Decisiones que merecen un ADR
})
export type TechnicalArchitectOutput = z.infer<typeof TechnicalArchitectOutput>

/** ValidationSuboperator — verifica outputs contra success_criteria */
export const ValidationOutput = z.object({
  overall_passed: z.boolean(),
  score: z.number().min(0).max(1),
  criteria_results: z.array(z.object({
    criterion: z.string(),
    passed: z.boolean(),
    evidence: z.string(),
    score: z.number().min(0).max(1),
  })),
  critical_failures: z.array(z.string()),  // Criterios que fallaron y son bloqueantes
  warnings: z.array(z.string()),            // Issues no bloqueantes
  auto_repair_possible: z.boolean(),
  repair_suggestion: z.string().optional(),
})
export type ValidationOutput = z.infer<typeof ValidationOutput>

/** ExecutionSuboperator — ejecuta acciones reales (mock en V0, real en V1+) */
export const ExecutionOutput = z.object({
  action_type: z.enum([
    "file_read", "file_write", "file_delete",
    "shell_command", "api_call",
    "browser_navigate", "browser_click", "browser_fill", "browser_extract",
    "computer_use_action",
    "sandbox_execute",
  ]),
  result: z.unknown(),
  side_effects: z.array(z.string()),  // Qué cambió en el mundo real
  reversible: z.boolean(),
  rollback_instructions: z.string().optional(),  // Cómo deshacer si se necesita
})
export type ExecutionOutput = z.infer<typeof ExecutionOutput>

/** MemoryCuratorSuboperator — evalúa qué merece ser recordado */
export const MemoryCuratorOutput = z.object({
  /**
   * Sugerencias de memoria — el MemoryCurator SOLO sugiere.
   * El Mission Kernel decide qué aplicar (ADR-009: auto-apply).
   */
  suggestions: z.array(z.object({
    layer: z.enum(["user", "company", "mission"]),
    key: z.string(),
    value: z.unknown(),
    confidence: z.number().min(0).max(1),
    reason: z.string(),
    priority: z.enum(["high", "medium", "low"]),
  })),

  /**
   * Memorias existentes que deberían actualizarse.
   */
  updates: z.array(z.object({
    entry_id: z.string().uuid(),
    new_value: z.unknown(),
    reason: z.string(),
  })),

  /**
   * Memorias que podrían estar desactualizadas (para revisión, no borrado auto).
   */
  potentially_stale: z.array(z.object({
    entry_id: z.string().uuid(),
    reason: z.string(),
  })),
})
export type MemoryCuratorOutput = z.infer<typeof MemoryCuratorOutput>

// ─────────────────────────────────────────────────────────────────────────────
// SUBOPERATOR INTERFACE
// Contrato que implementa cada suboperador.
// ─────────────────────────────────────────────────────────────────────────────

export interface SuboperatorInterface {
  readonly name: SuboperatorName

  /**
   * Descripción de lo que hace este suboperador.
   * Usada por el Orchestrator para decidir a quién asignar qué.
   */
  readonly description: string

  /**
   * Tipos de tareas que este suboperador puede ejecutar.
   * El Orchestrator no asigna tareas fuera de este scope.
   */
  readonly capabilities: string[]

  /**
   * Tools que este suboperador típicamente necesita.
   * El Orchestrator pre-filtra el ToolRegistry según esto.
   */
  readonly typical_tools: string[]

  /**
   * Modelo óptimo para este suboperador (ADR-001: model-agnostic).
   * El Model Router puede overridearlo según disponibilidad y costo.
   */
  readonly preferred_model: {
    provider: string
    model: string
    temperature: number
  }

  /**
   * Ejecuta la tarea y retorna el resultado.
   * Esta es la única función pública del suboperador.
   */
  execute(task: SuboperatorTask): Promise<SuboperatorResult>
}

// ─────────────────────────────────────────────────────────────────────────────
// SUBOPERATOR REGISTRY
// Metadata de todos los suboperadores — el Orchestrator la usa para routing.
// ─────────────────────────────────────────────────────────────────────────────

export const SUBOPERATOR_REGISTRY: Record<SuboperatorName, {
  description: string
  capabilities: string[]
  typical_tools: string[]
  preferred_model: { provider: string; model: string; temperature: number }
}> = {
  MarketResearchSuboperator: {
    description: "Análisis de mercado, competidores, ICP, pricing y canales — siempre con fuentes verificables",
    capabilities: ["competitor_analysis", "market_sizing", "icp_research", "pricing_research", "channel_research"],
    typical_tools: ["web_search", "web_fetch", "firecrawl"],
    preferred_model: { provider: "anthropic", model: "claude-sonnet-4-6", temperature: 0.2 },
  },
  TechnicalArchitectSuboperator: {
    description: "Stack, integraciones, tradeoffs técnicos, diagramas de arquitectura y riesgos de implementación",
    capabilities: ["stack_evaluation", "architecture_design", "integration_planning", "risk_assessment", "adr_drafting"],
    typical_tools: ["web_search", "file_read", "github_search"],
    preferred_model: { provider: "anthropic", model: "claude-sonnet-4-6", temperature: 0.1 },
  },
  SecurityReviewerSuboperator: {
    description: "Permisos, modelos de amenaza, sandboxing, secretos, prompt injection y auditabilidad",
    capabilities: ["permission_analysis", "threat_modeling", "secret_scanning", "code_security_review"],
    typical_tools: ["file_read", "code_analysis"],
    preferred_model: { provider: "anthropic", model: "claude-sonnet-4-6", temperature: 0.1 },
  },
  ExecutionSuboperator: {
    description: "Ejecución de acciones reales. Orden de selección por costo: shell/CLI → accessibility (ClawdCursor AT-SPI) → browser (Playwright/Stagehand) → OCR → screenshot → vision (Computer Use como último recurso si el usuario eligió Claude)",
    capabilities: [
      "shell_execution",         // 90% del trabajo — CLI, scripts, APIs, git, python, etc.
      "file_operations",         // filesystem local o en sandbox
      "desktop_gui",             // ClawdCursor — apps GUI sin CLI, model-agnostic
      "browser_deterministic",   // Playwright — páginas conocidas, <100ms
      "browser_ai",              // Stagehand — páginas dinámicas, act/extract/observe
      "browser_debug",           // chrome-devtools-mcp — console, network, perf
      "api_calls",               // HTTP directo
    ],
    typical_tools: [
      // Shell / OS (ADR-012 — el núcleo del "hacer todo en un computador")
      "linux_shell",             // E2B / subprocess — cualquier comando
      "file_read", "file_write", "file_delete",

      // Desktop GUI model-agnostic (ADR-012)
      "clawdcursor_computer",    // Compound tool general
      "clawdcursor_accessibility",// AT-SPI tree — más barato
      "clawdcursor_window",      // Window management
      "clawdcursor_screenshot",  // Screenshot cuando accessibility no alcanza

      // Browser (ADR-011)
      "playwright_navigate", "playwright_click", "playwright_fill", "playwright_screenshot",
      "stagehand_act", "stagehand_extract", "stagehand_observe", "stagehand_agent",
      "cdp_navigate", "cdp_console", "cdp_network",

      // APIs
      "http_request",

      // Último recurso — solo si el usuario tiene Claude y eligió esta opción
      "computer_use",
    ],
    preferred_model: { provider: "anthropic", model: "claude-haiku-4-5", temperature: 0.0 },
  },
  ValidationSuboperator: {
    description: "Verifica que los outputs cumplen los success_criteria definidos en el intent",
    capabilities: ["criteria_validation", "output_scoring", "repair_suggestion"],
    typical_tools: ["file_read"],  // Lee outputs para validarlos
    preferred_model: { provider: "anthropic", model: "claude-sonnet-4-6", temperature: 0.1 },
  },
  UXCriticSuboperator: {
    description: "Flujos de usuario, fricción, carga cognitiva y claridad ejecutiva",
    capabilities: ["ux_review", "flow_analysis", "friction_identification", "clarity_scoring"],
    typical_tools: ["file_read", "browser_navigate"],
    preferred_model: { provider: "anthropic", model: "claude-sonnet-4-6", temperature: 0.3 },
  },
  GrowthSuboperator: {
    description: "Posicionamiento, canales, landing pages, campañas y loops de adquisición. También puede entregar resultados via OpenClaw (ADR-013).",
    capabilities: ["positioning_analysis", "channel_strategy", "copy_writing", "campaign_planning", "multichannel_delivery"],
    typical_tools: ["web_search", "file_write", "openclaw_send", "openclaw_notify"],
    preferred_model: { provider: "anthropic", model: "claude-sonnet-4-6", temperature: 0.4 },
  },
  MemoryCuratorSuboperator: {
    description: "Evalúa qué merece ser recordado de una misión — solo sugiere, nunca escribe directo",
    capabilities: ["memory_evaluation", "pattern_detection", "staleness_detection"],
    typical_tools: [],  // No necesita tools — trabaja con el output de la misión
    preferred_model: { provider: "anthropic", model: "claude-haiku-4-5", temperature: 0.1 },
  },
}
