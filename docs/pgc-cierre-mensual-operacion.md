# PGC — Cierre mensual (operación)

Guía operativa para el **Centro de operaciones** del tablero PGC: importaciones, tipo de cambio, recálculo y validación contra el libro Objetivos (sin importarlo).

## Resumen post-mortem (cierre ene–jul 2026)

Tras alinear modo2 con la hoja Objetivos se documentaron estos puntos de fallo recurrentes:

1. **Dependencia del libro Objetivos** — ejecución cargada desde Excel en lugar de ER/`import_ingresos`.
2. **Metas de ingresos sin `presupuesto_gtq`** — proporción modo2 incorrecta.
3. **Score modo2 desactualizado** — cambios en datos sin recalcular el período.
4. **Recálculo global con pendientes** — ingresos STALE, TC faltante, Investment o score incompleto.
5. **Validación manual omitida** — no se ejecutó el validador CLI antes de publicar cifras.

El centro de operaciones muestra **banderas** (`pgc/ops_flags.py`) con mensajes en español y pasos de corrección.

## Política operativa (2026 en adelante)

**Libro compartido «Cumplimiento Objetivos PGC» (hoja Objetivos): nunca importar en producción.**  
Cuadre opcional con `validate_ejecucion_excel.py` (solo lectura, sin import). Ver [pgc-sin-excel-objetivos-validacion.md](pgc-sin-excel-objetivos-validacion.md).

| Dato | Fuente oficial | Libro Objetivos |
|------|----------------|-----------------|
| **Comisiones / INGRESOS** | `import_ingresos` (xlsx ER), matriz anual, hub financiero | **No importar** |
| **Clientes nuevos** | Hub / captura operativa | **No importar** |
| **Venta cruzada** | Cargas VC / `import_venta_cruzada`; política **VC=0** sin cross-sale real | **No importar** |
| **Requerimientos** | Matriz anual / edición manual | **No importar** |
| **Puntos / metas** | `import_pgc_metas` (TSV) | Solo validación CLI |

## Checklist de cierre

| Paso | Dónde | Acción |
|------|--------|--------|
| 1 | Tablero mensual | Subir y procesar cargas (financiero, clientes, venta cruzada) por mes. |
| 2 | TC | Editar tipo de cambio del mes antes de capturar ingresos en Q. |
| 3 | Ingresos | `import_ingresos` (Factoraje/Leasing ER xlsx) o matriz anual; revisar banderas STALE/TC. |
| 4 | Reqs | Matriz anual de requerimientos o edición manual. |
| 5 | Recálculo | «Recalcular período» en tablero mensual o recálculo inteligente si hay pendientes. |
| 6 | Validación (dev) | CLI contra libro Objetivos solo con `ALLOW_PGC_EXCEL_IMPORT=1`; no es paso de cierre. |
| 7 | Revisión | Tablero gerencial y bloque revisión del hub. |

## Comandos Objetivos (bloqueados en producción)

`import_pgc_objetivos` e `import_pgc_objetivos_tsv` están deshabilitados salvo `ALLOW_PGC_EXCEL_IMPORT=1` o `--force-legacy-excel` (migración/dev).

```bash
# NO usar en cierre mensual normal:
# python manage.py import_pgc_objetivos ...
# python manage.py import_pgc_objetivos_tsv ...
```

**Comisiones:** siempre `import_ingresos` y el hub financiero; ver gaps F/L en [pgc-sin-excel-objetivos-validacion.md](pgc-sin-excel-objetivos-validacion.md#comisiones-factoraje-y-leasing-import_ingresos).

### Limpieza de datos heredados (VC / reqs / notas Objetivos)

```bash
python manage.py clear_operational_fiction_from_objetivos --year 2026 --months 8,9
python manage.py clear_operational_fiction_from_objetivos --year 2026 --months 8,9 --dry-run
```

Pone **VENTA_CRUZADA** en 0 por UNE y elimina `ManualRequirementsCompliance` de Factoraje, Leasing e Inversiones (conserva Insurance).

Si aparece `legacy_objetivos_import`, reemplace ejecución con `import_ingresos` y recalcule.

## Recálculo

El estado global (`get_global_recalc_status`) lista períodos con motivos (STALE, score incompleto, Investment, etc.).

- Corrija la causa (p. ej. complete TC en la matriz de ingresos).
- Ejecute recálculo desde el tablero mensual o el flujo de recálculo inteligente.

Banderas **Recálculo pendiente** y **Score modo2 anterior al último import Objetivos** (solo si quedaron datos legacy) apuntan a este paso.

## Validacion Excel (dev)

Script en `tools/pgc/validate_ejecucion_excel.py`. Compara modo2 en base de datos con columnas S–X de la hoja Objetivos del **libro de validación**. No importa datos. **No forma parte del cierre operativo**; use solo en desarrollo con `ALLOW_PGC_EXCEL_IMPORT=1`.

```bash
cd dashboard
export ALLOW_PGC_EXCEL_IMPORT=1
python tools/pgc/validate_ejecucion_excel.py /ruta/archivo-referencia.xlsx --year 2026
```

Opciones útiles: `--month MM`, `--mode modo2` (por defecto proporción). Ver también `docs/pgc-puntos-proporcion-objetivos.md`.

## Banderas en la UI

| Código | Significado |
|--------|-------------|
| `ingresos_presupuesto_gtq` | Falta `presupuesto_gtq` en metas de ingresos. |
| `legacy_objetivos_import` | Hay resultados con nota «Importado desde … Objetivos» (migrar a operación). |
| `modo2_stale_objetivos` | Datos Objetivos legacy más recientes que score modo2. |
| `vc_without_operational_import` | VC medido > 0 sin `CrossSaleImportHeader` del mes. |
| `reqs_from_excel_objetivos` | MRC con nota de sync desde Excel Objetivos. |
| `recalc_pending` | El período aparece en pendientes del recálculo global. |
| `validate_hint` | Recordatorio del validador CLI (solo si `ALLOW_PGC_EXCEL_IMPORT=1`). |

Las banderas se muestran en pantallas del centro de operaciones (inicio, tablero mensual, ingresos año, etc.) vía `templates/pgc/admin/_ops_flags.html`.
