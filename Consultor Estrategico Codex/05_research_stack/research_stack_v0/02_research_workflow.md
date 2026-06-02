# 02 - Research Workflow

## Objetivo

Que Oli investigue con estructura, no con intuicion.

El subagente de research no decide solo. Produce evidencia. La decision la hace el Mission Kernel, consultor o judge con contexto y reglas.

## Flujo simple

```text
1. Entender pregunta
2. Elegir tipo de decision
3. Elegir fuentes
4. Buscar
5. Leer fuentes primarias
6. Guardar evidencia
7. Puntuar confianza
8. Comparar opciones
9. Validar contra TDD/memoria
10. Recomendar
11. Definir proximo paso y recheck
```

## Tipos de decision

### Model selection

Fuentes:

- OpenRouter Models;
- Hugging Face;
- Artificial Analysis;
- LMArena;
- model cards oficiales;
- vLLM/Ollama docs;
- TDD Model Router.

Output:

- modelos candidatos;
- fit de hardware;
- contexto realista;
- licencia;
- costo;
- riesgos;
- benchmark propio requerido.

### Agent/tool selection

Fuentes:

- official docs;
- GitHub repos;
- OpenRouter Apps;
- issues/releases;
- security advisories;
- TDD ADR-016/020/021/023.

Output:

- adopt/adapt/delegate/reject/monitor;
- ahorro estimado;
- riesgos;
- spike recomendado.

### Security decision

Fuentes:

- NVD/CVE;
- GitHub Advisories;
- vendor advisories;
- arXiv/security papers;
- repo issues;
- TDD ADR-020.

Output:

- risk list;
- mitigaciones;
- permission class;
- no-go conditions.

### Business/product research

Fuentes:

- web search;
- competitor docs/pricing;
- public case studies;
- customer data si existe;
- Oli memory;
- TDD ICP docs.

Output:

- segmento;
- pain;
- willingness to pay;
- demo/mision recomendada;
- gaps de evidencia.

## Contrato de evidencia

Cada hallazgo debe tener:

```text
claim
source_url
source_type
captured_at
published_at si existe
confidence
limitations
why_it_matters_for_oli
```

Sin fuente, no entra al memo como hecho. Puede entrar como inferencia marcada.

## Roles

### Researcher

Hace:

- buscar;
- leer;
- extraer claims;
- normalizar evidencia;
- marcar limites.

No hace:

- decision final;
- escribir memoria permanente;
- ejecutar acciones externas;
- aprobar herramientas.

### Judge / Consultant

Hace:

- comparar opciones;
- validar contra TDD;
- detectar riesgos;
- recomendar decision;
- pedir mas research si falta evidencia.

### Mission Kernel

Hace:

- decide permisos;
- registra Mission Black Box;
- guarda evidence pack;
- actualiza memoria/playbooks si corresponde.

## Reglas de fuente

1. Fuente primaria gana sobre blog.
2. Uso real no equivale a calidad.
3. Benchmarks no equivalen a fit con Oli.
4. GitHub stars no equivalen a madurez.
5. Reddit/HN son senales debiles, no decision.
6. TDD no gana contra realidad actual, pero obliga a explicar tradeoff.

