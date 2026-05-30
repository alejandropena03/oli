# ADR-004 — Modelo de permisos

**Estado:** proposed
**Fecha:** 2026-05-26
**Deciders:** Alejandro Peña (founder)

---

## Contexto

Oli ejecuta acciones con consecuencias reales. Necesita un modelo de permisos auditable, comprensible para el usuario y que escale con la autonomía de Oli.

---

## Decisión

**5 clases de permiso (0-4), definidas por impacto y reversibilidad:**

| Clase | Nombre | Descripción | Requiere aprobación |
|---|---|---|---|
| 0 | Read/Draft | Sin side effects externos | Nunca |
| 1 | Internal reversible | Acciones locales y reversibles | Configurable por usuario |
| 2 | Resource consuming | Costo real o uso de recursos | Sí, primera vez por tipo |
| 3 | External/brand impact | Comunicación o publicación | Siempre |
| 4 | Destructive/sensitive | Datos, producción, finanzas | Siempre + confirmación explícita |

---

## Consecuencias

- Toda acción en el sistema debe declarar su `permission_class`
- El usuario configura threshold de auto-aprobación (ej: "auto-aprueba hasta clase 1")
- Toda aprobación queda en el audit trail de la misión
- No existe "forzar" clase 4 — siempre requiere confirmación explícita
