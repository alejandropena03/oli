# 00 - Technical Thesis

## One-line thesis

Oli es el supervisor de ejecución digital que convierte intención humana en trabajo terminado, validado y auditable — coordinando modelos locales, agentes externos, herramientas, memoria y permisos bajo un único operador que el usuario controla.

## What makes Oli different

Oli no es un agente más que usa herramientas. Es el supervisor que coordina agentes.

La diferencia es estructural:

```
Agente genérico:
  Usuario → Agente → herramientas → respuesta

Oli:
  Usuario → Oli (supervisor)
               ├── Claude Code    (herramienta delegada)
               ├── Codex          (herramienta delegada)
               ├── Browser Use    (herramienta delegada)
               ├── Local models   (herramienta delegada)
               ├── Sandbox exec   (herramienta delegada)
               └── Memoria persistente encima de todos ellos
```

Oli recuerda lo que Claude Code hizo el mes pasado. Sabe qué funcionó. Convierte ese conocimiento en playbooks. Maneja los permisos. Captura la evidencia. Y le presenta al usuario solo lo que importa.

Un sistema de ejecución persistente es más difícil de copiar cuando compone sobre:

- Oli como supervisor/orquestador — no como agente terminal
- Claude Code, Codex, Browser Use como herramientas bajo el control de Oli
- Memoria operacional con procedencia, outcomes y correcciones
- Mission Replay — cada misión es una caja negra reproducible
- Model Registry con benchmark continuo — routing que mejora solo
- ExecutionEnvironment abstraction — sandbox intercambiable sin cambiar el kernel
- Permissioned tool use con taint tracking y prompt injection defense
- Evidence capture por misión — audit trail completo
- Playbooks que mejoran con cada ejecución
- Oli solution bank — soluciones generalizadas que mejoran el sistema globalmente
- GPU on-demand gestionada — el usuario tiene "su compute" sin administrar infra

Oli's moat is not one model. The model will change. The moat is the supervision layer around all models and agents.

## The strategic correction

External critiques are right if Oli is interpreted as:

> another AI assistant with a dashboard.

That version loses.

The stronger version is:

> a user-owned execution system where Oli orchestrates models, tools, memory, permissions, validation, and workflows across the user's actual digital environment.

This is not just a better UI. It is an operating layer.

## Productized local-first

The old Jarvis stack was optimized for the founder's own machine and workflow. Oli must generalize that without losing the advantage.

The correct product move is:

1. Let each user choose their deployment profile.
2. Let each user choose or approve their model stack.
3. Let Oli inspect hardware and recommend the best setup.
4. Let Oli install and benchmark local models when allowed.
5. Use premium models only when policy, quality, and value justify it.
6. Keep the experience simple: the user speaks to Oli, not to a model picker.

## Why this can beat premium-only agents

Premium-only agents pay high marginal cost for every meaningful unit of work and often require sending data to external providers.

Oli can be better for certain users because it can:

- run many routine tasks locally
- protect sensitive data by default
- use premium calls surgically
- learn from the user's actual operating environment
- run scripts, tests, browsers, APIs, and file operations on user-owned infrastructure
- maintain persistent memory and playbooks under user control

## The actual hard problem

The hard problem is not generating text. The hard problem is not even using tools.

The hard problem is:

> ¿Puede Oli coordinar de forma segura y confiable múltiples agentes y herramientas, terminar trabajo valioso, probar lo que hizo, recordar lo que importa, mejorar el próximo run, proteger los datos del usuario y hacer todo eso sin que el usuario tenga que microgestionar cada paso?

Everything in the architecture should serve that.

## First sale criterion

El primer criterio de venta no es "automatiza workflows".

Es: **"Oli coordina ejecución digital compleja con memoria y evidencia."**

La diferencia importa: automatizar es mecánico y pasivo. Coordinar con memoria y evidencia es activo, supervisor, y genera confianza para delegar trabajo de mayor valor.

## Strategic ICP stance

Founder/builders and small teams are still valid.

The mistake is not targeting founders. The mistake would be targeting generic founders.

Correct staged ICP:

- V1: Oli's own company and founder workflow.
- V2-V3: AI-first founders/operators with high digital workload and strong feedback quality.
- V4: small teams, agencies, and operational leads with repeated workflows.
- V5: paid private release for founders/operators/teams where mission classes have measurable ROI.
- Later: operations teams in 50-500 person companies once security, onboarding, and integrations are robust.

## Core product promise

**De intención a trabajo terminado.**

Expanded:

> Oli understands the mission, selects the tools and models, executes safely, validates the result, records evidence, updates memory, and reports only what matters.
