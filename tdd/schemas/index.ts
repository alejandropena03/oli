/**
 * OLI — Schemas Index
 *
 * Single entry point para todos los schemas de Oli.
 * Importar desde aquí en todo el código de implementación:
 *
 *   import { Mission, MissionStatus, ToolDefinition, MemoryEntry } from "../schemas"
 *
 * Stack de validación:
 *   - Zod: source of truth para schemas y validación runtime
 *   - TypeScript: tipos derivados de Zod via z.infer<>
 *   - @anthropic-ai/claude-agent-sdk: tool() pattern compatible con estos schemas
 */

// ── Tools & Connectivity ──────────────────────────────────────────────────────
export * from "./tool"

// ── Mission (agregado principal) ──────────────────────────────────────────────
export * from "./mission"

// ── Memory ────────────────────────────────────────────────────────────────────
export * from "./memory"

// ── Playbooks ─────────────────────────────────────────────────────────────────
export * from "./playbook"

// ── Suboperators ──────────────────────────────────────────────────────────────
export * from "./suboperator"
