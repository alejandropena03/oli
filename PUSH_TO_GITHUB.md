# Push del repo a GitHub — instrucciones

Ya dejé listo:
- `.gitignore` (excluye node_modules, dist, zips, secretos, .env)
- `README.md` raíz con estado del proyecto, stack, pricing, próximos pasos
- `REVIEW_2026-05-30.md` con el review profundo del repo

Falta el push. Mi sandbox no puede pushear (sin DNS ni tus llaves SSH), así que esto lo corrés vos.

---

## Paso 0 — Eliminar la carpeta `.git` rota

Cuando intenté hacer `git init` desde mi sandbox, los permisos del mount Windows dejaron una carpeta `.git/` a medias en `C:\Users\apenaosorio\Desktop\oli\.git`.

**Eliminala desde el Explorador de Windows:**
- Mostrar archivos ocultos (Vista → Elementos ocultos)
- Borrar la carpeta `.git`
- Vaciar la papelera (opcional)

O desde PowerShell elevada:
```powershell
Remove-Item -Recurse -Force "C:\Users\apenaosorio\Desktop\oli\.git"
```

---

## Paso 1 — Abrir terminal en la carpeta oli

PowerShell:
```powershell
cd C:\Users\apenaosorio\Desktop\oli
```

---

## Paso 2 — Verificar que GitHub esté creado y vacío

Antes de pushear, confirmá que:
- El repo `apenaosorio_meli/oli` existe en GitHub
- Es **privado** (lo que querías)
- Está **vacío** (sin README ni licencia inicial — eso lo trae nuestro primer commit)

Si lo creaste con README/LICENSE por error, eliminálos o usá `git pull --rebase` después del paso 4.

---

## Paso 3 — Init y primer commit

```powershell
git init -b main
git config user.email "alejandro.penaosorio@mercadolibre.com.co"
git config user.name "Alejandro Peña"
git add -A
git commit -m "Initial commit: Oli foundation — brand, TDD, bitácora, foundation docs"
```

Esto debería commitear **~118 archivos / ~2.2 MB** (sin node_modules ni dist ni zips).

---

## Paso 4 — Conectar el remote y pushear

```powershell
git remote add origin git@github.com:apenaosorio_meli/oli.git
git push -u origin main
```

Si tu SSH no está configurado en Windows, podés usar HTTPS:
```powershell
git remote add origin https://github.com/apenaosorio_meli/oli.git
git push -u origin main
```
(Te va a pedir credenciales — usá tu usuario de GitHub + un Personal Access Token como password, NO tu password real)

---

## Paso 5 — Verificar

Abrí `https://github.com/apenaosorio_meli/oli` y deberías ver:
- README renderizado en la home del repo
- Carpetas: bitacora, brand, docs_extracted, playbooks, tdd
- Branch `main`
- 1 commit
- Repo privado (candado al lado del nombre)

---

## Paso 6 — Conectar al Project en Claude

1. Andá a Claude.ai → barra lateral izquierda → **New project**
2. Nombre: `Oli` (o el que quieras)
3. En el modal del project → **Knowledge** → **Connect GitHub** (tu integración ya está activa)
4. Seleccioná `apenaosorio_meli/oli`
5. Branch `main`
6. Claude va a sincronizar los archivos como contexto del project

A partir de ahí, cada conversación que arranques desde ese Project tiene el repo entero como contexto (Claude lo reindexa cuando hay cambios).

**Tip:** Pegá el `REVIEW_2026-05-30.md` en las **Project instructions** o pedile a Claude que lo lea como primer paso de cada sesión — así arranca con el resumen y los gaps en mente.

---

## Si algo falla

| Error | Causa probable | Fix |
|---|---|---|
| `fatal: not a git repository` | No corriste `git init` o estás en otra carpeta | `cd C:\Users\apenaosorio\Desktop\oli` y reintenta |
| `fatal: remote origin already exists` | Ya estaba seteado | `git remote set-url origin git@github.com:apenaosorio_meli/oli.git` |
| `Permission denied (publickey)` | No tenés llave SSH cargada | Usá HTTPS (paso 4 alternativo) |
| `! [rejected] main -> main (fetch first)` | GitHub tiene un README inicial | `git pull --rebase origin main` y luego `git push -u origin main` |
| `Updates were rejected because the tip of your current branch is behind` | Mismo caso | Mismo fix |

---

## Si querés que vuelva a meter mano

Una vez que esté en GitHub, en cualquier conversación nueva con Claude (en el Project que conectaste) puedo:
- Generar `pyproject.toml` + esqueleto del Mission Kernel
- Escribir el primer playbook ejecutable (research-brief-v1)
- Iterar el wedge/ICP con vos
- Hacer análisis competitivo más profundo
- Revisar PRs que vayas creando
