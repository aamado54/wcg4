# PGC sin import del libro Objetivos (validación)

Política operativa: **no importar** el workbook compartido **Cumplimiento Objetivos PGC**, hoja **Objetivos**, como fuente de datos en producción.

Eso **no** prohíbe otros Excel operativos (estado de resultados, hub financiero, etc.).

## Qué está bloqueado

| Comando | Fuente | Producción |
|---------|--------|------------|
| `import_pgc_objetivos` | `.xlsx` hoja Objetivos (libro de validación) | **Bloqueado** |
| `import_pgc_objetivos_tsv` | Export TSV de la misma hoja | **Bloqueado** |

Desbloqueo solo para migración o desarrollo:

```bash
export ALLOW_PGC_EXCEL_IMPORT=1
# o en el comando:
python manage.py import_pgc_objetivos ... --force-legacy-excel
```

Ambas vías muestran advertencia en consola.

## Qué sigue permitido (operación)

| Dato | Fuente |
|------|--------|
| **Ingresos / comisiones GTQ** (Factoraje, Leasing) | `import_ingresos` con xlsx ER (`WCF…`, `WCL…`) |
| **Ingresos** (Insurance, etc.) | Hub tablero mensual → bloque financiero |
| **Clientes nuevos** | Hub / captura operativa |
| **Venta cruzada** | `import_venta_cruzada` o hub (política VC=0 sin cross-sale real) |
| **Metas anuales** | `import_pgc_metas` (TSV oficial) |
| **Requerimientos** | Matriz anual / edición manual (no Excel Objetivos) |

### Comisiones Factoraje y Leasing (`import_ingresos`)

Ruta oficial para **INGRESOS** en FACTORING, LEASING e INSURANCE:

1. Un ER `.xlsx` por UNE (`WCF`/`WC` → Factoraje, `WCL` → Leasing, `WCI` → Insurance).
2. Hoja **Datos**: suma cuentas detalle **4** y **8** del mes, o delta YTD mes actual vs anterior.
3. GTQ mensual bruto → para F/L/WCI se divide entre **1000** antes de `MonthlyExchangeRate.usd_to_gtq` → **USD miles** en `measured_value`.
4. **No incluye INVESTMENT** (flujo aparte en el runbook de cierre).

| Aspecto | Libro Objetivos (legacy) | `import_ingresos` (operación) |
|---------|--------------------------|-------------------------------|
| Archivo | Un xlsx multi-UEN | Un ER por UNE |
| `presupuesto_gtq` | Podía venir del import Objetivos | Matriz anual / manual |
| Puntos P_ing | Desde hoja Objetivos | `import_pgc_metas` |
| Clientes | Misma hoja | Cargas operativas |

Si falta TC del mes, el import falla — cargar TC antes en el hub o matriz de ingresos.

## Validación (sí usar el libro, sin importar)

```bash
cd dashboard
python tools/pgc/validate_ejecucion_excel.py /ruta/Cumplimiento-Objetivos-PGC.xlsx --year 2026
```

Compara scores modo2 en base de datos con columnas S–X de la hoja Objetivos. **No escribe** en la base.

## Pipeline mensual (resumen)

1. TC del mes  
2. `import_ingresos` (F/L) y/o cargas financieras en el hub  
3. Clientes, VC según operación  
4. Recalcular período  
5. Validador CLI opcional contra el libro compartido  
6. Revisión gerencial  

Detalle: `docs/pgc-cierre-mensual-operacion.md`.

## Banderas en el hub

- `legacy_objetivos_import` — aún hay filas con nota «Importado desde … Objetivos»; migrar a fuentes operativas.  
- `ingresos_presupuesto_gtq` — falta presupuesto GTQ en metas de ingresos (no implica importar Objetivos).
