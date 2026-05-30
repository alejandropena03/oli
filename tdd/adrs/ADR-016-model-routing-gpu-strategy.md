# ADR-016 — Model Routing: Dynamic Registry, Benchmarking y GPU Strategy

**Estado:** accepted — v2 actualizado 2026-05-27
**Fecha original:** 2026-05-26
**Deciders:** Alejandro Peña (founder)

---

## El principio central

> El routing de modelos no es solo una optimización técnica.
> Es la propuesta de valor económica de Oli.

Usar siempre APIs de frontier models cuesta ~$3-15 por millón de tokens.
Una misión típica de Oli usa ~50K tokens → $0.15-0.75 con modelos frontier.
Con modelo local en nuestra GPU: ~$0.00 en tokens. Solo costo de GPU mientras corre.

El usuario que paga suscripción a Oli no debería ver factura de APIs encima, salvo cuando elige explícitamente usar un modelo premium.

---

## Problema con routing atado a nombres específicos

El TDD anterior listaba modelos específicos (Qwen3 27B, Llama 3.1 8B, etc.) como si fueran decisiones permanentes. En 2026, eso envejece en semanas.

La decisión correcta: **Oli tiene un Model Registry + benchmark local continuo. El routing usa roles y capacidades, no nombres.**

---

## Model Registry

El registry es la fuente de verdad de modelos disponibles en la instancia de Oli.

```python
@dataclass
class ModelRegistryEntry:
    model_id: str                          # identificador interno
    provider: ModelProvider                # ollama | vllm | openai | anthropic | gemini | custom
    display_name: str
    family: str                            # qwen | llama | mistral | claude | gpt | gemini | custom
    roles: list[ModelRole]                 # ver enum abajo
    local: bool
    requires_gpu: bool
    min_vram_gb: int | None
    context_tokens_estimate: int | None
    tool_use_quality: Literal["unknown", "low", "medium", "high"]
    privacy_rating: Literal["local", "external"]
    cost_model: Literal["local_compute", "api_per_token", "unknown"]
    status: Literal["candidate", "installed", "benchmarked", "disabled"]
    benchmark_scores: dict[str, float]     # poblado por BenchmarkRunner
    last_benchmarked_at: datetime | None

class ModelRole(str, Enum):
    FAST_LOCAL       = "fast_local"        # clasificación, extracción, routing
    MAIN_LOCAL       = "main_local"        # coding, razonamiento, ejecución
    EMBEDDING        = "embedding"         # memoria semántica, RAG
    PREMIUM_REASONING = "premium_reasoning" # arquitectura compleja, síntesis crítica
    PREMIUM_CODING   = "premium_coding"    # coding de alta precisión
    JUDGE            = "judge"             # validación de outputs
    VISION           = "vision"            # screenshots, imágenes
```

El registry se actualiza con:
- Modelos que Oli descarga automáticamente (via Ollama) según el tier de GPU del usuario
- Modelos que el usuario agrega manualmente
- Resultados del BenchmarkRunner después de cada instalación

---

## BenchmarkRunner — benchmark continuo

Antes de que un modelo sea `canonical` para un rol, debe pasar un benchmark:

```python
BENCHMARK_SUITE = [
    "startup_load_test",
    "intent_classification",       # clasificar tipo de misión
    "structured_json_output",      # tool use básico
    "tool_call_formatting",        # formato de herramientas
    "memory_extraction",           # extraer memoria de conversación
    "short_coding_task",           # Python 50 líneas
    "repo_reasoning",              # entender un repo dado un README
    "summarization_quality",       # resumir documento largo
    "context_stress_16k",          # contexto largo
    "validation_repair",           # detectar error y proponer fix
    "latency_p50_p95",             # latencia real
]
```

Los resultados populan `benchmark_scores` en el registry. El router los usa para selección dinámica.

Política:
- Un modelo nuevo empieza como `candidate`
- Después de benchmark exitoso → `benchmarked`
- Si falla consistentemente en un rol → `disabled` para ese rol
- Re-benchmark automático cada 30 días o cuando el modelo se actualiza

---

## Las 3 tiers de routing (por rol, no por nombre)

### Tier 1 — Modelo local rápido (objetivo: siempre que posible)

Rol: `FAST_LOCAL`
Tasks: clasificación de intención, extracción de memoria, routing de steps, validación básica, formateo

Criterios de selección del registry:
- `local: true`
- `tool_use_quality >= "medium"`
- `benchmark_scores["intent_classification"] >= 0.85`
- Menor latencia p50 entre candidatos

### Tier 2 — Modelo local principal (cuando Tier 1 no alcanza)

Rol: `MAIN_LOCAL`
Tasks: creación de planes, síntesis, generación de reportes, coding, research

Criterios:
- `local: true`
- `tool_use_quality >= "high"`
- `benchmark_scores["short_coding_task"] >= 0.80`
- VRAM disponible en la GPU del tier del usuario

### Tier 3 — Frontier API (solo cuando lo vale)

Rol: `PREMIUM_REASONING` o `PREMIUM_CODING`
Tasks: arquitectura compleja, decisiones críticas, síntesis de alta complejidad, recovery de fallos de Tier 2

Cuándo usar Tier 3:
- La misión tiene `risk_class >= EXTERNAL_REVERSIBLE_WRITE` y el output tiene consecuencias reales
- El task requiere >32K tokens de contexto y el modelo local no lo soporta bien
- El modelo local falló 2 veces en el mismo step (repair loop)
- El usuario lo solicita explícitamente en la policy de la misión

---

## Privacy mode — el usuario controla el routing

```python
class PrivacyMode(str, Enum):
    LOCAL_ONLY  = "local_only"   # nada va a APIs externas — nunca Tier 3
    HYBRID      = "hybrid"       # local cuando puede, API cuando vale (default)
    CLOUD_OK    = "cloud_ok"     # puede usar APIs libremente
```

En `LOCAL_ONLY`: si el mejor modelo local falla, Oli reporta el límite y pide instrucciones. No hace fallback silencioso a una API externa.

---

## El modelo de negocio — GPU on-demand por detrás

```
USUARIO → paga suscripción mensual a Oli
NOSOTROS → alquilamos GPU on-demand cuando hay trabajo

Flujo:
  1. Usuario crea misión → Oli evalúa si necesita GPU
  2. Si sí → encendemos la GPU asignada al tier del usuario
  3. Misión corre → GPU ejecuta modelos Tier 1 y 2
  4. Misión termina → GPU se apaga o queda en stand-by configurable
  5. Nosotros pagamos GPU on-demand → facturamos al usuario como suscripción fija
```

Por qué on-demand y no dedicada 24/7:
- Usuario intensivo usa GPU activamente ~5-8 horas/mes de 720 disponibles
- On-demand compartido entre usuarios en distintas zonas horarias
- El usuario percibe la GPU como "suya" — el scheduling es invisible

### Tiers de GPU (mapeados a tiers de suscripción)

| Tier | GPU clase | Modelos locales posibles | Créditos incluidos |
|---|---|---|---|
| Starter | RTX 4090 (24GB VRAM) | Modelos hasta ~34B Q4 | 660/mes |
| Pro | A6000 (48GB VRAM) | Modelos hasta ~70B full precision | 660/seat/mes |
| Team | H100 (80GB VRAM) | Cualquier modelo abierto | 660/seat/mes |

Los modelos concretos que caben en cada tier los determina el BenchmarkRunner contra el hardware real, no una lista fija en este documento.

---

## Agent Router — Oli decide quién ejecuta

Oli no es solo otro agente que usa modelos. Es el supervisor que decide qué agente o herramienta ejecuta cada step:

```python
class AgentRouter:
    """
    Oli decide cuándo usar qué herramienta de ejecución.
    Ningún agente externo se invoca sin pasar por aquí.
    """
    def route(self, task: MissionTask) -> ExecutionRoute:
        if task.type == TaskType.CODE_GENERATION:
            if task.requires_full_repo_context:
                return ExecutionRoute.CLAUDE_CODE_DELEGATE
            return ExecutionRoute.LOCAL_SANDBOX

        if task.type == TaskType.CODE_COMPLETION:
            return ExecutionRoute.CODEX_DELEGATE

        if task.type == TaskType.BROWSER_NAVIGATION:
            return ExecutionRoute.BROWSER_AGENT

        if task.type == TaskType.SCRIPT_EXECUTION:
            return ExecutionRoute.EXECUTION_ENVIRONMENT

        return ExecutionRoute.LOCAL_MODEL  # default

class ExecutionRoute(str, Enum):
    LOCAL_MODEL          = "local_model"
    PREMIUM_API          = "premium_api"
    LOCAL_SANDBOX        = "local_sandbox"       # E2B/Docker
    BROWSER_AGENT        = "browser_agent"       # Stagehand/Browser Use
    CLAUDE_CODE_DELEGATE = "claude_code_delegate" # Claude Code como herramienta
    CODEX_DELEGATE       = "codex_delegate"      # Codex como herramienta
    HUMAN_APPROVAL       = "human_approval"      # escalación a humano
```

Claude Code y Codex son **herramientas de Oli**, no competidores. Oli los delega, captura evidencia de su output y lo integra en el resultado de la misión.

---

## Consecuencias

**Para el usuario:**
- Sin factura de APIs para el 70-80% de misiones (Tier 1 y 2 locales)
- APIs solo para lo que realmente necesita frontier quality
- GPU "propia" sin administrar infraestructura

**Para el negocio:**
- Margen real = precio suscripción − costo GPU on-demand − overhead
- El costo GPU on-demand escala con uso real
- Se optimiza scheduling entre usuarios

**Para el producto:**
- El routing mejora con el tiempo — el BenchmarkRunner acumula datos reales de qué modelo funciona mejor para qué tipo de misión en cada tier de hardware
- Si un modelo es reemplazado por uno mejor (en semanas/meses), el registry se actualiza y el routing mejora automáticamente sin cambiar el código del Mission Kernel

**Riesgo:**
- Si un usuario usa GPU mucho más de lo estimado → margen se comprime
- Necesita sistema de créditos extra ($0.08/cr Starter/Pro, $0.07/cr Team)
