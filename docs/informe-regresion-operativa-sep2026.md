# Informe — Regresión operativa PGC sep-2026 (baseline «sep-save»)

## Objetivo

Demostrar que **septiembre 2026** se puede cerrar **solo con importadores operativos** (sin `import_pgc_objetivos` / Excel Objetivos) y que **métricas y puntos modo2** coinciden con el baseline guardado antes del ejercicio.

## Baseline «sep-save»

```bash
cd dashboard
python manage.py pgc_operational_regression save --tag sep-save --year 2026 --month 9
```

Genera `pgc/fixtures/baselines/sep-save-2026-09.json` (resultados, `MonthlyMetricScore` y totales `MonthlyModeScorecard` en modo2).

## Rebuild operativo (sep 2026)

```bash
python manage.py pgc_operational_regression rebuild --year 2026 --month 9
python manage.py pgc_operational_regression verify --tag sep-save --year 2026 --month 9
```

Orden interno:

1. `import_clientes_nuevos` — `data/now/ClientesNuevos_2026-09_*.csv` (reglas `new_client_rules.py`: NIT único, sin Insurance, inversiones externas, intercompañía).
2. `import_inversiones_crecimiento` — sep 2026 + exclusión AP/PG intercompañía.
3. `import_bancos_fin_mes` — `Capital_Bancos_2026_09.csv`.
4. `recalc_investment_ingresos_from_new_clients` — INGRESOS Investment.
5. `import_ingresos` ×3 — **PGA Mensuales WC WCL WCI 2026.xlsx** (`--une-code` FACTORING / LEASING / INSURANCE).
6. `recalc_pgc` modo1 y modo2.

**Verificación (oct 2026):** `verify` reportó coincidencia al centavo con el baseline «sep-save».

## Cambios de código relevantes

| Área | Cambio |
|------|--------|
| `imports/ingresos_er_parse.py` | Lectura PGA Mensuales (fila Comisiones); par `source_value` / `measured_value` alineado a proporción modo2 (convención columna Objetivos: comisiones GTQ÷FX). |
| `import_ingresos` | Detecta PGA; `--une-code`; ya no depende de hoja «Datos» única. |
| `pgc_operational_regression` | Comando `save` / `rebuild` / `verify` para repetir cada mes (extender manifiesto). |

## Próximos meses

1. Añadir archivos operativos al manifiesto (o parametrizar rutas).
2. `save` al cierre → `rebuild` en entorno de prueba → `verify` antes de publicar.
3. Cuando existan ER `* ER 2609.xlsx` por UNE, se puede sustituir PGA por `import_ingresos` con ER sin cambiar la convención de puntos.

## Tests

```bash
python manage.py test imports.tests_ingresos_er_parse pgc.tests_operational_regression
```
