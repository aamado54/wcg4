# PGC — Cierre mensual (operación)

Guía operativa para el **Centro de operaciones** del tablero PGC: importaciones, Objetivos, requerimientos, tipo de cambio, recálculo y validación contra Excel.

## Resumen post-mortem (cierre ene–jul 2026)

Tras alinear modo2 con la hoja Objetivos se documentaron estos puntos de fallo recurrentes:

1. **Import Objetivos incompleto** — metas de ingresos sin `presupuesto_gtq` o ejecución sin nota «Importado desde … Objetivos» en `MonthlyMetricResult`.
2. **Score modo2 desactualizado** — se importó Objetivos pero no se recalculó el período; el tablero 2.Proporción quedó anterior al import.
3. **Recálculo global con pendientes** — ingresos STALE, TC faltante, Investment o score incompleto sin corregir antes del cierre.
4. **Validación manual omitida** — no se ejecutó el validador CLI contra el Excel de referencia antes de publicar cifras.

El centro de operaciones muestra **banderas** (`pgc/ops_flags.py`) con mensajes en español y pasos de corrección.

## Checklist de cierre

| Paso | Dónde | Acción |
|------|--------|--------|
| 1 | Tablero mensual | Subir y procesar cargas (financiero, clientes, venta cruzada) por mes. |
| 2 | TC | Editar tipo de cambio del mes antes de capturar ingresos en Q. |
| 3 | Objetivos | `python manage.py import_pgc_objetivos <archivo.xlsx> --year AAAA --month MM` |
| 4 | Ingresos | Matriz anual o captura manual; revisar banderas STALE/TC. |
| 5 | Reqs | Matriz anual de requerimientos o edición manual. |
| 6 | Recálculo | «Recalcular período» en tablero mensual o recálculo inteligente si hay pendientes. |
| 7 | Validación | CLI contra Excel (ver abajo). |
| 8 | Revisión | Tablero gerencial y bloque revisión del hub. |

## Import desde Objetivos

Comandos habituales (desde `dashboard/`):

```bash
python manage.py import_pgc_objetivos /ruta/PGC-Objetivos.xlsx --year 2026 --month 7
# Alternativa TSV legacy:
python manage.py import_pgc_objetivos_tsv /ruta/datos.tsv --year 2026 --month 7
```

Tras el import debe haber:

- Notas en resultados con texto **Importado desde … Objetivos**.
- `presupuesto_gtq` en metas **INGRESOS** por UNE del mes (presupuesto comisiones GTQ).

Si falta alguno, el hub muestra la bandera **Mes sin sincronía completa con Objetivos**.

## Recálculo

El estado global (`get_global_recalc_status`) lista períodos con motivos (STALE, score incompleto, Investment, etc.).

- Corrija la causa (p. ej. complete TC en la matriz de ingresos).
- Ejecute recálculo desde el tablero mensual o el flujo de recálculo inteligente.

Banderas **Recálculo pendiente** y **Score modo2 anterior al último import Objetivos** apuntan a este paso.

## Validación Excel

Script en `tools/pgc/validate_ejecucion_excel.py`. Compara modo2 en base de datos con columnas S–X de la hoja Objetivos (puntos y calificación mensual).

```bash
cd dashboard
python tools/pgc/validate_ejecucion_excel.py /ruta/archivo-referencia.xlsx --year 2026
```

Opciones útiles: `--month MM`, `--mode modo2` (por defecto proporción). Ver también `docs/pgc-puntos-proporcion-objetivos.md`.

## Banderas en la UI

| Código | Significado |
|--------|-------------|
| `objetivos_sync` | Falta import Objetivos o `presupuesto_gtq` en ingresos. |
| `modo2_stale_objetivos` | Import Objetivos más reciente que el score modo2. |
| `recalc_pending` | El período aparece en pendientes del recálculo global. |
| `validate_hint` | Recordatorio del validador CLI (enlace a esta sección). |

Las banderas se muestran en pantallas del centro de operaciones (inicio, tablero mensual, ingresos año, etc.) vía `templates/pgc/admin/_ops_flags.html`.
