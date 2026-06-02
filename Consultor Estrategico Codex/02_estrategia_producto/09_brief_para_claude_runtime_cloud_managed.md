# Brief para Claude Code: canonizar Oli como Managed Cloud Runtime

Fecha: 2026-05-30  
Autor: Codex como consultor estrategico  
Objetivo: explicar la vision correcta del founder para que Claude Code pueda editar el TDD sin mezclar arquitecturas.

---

## 1. Tesis que debe quedar clara

Oli no debe depender de que el usuario tenga una GPU local, instale Qwen, instale Ollama, se conecte por SSH a una GPU alquilada, ni entienda terminal.

La experiencia objetivo es:

> El usuario le pide algo a Oli. Oli trabaja en background usando infraestructura administrada por Oli: modelos open source en GPU cloud, sandboxes remotos, browser automation, repos, terminal, archivos, APIs y conectores. El usuario solo ve progreso, decisiones, aprobaciones y resultados.

En otras palabras:

- El usuario no compra hardware para usar Oli.
- El usuario no instala modelos locales por defecto.
- El usuario no administra RunPod, Vast, Lambda, Modal, E2B o Daytona.
- El usuario no debe saber si Oli uso Qwen, Llama, GPT, Claude, vLLM, SGLang u otra capa.
- Oli si puede usar modelos open source, pero corriendo en infraestructura de Oli.
- El runtime local debe ser un modo opcional, no la arquitectura principal.

---

## 2. Lo que esta mezclado hoy en el TDD

El TDD ya contiene la idea correcta, pero esta dispersa y mezclada con una tesis local-first.

### Documentos que ya apuntan a la vision correcta

1. `tdd/adrs/ADR-016-model-routing-gpu-strategy.md`

   Este ADR dice que Oli alquila GPU on-demand cuando hay trabajo, que la GPU se enciende por mision, que el usuario paga suscripcion y que el scheduling es invisible.

   Esto es correcto, pero debe evitar frases ambiguas como:

   - "modelo local"
   - "GPU del usuario"
   - "modelos que Oli descarga via Ollama segun tier de GPU del usuario"

   Esas frases hacen parecer que el usuario final debe tener o administrar la GPU.

2. `tdd/domain/setup-wizard-spec.md`

   Tiene un Perfil D de GPU Cloud asignada por Oli. Esto es correcto y deberia ser el perfil default del producto SaaS.

   Problema: los perfiles A, B y C parecen la experiencia principal, como si Oli primero detectara hardware local del usuario. Eso debe pasar a modo avanzado/dev/privacy.

3. `tdd/adrs/ADR-002-execution-sandbox.md`

   Dice explicitamente que el deployment corre en nuestra infraestructura y que el sandbox tambien corre en nuestros servidores. Esta es la base correcta.

4. `tdd/adrs/ADR-012-desktop-execution-strategy.md`

   Tiene la idea de E2B/Daytona como Linux completo para ejecutar comandos, instalar herramientas, clonar repos, correr tests y automatizar tareas. Esto es correcto.

   Problema: mezcla `subprocess local` y herramientas locales como si fueran el camino principal V1-V2. Eso debe quedar como modo puente o dev, no como promesa principal del SaaS.

5. `tdd/domain/connectivity-map.md`

   Contiene `linux_shell / E2B`, filesystem, browser, APIs y conectores. Esto encaja con el producto: Oli actua sobre el mundo digital desde un runtime remoto controlado.

---

## 3. Arquitectura canonica deseada

La arquitectura principal debe ser:

```text
Usuario
  -> Oli App / Web / Desktop Bridge ligero
  -> Mission Orchestrator
  -> Policy + Permission Engine
  -> Managed Cloud Runtime
       - Remote workspace por usuario/tenant/mision
       - GPU on-demand administrada por Oli
       - Model serving OpenAI-compatible
       - Sandbox Linux para comandos, builds y tests
       - Browser automation
       - Tool/connectors layer
       - Artifact store
       - Audit log
  -> Resultados, aprobaciones y trazabilidad para el usuario
```

El "modelo local" debe interpretarse como:

> modelo open source administrado por Oli en una GPU cloud asignada por tier/tenant/mision.

No debe interpretarse como:

> modelo instalado en el computador personal del usuario.

---

## 4. Modos de deployment que deben quedar ordenados

El TDD deberia distinguir cuatro modos, en este orden de prioridad:

### Modo 1: Oli Managed Cloud Runtime

Este es el default comercial.

- Oli administra GPU, modelos, sandboxes, browser automation y workers.
- Usuario no instala nada pesado.
- Ideal para founders, agencias, consultores, operadores y usuarios no tecnicos.
- Permite trabajar en background.
- Permite cobrar suscripcion + creditos de compute.

### Modo 2: Desktop Bridge

Este es un complemento, no el core.

Sirve para:

- acceder a archivos locales autorizados por el usuario;
- abrir navegador local si hace falta;
- manejar credenciales locales con keychain;
- pedir permisos;
- sincronizar artefactos entre maquina del usuario y runtime cloud.

No debe correr el modelo grande.

### Modo 3: BYOC / Customer Cloud

Para empresas o usuarios avanzados.

- Oli puede correr en una VPC del cliente, GPU alquilada por el cliente o infraestructura dedicada.
- Mismo contrato de runtime.
- No debe cambiar la experiencia del producto.

### Modo 4: Local Dev / Power User / Privacy Mode

Modo opcional.

- Ollama local, vLLM local, Docker local o subprocess local.
- Util para desarrollo, pruebas, usuarios tecnicos y escenarios de privacidad.
- No debe ser la experiencia default.

---

## 5. Cambios de lenguaje necesarios

Claude debe reemplazar o aclarar estos terminos en el TDD:

| Lenguaje actual ambiguo | Lenguaje recomendado |
| --- | --- |
| GPU local incluida | GPU cloud administrada incluida |
| GPU del usuario | GPU asignada al tenant/tier del usuario |
| modelo local | modelo open source administrado por Oli |
| correr localmente | correr en runtime privado/administrado por Oli |
| Oli descarga modelos en la GPU del usuario | Oli provisiona modelos en el runtime cloud asignado |
| Ollama como default del usuario | Ollama solo para dev/local/privacy mode |
| local-first | cloud-managed by default, deployment-flexible |
| subprocess local V1-V2 | dev bridge / modo local controlado |

La idea no es borrar el soporte local. La idea es que no parezca el camino principal.

---

## 6. Como debe funcionar el acceso a archivos y terminal

Pregunta clave del founder:

> Si el modelo corre en una GPU alquilada, como va a ver archivos del usuario y correr comandos en terminal?

Respuesta canonica:

El modelo no ve ni toca directamente el computador del usuario. Oli separa cerebro, runtime y permisos.

### Archivos

Hay tres rutas:

1. Archivos subidos o sincronizados al workspace remoto de Oli.
2. Repos conectados por GitHub/GitLab/Bitbucket.
3. Desktop Bridge que expone archivos locales seleccionados con permisos explicitos.

### Terminal

La terminal principal es remota:

- E2B, Daytona, Modal Sandbox, Fly Machines, RunPod pod, container aislado o microVM.
- Alli Oli puede clonar repos, instalar dependencias, correr tests, ejecutar scripts y producir artefactos.

La terminal local del usuario solo se usa cuando:

- el usuario lo autoriza;
- la tarea requiere recursos locales;
- se esta en modo dev/power-user;
- se necesita abrir una app local.

### Credenciales

Las credenciales nunca deben vivir sueltas en la GPU.

Debe existir:

- credential vault;
- broker de credenciales;
- tokens efimeros;
- scope minimo;
- audit log;
- human approval para acciones sensibles.

---

## 7. Reglas de producto que deben quedar explicitas

1. Oli debe trabajar en background.
2. El usuario no debe entender infraestructura.
3. La GPU es invisible para el usuario, salvo indicadores simples como "compute disponible", "mision corriendo", "creditos usados".
4. El runtime debe ser auditable.
5. Toda accion sensible requiere aprobacion humana.
6. El sistema debe ser model-agnostic: Qwen, Llama, Mistral, GPT, Claude, Gemini, Kimi, etc.
7. La capa de modelos debe exponer una API compatible tipo OpenAI para que el orquestador no dependa del proveedor.
8. El TDD debe separar claramente:
   - experiencia del usuario;
   - runtime de ejecucion;
   - serving de modelos;
   - bridge local;
   - conectores externos;
   - politicas de permisos.

---

## 8. Archivos que Claude deberia editar o revisar

Prioridad alta:

1. `tdd/README.md`
   - Cambiar el resumen para que Managed Cloud Runtime sea la arquitectura principal.
   - Aclarar que Ollama/local es modo dev o privacy, no default comercial.

2. `tdd/adrs/ADR-016-model-routing-gpu-strategy.md`
   - Reescribir el lenguaje de "GPU del usuario" hacia "GPU asignada al tenant/tier".
   - Aclarar "modelo local" como "modelo open source en compute administrado".

3. `tdd/domain/setup-wizard-spec.md`
   - Convertir Perfil D en default SaaS.
   - Mover perfiles A/B/C a "advanced/local/privacy modes".

4. `tdd/adrs/ADR-012-desktop-execution-strategy.md`
   - Aclarar que Desktop Bridge no es el runtime pesado.
   - Reforzar E2B/Daytona/remote Linux como terminal principal para background work.

5. `tdd/stack/stack-decision.md`
   - Reordenar stack alrededor de Managed Cloud Runtime.
   - Dejar Ollama como dev/local mode y vLLM/SGLang/LocalAI como produccion administrada.

Prioridad media:

6. `tdd/domain/connectivity-map.md`
   - Aclarar que las conexiones pueden operar desde runtime cloud, con bridge local opcional.

7. `tdd/domain/pricing-model-v6.md`
   - Cambiar "GPU local" por "GPU cloud administrada".

8. `tdd/domain/market-research-2026-05-27.md`
   - Revisar comparaciones que dicen "GPU local" para no vender algo equivocado.

9. `docs_extracted/oli_technical_foundation_v2/*`
   - Estos docs heredados son una fuente fuerte del sesgo local-first. Deben marcarse como legacy, reconsiderarse o reescribirse.

---

## 9. Nueva ADR recomendada

Crear:

`tdd/adrs/ADR-021-managed-cloud-runtime.md`

Titulo sugerido:

`ADR-021 — Managed Cloud Runtime como arquitectura principal de Oli`

Decision:

> Oli adopta Managed Cloud Runtime como arquitectura default para produccion. El runtime local queda como modo opcional para desarrollo, privacidad, power users o despliegues customer-managed.

Contenido minimo:

- Contexto.
- Decision.
- Arquitectura.
- Modos soportados.
- Como accede a archivos.
- Como corre comandos.
- Como sirve modelos open source.
- Como maneja credenciales.
- Como trabaja en background.
- Consecuencias.
- Alternativas rechazadas.

Alternativas rechazadas:

1. Exigir GPU local al usuario.
2. Exigir SSH manual a una GPU alquilada.
3. Correr todo en APIs premium externas.
4. Dejar que el modelo tenga acceso directo a credenciales o filesystem.
5. Usar subprocess local como runtime principal del SaaS.

---

## 10. Criterio de aceptacion para la limpieza del TDD

Despues de editar, una persona que lea el TDD debe poder responder sin duda:

1. Oli corre modelos grandes en infraestructura administrada por Oli, no en la laptop del usuario.
2. El usuario no necesita GPU local para usar el producto.
3. El trabajo pesado ocurre en un runtime remoto y aislado.
4. La app local, si existe, es un bridge de permisos/archivos/browser, no el cerebro principal.
5. Ollama local existe, pero no es la experiencia comercial default.
6. "GPU incluida" significa GPU cloud administrada, no tarjeta fisica del usuario.
7. Oli puede desarrollar software, automatizar workflows y actuar como asistente conectado a herramientas porque tiene terminal remota, browser automation, conectores y permission system.

---

## 11. Resumen ejecutivo para Claude

No conviertas Oli en una app que le pide al usuario configurar modelos locales.

El producto que Alejandro quiere es:

> Un operador AI conectado a todo, capaz de desarrollar software y automatizar trabajo digital en background, usando GPU cloud y runtime remoto administrado por Oli, con una experiencia simple para usuarios no tecnicos.

La arquitectura local-first puede seguir existiendo, pero solo como modo avanzado.

El TDD debe dejar de sonar como "instala Ollama, conecta tu GPU y corre local" y debe empezar a sonar como:

> "Oli te asigna compute, workspace y agentes. Tu solo das objetivos, permisos y aprobaciones."

