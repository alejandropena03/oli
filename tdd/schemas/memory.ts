/**
 * OLI — Memory Schema
 *
 * El sistema de memoria de Oli tiene 3 capas: User, Company y Mission.
 * La memoria es lo que hace que Oli mejore con el uso — convierte
 * cada interacción en conocimiento persistente que reduce fricción futura.
 *
 * Principios (ADR-009):
 * - Escritura automática — Oli guarda sin pedir aprobación
 * - El founder edita/borra después, no aprueba antes
 * - Declaraciones explícitas del founder siempre ganan sobre inferencias
 * - Oli puede explicar por qué recuerda cualquier cosa
 *
 * @see ADR-003 — Memory Storage (JSON files V0, hybrid V3+)
 * @see ADR-009 — Memory Auto-Write
 */

import { z } from "zod"

// ─────────────────────────────────────────────────────────────────────────────
// ENUMS
// ─────────────────────────────────────────────────────────────────────────────

export const MemoryLayer = z.enum([
  "user",     // Preferencias, estilo, hábitos, correcciones del founder
  "company",  // Producto, ICP, roadmap, decisiones, competidores
  "mission",  // Historial de misiones, playbook candidates, patrones
])
export type MemoryLayer = z.infer<typeof MemoryLayer>

export const MemorySource = z.enum([
  "explicit",         // El founder lo declaró directamente — máxima confianza
  "correction",       // El founder corrigió una inferencia previa
  "inferred_high",    // Patrón observado ≥ 3 veces — alta confianza
  "inferred_low",     // Observación única — baja confianza
  "mission_outcome",  // Derivado del resultado de una misión
  "imported",         // Importado desde archivo o integración externa
])
export type MemorySource = z.infer<typeof MemorySource>

export const MemoryStatus = z.enum([
  "active",     // En uso — el Memory Graph la incluye en recall
  "archived",   // El founder la archivó — no se usa pero existe
  "deleted",    // Soft delete — no se usa, solo en audit log
  "superseded", // Reemplazada por una versión más reciente de la misma clave
])
export type MemoryStatus = z.infer<typeof MemoryStatus>

// ─────────────────────────────────────────────────────────────────────────────
// MEMORY ENTRY
// La unidad atómica de memoria — un hecho sobre el usuario, la empresa o misiones.
// ─────────────────────────────────────────────────────────────────────────────

export const MemoryEntry = z.object({
  id: z.string().uuid(),

  /** Capa a la que pertenece */
  layer: MemoryLayer,

  /**
   * Clave semántica — define el "tema" de esta memoria.
   * Formato: snake_case descriptivo.
   * Ejemplo: "preferred_output_format", "product_icp", "competitor_lindy"
   */
  key: z.string().regex(/^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)*$/,
    "Formato: snake_case o dot.notation"),

  /** El valor de la memoria — puede ser string, número, objeto, array */
  value: z.unknown(),

  /**
   * Confianza de Oli en este hecho (0-1).
   * 1.0 = declaración explícita del founder.
   * 0.9+ = patrón repetido ≥ 5 veces.
   * 0.7-0.9 = patrón repetido 2-4 veces.
   * < 0.7 = inferencia única — baja confianza.
   */
  confidence: z.number().min(0).max(1),

  /** Cómo se originó esta memoria */
  source: MemorySource,

  status: MemoryStatus.default("active"),

  /**
   * Explicación de por qué Oli recuerda esto.
   * Requerido — Oli siempre puede justificar sus memorias.
   * Ejemplo: "Lo declaraste explícitamente en sesión del 2026-05-26"
   * Ejemplo: "Observé que rechazaste listas > 5 ítems en 4 misiones consecutivas"
   */
  reason: z.string(),

  /** Misión(es) que generaron o actualizaron esta memoria */
  source_mission_ids: z.array(z.string().uuid()).default([]),

  created_at: z.string().datetime(),
  updated_at: z.string().datetime(),

  /**
   * Historial de versiones anteriores de esta memoria.
   * Se guarda cuando el founder edita o cuando Oli actualiza con nueva info.
   */
  history: z.array(z.object({
    value: z.unknown(),
    changed_at: z.string().datetime(),
    changed_by: z.enum(["founder_explicit", "founder_correction", "oli_auto"]),
    previous_confidence: z.number().min(0).max(1),
  })).default([]),

  /**
   * Tags para facilitar recall y filtrado en el Memory Panel
   */
  tags: z.array(z.string()).default([]),

  /**
   * Fecha de expiración opcional — algunas memorias son temporales.
   * Ejemplo: "Esta semana el founder está en modo deep work — no interrumpir"
   */
  expires_at: z.string().datetime().optional(),
})
export type MemoryEntry = z.infer<typeof MemoryEntry>

// ─────────────────────────────────────────────────────────────────────────────
// USER MEMORY
// Preferencias, estilo de trabajo y patrones del founder.
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Claves canónicas de User Memory.
 * Usadas por el Orchestrator y suboperadores para tomar decisiones.
 * El founder puede agregar claves custom — estas son las que Oli conoce nativamente.
 */
export const USER_MEMORY_KEYS = {
  // Comunicación
  PREFERRED_OUTPUT_FORMAT: "preferred_output_format",      // "bullet_points" | "prose" | "table"
  MAX_LIST_ITEMS: "max_list_items",                        // número
  PREFERRED_LANGUAGE: "preferred_language",                // "es" | "en" | ...
  RESPONSE_LENGTH: "preferred_response_length",            // "concise" | "detailed"

  // Decisiones y trabajo
  RISK_TOLERANCE: "risk_tolerance",                        // "low" | "medium" | "high"
  DECISION_STYLE: "decision_style",                        // "data_driven" | "intuition_first"
  WORK_HOURS: "typical_work_hours",                        // { start: "09:00", end: "18:00", timezone }

  // Permisos y autonomía
  AUTO_APPROVE_THRESHOLD: "auto_approve_permission_class", // 0-4: Oli auto-aprueba hasta esta clase
  PREFERRED_CONFIRMATION_STYLE: "confirmation_style",      // "minimal" | "verbose"

  // Patrones observados
  FREQUENT_MISSION_TYPES: "frequent_mission_types",        // array de tipos
  REJECTION_PATTERNS: "rejection_patterns",                // qué tipos de output rechaza

  // Correcciones acumuladas
  CORRECTION_THEMES: "correction_themes",                  // temas recurrentes de corrección
} as const

// ─────────────────────────────────────────────────────────────────────────────
// COMPANY MEMORY
// Contexto organizacional persistente del producto/empresa del founder.
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Claves canónicas de Company Memory.
 */
export const COMPANY_MEMORY_KEYS = {
  // Producto
  PRODUCT_NAME: "product.name",
  PRODUCT_THESIS: "product.thesis",
  PRODUCT_PROMISE: "product.promise",
  PRODUCT_STAGE: "product.stage",                          // "pre-product" | "v0" | ...

  // Mercado
  ICP: "market.icp",
  POSITIONING: "market.positioning",
  PRICING: "market.pricing",
  COMPETITORS: "market.competitors",                       // array de CompetitorEntry

  // Roadmap
  CURRENT_MILESTONE: "roadmap.current_milestone",
  NEXT_MILESTONE: "roadmap.next_milestone",

  // Stack técnico
  TECH_STACK: "tech.stack",
  RUNTIME: "tech.runtime",

  // Decisiones importantes
  KEY_DECISIONS: "decisions.key",                          // array de DecisionRecord

  // Team
  TEAM_SIZE: "team.size",
  TEAM_ROLES: "team.roles",
} as const

// ─────────────────────────────────────────────────────────────────────────────
// MISSION MEMORY
// Historial de misiones — para aprender patrones y detectar playbooks.
// ─────────────────────────────────────────────────────────────────────────────

export const MissionMemoryEntry = z.object({
  mission_id: z.string().uuid(),
  mission_type: z.string(),         // "research_brief" | "code_review" | ...
  goal_summary: z.string(),

  outcome: z.enum(["completed", "completed_with_warning", "failed", "cancelled"]),

  // Métricas de la misión
  duration_ms: z.number().int().nonnegative(),
  cost_usd: z.number().nonnegative(),
  human_time_saved_hr: z.number().nonnegative(),
  repair_cycles: z.number().int().nonnegative(),

  // Playbook
  playbook_candidate: z.boolean(),
  playbook_id: z.string().uuid().optional(),  // Si ya fue convertida en playbook

  // Aprendizajes
  what_worked: z.array(z.string()),
  what_failed: z.array(z.string()),

  completed_at: z.string().datetime(),
})
export type MissionMemoryEntry = z.infer<typeof MissionMemoryEntry>

// ─────────────────────────────────────────────────────────────────────────────
// MEMORY QUERY
// Cómo el Mission Kernel y suboperadores consultan la memoria.
// ─────────────────────────────────────────────────────────────────────────────

export const MemoryQuery = z.object({
  /** Qué capas consultar */
  layers: z.array(MemoryLayer),

  /**
   * Búsqueda por clave exacta.
   * Para claves conocidas (USER_MEMORY_KEYS, COMPANY_MEMORY_KEYS).
   */
  keys: z.array(z.string()).optional(),

  /**
   * Búsqueda semántica — qué necesita saber el caller.
   * En V0: búsqueda por substring en key/value.
   * En V3+: embedding similarity.
   */
  semantic_query: z.string().optional(),

  /** Solo memorias con confianza >= este umbral */
  min_confidence: z.number().min(0).max(1).default(0.5),

  /** Solo memorias activas (excluye archived/deleted/superseded) */
  active_only: z.boolean().default(true),

  /** Máximo de resultados */
  limit: z.number().int().positive().default(20),

  /** Tags que deben estar presentes */
  tags: z.array(z.string()).optional(),
})
export type MemoryQuery = z.infer<typeof MemoryQuery>

// ─────────────────────────────────────────────────────────────────────────────
// MEMORY GRAPH
// Interfaz del módulo de memoria — invariante entre implementaciones.
// V0: JSON files. V3+: vector DB + structured DB.
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Contrato del Memory Graph — la interfaz que el Mission Kernel usa.
 * La implementación concreta cambia entre versiones (ADR-003),
 * pero este contrato NO cambia.
 */
export interface MemoryGraphInterface {
  /** Guardar una memoria (crea o actualiza) */
  remember(entry: Omit<MemoryEntry, "id" | "created_at" | "updated_at" | "history">): Promise<MemoryEntry>

  /** Recuperar memorias según query */
  recall(query: MemoryQuery): Promise<MemoryEntry[]>

  /** Recuperar una memoria específica por ID */
  get(id: string): Promise<MemoryEntry | null>

  /** Recuperar por clave exacta en una capa */
  getByKey(layer: MemoryLayer, key: string): Promise<MemoryEntry | null>

  /** Editar una memoria existente (registra en history) */
  edit(id: string, value: unknown, reason: string): Promise<MemoryEntry>

  /** Archivar una memoria (soft) */
  archive(id: string): Promise<void>

  /** Eliminar una memoria (soft delete) */
  forget(id: string): Promise<void>

  /** Listar todas las memorias de una capa con filtros */
  list(filter: { layer?: MemoryLayer; status?: MemoryStatus; tags?: string[]; limit?: number }): Promise<MemoryEntry[]>

  /** Explicar por qué existe una memoria */
  explain(id: string): Promise<{ reason: string; source_missions: MissionMemoryEntry[] }>

  /** Guardar entrada en Mission Memory */
  recordMission(entry: MissionMemoryEntry): Promise<void>

  /** Buscar misiones similares (para contexto y detección de playbooks) */
  findSimilarMissions(mission_type: string, limit?: number): Promise<MissionMemoryEntry[]>
}

// ─────────────────────────────────────────────────────────────────────────────
// MEMORY PANEL VIEW
// La proyección de memoria que el founder ve en el UI.
// ─────────────────────────────────────────────────────────────────────────────

export const MemoryPanelView = z.object({
  /** Memorias de usuario agrupadas por categoría */
  user: z.record(z.string(), z.array(MemoryEntry)),

  /** Memorias de empresa agrupadas por categoría */
  company: z.record(z.string(), z.array(MemoryEntry)),

  /**
   * Memorias agregadas recientemente (últimas 24h) — para revisión opcional.
   * Aparecen highlighted en el UI.
   */
  recently_added: z.array(MemoryEntry),

  /** Estadísticas generales */
  stats: z.object({
    total_entries: z.number().int(),
    explicit_entries: z.number().int(),
    inferred_entries: z.number().int(),
    missions_recorded: z.number().int(),
    oldest_entry_at: z.string().datetime().optional(),
  }),
})
export type MemoryPanelView = z.infer<typeof MemoryPanelView>
