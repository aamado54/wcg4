# Checklist release único — bloque 2026-11-18

**Regla:** el usuario autoriza **un solo** `git commit` + `push` + deploy cuando **todo** lo siguiente esté verde. Hasta entonces: **sin commit, sin push**.

## 1. Código y documentación del bloque

- [ ] Alcance precisión/auditoría: `docs/precision-and-audit-scope-20261118.md`
- [ ] Brechas Fase 2: `docs/import-audit-gap-phase2-20261118.md`
- [ ] UI auditoría staff alineada a ops (`templates/imports/audit_*.html`, `imports/audit_views.py`)
- [ ] Layout data: `core/services/data_layout.py` + comandos `inventory_data_layout`, `apply_data_layout_moves`, `scaffold_data_layout`
- [ ] **No** incluir en commit: `wcg_pre_reload_*.dump`, uploads `media/`, inventarios generados en `data/done/` salvo acuerdo explícito

## 2. Migraciones (local = prod objetivo)

```bash
cd dashboard
.venv/bin/python manage.py migrate --plan
```

- [ ] `imports` ≥ `0012` (audit `0011`, investment precision)
- [ ] `pgc` ≥ `0009` (ingresos target 6 dec)

## 3. Tests automatizados (obligatorio)

```bash
cd dashboard
.venv/bin/python manage.py test imports pgc core -v1
```

- [ ] `imports.tests_import_audit` (hub, mixin, CLI, vistas)
- [ ] `core.tests_money_precision`
- [ ] `core.tests_data_layout` (clasificación YYMM / módulos)
- [ ] Suite `pgc` sin regresiones en ingresos/objetivos/investment

Registrar en este doc la salida resumida: total tests, failures, tiempo.

## 4. Verificación manual ops

- [ ] `/importaciones/` → enlace **Auditoría** visible
- [ ] `/importaciones/auditoria/` filtros tipo / éxito / usuario / fechas
- [ ] Detalle evento: ruta, error, `detail_json`, historial misma ruta
- [ ] `manage.py audit_import_status --checklist` sin sorpresas en FAIL
- [ ] Admin mensual: subir CSV clientes o ER → nuevo evento en lista
- [ ] Hub importación: dispatch CRM o PGC → evento `manual`

## 5. Precisión PGC (muestra)

- [ ] Ingresos vs meta (vista/reporte): meta y real coherentes con 6 dec (Insurance sigue 3 dec display)
- [ ] `recalc_pgc` + `recalc_investment_ingresos_from_new_clients` sin drift vs `core.money_precision`
- [ ] Export verifica TSV si aplica al período de prueba

## 6. Data layout (sin apply masivo sin revisar)

```bash
.venv/bin/python manage.py inventory_data_layout
.venv/bin/python manage.py apply_data_layout_moves          # dry-run
# solo tras revisar TSV:
# .venv/bin/python manage.py apply_data_layout_moves --apply
```

- [ ] Inventario generado; movimientos ambiguos en `dudas/` aceptables
- [ ] Carpetas YYMM solo bajo `data/{pgc,pgo,ger,pla}/`

## 7. Pre-deploy prod

- [ ] Backup BD (`pgc_pre_reload_backup` o dump acordado) **fuera** del repo
- [ ] Variables Railway / settings sin cambios accidentales
- [ ] Plan rollback: commit anterior + migraciones reversibles documentadas

## 8. Commit único (cuando usuario diga)

Mensaje sugerido (ajustar si hace falta):

> PGC pre-reload block: import audit UI, data layout commands, 6-dec ingresos paths, release docs.

Después: `push` + deploy + `migrate` en prod + repetir §3 smoke en prod.

---

**Estado agente 2026-11-18:**

- Tests: `manage.py test imports pgc core` → **112** corridos, **0** fallos, **7** skipped (~9.3 s) — 2026-11-18.
- Sin `git commit` ni `push` en esta iteración.
- Pendiente: validación manual §4–§6 por usuario antes del commit único.