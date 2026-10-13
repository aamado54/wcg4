# PGC — Puntos en proporción (Tablero) y hoja Objetivos

Documento de **procedimiento acordado** para alinear el Tablero PGC (modalidad **2.Proporción**) con la hoja **Objetivos** del archivo de cumplimiento (p. ej. `Cumplimiento Objetivos PGC … (Notas).xlsx`).

**Estado:** implementado en `recalc_pgc` (modo2), `pgc/objetivos_scoring.py`, import Objetivos (`presupuesto_gtq` en `MonthlyTarget`).

**Principio rector:** la hoja del autor del PGC es la **referencia oficial** para los **puntos de ejecución** del Tablero (columnas equivalentes a **S–W** en Excel). La aplicación solo debe **desviarse** cuando exista una razón poderosa, documentada y aceptada (ver §6).

---

## 1. Qué cubre este documento y qué no

| Ámbito | Fuente / regla |
|--------|----------------|
| **Tablero — puntos por métrica** (Ingresos, Clientes, VC, Reqs, Total, Clasifica) en **2.Proporción** | Procedimiento **Objetivos** (este documento) |
| **Ingresos vs meta** — meta y ejecutado en **miles de US$** | Política PGC en dólares + imports (`import_pgc_objetivos`, TC, `import_pgc_metas`) |
| **Inversiones — tabla de crecimiento neto** (validada al centavo) | Crecimiento neto mensual dolarizado (AP+PG ± bancos según reglas ya acordadas); **no** sustituir por saldo GTQ de la hoja |
| **1.Absolutos** (modo1) | Binario: cumple meta → puntos completos; no cumple → 0 (sin cambio) |

El Tablero puede mostrar dos modalidades; **la comparación con el autor** se hace en **2.Proporción** usando las fórmulas de abajo.

---

## 2. Por qué hay un procedimiento “excepcional” en quetzales

- La **política y los reportes operativos** del PGC (metas de ingresos, ejecutado, Ingresos vs meta, textos de comité) se expresan en **miles de US$**.
- En la hoja **Objetivos**, los **puntos de ingresos** de Factoraje, Leasing e Insurance se calculan con una proporción sobre **comisiones presupuesto vs comisiones ejecución en GTQ** (columnas D e I), **sin usar el tipo de cambio dentro de la razón**.
- Esa práctica es **histórica y coherente en la hoja** (reproducible mes a mes); no es un error de tipeo aislado.
- Se adoptará **como procedimiento oficial del Tablero (puntos de ingresos)** para esas tres UNE, documentado explícitamente como **excepción al criterio general en USD**: solo afecta al **otorgamiento de puntos** en proporción, no redefine el ejecutado en dólares ni las metas en miles USD.

**Implementación:** `MonthlyTarget.presupuesto_gtq` (import Objetivos) o, si falta, **fallback** `presupuesto_gtq = meta_miles × 1000` (convención de la hoja: columna D en GTQ = meta en miles × 1000). Ejecución GTQ en `MonthlyMetricResult.source_value`. El reporte **Ingresos vs meta** sigue en miles USD.

---

## 3. Fórmulas oficiales (puntos de ejecución — estilo Objetivos)

Notación:

- `P_ing`, `P_cli`, `P_vc`, `P_req` = puntos meta del mes (columnas **O–R** en Excel: “Pts Ingresos”, “Pts Clientes Nuevos”, etc.).
- `min(1, x)` = tope al 100 % del presupuesto (no se premia superar el presupuesto en la proporción base).

### 3.1 Ingresos — Factoraje (WC), Leasing (WCL), Insurance (WCI)

**Procedimiento excepcional (GTQ):**

```
ratio_ing = ejecucion_comisiones_GTQ / presupuesto_comisiones_GTQ   (si presupuesto > 0)
puntos_ing_ejec = P_ing × min(1, max(0, ratio_ing))
```

- Si `ejecucion_comisiones_GTQ < 0` → `puntos_ing_ejec = 0` (mes con comisión negativa en la hoja).
- Redondeo: alinear con la hoja (típicamente **2 decimales** en puntos; confirmar en un mes patrón antes de codificar).

**Ejemplo (Factoraje, ago-2026):**  
`P_ing = 70`, ejec. 460 285 GTQ, pres. 770 000 GTQ → `70 × (460 285/770 000) = 41,84`.

**No usar para estos puntos:** `P_ing × (ejecutado_miles_USD / meta_miles_USD)` — produce cifras distintas (p. ej. ~5,5 vs 41,84 en el mismo mes) porque la meta en USD y el presupuesto GTQ no definen la misma razón.

### 3.2 Ingresos — Inversiones (WCINV)

En la hoja, la columna de “comisiones” refleja **magnitud/saldo en GTQ**, no el **crecimiento neto** en miles USD del reporte de inversiones ya validado.

**Procedimiento oficial Tablero (alineado al autor):**

```
ratio_inv = ejecucion_comisiones_GTQ / presupuesto_comisiones_GTQ   (presupuesto > 0)
puntos_ing_ejec = P_ing × min(1, max(0, ratio_inv))
```

- Meses con ejecución GTQ **negativa** → `puntos_ing_ejec = 0` (como ene–abr 2026 en la hoja).
- Meses con ratio ≥ 1 → puntos completos `P_ing` (p. ej. jul–ago 2026 → **70** en la hoja).

**Razón poderosa para no mezclar con el ejecutado de Ingresos vs meta:** el crecimiento neto mensual en USD es el indicador operativo acordado y validado; cambiarlo para cuadrar puntos rompería esa validación. Por tanto:

- **Ingresos vs meta (Inversiones):** sigue el **crecimiento neto** en miles USD.
- **Tablero (puntos ing Inversiones):** sigue la **proporción GTQ** de la hoja Objetivos, como procedimiento excepcional análogo al §2.

Si en el futuro el autor unifica ambos conceptos en una sola columna, se actualizará este documento.

### 3.3 Clientes nuevos (todas las UNE con meta de clientes)

```
ratio_cli = clientes_ejecucion_mes / clientes_presupuesto_mes
puntos_cli_ejec = P_cli × min(1, max(0, ratio_cli))
```

- Conteos **adimensionales**; no implican excepción GTQ/USD.
- Coincide con la práctica habitual de la hoja (validado ene–ago 2026 salvo casos de redondeo).

### 3.4 Venta cruzada

```
ratio_vc = referidos_VC_ejecucion / referidos_VC_presupuesto
puntos_vc_ejec = P_vc × min(1, max(0, ratio_vc))
```

- Columnas **L–N** (Referidos objetivo / presupuesto VC / ejecución VC) en Objetivos.

### 3.5 Respuesta a requerimientos (OA)

**Factoraje, Leasing, Inversiones:** en la hoja, puntos de ejecución de reqs suelen ser **0 o 5** según cumplimiento (binario), alineado con `P_req` cuando aplica.

**Insurance (excepción de negocio, documentada en UI):** la hoja marca **“NO APLICA”** y **0** puntos de reqs. Por ahora la app **sí otorga los puntos provisionales** (p. ej. 5) vía cumplimiento manual, porque aún falta información y no se penaliza a Insurance con el mismo esquema que otras UNE. Esa decisión **no** se presenta como equivalente a la hoja: en **Tablero** y **Respuesta reqs** aparece una **nota visible** (`INSURANCE_REQS_GRACE_NOTE` en `pgc/objetivos_scoring.py`).

**Otras UNE:** reqs en modo2 = **binario** (cumple manual → `P_req`; no cumple → 0).

### 3.6 Total y Clasifica

```
total_puntos = puntos_ing_ejec + puntos_cli_ejec + puntos_vc_ejec + puntos_req_ejec
```

**Clasifica mes:** según regla ya existente en la hoja y en la app (`is_month_qualified`), típicamente **total ≥ umbral** (80 puntos por defecto en `MonthlyModeScorecard`). La columna **Califica mes** de la hoja es la referencia para validar; **Califica trimestre** queda fuera del alcance del Tablero mensual salvo reporte aparte.

---

## 4. Implementación en código

| Pieza | Ubicación |
|-------|-----------|
| Fórmulas Objetivos | `pgc/objetivos_scoring.py` |
| Modo2 Tablero | `core/management/commands/recalc_pgc.py` → `apply_modo2` (sin reservas de puntos) |
| Presupuesto comisiones GTQ | `MonthlyTarget.presupuesto_gtq` (import Objetivos / TSV) |
| Ejecución comisiones GTQ | `MonthlyMetricResult.source_value` (moneda GTQ) |
| Import masivo TSV | `import_pgc_objetivos_tsv` |
| Nota Insurance reqs | Tablero + Respuesta reqs + constante `INSURANCE_REQS_GRACE_NOTE` |

**Modo1** sin cambios (binario USD).

### 4.1 Validación cruzada USD / GTQ (Ingresos vs meta)

- **Default:** montos en **miles USD** (política PGC).
- Selector **Moneda → GTQ (Objetivos)** en Ingresos vs meta: muestra **Meta GTQ** (`presupuesto_gtq`) y **Ejec. GTQ** (`source_value`) para cuadre con el autor; columna **Ref. USD** con miles oficiales.
- Los **puntos** de ingresos en 2.Proporción usan la razón **GTQ** cuando existe `presupuesto_gtq` (§3.1).

---

## 5. Datos de entrada y validación

| Dato | Origen previsto |
|------|------------------|
| Presupuesto / ejecución comisiones GTQ, clientes, VC | Hoja **Objetivos** (`import_pgc_objetivos` o equivalente) |
| `P_ing` … `P_req` | Columnas meta de puntos en la misma hoja (O–R) o `MonthlyTarget.points_if_achieved` si están sincronizados |
| Ejecutado miles USD (reportes) | Imports + TC; **no** reemplaza las columnas GTQ para puntos §3.1–3.2 |
| Crecimiento neto Inversiones (USD) | `investment_ingresos` / imports AP+PG (+ reglas bancarias acordadas) |

**Validación:** por cada mes/UNE, comparar puntos calculados con columnas **S–V** y total de la hoja (tolerancia acordada, p. ej. ±0,01 en puntos). Producción: base **Railway** (Postgres), no SQLite local.

---

## 6. Cuándo **no** seguir al autor (solo razón poderosa)

| Situación | Acción |
|-----------|--------|
| **Crecimiento neto Inversiones** en Ingresos vs meta / tabla validada | Mantener USD neto; no sustituir por saldo GTQ de la hoja |
| **Política escrita PGC** en USD para comunicación externa | Ingresos vs meta y metas oficiales siguen en miles USD; la excepción GTQ queda **acotada a puntos Tablero** §3.1–3.2 |
| **Error aritmético demostrable** en la hoja (fórmula inconsistente con el resto del libro en el mismo mes) | Corregir en app y anotar el mes; informar al autor |
| **Reservas de puntos (modo2 app)** | No aplicar al Tablero “Objetivos” salvo que negocio extienda la política |
| **Insurance reqs = 5** en app vs **0 / NO APLICA** en hoja | **Excepción firmada:** puntos provisionales + nota en reportes (§3.5) |

No se cambiará el procedimiento validado de **inversiones en miles USD** solo para igualar un saldo GTQ en la hoja.

---

## 7. Operación en Railway

Tras desplegar migración `0008_monthlytarget_presupuesto_gtq`:

```bash
python manage.py import_pgc_objetivos_tsv --path data/now/Cumplimiento...Objetivos.tsv --year 2026
# Recálculo inteligente desde admin o:
python manage.py recalc_pgc --year=2026 --month=M --mode=modo2  # por mes pendiente
```

Cuadre: Tablero en **2.Proporción** vs columnas S–W del TSV; Ingresos vs meta en USD o GTQ según selector.

---

## 8. Referencias en el repo

- Código actual modo1/modo2: `core/management/commands/recalc_pgc.py`
- Import ejecución Objetivos: `pgc/management/commands/import_pgc_objetivos.py`
- Tablero: `pgc/views.py`, `templates/pgc/dashboard.html`
- Contexto PGC general: `docs/pgc_vs_pgo_explicacion.md`

---

*Última revisión: 2026-09-29 — borrador para alineación con autor de hoja Objetivos.*
