# Modelo de Pricing — Oli v5 (definitivo)

**Fecha:** 2026-05-27
**Modelo:** Híbrido — suscripción cubre uso normal, intensivo paga créditos extra
**Dato clave:** 31.9% de usuarios AI usan 1+ hr/día (intensivos) — esos generan el margen real

---

## La distribución real de uso (datos 2026)

```
De usuarios que usan AI en el trabajo:
  ~32% → INTENSIVOS:  1+ hora/día de AI activa
  ~47% → NORMALES:    15-59 min/día
  ~21% → LIGEROS:     <15 min/día

Traducido a GPU activa por mes (22 días laborales):
  Intensivo:  60 min × 22 días = 1,320 min = 22 hrs GPU/mes
  Normal:     30 min × 22 días = 660 min  = 11 hrs GPU/mes
  Ligero:     10 min × 22 días = 220 min  = 3.7 hrs GPU/mes
```

**La suscripción cubre al usuario NORMAL (11 hrs GPU/mes).**
**El usuario INTENSIVO paga créditos extra — ese 32% genera el margen que el negocio necesita.**

---

## COGS con uso normal incluido (11 hrs GPU/mes)

```
Starter (RTX 4090, $1.116/hr serverless):
  GPU: 11 hrs × $1.116 = $12.28
  Infra + ops: $15
  COGS total: ~$27.28/seat/mes

Pro (A6000, $1.224/hr serverless):
  GPU: 11 hrs × $1.224 = $13.46
  Infra + ops: $12
  COGS total: ~$25.46/seat/mes

Team (H100 reservada, $2.20/hr):
  GPU: 11 hrs × $2.20 = $24.20
  Infra + ops: $10
  COGS total: ~$34.20/seat/mes
```

---

## Los 3 tiers — v5

### Starter — $79/mes

```
Para: founders solos, primeros pasos con Oli
GPU:  RTX 4090 (24GB) serverless
Créditos incluidos: 660/mes = 11 hrs GPU activa = uso NORMAL
  ~66 misiones simples, o ~33 medias, o ~13 complejas

Créditos extra: $0.08/crédito
  RTX 4090 costo real: $0.0186/min → markup 4.3x
  El usuario INTENSIVO (22 hrs) paga: 660 extra × $0.08 = $52.80 extra
  → Revenue total usuario intensivo: $79 + $52.80 = $131.80

COGS con uso normal ($27.28):
  Revenue $79 / COGS $27 = gross margin 65.8%

COGS con usuario intensivo:
  GPU extra: 11 hrs × $1.116 = $12.28 extra COGS
  Revenue $131.80 / COGS $39.56 = gross margin 70% ✓

Seats: 1
Concurrent: 1 misión activa
Memoria: personal
APIs externas: el usuario paga las suyas
```

---

### Pro — $99/seat/mes

```
Para: founders activos, equipos 1-15 personas
GPU:  A6000 (48GB) serverless — Qwen3 35B-A3B MoE local
Créditos incluidos: 660/seat/mes = 11 hrs GPU activa = uso NORMAL
  Pool compartido del equipo

Créditos extra: $0.08/crédito
  Usuario intensivo paga: 660 extra × $0.08 = $52.80 extra/seat
  → Revenue total por seat intensivo: $99 + $52.80 = $151.80

COGS con uso normal ($25.46/seat):
  Revenue $99 / COGS $25.46 = gross margin 74.3%

COGS usuario intensivo:
  GPU extra: 11 hrs × $1.224 = $13.46 extra COGS
  Revenue $151.80 / COGS $38.92 = gross margin 74.4% ✓

Concurrent: 2 misiones/seat
Multi-user: ilimitado
Memoria: personal (privada) + empresa (compartida)
Playbooks de equipo
APIs externas: el equipo paga las suyas

Ejemplos de revenue mensual:
  1 seat:  $99/mes
  3 seats: $297/mes
  5 seats: $495/mes
  10 seats: $990/mes
  15 seats: $1,485/mes
```

---

### Team — $149/seat/mes (mínimo 5 seats)

```
Para: empresas, compliance, SLA garantizado
GPU:  H100 SXM (80GB) reservada — más rápida, más concurrencia
Créditos incluidos: 660/seat/mes = 11 hrs = uso NORMAL
  Pero la H100 es más rápida: una misión de 30 min en A6000
  tarda ~18 min en H100 → efectivamente cubre más trabajo

Créditos extra: $0.07/crédito (descuento por volumen)
  Usuario intensivo: 660 extra × $0.07 = $46.20 extra/seat
  → Revenue total intensivo: $149 + $46.20 = $195.20

COGS con uso normal ($34.20/seat):
  Revenue $149 / COGS $34.20 = gross margin 77% ✓

COGS usuario intensivo:
  GPU extra: 11 hrs × $2.20 = $24.20 extra COGS
  Revenue $195.20 / COGS $58.40 = gross margin 70.1% ✓

Concurrent: ilimitado
Multi-user: ilimitado
Memoria: personal + empresa + por proyecto/cliente
Onboarding dedicado
SLA: 99.5%
Audit logs exportables
Descuento anual: 15%

Ejemplos de revenue mensual:
  5 seats:  $745/mes  ($8,940/año)
  10 seats: $1,490/mes ($17,880/año)
  15 seats: $2,235/mes ($26,820/año) ← gross profit ~$1,700/mes ✓
  50 seats: $7,450/mes ($89,400/año)
```

---

## La escalera correcta

```
$79/mes   Starter — 1 seat, RTX 4090, entrada fácil
$99/seat  Pro     — A6000, mejor GPU, equipo, más caro que Starter ✓
$149/seat Team    — H100, enterprise, más caro que Pro ✓
```

**La lógica es clara:**
- Starter < Pro por seat < Team por seat
- Cada tier tiene mejor GPU y más capacidades
- El precio sube con el valor entregado

---

## Cómo el usuario intensivo genera el margen que necesitamos

```
Equipo de 10 en Pro, todos NORMALES (la suscripción):
  Revenue: 10 × $99 = $990/mes
  COGS:    10 × $25.46 = $254.60
  Gross profit: $735.40 (74.3%)

Equipo de 10 en Pro, 30% son INTENSIVOS (3 usuarios × 660 créditos extra):
  Revenue base: $990
  Créditos extra: 3 × 660 × $0.08 = $158.40
  Revenue total: $1,148.40
  COGS extra GPU: 3 × $13.46 = $40.38
  COGS total: $294.98
  Gross profit: $853.42 (74.3%)

Empresa de 15 en Team, 32% intensivos (5 usuarios):
  Revenue base: 15 × $149 = $2,235
  Créditos extra: 5 × 660 × $0.07 = $231
  Revenue total: $2,466
  COGS base: 15 × $34.20 = $513
  COGS extra: 5 × $24.20 = $121
  COGS total: $634
  Gross profit: $1,832 (74.3%) ✓ vs $500 del modelo v3
```

---

## Comparativa vs. competencia

| | **Starter $79** | **Pro $99/seat** | Lindy Pro | Manus Std | Cursor Pro |
|---|---|---|---|---|---|
| GPU local | ✅ RTX 4090 | ✅ A6000 | ❌ | ❌ | ❌ |
| Memoria real | ✅ | ✅ | ❌ | ❌ | ❌ |
| Ejecución real | ✅ | ✅ | ❌ | Parcial | Parcial |
| Créditos ruedan | ✅ | ✅ | ❌ | ❌ | N/A |
| Precio | $79 | $99/seat | $49.99 | $20 | $20 |
| APIs incluidas | ❌ (usuario) | ❌ (usuario) | ✅ (límite) | ✅ (expiran) | ✅ (límite) |

**Oli es más caro pero entrega GPU propia, memoria real y ejecución real.**
**La competencia solo entrega acceso a chat.**

---

## MRR proyectado con 32% de usuarios intensivos

```
Escenario: 20 Starter + 8 equipos Pro (5 seats) + 3 Team (10 seats)

Revenue suscripciones:
  Starter: 20 × $79 = $1,580
  Pro:     8 × 5 × $99 = $3,960
  Team:    3 × 10 × $149 = $4,470
  Base MRR: $10,010

Revenue créditos extra (32% intensivos):
  Starter: 6 × 660 × $0.08 = $316.80
  Pro:     13 × 660 × $0.08 = $686.40
  Team:    10 × 660 × $0.07 = $462
  Extra MRR: $1,465.20

MRR total: $11,475.20
COGS total (~26%): ~$2,983
Gross profit: ~$8,492 (74%) ✓

OPEX $2,000 + Growth 25% ($2,869) = $4,869
Profit neto: $8,492 - $4,869 = $3,623/mes
```
