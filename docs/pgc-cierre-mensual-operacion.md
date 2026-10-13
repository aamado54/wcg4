# PGC — Cierre mensual (operación)

Guía operativa para el **Centro de operaciones** del tablero PGC: importaciones, Objetivos, requerimientos, tipo de cambio, recálculo y validación contra Excel.

## Resumen post-mortem (cierre ene–jul 2026)

Tras alinear modo2 con la hoja Objetivos se documentaron estos puntos de fallo recurrentes:

1. **Import Objetivos incompleto** — metas de ingresos sin `presupuesto_gtq` o ejecución sin nota «Importado desde … Objetivos» en `MonthlyMetricResult`.
2. **Score modo2 desactualizado** — se importó Objetivos pero no se recalculó el período; el tablero 2.Proporción quedó anterior al import.
3. **Recálculo global con pendientes** — ingresos STALE, TC faltante, Investment o score incompleto sin corregir antes del cierre.
4. **Validación manual omitida** — no se ejecutó el validador CLI contra el Excel de referencia antes de publicar cifras.

El centro de operaciones muestra **banderas** (`pgc/ops_flags.py`) con mensajes en español y pasos de corrección.

## Política operativa (2026 en adelante)

| Dato | Fuente oficial | Excel Objetivos |
|------|----------------|-----------------|
| **Comisiones / INGRESOS** | `import_ingresos`, matriz anual, cargas financieras | Opcional / deprecado para ejecución |
| **Clientes nuevos** | Objetivos o captura operativa | Sí (clientes) |
| **Venta cruzada** | Cargas VC / `import_venta_cruzada`; política **VC=0** sin cross-sale real | **No** (salvo `--sync-vc` explícito) |
| **Requerimientos** | Matriz anual / edición manual | **No** (salvo `--sync-reqs` explícito; reqs no reportados vía Excel) |

## Checklist de cierre

| Paso | Dónde | Acción |
|------|--------|--------|
| 1 | Tablero mensual | Subir y procesar cargas (financiero, clientes, venta cruzada) por mes. |
| 2 | TC | Editar tipo de cambio del mes antes de capturar ingresos en Q. |
| 3 | Ingresos | `import_ingresos` o matriz anual; revisar banderas STALE/TC. |
| 4 | Objetivos (opcional) | `import_pgc_objetivos` solo clientes/puntos; **sin** VC/reqs por defecto. |
| 5 | Reqs | Matriz anual de requerimientos o edición manual (no Excel Objetivos). |
| 6 | Recálculo | «Recalcular período» en tablero mensual o recálculo inteligente si hay pendientes. |
| 7 | Validación | CLI contra Excel (ver abajo), si aplica. |
| 8 | Revisión | Tablero gerencial y bloque revisión del hub. |

## Import desde Objetivos

Comandos habituales (desde `dashboard/`):

```bash
# Por defecto: no escribe VC ni ManualRequirementsCompliance
python manage.py import_pgc_objetivos /ruta/PGC-Objetivos.xlsx --year 2026 --month 7

# Solo si necesita reproducir legacy Excel (no recomendado en operación):
python manage.py import_pgc_objetivos /ruta/archivo.xlsx --year 2026 --month 7 --sync-vc --sync-reqs

# Alternativa TSV legacy (clientes/comisiones; sin VC/reqs en ruta TSV):
python manage.py import_pgc_objetivos_tsv /ruta/datos.tsv --year 2026 --month 7
```

**Comisiones:** usar `import_ingresos` y la matriz de ingresos; no depender del Excel Objetivos para ejecución de comisiones.

Tras un import de clientes/puntos puede haber:

- Notas en resultados con texto **Importado desde … Objetivos** (clientes; comisiones solo si aún se importan desde Excel).
- `presupuesto_gtq` en metas **INGRESOS** cuando el import lo actualiza o cuando se captura vía ingresos.

Si falta sincronía esperada con Objetivos (p. ej. presupuesto GTQ), el hub muestra la bandera **Mes sin sincronía completa con Objetivos**.

### Limpieza de datos heredados (VC / reqs desde Excel)

```bash
python manage.py clear_operational_fiction_from_objetivos --year 2026 --months 8,9
python manage.py clear_operational_fiction_from_objetivos --year 2026 --months 8,9 --dry-run
```

Pone **VENTA_CRUZADA** en 0 por UNE y elimina `ManualRequirementsCompliance` de Factoraje, Leasing e Inversiones (conserva Insurance).

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
| `vc_without_operational_import` | VC medido > 0 sin `CrossSaleImportHeader` del mes. |
| `reqs_from_excel_objetivos` | MRC con nota de sync desde Excel Objetivos. |
| `recalc_pending` | El período aparece en pendientes del recálculo global. |
| `validate_hint` | Recordatorio del validador CLI (enlace a esta sección). |

Las banderas se muestran en pantallas del centro de operaciones (inicio, tablero mensual, ingresos año, etc.) vía `templates/pgc/admin/_ops_flags.html`.
