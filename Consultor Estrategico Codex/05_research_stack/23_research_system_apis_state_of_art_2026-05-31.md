# Sistema de Research SOTA para Oli - APIs y Herramientas

Fecha: 2026-05-31
Autor: Codex (Consultor Estrategico)

## El Problema del "Web Fetch" tradicional
Un simple `requests.get()` o un web fetch basico falla constantemente en 2026 debido a protecciones anti-bot (Cloudflare, Datadome), sitios basados fuertemente en JavaScript (SPAs), y la falta de semantica clara en el HTML devuelto, lo que consume excesivos tokens del LLM y genera alucinaciones o ruido. 

Modelos como los de Google (Gemini con Google Search Grounding) tienen una ventaja nativa porque acceden al indice directo de Google y a contenido pre-procesado. Para que Oli ofrezca un nivel SOTA de forma open-source o vendor-neutral, no puede depender de un fetch basico. Necesita APIs y librerias nativas diseñadas para alimentar agentes LLM.

## Ecosistema de APIs de Research (Open Source & Free Tier)

### 1. APIs Nativas para Agentes LLM (Search + Scrape + Markdown)
Estas herramientas no solo buscan, sino que ingresan a los links, renderizan JS, evaden anti-bots y devuelven Markdown limpio optimizado para RAG/LLMs.

*   **Firecrawl (Recomendacion Principal para Produccion):**
    *   *Que es:* Convierte sitios web enteros en Markdown limpio. Integra busqueda y crawling en un solo paso. Permite extraccion estructurada.
    *   *Licencia/Costo:* Open Source (self-hostable) + Cloud managed con Free tier (500 creditos/mes).
    *   *Por que usarlo en Oli:* Excelente para construir knowledge bases dinamicas o investigar un dominio completo (ej. competidores). Se integra nativo con LangGraph y frameworks de agentes.
*   **Tavily Search:**
    *   *Que es:* Search API construida especificamente para agentes IA. Devuelve resultados como contexto curado en vez de una simple lista de links (hace el fetch intermedio por ti).
    *   *Licencia/Costo:* Comercial con Free Tier generoso (1000 busquedas/mes).
    *   *Por que usarlo en Oli:* Es el estandar de facto en ejemplos de agents. Reduce latencia y consumo de tokens al dar la respuesta resumida y las fuentes de inmediato.
*   **Jina Reader API (`r.jina.ai` y `s.jina.ai`):**
    *   *Que es:* Pasas cualquier URL por `r.jina.ai/https...` y devuelve Markdown perfecto para LLMs. `s.jina.ai` hace la busqueda.
    *   *Licencia/Costo:* Open Source core, Free tier muy rapido y simple.
    *   *Por que usarlo en Oli:* Excelente para research tactico y rapido. Cero configuracion, instalacion de librerias minimas.

### 2. Scraping & Crawling Local/Self-Hosted Puro (Control Total)
Si Oli va a correr localmente o como un *Dedicated Runtime* (como sugiere la ADR-021), es posible evitar las APIs externas usando librerias locales muy potentes.

*   **Crawl4AI:**
    *   *Que es:* Libreria Python open-source diseñada especificamente para agentes AI. Usa Playwright bajo el capó, extrae contenido estructurado, maneja proxies y permite extraccion semantica guiada por LLM directamente local.
    *   *Licencia/Costo:* 100% Free y Open Source.
    *   *Por que usarlo en Oli:* Si se busca que Oli no dependa de cuotas mensuales de APIs externas y corra on-premise, integrar Crawl4AI en un suboperador de web_fetcher es la opcion SOTA actual.

### 3. Motores de Busqueda Puros (Solo Links y Snippets)

*   **DuckDuckGo Search (`duckduckgo-search` en Python):**
    *   *Licencia/Costo:* Gratis, sin API key, open source.
    *   *Por que usarlo en Oli:* El fallback perfecto por defecto. Cero friccion para nuevos usuarios, aunque requiere un fetcher adicional (como Jina o Crawl4AI) para leer el contenido de las paginas.
*   **SearxNG:**
    *   *Que es:* Metabuscador open-source, privacy-respecting.
    *   *Por que usarlo en Oli:* Puede ser instanciado en el servidor dedicado de Oli para no depender de corporaciones para los resultados base.
*   **Serper.dev / SerpApi:**
    *   *Para resultados estrictamente de Google Search (SEO, local, shopping).* Tienen free tiers generosos.

### 4. Fuentes Cientificas y Especializadas (El "Deep Research")
Para "State of the Art" research (ej. papers, medicina, biologia), web search general es insuficiente. Oli debe aprovechar *skills* o plugins especificos:
*   **OpenAlex / Semantic Scholar:** Para literature research libre.
*   **arXiv / PubMed / EuropePMC:** Preprints y ciencias de la salud (herramientas que el entorno de Oli ya puede orquestar segun las skills registradas).

## Arquitectura de Research Propuesta para Oli

Oli no deberia tener "una" herramienta de web search harcodeada. Deberia tener un `Research Subsystem` (alineado con la `ADR-025-state-of-art-discovery-and-decision-memos.md`) que enrute segun la necesidad y el tier del usuario:

1.  **Tier 1 (Zero-Cost / Fallback local):** `duckduckgo-search` + `Jina Reader API` (busqueda gratis, fetch a Markdown gratis).
2.  **Tier 2 (AI-Native / Production Managed):** `Tavily` (para preguntas amplias) o `Firecrawl` (para deep crawls de dominios comerciales).
3.  **Tier 3 (Self-Hosted / Dedicated Runtime):** `Crawl4AI` para misiones pesadas donde pagar una API externa por miles de paginas destruiria el margen de Oli.
4.  **Tier Especializado:** Enrutar a APIs de literatura y ciencia si el *intent* de la mision es de deep tech o academico.

## Siguiente Decision

El proximo build tecnico de research en Oli deberia implementar `Crawl4AI` si priorizamos la infraestructura local open-source, o `Firecrawl`/`Tavily` si priorizamos integracion rapida y calidad imediata de output. Recomendaria construir un adapter comun (ej. `WebResearchAdapter`) que permita hacer swap entre ellas.
