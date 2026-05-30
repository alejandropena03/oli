# Modelo de Pricing — Oli v3

**Fecha:** 2026-05-27
**Modelo:** Híbrido — base fija + créditos de uso (estándar 2026, 43% de AI SaaS)
**Benchmark:** Cursor ($20-200/mes individual, $40/seat team)
**Insight clave:** base baja convierte, uso variable paga el COGS real de GPU

---

## Por qué modelo híbrido (base + uso)

Research 2026 es claro:
- Hybrid pricing: **43% de AI SaaS, creciendo a 61% en 2026**
- Hybrid vs. pure subscription: **38% más revenue growth, 38% más NRR**
- Pure per-seat cayó de 21% a 15% entre 2025-2026
- La clave: **base predecible para el buyer + variable que refleja el valor real entregado**

Para Oli específicamente:
- El COGS de GPU es **variable** — depende del uso real
- Un founder que hace 20 misiones/mes usa 2x menos GPU que uno que hace 100
- Cobrarles igual es injusto para el ligero y pérdida para nosotros con el intensivo
- **Solución: base fija accesible + créditos de GPU que reflejan el uso real**

---

## La unidad de valor

**1 crédito = 1 minuto de GPU activa**

Intuitivo para el usuario:
- "Misión simple tardó 3 min → usé 3 créditos"
- "Misión compleja tardó 45 min → usé 45 créditos"

Costo real para nosotros (RunPod serverless, verificado 2026-05-27):
- RTX 4090: $1.116/hr = **$0.0186/min** (Starter)
- A6000:    $1.224/hr = **$0.0204/min** (Pro)
- H100 reservada: $2.20/hr = **$0.0367/min** (Team)

Markup sobre GPU para cubrir infra + ops + margen:
- Cobramos $0.05/crédito al usuario
- Margen sobre GPU varía por tier (ver abajo)
- Los créditos incluidos en el plan absorben el uso normal
- El uso extra se cobra a $0.05/crédito adicional

---

## Los 3 tiers

### Starter — $29/mes

```
Para: founders solos, uso moderado (primeras semanas/meses con Oli)
GPU:  RTX 4090 (24GB) serverless — corre Qwen3 27B Q4

Créditos incluidos: 300/mes
  = 300 minutos de GPU activa
  = ~5 horas de GPU activa
  = ~50-80 misiones simples, o ~20-30 misiones medias
  Realidad: un founder que está arrancando con Oli

Créditos extra: $0.05/crédito (=  $0.05/min GPU)

COGS cuando usa los 300 créditos incluidos:
  GPU: 5 hrs × $1.116 = $5.58
  Infra: $8
  Ops: $5
  Total COGS: ~$18.58

Revenue: $29
Gross margin con uso promedio: ~36% — bajo, pero el objetivo es conversión
¿Por qué 36% es aceptable en Starter?
  → Starter es la puerta de entrada, no el producto
  → Se asume churn bajo si el producto cumple → upsell a Pro
  → Si el usuario usa menos de 300 créditos, el margen sube
  → Los créditos extra son puro margen adicional

¿Cuándo es rentable Starter?
  Usuario usa 150 créditos (uso ligero):
    GPU: 2.5 hrs × $1.116 = $2.79
    COGS total: ~$15.79
    Revenue: $29
    Margin: 45.5% ✓

Seats: 1
Concurrent: 1 misión activa
APIs externas: el usuario conecta y paga las suyas
```

---

### Pro — $79/mes (por seat)

```
Para: founders activos, operadores intensivos, equipos pequeños
GPU:  A6000 (48GB) serverless — corre Qwen3 35B-A3B MoE (Tier 2 local)

Créditos incluidos: 1,200/mes por seat
  = 1,200 minutos = 20 horas de GPU activa
  = ~200 misiones simples o ~80 medias o ~30 complejas/mes
  Realidad: cubre el uso promedio de 37 hrs/mes del ICP activo
  (37 hrs × 60 min × uso no continuo de GPU: ~50% del tiempo = 20 hrs efectivas)

Créditos extra: $0.05/crédito adicional

COGS por seat con uso pleno (1,200 créditos):
  GPU: 20 hrs × $1.224 = $24.48
  Infra prorrateada: $8/seat (equipo de 3+)
  Ops: $6/seat
  Total COGS: ~$38.48/seat

Revenue/seat: $79
Gross margin: 51.3%

Con uso ligero (500 créditos):
  GPU: 8.3 hrs × $1.224 = $10.16
  COGS: ~$24.16
  Margin: 69.4%

Con créditos extra (uso intensivo, 2,000 créditos total):
  800 créditos extra × $0.05 = $40 adicional
  Revenue: $79 + $40 = $119
  GPU extra: 800 min = 13.3 hrs × $1.224 = $16.32
  COGS extra: ~$16.32
  Margin con uso intensivo: ($119 - $55) / $119 = 53.8%

Seats: ilimitado (paga por cada seat que agrega)
Concurrent: 2 misiones/seat activo
Multi-user: sí — cada persona tiene su seat
Memoria: personal (privada) + empresa (compartida con el equipo)
Playbooks compartidos entre el equipo
```

---

### Team — $59/seat/mes (mínimo 5 seats)

```
Para: empresas, equipos grandes, agencias
GPU:  H100 SXM (80GB) reservada — negociada con RunPod a $2.20/hr
      La H100 compartida soporta múltiples seats corriendo en paralelo

Créditos incluidos: 1,500/mes por seat
  = 25 horas de GPU activa por seat
  Más créditos por dólar que Pro — economía de escala de la H100

  ¿Por qué más créditos por menos dinero?
  H100 reservada es más eficiente: los modelos corren más rápido
  Una misión que tarda 30 min en A6000 tarda 18-20 min en H100
  → Mismo trabajo, menos minutos consumidos → más créditos te "sobran"

Créditos extra: $0.04/crédito (descuento vs. Pro por volumen)

COGS por seat con uso pleno (1,500 créditos):
  GPU: 25 hrs × $2.20 = $55 (H100 reservada compartida)
  Pero la H100 es compartida entre N seats simultáneos
  Con 10 seats usando en promedio 25% concurrencia:
  GPU real/seat: 25 hrs × $2.20 × 0.25 utilización real = $13.75
  Infra prorrateada: $3/seat (economía de escala)
  Ops + SLA + onboarding: $8/seat
  Total COGS: ~$24.75/seat

Revenue/seat: $59
Gross margin: 58% — y sube con más seats

Escala del margen:
  5 seats:  Revenue $295, COGS ~$147 → 50% margin
  15 seats: Revenue $885, COGS ~$371 → 58% margin
  50 seats: Revenue $2,950, COGS ~$1,237 → 58% margin

¿Por qué Team cobra MENOS por seat que Pro?
  1. Volumen → economía de escala en H100
  2. Contratos anuales → churn bajo → LTV muy alto
  3. La H100 compartida baja el COGS por seat
  4. Estrategia: las empresas grandes tienen más seats = más revenue total

  Team 10 seats: $590/mes
  Pro   10 seats: $790/mes
  → Team más barato por seat PERO más rentable en total por economía de escala

Concurrent: ilimitado dentro de capacidad H100
Multi-user: ilimitado
Memoria: personal + empresa + por proyecto/cliente
SLA: 99.5% uptime
Audit logs exportables
Onboarding dedicado
APIs externas: el equipo conecta las suyas
Créditos extra: $0.04/crédito
Contratos: mínimo 3 meses, descuento 15% anual
```

---

## TABLA RESUMEN

| | Starter | Pro | Team |
|---|---|---|---|
| **Precio base** | **$29/mes** | **$79/seat/mes** | **$59/seat/mes** |
| GPU | RTX 4090 | A6000 | H100 (compartida) |
| Créditos incluidos | 300/mes | 1,200/seat | 1,500/seat |
| GPU activa incluida | ~5 hrs | ~20 hrs | ~25 hrs |
| Créditos extra | $0.05/cr | $0.05/cr | $0.04/cr |
| Mínimo seats | 1 | 1 | 5 |
| Gross margin (uso promedio) | ~36-45% | ~51-69% | ~50-58% |
| Concurrent misiones | 1 | 2/seat | Ilimitado |
| Memoria empresa compartida | ❌ | ✅ | ✅ |
| Audit logs exportables | ❌ | ❌ | ✅ |
| SLA garantizado | ❌ | ❌ | ✅ (99.5%) |

---

## LA ESCALERA DE VALOR

```
$29    → entra, prueba, ve que Oli funciona
         [si le gusta y quiere más créditos → sube a Pro o compra extras]

$79    → usa Oli activamente, modelos más potentes, equipo pequeño
         [si crece el equipo → Team]

$59/seat → empresa, volumen, H100, contratos, compliance
         [precio por seat baja, revenue total sube, LTV alto]
```

**El usuario nunca siente el precio como barrera de entrada.**
**El negocio gana más cuando el usuario usa más — los incentivos están alineados.**

---

## COMPARATIVA FINAL VS. COMPETENCIA

| | Starter Oli | Pro Oli (1) | Lindy Pro | Manus Standard | Cursor Pro |
|---|---|---|---|---|---|
| Precio | $29/mes | $79/mes | $49.99/mes | $20/mes | $20/mes |
| GPU local | ✅ RTX 4090 | ✅ A6000 | ❌ | ❌ | ❌ |
| Memoria persistente | ✅ | ✅ | ❌ | ❌ | ❌ |
| Ejecución real | ✅ | ✅ | ❌ | Parcial | Parcial |
| Audit trail | ❌ | ❌ | ❌ | ❌ | ❌ |
| Créditos ruedan | ✅ | ✅ | ❌ | ❌ | N/A |
| APIs incluidas | No (usuario paga) | No | Sí (con límite) | Sí (expiran) | Sí (con límite) |

**Starter a $29 es más barato que Lindy Pro ($49.99) y tiene GPU local real.**
**Pro a $79 compite con Lindy Max ($199) siendo más capaz.**

---

## NOTAS DE IMPLEMENTACIÓN

### Los créditos no son el número que ve el usuario

El usuario ve: **"Misión completada. Usaste 23 min de GPU."**
No ve créditos directamente — ve tiempo, que es intuitivo.

Internamente: 23 créditos consumidos del pool.

### El modelo de créditos que ruedan

```
Si Starter usa 150 créditos en enero:
  → 150 créditos restantes se acumulan
  → Febrero: 300 + 150 = 450 créditos disponibles
  → Cap: 2x el plan mensual (600 para Starter)
  → No expiran sin cap — eso es justo y diferencia de Manus
```

### Cómo sube el margen con el tiempo

```
Mes 1-3 (usuario aprendiendo):      uso ligero → margin ~45-55%
Mes 4-6 (usuario adoptando):        uso medio  → margin ~50-60%
Mes 7+ (usuario intensivo + extras): uso alto   → margin ~55-65%

Los créditos extra son el mejor driver de margen:
  $0.05/crédito cobrado al usuario
  $0.019/minuto (RTX 4090) costo real para nosotros
  → Markup de 163% sobre el COGS de GPU en extras
```
