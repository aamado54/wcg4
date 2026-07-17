# Migración PGC pgc1 → wcg4 — estado del dump

## Archivo recibido

`/home/caa/wc/wcg4/data/pgc1_pgc_data.json` (~257 KB)

## Hallazgo bloqueante

El archivo **no es un `dumpdata` válido completo**:

1. **Truncado al inicio**: empieza a mitad de un objeto (`"carry_generated": ...`), no con `[`.
2. **Contaminado al final** con prompt de shell Railway: `root@5e91e51e5764:/app#`.
3. Tras reparación mecánica solo se recuperan **468 objetos** de **3 modelos**:

| Modelo | Cantidad |
|--------|----------|
| `pgc.monthlymetricscore` | 368 |
| `pgc.monthlymodescorecard` | 96 |
| `pgc.manualrequirementscompliance` | 4 |

## Lo que falta (imprescindible para un clon PGC)

No están en el dump (o se perdieron en el truncado):

- `core.une`, `core.unealias`, `core.currency`, `core.metricdefinition`, `core.systemsetting`
- `pgc.pgcplan`, `pgc.monthlytarget`, `pgc.monthlyexchangerate`, `pgc.monthlymetricresult`
- `pgc.monthlyscorecard`, `pgc.metricreserve`, `pgc.adminmanualeditlog`
- Todo `imports.*` (`fileupload`, headers/rows de clientes, etc.)

Sin plan/UNE/métricas/targets/resultados, cargar solo scorecards dejaría FKs huérfanas o datos incoherentes.

## Esquema pgc1 vs wcg4 (sobre lo recuperado)

Los 3 modelos presentes tienen campos alineados con wcg4 (`plan`, `une`, `metric`, `mode`, carry_*, etc.).  
La diferencia OneToOne→FK de `NewClientImportHeader.file_upload` **no aplica** a este fragmento (no hay imports en el archivo).

## Decisión

- **NO** ejecutar `loaddata` sobre este JSON.
- **NO** cargar el fragmento parcial a producción.
- Guardado de referencia: `dashboard/data/pgc1_pgc_data_RECOVERED_PARTIAL.json` (solo evidencia).

## Qué hacer en pgc1 (Railway wcg.lol)

Volver a exportar **completo**, redirigiendo a archivo (no copiar/pegar de la consola):

```bash
python manage.py dumpdata \
  core.UNE core.UNEAlias core.Currency core.MetricDefinition core.SystemSetting \
  pgc.PGCPlan pgc.MonthlyExchangeRate pgc.MonthlyTarget pgc.MonthlyMetricResult \
  pgc.MonthlyScorecard pgc.MonthlyMetricScore pgc.MonthlyModeScorecard \
  pgc.ManualRequirementsCompliance pgc.MetricReserve pgc.AdminManualEditLog \
  imports.FileUpload imports.FileImportLog \
  imports.FinancialStatementImportHeader \
  imports.NewClientImportHeader imports.NewClientImportRow \
  imports.CrossSaleImportHeader imports.CrossSaleImportRow \
  imports.StationTimeImportHeader \
  --indent 2 -o /tmp/pgc1_pgc_data.json

# Verificar
python -c "import json; d=json.load(open('/tmp/pgc1_pgc_data.json')); print(len(d), sorted(set(x['model'] for x in d)))"

# Descargar el archivo al repo, p.ej. wcg4/data/pgc1_pgc_data.json
```

Cuando el JSON nuevo empiece con `[` y contenga al menos `core.une` + `pgc.pgcplan` + `pgc.monthlymetricresult`, se puede reintentar la carga (idealmente con comando de migración controlada).
