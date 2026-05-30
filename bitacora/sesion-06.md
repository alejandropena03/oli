# Sesión 06 — 2026-05-27

## Contexto
Primera validación del TDD usando GitHub MCP en vivo. Datos duros de repos reales, no suposiciones.

## Metodología
GitHub MCP conectado → queries en paralelo → datos de stars, estado (archived/active), fechas de actualización → cambios aplicados directamente a los ADRs afectados.

## Hallazgos con evidencia de GitHub

| Repo | Stars | Estado | Implicación para TDD |
|---|---|---|---|
| `minio/minio` | 61,013 | **🔴 archived: true** | MinIO reemplazado por SeaweedFS |
| `pgvector/pgvector` | 21,501 | ✅ Updated 2026-05-27 | pgvector confirma ser la elección correcta |
| `pgvectorscale` (Timescale) | 3,031 | ✅ Activo | Disponible para escala mayor |
| `seaweedfs/seaweedfs` | 32,530 | ✅ Activo, Apache 2.0 | Reemplazo de MinIO confirmado |
| `rustfs/rustfs` | 28,050 | ✅ Activo, Apache 2.0 | Alternativa: 2.3x más rápido que MinIO |
| `QwenLM/Qwen3` | 27,263 | ✅ Activo | Modelos Qwen3 actualizados en ADR-016 |
| `QwenLM/Qwen3-Coder` | 16,569 | ✅ Activo | Para tasks de código en Tier 1/2 |

## Cambios aplicados al TDD

| Archivo | Cambio |
|---|---|
| `ADR-003-memory-storage.md` | ChromaDB → pgvector. BGE-M3 para español. Qwen3-Embedding como alternativa. |
| `ADR-005-runtime-stack.md` | Redis → Valkey. MinIO → SeaweedFS. |
| `ADR-016-model-routing-gpu-strategy.md` | Tier 1: Qwen3 27B como sweet spot RTX 5090. Tier 2: Qwen3 35B-A3B MoE (más eficiente que Llama 70B). |
| `stack-decision.md` | Tabla actualizada. Sección de validación con datos de GitHub. |

## Inconsistencias internas resueltas

- ADR-003 (ChromaDB) vs ADR-010 (pgvector): **resuelto → pgvector ganó**
- Stagehand v3 descrito como "built on Playwright": **pendiente actualizar ADR-011** (v3 usa CDP directo)

## Segunda ronda — ADR-011 + arXiv

### Hallazgos GitHub para ADR-011

| Repo | Stars | Dato clave |
|---|---|---|
| `browser-use/browser-use` | **95,876** ⭐ | El ADR decía "50K+" — casi el doble. Python, compatible con ADR-005. |
| `browserbase/mcp-server-browserbase` | 3,359 | MCP server activo, topics incluyen `playwright` pero v3 es CDP-native |

### Cambios aplicados a ADR-011
- Browser Use actualizado de "50K+" a **95,876 stars** (verificado)
- Stagehand v3 corregido: **ya no usa Playwright como dependencia** — CDP nativo directamente. Playwright sigue integrable como driver opcional.
- Browser Use re-evaluado: con backend Python (ADR-005), es compatible como subagente interno para tasks de browser completamente autónomas
- Tabla comparativa Stagehand vs Browser Use agregada con criterios de cuándo usar cada uno

### Hallazgos arXiv para ADR-003 (memoria)
- arXiv:2605.26252 "Is Agent Memory a Database?" — confirma que la memoria debe estar en DB real, no solo RAG
- arXiv:2604.04853 "MemMachine" — agentes necesitan store/organizar/recall/razonar, no solo retrieval
- Mem0 benchmark ECAI 2025 — diseño híbrido (RAG semántico + structured DB) es el mejor en largo horizonte
- **El diseño de memoria de Oli está alineado con el estado del arte académico 2026**

### LangGraph confirmado por arXiv
- arXiv:2605.22502 referencia LangGraph como "most widely adopted agent framework ~30K stars (Mar 2026)"
- arXiv:2603.16104 confirma LangGraph para composición de workflows agenticos
- Decisión del TDD 100% validada por literatura académica actual

## Tercera ronda — Market Research

### Documento creado: `tdd/domain/market-research-2026-05-27.md`

**Hallazgos clave:**

**Mercado:**
- AI Agents market 2026: $11.5B-$15B → 2035: $221B-$294B (CAGR 34-46%)
- 85% empresas implementarán AI agents para fin de 2025

**Competidores con precios reales:**
- Lindy: $19.99-$199.99/mes, créditos por acción, sin modelo local, sin ejecución real
- Manus: $20-$200/mes, créditos expiran, cloud-only (Meta), sin memoria real

**GPU on-demand (nuestro costo):**
- RTX 4090: $0.43-0.50/hr (RunPod serverless)
- A6000: ~$0.41/hr (Vast.ai)
- H100: $1.99/hr (RunPod) / $1.25/hr spot

**Pricing de Oli propuesto:**
- Starter: $49/mes (RTX 4090, 1 user)
- Pro: $99/mes (A6000, 3 users, Qwen3 70B local)
- Team: $299/mes (H100, 15 users)
- Margen bruto estimado: 70-80%

**Argumento de valor:**
- vs. Lindy ($49.99): Oli tiene ejecución real, modelo local, memoria, audit trail al mismo precio
- vs. Manus ($20): Oli es más caro pero los créditos no expiran, es local-first, y aprende con el uso
- vs. DIY APIs: menos costoso en APIs + todo el setup incluido

## Pendiente

- Conseguir API keys Exa + Tavily para ampliar el research workflow con semantic search
- Validar Valkey directamente en GitHub (repo: valkey-io/valkey)
- Entrevistas reales con founders/operators del ICP (ningún dato es de entrevistas directas aún)
- WTP real con metodología correcta
