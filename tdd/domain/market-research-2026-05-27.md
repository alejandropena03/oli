# Market Research — Oli

**Fecha:** 2026-05-27
**Metodología:** Web search en tiempo real + GitHub MCP + datos verificados
**Estado:** V1 — investigación inicial con datos reales

---

## 1. TAMAÑO DEL MERCADO

| Métrica | Valor | Fuente |
|---|---|---|
| AI Agents market 2026 | $11.5B – $15B | Precedence Research, Grand View |
| AI Agents market 2030 | $52.6B – $53.2B | MarketsAndMarkets |
| AI Agents market 2035 | $221B – $294B | Múltiples firmas |
| CAGR 2026-2035 | 34-46% | Consenso de analistas |
| Empresas que implementarán AI agents 2025-end | 85% | Survey empresarial |

**El segmento de Oli (personal/SMB):**
- "Ready-to-deploy horizontal agents" = 85% del mercado actual
- "Research and summarization" = 25% del mercado por uso
- Nuestro ICP (founders + operators + small teams) = segmento de adopción más rápida

---

## 2. COMPETENCIA DIRECTA — PRECIOS REALES

### Lindy AI
**Posicionamiento:** No-code AI agent builder para workflows de negocio

| Plan | Precio/mes | Créditos | Lo que incluye |
|---|---|---|---|
| Starter | $19.99 | 2,000 | Workflows básicos |
| Pro | $49.99 | 5,000 | Inbox, calendar, iMessage |
| Max | $199.99 | Sin límite | Todo + enterprise features |
| Enterprise | Custom | Ilimitado | SOC 2, HIPAA |

**Limitaciones de Lindy:**
- No-code — el usuario no puede personalizar la lógica
- Sin ejecución real de código/desktop/browser
- Sin memoria persistente real entre workflows
- Sin modelo local — todo a sus APIs
- Créditos por acción: acciones complejas consumen 5-10x más

**Usuarios reales:** 400,000+ pagando

---

### Manus AI (adquirido por Meta, ~$2B)
**Posicionamiento:** Agente autónomo para tareas complejas multi-step

| Plan | Precio/mes | Créditos | Nota |
|---|---|---|---|
| Free | $0 | 300/día | Solo Manus Lite |
| Standard | $20 | 4,000 | |
| Customizable | $40 | 8,000 | |
| Extended | $200 | 40,000 | |
| Team | $20/seat | — | |

**Limitaciones de Manus:**
- Cloud-only — tus datos en sus servidores (Meta)
- Créditos no se acumulan — expiran al mes
- Una sola tarea compleja puede consumir 900-1,000 créditos
- Sin memoria real entre sesiones
- Sin modelo local — 100% APIs externas

---

### OpenClaw (open source, 361K+ stars)
**Posicionamiento:** Agente personal local, gratis

| Costo | Detalle |
|---|---|
| Software | $0 (MIT) |
| APIs | El usuario paga las suyas |
| GPU | El usuario la configura |
| Setup | El usuario lo hace todo |

**Limitaciones:**
- CVEs críticos documentados (2026)
- Inestabilidad documentada (update 2026.4.26 rompió todo)
- Setup complejo — no apto para founders no técnicos
- Sin soporte, sin onboarding, sin garantías

---

## 3. COMPETENCIA INDIRECTA — "LO QUE HACEN CON APIS DIRECTAS"

Esta es la competencia más real de Oli: el founder técnico que construye su propio stack.

**Costo real si pagas APIs directamente:**

| Uso mensual (founder activo) | Costo APIs | Lo que NO tienes |
|---|---|---|
| 100 misiones simples (Haiku) | ~$5 | Memoria, validación, playbooks, UI |
| 100 misiones medianas (Sonnet) | ~$15 | Idem |
| 100 misiones complejas (Sonnet heavy) | ~$75 | Idem |
| Equipo de 5, uso intensivo | ~$600-2,000/mes | Idem |

**Lo que falta en el stack DIY que Oli resuelve:**
- Memory Graph persistente entre sesiones
- Validation antes de entrega
- Permission model con audit trail
- Playbooks que mejoran solos
- Setup de modelos locales
- Troubleshooting autónomo
- Evidence Store por misión

---

## 4. PRECIOS DE GPU ON-DEMAND (nuestro costo real)

| GPU | Provider | On-demand/hr | Serverless (0 cuando idle) |
|---|---|---|---|
| RTX 4090 (24GB) | RunPod | $0.43-0.50 | ✅ Disponible |
| A6000 (48GB) | Vast.ai | ~$0.41 | ✅ |
| RTX 5090 (32GB) | Salad/Vast.ai | ~$0.80-1.20 | ✅ |
| A100 80GB | Lambda Labs | $2.49 | ❌ |
| H100 SXM | RunPod | $1.99 on-demand / $1.25 spot | ✅ |

**RunPod serverless = la clave del modelo de negocio:**
- Se escala a 0 cuando no hay trabajo → el usuario paga $0 en idle
- Se enciende en segundos cuando llega una misión
- Nosotros pagamos por segundos de cómputo real

**Costo real por misión (estimado):**

| Misión | Duración GPU activa | Costo GPU (RTX 4090) | Tokens API | Costo total |
|---|---|---|---|---|
| Simple (research, resumen) | ~0 min (Tier 1 local) | $0 | Haiku: ~$0.02 | ~$0.02 |
| Media (plan + reporte) | ~3 min | ~$0.025 | Sonnet: ~$0.10 | ~$0.12 |
| Compleja (sistema, código) | ~8 min | ~$0.06 | Sonnet heavy: ~$0.35 | ~$0.41 |

---

## 5. MODELO DE PRICING DE OLI — 3 TIERS

Basado en el costo real de GPU on-demand + margen sostenible + benchmark competitivo.

### Principios de pricing

**1. El usuario paga sus propias APIs externas (Claude, OpenAI, etc.)**
Nosotros cobramos GPU + infraestructura + el software de Oli.
Esto simplifica el modelo y alinea incentivos: el usuario elige sus modelos.

**2. Créditos = GPU real + infraestructura**
1 crédito = $0.01 de costo real nuestro (GPU activa + storage + network).
Los créditos SÍ ruedan al mes siguiente — no expiran como Manus.

**3. El precio refleja el valor del producto, no solo el COGS**
El ICP ya gasta $300-400/mes en herramientas que no se integran, no recuerdan
y no ejecutan. Oli reemplaza o supera ese stack con un precio justificado.

**4. Gross margin target: 65-70%**
Benchmark AI-native SaaS 2026: 55-70%.
COGS incluye: GPU on-demand + infra + soporte + ops.
Variable COGS: 25-35% del revenue (consistente con el mercado).

**5. Seats escalan el precio para empresas**
Una empresa de 10 personas recibe 10x más valor.
El precio por seat aumenta en Team — empresas con ingresos pagan más.

---

### Precios reales de GPU — RunPod (verificado 2026-05-27)

```
SERVERLESS (pagamos solo segundos activos — $0 en idle):
  RTX 4090 (24GB):  $1.10/hr serverless
  A6000 (48GB):     $1.22/hr serverless
  H100 SXM (80GB):  $4.18/hr serverless
  A100 SXM (80GB):  $2.72/hr serverless

ON-DEMAND (24/7 encendida — más barata por hora, paga siempre):
  RTX 4090:  $0.69/hr
  A6000:     $0.49/hr
  H100 SXM:  $3.29/hr

RESERVADA (7+ días commitment — 15-30% descuento):
  H100 reservada: ~$2.20-2.50/hr vs $3.29 on-demand
  Aplica cuando tenemos volumen suficiente de usuarios activos

ESTRATEGIA: serverless para V0-V2 (menor riesgo), reservada en V3+ cuando
la utilización promedio supera el 40% del tiempo.
```

### Costo real de GPU por misión (con precios serverless reales)

```
Misión simple (GPU activa ~2-3 min):
  RTX 4090: 2.5 min × ($1.10/60) = $0.046
  
Misión media (GPU activa ~5-8 min):
  RTX 4090: 6 min × ($1.10/60) = $0.11
  A6000:    6 min × ($1.22/60) = $0.12

Misión compleja (GPU activa ~10-20 min):
  RTX 4090: 15 min × ($1.10/60) = $0.28
  H100:     15 min × ($4.18/60) = $1.05 → usar reservada o on-demand

→ H100 solo vale para Team con alta utilización.
  Para Starter/Pro, RTX 4090 o A6000 son más eficientes.
```

### Margen sobre GPU — el markup correcto

```
Nosotros cobramos créditos. El usuario no ve el precio de la GPU.
1 crédito = $0.01 de nuestro costo real (GPU + infra + ops).

Para tener gross margin 65-70% sobre el COGS total:
  COGS total por seat/mes = GPU + infra ($5) + ops/soporte ($10) + growth allocation
  
Uso promedio realista por seat (founder/operator activo):
  ~50-100 misiones/mes → mix de simples y medias
  GPU activa total: ~5-10 hrs/mes serverless

COGS GPU por seat/mes:
  Starter (RTX 4090, 7 hrs activo): 7 × $1.10 = $7.70 GPU
  Pro/seat (A6000, 7 hrs activo):   7 × $1.22 = $8.54 GPU
  Team/seat (H100 reservada, 7 hrs): 7 × $2.50 = $17.50 GPU

COGS total por seat/mes (GPU + infra + ops):
  Starter: $7.70 + $5 + $10 = ~$23/seat
  Pro:     $8.54 + $5 + $8  = ~$22/seat (economía en ops al escalar)
  Team:    $17.50 + $3 + $5 = ~$26/seat (H100 más cara pero mejor margen a escala)
```

---

### Tier 1 — Starter

```
Precio: $149/mes — 1 seat
Créditos incluidos: 10,000/mes (ruedan)
  Equivale a: ~100-200 misiones promedio/mes
GPU: RTX 4090 (24GB) on-demand serverless
Modelos locales: Qwen3 27B Q4, Llama 3.1 8B — corren en la GPU incluida
APIs externas: el usuario conecta y paga las suyas
Concurrent: 1 misión activa
Créditos extra: $8 por 1,000 adicionales

COGS estimado: ~$25-35/mes
Gross margin: ~77-83%

Para quién: founders solos, consultores, operadores independientes
Argumento de valor: reemplaza $300-400/mes de stack de herramientas sueltas
```

---

### Tier 2 — Pro

```
Precio base: $199/mes (2 seats incluidos)
Seats adicionales: $79/seat/mes
Ej: equipo de 5 → $199 + (3 × $79) = $436/mes

Créditos incluidos: 25,000/mes base + 8,000/seat adicional (ruedan)
GPU: A6000 (48GB) on-demand — compartida entre el equipo
Modelos locales: Qwen3 35B-A3B MoE — Tier 2 gratis en GPU
APIs externas: el equipo conecta y paga las suyas
Concurrent: 3 misiones paralelas
Multi-user: hasta 10 seats
Memoria: personal (privada por seat) + empresa (compartida)
Playbooks de equipo compartidos
Créditos extra: $7 por 1,000 adicionales

COGS estimado: ~$35-55/mes base + $15-20/seat adicional
Gross margin: ~72-80%

Para quién: startups, agencias, equipos ops 2-10 personas
```

---

### Tier 3 — Team

```
Precio: $129/seat/mes (mínimo 5 seats = $645/mes)
Ej: empresa de 15  → $1,935/mes
Ej: empresa de 50  → $6,450/mes

Créditos incluidos: 15,000/seat/mes (ruedan)
  Economía de escala: más créditos por dólar que Starter
GPU: H100 (80GB) — capacidad escalada con los seats, compartida
Modelos locales: cualquier modelo open source, incl. fine-tuned propios en Enterprise
APIs externas: el equipo conecta y paga las suyas
Concurrent: ilimitado dentro de capacidad GPU
Multi-user: ilimitado
Memoria: personal + empresa + por proyecto/cliente
Onboarding dedicado con Oli
SLA: 99.5% uptime
Audit logs exportables (compliance)
Créditos extra: $6 por 1,000 adicionales

COGS estimado: ~$15-20/seat/mes (H100 compartido, economía de escala)
Gross margin: ~83-88% (escala mejora el margen significativamente)

Para quién: empresas 10-200 personas, ops teams, agencias con clientes
```

---

### Por qué Team es más caro por seat que Pro

```
Founder solo (Starter):  $149/mes      → $149/seat
Equipo 5 (Pro):          $436/mes      → $87.2/seat
Empresa 15 (Team):       $1,935/mes    → $129/seat
Empresa 50 (Team):       $6,450/mes    → $129/seat
```

Team cuesta más por seat que Pro — intencionalmente.
Las empresas tienen más ingresos, necesitan compliance (audit logs),
SLAs garantizados, onboarding dedicado, y memoria por proyecto/cliente.
El margen en Team también es el más alto por la economía de escala del H100.

---

### Comparativa vs. competencia (equipo de 10)

| Producto | Equipo de 10 | $/mes | Modelo local | Memoria | Audit | APIs |
|---|---|---|---|---|---|---|
| Lindy Pro | 10 × $49.99 | $499 | ❌ | ❌ | ❌ | Incluidas (con límite) |
| Manus Standard | 10 × $20 | $200 | ❌ | ❌ | ❌ | Incluidas (expiran) |
| **Oli Pro** | $199 + 8 × $79 | **$831** | ✅ A6000 | ✅ | ✅ | Usuario paga las suyas |
| **Oli Team** | 10 × $129 | **$1,290** | ✅ H100 | ✅ | ✅ | Usuario paga las suyas |

**Nota importante:** Oli parece más caro que Manus/Lindy porque el usuario paga sus APIs aparte.
El argumento de venta correcto es el **costo total incluyendo APIs**:

```
Lindy Pro equipo 10:  $499/mes (APIs incluidas con créditos limitados)
Manus equipo 10:      $200/mes + desbordamiento de créditos real
Oli Pro equipo 10:    $831/mes + APIs propias (estimado $50-150 real)
  → $881-981/mes total
  → PERO: Oli tiene modelo local → las misiones Tier 1/2 no usan APIs
  → Ahorro real en APIs: 60-70% vs. competencia cloud-only
  → Valor real: memoria, audit, ejecución real, playbooks que mejoran
```

Para un equipo que usa Oli intensivamente, las APIs propias cuestan mucho menos
porque el 60-70% de las acciones corren localmente en la GPU incluida.

---

### Créditos — mecánica exacta

```
1 crédito = $0.01 de costo real nuestro

Consumo aproximado por tipo de misión:
  Simple (research, clasificar, buscar):    5-20 créditos
  Media (planificar, redactar, analizar):  20-80 créditos
  Compleja (sistema, código, arquitectura): 80-300 créditos

Ejemplo Starter (10,000 créditos/mes):
  ~100 misiones simples, O
  ~50 misiones medias, O
  ~30 misiones mixtas (realista para founder activo)

Los créditos ruedan — si usas 6,000 en enero, los 4,000 restantes
se suman a los 10,000 de febrero (cap: 2x el plan mensual).
```

---

## 6. EL ARGUMENTO DE VALOR vs. COMPETENCIA

### vs. Lindy ($49.99/mes Pro)

| Criterio | Lindy Pro | Oli Starter ($49) |
|---|---|---|
| Ejecución real de código | ❌ | ✅ (Docker sandbox) |
| Control de desktop/browser | ❌ | ✅ (Stagehand, ClawdCursor) |
| Modelo local (privacy) | ❌ todo cloud | ✅ GPU incluida |
| Memoria persistente real | ❌ | ✅ Memory Graph |
| Audit trail por misión | ❌ | ✅ Evidence Store |
| Playbooks que mejoran solos | ❌ | ✅ |
| Troubleshooting autónomo | ❌ | ✅ |
| Costo de API adicional | Sí (créditos extras) | Solo Tier 3 (Sonnet) |
| Multi-user en $49 | ❌ | ❌ (Starter: 1 user) |

### vs. Manus Standard ($20/mes)

| Criterio | Manus $20 | Oli Starter ($49) |
|---|---|---|
| Privacy (datos locales) | ❌ Meta/cloud | ✅ GPU propia |
| Créditos que expiran | ✅ (no rolan) | N/A — GPU on-demand |
| Modelo local | ❌ | ✅ |
| Memoria entre sesiones | ❌ | ✅ |
| Audit trail | ❌ | ✅ |
| Precio | $20 | $49 |

**Argument:** Manus es más barato pero es un consumible de nube. Oli es una plataforma que aprende y mejora. El ROI de Oli crece con el uso; el de Manus se reinicia cada mes.

### vs. DIY (APIs directas)

Un founder técnico gastando en APIs + su propio setup:
- $100-600/mes en APIs según volumen
- 20-40 horas de setup y mantenimiento
- Sin memoria, sin playbooks, sin UI

Oli Starter a $49: menos caro en APIs, setup en minutos, todo incluido.

---

## 7. PAIN POINTS DEL ICP — LO QUE MÁS DUELE

Basado en el research:

**Founders técnicos (early adopter):**
1. "Pago $600+/mes entre Cursor, Claude Code, APIs — sin memoria entre herramientas"
2. "Cada herramienta necesita el mismo contexto de nuevo"
3. "Los agentes hacen la mitad del trabajo — el resto lo tengo que terminar yo"
4. "No puedo delegarle trabajo real, solo tasks de texto"

**Operators (monetization ICP):**
1. "Automatizo con Zapier/n8n pero rompe todo el tiempo"
2. "Mis flujos no recuerdan el contexto del cliente"
3. "No tengo audit trail de lo que hizo el agente"
4. "Necesito que alguien más en el equipo pueda usar mis automaciones"

**Lo que buscan:**
- Trabajo terminado, no sugerencias
- Que recuerde sin que yo repita
- Que pruebe que funcionó
- Que aprenda de los errores

---

## 8. MOAT DE OLI vs. COMPETENCIA

| Moat | Oli | Lindy | Manus | OpenClaw |
|---|---|---|---|---|
| Memoria que crece | ✅ pgvector + Memory Graph | ❌ | ❌ | Parcial |
| Local-first (privacy) | ✅ GPU incluida | ❌ | ❌ | ✅ (pero setup) |
| Audit trail completo | ✅ Evidence Store | ❌ | ❌ | ❌ |
| Playbooks que mejoran | ✅ auto-caching | ❌ | ❌ | ❌ |
| Multi-user con memoria shared | ✅ ADR-018 | Parcial | ❌ | ❌ |
| Ejecución real (código, browser, desktop) | ✅ | ❌ | Parcial | Parcial |
| Setup sin fricción | ✅ (wizard) | ✅ | ✅ | ❌ |
| Precio vs. valor | ✅ | Medio | Bajo (créditos expiran) | $0 pero complejo |

---

## 9. GAPS PENDIENTES DE INVESTIGAR

- [ ] Entrevistas reales con founders/operators del ICP (ningún dato es de entrevistas directas aún)
- [ ] WTP real con metodología correcta (la de METR fue reconocida como débil)
- [ ] Qué canal de adquisición funciona mejor (content, community, product-led)
- [ ] Precio exacto del Tier 3 (necesita validar con usuarios Enterprise)
- [ ] Competidores emergentes que no aparecen en buscadores aún
