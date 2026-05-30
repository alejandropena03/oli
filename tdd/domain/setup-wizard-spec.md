# Setup Wizard Spec

**Fecha:** 2026-05-26
**Propósito:** Cómo Oli se instala, detecta hardware y configura los modelos sin que el usuario toque una terminal.
**Referencia:** 03_SETUP_WIZARD_AND_MODEL_SELECTION.md (doc fundacional)

---

## El principio

El setup de Oli debe ser tan simple como instalar una app.
El usuario no debería necesitar saber qué es Ollama, pgvector, ni Docker para empezar.
Oli hace el diagnóstico, recomienda el stack, instala lo necesario y confirma que todo funciona.

---

## Flujo del setup wizard — 5 pasos

### Paso 1 — Detección de hardware

Oli detecta automáticamente:

```python
class HardwareProfile:
    gpu_available: bool
    gpu_name: str | None          # "NVIDIA RTX 5090", "Apple M3 Max", etc.
    gpu_vram_gb: float | None
    ram_gb: float
    cpu_cores: int
    storage_available_gb: float
    os: str                       # "Ubuntu 24.04", "macOS 15", "Windows 11"
    is_cloud_vm: bool             # detecta si corre en GPU alquilada

def detect_hardware() -> HardwareProfile:
    # nvidia-smi para NVIDIA
    # system_profiler para macOS
    # /proc/cpuinfo + /proc/meminfo para Linux
    # psutil como fallback cross-platform
```

### Paso 2 — Recomendación de perfil

Basado en el hardware, Oli recomienda uno de 4 perfiles:

```
PERFIL A — GPU Potente (VRAM >= 24GB)
  Tier 1: Llama 3.1 8B o Qwen 2.5 14B (local, $0)
  Tier 2: Llama 3.1 70B quantized Q4 (local, $0)
  Tier 3: Claude Sonnet via API (solo para casos complejos)
  Embeddings: nomic-embed-text (local, $0)
  Mensaje: "Tu GPU puede correr el 85% de las misiones sin gastar en APIs."

PERFIL B — GPU Mediana (VRAM 8-23GB)
  Tier 1: Llama 3.1 8B (local, $0)
  Tier 2: Claude Haiku via API (barato)
  Tier 3: Claude Sonnet via API
  Embeddings: nomic-embed-text (local) o text-embedding-3-small (API)
  Mensaje: "Tu GPU maneja tasks simples. Para lo complejo usamos APIs de forma quirúrgica."

PERFIL C — Sin GPU / CPU only
  Tier 1: Claude Haiku via API
  Tier 2: Claude Haiku via API
  Tier 3: Claude Sonnet via API
  Embeddings: text-embedding-3-small via API
  Mensaje: "Sin GPU local, usamos APIs. El costo es más alto pero todo funciona igual."

PERFIL D — GPU Cloud (asignada por Oli en suscripción)
  Tier 1: Llama 3.1 8B en GPU cloud (incluido en suscripción)
  Tier 2: Llama 3.1 70B en GPU cloud (incluido en suscripción)
  Tier 3: Claude Sonnet via API del usuario
  Mensaje: "Tu GPU cloud ya está lista. Usamos APIs solo para lo que vale la pena."
```

### Paso 3 — Instalación

Oli instala lo necesario según el perfil:

```python
class SetupInstaller:
    def install_profile(self, profile: HardwareProfile) -> None:
        # Siempre:
        self.install_postgres()          # PostgreSQL + pgvector
        self.install_docker()            # para code sandbox
        self.run_migrations()            # schema inicial

        # Si hay GPU:
        if profile.gpu_available:
            self.install_ollama()
            self.pull_models(profile.recommended_models)
            self.benchmark_models()     # verifica que corren bien

        # Verifica todo:
        self.run_health_check()
```

**Lo que el usuario ve:**
```
Instalando Oli...
✓ Base de datos lista
✓ Sandbox de código listo
⬇ Descargando modelo Llama 3.1 8B (4.7GB)... [████████░░] 80%
✓ Modelo listo — velocidad: 45 tokens/seg en tu hardware
✓ Todo listo. Oli está configurado para tu hardware.
```

### Paso 4 — Configuración de APIs (si aplica)

Si el perfil necesita APIs:

```
Oli necesita conectarse a Claude para misiones complejas.

Puedes pegar tu API key de Anthropic aquí:
[_________________________]

No tienes una? Te la consigo → [Obtener API key]
¿Prefieres no usar APIs? Oli funcionará con modelos locales únicamente.
[Solo local] [Agregar key]
```

La key se guarda en el OS Keychain (ADR-014). Nunca en texto plano.

### Paso 5 — Primera misión de prueba

Oli ejecuta una misión de demostración para verificar que todo funciona:

```
Todo está listo. Voy a ejecutar una misión corta para verificar que funciona.

"Investiga qué es pgvector y dame un párrafo."

[Ejecutando...]
✓ Modelo local respondió en 3.2s
✓ Búsqueda semántica funcionando
✓ Evidence store guardando correctamente

Oli está listo. Tiempo total de setup: 8 minutos.
```

---

## Instalador por OS

```
macOS:
  Distribución como .dmg (Electron/Tauri app)
  El wizard corre dentro de la app
  Homebrew para dependencias de sistema si es necesario

Ubuntu/Linux:
  Script de instalación: curl -fsSL https://oli.ai/install | bash
  O .deb package
  Docker para aislamiento de componentes

Windows:
  .exe installer (NSIS o WiX)
  WSL2 para el backend Python si es necesario
  GPU: CUDA toolkit como prerequisito
```

---

## Configuración de GPU cloud (Perfil D)

Cuando el usuario está en el tier de suscripción que incluye GPU:

```
Tu suscripción incluye una GPU en la nube para Oli.

Oli la enciende automáticamente cuando tienes misiones activas
y la apaga cuando no hay trabajo. No pagas por tiempo idle.

Región asignada: us-east-1 (más cerca a tu ubicación)
GPU asignada: [según el tier]
Latencia estimada: ~180ms

[Probar la conexión]
```

El founder no ve la complejidad del RunPod/Vast.ai detrás.
Solo ve "GPU lista" o "GPU ocupada".
