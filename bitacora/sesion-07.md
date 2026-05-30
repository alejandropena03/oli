# Sesión 07 — 2026-05-27

## Contexto
Sesión de investigación de mercado, validación del TDD con GitHub MCP, y diseño del modelo de pricing definitivo.

---

## Artefactos creados / actualizados

| Artefacto | Acción | Descripción |
|---|---|---|
| `tdd/domain/state-of-art-validation-2026-05-27.md` | Creado | Resumen de todos los hallazgos del research con GitHub MCP |
| `tdd/domain/market-research-2026-05-27.md` | Creado | Competencia, TAM, GPU pricing, primeras versiones de pricing |
| `tdd/domain/pricing-model-v2.md` | Creado | Pricing con números reales RunPod (descartado — lógica de tiers incorrecta) |
| `tdd/domain/pricing-model-v3.md` | Creado ✅ DEFINITIVO | Modelo híbrido base + créditos. La versión correcta. |
| `tdd/adrs/ADR-003-memory-storage.md` | Actualizado | ChromaDB → pgvector. BGE-M3 para español. Validación arXiv. |
| `tdd/adrs/ADR-005-runtime-stack.md` | Actualizado | Redis → Valkey. MinIO → SeaweedFS. LocalAI abstracción. |
| `tdd/adrs/ADR-011-browser-strategy.md` | Actualizado | Stagehand v3 CDP-native (no Playwright). Browser-use 95,876 stars re-evaluado. |
| `tdd/adrs/ADR-016-model-routing-gpu-strategy.md` | Actualizado | Qwen3 35B-A3B MoE como Tier 2. Qwen3 27B como Tier 1 sweet spot. |
| `tdd/stack/stack-decision.md` | Actualizado | Tabla de validación con datos de GitHub. MinIO y Redis marcados. |

---

## Hallazgos del GitHub MCP (datos verificados)

| Repo | Stars | Estado | Cambio en TDD |
|---|---|---|---|
| `minio/minio` | 61,013 | **🔴 archived: true** | MinIO → SeaweedFS |
| `pgvector/pgvector` | 21,501 | ✅ Updated ayer | Confirma pgvector como elección correcta |
| `seaweedfs/seaweedfs` | 32,530 | ✅ Apache 2.0 | Reemplazo de MinIO |
| `rustfs/rustfs` | 28,050 | ✅ Apache 2.0 | Alternativa a SeaweedFS |
| `browser-use/browser-use` | **95,876** | ✅ Python | Re-evaluado: compatible con stack Python |
| `QwenLM/Qwen3` | 27,263 | ✅ Activo | Modelos actualizados en ADR-016 |
| `QwenLM/Qwen3-Coder` | 16,569 | ✅ Activo | Tier 1/2 para código |

---

## Hallazgos arXiv (papers 2026)

- **arXiv:2605.26252** "Is Agent Memory a Database?" — confirma arquitectura de memoria de Oli
- **arXiv:2604.04853** "MemMachine" — agentes necesitan store/organizar/recall, no solo RAG estático
- **arXiv:2605.22502** — cita LangGraph como "most widely adopted agent framework ~30K stars"
- Arquitectura de memoria de Oli alineada con estado del arte académico 2026

---

## Investigación de mercado

### Competencia
| Competidor | Precio | Limitación |
|---|---|---|
| Lindy | $19.99-$199.99/mes | Sin GPU local, sin memoria real, sin ejecución |
| Manus | $20-$200/mes | Cloud-only (Meta), créditos expiran, sin memoria |
| OpenClaw | $0 (open source) | CVEs críticos, inestable, setup complejo |

### TAM
- AI Agents market 2026: **$11.5B-$15B**
- Crecimiento a 2035: **$221B-$294B** (CAGR 34-46%)

### GPU pricing real (RunPod, verificado)
- RTX 4090 serverless: **$1.116/hr**
- A6000 serverless: **$1.224/hr**
- H100 SXM serverless: **$4.176/hr**
- H100 on-demand: **$3.29/hr**
- H100 reservada (negociada 5+ seats): **~$2.20/hr**

### Uso real del ICP
- Knowledge workers con AI agents ahorran **6.4 hrs/semana** (McKinsey/Slack 2026)
- Equivale a **~37 hrs de GPU activa/mes** por seat activo

---

## Modelo de pricing definitivo (v3)

**Modelo:** Híbrido — base fija + créditos de uso
**Referencia:** 43% de AI SaaS usa híbrido en 2026, creciendo a 61%
**Unidad:** 1 crédito = 1 minuto de GPU activa (intuitivo para el usuario)
**Créditos ruedan** (cap 2x plan mensual) — diferenciador vs. Manus

| Tier | Precio | GPU | Créditos incluidos | Créditos extra |
|---|---|---|---|---|
| **Starter** | $29/mes (1 seat) | RTX 4090 | 300/mes (~5 hrs) | $0.05/crédito |
| **Pro** | $79/seat/mes | A6000 | 1,200/seat/mes (~20 hrs) | $0.05/crédito |
| **Team** | $59/seat/mes (mín 5) | H100 compartida | 1,500/seat/mes (~25 hrs) | $0.04/crédito |

**La escalera:** Starter < Pro por seat > Team por seat (economía de escala H100)
**APIs externas:** el usuario conecta y paga las suyas en todos los tiers

---

## Estado del TDD al cierre de sesión 07

| Área | Estado |
|---|---|
| 18 ADRs (001-018) | ✅ Todos validados con estado del arte 2026 |
| State-of-art validation | ✅ GitHub MCP + arXiv + web search |
| Market research V1 | ✅ Competencia, TAM, GPU pricing |
| Pricing model v3 | ✅ Híbrido base + créditos — definitivo |
| Constitución de Oli (14 pilares) | ✅ |
| System prompts | ✅ |
| LangGraph mission graph | ✅ |
| 2 slices en papel | ✅ |
| Multi-user ADR-018 | ✅ |
| Setup wizard | ✅ |
| Research workflow con MCPs | ✅ |
| **Build V0 (código)** | 🔲 **PRÓXIMO PASO** |

## Pricing model v4 — corrección final

El v3 tenía gross margins de 38-58% — insuficientes para cubrir OPEX + growth + reinversión.
Con benchmarks reales de AI SaaS (target 75% gross margin), los precios correctos son:

| Tier | Precio | COGS/seat | Gross margin |
|---|---|---|---|
| Starter | **$179/mes** | $44.55 | 74.9% |
| Pro | **$169/seat/mes** | $41.93 | 75.1% |
| Team | **$249/seat/mes** | $61.40 | 75.3% |

**15 seats Team → $2,814/mes de gross profit** (vs. $500 del v3).
Archivo: `tdd/domain/pricing-model-v4.md`

## Próximo paso
`pyproject.toml` → `packages/mission_kernel/mission_state.py` → `state_machine.py` → primer test e2e del Slice-001
