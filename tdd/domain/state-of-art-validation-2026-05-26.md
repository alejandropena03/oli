# Validación State of the Art — TDD de Oli

**Fecha:** 2026-05-26
**Método:** Research web en paralelo sobre cada decisión técnica del TDD
**Resultado:** 4 cambios necesarios, 8 decisiones confirmadas, 2 inconsistencias internas resueltas

---

## RESUMEN EJECUTIVO

| Decisión | Estado | Acción |
|---|---|---|
| LangGraph como orquestador | ✅ Confirmado — v1.0, producción en Uber/LinkedIn/Klarna | Ninguna |
| FastAPI como backend | ✅ Confirmado — estándar de facto para AI backends | Ninguna |
| PostgreSQL + pgvector | ✅ Confirmado — pero hay inconsistencia interna con ChromaDB | **Resolver inconsistencia** |
| n8n para automatizaciones | ✅ Confirmado — v2.0 lanzado, 150k+ stars, production-grade | Ninguna |
| Ollama → vLLM | ✅ Confirmado pero **incompleto** — falta LocalAI como abstracción | **Agregar LocalAI** |
| nomic-embed-text | ⚠️ Desactualizado — nomic-embed-text v2 disponible, Qwen3-Embedding mejor | **Actualizar** |
| Redis | ⚠️ Reemplazar por Valkey — 8% más rápido, 20% más barato, open source real | **Actualizar** |
| MinIO para artifacts | 🔴 MinIO archivó su repo en Feb 2026 — reemplazar por SeaweedFS | **Actualizar urgente** |
| Stagehand v3 | ✅ Confirmado — pero v3 ya no usa Playwright, usa CDP directo | **Actualizar nota** |
| Llama 3.1 para Tier 1/2 | ⚠️ Actualizar — Qwen3 35B-A3B MoE es más eficiente en 2026 | **Actualizar** |

---

## HALLAZGOS DETALLADOS

### 1. LangGraph — ✅ CONFIRMADO

**Pregunta:** ¿Sigue siendo LangGraph la mejor opción para orquestación de agentes?

**Hallazgo:** Sí. LangGraph alcanzó v1.0 en octubre 2025. Es el framework #1 para workflows stateful complejos según múltiples benchmarks de producción. Usado en producción por Uber, LinkedIn, Klarna. Superó a CrewAI en GitHub stars en early 2026.

**Características que confirman la elección para Oli:**
- Durable state persistente automático ✓
- Human-in-the-loop interrupts nativos ✓
- Checkpointing y resume tras crash ✓
- Streaming de tokens, tool calls y state updates ✓
- LangSmith para observabilidad node-by-node ✓

**Decisión del TDD: sin cambio.**

---

### 2. FastAPI — ✅ CONFIRMADO

**Hallazgo:** FastAPI es el estándar de facto para Python AI backends en 2026. Para endpoints LLM-bound (200ms+), la diferencia de throughput con Node.js desaparece. La arquitectura de producción más común en 2026 es: Python/FastAPI para AI + Node para gateway/realtime.

**Decisión del TDD: sin cambio.**

---

### 3. pgvector vs ChromaDB — 🔴 INCONSISTENCIA INTERNA RESUELTA

**El problema encontrado:** ADR-003 dice ChromaDB para V0-V2, pero ADR-010 dice pgvector dentro de Postgres para todo. Son incompatibles.

**El research dice:**
- ChromaDB: buen default para < 1M vectores, simple, $30/mes self-hosted
- pgvector: hasta 50M vectores, $0 incremental si ya tienes Postgres, transaccional
- Qdrant: mejor para filtering complejo y producción a escala

**Decisión correcta para Oli:** pgvector desde V0.

**Razón:** Oli ya tiene Postgres (para el estado de misiones). Agregar pgvector es activar una extensión. ChromaDB sería una segunda base de datos solo para vectores — complejidad innecesaria. La arquitectura de una sola DB es más simple y correcta.

**Acción:** ADR-003 se actualiza — ChromaDB eliminado, pgvector desde V0.

---

### 4. Modelos locales Tier 1/2 — ⚠️ ACTUALIZAR

**Pregunta:** ¿Siguen siendo Llama 3.1 y Qwen 2.5 los mejores para Tier 1 y 2?

**Hallazgo:** No exactamente. En Mayo 2026:

**Tier 1 (intent, clasificación, queries — 8-14B params):**
- Llama 3.1 8B sigue siendo sólido
- **Qwen 3.6 27B (nueva) es mejor si la GPU lo aguanta** — 160 tok/s en RTX 6000
- Para RTX 5090 (32GB): Qwen 3.6 27B Q4_K_M es el nuevo sweet spot
- Phi-4 y Gemma 4 son alternativas válidas con licencia comercial limpia

**Tier 2 (planning, synthesis — 70B params):**
- Llama 3.1 70B sigue válido
- **Qwen 3 35B-A3B MoE es más eficiente:** 3B parámetros activos por token, 240 tok/s, cabe en 32GB
- Para A6000 (48GB): Qwen 3 35B-A3B MoE es mejor que Llama 70B full precision

**Embeddings:** nomic-embed-text v1.5 sigue válido para inglés. **Para español/multilingüe: BGE-M3 o Qwen3-Embedding**. Nomic embed v2 (MoE architecture) es el upgrade directo.

**Acción:** Actualizar ADR-016 con los modelos 2026.

---

### 5. Ollama → LocalAI → vLLM — ⚠️ FALTA LocalAI

**Hallazgo confirmado (del research anterior):**
- Ollama: desarrollo local + macOS, single user, suficiente para V0-V1
- vLLM: throughput en producción, Linux-only, 9-16x más rápido bajo carga
- **LocalAI: capa de abstracción** — API OpenAI-compatible que puede usar Ollama/vLLM/SGLang por detrás. Ya está en ADR-005 pero no en ADR-016.

**SGLang** también confirmado como alternativa válida a vLLM — benchmarks comparables, más simple de operar.

**Acción:** Actualizar ADR-016 explícitamente con LocalAI como capa de abstracción.

---

### 6. Redis → Valkey — ⚠️ ACTUALIZAR

**Hallazgo:** Redis cambió su licencia en 2024. La comunidad forkeó a **Valkey** bajo Linux Foundation.

- Valkey 8.1: 8% más throughput que Redis OSS, 20% menos memoria
- Adoptado por AWS (Elasticache), Google Cloud (Memorystore), Akamai
- Completamente open source (BSD), drop-in replacement de Redis
- Para AI agent events: misma API, misma performance, mejor licencia

**Acción:** Reemplazar Redis por Valkey en ADR-005 y stack-decision.

---

### 7. MinIO → SeaweedFS — 🔴 URGENTE

**Hallazgo crítico:** MinIO archivó su repositorio community edition en **Febrero 2026**. Ya no es open source mantenido.

**Alternativas evaluadas:**
- **SeaweedFS** (recomendado): adoptado por Kubeflow Pipelines como default post-MinIO, 12 años de desarrollo, cientos de contributors, Apache 2.0
- **Garage**: single Go binary, sin dependencias, ideal para setups pequeños
- **RustFS**: más rápido que MinIO en benchmarks, Apache 2.0, pero más nuevo

**Para Oli:** SeaweedFS es el reemplazo más sólido. S3-compatible, bien mantenido, escala.

**Acción:** Reemplazar MinIO por SeaweedFS en ADR-005 y stack-decision.

---

### 8. Stagehand v3 — ✅ CONFIRMADO con nota importante

**Hallazgo:** Stagehand v3 está en producción y es uno de los 5 stacks dominantes de browser automation en 2026. Pero hay un detalle importante:

**V3 ya no usa Playwright internamente — usa CDP directo.** El ADR-011 dice "built on Playwright" — eso era v2. V3 habla directamente al browser via Chrome DevTools Protocol, eliminando la dependencia de Playwright como runtime.

Esto es una mejora (44% más rápido), no un problema. Pero el ADR dice algo incorrecto.

**Acción:** Actualizar nota en ADR-011.

---

### 9. n8n — ✅ CONFIRMADO

**Hallazgo:** n8n lanzó v2.0 en 2026 con enfoque en security, scalability y AI agents. 150k+ stars. 400+ nodos. Multi-model AI support (Claude, Gemini, Groq). El "action layer" de facto para AI agents.

**Decisión del TDD: sin cambio.**

---

### 10. LangGraph v1.0 — checkpoint storage

**Hallazgo adicional:** LangGraph 1.0 incluye **built-in persistence** sin necesidad de implementar PostgresSaver manualmente en V0. Se puede usar `MemorySaver` en V0 (en memoria) y migrar a `PostgresSaver` en V1.

Esto simplifica el build V0.

**Acción:** Actualizar ADR-010 con esta nota de implementación.

---

## INCONSISTENCIAS INTERNAS DETECTADAS

| Inconsistencia | Archivos afectados | Resolución |
|---|---|---|
| ADR-003 dice ChromaDB, ADR-010 dice pgvector | ADR-003, ADR-010 | pgvector gana — una sola DB |
| ADR-005 menciona LocalAI pero ADR-016 no | ADR-016 | Agregar LocalAI explícitamente |
| Stagehand v3 descrito como "built on Playwright" | ADR-011 | V3 usa CDP directo, no Playwright |
| Redis mencionado en stack pero ya obsoleto como OSS | ADR-005, stack-decision | Reemplazar por Valkey |
| MinIO mencionado como artifact store | ADR-005, stack-decision | Reemplazar por SeaweedFS (MinIO archivado Feb 2026) |

