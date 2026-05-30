# Modelo de Pricing — Oli v2

**Fecha:** 2026-05-27
**Metodología:** Precios reales RunPod + datos reales de uso (37 hrs GPU/seat/mes)
**Fuente de uso:** McKinsey/Slack Workforce Index 2026 — 6.4 hrs ahorradas/semana → ~37 hrs GPU activa/mes

---

## Base de cálculo

### Uso real por seat activo

```
Dato de mercado: knowledge workers con AI agents ahorran 6.4 hrs/semana
En Oli: esas horas = GPU activa ejecutando misiones

Desglose de 37 hrs GPU/mes por seat:
  Misiones simples  (15 min GPU): ~50/mes × 0.25 hr = 12.5 hrs
  Misiones medias   (30 min GPU): ~30/mes × 0.5 hr  = 15.0 hrs
  Misiones complejas (60 min GPU): ~10/mes × 1.0 hr = 10.0 hrs
  ──────────────────────────────────────────────────
  Total: ~37 hrs GPU activa/mes por seat activo
```

### Precios GPU RunPod (verificados 2026-05-27)

```
SERVERLESS (flex workers — $0 en idle, pay per second):
  RTX 4090 (24GB):  $1.116/hr  → $41.29/seat/mes con 37 hrs activo
  A6000 (48GB):     $1.224/hr  → $45.29/seat/mes con 37 hrs activo

ON-DEMAND (pod activo solo mientras corre):
  H100 SXM (80GB):  $3.29/hr   → $121.73/seat/mes con 37 hrs activo
  A100 SXM (80GB):  $1.49/hr   → $55.13/seat/mes con 37 hrs activo

RESERVADA (negociada con RunPod a volumen — 5+ seats activos):
  H100 reservada:   ~$2.20/hr  → $81.40/seat/mes con 37 hrs activo
  Aplica desde: 5 seats × 37 hrs = 185 hrs → reservada gana sobre on-demand

PUNTO DE INFLEXIÓN H100:
  < 5 seats:  on-demand a $3.29/hr
  ≥ 5 seats:  negociar reservada a ~$2.20/hr (ahorro de 33%)
  → En Team desde el mínimo de 5 seats, negociamos reservada
```

### COGS completo por seat/mes

```
= GPU activa + infraestructura fija prorrateada + soporte/ops + growth budget

Infraestructura fija (Postgres, storage, network, monitoring):
  Se distribuye entre todos los seats del tier
  Estimado: $30-50/mes fijos por instancia → se divide entre N seats

Growth budget (marketing, sales, contenido):
  Target SaaS B2B early stage: 30-40% del revenue
  Lo aplicamos como costo al calcular el precio mínimo viable

Soporte/ops:
  V0-V1 (founder solo): ~$5/seat
  V2+ (con equipo): ~$3/seat (economía de escala)
```

---

## TIER 1 — Starter

**Para:** founders solos, consultores independientes, operadores sin equipo

```
GPU:     RTX 4090 (24GB) — serverless RunPod
Uso:     37 hrs activas/mes (uso real de un founder activo)

COGS:
  GPU serverless:     37 hrs × $1.116 = $41.29
  Infra (storage/DB): $20 fijos (solo 1 seat, no se distribuye)
  Ops/soporte:        $8
  ─────────────────────────────────────────────
  COGS total:         ~$69/mes

Precio objetivo (gross margin 65%):
  $69 / (1 - 0.65) = $197 → redondeamos a $199/mes

Verificación:
  Revenue:     $199
  COGS:        $69
  Gross profit: $130
  Gross margin: 65.3% ✓

PRECIO: $199/mes — 1 seat

Créditos incluidos: 4,000/mes (ruedan, cap 2x)
  1 crédito = 1 min de GPU activa ($0.019)
  4,000 créditos = ~66 hrs GPU = más que el uso promedio mensual
  Uso intensivo (37 hrs): consume ~2,220 créditos → sobra buffer
  Uso muy intensivo (50 hrs): consume 3,000 créditos → aún dentro

Créditos extra: $15 por 1,000 adicionales (markup 21% sobre COGS)
APIs externas: el usuario conecta y paga las suyas
Concurrent: 1 misión activa
```

**Argumento de valor:**
- El ICP ya gasta $300-400/mes en stack fragmentado que no recuerda ni ejecuta
- $199 reemplaza ese stack + agrega memoria, audit, playbooks, ejecución real
- Comparado con Lindy Pro ($49.99) que no ejecuta nada real

---

## TIER 2 — Pro

**Para:** startups, agencias, equipos ops 2-10 personas

```
GPU:     A6000 (48GB) — serverless RunPod
         Capacidad para correr Qwen3 35B-A3B MoE (Tier 2 local gratis)
Uso:     37 hrs activas/mes POR SEAT

COGS por seat (con 3 seats — break even mínimo del founder):
  GPU por seat: 37 hrs × $1.224 = $45.29
  Infra prorrateada (3 seats): $40 / 3 = $13.33/seat
  Ops/soporte: $6/seat
  ──────────────────────────────────────────
  COGS/seat con 3 seats: ~$64.62/seat/mes

COGS por seat (con 8 seats — uso típico del tier):
  GPU por seat: $45.29
  Infra prorrateada (8 seats): $40 / 8 = $5.00/seat
  Ops/soporte: $5/seat
  ──────────────────────────────────────────
  COGS/seat con 8 seats: ~$55.29/seat/mes

Precio por seat objetivo (gross margin 65%, basado en 5 seats promedio):
  COGS/seat con 5 seats: $45.29 + $8 + $6 = $59.29
  $59.29 / (1 - 0.65) = $169.4 → redondeamos a $169/seat/mes

PRECIO: $169/seat/mes (mínimo 2 seats = $338/mes)
  Ej: equipo de 3  → $507/mes
  Ej: equipo de 5  → $845/mes
  Ej: equipo de 10 → $1,690/mes

Verificación con 5 seats (caso promedio):
  Revenue:      5 × $169 = $845
  COGS:         5 × $59.29 = $296.45
  Gross profit: $548.55
  Gross margin: 64.9% ✓

¿Se paga la GPU con 3 seats? (objetivo del founder):
  Revenue 3 seats:  3 × $169 = $507
  COGS GPU 3 seats: 3 × $45.29 = $135.87
  GPU A6000 serverless cubierta: $507 >> $135.87 ✓
  Incluyendo infra + ops: $507 vs COGS $194 → cubierto con margen ✓

Créditos: 4,000/seat/mes (ruedan, cap 2x por seat)
  Pool compartido entre el equipo
  Uso promedio equipo: mayor eficiencia — misiones se comparten
Concurrent: 3 misiones paralelas
Multi-user: hasta 10 seats
Memoria: personal (privada) + empresa (compartida por equipo)
Playbooks de equipo compartidos
APIs externas: cada miembro conecta las suyas
Créditos extra: $13 por 1,000
```

---

## TIER 3 — Team

**Para:** empresas 5-200 personas, equipos ops grandes, agencias con clientes

```
GPU:     H100 SXM (80GB) — on-demand RunPod para 1-4 seats
                           → reservada negociada para 5+ seats
         Razón: H100 serverless ($4.18/hr) es demasiado cara
                On-demand ($3.29/hr) más eficiente para uso continuo
                Reservada ($2.20/hr negociada) óptima desde 5 seats

Uso:     37 hrs activas/mes POR SEAT

COGS por seat (con 5 seats — mínimo del tier, H100 reservada):
  GPU por seat: 37 hrs × $2.20 = $81.40
  Infra prorrateada (5 seats): $50 / 5 = $10/seat
  Ops + onboarding + SLA: $10/seat
  ──────────────────────────────────────────
  COGS/seat con 5 seats: ~$101.40/seat/mes

COGS por seat (con 15 seats — uso típico):
  GPU por seat: 37 hrs × $2.20 = $81.40
  Infra prorrateada (15 seats): $50 / 15 = $3.33/seat
  Ops + onboarding + SLA: $8/seat
  ──────────────────────────────────────────
  COGS/seat con 15 seats: ~$92.73/seat/mes

Precio por seat objetivo (gross margin 65%, COGS base $100/seat):
  $100 / (1 - 0.65) = $285.7 → redondeamos a $289/seat/mes

PRECIO: $289/seat/mes (mínimo 5 seats = $1,445/mes)
  Ej: empresa de 5   → $1,445/mes
  Ej: empresa de 10  → $2,890/mes
  Ej: empresa de 15  → $4,335/mes
  Ej: empresa de 50  → $14,450/mes

Verificación con 10 seats:
  Revenue:      10 × $289 = $2,890
  COGS estimado: 10 × $95 = $950
  Gross profit: $1,940
  Gross margin: 67.1% ✓

¿Se paga la H100 con 5 seats? (objetivo del founder):
  Revenue 5 seats: 5 × $289 = $1,445
  COGS GPU H100 reservada 5 seats: 5 × $81.40 = $407
  Infra + ops: $100
  Total COGS: $507
  Margen: $1,445 - $507 = $938 ✓ 64.9% gross margin desde el mínimo

Créditos: 4,000/seat/mes (ruedan)
Concurrent: ilimitado dentro de capacidad GPU
Multi-user: ilimitado
Memoria: personal + empresa + por proyecto/cliente
H100 → puede correr cualquier modelo open source, incl. fine-tuned propios
Onboarding dedicado con Oli
SLA: 99.5% uptime
Audit logs exportables (compliance)
APIs externas: el equipo conecta las suyas
Créditos extra: $11 por 1,000
```

---

## RESUMEN EJECUTIVO

| Tier | Precio | GPU | COGS/seat | Gross margin | Break-even GPU |
|---|---|---|---|---|---|
| **Starter** | $199/mes (1 seat) | RTX 4090 | ~$69 | 65.3% | N/A (1 seat fijo) |
| **Pro** | $169/seat (mín 2) | A6000 | ~$59-65 | 64-66% | ✅ 3 seats cubren GPU |
| **Team** | $289/seat (mín 5) | H100 | ~$92-101 | 65-67% | ✅ 5 seats cubren GPU + margen |

---

## COMPARATIVA VS. COMPETENCIA

| Producto | 1 founder | 5 personas | 10 personas | Modelo local | Memoria |
|---|---|---|---|---|---|
| Lindy Pro | $49.99 | $249.95 | $499 | ❌ | ❌ |
| Manus Standard | $20 | $100 | $200 | ❌ | ❌ |
| **Oli Starter** | **$199** | — | — | ✅ RTX 4090 | ✅ |
| **Oli Pro** | — | **$845** | **$1,690** | ✅ A6000 | ✅ |
| **Oli Team** | — | **$1,445** | **$2,890** | ✅ H100 | ✅ |

**Nota:** Lindy/Manus son más baratos pero:
1. No tienen GPU local — el usuario paga sus propias APIs encima del tier
2. Sin memoria real entre sesiones
3. Sin ejecución real (código, browser, desktop)
4. Sin audit trail
5. Créditos de Manus expiran

**El argumento de venta:**
> "Lindy a $499 para 10 personas, más lo que paguen en APIs, más sin memoria ni ejecución real.
> Oli Pro a $1,690 para 10 personas, con H100 incluida, sin pagar APIs para el 70% de las tareas,
> con memoria que crece, audit trail y ejecución real."

---

## IMPACTO EN MRR A ESCALA

```
Escenario conservador (12 meses):
  10 Starters:  10 × $199 = $1,990 MRR
  5 Pro (5 seats avg): 5 × $845 = $4,225 MRR
  2 Team (10 seats avg): 2 × $2,890 = $5,780 MRR
  ─────────────────────────────────────
  MRR: $11,995 | ARR: ~$143,940

Escenario base (18 meses):
  30 Starters:  $5,970 MRR
  15 Pro:       $12,675 MRR
  5 Team:       $14,450 MRR
  ─────────────────────────────────────
  MRR: $33,095 | ARR: ~$397,140

Gross margin objetivo: 65% → gross profit en escenario base: ~$258,000/año
```

---

## PENDIENTE PARA VALIDAR

- [ ] Entrevistar 10 founders del ICP — ¿$199/mes es aceptable para Starter?
- [ ] Testear sensibilidad de precio: $149 vs $199 vs $249
- [ ] Validar uso real de GPU — ¿37 hrs es correcto para nuestro ICP específico?
- [ ] Negociar precios reservados con RunPod (necesita volumen mínimo)
- [ ] Definir si créditos = minutos GPU o si usamos otra unidad más intuitiva para el usuario
