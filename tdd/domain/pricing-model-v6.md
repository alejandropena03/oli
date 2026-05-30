# Pricing Model V6

**Estado:** definitivo
**Fecha:** 2026-05-27
**Supersede:** pricing-model-v5.md

---

## Cambios respecto a V5

| Aspecto | V5 | V6 |
|---|---|---|
| Precio Starter | $79 | $79 (sin cambio) |
| Precio Pro | $99/seat | $129/seat |
| Precio Team | $149/seat (mín 5) | $199/seat (mín 4) |
| Créditos Starter | 660 | 660 (sin cambio) |
| Créditos Pro | 660/seat | 1,100/seat |
| Créditos Team | 660/seat | 1,500/seat |
| Overage Starter | $0.08/cr | $0.09/cr |
| Overage Pro | $0.08/cr | $0.08/cr (sin cambio) |
| Overage Team | $0.07/cr | $0.08/cr |
| Mínimo Team | 5 seats | 4 seats |
| Unit economics | Sin infra+ops | Incluye infra+ops por seat |
| Promedio cr/seat | Asumía 660 | Corregido a 778.8 (promedio ponderado real) |

**Motivación del aumento:** análisis de mercado (GPT + benchmarks de competidores) indicó que V5 estaba significativamente por debajo del rango de mercado para productos equivalentes.

---

## Nota operativa

> Estos son unit economics estimados para decisiones internas.
> Los créditos son la unidad operativa interna de cómputo — no necesariamente el copy principal de pricing público.
> 1 crédito = 1 minuto de GPU activa.

---

## Tiers

### Starter — $79/mes
```
1 seat
GPU: RTX 4090 clase
660 créditos/mes incluidos
Overage: $0.09/crédito
Créditos ruedan (cap 2x plan)
APIs externas: BYOK

Features:
  Memoria personal
  1 workspace
  1 misión activa
  BYOK para APIs externas

Para: founder solo, power user individual
```

### Pro — $129/seat/mes
```
Máximo 3 seats
GPU: A6000 clase
1,100 créditos/seat incluidos — pool compartido entre seats
Overage: $0.08/crédito
Créditos ruedan (cap 2x plan)

Features:
  Memoria personal + memoria colectiva
  Playbooks compartidos
  2-3 misiones concurrentes
  Sin SLA formal
  Sin audit export avanzado

Para: cofounders, mini-equipos, agencias pequeñas
```

### Team — $199/seat/mes
```
Mínimo 4 seats
GPU: H100 reservada
1,500 créditos/seat incluidos — pool compartido
Overage: $0.08/crédito
Créditos ruedan (cap 2x plan)

Features:
  Memoria por empresa + por proyecto/cliente
  Admin, roles, permisos avanzados
  Audit logs exportables
  Mayor concurrencia
  SLA (solo cuando el producto pueda cumplirlo de verdad)
  Done-with-you onboarding

Para: empresa pequeña, equipo formal, agencia mediana
```

---

## Distribución de uso base

```
21% ligeros    →   220 cr/mes  (10 min/día × 22 días)
47% normales   →   660 cr/mes  (30 min/día × 22 días)
32% intensivos → 1,320 cr/mes  (60 min/día × 22 días)

Promedio ponderado real:
  0.21 × 220 + 0.47 × 660 + 0.32 × 1,320
  = 46.2 + 310.2 + 422.4
  = 778.8 cr/seat/mes
```

---

## Costos GPU

Fuente: precios RunPod/serverless verificados 2026-05-27.

```
RTX 4090: $1.116/hr → $0.01860/cr
A6000:    $1.224/hr → $0.02040/cr
H100 res: $2.200/hr → $0.03667/cr
```

Infra + ops estimada por seat/mes:
```
Starter: $15.00
Pro:     $12.00
Team:    $10.00
```

---

## Unit economics por tier

### Starter — RTX 4090 ($0.0186/cr) + $15 infra

| Tipo | Cr usados | Overage ingresos | Ingreso total | Costo GPU | Infra | Costo total | Gross Profit | Margin |
|---|---|---|---|---|---|---|---|---|
| Ligero (21%) | 220 | $0 | $79.00 | $4.09 | $15 | $19.09 | $59.91 | 75.8% |
| Normal (47%) | 660 | $0 | $79.00 | $12.28 | $15 | $27.28 | $51.72 | 65.5% |
| Intensivo (32%) | 1,320 | $59.40 | $138.40 | $24.55 | $15 | $39.55 | $98.85 | 71.4% |

**Ponderado:**
- Revenue: $98.01/seat
- Gross profit: $68.52/seat
- **Gross margin: ~70%**

### Pro — A6000 ($0.0204/cr) + $12 infra

| Tipo | Cr usados | Overage ingresos | Ingreso total | Costo GPU | Infra | Costo total | Gross Profit | Margin |
|---|---|---|---|---|---|---|---|---|
| Ligero (21%) | 220 | $0 | $129.00 | $4.49 | $12 | $16.49 | $112.51 | 87.2% |
| Normal (47%) | 660 | $0 | $129.00 | $13.46 | $12 | $25.46 | $103.54 | 80.3% |
| Intensivo (32%) | 1,320 | $17.60 | $146.60 | $26.93 | $12 | $38.93 | $107.67 | 73.4% |

**Ponderado:**
- Revenue: $134.63/seat
- Gross profit: $106.74/seat
- **Gross margin: ~79%**

*Nota: el pool entre 2-3 seats suaviza picos — en la práctica los seats raramente son todos intensivos simultáneamente. El margen real tiende a ser mejor que este cálculo por-seat.*

### Team — H100 ($0.0367/cr) + $10 infra

| Tipo | Cr usados | Overage ingresos | Ingreso total | Costo GPU | Infra | Costo total | Gross Profit | Margin |
|---|---|---|---|---|---|---|---|---|
| Ligero (21%) | 220 | $0 | $199.00 | $8.07 | $10 | $18.07 | $180.93 | 90.9% |
| Normal (47%) | 660 | $0 | $199.00 | $24.22 | $10 | $34.22 | $164.78 | 82.8% |
| Intensivo (32%) | 1,320 | $0 | $199.00 | $48.44 | $10 | $58.44 | $140.56 | 70.6% |

**Ponderado (778.8 cr promedio — ningún tipo base supera el techo de 1,500 cr):**
- Revenue: $199.00/seat
- Gross profit: $160.43/seat
- **Gross margin: ~81%**

**Escenario referencia — 15 seats Team:**
```
Revenue base:   15 × $199.00           = $2,985.00
Overage:        $0 (distribución base)
Costo GPU:      15 × 778.8 × $0.0367   = $428.87
Infra + ops:    15 × $10.00            = $150.00
Costo total:                             $578.87
Gross profit:                          $2,406.13
Gross margin:                           ~80.6%
```

---

## Sensibilidad — usuarios ultra-intensivos en Team

Bajo la distribución base, el intensivo típico (1,320 cr) queda dentro del plan (techo 1,500 cr incluidos). Usuarios ultra-intensivos sí activan overage:

| Uso cr/mes | Overage | Ingreso total | Costo GPU | Infra | Costo total | Gross Profit | Margin |
|---|---|---|---|---|---|---|---|
| 1,500 (techo) | $0 | $199.00 | $55.01 | $10 | $65.01 | $133.99 | 67.3% |
| 2,000 | 500 × $0.08 = $40 | $239.00 | $73.40 | $10 | $83.40 | $155.60 | 65.1% |
| 3,000 | 1,500 × $0.08 = $120 | $319.00 | $110.10 | $10 | $120.10 | $198.90 | 62.4% |

**El overage sigue siendo positivo** — el margen sobre el exceso de GPU vs overage price es ~54%. El riesgo es compresión de margen, no pérdida. A 3,000 cr/mes el producto sigue siendo rentable por seat.

---

## Política de control de uso

Aplicable a todos los tiers. Estos controles son **producto** (UX de confianza y transparencia), no solo billing.

```
1. Alerta automática al 80% del uso incluido del período
   → Oli notifica al usuario proactivamente, con estimación del ritmo actual

2. Estimación pre-misión
   → Antes de ejecutar una misión con proyección de uso significativo,
     Oli muestra estimado de créditos y pide confirmación si supera threshold

3. Approval threshold configurable
   → Misión que puede superar umbral definido por el usuario/org
     requiere aprobación explícita antes de ejecutar (manual o auto según policy)

4. Hard cap opcional por usuario o equipo
   → Configurable en settings de org
   → Si se alcanza: Oli pausa la misión y notifica — no aborta silenciosamente
   → El usuario decide si ampliar, posponer o cancelar

Principio: el usuario debe sentir visibilidad total sobre su uso de compute.
Oli nunca debe sorprender al usuario con un cargo inesperado.
```

---

## Resumen ejecutivo

| Tier | Revenue ponderado | Gross profit | Margin | Overage upside |
|---|---|---|---|---|
| Starter | $98.01/seat | $68.52 | **~70%** | Sí — intensivos generan +$59.40 |
| Pro | $134.63/seat | $106.74 | **~79%** | Bajo — techo 1,100 absorbe intensivos típicos |
| Team | $199.00/seat | $160.43 | **~81%** | Muy bajo en dist. base — viene del precio, no overage |

**Riesgo principal:** Starter con usuarios muy intensivos tiene margen más ajustado (65.5% en normales). Mitigación: los intensivos generan overage que sube el margen promedio del tier.

**Riesgo Team:** ultra-intensivos (>1,500 cr) comprimen margen pero no lo invierten. Fair-use policy + approval threshold son la mitigación correcta.
