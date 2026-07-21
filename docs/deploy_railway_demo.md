# Deploy Railway — demo gerencial WCG

Guía corta para desplegar `wcg4/dashboard` como demo funcional en Railway.

## Root directory

En el servicio Railway, el **Root Directory** debe apuntar al directorio que contiene `manage.py`:

```
wcg4/dashboard
```

(Si el repo es solo el dashboard, usa la raíz del repo.)

## Variables de entorno requeridas

| Variable | Valor recomendado | Notas |
|----------|-------------------|--------|
| `SECRET_KEY` | cadena larga aleatoria | **Obligatoria** si `DEBUG=False`. Sin ella la app no arranca. |
| `DEBUG` | `False` en Railway | Si no se define: **True en local**, **False en Railway**. |
| `ALLOWED_HOSTS` | host del servicio, p.ej. `xxx.up.railway.app` | Separar varios hosts con comas. |
| `CSRF_TRUSTED_ORIGINS` | `https://xxx.up.railway.app` | Debe incluir esquema `https://`. Comas si hay varios. |
| `DATABASE_URL` | (auto) | La provee el plugin PostgreSQL de Railway. |

Opcional: dominio custom → añade ese host a `ALLOWED_HOSTS` y `https://tu-dominio` a `CSRF_TRUSTED_ORIGINS`.

Generar `SECRET_KEY` localmente:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Start command recomendado

Ya definido en `railway.toml`:

```bash
python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:${PORT}
```

Equivalente en `Procfile`:

```text
web: gunicorn config.wsgi:application --bind 0.0.0.0:${PORT}
```

## Migraciones y collectstatic

- **Migraciones:** `railway.toml` → `preDeployCommand = "python manage.py migrate --noinput"`
- **Static:** WhiteNoise + `collectstatic` en el start command (y en `Procfile` release)

No hace falta inventar dependencias nuevas: el proyecto ya incluye `gunicorn`, `whitenoise`, `psycopg[binary]`, `dj-database-url`.

## Orden exacto de despliegue

1. Crear proyecto/servicio en Railway desde el repo.
2. Fijar **Root Directory** a `wcg4/dashboard` (si aplica).
3. Añadir plugin **PostgreSQL** (inyecta `DATABASE_URL`).
4. Configurar variables: `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`.
5. Deploy (Railway corre `preDeploy` migrate, luego start con collectstatic + gunicorn).
6. Crear usuario de acceso (superuser o staff) vía Railway shell:

```bash
python manage.py createsuperuser
```

7. Abrir `https://<host>/` → splash → login → `/panel/` → **PGC**.

## Recorrido demo recomendado

```
/  →  /panel/  →  /tablero/ (PGC)  →  reportes desde el tablero (/reports/*)
```

## Áreas listas para mostrar

- Splash (`/`)
- Panel (`/panel/`)
- **PGC** (`/tablero/`, `/pgc/`, métricas, exports)
- **Reports** (`GET /reports/defaults/`, `POST /reports/generate/` — UI en tablero PGC)

## Áreas preliminares (no foco de demo)

- CRM productivo (`/crm/`)
- PGO productivo (`/pgo/`)
- Balón de Riesgo productivo (`/risk/`)
- Todo el stack paralelo `/wcgone/*` (coexistencia; no promocionado en el menú principal)

## Riesgos conocidos (no bloquean la demo)

- **Media efímera:** `MEDIA_ROOT` / uploads / output en disco del contenedor; se pierden al redeploy. El tablero PGC y la generación de reportes (ZIP) no dependen de persistencia de media para la demo básica.
- **Stacks duales:** legacy vs `/wcgone/*` siguen en el código; el menú visible apunta al stack productivo.
- **Datos:** hace falta DB migrada y, idealmente, datos/importaciones para que PGC se vea con números reales.
- **HTTPS local:** con `DEBUG=False` hay redirect SSL; en Railway (TLS terminado en proxy) es correcto gracias a `SECURE_PROXY_SSL_HEADER`.

## Runtime

- Python: ver `runtime.txt` (`python-3.11.11`)
- WSGI: `config.wsgi:application`
- Settings: `config.settings`
