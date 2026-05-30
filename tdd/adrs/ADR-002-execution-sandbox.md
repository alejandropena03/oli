# ADR-002 — Estrategia de sandbox de ejecución

**Estado:** accepted — v2 actualizado 2026-05-27
**Fecha original:** 2026-05-26
**Deciders:** Alejandro Peña (founder)

---

## Contexto

Oli necesita ejecutar acciones reales: correr scripts, manipular archivos, llamar APIs, automatizar browsers. El deployment corre en nuestra infraestructura (no en hardware del usuario), lo que significa que el sandbox de ejecución también corre en nuestros servidores.

El estándar del ecosistema se está moviendo hacia sandboxes dedicados con aislamiento fuerte: E2B, Modal Sandboxes, microVMs (gVisor, Firecracker), runtimes controlados. Docker solo no es suficiente para ejecutar código de agentes con confianza en producción.

La decisión correcta no es elegir un proveedor de sandbox hoy para siempre — es definir la abstracción `ExecutionEnvironment` que permita intercambiar el backend sin cambiar el contrato.

---

## Decisión

**Abstracción `ExecutionEnvironment` con backends intercambiables:**

```python
class ExecutionEnvironment(Protocol):
    """
    Contrato que todo backend de sandbox debe cumplir.
    Oli nunca habla directamente a Docker/E2B/Modal — habla a esta interfaz.
    """
    async def run(self, request: ExecutionRequest) -> ExecutionResult: ...
    async def health(self) -> HealthStatus: ...
    async def cleanup(self, session_id: str) -> None: ...
```

**Backends por versión:**

| Versión | Backend | Justificación |
|---|---|---|
| V0 | `MockExecutionEnvironment` | Valida arquitectura sin ejecutar nada real |
| V1-V2 | `DockerSandboxEnvironment` | Suficiente para validar flujo completo en nuestra infra |
| V3 | `E2BEnvironment` o `ModalEnvironment` | Aislamiento fuerte, Linux persistente por sesión, herramientas preinstaladas |
| V4+ | Selección dinámica por misión | Rutear según risk_class, duración esperada, tipo de tarea |

---

## Backends en detalle

### DockerSandboxEnvironment (V1-V2)

Suficiente para empezar porque:
- Corre en nuestra infra (no en la máquina del usuario)
- Aislamiento por contenedor por misión
- Sin host filesystem, sin red por defecto, sin Docker socket

Requisitos mínimos:
- Imagen base read-only
- Workspace mount efímero por misión
- CPU/RAM/tiempo limitados
- Captura stdout/stderr como artefactos
- Sin acceso a red salvo policy explícita

Limitación real: Docker no es microVM. Un proceso con suficientes permisos puede escapar del container. Aceptable en V1-V2 con política restrictiva. No aceptable para código arbitrario de usuario en V3+.

### E2BEnvironment (V3+)

E2B (e2b.dev) provee sandboxes Linux con:
- Aislamiento fuerte (microVM por sesión)
- SDK Python nativo
- Filesystem persistente por sesión (el "Linux del usuario" que acumula herramientas)
- Soporte para cualquier lenguaje, cualquier CLI
- Browser headless sin display
- API de archivos, procesos, terminal

Por qué E2B sobre Modal para este caso:
- Modal es superior para workloads de ML/compute intensivo
- E2B está diseñado específicamente para ejecutar código de agentes
- SDK Python más simple para el caso de Oli

### ModalEnvironment (alternativa para V3+)

Mejor opción cuando:
- La misión requiere GPU (ML, inference, procesamiento de imágenes)
- El workload necesita escalar horizontalmente
- Se requiere paralelismo real entre tareas de una misión

### Selección dinámica (V4+)

```python
def select_environment(request: ExecutionRequest) -> ExecutionEnvironmentBackend:
    if request.requires_gpu:
        return ModalEnvironment
    if request.risk_class >= RiskClass.SENSITIVE_EXTERNAL_READ:
        return E2BEnvironment  # microVM siempre para código de riesgo
    if request.estimated_duration_seconds < 30:
        return DockerSandboxEnvironment  # Docker para tasks cortas y simples
    return E2BEnvironment  # default para el resto
```

---

## Contrato de ExecutionRequest / ExecutionResult

```python
@dataclass
class ExecutionRequest:
    mission_id: str
    task_id: str
    objective: str
    workspace_id: str
    inputs: list[ArtifactRef]
    model_policy: ModelPolicy
    tool_policy: ToolPolicy
    expected_outputs: list[str]
    timeout_seconds: int = 600
    requires_gpu: bool = False
    risk_class: RiskClass = RiskClass.LOCAL_REVERSIBLE

@dataclass
class ExecutionResult:
    mission_id: str
    task_id: str
    status: Literal["succeeded", "failed", "partial", "timeout"]
    summary: str
    artifacts: list[ArtifactRef]
    tool_calls: list[ToolCallRecord]
    model_calls: list[ModelCallRecord]
    evidence: list[EvidenceRef]
    errors: list[ErrorRecord]
    recommendations: list[str]
    solution_derivable: bool = False  # flag para Oli solution bank
```

---

## Reglas inamovibles del sandbox

- El LLM nunca ejecuta código directamente — siempre pasa por `ExecutionEnvironment`
- Cada misión tiene su propio workspace aislado — sin acceso cross-mission
- Las credenciales nunca entran al sandbox — el credential broker las inyecta como env vars efímeras con scope mínimo
- Todo output es capturado como artefacto antes de salir del sandbox
- El sandbox no puede escribir memoria de Oli directamente — retorna `ExecutionResult` y Oli decide qué recordar

---

## Consecuencias

- V0 puede construirse sin Docker real — el Mock valida toda la arquitectura
- V1-V2 con Docker en nuestra infra es suficiente para usuarios reales
- V3+ la abstracción permite migrar a E2B/Modal sin cambiar el Mission Kernel ni el Orchestrator
- `solution_derivable` en `ExecutionResult` alimenta el Oli solution bank (ADR-019)

---

## Alternativas descartadas

| Opción | Por qué no |
|---|---|
| subprocess directo | Sin aislamiento. Inaceptable para código de agentes en producción |
| Cloud VM dedicada por usuario | Costo prohibitivo. GPU on-demand resuelve el mismo problema mejor |
| WebAssembly sandbox | Limitado a WASM. No sirve para código Python/Node/shell arbitrario |
| Sin sandbox (confiar en el LLM) | No. Jamás. El LLM se equivoca y puede ser manipulado |
