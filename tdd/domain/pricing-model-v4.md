# Modelo de Pricing — Oli v4

**Fecha:** 2026-05-27
**Metodología:** Bottom-up desde los costos reales del negocio, no desde la competencia
**Principio:** El precio correcto es el que hace el negocio sostenible y escalable, no el más barato

---

## 1. ¿Cuánto necesita el negocio para ser sostenible?

Antes de fijar precios, hay que saber qué cuesta operar Oli como negocio real.

### Estructura de costos de un AI SaaS bootstrapped (benchmarks 2026)

```
COGS (costo directo de entregar el servicio):
  GPU on-demand (RunPod serverless)    variable por uso
  Infraestructura (Postgres, storage)  ~$200-500/mes fijos
  Objetivo gross margin:               70-80% (benchmark AI SaaS)

OPEX (costos operativos mensuales estimados para bootstrapped):
  Founder (tiempo propio):             $0 en cash inicial
  Herramientas + SaaS stack:           ~$300/mes
  Infraestructura base (dominio, CI):  ~$200/mes
  Legal/contabilidad:                  ~$300/mes
  Total OPEX mínimo bootstrapped:      ~$800/mes

GROWTH (marketing, contenido, distribución):
  Benchmark early B2B SaaS:            20-30% del revenue
  Content + community (bootstrapped):  ~$500-1,000/mes iniciales

TOTAL MENSUAL MÍNIMO PARA OPERAR:     ~$1,500-2,000/mes
```

### El objetivo de MRR para ser viable

```
Para cubrir OPEX + growth + tener algo para reinvertir:
  MRR mínimo de supervivencia:  $3,000-5,000/mes
  MRR de crecimiento saludable: $10,000-15,000/mes
  MRR para contratar primera persona: $20,000+/mes

Regla del 40 (benchmark SaaS):
  Growth rate % + Profit margin % ≥ 40
  Si crecemos 30% MoM → podemos tener -10% de margen (invertir en growth)
  Si crecemos 10% MoM → necesitamos 30% de margen neto mínimo
```

---

## 2. El error del modelo anterior

El modelo v3 tenía:
- Starter: $29/mes → con 300 créditos incluidos y COGS de $18 → gross margin 38%
- Pro: $79/seat → COGS $38 → gross margin 51%
- Team: $59/seat → COGS $25 → gross margin 58%

**El problema:** gross margins de 38-58% son insuficientes para un AI SaaS que necesita:
- Pagar growth (20-30% del revenue)
- Pagar OPEX (20-25% del revenue)
- Quedar algo para reinvertir en R&D y el producto

Con 38% gross margin, después de OPEX y growth no queda nada.
**El objetivo es 70-80% gross margin** — eso es lo que permite escalar.

---

## 3. Recalcular: precio desde el gross margin objetivo

### COGS real por tier (RunPod serverless verificado)

```
Uso real por seat activo: ~37 hrs GPU/mes (datos McKinsey/Slack 2026)
  Pero: no toda la misión usa GPU al 100%
  Promedio efectivo: ~60% del tiempo de misión = GPU activa
  37 hrs × 0.6 = ~22 hrs de GPU activa real por seat/mes

COGS de GPU:
  Starter (RTX 4090, $1.116/hr):  22 hrs × $1.116 = $24.55
  Pro     (A6000, $1.224/hr):     22 hrs × $1.224 = $26.93
  Team    (H100 reservada, $2.20): 22 hrs × $2.20  = $48.40

Más infraestructura y ops:
  Starter: $24.55 + $15 infra + $5 ops = $44.55 COGS/seat
  Pro:     $26.93 + $10 infra + $5 ops = $41.93 COGS/seat (economía de escala)
  Team:    $48.40 + $5 infra + $8 ops  = $61.40 COGS/seat
```

### Precio mínimo para 75% gross margin

```
Fórmula: Precio = COGS / (1 - target_margin)

Starter: $44.55 / (1 - 0.75) = $178.20 → redondear a $179/mes
Pro:     $41.93 / (1 - 0.75) = $167.72 → redondear a $169/seat/mes
Team:    $61.40 / (1 - 0.75) = $245.60 → redondear a $249/seat/mes
```

**Verificación:**

```
Starter $179:
  Revenue: $179 | COGS: $45 | Gross profit: $134 | GM: 74.9% ✓

Pro $169/seat (equipo de 5):
  Revenue: $845 | COGS: $210 | Gross profit: $635 | GM: 75.1% ✓

Team $249/seat (empresa de 15):
  Revenue: $3,735 | COGS: $921 | Gross profit: $2,814 | GM: 75.3% ✓
```

### ¿Qué queda después de OPEX y growth?

```
Escenario: 20 clientes Starter + 5 equipos Pro (5 seats avg) + 2 Team (10 seats avg)

MRR:
  Starter: 20 × $179     = $3,580
  Pro:     5 × 5 × $169  = $4,225
  Team:    2 × 10 × $249 = $4,980
  Total MRR: $12,785

OPEX mensual: $2,000
Growth (25% del revenue): $3,196
COGS (25% del revenue): $3,196
  
Profit neto: $12,785 - $2,000 - $3,196 - $3,196 = $4,393/mes ✓

→ $4,393/mes de profit neto permite:
  - Reinvertir en el producto
  - Primer contrato part-time de soporte
  - Runway para escalar
```

---

## 4. El modelo v4 — precios reales

### Starter — $179/mes

```
Para: founders solos, uso individual activo
GPU:  RTX 4090 (24GB) serverless RunPod
Créditos incluidos: 1,300/mes (~22 hrs GPU efectiva)
  = cubre el uso promedio de un founder activo
  = ~130 misiones simples / ~65 medias / ~26 complejas

Créditos extra: $0.08/crédito
  (RTX 4090 $1.116/hr = $0.0186/min de costo → markup 4.3x)
  (markup alto en extras = el que más usa, más contribuye al margen)

Gross margin: 74.9%
Seats: 1
Concurrent: 1 misión activa
Memoria: personal + empresa (solo su propia)
APIs externas: el usuario conecta y paga las suyas
```

---

### Pro — $169/seat/mes

```
Para: equipos pequeños, startups, agencias (2-15 personas)
GPU:  A6000 (48GB) serverless — Qwen3 35B-A3B MoE local (Tier 2 gratis)
Créditos incluidos: 1,300/seat/mes (~22 hrs GPU efectiva por seat)
  Pool compartido del equipo (si un seat usa 500 y otro usa 2,100, se balancea)

Créditos extra: $0.08/crédito
Mínimo: 1 seat ($169/mes)
Concurrent: 2 misiones/seat simultáneas
Multi-user: ilimitado (paga por cada seat)
Memoria: personal (privada por seat) + empresa (compartida)
Playbooks de equipo
APIs externas: el equipo conecta las suyas

Gross margin: 75.1% (con 5+ seats)

Ejemplos:
  Solo founder Pro (más GPU que Starter): $169/mes
  Equipo 3: $507/mes
  Equipo 5: $845/mes
  Equipo 10: $1,690/mes
```

---

### Team — $249/seat/mes (mínimo 5 seats)

```
Para: empresas, equipos grandes, compliance requerido
GPU:  H100 SXM (80GB) reservada — negociada con RunPod ~$2.20/hr
      La H100 compartida permite más concurrencia y modelos más grandes
Créditos incluidos: 1,300/seat/mes
  Mismo volumen que Pro PERO la H100 es más rápida:
  una misión que tarda 30 min en A6000 tarda ~18 min en H100
  → mismo trabajo, menos créditos consumidos → efectivamente más capacidad

Créditos extra: $0.07/crédito (ligero descuento por volumen)
Mínimo: 5 seats ($1,245/mes)
Concurrent: ilimitado dentro de capacidad GPU
Multi-user: ilimitado
Memoria: personal + empresa + por proyecto/cliente
H100: corre modelos más grandes, más rápido, más misiones paralelas
Onboarding dedicado con Oli
SLA: 99.5% uptime
Audit logs exportables (compliance)
APIs externas: el equipo conecta las suyas
Descuento anual: 15%

Gross margin: 75.3%

Ejemplos:
  Empresa 5 seats:  $1,245/mes  → $14,940/año
  Empresa 10 seats: $2,490/mes  → $29,880/año
  Empresa 15 seats: $3,735/mes  → $44,820/año ← profit $2,814/mes
  Empresa 50 seats: $12,450/mes → $149,400/año
```

---

## 5. Profit por escenario — respondiendo la pregunta original

```
¿Cuánto profit con 15 seats Team?
  Revenue: 15 × $249 = $3,735/mes
  COGS:    15 × $61.40 = $921/mes
  Gross profit: $2,814/mes ✓ (mucho mejor que los $500 del modelo v3)

¿Cuánto profit con 10 seats Pro?
  Revenue: 10 × $169 = $1,690/mes
  COGS:    10 × $42 = $420/mes
  Gross profit: $1,270/mes ✓

¿Y después de OPEX y growth?
  OPEX del negocio: ~$2,000/mes fijo
  Growth (25% revenue): varía con el MRR
  
  Break-even operativo (solo OPEX):
    $2,000 OPEX / ($179 × 0.75) = ~15 clientes Starter
    → Con 15 Starters, el negocio cubre sus costos fijos
```

---

## 6. La escalera de valor — revisada

```
$179/mes  → entrada de founders activos
             Más caro que v3 ($29) pero justificado:
             La GPU cuesta $45 de COGS — $29 era perder dinero

$169/seat → equipos, precio POR SEAT más barato que Starter
             (economía de A6000 vs RTX 4090 en COGS)
             El equipo de 3 paga $507, menos que 3 Starters ($537)

$249/seat → empresa, H100, compliance, SLA
             El costo es más alto (H100), el precio refleja el valor
             Una empresa de 15 personas con Oli vs. sin Oli:
             $3,735/mes vs. contratar 1 persona ops a ~$5,000-8,000/mes
```

---

## 7. Comparativa final con competencia

| | Starter Oli | Lindy Pro | Manus Standard | Cursor Pro |
|---|---|---|---|---|
| Precio | **$179/mes** | $49.99/mes | $20/mes | $20/mes |
| GPU local incluida | ✅ RTX 4090 | ❌ | ❌ | ❌ |
| Memoria persistente real | ✅ | ❌ | ❌ | ❌ |
| Ejecución real de código/browser | ✅ | ❌ | Parcial | Parcial |
| Créditos que ruedan | ✅ | ❌ | ❌ | N/A |
| APIs externas | Usuario paga | Incluidas con límite | Incluidas (expiran) | Incluidas con límite |

**Oli es más caro que la competencia y debe serlo.**
La competencia vende acceso a chat con herramientas. Oli vende un operador con GPU propia, memoria real, ejecución real y audit trail. Son productos diferentes.

**El argumento de venta:**
> "Lindy Pro $49.99: pagas por workflows sin ejecución real. Sin modelo local. Sin memoria.
> Oli $179: tienes GPU propia que corre modelos locales. Memoria que crece con el uso.
> Ejecución real en cualquier herramienta. El 70% de tus tareas corren localmente — 
> no pagas APIs para eso. Y todo queda en audit trail."

---

## 8. Pendiente validar

- [ ] ¿$179 convierte para founders? Testear con 10 entrevistas del ICP
- [ ] ¿El precio es sensible a si incluimos créditos extras como "free trial"?
- [ ] Modelo freemium vs. trial 14 días — ¿cuál convierte mejor para este ICP?
- [ ] Negociar precios reservados con RunPod (necesita volumen)
- [ ] Descuento anual: ¿15% o 20% para anual?
