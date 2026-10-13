# PGC — Solo datos operativos (sin importar libro de validación)

Política: el workbook compartido **Cumplimiento Objetivos PGC**, hoja **Objetivos**, **nunca** alimenta la base de datos en producción. Sirve únicamente para **comparar** puntos modo2 (columnas S–X) con el validador CLI.

Los **Excel/CSV operativos** (estados de resultados, clientes nuevos, inversiones, bancos, etc.) **sí** son fuentes oficiales.

## Qué está bloqueado (escribe en BD)

| Comando | Fuente | Producción |
|---------|--------|------------|
| `import_pgc_objetivos` | `.xlsx` hoja Objetivos (libro de validación) | **Bloqueado** |
| `import_pgc_objetivos_tsv` | Export TSV de la misma hoja | **Bloqueado** |

Desbloqueo solo migración o desarrollo:

```bash
export ALLOW_PGC_EXCEL_IMPORT=1
# o en el comando:
python manage.py import_pgc_objetivos ... --force-legacy-excel
```

`ALLOW_PGC_EXCEL_IMPORT` aplica **solo** a esos imports legacy. **No** hace falta para el validador.

## Validación Excel (solo lectura, no carga BD)

```bash
cd dashboard
python tools/pgc/validate_ejecucion_excel.py --path /ruta/Cumplimiento-Objetivos-PGC.xlsx --year 2026 --month 9
```

- Lee la hoja Objetivos y compara con lo ya cargado en la BD.
- **No escribe** filas ni metas.
- Opcional en cierre; útil para cuadre con el autor del PGC.

Opciones: `--months all`, `--scores-only`, `--mode modo2`.

## Mapa métrica → fuente operativa {#mapa-fuentes-operativas}

| Rubro PGC | Campo en BD (idea) | Archivo / proceso | Comando | Dónde en el hub |
|-----------|-------------------|-------------------|---------|-----------------|
| **Ingresos / comisiones** (Factoraje, Leasing, Insurance) | `MonthlyMetricResult`: `source_value` (GTQ bruto mes), `measured_value` (miles USD) | Estado de resultados `.xlsx` por UNE (`WCF`/`WC`, `WCL`, `WCI`) | `import_ingresos` | Tablero mensual → bloque **Estados de resultados** (financiero) |
| **Presupuesto comisiones GTQ** (denominador puntos ingresos modo2) | `MonthlyTarget.presupuesto_gtq` | Meta miles USD del plan × 1000 (convención hoja) o captura explícita | (derivado al importar ER si falta) + matriz anual | **Ingresos (año completo)** / edición manual metas |
| **Metas ingresos (miles USD)** y **P_ing / P_cli…** | `MonthlyTarget.target_value`, `points_if_achieved` | TSV oficial anual | `import_pgc_metas` | Metas del plan (seed / TSV) |
| **Tipo de cambio** | `MonthlyExchangeRate.usd_to_gtq` | Captura mensual | (UI) | Matriz ingresos / edición manual |
| **Clientes nuevos** | `MonthlyMetricResult` CLIENTES_NUEVOS | CSV clientes nuevos | `import_clientes_nuevos` | Tablero mensual → **Clientes nuevos**; hub **Importación general** |
| **Venta cruzada** | `MonthlyMetricResult` VENTA_CRUZADA | CSV VC (si existe operación) | `import_venta_cruzada` | Tablero mensual → **Venta cruzada** |
| **Ingresos Inversiones** (crecimiento neto miles USD) | `MonthlyMetricResult` INVESTMENT | CSV crecimiento + bancos mes anterior | `import_inversiones_crecimiento`, `import_bancos_fin_mes` → `recalc_investment_ingresos_from_new_clients` | Hub importaciones; recálculo en tablero |
| **Requerimientos OA** | `ManualRequirementsCompliance` | Matriz anual / edición manual | (UI) | **Requerimientos (año completo)** |
| **Puntos modo1 / modo2** | `MonthlyMetricScore`, `MonthlyModeScorecard` | Cálculo tras cargas | `recalc_pgc` o «Recalcular período» | Tablero mensual → **Revisar resultado** |

Detalle fórmulas modo2 ingresos en GTQ: [pgc-puntos-proporcion-objetivos.md](pgc-puntos-proporcion-objetivos.md).

### Comisiones Factoraje y Leasing (`import_ingresos`)

1. Un ER `.xlsx` por UNE (`WCF`/`WC` → Factoraje, `WCL` → Leasing, `WCI` → Insurance).
2. Hoja **Datos**: suma cuentas detalle **4** y **8** del mes, o delta YTD mes actual vs anterior.
3. GTQ mensual bruto → para F/L/WCI se divide entre **1000** antes de `MonthlyExchangeRate.usd_to_gtq` → **USD miles** en `measured_value`.
4. `source_value` = GTQ bruto (sin ÷1000); alimenta **2.Proporción** modo2 junto con `presupuesto_gtq`.
5. Si falta `presupuesto_gtq`, `import_ingresos` puede derivarlo como **meta (miles USD) × 1000**; sustituya en matriz anual si el presupuesto GTQ real difiere.
6. **No incluye INVESTMENT** (flujo aparte; ver [pgc-inversiones-captaciones.md](pgc-inversiones-captaciones.md)).

| Aspecto | Libro Objetivos (legacy) | `import_ingresos` (operación) |
|---------|--------------------------|-------------------------------|
| Archivo | Un xlsx multi-UEN | Un ER por UNE |
| `presupuesto_gtq` | Columna presupuesto comisiones | Matriz / derivado meta×1000 / manual |
| Puntos P_ing | Desde hoja | `import_pgc_metas` |
| Clientes / VC / reqs | Misma hoja | Cargas operativas (VC=0 sin archivo real) |

Si falta TC del mes, el import falla — cargar TC antes en el hub o matriz de ingresos.

## Pipeline mensual (resumen)

1. TC del mes  
2. `import_ingresos` (F/L/WCI) vía hub financiero y/o CLI  
3. Clientes, inversiones/bancos, VC según operación  
4. Metas / `presupuesto_gtq` si aplica  
5. Recalcular período (`recalc_pgc` modo1 + modo2)  
6. (Opcional) Validador CLI contra libro de validación — **sin importar**  
7. Revisión gerencial  

Checklist operativo: [pgc-cierre-mensual-operacion.md](pgc-cierre-mensual-operacion.md).

## Banderas en el hub

- `legacy_objetivos_import` — filas con nota «Importado desde … Objetivos»; migrar a fuentes operativas.  
- `ingresos_presupuesto_gtq` — falta presupuesto GTQ en metas de ingresos.  
- `validate_hint` — recordatorio del validador CLI (solo lectura).
