# SUPER-TAREA (PAUSADA) — Regresión PGC solo importadores operativos

**Estado:** PAUSADA — retomar en ~2 semanas (aprox. fin de octubre 2026).  
**Alcance inicial:** cierre **septiembre 2026** sin `import_pgc_objetivos` / Excel Objetivos.  
**Workspace:** `dashboard/` (Django + SQLite local `db.sqlite3`).

---

## 1. Propósito

Demostrar de forma repetible que un mes PGC se puede **cerrar solo con fuentes operativas** (CSV, PGA/ER, bancos, recálculos) y que:

1. Las métricas en BD reflejan las reglas acordadas (clientes nuevos, inversiones, ingresos).
2. Los **puntos modo2** coinciden **al centavo** con un **baseline JSON** guardado antes del ejercicio (`sep-save`).
3. El libro *Cumplimiento Objetivos PGC* se usa **únicamente** para cuadre opcional (`validate_ejecucion_excel.py`), **nunca** para cargar BD.

No ejecutar el **rebuild completo** de la super-tarea salvo que el agente o humano retome explícitamente este documento.

---

## 2. Prerrequisitos

| Requisito | Detalle |
|-----------|---------|
| Entorno Python | `cd dashboard && source .venv/bin/activate` (o `.venv/bin/python` en cada comando). |
| Base local | SQLite `dashboard/db.sqlite3` con plan PGC 2026 y metas (`import_pgc_metas` / seed). |
| Política Excel | **No** `import_pgc_objetivos` ni `import_pgc_objetivos_tsv` en producción. Ver [pgc-sin-excel-objetivos-validacion.md](pgc-sin-excel-objetivos-validacion.md). |
| Baseline existente | `pgc/fixtures/baselines/sep-save-2026-09.json` (generado con `save`). |
| Documentación relacionada | [informe-regresion-operativa-sep2026.md](informe-regresion-operativa-sep2026.md), [pgc-clientes-nuevos-reglas-importacion.md](pgc-clientes-nuevos-reglas-importacion.md), [pgc-inversiones-captaciones.md](pgc-inversiones-captaciones.md), [pgc-cierre-mensual-operacion.md](pgc-cierre-mensual-operacion.md). |

---

## 3. Baseline «sep-save»

El baseline congela, para un año-mes y **modo2**:

- `MonthlyMetricResult` (ejecución),
- `MonthlyMetricScore` (puntos por métrica),
- totales `MonthlyModeScorecard`.

**Guardar** (solo cuando el cierre operativo ya es el “golden” acordado):

```bash
cd dashboard
.venv/bin/python manage.py pgc_operational_regression save --tag sep-save --year 2026 --month 9
```

Salida: `pgc/fixtures/baselines/sep-save-2026-09.json`.

**Importante:** `save` lee la BD **tal como está**; no importa archivos. Hacer `save` después de un cierre correcto, no antes de un rebuild experimental.

---

## 4. Comandos `pgc_operational_regression`

Implementación: `pgc/management/commands/pgc_operational_regression.py`.

| Acción | Comando | Efecto |
|--------|---------|--------|
| **save** | `… save --tag sep-save --year 2026 --month 9` | Exporta JSON baseline. |
| **rebuild** | `… rebuild --year 2026 --month 9` | Reimporta **solo** el manifiesto sep-2026 y ejecuta `recalc_pgc` modo1 + modo2. **Destructivo** para datos del mes importados por esos comandos. |
| **verify** | `… verify --tag sep-save --year 2026 --month 9` | Compara BD actual vs JSON; exige coincidencia **al centavo** en modo2. Exit code ≠ 0 si falla. |

Opciones útiles:

- `--baseline-path /ruta/custom.json` — baseline alternativo.
- `--skip-bancos` — omitir `Capital_Bancos` si falta el archivo.

**Orden recomendado al retomar la super-tarea:**

1. (Opcional) Triple validación local **sin** rebuild — sección 7.
2. Si se prueba regresión end-to-end: `rebuild` → `verify`.
3. Si `verify` falla: corregir importadores/reglas, **no** importar Objetivos; volver a `rebuild` + `verify`.
4. Actualizar baseline solo si negocio aprueba nuevo golden: `save`.

---

## 5. Manifiesto de archivos operativos (2026-09)

Rutas relativas a `dashboard/`; el comando prueba también `../data/now/…`.

| Clave | Archivos (primer existente gana) |
|-------|----------------------------------|
| Clientes nuevos | `data/now/ClientesNuevos_2026-09_20261008.csv` |
| Inversiones crecimiento | `data/now/Inversiones_crecimiento_2026_09.csv` |
| Capital bancos | `data/now/Capital_Bancos_2026_09.csv` |
| Ingresos F/L/I (PGA sep) | `data/now/0/PGA Mensuales WC WCL WCI 2026.xlsx` |

**Secuencia interna del `rebuild`:**

1. `import_clientes_nuevos`
2. `import_inversiones_crecimiento`
3. `import_bancos_fin_mes` (si existe)
4. `recalc_investment_ingresos_from_new_clients --year 2026 --month 9`
5. `import_ingresos` ×3 con `--une-code FACTORING`, `LEASING`, `INSURANCE` (mismo PGA, mes 9)
6. `recalc_pgc` modo1 y modo2

Copias en repo padre: `/home/caa/wc/wcg4/data/now/…` (mismos nombres).

---

## 6. Qué NO hacer (Excel Objetivos)

- **Prohibido en producción:** `import_pgc_objetivos`, `import_pgc_objetivos_tsv` sobre el libro *Cumplimiento Objetivos PGC* (hoja Objetivos).
- **Permitido solo lectura:** cuadre CLI:

```bash
cd dashboard
.venv/bin/python tools/pgc/validate_ejecucion_excel.py \
  --path "/ruta/Cumplimiento Objetivos PGC Sep26 (Notas).xlsx" \
  --year 2026 --month 9
```

Libros de referencia en el monorepo (oct 2026):

- Sep 2026: `../data/now/Cumplimiento Objetivos PGC Sep26 (Notas).xlsx`
- Ago 2026: `../data/done/Cumplimiento Objetivos PGC Ago26 (Notas).xlsx`

El Excel **no define** el éxito de la super-tarea; el criterio oficial es **`verify` vs `sep-save`**. Las diferencias vs Excel pueden ser esperadas (p. ej. VC=0 operativo, reglas clientes nuevos).

---

## 7. Triple validación local (sin rebuild) — checklist

Ejecutar al retomar o antes de un `rebuild` para no perder tiempo.

### 7.1 Clientes nuevos (sep 2026)

**Reglas:** `imports/new_client_rules.py` → `aggregate_clientes_nuevos_counts()`.

**Criterio sep-2026 acordado:**

| UNE | Conteo |
|-----|--------|
| Leasing | **3** |
| Investment | **3** |
| Insurance | **0** |

**Evidencia desde CSV** (`ClientesNuevos_2026-09_20261008.csv`):

```bash
cd dashboard
.venv/bin/python manage.py shell -c "
from pathlib import Path
import csv
from collections import defaultdict
from imports.new_client_rules import aggregate_clientes_nuevos_counts
from imports.client_rates import row_get
from core.models import UNE, UNEAlias
from core.services.une_resolve import resolve_une_from_text

path = Path('../data/now/ClientesNuevos_2026-09_20261008.csv')
aliases = {a.raw_value.strip().upper(): a.une for a in UNEAlias.objects.select_related('une').filter(is_active=True)}
unes = {u.code: u for u in UNE.objects.all()}

class R: pass
rows = []
with path.open(encoding='utf-8-sig', newline='') as f:
    for raw in csv.DictReader(f):
        r = R(); r.year, r.month = 2026, 9
        raw_une = row_get(raw, 'UNE', 'Une', 'Unidad')
        r.raw_une_value = raw_une or ''
        r.une = resolve_une_from_text(raw_une, aliases=aliases, unes_by_code=unes)
        r.nit = row_get(raw, 'NIT', 'Nit')
        r.client_name = row_get(raw, 'Cliente', 'NombreCliente', 'Nombre')
        r.operation_code = row_get(raw, 'CodigoOperacion', 'Operacion')
        cp = row_get(raw, 'ContratosPrevios') or '0'
        r.counts_as_new = str(cp).strip() in ('0', '0.0', '')
        rows.append(r)

counts = aggregate_clientes_nuevos_counts(rows)
by_id = {u.id: u.code for u in UNE.objects.all()}
print({by_id[k[2]]: v for k, v in counts.items() if k[0]==2026 and k[1]==9})
"
```

Debe imprimir `LEASING: 3`, `INVESTMENT: 3`, sin Insurance. Leasing: varias filas / mismo NIT → un solo cliente (dedup NIT).

**BD:** mismos totales vía filas `NewClientImportRow` sep 2026 + la misma función de agregación.

### 7.2 Inversiones en estadísticas (sep 2026)

Comprobar:

- `InvestmentGrowthRow` con `year=2026`, `month=9` (filas > 0).
- `BankLoanMonthSnapshot` para 2026-09 (si el mes usa captaciones con bancos).
- `MonthlyMetricResult` INGRESOS / UNE INVESTMENT: `measured_value` en **miles USD** (crecimiento neto).
- `investment_real_map_for_periods([(2026, 9)])` **no vacío** (`pgc/investment_ingresos.py`).

```bash
.venv/bin/python manage.py shell -c "
from core.models import UNE, MetricDefinition
from imports.models import InvestmentGrowthRow, BankLoanMonthSnapshot
from pgc.models import MonthlyMetricResult
from pgc.investment_ingresos import investment_real_map_for_periods, has_investment_growth_data

print('growth rows', InvestmentGrowthRow.objects.filter(year=2026, month=9).count())
print('banks', BankLoanMonthSnapshot.objects.filter(year=2026, month=9).count())
u = UNE.objects.get(code='INVESTMENT')
r = MonthlyMetricResult.objects.filter(year=2026, month=9, une=u, metric__code=MetricDefinition.CODE_INGRESOS).first()
print('INGRESOS measured_value', r.measured_value if r else None)
print('has_growth', has_investment_growth_data())
print('real_map', investment_real_map_for_periods([(2026, 9)]))
"
```

### 7.3 Cuadre Excel (solo validación)

```bash
.venv/bin/python tools/pgc/validate_ejecucion_excel.py \
  --path "../data/now/Cumplimiento Objetivos PGC Sep26 (Notas).xlsx" --year 2026 --month 9

.venv/bin/python tools/pgc/validate_ejecucion_excel.py \
  --path "../data/done/Cumplimiento Objetivos PGC Ago26 (Notas).xlsx" --year 2026 --month 8
```

Reportar hallazgos **por UNE** (`WC`, `WCL`, `WCI`, `WCINV`, `WCG`). No corregir cargando Objetivos.

### 7.4 Baseline (criterio de regresión)

```bash
.venv/bin/python manage.py pgc_operational_regression verify --tag sep-save --year 2026 --month 9
```

Éxito: mensaje `OK: 2026-09 coincide con baseline «sep-save» (modo2).`

---

## 8. Cuándo extender a otros meses

Hoy el manifiesto está **codificado solo para 2026-09** (`SEP_2026_MANIFEST` en `pgc_operational_regression.py`). Para otro mes:

1. Añadir entradas CSV/XLSX en un manifiesto nuevo (p. ej. `OCT_2026_MANIFEST`) o parametrizar `--year` / `--month` con rutas.
2. Generar baseline propio: `save --tag oct-save --year 2026 --month 10`.
3. Sustituir PGA por ER mensuales cuando existan (`* ER 2609.xlsx` por UNE) en `import_ingresos` — misma convención GTQ/miles que [pgc-puntos-proporcion-objetivos.md](pgc-puntos-proporcion-objetivos.md).
4. Repetir triple validación + `rebuild` + `verify` en entorno de prueba antes de producción.

---

## 9. Criterios de éxito (resumen)

| # | Criterio | Herramienta |
|---|----------|-------------|
| A | Clientes nuevos sep: Leasing 3, Investment 3, Insurance 0; dedup NIT | `aggregate_clientes_nuevos_counts` (CSV + BD) |
| B | Inversiones sep en tablero: filas crecimiento, bancos si aplica, INGRESOS Investment, `investment_real_map` | Shell / admin ingresos |
| C | Puntos modo2 **al centavo** vs baseline operativo | `pgc_operational_regression verify --tag sep-save` |
| D | (Opcional) Cuadre vs Excel autor | `validate_ejecucion_excel.py`; diferencias documentadas, **sin import Objetivos** |

**Tests automatizados relacionados:**

```bash
.venv/bin/python manage.py test imports.tests_ingresos_er_parse pgc.tests_operational_regression imports.tests_new_client_rules
```

---

## 10. Notas de la pausa (2026-10-14)

- Triple validación local ejecutada **sin** `rebuild` completo.
- `verify --tag sep-save` en SQLite local: **OK** (modo2 al centavo vs baseline).
- Cuadre Excel sep/ago: pueden aparecer diferencias en VC, clientes (reglas operativas vs libro legacy) e ingresos ago; tratar como **informe**, no como fallo de baseline salvo que negocio decida alinear Excel.

**Próximo paso al retomar:** ejecutar sección 7 → si todo verde, opcionalmente `rebuild` + `verify` en copia de BD; si falla `verify`, depurar importadores (ingresos PGA/ER, clientes, inversiones) antes de tocar metas u Objetivos.
