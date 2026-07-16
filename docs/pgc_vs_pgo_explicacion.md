# PGC vs PGO

Documento de evidencia del sistema integrado en `~/wc/wcg4/dashboard`.
Solo afirma lo verificado en código, modelos, vistas, templates, comandos y docs del repo.
Si no hay soporte suficiente, se indica explícitamente.

---

## PGC

### Información usada

**Modelos principales (app `pgc`, tablas `pgc_*`):**

- `PGCPlan` — plan por año.
- `MonthlyTarget` — meta mensual por UNE y métrica.
- `MonthlyMetricResult` — valor medido (ingresos, clientes, venta cruzada, reqs, etc.).
- `MonthlyMetricScore` — puntos por métrica dentro de un `MonthlyModeScorecard`.
- `MonthlyModeScorecard` — total del mes por UNE y modalidad (`modo1` / `modo2`):
  - `total_points`
  - `qualified_threshold` (default **80** en modelo y en recalc)
  - `is_month_qualified` (booleano “Clasifica”)
- `MonthlyExchangeRate` — TC USD↔GTQ por mes.
- `ManualRequirementsCompliance` — override manual de respuesta a requerimientos.

**Métricas (`core.MetricDefinition`):** códigos `INGRESOS`, `CLIENTES_NUEVOS`, `VENTA_CRUZADA`, `RESPUESTA_REQS`.

**UNEs (`core.UNE`):** FACTORING, LEASING, INSURANCE, INVESTMENT.

**Imports (`imports`):**

- `FileUpload` + detector `guess_file_type_and_period`.
- `NewClientImportHeader` / `NewClientImportRow` — clientes nuevos (también fuente de ingresos Investment).
- `CrossSaleImportRow` — venta cruzada.
- Estado de resultados vía comando `import_ingresos` (tipo FINANCIAL).

**Períodos:** año/mes en targets, resultados y scorecards.

**Dependencias relevantes:**

- Recálculo inteligente: `pgc/admin_recalc.py` → cadena STALE ingresos → Investment desde clientes → `recalc_pgc`.
- Ingresos Investment: `pgc/investment_ingresos.py` + comando `recalc_investment_ingresos_from_new_clients`.

### Procesamiento

1. **Carga:** Administración mensual (`pgc/admin_views.py`, `pgc/admin_period.py`) sube `FileUpload` y procesa con `import_clientes_nuevos`, `import_venta_cruzada`, `import_ingresos`.
2. **Persistencia operativa:** filas en `NewClientImportRow` / `CrossSaleImportRow` / métricas de ingresos en `MonthlyMetricResult`.
3. **Score:** comando `core/management/commands/recalc_pgc.py`:
   - Lee `MonthlyMetricResult` + `MonthlyTarget` por UNE/métrica/mes.
   - `apply_modo1` / `apply_modo2` asignan `points_awarded` en `MonthlyMetricScore`.
   - Suma a `MonthlyModeScorecard.total_points`.
   - Define clasificación: `is_month_qualified = total_points >= qualified_threshold` (default 80).
4. **Tablero:** vista `pgc.views.pgc_dashboard` → template `templates/pgc/dashboard.html` (columnas Ingresos, Clientes nuevos, Venta cruzada, Respuesta reqs, Total, Clasifica).

### Análisis / comparación

**Implementado actualmente:**

- Por métrica: comparación **meta (`target_value`) vs real (`measured_value`)** para otorgar puntos (`recalc_pgc.apply_modo1` / `apply_modo2`).
- Por UNE/mes/modo: **suma de puntos** → umbral → `is_month_qualified` (Sí/No = Clasifica).
- UI: filas coloreadas según `is_month_qualified` (`row-clasifica-si` / `row-clasifica-no` en `dashboard.html`).

**Documentado** (alineado con lo anterior en lo esencial): pantallas históricas con esas columnas y estado Clasifica; umbral ~80 puntos.

### Qué sí está claro

- Existe pipeline completo: import → resultados → score → Clasifica booleana calculada.
- Umbral default 80 está en modelo `MonthlyModeScorecard` y en `recalc_pgc.py`.
- El tablero productivo del menú (`/tablero/`) usa ese booleano.

### Qué falta confirmar

- Detalle fino de todas las reglas `modo2` por métrica (el código las tiene; este documento no reescribe cada fórmula).
- Si en producción siempre se recalcula tras cada carga (depende del uso del botón “Recalcular pendientes” / admin).

---

## PGO

### Información usada

Hay **dos implementaciones coexistentes**:

#### A) PGO operativo / productivo del menú (`app` `pgo/`, URL `/pgo/`)

- `Ticket` — tickets operativos (estado, fechas, `sla_horas`, unidad, entidad).
- `TicketEvento` — bitácora.
- `PgoResultadoPeriodo` — agregado mensual por unidad:
  - `tickets_cerrados`, `tickets_abiertos`
  - `tiempo_promedio_horas`
  - `cumplimiento_sla_pct`
- **No** hay campos `puntaje_total`, `clasifica`, `puntos` ni `peso` en estos modelos.

#### B) PGO WCG One (`apps/pgo/`, URL `/wcgone/pgo/`)

- `Ticket` (schema WCG One) con `sla_horas`, `sla_cumplido`.
- `PgoMetricRule` — `puntos`, `peso`, `formula_texto`, etc. (catálogo de reglas).
- `PgoPeriodScore` — `puntaje_total`, **`clasifica` (BooleanField default=False)**, `detalle_json`.
- `PgoMonthlyAgg` — agregados de tickets (recibidos/cerrados/SLA counts); sin Clasifica.

### Procesamiento

#### A) `pgo/` (productivo menú)

1. Import: `pgo/services.py` → `import_tickets` → modelo `Ticket`.
2. Tras import o al abrir dashboard: `pgo/periodo.recalculate_pgo_periodos()`.
3. Cálculo real encontrado:
   - Agrupa tickets por período (`YYYY-MM` de `fecha_apertura`) y unidad.
   - Cerrados / abiertos.
   - Horas promedio de cierre.
   - `% SLA` = cerrados con `(fecha_cierre - fecha_apertura) <= sla_horas` / cerrados con fechas.
4. Dashboard: `pgo.views.dashboard` → `templates/pgo/pgodashboard.html`  
   Columnas: Período, Unidad, Cerrados, Abiertos, T. promedio, **SLA %**.  
   **Sin columna Clasifica. Sin color Sí/No.**

#### B) `apps/pgo/`

1. Import tickets: `apps/pgo/imports/tickets.py` (incluye `sla_cumplido` por ticket).
2. Vista `apps/pgo/views.resultados` **solo lee** `PgoPeriodScore` y `PgoMonthlyAgg`.
3. Template `templates/wcgone/pgo/resultados.html` muestra Puntaje + Clasifica.
4. **No se encontró** comando / servicio que:
   - cree/actualice `PgoPeriodScore`,
   - sume puntos desde `PgoMetricRule`,
   - asigne `clasifica` según umbral (p. ej. ≥80).

Búsqueda en código: no hay `recalc_pgo`; asignaciones a `puntaje_total` / `clasifica` solo aparecen como definición de modelo.

### Análisis / comparación

| Fuente | Qué dice | Estado vs código |
|--------|----------|------------------|
| Docs (`Documento-1`, `documento-2`, `documento-3`) | PGO con puntaje total ~100 y **clasifica desde 80 puntos**; reglas por unidad | **Documentado** |
| `apps/pgo` modelos | Campos `puntaje_total`, `clasifica`, reglas con `puntos`/`peso` | **Schema implementado** |
| `apps/pgo` lógica de cálculo de score | — | **Faltante / no verificable en código** |
| Docs / demo (`06-guia-demo-operativa.md`) | “Scoring PGO avanzado \| Pendiente” | Coherente con el faltante |
| `pgo/periodo.py` | Compara duración vs `sla_horas` por ticket cerrado | **Implementado** (SLA %, no Clasifica) |
| Umbral SLA → “Clasifica” | — | **No implementado** (no hay regla tipo SLA% ≥ X → clasifica) |

**Tensión docs vs código (resolución basada solo en evidencia):**

- La definición documental de “Clasifica con nota ≥ 80” **no está implementada** como cálculo en el sistema actual.
- Lo que **sí** está implementado en el menú principal PGO es el tablero operacional basado en tickets y `PgoResultadoPeriodo` (SLA y volúmenes).
- `PgoPeriodScore.clasifica` es un **campo persistido + UI**; sin escritor/calculador encontrado, su valor efectivo depende de carga manual/admin/seeds no evidenciadas en esta revisión (default `False`).

### Qué sí está claro

- Pipeline operativo tickets → `PgoResultadoPeriodo` existe y se usa en `/pgo/`.
- Schema de scoring WCG One existe y la pantalla `/wcgone/pgo/resultados/` puede mostrar Clasifica.
- Estilos verde/rojo (mismo patrón PGC) se aplicaron **solo** a la tabla de `PgoPeriodScore` leyendo `clasifica` real, sin inventar el cálculo.

### Qué falta confirmar / faltante para paralelismo con PGC

- Implementar (si se desea) un recálculo que use `PgoMetricRule` → `puntaje_total` → `clasifica = puntaje_total >= 80` (u otro umbral parametrizado).
- Decidir si el menú productivo debe apuntar a resultados WCG One o extender `PgoResultadoPeriodo` con clasificación derivada de una regla explícita.
- Hoy **no** es legítimo pintar verde/rojo en `pgodashboard.html` como “Clasifica”, porque no hay booleano ni umbral implementado allí.

---

## Diferencias prácticas entre PGC y PGO

| Aspecto | PGC (productivo) | PGO menú (`/pgo/`) | PGO WCG One (`/wcgone/pgo/`) |
|---------|------------------|--------------------|------------------------------|
| Comparación principal | Meta vs real → puntos | SLA tiempo vs `sla_horas` | Tickets/SLA; score schema sin motor |
| Total puntuable | `MonthlyModeScorecard.total_points` | No | `PgoPeriodScore.puntaje_total` (sin calculator hallado) |
| Clasifica | `is_month_qualified` calculado (≥ umbral, default 80) | No existe | Campo `clasifica` sin calculator hallado |
| Filas verde/rojo | Sí (`dashboard.html`) | No | Sí en `resultados.html` si hay filas (lee booleano) |
| Recalc score | `recalc_pgc` | `recalculate_pgo_periodos` (solo agregados) | No encontrado |

---

## Recomendación mínima de coherencia visual y analítica

1. **Visual:** Mantener el mismo par de fondos PGC (cian = Sí, ámbar = No) donde exista un booleano real de clasificación (`is_month_qualified` / `PgoPeriodScore.clasifica`).
2. **Analítico:** No equivaler `cumplimiento_sla_pct` a Clasifica hasta documentar e implementar un umbral explícito en código.
3. **Cierre de gaps:** Si el negocio quiere “Clasifica ≥ 80” en PGO, falta un servicio/comando de score que escriba `PgoPeriodScore` (hoy solo está el schema y la UI).

---

## Referencias de archivos citados

- `pgc/models.py`, `pgc/views.py`, `templates/pgc/dashboard.html`
- `core/management/commands/recalc_pgc.py`
- `pgc/admin_recalc.py`, `pgc/investment_ingresos.py`
- `imports/models.py`, comandos `import_*`
- `pgo/models.py`, `pgo/periodo.py`, `pgo/views.py`, `templates/pgo/pgodashboard.html`
- `apps/pgo/models.py`, `apps/pgo/views.py`, `templates/wcgone/pgo/resultados.html`
- Docs: `docs/Documento-1-Memoria-maestra-WCG-One.md`, `docs/documento-2-especificacion-funcional-v1-wcg-one.md`, `docs/documento-3-especificacion-tecnica-django-wcg-one.md`, `docs/documento-4-modelos-migraciones-admin-para-cursor.md`, `docs/06-guia-demo-operativa.md`
