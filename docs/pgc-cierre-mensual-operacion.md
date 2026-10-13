# PGC — Cierre mensual (operación)

Guía operativa para el **Centro de operaciones** del tablero PGC: importaciones, tipo de cambio, recálculo y cuadre opcional contra el libro de validación (**sin importarlo**).

## Regla de oro

| Libro *Cumplimiento Objetivos PGC* (hoja Objetivos) | Acción |
|-----------------------------------------------------|--------|
| En producción | **No importar** (`import_pgc_objetivos` bloqueado) |
| Cuadre externo | `validate_ejecucion_excel.py` — **solo lectura**, no escribe en BD |

Mapa completo métrica → comando: [pgc-sin-excel-objetivos-validacion.md#mapa-fuentes-operativas](pgc-sin-excel-objetivos-validacion.md#mapa-fuentes-operativas).

## Resumen post-mortem (cierre ene–jul 2026)

1. **Dependencia del libro Objetivos** — ejecución cargada desde Excel en lugar de ER/`import_ingresos`.
2. **Metas de ingresos sin `presupuesto_gtq`** — proporción modo2 incorrecta o bandera en hub.
3. **Score modo2 desactualizado** — cambios en datos sin recalcular el período.
4. **Recálculo global con pendientes** — ingresos STALE, TC faltante, Investment o score incompleto.
5. **Validación manual omitida** — no se ejecutó el validador CLI antes de publicar cifras (opcional).

El centro de operaciones muestra **banderas** (`pgc/ops_flags.py`) con mensajes en español y pasos de corrección.

## Política operativa (2026 en adelante)

| Dato | Fuente oficial | Libro Objetivos |
|------|----------------|-----------------|
| **Comisiones / INGRESOS** | `import_ingresos` (xlsx ER), matriz anual, hub financiero | **No importar** |
| **Clientes nuevos** | Hub / `import_clientes_nuevos` | **No importar** |
| **Venta cruzada** | Cargas VC / `import_venta_cruzada`; política **VC=0** sin cross-sale real | **No importar** |
| **Inversiones / bancos** | CSV + `recalc_investment_ingresos_from_new_clients` | **No importar** |
| **Requerimientos** | Matriz anual / edición manual | **No importar** |
| **Puntos / metas** | `import_pgc_metas` (TSV) | Solo validación CLI |

## Checklist equipo operación (cierre mensual)

Use este orden en **Centro de operaciones** (`/admin-hub/`):

| # | Pantalla / ruta | Qué hacer | Comando equivalente (CLI) |
|---|-----------------|-----------|---------------------------|
| 1 | **1. Tablero mensual** | Confirmar año-mes del cierre | — |
| 2 | **2. Ingresos (año completo)** | Registrar **tipo de cambio** del mes | — |
| 3 | **1. Tablero mensual** → Estados de resultados | Subir ER Factoraje (`WCF…`) y Leasing (`WCL…`); procesar | `import_ingresos --path … --year Y --month M` |
| 4 | Mismo bloque / matriz | Insurance (`WCI…`) si aplica | `import_ingresos` |
| 5 | **Importación general** | Clientes nuevos CSV del mes | `import_clientes_nuevos` |
| 6 | Importación general | Inversiones crecimiento + bancos (si reportan) | `import_inversiones_crecimiento`, `import_bancos_fin_mes` |
| 7 | Tablero mensual | Venta cruzada **solo** si hay archivo real; si no, VC=0 | `import_venta_cruzada` |
| 8 | **3. Requerimientos (año completo)** | Capturar cumplimiento OA cuando exista reporte | (UI) |
| 9 | Tablero → **Revisar resultado** | **Recalcular período**; corregir banderas rojas | `recalc_pgc --year=Y --month=M --mode=modo2` |
| 10 | (Opcional, soporte) | Cuadre contra libro de validación **sin cargar datos** | `python tools/pgc/validate_ejecucion_excel.py --path …` |
| 11 | Tablero gerencial | Revisión final y cierre del mes | — |

**No hacer en producción:** `import_pgc_objetivos`, `import_pgc_objetivos_tsv`, ni subir el libro de validación como “carga mensual”.

## Comandos Objetivos (bloqueados en producción)

```bash
# NO usar en cierre mensual normal:
# python manage.py import_pgc_objetivos ...
# python manage.py import_pgc_objetivos_tsv ...
```

Desbloqueo solo dev/migración: `ALLOW_PGC_EXCEL_IMPORT=1` o `--force-legacy-excel`.

**Comisiones:** siempre `import_ingresos` y el hub financiero; ver [pgc-sin-excel-objetivos-validacion.md](pgc-sin-excel-objetivos-validacion.md#comisiones-factoraje-y-leasing-import_ingresos).

Ejemplo CLI:

```bash
cd dashboard
python manage.py import_ingresos --path /ruta/WCF202609.xlsx --year 2026 --month 9
python manage.py import_ingresos --path /ruta/WCL202609.xlsx --year 2026 --month 9
```

### Limpieza de datos heredados (VC / reqs / notas Objetivos)

```bash
python manage.py clear_operational_fiction_from_objetivos --year 2026 --months 8,9
python manage.py clear_operational_fiction_from_objetivos --year 2026 --months 8,9 --dry-run
```

Si aparece `legacy_objetivos_import`, reemplace ejecución con `import_ingresos` y recalcule.

## Recálculo {#recalculo}

El estado global (`get_global_recalc_status`) lista períodos con motivos (STALE, score incompleto, Investment, etc.).

- Corrija la causa (p. ej. complete TC en la matriz de ingresos).
- Ejecute recálculo desde el tablero mensual o el flujo de recálculo inteligente.

## Validación Excel (opcional, solo lectura) {#validacion-excel}

Script en `tools/pgc/validate_ejecucion_excel.py`. Compara modo2 en base de datos con columnas S–X de la hoja Objetivos del **libro de validación**. **No importa datos ni requiere `ALLOW_PGC_EXCEL_IMPORT`.** No es paso obligatorio del cierre operativo.

```bash
cd dashboard
python tools/pgc/validate_ejecucion_excel.py --path /ruta/archivo-referencia.xlsx --year 2026 --month 9
```

Opciones útiles: `--months all`, `--scores-only`, `--mode modo2`. Ver [pgc-puntos-proporcion-objetivos.md](pgc-puntos-proporcion-objetivos.md).

## Banderas en la UI

| Código | Significado |
|--------|-------------|
| `ingresos_presupuesto_gtq` | Falta `presupuesto_gtq` en metas de ingresos. |
| `legacy_objetivos_import` | Hay resultados con nota «Importado desde … Objetivos» (migrar a operación). |
| `modo2_stale_objetivos` | Datos Objetivos legacy más recientes que score modo2. |
| `vc_without_operational_import` | VC medido > 0 sin `CrossSaleImportHeader` del mes. |
| `reqs_from_excel_objetivos` | MRC con nota de sync desde Excel Objetivos. |
| `recalc_pending` | El período aparece en pendientes del recálculo global. |
| `validate_hint` | Recordatorio del validador CLI (solo lectura, sin import). |

Las banderas se muestran en pantallas del centro de operaciones vía `templates/pgc/admin/_ops_flags.html`.
