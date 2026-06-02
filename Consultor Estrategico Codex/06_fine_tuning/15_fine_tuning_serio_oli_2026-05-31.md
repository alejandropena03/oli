# Fine-tuning serio para Oli

Fecha: 2026-05-31
Rol: Codex como consultor estrategico/auditor

## Veredicto

Oli no debe hacer fine-tuning como feature generica ni como promesa de "modelo personalizado" para vender humo.

Pero tampoco debe reducirse a un lab publico. Esa fue una inferencia demasiado estrecha.

Fine-tuning debe analizarse en tres planos distintos:

1. **Oli Core privado**: como mecanismo de aprendizaje acumulado del sistema, conectado a mission traces, evals, playbooks, model routing y solution bank.
2. **Oli Runtime por usuario/equipo**: como posible especializacion controlada dentro del boundary del tenant, solo si hay derechos de datos, utilidad medible y aislamiento.
3. **Oli Labs publico**: como demostracion reproducible y sanitizada de post-training, sin regalar el core.

Fine-tuning si tiene sentido para Oli en tres casos operacionales:

1. Enseñar comportamientos operacionales repetibles que prompts largos no estabilizan.
2. Reducir costo/latencia en tareas frecuentes con formato estable.
3. Demostrar en Oli Labs una pipeline seria de post-training: dataset, baseline, SFT/LoRA, preference tuning si aplica, evals antes/despues, serving y model registry.

No tiene sentido para meter conocimiento privado cambiante del usuario. Eso debe vivir primero en memoria, RAG, traces, playbooks y permisos.

## Correccion de marco

La pregunta correcta no es:

```text
Que lab publico hacemos?
```

La pregunta correcta es:

```text
Que partes del sistema Oli deben mejorar por post-training,
que partes deben mejorar por memoria/RAG/playbooks/router,
y que parte podemos mostrar publicamente sin exponer el moat?
```

El lab publico es una consecuencia, no el centro.

## Fine-tuning dentro del TDD de Oli

El TDD ya tiene piezas que apuntan naturalmente a post-training:

- `Mission Kernel`: produce estados, eventos, errores, approvals y outcomes.
- `Mission Black Box / Mission Replay`: permite convertir ejecucion en ejemplos evaluables.
- `ValidationSuboperator`: produce señales de exito/fallo.
- `MemoryCuratorSuboperator`: decide que se recuerda.
- `PlaybookEngine`: detecta patrones repetibles.
- `Model Router`: decide cuando un modelo/adaptador conviene para una tarea.
- `Oli-to-Oli solution bank`: acumula soluciones generalizadas sin contenido privado.
- `Dedicated Oli Runtime`: crea boundaries de tenant/runtime para serving y aislamiento.

Fine-tuning serio debe colgar de esas piezas. Si se entrena fuera de ese loop, es teatro.

Arquitectura logica:

```text
Mission executed
  -> trace + evidence + validation
  -> error analysis + user feedback
  -> memory/playbook/router updates
  -> candidate training examples
  -> data rights/privacy filter
  -> eval gate
  -> SFT/LoRA or preference tuning
  -> model registry
  -> Model Router can select adapter
  -> future missions cheaper/safer/more consistent
```

## Tipos de aprendizaje en Oli

### 1. Prompt/config learning

Cambios en prompts, policies, thresholds, validators o routing.

Debe ser la primera capa. Barata, reversible, facil de evaluar.

### 2. Memory/RAG learning

Conocimiento del usuario, empresa, proyectos, decisiones, documentos y preferencias.

Debe ser la capa principal para informacion privada, temporal o cambiante.

### 3. Playbook learning

Una mision repetida se convierte en workflow parametrizable.

Este probablemente sera el aprendizaje mas valioso comercialmente antes del fine-tuning.

### 4. Router learning

Oli aprende que modelo/adaptador funciona mejor por mission class, riesgo, costo, tenant y privacidad.

Esto puede mejorar mucho sin tocar pesos.

### 5. Post-training / fine-tuning

Se justifica cuando una conducta estable se repite en muchas misiones y los datos pasan filtros de calidad/derechos.

Debe ser la ultima capa, no la primera.

## Fine-tuning privado vs publico

### Private Oli Core

Puede usar ejemplos derivados de:

- estructuras de misiones;
- tool call patterns;
- permission labels;
- validation outcomes;
- generalized solution bank;
- synthetic traces basadas en patrones reales;
- preferencias humanas anonimizadas si existe consentimiento y politica.

No debe usar por defecto:

- documentos privados;
- texto de clientes;
- correos;
- Slack/Notion/Drive raw content;
- artefactos externos con licencia dudosa;
- resúmenes derivados de contenido privado si pueden reconstruir informacion sensible.

### Per-tenant / per-org adaptation

Es teoricamente posible, pero no debe ser V0-V2.

Solo tiene sentido para clientes Team/Enterprise cuando:

- hay consentimiento explicito;
- el adapter queda aislado por tenant;
- hay derecho de borrado/export;
- hay evals contra regresiones;
- existe rollback;
- el beneficio supera memoria/playbooks.

Para la mayoria de organizaciones pequenas, memoria + playbooks + prompts + router sera suficiente por bastante tiempo.

### Public Oli Labs

Debe probar la capacidad tecnica con:

- datos sinteticos;
- schemas reducidos;
- tareas compatibles con Oli pero no identicas al core;
- reportes antes/despues;
- failure analysis honesto.

Labs no son el producto. Son evidencia.

## Regla de decision

Antes de fine-tunear cualquier cosa, Oli debe pasar este filtro:

```text
Si el problema es conocimiento factual cambiante -> RAG/memoria.
Si el problema es formato o estilo simple -> prompt/template/evals.
Si el problema es seleccion de modelo/costo -> model router.
Si el problema es conducta repetible y medible -> considerar fine-tuning.
Si el problema requiere aprender de preferencias comparativas -> DPO/ORPO/GRPO solo despues de SFT y evals.
```

## Tareas de Oli que si justifican fine-tuning

### 0. Behavioral alignment / Oli voice and operating style

Entrada: solicitud del usuario + contexto de mision + memoria relevante + restricciones.

Salida: respuesta o plan con la conducta correcta de Oli: directo, critico, ejecutivo, audit-ready, con ruta visible cuando hay impacto, sin fluff, sin exceso de preguntas y con buen gusto.

Este es el punto que no debe confundirse con "personalidad decorativa".

Hay tres capas distintas:

1. **Tono superficial**
   - Como suena Oli.
   - Ejemplos: no decir "con gusto", no sonar corporativo, ser directo, humor seco ocasional.
   - Mejor primera herramienta: system prompt + microcopy + style evals.
   - Fine-tuning: solo despues de tener muchas respuestas buenas/malas y un test set de tono.

2. **Comportamiento operacional**
   - Como decide Oli si pregunta, investiga, ejecuta, frena, propone alternativa o pide aprobacion.
   - Esto es mas importante que el tono.
   - Ejemplos: investigar antes de preguntar, mostrar ruta antes de clase 3, reportar fallos sin ocultarlos, proponer playbook si detecta repeticion.
   - Mejor primera herramienta: policies + orchestrator + eval harness.
   - Fine-tuning: si el modelo base incumple estos patrones de forma repetida aun con buen prompt.

3. **Calidad de escritura/deliverables**
   - Como redacta specs, reportes, memos, briefs, outreach, summaries y decision logs.
   - Esto puede justificar fine-tuning antes que la "voz general", porque es medible por formato, claridad, utilidad y preferencias humanas.
   - Ejemplo: founder notes -> Claude Code-ready spec con estructura estable y buen criterio.

Decision:

```text
No fine-tunear "personalidad Oli" como primer paso.
Si fine-tunear comportamiento, hacerlo como behavioral adapter medido contra tareas concretas.
```

Dataset posible:

- pares de respuesta mala/buena segun Constitucion de Oli;
- ejemplos de "pregunta innecesaria" -> "investiga/ejecuta con supuesto declarado";
- ejemplos de "respuesta chatbot" -> "respuesta operador";
- ejemplos de "accion peligrosa" -> "ruta visible + aprobacion";
- ejemplos de "analisis flojo" -> "veredicto, razon, riesgo, recomendacion, siguiente decision";
- ejemplos de reportes/escritura para mission classes especificas.

Metricas:

- adherence a Constitucion;
- numero de preguntas innecesarias;
- presencia de ruta visible en acciones sensibles;
- honestidad sobre incertidumbre/fallo;
- claridad del siguiente paso;
- preferencia humana;
- no degradar factualidad ni cumplimiento de permisos.

Riesgo:

Un fine-tune de voz puede enseñar al modelo a sonar como Oli mientras decide peor. Eso seria peligroso: Oli con colmillo falso.

Regla:

```text
La voz nunca puede mejorar a costa de permisos, verdad, evidencia o calidad de decision.
```

### 1. Mission brief normalization

Entrada: intencion humana desordenada, contexto parcial, restricciones.

Salida: `MissionSpec` estructurado, con objetivo, permisos, riesgos, datos requeridos, criterios de exito y plan inicial.

Por que si:
- Es una tarea frecuente.
- Tiene formato estable.
- Se puede evaluar con schemas y rubricas.
- Afecta la calidad de todo Oli.

Dataset inicial:
- 300-800 ejemplos sinteticos curados.
- 50-100 ejemplos adversariales.
- Ningun dato privado real.

Metricas:
- schema validity;
- missing-risk detection;
- permission-class accuracy;
- human preference sobre claridad del spec.

### 2. Tool-risk classifier / permission policy explainer

Entrada: accion propuesta por un agente o tool call.

Salida: clase de permiso, razon, datos sensibles involucrados, si requiere aprobacion humana, y texto explicable al usuario.

Por que si:
- Es core de Oli.
- Es pequeno y evaluable.
- Tiene valor de seguridad real.
- Puede convertirse en lab publico sin revelar el core.

Dataset inicial:
- 500-1500 casos de acciones digitales: leer, escribir, enviar, comprar, borrar, publicar, contactar, ejecutar comandos, mover archivos.
- Etiquetas por politica Oli.
- Casos limite: consentimiento ambiguo, tool injection, acciones encadenadas.

Metricas:
- accuracy por clase;
- false negative rate en clases 3/4;
- calibration: cuando debe decir "no se";
- explicacion correcta.

### 3. Mission trace summarizer / black box report

Entrada: eventos, evidence refs, tool calls, decisiones de routing, approvals.

Salida: reporte corto y auditable: que paso, que se uso, que quedo pendiente, riesgos, costo estimado.

Por que si:
- Es repetitivo.
- Tiene estructura estable.
- Reduce costo frente a modelos grandes.
- Demuestra el moat de Oli: supervision y evidencia.

Dataset inicial:
- Traces sinteticas generadas desde misiones V0/V1.
- Pares trace -> report curados.
- Casos con errores, bloqueos y aprobaciones.

Metricas:
- factual consistency contra trace;
- omission rate de eventos criticos;
- costo/latencia;
- preferencia humana.

### 4. Playbook candidate detector

Entrada: mision completada + trace + outcome.

Salida: si merece convertirse en playbook, por que, que parametros abstraer, que partes requieren aprobacion.

Por que si:
- Conecta fine-tuning con aprendizaje acumulado de Oli.
- Es diferenciador: convierte ejecucion repetida en activo operacional.
- Se puede evaluar con casos sinteticos y decision labels.

No debe ser el primer fine-tune. Mejor despues de tener traces reales o simuladas robustas.

## Tareas que NO deben ir a fine-tuning por ahora

### Conocimiento del usuario

No entrenar modelos con correos, documentos, Notion, Drive, Slack o historiales privados del usuario.

Razon:
- Riesgo legal/privacidad alto.
- Conocimiento cambia.
- El valor se captura mejor en memoria gobernada + RAG + permisos.

### Research state-of-the-art

No fine-tunear para "saber lo ultimo".

Razon:
- Se vuelve obsoleto.
- Requiere browsing, fuentes, ranking y decision memos.
- Debe vivir en un research protocol con citas y verificadores.

### Personalidad general de Oli

No fine-tunear "para que suene como Oli" en la primera etapa.

Razon:
- Es dificil de medir.
- Puede sobreajustar estilo y empeorar razonamiento.
- Se resuelve primero con prompt constitution + evals de tono.

### Multi-agent planning completo

No intentar fine-tunear "el cerebro entero de Oli".

Razon:
- Demasiado amplio.
- Difícil aislar mejora.
- Mejor dividir en clasificadores, normalizadores, summarizers y validators.

## Pipeline serio recomendado

### Fase 0: Evals primero

No hay fine-tuning serio sin baseline.

Crear un harness que compare:
- modelo base pequeño;
- modelo grande via API como juez/teacher;
- prompt actual;
- fine-tune candidato.

Artefactos:
- dataset versionado;
- eval runner;
- reporte markdown/json;
- trazabilidad de prompts;
- matriz de errores.

### Fase 1: SFT con LoRA/QLoRA

Primer experimento recomendado:

```text
Task: tool-risk classifier / permission policy explainer
Method: SFT con LoRA o QLoRA
Base model: instruct open-weight pequeño/mediano
Dataset: 500-1500 ejemplos
Target: mayor recall en acciones peligrosas y explicacion consistente
Serving: vLLM con LoRA adapter
```

Por que esta tarea primero:
- Tiene impacto core.
- Es evaluable.
- No necesita datos privados.
- Permite demostrar seguridad, no solo "chat bonito".

### Fase 2: Preference tuning solo si hay pares

Usar DPO/ORPO/GRPO solo cuando existan comparaciones buenas:

```text
prompt/context + respuesta A + respuesta B + preferencia + razon
```

No inventar DPO antes de tener errores reales del SFT.

### Fase 3: Registry y serving

Cada adapter debe tener ficha:
- base model;
- dataset version;
- method;
- hyperparameters;
- eval deltas;
- known failures;
- allowed tasks;
- privacy class;
- serving target;
- rollback path.

Oli no debe cargar un adapter porque "existe"; debe cargarlo porque el Model Router decide que mejora una tarea concreta.

## Stack recomendado

### Entrenamiento

- Unsloth para el primer LoRA/QLoRA por velocidad y accesibilidad.
- Hugging Face TRL para SFT/DPO/GRPO cuando el lab madure.
- Weights & Biases o MLflow para tracking si se quiere mostrar seriedad publica.

### Serving

- vLLM como ruta canonica para servir base model + LoRA adapters.
- OpenAI-compatible API para integrarlo con el Model Router actual.
- No Ollama como runtime canonico de produccion; puede quedar para dev local simple.

### Datos

- JSONL versionado.
- Splits fijos: train/validation/test.
- Test set congelado y no usado para generar datos.
- Dataset card con licencia, origen, riesgos y limitaciones.

## Oli Labs: lab publico recomendado

Nombre tentativo:

```text
oli-labs-post-training-permission-policy
```

Objetivo:

Demostrar que Alejandro sabe construir una pipeline seria de post-training aplicada a agentes seguros:

1. Dataset sintetico y curado de acciones digitales.
2. Baseline con modelo instruct.
3. SFT LoRA/QLoRA.
4. Evals antes/despues.
5. Error analysis.
6. Serving con vLLM LoRA.
7. Integracion conceptual con Model Router.

No revelar:
- Oli Core privado.
- prompts internos finales;
- datos de usuarios;
- playbooks comerciales completos.

## Criterio de exito

El primer fine-tune serio es exitoso si logra:

- Mejorar una metrica core frente al modelo base.
- Reducir costo/latencia o tamaño de prompt.
- Mantener o mejorar seguridad en casos adversariales.
- Producir un reporte reproducible.
- Servirse como adapter enrutable.
- Documentar claramente donde falla.

Si no mejora el baseline, tambien sirve, pero solo si el lab muestra honestamente por que fine-tuning no era la tecnica correcta.

## Riesgos

1. Sobreajuste a datasets sinteticos bonitos.
2. Confundir estilo consistente con mejor decision.
3. Usar jueces LLM sin test humano ni checks deterministas.
4. Entrenar conocimiento que deberia estar en RAG.
5. Publicar demasiado del core.
6. No tener infraestructura de evals y aun asi declarar victoria.

## Recomendacion

El primer experimento no debe ser "Oli personality model".

Debe ser:

```text
Permission Policy Adapter:
un modelo/adaptador que clasifica y explica riesgo de acciones digitales para agentes.
```

Este es el mejor balance entre:
- valor real para Oli;
- demostracion tecnica;
- seguridad;
- dataset publico/sanitizado;
- evaluabilidad;
- conexion con Model Router y Dedicated Oli Runtime.

## Siguiente decision

Elegir el alcance del primer lab:

```text
A. Permission Policy Adapter
B. MissionSpec Normalizer
C. Mission Trace Summarizer
```

Mi recomendacion es A.
