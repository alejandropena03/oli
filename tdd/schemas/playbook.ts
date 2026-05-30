/**
 * OLI — Playbook Schema
 *
 * Los playbooks son la memoria procedimental de Oli — convierten trabajo
 * repetido en sistemas reutilizables. Cuando Oli detecta que ejecuta
 * el mismo tipo de misión repetidamente, propone un playbook.
 *
 * El founder aprueba, rechaza o edita. Una vez aprobado, el playbook
 * reemplaza el ciclo completo de InterpretIntent + CreatePlan con
 * un template pre-validado.
 *
 * @see Event Storming V3 — Sección 7: Sistema de Playbooks
 */

import { z } from "zod"
import { PermissionClass } from "./tool"
import { MissionStatus } from "./mission"

// ─────────────────────────────────────────────────────────────────────────────
// PLAYBOOK STATUS
// ─────────────────────────────────────────────────────────────────────────────

export const PlaybookStatus = z.enum([
  "proposed",    // Oli lo detectó y propuso — esperando aprobación del founder
  "approved",    // El founder lo aprobó — disponible para ejecutar
  "deprecated",  // Ya no se usa — puede haber una versión nueva
])
export type PlaybookStatus = z.infer<typeof PlaybookStatus>

// ─────────────────────────────────────────────────────────────────────────────
// PLAYBOOK VARIABLE
// Las variables que el founder puede customizar en cada ejecución.
// ─────────────────────────────────────────────────────────────────────────────

export const PlaybookVariableType = z.enum([
  "string",
  "number",
  "boolean",
  "enum",        // Lista de opciones válidas
  "entity",      // Referencia a una entidad conocida (competitor, feature, etc.)
])
export type PlaybookVariableType = z.infer<typeof PlaybookVariableType>

export const PlaybookVariable = z.object({
  /** Nombre de la variable — referenciada en los steps como {variable_name} */
  name: z.string().regex(/^[a-z][a-z0-9_]*$/),

  /** Descripción para el founder — qué debe ingresar */
  description: z.string(),

  type: PlaybookVariableType,

  /** Si type = "enum": las opciones válidas */
  enum_options: z.array(z.string()).optional(),

  /** Valor por defecto — si el founder no lo cambia, se usa este */
  default_value: z.unknown().optional(),

  /** Si true, el founder DEBE proveer un valor — no hay default */
  required: z.boolean().default(false),

  /**
   * Ejemplo de valor — mostrado en el UI para guiar al founder.
   * Ejemplo: "Lindy" para una variable competitor
   */
  example: z.string().optional(),
})
export type PlaybookVariable = z.infer<typeof PlaybookVariable>

// ─────────────────────────────────────────────────────────────────────────────
// PLAYBOOK STEP
// Los steps de un playbook son templates — se instancian con las variables
// del founder en cada ejecución.
// ─────────────────────────────────────────────────────────────────────────────

export const PlaybookStep = z.object({
  id: z.string().uuid(),
  order: z.number().int().positive(),

  /** Descripción del step — puede incluir variables como {topic} */
  description: z.string(),

  executor: z.enum([
    "MarketResearchSuboperator",
    "TechnicalArchitectSuboperator",
    "SecurityReviewerSuboperator",
    "ExecutionSuboperator",
    "ValidationSuboperator",
    "UXCriticSuboperator",
    "GrowthSuboperator",
    "MemoryCuratorSuboperator",
    "Orchestrator",
  ]),

  /** Tools que este step típicamente usa */
  typical_tools: z.array(z.string()),

  permission_class: PermissionClass,
  reversible: z.boolean(),

  /** Tiempo típico de este step (del historial de ejecuciones) */
  typical_duration_ms: z.number().int().positive(),

  /** Criterios de éxito específicos de este step */
  success_criteria: z.array(z.string()),

  /**
   * Si true, este step puede ejecutarse en paralelo con el anterior.
   * El Orchestrator decide el scheduling real.
   */
  parallelizable: z.boolean().default(false),
})
export type PlaybookStep = z.infer<typeof PlaybookStep>

// ─────────────────────────────────────────────────────────────────────────────
// PLAYBOOK EXECUTION RECORD
// Registro de cada vez que se ejecutó un playbook — para estadísticas.
// ─────────────────────────────────────────────────────────────────────────────

export const PlaybookExecutionRecord = z.object({
  execution_id: z.string().uuid(),
  playbook_id: z.string().uuid(),
  mission_id: z.string().uuid(),

  /** Variables usadas en esta ejecución */
  variables_used: z.record(z.string(), z.unknown()),

  outcome: z.enum(["completed", "failed", "cancelled"]),

  duration_ms: z.number().int().nonnegative(),
  cost_usd: z.number().nonnegative(),
  human_time_saved_hr: z.number().nonnegative(),
  repair_cycles: z.number().int().nonnegative(),

  /**
   * Si el playbook tuvo que desviarse del template — qué cambió.
   * Si está vacío, el playbook corrió exactamente como estaba definido.
   */
  deviations: z.array(z.object({
    step_id: z.string().uuid(),
    reason: z.string(),
    what_changed: z.string(),
  })).default([]),

  executed_at: z.string().datetime(),
})
export type PlaybookExecutionRecord = z.infer<typeof PlaybookExecutionRecord>

// ─────────────────────────────────────────────────────────────────────────────
// PLAYBOOK (AGREGADO)
// ─────────────────────────────────────────────────────────────────────────────

export const Playbook = z.object({
  // ── Identidad ──────────────────────────────────────────────────────────────
  id: z.string().uuid(),
  name: z.string().min(3),  // "research-brief-v1"
  version: z.number().int().min(1).default(1),
  status: PlaybookStatus.default("proposed"),

  // ── Qué hace ──────────────────────────────────────────────────────────────
  description: z.string(),

  /**
   * Patrón de trigger en lenguaje natural.
   * El Orchestrator usa esto para detectar si una intención encaja con el playbook.
   * Ejemplo: "investiga [tema] y dame un brief de [formato]"
   */
  trigger_pattern: z.string(),

  /**
   * Tags de categoría — para el Playbook Library view
   */
  tags: z.array(z.string()),

  // ── Variables ─────────────────────────────────────────────────────────────
  variables: z.array(PlaybookVariable),

  // ── Plan ──────────────────────────────────────────────────────────────────
  steps: z.array(PlaybookStep),

  /**
   * Clase de permiso total del playbook — max(steps.permission_class).
   * Calculado al crear el playbook, re-calculado si cambian los steps.
   */
  total_permission_class: PermissionClass,

  // ── Métricas (actualizadas en cada ejecución) ─────────────────────────────
  execution_count: z.number().int().nonnegative().default(0),
  success_count: z.number().int().nonnegative().default(0),

  /** Tasa de éxito (0-1) */
  success_rate: z.number().min(0).max(1).default(0),

  /** Promedios del historial de ejecuciones */
  avg_duration_ms: z.number().nonnegative().default(0),
  avg_cost_usd: z.number().nonnegative().default(0),
  avg_human_time_saved_hr: z.number().nonnegative().default(0),

  // ── Origen ────────────────────────────────────────────────────────────────
  /**
   * La misión que originó este playbook.
   * Oli detectó el patrón en esta misión y propuso convertirla en playbook.
   */
  origin_mission_id: z.string().uuid(),

  /**
   * Razón por la que Oli propuso este playbook.
   * Ejemplo: "Ejecutaste 3 research briefs con estructura similar en 2 semanas"
   */
  proposal_reason: z.string(),

  // ── Historial de versiones ────────────────────────────────────────────────
  previous_versions: z.array(z.object({
    version: z.number().int(),
    deprecated_at: z.string().datetime(),
    deprecation_reason: z.string(),
  })).default([]),

  // ── Ejecuciones ───────────────────────────────────────────────────────────
  executions: z.array(PlaybookExecutionRecord).default([]),

  // ── Timestamps ────────────────────────────────────────────────────────────
  proposed_at: z.string().datetime(),
  approved_at: z.string().datetime().optional(),
  deprecated_at: z.string().datetime().optional(),
  last_executed_at: z.string().datetime().optional(),
})
export type Playbook = z.infer<typeof Playbook>

// ─────────────────────────────────────────────────────────────────────────────
// PLAYBOOK LIBRARY VIEW
// La proyección del Playbook Engine que el founder ve en el UI.
// ─────────────────────────────────────────────────────────────────────────────

export const PlaybookLibraryView = z.object({
  /** Playbooks aprobados — listos para usar */
  approved: z.array(Playbook),

  /** Propuestas pendientes de revisión del founder */
  pending_approval: z.array(Playbook),

  /** Estadísticas de la biblioteca */
  stats: z.object({
    total_playbooks: z.number().int(),
    total_executions: z.number().int(),
    total_human_hours_saved: z.number().nonnegative(),
    most_used_playbook: z.string().optional(),
  }),
})
export type PlaybookLibraryView = z.infer<typeof PlaybookLibraryView>

// ─────────────────────────────────────────────────────────────────────────────
// PLAYBOOK ENGINE INTERFACE
// Contrato del módulo que gestiona playbooks — invariante entre versiones.
// ─────────────────────────────────────────────────────────────────────────────

export interface PlaybookEngineInterface {
  /**
   * Evalúa si una misión completada debe generar un playbook candidate.
   * Criterio: tipo similar ≥ 3 veces OR estructura claramente reutilizable.
   */
  evaluateCandidate(mission_id: string): Promise<{
    is_candidate: boolean
    reason?: string
    draft?: Omit<Playbook, "id" | "proposed_at" | "execution_count" | "success_count" | "success_rate">
  }>

  /**
   * Instancia un playbook con las variables del founder.
   * Retorna el plan de misión listo para ejecutar.
   */
  instantiate(playbook_id: string, variables: Record<string, unknown>): Promise<{
    steps: PlaybookStep[]
    total_permission_class: PermissionClass
    estimates: { duration_ms: number; cost_usd: number; human_time_saved_hr: number }
  }>

  /** Registra el resultado de una ejecución */
  recordExecution(record: PlaybookExecutionRecord): Promise<void>

  /**
   * Detecta si la intención de una nueva misión encaja con un playbook existente.
   * Retorna el playbook más relevante si existe.
   */
  matchIntent(intent: string): Promise<{ playbook: Playbook; confidence: number } | null>
}
