# Guía demo operativa — WCG One (Fase E)

Documento breve para levantar el sistema, sembrar datos de ejemplo y ejecutar una demo interna o gerencial.

---

## 1. Levantar el sistema

```bash
cd /home/caa/wc/wcg_one
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # solo la primera vez
python manage.py runserver
```

Abrir: **http://127.0.0.1:8000/**

Credenciales: las del superusuario creado con `createsuperuser`.

---

## 2. Sembrar datos demo

Comando de management (recomendado):

```bash
python manage.py seed_wcg_demo
```

Para limpiar datos demo previos y volver a sembrar:

```bash
python manage.py seed_wcg_demo --fresh
```

### Qué crea el seed

| Área | Contenido |
|------|-----------|
| **CRM** | 5 entidades guatemaltecas, 4 contactos, 2 interacciones, 2 tareas |
| **Risk** | 3 operaciones, snapshots históricos (2 fechas c/u), 2 EEFF, 1 alerta de mora |
| **PGO** | 8 tickets TI simulados (abiertos, en proceso, cerrados) |
| **Core** | 3 lotes de importación simulados (CRM, Risk, PGO) |
| **Maestros** | Unidades de negocio y productos básicos |

Los registros demo se marcan con `origen=demo` en entidades y prefijos `TI-DEMO-*` en tickets.

---

## 3. Acceso al admin

URL: **http://127.0.0.1:8000/admin/**

Útil para:

- Revisar entidades, contactos, operaciones y tickets
- Inspeccionar lotes de importación (`DataImportBatch`)
- Soporte operativo durante la demo

---

## 4. Ruta sugerida para demo (15–20 min)

| Paso | URL | Qué mostrar |
|------|-----|-------------|
| 1 | `/` | KPIs globales, módulos, importaciones recientes |
| 2 | `/crm/entidades/` | Listado, filtros, resumen por ciudad/riesgo, export CSV |
| 3 | `/crm/entidades/<id>/` | Detalle: contactos, productos, interacciones, tareas |
| 4 | `/crm/contactos/` | Contactos vinculados a entidades |
| 5 | `/crm/tareas/` | Tareas pendientes de seguimiento |
| 6 | `/risk/comando-balon/` | Mora, saldos vencidos, export CSV |
| 7 | `/risk/operaciones/<id>/` | Historial de snapshots por operación |
| 8 | `/pgo/` | Dashboard tickets, SLA, tiempos |
| 9 | `/pgo/tickets/` | Listado completo con filtros |
| 10 | `/pgc/` | Placeholder — explicar transición al legado |
| 11 | `/ayuda/` | Guía integrada en el portal |
| 12 | `/admin/` | Soporte y trazabilidad de importaciones |

---

## 5. Qué muestra cada módulo

### CRM — Clientes
- Maestro único de entidades (clientes/prospectos)
- Contactos, productos relacionados, interacciones y tareas
- Importación CSV/XLSX y exportación CSV
- **Estado: operativo**

### Balón de Riesgo
- Comando Balón: snapshots de mora y saldos vencidos
- Detalle por cliente y por operación
- Importación snapshots leasing + EEFF
- **Estado: operativo**

### PGO — Operación
- Dashboard de tickets helpdesk
- Indicadores de SLA y tiempos de atención
- Importación y exportación CSV
- **Estado: operativo** (scoring avanzado pendiente)

### PGC
- Placeholder ordenado con enlace al sistema legado
- **Estado: placeholder** — integración profunda pendiente

---

## 6. Placeholders vs operativo

| Funcionalidad | Estado |
|---------------|--------|
| Login / portal / navegación | Operativo |
| CRM listado, detalle, import, export | Operativo |
| Risk Comando Balón, import, export | Operativo |
| PGO dashboard, tickets, import, export | Operativo |
| Seed demo (`seed_wcg_demo`) | Operativo |
| PGC integrado | Placeholder |
| PGC legado (`/legacy-pgc1/`) | Enlace de transición |
| Scoring PGO avanzado | Pendiente |
| Permisos granulares por módulo | Pendiente |

---

## 7. Checklist pre-demo

Marcar antes de presentar:

- [ ] Servidor corriendo (`runserver`)
- [ ] Usuario creado y login probado
- [ ] `python manage.py seed_wcg_demo` ejecutado sin errores
- [ ] Panel principal (`/`) muestra KPIs > 0
- [ ] CRM: listado y detalle de entidad navegables
- [ ] Risk: Comando Balón con snapshots y mora visible
- [ ] PGO: dashboard con tickets y SLA
- [ ] Export CSV probado (CRM, Risk, PGO)
- [ ] Admin accesible
- [ ] Página `/ayuda/` revisada

---

## 8. Solución de problemas

| Problema | Acción |
|----------|--------|
| KPIs en cero | Ejecutar `seed_wcg_demo` o importar archivos reales |
| Error 404 en login | Ir a `/accounts/login/` |
| Export vacío | Verificar filtros GET en la URL |
| Duplicados demo | `python manage.py seed_wcg_demo --fresh` |

---

*Fase E — demo interna. No incluye Fase F ni rediseño de importadores.*
