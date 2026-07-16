# Plan: Deploy demo Railway — hardening mínimo

**Estado:** plan aprobado pendiente de ejecución (no implementado aún).  
**Copia accesible en el workspace** — espejo del plan Cursor  
`~/.cursor/plans/railway_demo_hardening_b0c1d655.plan.md`  
(nombre Cursor: **Railway demo hardening**; no confundir con títulos tipo "Railway project deployment").

**Alcance de escritura:** solo `~/wc/wcg4/dashboard`. `pgc1` y `wcg3` son referencia de solo lectura.

**Decisión de demo (fija):** recorrido gerencial = stack productivo: `/` (splash) → `/panel/` → **PGC** (`/tablero/`) + reports embebidos. Las rutas `/wcgone/*` permanecen en código pero no se promocionan en el menú visible.

---

## Todos

1. Hardening en `config/settings.py`: SECRET_KEY, HTTPS cookies/HSTS, ssl_require; correr `check --deploy`
2. Ajustar `base_wcg.html` y `dashboardhome.html` para navegación demo clara (PGC primero, sin guía wcgone)
3. Verificar montaje PGC/reports sin tocar lógica de negocio
4. Crear `docs/deploy_railway_demo.md` con pasos y riesgos
5. Entregar reporte final corto en chat

---

## 1. Config producción mínima

Archivo principal: `config/settings.py`

Cambios concretos:

- **SECRET_KEY:** exigir variable de entorno cuando `DEBUG=False`. Si falta → `ImproperlyConfigured`. El fallback `"unsafe-dev-key"` solo se permite con `DEBUG=True` (desarrollo local).
- **DEBUG:** se mantiene el default actual (`False` si no se define).
- **ALLOWED_HOSTS / CSRF_TRUSTED_ORIGINS:** se mantienen env-driven; documentar valores Railway obligatorios (sin hardcodear el host).
- **HTTPS detrás de proxy (solo si `not DEBUG`):**
  - `SESSION_COOKIE_SECURE = True`
  - `CSRF_COOKIE_SECURE = True`
  - `SECURE_SSL_REDIRECT = True`
  - `SECURE_HSTS_SECONDS = 31536000` (y `SECURE_HSTS_INCLUDE_SUBDOMAINS` / `SECURE_HSTS_PRELOAD` en valores razonables)
  - Ya existe `SECURE_PROXY_SSL_HEADER`; no tocar.
- **Postgres:** con `DATABASE_URL`, pasar `ssl_require=True` a `dj_database_url.parse` (Railway Postgres).
- **Static / WhiteNoise:** ya correctos. No inventar deps nuevas.
- **Deploy files existentes:** conservar `railway.toml` y `Procfile`. Ajustar solo si `check --deploy` lo exige.

Verificación: `python manage.py check --deploy` con env de producción simulada.

**No tocar:** lógica de PGC/reports, modelos, vistas de negocio, refactor de stacks duales.

---

## 2. Navegación demo coherente

| Archivo | Cambio |
|---------|--------|
| `templates/base_wcg.html` | Marca del header: **"WCG One"** → **"WCG"**. Nav sigue a PGC/PGO/CRM/Risk productivos. |
| `templates/dashboard/dashboardhome.html` | Lead claro (PGC/reports foco). CRM/PGO/Risk como **vista preliminar**. Quitar link **Guía de uso** → `portal:ayuda`. |
| Splash productivo | Sin cambio: `/` → `/panel/`. |

---

## 3. PGC y reports

- Smoke check: `/tablero/`, `/pgc/`, `/reports/defaults/`, `/reports/generate/`
- No modificar vistas/templates de PGC ni `reports` salvo fallo de config/static.

---

## 4. Documentación de deploy

Crear `docs/deploy_railway_demo.md` con variables, root directory, start command, migraciones, collectstatic, orden de despliegue, riesgos, áreas listas vs preliminares.

Referencias: patrón Railway de `pgc1`; `wcg3` no aporta producción.

---

## 5. Reporte final (en chat al terminar)

Archivos modificados, seguridad/nav, `check --deploy`, comando de arranque, env requeridas, limitaciones, uso de referencias `pgc1`/`wcg3`.

---

## Flujo demo

```
splash (/) → panel (/panel/) → PGC (/tablero/) → reports (/reports/* embebido)
                              ↘ CRM / PGO / Risk (preliminares)
```
