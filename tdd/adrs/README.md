# ADRs — Architecture Decision Records

Un ADR documenta una decisión arquitectural importante: su contexto, la decisión tomada, las alternativas consideradas y las consecuencias.

## Por qué ADRs

- En 6 meses sabrás por qué algo está como está
- Nuevos colaboradores entienden el sistema sin preguntar
- Evita deshacer decisiones por no recordar el razonamiento original

## Formato de un ADR

```markdown
# ADR-NNN — Título

**Estado:** proposed | accepted | deprecated | superseded por ADR-XXX
**Fecha:** YYYY-MM-DD
**Deciders:** [nombres o roles]

## Contexto
Qué situación o problema motiva esta decisión.

## Decisión
Qué se decidió.

## Alternativas consideradas
| Opción | Pros | Contras |
|---|---|---|

## Consecuencias
Qué implica esta decisión a futuro.

## Referencias
Links relevantes.
```

## ADRs existentes

- [ADR-001](ADR-001-model-strategy.md) — Estrategia de modelo (model-agnostic, Claude default) — proposed
- [ADR-002](ADR-002-execution-sandbox.md) — Sandbox de ejecución (mock → subprocess → Linux) — proposed
- [ADR-003](ADR-003-memory-storage.md) — Storage de memoria (JSON V0, hybrid V3+) — proposed
- [ADR-004](ADR-004-permission-model.md) — Modelo de permisos (5 clases 0-4) — proposed
- [ADR-005](ADR-005-runtime.md) — Runtime principal (TypeScript + Bun/Node) — proposed
- [ADR-021](ADR-021-dedicated-oli-runtime.md) - Dedicated Oli Runtime and User-Owned Execution Environment - accepted
- [ADR-022](ADR-022-public-oli-labs.md) - Public Oli Labs and Private Core Boundary - accepted
- [ADR-023](ADR-023-subagent-engineering-contracts.md) - Subagent Engineering Contracts - accepted
- [ADR-025](ADR-025-state-of-art-discovery-and-decision-memos.md) - State-of-the-Art Discovery and Decision Memos - accepted

## ADRs pendientes

- [ ] ADR-006 — Arquitectura de comunicación entre módulos (event bus vs. direct calls)
- [ ] ADR-007 — Estrategia de testing (unit vs. integration vs. eval-based)
