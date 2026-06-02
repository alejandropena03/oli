# ADR-025 - State-of-the-Art Discovery and Decision Memos

**Estado:** accepted
**Fecha:** 2026-05-31
**Deciders:** Alejandro Pena (founder)

---

## Contexto

Oli tiene como principio constitucional construir con excelencia. Eso implica que, ante decisiones tecnicas, operativas, de herramientas, modelos, cloud, automatizacion o arquitectura, Oli no puede responder desde memoria vieja ni recomendar lo popular sin verificar.

El riesgo no es solo dar una mala respuesta. El riesgo es que Oli convierta una recomendacion floja en ejecucion real, instalando herramientas mediocres, modelos obsoletos, servicios caros o arquitecturas incorrectas.

El caso de seleccion de modelos locales por GPU/tier demostro que el problema es mas amplio:

- que modelo usar;
- que MCP/tool instalar;
- que API de search conviene;
- que servicio cloud provisionar;
- que stack usar;
- que automatizacion recomendar;
- que decision build-vs-buy tomar.

Todas esas decisiones necesitan un mismo patron: discovery actual, evidencia, scoring, buildability, riesgo y decision memo.

---

## Decision

Oli adopta un **State-of-the-Art Discovery Engine** como capacidad canonica.

La salida canonica no es un "research brief" generico. Es un:

```text
Decision Memo + Evidence Pack + Recommended Action + Recheck Date
```

Workflow canonico:

```text
DecisionClassifier
  -> CriteriaBuilder
  -> SourcePlanner
  -> EvidenceRetriever
  -> SourceRanker
  -> OptionGenerator
  -> OptionScorer
  -> BuildabilityChecker
  -> RiskChecker
  -> DecisionMemoWriter
  -> Validator
  -> Mission Black Box
```

Regla:

```text
Oli recommends excellence, then lands it to constraints.
No recommendation is accepted until it passes buildability and risk checks.
```

---

## Decision Classes

Oli must support at least:

- `model_selection`
- `tool_selection`
- `cloud_service_selection`
- `architecture_pattern`
- `automation_strategy`
- `security_policy`
- `pricing_vendor_decision`
- `ai_first_workflow_recommendation`
- `build_vs_buy`

Each decision class defines criteria, source types, evidence requirements and validation strategy.

---

## Source Quality

Sources are ranked by quality. Oli does not treat all web results equally.

### Tier A - Primary Sources

- official docs;
- API docs;
- model cards;
- technical reports;
- release notes;
- GitHub repo official;
- official pricing;
- security advisories;
- status pages;
- benchmark papers with methodology.

### Tier B - Trusted Aggregators

- LMArena/Arena;
- Artificial Analysis;
- OpenRouter Rankings;
- Hugging Face leaderboards/eval results;
- benchmark aggregators with visible methodology.

### Tier C - Community Signals

- GitHub issues;
- Reddit/practitioner reports;
- Hacker News;
- Discord/community posts;
- independent benchmarks.

Community signals detect real-world problems. They do not canonize a decision alone.

### Tier D - Low-Authority Content

- SEO blogs;
- affiliate comparisons;
- undated posts;
- AI-generated listicles;
- pages with unclear methodology.

These can discover names but cannot justify a recommendation.

---

## Consequences

### Positive

- Oli recommendations become auditable and current.
- Decisions become comparable across time.
- Recheck dates prevent stale "best practice" drift.
- Source quality reduces SEO/AI-generated noise.
- Buildability checks keep excellence grounded in constraints.
- Decision memos become reusable evidence for playbooks, evals and Oli Labs.

### Negative

- More latency and cost than casual answers.
- Requires source connectors and validators.
- Some decisions need browsing/API access.
- Recommendations may still be uncertain if sources conflict.
- Requires discipline to avoid over-researching simple tasks.

---

## Acceptance Criteria

This ADR is applied when:

1. `tdd/domain/state-of-art-discovery.md` exists.
2. `tdd/schemas/decision_memo.ts` exists.
3. `tdd/domain/state-of-art-evals.md` exists.
4. Every state-of-the-art recommendation has a decision class.
5. Every decision memo records criteria, evidence, source quality, alternatives, risks, buildability and recheck date.
6. Strong recommendations require at least two Tier A/B sources or one Tier A source plus an Oli benchmark/eval.
7. No recommendation can be marked accepted without buildability and risk checks.
8. Mission Black Box can record source refs, option scores and final decision.

---

## Relationship To Other ADRs

- ADR-016 Model Routing depends on this for current model/runtime selection.
- Future ADR-024 Model Intelligence is a specialized module inside this capability.
- ADR-023 Subagent Engineering defines how discovery tasks can be delegated.
- ADR-021 Dedicated Oli Runtime provides runtime constraints for buildability.
- ADR-022 Public Oli Labs can expose sanitized versions of decision memo labs.

---

## References

- `Consultor Estrategico Codex/18_state_of_art_discovery_recommendations_2026-05-31.md`
- `tdd/domain/state-of-art-discovery.md`
- `tdd/domain/state-of-art-evals.md`
- `tdd/schemas/decision_memo.ts`

