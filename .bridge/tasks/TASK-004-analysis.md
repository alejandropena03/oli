# TASK-004 — Análisis comparativo

## Output hardcodeado de Claude vs Output real de Oli

Fecha: 2026-06-02
Analista: DeepSeek (local agent)

---

## Tabla comparativa

| Dimensión | Output de Claude (hardcoded) | Output de Oli via API (real) |
|---|---|---|
| **Quién lo generó** | Claude escribiendo Python inline | Oli (Mission Kernel + Orchestrator) vía HTTP |
| **Datos** | Inventados (Carlos, Maria, investor@vc.com) | Mock (Lindy, Dust, Claude Projects) — ver nota 1 |
| **Pasos** | 9 pasos hardcodeados en Python | 7 pasos generados por el orchestrator |
| **Permisos** | Estáticos: permisos por paso | Clasificados: permission_class=0 completo |
| **Estados** | No aplica — era código lineal | **11 estados reales** con transiciones auditables |
| **Evidencia** | Simulada (8 registros inline) | **6 registros reales** guardados en Postgres via SQLAlchemy |
| **Validación** | 5/5 contra datos que él mismo fabricó | 4/4 criteria con evidence textual |
| **Checkpointing** | No aplica | ✅ PostgresSaver — misión sobrevive reinicio |
| **Costo** | No calculado | $0.12 estimado + 2hr human-time-saved |
| **Playbook candidate** | No | ✅ Sí — estructura repetible detectada |
| **Utilidad real** | Ninguna — teatro | **Demostración del pipeline real** |

---

## ¿Qué significa esto para Oli?

### Lo que funciona (real)

1. **El Mission Kernel es real.** La petición HTTP → misión con estados → eventos → evidencia → reporte es pipeline funcional, no simulación.
2. **Postgres persiste todo.** La misión, eventos, evidencia — todo está en Postgres, no en memoria volátil.
3. **El flujo de estados es correcto.** 11 estados desde intake hasta completed, cada uno con trigger y timestamp.
4. **La validación es real.** Criterios de éxito evaluados contra el output.
5. **Checkpointing con PostgresSaver funciona.** 55 tests lo confirman.

### Lo que es mock (V0)

1. **El adaptador de modelo es `development`.** Los datos de competidores son inline, no de un modelo real. La research no es real — es `mock_web_research`.
2. **La intención está hardcodeada.** Toda petición a `research-brief` se interpreta como `competitor_research_brief`, ignorando el input real del usuario.
3. **El output es genérico.** "Oli compite contra Lindy, Dust, Claude Projects" — siempre el mismo, independientemente del input.

### El salto cualitativo

| Output Claude | Output Oli |
|---|---|
| Script que corre y muere | Pipeline que persiste, audita y aprende |
| Datos inline | Datos estructurados en DB |
| Sin trazabilidad | 11 eventos + 6 evidence records |
| Sin validación real | 4 criteria evaluados con evidence |
| Sin costo | Cost tracking + playbook candidato |

---

## Veredicto

**Output hardcodeado de Claude:** 2/10 — teatro. Demuestra que Claude sabe escribir Python, no que Oli funcione.

**Output real de Oli:** 7/10 — pipeline real con contenido mock. Demuestra que el Mission Kernel, Orchestrator, Postgres persistencia, eventos, validación y checkpoints funcionan. Lo que falta es conectar un modelo real al adaptador para que el contenido no sea mock.

**La razón:** Claude escribió una simulación. Oli ejecuta un pipeline real. La diferencia no es el output textual — es que Oli deja un rastro auditable en Postgres de cada paso, cada decisión y cada validación. Eso no se puede hardcodear.

**Riesgo:** Que el contenido mock se confunda con producto terminado. No lo está.

**Recomendación:** El siguiente paso es conectar un modelo real (OpenRouter) al adaptador para que el contenido `development` sea reemplazado por inferencia real. Eso transforma el 7/10 en 9/10.

**Siguiente decisión:** ¿Configuramos OpenRouter con `openrouter/quasar-alpha` en `.env.local` y repetimos esta misma petición para ver la diferencia?
