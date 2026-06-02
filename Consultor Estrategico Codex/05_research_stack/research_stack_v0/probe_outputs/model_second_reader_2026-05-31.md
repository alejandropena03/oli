# Model second reader probe

Fecha: 2026-05-31T19:25:10.163993+00:00

# Evaluación Crítica — Oli vs. State of the Art

---

## Veredicto

Oli tiene una arquitectura ambiciosa y bien direccionada, pero presenta **dos brechas estructurales** que lo separan del SOTA: el modelo de runtime/SSH y la profundidad de la capa de memoria. La dirección es correcta; la ejecución requiere ajustes antes de que el sistema sea competitivo y seguro.

---

## Score Runtime/SSH: 5/10

**Lo que está bien:**
- Separación entre SSH como canal admin/power-user y no como bypass de permisos → correcto.
- Mission Kernel + audit log + sandbox Linux → alineado con Zero Trust / Teleport.
- Desktop Bridge + app/API/CLI → cubre los vectores de acceso modernos (Claude Code Desktop, Cloudflare browser SSH).

**Gaps críticos:**
- **No hay evidencia de session recording granular** estilo Teleport (grabación de sesión con replay + command-level audit). Audit log genérico no es suficiente.
- **No menciona approval gates para comandos de riesgo** (RCE, exfiltración de claves, SSRF). Claude Code y agentes de coding SOTA ya implementan command approval workflows.
- **Sandbox Linux sin especificar límites**: ¿seccomp? ¿namespaces? ¿network policy? Sin esto, el sandbox es nominal, no efectivo.
- **SSH como power-user channel sin definir qué comandos están permitidos** → riesgo de root shell de facto.
- **No hay mención de modelo de amenaza documentado** para el runtime remoto.

---

## Score Memoria: 6/10

**Lo que está bien:**
- Postgres + pgvector como base → sólido y práctico.
- Campos de provenance (confidence, source, status, reason, source missions) → alineado con SOTA.
- Mission Black Box + After Action Review + playbooks → diferenciador real.
- User inspect/edit/delete/export → correcto para trust y control.

**Gaps críticos:**
- **No hay jerarquía de memoria** (core vs. archival vs. working). Letta demuestra que esto es esencial para escalar sin contaminar el contexto.
- **No hay knowledge graph temporal**. Zep/Graphiti muestran que relaciones entre entidades y su evolución en tiempo son críticas para business data cambiante. pgvector solo resuelve similitud, no relaciones ni temporalidad.
- **No hay write-time reconciliation**. Mem0 extrae entidades y relaciones al escribir; Oli no menciona extracción estructurada ni deduplicación al ingreso.
- **No hay evals de memoria**. Sin métricas de recall/precision de memoria, no se puede iterar con confianza.
- **Memory entries con expires_at es bueno pero insuficiente**: falta policy de degradación gradual (confidence decay) y no solo TTL binario.

---

## Gaps Críticos (resumen)

| # | Gap | Severidad |
|---|-----|-----------|
| 1 | Sin session recording granular (Teleport-style) | 🔴 Alta |
| 2 | Sin approval gates para comandos de riesgo en runtime | 🔴 Alta |
| 3 | Sin jerarquía de memoria (core/archival/working) | 🔴 Alta |
| 4 | Sin knowledge graph temporal (solo vector, no relaciones) | 🟡 Media-Alta |
| 5 | Sin write-time entity extraction / reconciliation | 🟡 Media |
| 6 | Sin evals de memoria | 🟡 Media |
| 7 | Sandbox sin especificar mecanismos (seccomp/ns/policy) | 🟡 Media |

---

## Qué Construir Primero

**Fase 1 (bloqueador de seguridad):**
1. **Session recording + command-level audit** en el runtime. Sin esto, no se lanza terminal/SSH.
2. **Approval gates** para comandos de riesgo (definir allowlist + prompt para el resto).

**Fase 2 (memoria competitiva):**
3. **Jerarquía de memoria**: core (siempre en contexto), archival (buscada on-demand), working (misión actual). Migrar el esquema actual a esta estructura.
4. **Write-time entity extraction** sobre los campos de memoria existentes (usar LLM para extraer entidades/relaciones al crear entries).

**Fase 3 (diferenciación):**
5. **Knowledge graph layer** sobre o junto a pgvector para relaciones temporales.
6. **Memory evals**: definir métricas de recall y precision por tipo de memoria.

---

**Decisión ejecutiva:** No lanzar runtime/SSH hasta Fase 1 completa. La memoria actual es funcional pero no competitiva a escala — Fase 2 es el mínimo para estar al nivel SOTA. El Mission Black Box y los playbooks son el diferenciador real de Oli; protegerlos con runtime seguro y memoria robusta es la prioridad.
