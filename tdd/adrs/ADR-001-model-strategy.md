# ADR-001 — Estrategia de modelo de IA

**Estado:** proposed
**Fecha:** 2026-05-26
**Deciders:** Alejandro Peña (founder)

---

## Contexto

Oli necesita un modelo de IA para interpretar intención, generar planes, sintetizar outputs de suboperadores y generar reportes. La decisión es si atar Oli a un proveedor específico o construir model-agnostic desde el inicio.

---

## Decisión

**Oli es model-agnostic con Claude Sonnet como modelo default en V0.**

El usuario puede configurar qué modelo usa Oli por tipo de tarea. La capa de Model Router abstrae la implementación de cada proveedor.

---

## Alternativas consideradas

| Opción | Pros | Contras |
|---|---|---|
| Claude-only | Simplicidad, máximo aprovechamiento de tool use | Dependencia de Anthropic, riesgo de pricing |
| OpenAI-first | Ecosistema grande, fine-tuning | Misma dependencia, peor tool use |
| OSS-only (Ollama) | Privacy máxima, costo cero | Capacidad menor en V0, setup complejo |
| **Model-agnostic ✓** | Independencia, flexibilidad por tarea | Más complejidad en Model Router |

---

## Consecuencias

**Positivo:** Oli no muere si Anthropic sube precios. El usuario puede elegir modelo por misión. Posibilidad futura de OSS para privacidad.

**Negativo:** Model Router requiere abstracción. Testing debe cubrir múltiples providers. Prompt engineering varía por modelo.

---

## Implementación en V0

```typescript
interface ModelConfig {
  provider: 'anthropic' | 'openai' | 'ollama' | 'gemini'
  model: string
  temperature: number
  maxTokens: number
}

// Default V0 routing
const defaultRouting: Record<TaskType, ModelConfig> = {
  intent_interpretation: { provider: 'anthropic', model: 'claude-sonnet-4-6', temperature: 0.3, maxTokens: 2048 },
  planning:              { provider: 'anthropic', model: 'claude-sonnet-4-6', temperature: 0.2, maxTokens: 4096 },
  execution:             { provider: 'anthropic', model: 'claude-haiku-4-5', temperature: 0.1, maxTokens: 1024 },
  validation:            { provider: 'anthropic', model: 'claude-sonnet-4-6', temperature: 0.1, maxTokens: 2048 },
}
```
