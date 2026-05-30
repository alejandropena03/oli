# ADR-014 — Auth y credenciales: arquitectura completa

**Estado:** accepted
**Fecha:** 2026-05-26
**Deciders:** Alejandro Peña (founder) — decisión explícita
**Principio:** El LLM nunca ve credenciales. Oli maneja todo por detrás. El usuario conecta una vez.

---

## Contexto

Oli necesita conectarse a docenas de servicios (Notion, Slack, GitHub, Gmail, etc.)
en nombre del usuario. El problema tiene 3 dimensiones:

1. **Seguridad** — las credenciales no pueden estar en el contexto del LLM
   (un prompt injection attack las robaría)
2. **Experiencia** — el usuario no debe configurar tokens manualmente
   (especialmente el founder no técnico)
3. **Ciclo de vida** — los tokens OAuth expiran, se rotan, se revocan.
   Alguien tiene que manejar eso automáticamente

**La visión del founder:** Oli hace el onboarding por detrás. El usuario le dice qué conectar,
Oli lo resuelve. Sin tokens visibles, sin configuración manual, sin fricción.

---

## El patrón correcto: Brokered Credentials

El principio más importante de la industria en 2026:

> **El LLM decide QUÉ hacer. El broker maneja el CÓMO.**
> **El LLM nunca ve el token. Nunca.**

```
❌ MAL — el LLM tiene la credencial:
   Oli (LLM): "voy a usar el token sk-xxx para llamar a Slack"
   → Cualquier prompt injection puede robar sk-xxx

✅ BIEN — brokered credentials:
   Oli (LLM): "necesito enviar un mensaje en Slack al canal #general"
   → Credential Broker: recupera el token del vault, ejecuta el API call
   → Oli recibe solo el resultado, nunca el token
```

---

## Arquitectura: 4 capas

```
┌─────────────────────────────────────────────────────────────────┐
│  CAPA 1 — CREDENTIAL VAULT (almacenamiento seguro)             │
│  ─────────────────────────────────────────────────────────────  │
│  Guarda: tokens OAuth, API keys, refresh tokens, secrets        │
│  Cifrado: AES-256 at rest, nunca en texto plano                 │
│  Aislado del contexto del LLM: el modelo nunca accede al vault  │
│                                                                 │
│  V1-V2: archivo local cifrado (keytar del OS — macOS Keychain,  │
│          Windows Credential Manager, Linux Secret Service)      │
│  V3+:   Vault service propio (o integración con 1Password SDK,  │
│          Bitwarden Secrets, AWS Secrets Manager)                │
└────────────────────────────┬────────────────────────────────────┘
                             │ solo el broker accede
┌────────────────────────────▼────────────────────────────────────┐
│  CAPA 2 — CREDENTIAL BROKER (el intermediario)                 │
│  ─────────────────────────────────────────────────────────────  │
│  Recibe: {service: "slack", action: "send_message", params: {}} │
│  Hace:   recupera token del vault, ejecuta el API call          │
│  Retorna: resultado (nunca el token)                            │
│                                                                 │
│  Reglas:                                                        │
│  - El token nunca sale del broker                               │
│  - Toda acción se loggea con trace_id                           │
│  - Si el token expiró: refresh automático antes de ejecutar     │
│  - Si el scope es insuficiente: solicita re-autorización        │
└────────────────────────────┬────────────────────────────────────┘
                             │ solo el broker llama APIs externas
┌────────────────────────────▼────────────────────────────────────┐
│  CAPA 3 — OAUTH MANAGER (ciclo de vida de tokens)              │
│  ─────────────────────────────────────────────────────────────  │
│  Maneja:                                                        │
│  - Authorization URL generation (el link que el usuario abre)   │
│  - Callback handling (recibe el code, lo intercambia por token) │
│  - PKCE (Proof Key for Code Exchange — previene interceptación) │
│  - Refresh Token Rotation (cada refresh genera nuevo token;     │
│    el anterior se invalida inmediatamente)                      │
│  - Token expiry monitoring (refresca antes de que expire)       │
│  - Revocation (cuando el usuario desconecta un servicio)        │
└────────────────────────────┬────────────────────────────────────┘
                             │ Oli habla solo con el broker
┌────────────────────────────▼────────────────────────────────────┐
│  CAPA 4 — TOOL EXECUTION (lo que Oli usa)                      │
│  ─────────────────────────────────────────────────────────────  │
│  Oli dice: executeTool("slack_send", {channel, message})        │
│  El broker hace todo el trabajo de credenciales                 │
│  Oli recibe: {success: true, message_id: "..."}                 │
│  Oli nunca supo qué token se usó                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Cómo funciona el onboarding — Oli lo hace por detrás

### Flujo completo para el founder

```
Escenario: el founder quiere que Oli use Notion

OPCIÓN A — Oli detecta la necesidad durante una misión:
  Usuario: "Oli, guarda este resumen en mi Notion"
  Oli: "Para hacer eso necesito acceso a tu Notion.
        Te abro el link de autorización — es solo un click."
  → Oli genera la Authorization URL (OAuth PKCE flow)
  → Se abre el browser del usuario
  → Usuario hace login en Notion y aprueba el scope
  → Notion redirige a localhost:PORT/callback (servidor temporal de Oli)
  → Oli recibe el code → lo intercambia por token → guarda en vault cifrado
  → Oli: "Listo. Conecté tu Notion. ¿Continúo con la misión?"
  → Misión continúa — el founder nunca vio el token

OPCIÓN B — Onboarding inicial proactivo:
  (Primera vez que el usuario abre Oli)
  Oli: "Hola. Para funcionar bien, dime qué herramientas usas.
        ¿Cuáles de estas tienes? [Notion] [Slack] [GitHub] [Gmail] [Linear] [otras...]"
  Usuario selecciona → Oli abre los flows de autorización en secuencia
  → En 5 minutos: todo conectado, todo en el vault, Oli listo para trabajar
```

### Implementación técnica del flow OAuth

```typescript
// oauth-manager.ts

class OAuthManager {
  /**
   * Genera el link de autorización que el usuario abre.
   * PKCE incluido — previene interceptación del authorization code.
   */
  async generateAuthUrl(service: ServiceName): Promise<{
    url: string
    code_verifier: string  // guardado temporalmente para el intercambio
    state: string          // CSRF protection
  }> {
    const { code_verifier, code_challenge } = await generatePKCE()
    const state = crypto.randomUUID()

    const url = new URL(OAUTH_CONFIGS[service].auth_endpoint)
    url.searchParams.set("client_id", OAUTH_CONFIGS[service].client_id)
    url.searchParams.set("redirect_uri", "http://localhost:3847/oauth/callback")
    url.searchParams.set("scope", OAUTH_CONFIGS[service].scopes.join(" "))
    url.searchParams.set("response_type", "code")
    url.searchParams.set("code_challenge", code_challenge)
    url.searchParams.set("code_challenge_method", "S256")
    url.searchParams.set("state", state)

    return { url: url.toString(), code_verifier, state }
  }

  /**
   * Recibe el callback de OAuth y completa el intercambio.
   * Guarda el token en el vault — nunca en memoria del LLM.
   */
  async handleCallback(
    service: ServiceName,
    code: string,
    state: string,
    code_verifier: string
  ): Promise<void> {
    // Intercambia el code por access_token + refresh_token
    const tokens = await exchangeCodeForTokens(service, code, code_verifier)

    // Guarda en el vault cifrado del OS — nunca texto plano
    await credentialVault.store(service, {
      access_token: tokens.access_token,
      refresh_token: tokens.refresh_token,
      expires_at: Date.now() + tokens.expires_in * 1000,
      scope: tokens.scope,
    })
  }

  /**
   * Refresca el token automáticamente antes de que expire.
   * Refresh Token Rotation: el token viejo se invalida inmediatamente.
   */
  async ensureFreshToken(service: ServiceName): Promise<string> {
    const stored = await credentialVault.get(service)

    // Si expira en menos de 5 minutos, refrescar ahora
    if (stored.expires_at - Date.now() < 5 * 60 * 1000) {
      const fresh = await refreshToken(service, stored.refresh_token)

      // Guardar el nuevo token — el refresh_token viejo ya no sirve
      await credentialVault.store(service, {
        access_token: fresh.access_token,
        refresh_token: fresh.refresh_token,  // nuevo refresh token
        expires_at: Date.now() + fresh.expires_in * 1000,
        scope: fresh.scope,
      })

      return fresh.access_token
    }

    return stored.access_token
  }
}
```

### El Credential Broker — lo que ejecuta las API calls

```typescript
// credential-broker.ts

class CredentialBroker {
  /**
   * Punto de entrada único para toda tool call que requiere credenciales.
   * El LLM llama esto — nunca accede al vault directamente.
   */
  async execute(
    service: ServiceName,
    action: string,
    params: Record<string, unknown>,
    mission_id: string
  ): Promise<unknown> {
    // 1. Verificar que el servicio está conectado
    const isConnected = await credentialVault.has(service)
    if (!isConnected) {
      throw new CredentialError("not_connected", service)
      // → Oli detecta esto y lanza el flujo de onboarding
    }

    // 2. Obtener token fresco (refresca si está por expirar)
    const token = await oauthManager.ensureFreshToken(service)

    // 3. Ejecutar el API call — el token nunca sale de aquí
    const result = await this.callApi(service, action, params, token)

    // 4. Loggear para audit trail (sin el token, solo la acción)
    await auditLog.record({
      trace_id: crypto.randomUUID(),
      mission_id,
      service,
      action,
      params_summary: sanitize(params),  // sin datos sensibles
      outcome: result.success ? "success" : "failure",
      timestamp: new Date().toISOString(),
    })

    // 5. Retornar resultado al LLM — sin el token
    return result
  }
}
```

---

## Credential Vault — implementación por versión

### V1-V2: keytar (OS native secret storage)

```typescript
// credential-vault.ts — V1
import keytar from "keytar"  // npm install keytar

const SERVICE_NAME = "oli-credentials"

class CredentialVault {
  async store(service: string, tokens: TokenData): Promise<void> {
    // macOS: Keychain | Windows: Credential Manager | Linux: Secret Service
    await keytar.setPassword(
      SERVICE_NAME,
      service,
      JSON.stringify(tokens)  // cifrado por el OS
    )
  }

  async get(service: string): Promise<TokenData | null> {
    const raw = await keytar.getPassword(SERVICE_NAME, service)
    return raw ? JSON.parse(raw) : null
  }

  async has(service: string): Promise<boolean> {
    return (await this.get(service)) !== null
  }

  async delete(service: string): Promise<void> {
    await keytar.deletePassword(SERVICE_NAME, service)
  }

  async listConnected(): Promise<string[]> {
    const credentials = await keytar.findCredentials(SERVICE_NAME)
    return credentials.map(c => c.account)
  }
}
```

**Por qué keytar en V1:**
- Zero configuración — usa el secret store nativo del OS
- macOS Keychain: cifrado por hardware, desbloqueado con Touch ID / password del sistema
- Windows Credential Manager: mismo nivel de seguridad
- Linux: GNOME Keyring / KWallet via libsecret
- El usuario nunca ve el token — está en el OS, no en un archivo

### V3+: Vault service propio o integración

```typescript
// Opciones para V3+:

// Opción A: 1Password SDK (el usuario ya tiene 1Password)
import { createClient } from "@1password/sdk"
// → Los tokens de Oli viven en la bóveda del usuario
// → El usuario puede verlos, auditarlos, revocarlos
// → Touch ID / Face ID para desbloquear

// Opción B: Bitwarden Secrets Manager (open source, self-hosted)
// → El usuario controla su propio vault
// → API para que Oli lea/escriba secrets

// Opción C: Vault service propio (para escalar a multi-usuario)
// → Oli.app gestiona credenciales por usuario
// → Útil cuando Oli pasa de local a SaaS
```

---

## Servicios OAuth que Oli conecta y sus scopes exactos

El principio de least privilege: pedir solo los scopes que Oli realmente necesita.

```typescript
const OAUTH_CONFIGS: Record<ServiceName, OAuthConfig> = {
  notion: {
    auth_endpoint: "https://api.notion.com/v1/oauth/authorize",
    token_endpoint: "https://api.notion.com/v1/oauth/token",
    client_id: process.env.OLI_NOTION_CLIENT_ID,
    // Solo lo que Oli necesita — no scope de admin
    scopes: ["read_content", "update_content", "insert_content"],
    token_type: "oauth2",
  },
  slack: {
    auth_endpoint: "https://slack.com/oauth/v2/authorize",
    token_endpoint: "https://slack.com/api/oauth.v2.access",
    client_id: process.env.OLI_SLACK_CLIENT_ID,
    scopes: ["chat:write", "channels:read", "files:write"],
    token_type: "oauth2",
  },
  github: {
    auth_endpoint: "https://github.com/login/oauth/authorize",
    token_endpoint: "https://github.com/login/oauth/access_token",
    client_id: process.env.OLI_GITHUB_CLIENT_ID,
    // Scopes mínimos — el usuario puede otorgar más si quiere
    scopes: ["repo", "issues:write", "pull_requests:write"],
    token_type: "oauth2",
  },
  gmail: {
    auth_endpoint: "https://accounts.google.com/o/oauth2/auth",
    token_endpoint: "https://oauth2.googleapis.com/token",
    client_id: process.env.OLI_GOOGLE_CLIENT_ID,
    // Gmail: leer + enviar. NO acceso a Drive, Calendar (scope separado)
    scopes: [
      "https://www.googleapis.com/auth/gmail.readonly",
      "https://www.googleapis.com/auth/gmail.send",
    ],
    token_type: "oauth2",
  },
  google_calendar: {
    auth_endpoint: "https://accounts.google.com/o/oauth2/auth",
    token_endpoint: "https://oauth2.googleapis.com/token",
    client_id: process.env.OLI_GOOGLE_CLIENT_ID,
    scopes: ["https://www.googleapis.com/auth/calendar"],
    token_type: "oauth2",
  },
  linear: {
    auth_endpoint: "https://linear.app/oauth/authorize",
    token_endpoint: "https://api.linear.app/oauth/token",
    client_id: process.env.OLI_LINEAR_CLIENT_ID,
    scopes: ["read", "write", "issues:create"],
    token_type: "oauth2",
  },
  // API keys simples (no OAuth — el usuario pega el key una vez)
  anthropic: { token_type: "api_key" },
  openai:    { token_type: "api_key" },
  elevenlabs:{ token_type: "api_key" },
}
```

---

## Flujo de error: credencial no conectada

Cuando Oli necesita un servicio que el usuario no ha conectado:

```typescript
// En el Credential Broker:
if (!isConnected) {
  // No falla silenciosamente — genera un evento de dominio
  throw new CredentialNotConnectedError(service)
}

// El Mission Kernel captura esto:
// → Emite evento: CredentialRequired
// → Status de la misión: blocked (bloqueado por credencial faltante)
// → Oli le dice al usuario:
//   "Para continuar necesito acceso a tu {service}.
//    ¿Lo conecto ahora? [Sí, conectar] [Saltar este paso]"
// → Si el usuario dice sí: lanza el OAuth flow
// → Si el usuario dice no: el Mission Kernel busca una alternativa sin ese servicio
//   o marca el step como skipped con nota
```

---

## Lo que el usuario ve vs. lo que pasa por detrás

```
LO QUE VE EL USUARIO:
  "Para guardar en tu Notion necesito acceso. ¿Lo conecto?"
  [click] → Browser abre Notion → click "Autorizar" → browser se cierra
  "Listo. Conectado."

LO QUE PASA POR DETRÁS:
  1. OAuthManager genera URL con PKCE (code_verifier guardado temporalmente)
  2. Se abre el browser del usuario en la URL de Notion
  3. Oli levanta servidor temporal en localhost:3847/oauth/callback
  4. El usuario aprueba en Notion
  5. Notion redirige a localhost:3847/oauth/callback?code=xxx&state=yyy
  6. OAuthManager verifica state (CSRF) y code_verifier (PKCE)
  7. OAuthManager intercambia code por {access_token, refresh_token}
  8. CredentialVault.store("notion", tokens) → macOS Keychain / Windows CM / libsecret
  9. El servidor temporal se cierra
  10. Oli confirma: "Listo"

El usuario nunca vio un token. Oli nunca tuvo el token en su contexto.
```

---

## Audit trail — todo queda registrado

```typescript
// Cada tool call que usa credenciales genera una entrada de audit:
{
  trace_id: "uuid",
  mission_id: "uuid",
  timestamp: "2026-05-26T10:32:15Z",
  service: "notion",
  action: "create_page",
  params_summary: { parent_db: "Projects", title: "Resumen reunión" },
  // NUNCA: tokens, passwords, secrets
  outcome: "success",
  duration_ms: 342,
  http_status: 200,
}
```

El founder puede ver en el Evidence Drawer de cada misión exactamente qué servicios usó Oli y con qué acciones — sin ver credenciales.

---

## Resumen de decisiones

| Decisión | Elección | Razón |
|---|---|---|
| Patrón de seguridad | Brokered Credentials | El LLM nunca ve tokens — elimina prompt injection risk |
| Storage V1-V2 | keytar (OS Keychain) | Zero config, cifrado nativo del OS, cross-platform |
| Storage V3+ | 1Password SDK o Bitwarden | El usuario controla su vault, auditable |
| OAuth flow | PKCE mandatory | Previene interceptación — estándar 2026 para native apps |
| Token refresh | Automático antes de expirar | El usuario nunca tiene que re-conectar por token expirado |
| Onboarding | Oli lanza el flow cuando lo necesita | Sin configuración manual — el usuario solo da click |
| Scope | Mínimo necesario | Least privilege — si Oli solo necesita leer, no pide write |
| Revocación | El usuario puede desconectar desde Oli | Control total sin tocar el OS keychain |

---

## Referencias

- [OAuth 2.0 for AI Agents — Security Boulevard](https://securityboulevard.com/2026/05/oauth-2-0-for-ai-agents-implementation-patterns-and-best-practices/)
- [Brokered Credentials — Composio](https://composio.dev/blog/secure-ai-agent-infrastructure-guide)
- [Nango — Secure AI Agent Auth](https://nango.dev/blog/guide-to-secure-ai-agent-api-authentication/)
- [Mastra Auth Docs](https://mastra.ai/docs/server/auth)
- [PKCE RFC 7636](https://datatracker.ietf.org/doc/html/rfc7636)
