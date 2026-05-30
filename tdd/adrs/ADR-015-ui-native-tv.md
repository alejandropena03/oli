# ADR-015 — UI nativa: app de escritorio y experiencia en TV

**Estado:** accepted
**Fecha:** 2026-05-26
**Deciders:** Alejandro Peña (founder) — decisión explícita
**Contexto nuevo:** El TDD no tenía definida la capa de UI. Este ADR la establece.

---

## Contexto

La UI de Oli no es una página web. Es una **app nativa de escritorio** que vive en el computador del usuario, siempre activa en background, accesible desde el tray del sistema.

El founder también quiere ver Oli en el TV — el dashboard de misiones activas, el reporte del día, el estado del sistema en pantalla grande mientras trabaja.

---

## Decisión: Electron + Tauri como opciones, TV via casting

### App de escritorio

**Recomendación: Tauri v2 (Rust + WebView)**

| Criterio | Tauri | Electron |
|---|---|---|
| Tamaño del bundle | ~8MB | ~150MB |
| Consumo de RAM | Bajo (~30MB) | Alto (~300MB) |
| Acceso al OS | Rust nativo | Node.js |
| Keychain (credenciales) | ✅ Plugin nativo | ✅ keytar |
| Wake word / audio | ✅ Plugin Rust | ✅ Node bindings |
| Web technologies | ✅ HTML/CSS/JS | ✅ HTML/CSS/JS |
| Velocidad de dev | Media | Alta |
| Madurez 2026 | Alta (v2 estable) | Muy alta |

**Elección V0-V2: Electron** — velocidad de desarrollo, el founder es el único usuario, el overhead de RAM no importa en esta etapa.

**Elección V3+: Tauri** — cuando Oli vaya a más usuarios, el bundle size y RAM sí importan.

### Experiencia en TV

**Tres opciones según el hardware del usuario:**

```
OPCIÓN A — AirPlay (macOS → Apple TV / Smart TV compatible)
  Oli castea una "TV view" via AirPlay
  Sin app adicional en el TV
  Limitación: solo macOS, latencia variable

OPCIÓN B — Chromecast / Google Cast
  Oli expone una Cast receiver app
  Funciona desde cualquier OS
  TV view sirve como página web local

OPCIÓN C — HDMI directo (más simple, más confiable)
  Oli detecta segundo monitor (el TV conectado por HDMI)
  Lanza automáticamente la TV view como segunda pantalla
  Sin latencia, sin dependencias de red
  Recomendado para V2
```

**La TV view no es una réplica de la app desktop.** Es un dashboard de solo lectura optimizado para ver desde lejos:
- Misiones activas con estado en tiempo real
- Últimas 3 notificaciones importantes
- Métricas del día (tiempo ahorrado, costo, misiones completadas)
- El Orb de Oli en estado real (ejecutando / idle / esperando aprobación)

---

## Arquitectura de la app desktop

```
PROCESO PRINCIPAL (Electron/Tauri main process)
├── Mission Kernel (TypeScript) — el cerebro
├── Credential Vault (keytar / OS Keychain)
├── OAuth Manager (localhost:3847)
├── Voice pipeline (OpenWakeWord + Whisper)
├── MCP clients (filesystem, browser, etc.)
└── IPC Bridge → UI

PROCESO RENDERER (WebView — HTML/CSS/JS)
├── Mission List view
├── Mission Detail + Evidence Drawer
├── Memory Panel
├── Playbook Library
├── Tool Registry (qué está conectado)
├── Decision Queue (aprobaciones pendientes)
└── Settings

TRAY (background permanente)
├── Ícono con estado: activo / ejecutando / bloqueado
├── Quick mission input (Cmd+Space o wakeword)
└── Notificaciones del sistema
```

---

## Conexión app desktop → TV

```typescript
// En el proceso principal de Electron/Tauri:

class TVDisplay {
  // Detecta si hay un segundo monitor
  async detectSecondScreen(): Promise<Display | null> {
    const displays = screen.getAllDisplays()
    return displays.find(d => d.id !== screen.getPrimaryDisplay().id) || null
  }

  // Lanza la TV view en el segundo monitor
  async launchTVView(display: Display): Promise<void> {
    const tvWindow = new BrowserWindow({
      x: display.bounds.x,
      y: display.bounds.y,
      width: display.bounds.width,
      height: display.bounds.height,
      fullscreen: true,
      frame: false,
      webPreferences: { contextIsolation: true }
    })
    tvWindow.loadFile('tv-view/index.html')
  }

  // La TV view recibe updates via IPC del Mission Kernel
  pushUpdate(event: MissionEvent): void {
    tvWindow.webContents.send('mission-update', event)
  }
}
```

---

## Consecuencias

**Positivo:**
- App desktop = acceso nativo al OS Keychain, wake word, filesystem
- TV view = segundo monitor detectado automáticamente, sin configuración
- Tauri V3+ = bundle pequeño, distribuible sin Electron overhead

**Negativo:**
- Electron en V0 = bundle pesado (~150MB) — aceptable para fase de desarrollo
- TV via HDMI requiere que el TV esté físicamente conectado

**Pendiente para V3:**
- Chromecast receiver app para TV sin HDMI
- iOS/Android companion app para aprobaciones desde el celular
