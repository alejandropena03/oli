/**
 * OLI — Mission Schema
 *
 * La misión es la unidad de trabajo de Oli. Todo empieza con una intención
 * y termina con un entregable validado, un reporte y un evento de aprendizaje.
 *
 * Este schema es el agregado principal del sistema — el Mission Kernel
 * es el único módulo que puede mutar el estado de una misión.
 *
 * Patrón: Zod como source of truth → TypeScript types derivados.
 *
 * @see ADR-006 — Mission Blocking Strategy (3 intentos antes de escalar)
 * @see ADR-007 — Intent Clarification (preguntar siempre, máx 2 preguntas)
 * @see ADR-008 — Parallel Missions (límite conservador por modelo)
 * @see Event Storming V3 — 46 eventos de dominio
 */

import { z } from "zod"
import { PermissionClass, ToolCall, ToolResult } from "./tool"

// ─────────────────────────────────────────────────────────────────────────────
// MISSION STATUS
// Los 18 estados válidos de una misión.
// Solo el Mission Kernel puede cambiar este valor.
// ─────────────────────────────────────────────────────────────────────────────

export const MissionStatus = z.enum([
  "idle",
  "listening",
  "intake_received",
  "interpreting_intent",
  "clarifying",             // Esperando respuesta del founder (ADR-007)
  "retrieving_context",
  "classifying_permissions",
  "planning",
  "awaiting_approval",      // Esperando aprobación del founder (permission_class ≥ 2)
  "executing",
  "repairing",              // Oli intentando reparar autónomamente (ADR-006)
  "validating",
  "delivering",
  "generating_report",
  "updating_memory",
  "completed",
  "blocked",                // Agotó 3 intentos de repair — necesita founder
  "failed",
  "cancelled",
  "archived",
  "queued",                 // En cola esperando capacidad (ADR-008)
])
export type MissionStatus = z.infer<typeof MissionStatus>

export const MissionSource = z.enum([
  "chat",              // El founder escribió la intención directamente en la UI de Oli
  "playbook",          // Creada desde un playbook reutilizable
  "scheduled",         // Disparada por schedule/cron
  "api",               // Creada via API externa
  // OpenClaw channels (ADR-013) — el founder crea misiones desde donde ya está
  "openclaw_whatsapp",
  "openclaw_telegram",
  "openclaw_slack",
  "openclaw_discord",
  "openclaw_signal",
  "openclaw_imessage",
  "openclaw_teams",
  "openclaw_other",    // Cualquier otro canal de OpenClaw
])
export type MissionSource = z.infer<typeof MissionSource>

// ─────────────────────────────────────────────────────────────────────────────
// INTENT
// La intención interpretada del founder — resultado de InterpretIntent.
// ─────────────────────────────────────────────────────────────────────────────

export const ClarificationQuestion = z.object({
  /** La pregunta que Oli hace al founder */
  question: z.string(),

  /** Por qué necesita esta info — "necesito saber X porque determinará si hago A o B" */
  purpose: z.string(),

  /** Ronda de clarificación (máx 2 rondas por ADR-007) */
  round: z.number().int().min(1).max(2),
})
export type ClarificationQuestion = z.infer<typeof ClarificationQuestion>

export const ClarificationExchange = z.object({
  questions: z.array(ClarificationQuestion),
  answers: z.record(z.string(), z.string()),  // question → answer
  completed_at: z.string().datetime().optional(),
})
export type ClarificationExchange = z.infer<typeof ClarificationExchange>

export const InterpretedIntent = z.object({
  /** Qué quiere lograr el founder */
  goal: z.string(),

  /**
   * Criterios de éxito verificables — el ValidationSuboperator los chequea.
   * Deben ser observables: "brief tiene < 600 palabras", "3 competidores identificados"
   */
  success_criteria: z.array(z.string()).min(1),

  /** Formato esperado del output */
  output_format: z.string(),

  /** Scope — qué está IN y qué está OUT de esta misión */
  scope: z.object({
    in_scope: z.array(z.string()),
    out_of_scope: z.array(z.string()).default([]),
  }),

  /**
   * Clarificaciones realizadas antes de llegar a este intent.
   * Null si no se necesitaron clarificaciones.
   */
  clarifications: z.array(ClarificationExchange).default([]),

  /**
   * Confianza de Oli en la interpretación (0-1).
   * Si < 0.7, debería clarificar aunque no sea obligatorio.
   */
  confidence: z.number().min(0).max(1),
})
export type InterpretedIntent = z.infer<typeof InterpretedIntent>

// ─────────────────────────────────────────────────────────────────────────────
// CONTEXT
// Contexto recuperado del Memory Graph para esta misión.
// ─────────────────────────────────────────────────────────────────────────────

export const MissionContext = z.object({
  /** Preferencias y patrones del usuario relevantes para esta misión */
  user_preferences: z.record(z.string(), z.unknown()),

  /** Hechos de la empresa relevantes (ICP, producto, decisiones) */
  company_context: z.record(z.string(), z.unknown()),

  /**
   * Misiones anteriores similares — para aprender de ellas y detectar playbooks.
   * Solo metadata, no los outputs completos (demasiado peso).
   */
  similar_past_missions: z.array(z.object({
    mission_id: z.string().uuid(),
    goal: z.string(),
    outcome: z.enum(["completed", "failed", "cancelled"]),
    duration_ms: z.number().int(),
    cost_usd: z.number(),
  })),

  /**
   * Playbooks aplicables — si existe uno, el Orchestrator puede usarlo
   * como plan base en lugar de generar uno desde cero.
   */
  applicable_playbooks: z.array(z.object({
    playbook_id: z.string().uuid(),
    name: z.string(),
    relevance_score: z.number().min(0).max(1),
  })),
})
export type MissionContext = z.infer<typeof MissionContext>

// ─────────────────────────────────────────────────────────────────────────────
// PLAN & STEPS
// El plan es la secuencia de pasos que Oli ejecutará para cumplir la misión.
// ─────────────────────────────────────────────────────────────────────────────

export const StepStatus = z.enum([
  "pending",
  "executing",
  "completed",
  "failed",
  "repairing",     // En ciclo de repair autónomo (ADR-006)
  "repaired",      // Reparado con éxito
  "repaired_partial", // Reparado con scope reducido
  "skipped",       // Skipped por decisión del plan
  "blocked",       // No se pudo reparar — escalado a founder
])
export type StepStatus = z.infer<typeof StepStatus>

export const RepairAttempt = z.object({
  attempt_number: z.number().int().min(1).max(3),
  strategy: z.enum(["retry", "alternative_tool", "alternative_approach", "reduce_scope"]),
  started_at: z.string().datetime(),
  completed_at: z.string().datetime().optional(),
  outcome: z.enum(["success", "partial_success", "failed"]),
  notes: z.string().optional(),
})
export type RepairAttempt = z.infer<typeof RepairAttempt>

export const MissionStep = z.object({
  /** ID único del step — referenciado en el audit trail */
  id: z.string().uuid(),

  /** Número de orden en el plan — empieza en 1 */
  order: z.number().int().positive(),

  /** Qué hace este step — descripción legible para el founder */
  description: z.string(),

  /** Qué suboperador o módulo ejecuta este step */
  executor: z.enum([
    "MarketResearchSuboperator",
    "TechnicalArchitectSuboperator",
    "SecurityReviewerSuboperator",
    "ExecutionSuboperator",
    "ValidationSuboperator",
    "UXCriticSuboperator",
    "GrowthSuboperator",
    "MemoryCuratorSuboperator",
    "Orchestrator",   // El orquestador mismo hace síntesis
  ]),

  /** Tools que este step puede necesitar */
  required_tools: z.array(z.string()),  // nombres en ToolRegistry

  /** Clase de permiso requerida para este step */
  permission_class: PermissionClass,

  /** Si es reversible — afecta qué repair strategies están disponibles */
  reversible: z.boolean(),

  /** Tiempo estimado — para timeout y UI */
  estimated_duration_ms: z.number().int().positive(),

  status: StepStatus.default("pending"),

  /** Input del step — puede venir del plan o del output de un step anterior */
  input: z.record(z.unknown()).optional(),

  /** Output si el step completó (éxito o parcial) */
  output: z.unknown().optional(),

  /** Tool calls realizadas en este step */
  tool_calls: z.array(ToolCall).default([]),
  tool_results: z.array(ToolResult).default([]),

  /**
   * Intentos de repair si el step falló (ADR-006: máx 3 antes de bloquear)
   */
  repair_attempts: z.array(RepairAttempt).default([]),

  /** Error final si el step terminó en blocked */
  final_error: z.object({
    error_type: z.string(),
    message: z.string(),
    all_repair_attempts: z.array(RepairAttempt),
  }).optional(),

  /** Timestamps */
  started_at: z.string().datetime().optional(),
  completed_at: z.string().datetime().optional(),
})
export type MissionStep = z.infer<typeof MissionStep>

export const MissionPlan = z.object({
  /** ID del plan — se versiona si el founder pide revisión */
  id: z.string().uuid(),

  /** Versión del plan — incrementa en cada revisión */
  version: z.number().int().min(1).default(1),

  /** Steps en orden de ejecución */
  steps: z.array(MissionStep),

  /**
   * Clase de permiso total del plan — el máximo entre todos los steps.
   * Determina si se requiere aprobación del founder.
   */
  total_permission_class: PermissionClass,

  /** Estimados totales del plan */
  estimates: z.object({
    duration_ms: z.number().int().positive(),
    cost_usd: z.number().nonnegative(),
    human_time_saved_hr: z.number().nonnegative(),
  }),

  created_at: z.string().datetime(),

  /**
   * Si el founder revisó y pidió cambios — las notas de revisión
   */
  revision_notes: z.string().optional(),

  /**
   * Historial de versiones anteriores del plan
   */
  previous_versions: z.array(z.object({
    version: z.number().int(),
    created_at: z.string().datetime(),
    revision_reason: z.string(),
  })).default([]),
})
export type MissionPlan = z.infer<typeof MissionPlan>

// ─────────────────────────────────────────────────────────────────────────────
// APPROVAL
// Registro de aprobaciones del founder — parte del audit trail.
// ─────────────────────────────────────────────────────────────────────────────

export const ApprovalRecord = z.discriminatedUnion("decision", [
  z.object({
    decision: z.literal("approved"),
    approved_by: z.string(),   // user_id
    approved_at: z.string().datetime(),
    notes: z.string().optional(),
  }),
  z.object({
    decision: z.literal("rejected"),
    rejected_by: z.string(),
    rejected_at: z.string().datetime(),
    reason: z.string(),
  }),
  z.object({
    decision: z.literal("revision_requested"),
    requested_by: z.string(),
    requested_at: z.string().datetime(),
    revision_notes: z.string(),
  }),
])
export type ApprovalRecord = z.infer<typeof ApprovalRecord>

// ─────────────────────────────────────────────────────────────────────────────
// VALIDATION
// ─────────────────────────────────────────────────────────────────────────────

export const ValidationResult = z.object({
  passed: z.boolean(),

  /** Criterios verificados — mapea a success_criteria del InterpretedIntent */
  criteria_results: z.array(z.object({
    criterion: z.string(),
    passed: z.boolean(),
    evidence: z.string().optional(),
  })),

  /** Score general (0-1) */
  score: z.number().min(0).max(1),

  /** Si failed: ¿puede Oli intentar reparar solo? */
  auto_repair_possible: z.boolean(),

  validated_at: z.string().datetime(),
  repair_cycle: z.number().int().nonnegative().default(0),  // 0 = primera validación
})
export type ValidationResult = z.infer<typeof ValidationResult>

// ─────────────────────────────────────────────────────────────────────────────
// EVIDENCE
// Todo artefacto, log y fuente generado durante la misión.
// El Evidence Drawer del founder consume esto.
// ─────────────────────────────────────────────────────────────────────────────

export const EvidenceRef = z.object({
  id: z.string().uuid(),
  type: z.enum([
    "file",        // Archivo generado
    "url",         // Fuente web consultada
    "api_response",// Respuesta de API
    "screenshot",  // Screenshot de browser/desktop
    "log",         // Log de ejecución
    "tool_output", // Output de un tool específico
    "validation",  // Resultado de validación
  ]),
  label: z.string(),
  path_or_url: z.string(),
  created_at: z.string().datetime(),
  step_id: z.string().uuid().optional(),  // Qué step lo generó
  size_bytes: z.number().int().nonnegative().optional(),
})
export type EvidenceRef = z.infer<typeof EvidenceRef>

// ─────────────────────────────────────────────────────────────────────────────
// COST RECORD
// Registro detallado de costo — tokens, tiempo, valor generado.
// El Cost Tracker escribe aquí.
// ─────────────────────────────────────────────────────────────────────────────

export const CostRecord = z.object({
  /** Tokens usados por llamadas al modelo */
  tokens: z.object({
    input: z.number().int().nonnegative(),
    output: z.number().int().nonnegative(),
    cache_read: z.number().int().nonnegative().default(0),
    cache_write: z.number().int().nonnegative().default(0),
  }),

  /** Costo monetario USD */
  model_cost_usd: z.number().nonnegative(),

  /** Costo de tools externos (APIs pagas, sandbox time, etc.) */
  tool_cost_usd: z.number().nonnegative().default(0),

  /** Duración total de la misión */
  duration_ms: z.number().int().nonnegative(),

  /**
   * Estimado de tiempo humano ahorrado.
   * Calculado por lookup de tipo de misión — editable por el founder.
   */
  human_time_saved_hr: z.number().nonnegative(),

  /** Costo total (model + tools) */
  total_cost_usd: z.number().nonnegative(),

  /** Ratio valor/costo: human_hours_saved / total_cost_usd */
  value_ratio: z.number().nonnegative(),
})
export type CostRecord = z.infer<typeof CostRecord>

// ─────────────────────────────────────────────────────────────────────────────
// MISSION REPORT
// El resumen ejecutivo post-misión que ve el founder.
// ─────────────────────────────────────────────────────────────────────────────

export const MissionReport = z.object({
  mission_id: z.string().uuid(),

  /** Resumen ejecutivo en lenguaje natural */
  summary: z.string(),

  /** Qué se entregó */
  deliverable_description: z.string(),

  /** Steps completados / total */
  steps_completed: z.number().int().nonnegative(),
  steps_total: z.number().int().positive(),

  /** Resultado de validación */
  validation_result: ValidationResult,

  /** Ciclos de repair realizados */
  repair_cycles_used: z.number().int().nonnegative(),

  /** Costo real */
  cost: CostRecord,

  /**
   * Si Oli detectó que esta misión podría convertirse en playbook.
   * Criterio: tipo similar ≥ 3 veces O estructura claramente reutilizable.
   */
  playbook_candidate: z.boolean(),
  playbook_candidate_reason: z.string().optional(),

  generated_at: z.string().datetime(),
})
export type MissionReport = z.infer<typeof MissionReport>

// ─────────────────────────────────────────────────────────────────────────────
// CHECKPOINT
// Estado serializado de una misión en progreso — para resume (ADR hotspot H04).
// ─────────────────────────────────────────────────────────────────────────────

export const MissionCheckpoint = z.object({
  mission_id: z.string().uuid(),
  checkpointed_at: z.string().datetime(),
  current_step_id: z.string().uuid(),
  completed_steps: z.array(z.string().uuid()),
  partial_outputs: z.record(z.string(), z.unknown()),  // step_id → output parcial
  status_before_checkpoint: MissionStatus,
})
export type MissionCheckpoint = z.infer<typeof MissionCheckpoint>

// ─────────────────────────────────────────────────────────────────────────────
// MISSION (AGREGADO PRINCIPAL)
// El objeto completo de una misión — todo el estado en un lugar.
// ─────────────────────────────────────────────────────────────────────────────

export const Mission = z.object({
  // ── Identidad ──────────────────────────────────────────────────────────────
  id: z.string().uuid(),
  source: MissionSource,
  status: MissionStatus,

  // ── Input original ─────────────────────────────────────────────────────────
  raw_input: z.string().min(1),
  created_at: z.string().datetime(),

  // ── Intent (nullable hasta que se interprete) ──────────────────────────────
  interpreted_intent: InterpretedIntent.nullable().default(null),

  // ── Contexto (nullable hasta que se recupere) ─────────────────────────────
  context: MissionContext.nullable().default(null),

  // ── Plan (nullable hasta que se genere) ───────────────────────────────────
  plan: MissionPlan.nullable().default(null),

  /**
   * Clase de permiso total — el max(steps.permission_class).
   * Determina si requiere aprobación del founder.
   * null hasta que el plan esté creado.
   */
  permission_class: PermissionClass.nullable().default(null),

  // ── Aprobaciones ──────────────────────────────────────────────────────────
  approval_records: z.array(ApprovalRecord).default([]),

  // ── Ejecución ─────────────────────────────────────────────────────────────
  current_step_index: z.number().int().nonnegative().default(0),

  // ── Validación ────────────────────────────────────────────────────────────
  validation_result: ValidationResult.nullable().default(null),

  // ── Output final ──────────────────────────────────────────────────────────
  output: z.unknown().nullable().default(null),
  output_accepted_with_warning: z.boolean().default(false),

  // ── Evidencia ─────────────────────────────────────────────────────────────
  evidence: z.array(EvidenceRef).default([]),

  // ── Reporte ───────────────────────────────────────────────────────────────
  report: MissionReport.nullable().default(null),

  // ── Costo (acumulado durante ejecución) ────────────────────────────────────
  cost: CostRecord.partial().default({}),

  // ── Estado de bloqueo ─────────────────────────────────────────────────────
  block_reason: z.object({
    step_id: z.string().uuid(),
    message: z.string(),
    all_repair_attempts: z.array(RepairAttempt),
    unblock_instructions: z.string(),  // Qué necesita el founder hacer
  }).nullable().default(null),

  // ── Playbook de origen (si aplica) ────────────────────────────────────────
  playbook_id: z.string().uuid().nullable().default(null),

  // ── Checkpoint para resume ────────────────────────────────────────────────
  checkpoint: MissionCheckpoint.nullable().default(null),

  // ── Timestamps ────────────────────────────────────────────────────────────
  started_at: z.string().datetime().nullable().default(null),
  completed_at: z.string().datetime().nullable().default(null),
  archived_at: z.string().datetime().nullable().default(null),
})
export type Mission = z.infer<typeof Mission>

// ─────────────────────────────────────────────────────────────────────────────
// MISSION QUEUE
// El estado de todas las misiones en el sistema (ADR-008: paralelo conservador).
// ─────────────────────────────────────────────────────────────────────────────

export const MissionQueue = z.object({
  /**
   * Límite de misiones activas simultáneas.
   * default: min(3, model_capacity)
   */
  max_concurrent: z.number().int().min(1).max(10).default(3),

  /** Misiones ejecutando o validando — consumen capacidad del modelo */
  active: z.array(z.string().uuid()),

  /** Misiones en estados que no consumen modelo (awaiting_approval, blocked, clarifying) */
  pending_human_input: z.array(z.string().uuid()),

  /** Misiones esperando que haya capacidad disponible */
  queued: z.array(z.string().uuid()),
})
export type MissionQueue = z.infer<typeof MissionQueue>

// ─────────────────────────────────────────────────────────────────────────────
// HELPERS — Funciones de type narrowing comunes
// ─────────────────────────────────────────────────────────────────────────────

/** Una misión está "activa" si consume capacidad del modelo */
export const isActiveMission = (m: Mission): boolean =>
  ["executing", "repairing", "validating", "generating_report", "updating_memory"]
    .includes(m.status)

/** Una misión terminó — ya no puede transicionar (excepto a archived) */
export const isTerminalMission = (m: Mission): boolean =>
  ["completed", "failed", "cancelled", "archived"].includes(m.status)

/** Una misión necesita input del founder */
export const needsHumanInput = (m: Mission): boolean =>
  ["clarifying", "awaiting_approval", "blocked"].includes(m.status)
