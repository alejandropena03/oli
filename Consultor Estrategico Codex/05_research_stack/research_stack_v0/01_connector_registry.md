# 01 - Connector Registry

## Principio

Oli debe traer conectores preestablecidos. El usuario no deberia configurar desde cero como investigar.

Cada conector debe declarar:

- proposito;
- trust level;
- costo esperado;
- tipo de evidencia;
- limitaciones;
- cuando usarlo;
- cuando no usarlo.

## Web search y lectura web

| Conector | Uso principal | Fortaleza | Limitacion |
|---|---|---|---|
| Brave Search | Busqueda web general, docs, noticias, fuentes primarias | Indice web propio, bueno para RAG/agentes | Devuelve resultados; necesita reader/fetch |
| Tavily | Research rapido y contexto curado para agentes | Search API pensada para LLMs | Vendor externo, puede resumir demasiado |
| Exa | Busqueda semantica/profunda | Encuentra fuentes por significado, no solo keywords | Requiere validacion posterior |
| Jina Reader | URL a Markdown limpio | Baja friccion, ideal despues de search | No siempre resuelve SPAs/anti-bot |
| Firecrawl | Crawling, scraping, extraction | Search + scrape + crawl, cloud/self-hosted | Costo/creditos, requiere scope |
| Crawl4AI | Crawling local para Dedicated Runtime | Open-source, control local | Mas mantenimiento y dependencias |
| DuckDuckGo/SearXNG | Fallback/zero-cost/privacy | Cero o baja friccion | No debe ser fuente principal seria |

## Codigo y open source

| Conector | Uso principal | Fortaleza | Limitacion |
|---|---|---|---|
| GitHub API | Repo metadata, releases, issues, PRs, commits, license, file tree | Fuente primaria para proyectos open-source | Stars/forks pueden enganar |
| GitHub Search | Descubrir repos y ejemplos | Cobertura amplia | Ruido alto sin scoring |
| GitHub Security Advisories | Vulnerabilidades en repos/dependencias | Cercano al codigo real | Incompleto frente a vendor advisories |

## Modelos y agentes

| Conector | Uso principal | Fortaleza | Limitacion |
|---|---|---|---|
| OpenRouter Apps | Senal de uso real de agentes/apps | Mide volumen publico opt-in | Token volume no es calidad |
| OpenRouter Models/Docs | Modelos, pricing, context, providers, routing | Fuente primaria de OpenRouter | No reemplaza evals propias |
| Hugging Face Hub | Model cards, licencias, downloads, datasets | Fuente primaria de modelos open-weight | Model cards pueden ser optimistas |
| Artificial Analysis | Comparativas de modelos, precio, velocidad | Buen benchmark/pricing externo | Metodologia debe revisarse |
| LMArena/Arena | Preferencia humana y ranking general | Human preference at scale | No especifico para misiones Oli |

## Papers y literatura

| Conector | Uso principal | Fortaleza | Limitacion |
|---|---|---|---|
| Semantic Scholar | Papers, citas, autores, abstracts | API estable para literatura cientifica | No todo paper es reproducible |
| arXiv | Preprints recientes | Muy actual | No peer reviewed necesariamente |
| OpenAlex | Grafo abierto de literatura | Buen landscape mapping | Menos orientado a codigo/agentes |

## Seguridad

| Conector | Uso principal | Fortaleza | Limitacion |
|---|---|---|---|
| NVD/CVE | Vulnerabilidades, CVEs, CPEs | Estandar publico | Puede estar atrasado |
| Vendor advisories | Mitigaciones y reportes recientes | A veces mas actual que NVD | Sesgo/formato vendor |
| GitHub Advisories | Riesgo por package/repo | Directo para dependencias | Incompleto |
| Security papers | Nuevas clases de ataque | Frontera tecnica | Puede no ser operativo |

## Contexto interno

| Conector | Uso principal | Fortaleza | Limitacion |
|---|---|---|---|
| TDD Connector | ADRs, domain docs, schemas, decisiones previas | Evita contradicciones con Oli | TDD puede estar viejo |
| Memory Connector | Misiones previas, preferencias, decisiones | Moat real por contexto propio | Riesgo de memoria contaminada |
| Mission Black Box | Evidencia, costos, fallos, tool calls | Aprendizaje por ejecucion real | Requiere instrumentacion |

## No-V0

Postergar como conectores formales:

- Reddit/Hacker News: senal debil, no decision.
- LinkedIn/X scraping: alto ruido y riesgos de ToS.
- Browser automation general: esperar tool security mas fuerte.
- SerpApi/Serper: solo si Brave/Tavily/Exa no cubren necesidad.

