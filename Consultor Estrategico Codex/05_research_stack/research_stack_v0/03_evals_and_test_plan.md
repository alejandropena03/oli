# 03 - Evals and Test Plan

## Por que evals

Si no probamos el research, Oli va a parecer inteligente pero perdera cosas obvias.

El fallo Hermes/OpenRouter Apps debe convertirse en fixture:

> Si el research de agentes no encuentra OpenRouter Apps y Hermes, falla.

## Eval 1 - Agent usage discovery

Pregunta:

```text
Que agentes AI/open-source/developer agents tienen uso real alto actualmente?
```

Debe consultar:

- OpenRouter Apps;
- GitHub;
- official docs;
- al menos una fuente secundaria para contexto.

Debe encontrar:

- Hermes;
- OpenClaw;
- Kilo Code;
- Claude Code;
- OpenCode o equivalente;
- limitacion del ranking de OpenRouter Apps.

## Eval 2 - Coding delegate choice

Pregunta:

```text
Que conviene para Oli: Claude Agent SDK, OpenCode o Kilo?
```

Debe responder:

- Claude Agent SDK como delegate premium;
- OpenCode como pattern/local delegate candidato;
- Kilo como benchmark workflow/team;
- Mission Black Box obligatorio;
- PermissionClass obligatorio;
- no vendor lock-in.

## Eval 3 - Model selection for GPU tier

Pregunta:

```text
Que modelo open-weight conviene instalar para una GPU de 24GB/48GB/80GB?
```

Debe consultar:

- OpenRouter Models;
- Hugging Face;
- Artificial Analysis o benchmark equivalente;
- model cards;
- vLLM/Ollama docs;
- TDD ADR-016.

Debe responder:

- no lista fija permanente;
- modelos candidatos;
- VRAM/context/license;
- benchmark local requerido;
- fallback API cuando aplica.

## Eval 4 - Security risk for multi-channel agents

Pregunta:

```text
Que riesgos tiene un agente multi-channel con tools, memoria y plugins?
```

Debe encontrar:

- prompt injection;
- SSRF/network abuse;
- credential leakage;
- plugin/skill poisoning;
- memory poisoning;
- supply-chain risk;
- command execution risk;
- approval bypass.

Debe conectar a:

- ADR-020 Tool Security;
- permission classes;
- credential broker;
- evidence/audit.

## Eval 5 - TDD conflict detection

Pregunta:

```text
El TDD dice X, pero el estado actual del mercado dice Y. Que hacemos?
```

Debe:

- citar TDD;
- citar fuente actual;
- explicar tradeoff;
- recomendar actualizar TDD o mantenerlo;
- proponer recheck date.

## Scoring

| Dimension | Peso |
|---|---:|
| Encuentra fuentes correctas | 25% |
| Usa fuentes primarias | 20% |
| Separa hecho/inferencia | 15% |
| Valida contra TDD/memoria | 15% |
| Recomendacion accionable | 15% |
| Marca limitaciones/recheck | 10% |

Threshold:

```text
>= 85: usable
70-84: necesita revision humana
< 70: falla
```

