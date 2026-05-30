# ADR-003 — Memoria infinita: arquitectura completa

**Estado:** accepted — v2 completamente reescrito
**Fecha:** 2026-05-26
**Decisión del founder:** La memoria es la feature más importante del producto.

---

## El problema real

Un LLM tiene ventana de contexto finita. Una empresa con historial, meses de misiones, miles de documentos — nada cabe ahí. Sin RAG, Oli empieza cada misión desde cero. Eso no es Oli.

## Decisión: RAG desde V0, memoria ilimitada — pgvector en Postgres

**Validado por GitHub 2026-05-27:** pgvector/pgvector → 21,501 stars, activo (updated ayer).

pgvector desde el primer día — dentro de Postgres. No es opcional. No es V3+. Es el núcleo.
ChromaDB eliminado — era una segunda DB innecesaria cuando pgvector da lo mismo dentro de Postgres.

SIN RAG: Oli olvida todo entre misiones.
CON RAG: Oli recuerda todo, para siempre, y recupera solo lo relevante.

---

## Las 4 capas de memoria

### Capa 1 — Contexto activo (RAM)
La misión actual + lo recuperado del vector store. ~10-50K tokens. Dura la sesión.

### Capa 2 — Vector store (memoria semántica — el núcleo)
Todo lo que Oli aprendió, en embeddings. Búsqueda por similitud semántica.
- V0+: **pgvector dentro de PostgreSQL** — una sola DB para estado Y semántica
- Escala hasta 50M vectores. $0 incremental si ya tienes Postgres.
- pgvectorscale (Timescale) disponible para escala mayor: 3,031 stars, activo.

### Capa 3 — Base de datos estructurada
Para queries exactas: "todas las misiones de este mes", "costo total por tipo".
- V0+: **PostgreSQL** (misma instancia que el vector store)

### Capa 4 — Cold storage (archivo histórico)
Datos de más de N meses. JSON comprimido. Recuperable on-demand.

---

## Qué guarda Oli

Preferencias del usuario, correcciones, contexto de empresa (ICP, producto, competidores, roadmap, decisiones), misiones completas (qué se pidió, qué se hizo, resultado, costo), documentos analizados (contratos, emails, reportes, código), research web con fuentes, historial de contactos por canal, conversaciones, playbooks y sus versiones.

---

## Cómo funciona RAG en cada misión

```
Founder: "Oli, prepara la propuesta para Acme Corp"

RETRIEVAL — antes de hacer nada:
  Query "Acme Corp"       → reuniones pasadas, pain points, sector
  Query "propuesta"       → formato del founder, propuestas anteriores
  Query "Acme + industria"→ research previo, competidores

  Resultado: 5-15K tokens de contexto exactamente relevante
  inyectados al LLM. No todo — solo lo que importa.

EJECUCIÓN:
  Oli sabe quién es Acme, qué formato funciona, qué funcionó antes.

ALMACENAMIENTO post-misión:
  → Propuesta generada → vector store
  → Resultado (aprobada/rechazada) → actualiza el registro
  → Tiempo y costo → SQLite
```

---

## Embeddings: cuándo usar qué modelo

**V0-V1 sin GPU:** text-embedding-3-small (OpenAI). Costo ~$0.01/año. Datos van a OpenAI.

**V1+ con GPU local (inglés only):** nomic-embed-text v1.5 via Ollama. Costo $0. 100% local.

**V1+ con GPU local (español/multilingüe):** BGE-M3 (BAAI). Costo $0. Soporte 100+ idiomas.
— Qwen3-Embedding también válido si ya se usa Qwen para inferencia (mismo ecosistema).

---

## Conexión con la GPU alquilada

```
GPU ALQUILADA (RunPod, Lambda Labs, Vast.ai):
  ├── Modelo de inferencia (Ollama + Llama/Mistral/Qwen)
  │    → Reemplaza Haiku para tasks simples sin costo de API
  ├── Modelo de embeddings (nomic-embed-text) — costo $0
  ├── pgvector en Postgres (vector store — misma DB que el estado)
  └── Whisper STT (si se prefiere off-device)

MÁQUINA LOCAL (siempre):
  ├── App desktop — lo que ve el founder
  ├── Credential Vault — NUNCA en la GPU
  ├── Wake word (OpenWakeWord)
  └── OAuth callbacks (localhost:3847)
```

---

## Validación académica (arXiv 2026)

Papers recientes confirman la arquitectura de memoria de Oli:

- **arXiv:2605.26252** "Is Agent Memory a Database?" (Mayo 2026): argumenta exactamente la decisión de Oli — la memoria de agentes debe estar en una DB real, no solo en RAG estático. pgvector dentro de Postgres resuelve esto.
- **arXiv:2604.04853** "MemMachine" (Abril 2026): los agentes necesitan memoria que va más allá del document retrieval — store, organizar, recall Y razonar sobre experiencias pasadas. El Memory Graph de Oli implementa exactamente esto.
- **Mem0 benchmark (ECAI 2025)**: comparó 10 arquitecturas de memoria. El diseño híbrido (RAG semántico + structured DB) es el que mejor performa en tasks de largo horizonte.

**Hotspot resuelto por research académico:** el diseño de memoria de Oli (pgvector para semántica + Postgres para estructura + MemoryCurator que actualiza dinámicamente) está alineado con el estado del arte de 2026.

---

## La memoria como moat del producto

Un competidor puede copiar la UI, el Mission Kernel, los tools. No puede copiar 2 años de contexto acumulado de un usuario. Cuanto más usa Oli el founder, más valioso se vuelve y más difícil es irse.

---

## Estimación de volumen a 1 año de uso intensivo

- Misiones: ~2,000 | Documentos: ~5,000 | Conversaciones: ~10,000
- Total: ~500K vectores | ~2-4 GB en disco
- pgvector en Postgres maneja esto sin problema (escala hasta 50M vectores)
- Costo embeddings (OpenAI): ~$0.01/año | Con modelo local: $0

---

## Control total del usuario sobre su memoria

El founder puede ver todo, editar cualquier entrada, borrar (soft delete), archivar, exportar o resetear completamente. Oli puede explicar por qué recuerda cualquier cosa: fuente exacta, fecha, misión de origen.
