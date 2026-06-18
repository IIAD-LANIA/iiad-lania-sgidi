# Configuración de Persistencia — Streamlit Cloud

## Problema
Streamlit Cloud tiene un **sistema de archivos efímero**: los cambios guardados en `sgi_state.json` se pierden al reiniciar el contenedor (redeploy, inactividad prolongada, etc.).

La app ya tiene toda la lógica para sincronizar con GitHub, pero necesita que configures los **Secrets** en Streamlit Cloud.

---

## Solución: Configurar Secrets en Streamlit Cloud

### Paso 1 — Crear un Personal Access Token en GitHub

1. Ve a [github.com/settings/tokens](https://github.com/settings/tokens)
2. Haz clic en **"Generate new token (classic)"**
3. Nombre: `streamlit-sgidi`
4. Expiración: **No expiration** (o la que prefieras)
5. Permisos requeridos: ✅ `repo` (todo el checkbox)
6. Clic en **"Generate token"**
7. **Copia el token** (solo se muestra una vez)

### Paso 2 — Configurar Secrets en Streamlit Cloud

1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Busca tu app `implementacion-sg-idi-iiad`
3. Clic en los **tres puntos (⋮)** → **"Settings"**
4. Ve a la pestaña **"Secrets"**
5. Pega el siguiente contenido (reemplazando con tus valores reales):

```toml
GITHUB_TOKEN = "ghp_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
GITHUB_REPO  = "IIAD-LANIA/iiad-lania-sgidi"
GITHUB_FILE_PATH = "sgi_state.json"
GITHUB_BRANCH = "main"
```

6. Clic en **"Save"** → La app se reiniciará automáticamente

### Paso 3 — Verificar que funciona

Después del reinicio, en la barra lateral deberías ver:

> 🟢 **GitHub activo**

Y al hacer cambios, el botón **Guardar** los sincronizará con el archivo `sgi_state.json` en este repositorio.

---

## Flujo de funcionamiento

```
Usuario hace cambio en la app
        ↓
se guarda en st.session_state (memoria)
        ↓
se marca pending_save = True
        ↓
auto-guardado → PUT a GitHub API
        ↓
sgi_state.json actualizado en el repo
        ↓
próxima visita → carga desde GitHub → estado recuperado ✅
```

---

## Notas de seguridad

- El token se guarda **encriptado** en Streamlit Cloud, nunca queda expuesto en el código.
- Nunca subas el token al repositorio ni lo incluyas en el código fuente.
- Si el token se compromete, revócalo desde [github.com/settings/tokens](https://github.com/settings/tokens) y crea uno nuevo.

---

## ¿Qué pasa si no configuro los Secrets?

La app funciona en **modo local**: los cambios se guardan durante la sesión activa, pero se pierden al recargar la página o al reiniciar el contenedor. El botón de "Descargar JSON" en la barra lateral permite hacer backups manuales.
