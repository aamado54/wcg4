# PGO — hallazgos actuales (documentación, sin implementar tabla de resultados)

Fecha de revisión: 2026-07-23.  
Alcance: `~/wc/wcg4/dashboard`. Solo documenta; **no** implementa scoreboard Clasifica ni tabla de puntos.

Referencia de negocio aportada (pesos Factoring 50% / Leasing 30% / Investment 15% / Insurance 5%; umbral ≥ 80) se contrasta abajo con lo que el código hace hoy.

---

## Archivos revisados

| Área | Rutas |
|------|--------|
| Docs previos | `docs/pgc_vs_pgo_explicacion.md`, `docs/Documento-1-Memoria-maestra-WCG-One.md`, `docs/documento-2-especificacion-funcional-v1-wcg-one.md`, `docs/06-guia-demo-operativa.md` |
| PGO productivo | `pgo/models.py`, `pgo/periodo.py`, `pgo/services.py`, `pgo/views.py`, `templates/pgo/pgodashboard.html` |
| PGO WCG One | `apps/pgo/models.py`, `apps/pgo/views.py`, `apps/pgo/imports/tickets.py`, `templates/wcgone/pgo/resultados.html` |
| Reportes | `reports/services/pgo_results.py` |
| Risk / EEFF (archivos) | `apps/risk/imports/estados_financieros.py`, `risk/services.py` (`import_estados_financieros`) |
| Guías índice | `all_python_scripts.index-07-23-15-11.md`, `all_html_templates.index-07-23-15-11.md` |

---

## Cómo se calcula el PGO hoy (lo que el sistema realmente hace)

### A) Menú productivo `/pgo/`

1. Import de tickets → `pgo.services.import_tickets` → modelo `pgo.Ticket` (upsert por `codigo`).
2. Tras import (o al abrir dashboard) → `pgo.periodo.recalculate_pgo_periodos()`.
3. Agrega por período (`YYYY-MM` de `fecha_apertura`) y unidad:
   - tickets cerrados / abiertos
   - tiempo promedio de cierre (horas)
   - `% SLA` = cerrados con duración ≤ `sla_horas` / cerrados con fechas
4. UI (`pgodashboard.html`): Período, Unidad, Cerrados, Abiertos, T. promedio, SLA %.  
   **Sin puntaje total, sin pesos por UNE, sin Clasifica.**

Unidad por defecto en tickets sin UN: **TI / Tecnología** (`code="TI"` en import).

### B) Stack WCG One `/wcgone/pgo/`

- Schema: `PgoMetricRule` (puntos, peso, fórmula texto), `PgoPeriodScore` (`puntaje_total`, `clasifica`), `PgoMonthlyAgg`, `PgoTicket`.
- UI de resultados puede mostrar Puntaje + Clasifica **si hay filas**.
- **No hay** comando/servicio `recalc_pgo` que lea las reglas de negocio (tabla de puntos de la referencia) y escriba `PgoPeriodScore`.

---

## Qué datos ya usa vs qué pide la referencia de puntos

| Variable de negocio (referencia) | ¿Datos en sistema? | ¿Procesamiento hacia puntos? |
|----------------------------------|--------------------|------------------------------|
| Análisis 100% casos en 10 días hábiles (solo Planner Power App / WCG Créditos) | Parcial: tickets con fechas/SLA; **no** hay filtro “solo Planner” ni calendario de días hábiles | No → puntos 30 Factoring/Leasing |
| Plan valuación 100% cartera F/L + dictámenes | No modelo/evidencia de plan de valuación ni dictámenes | No → 40 F/L |
| Carga mensual datos analítica (EEFF cartera, ingresos/pagos) antes del día 7 | Parcial: imports PGC/Risk/EEFF por archivo+fecha; **sin** control “antes del 7” ni checklist PGO | No → 10 F/L, 50 Inv/Ins |
| Info a acreedores 3 meses antes del vencimiento de líneas | No | No → 10 F/L |
| EEFF WCG completos y firmados 5 días hábiles post-cierre | Parcial: `EstadoFinanciero` / imports Risk; **sin** firma, plazo hábil ni score | No → 10 F/L, 50 Inv/Ins |
| Tickets TI / operación | Sí: pipeline tickets + SLA % | Solo agregados; no ponderación 50/30/15/5 |

**Nota total del mes** = suma ponderada de pesos por UNE (≥ 80 clasifica): **no implementada**.

---

## Archivos/fechas vs tickets (especialmente Tecnología)

| Área | Mecanismo actual | Observación |
|------|------------------|-------------|
| **Tecnología / TI** | **Tickets** (import PGO; UN default TI) | Es el único tramo PGO con pipeline operativo completo (volumen + SLA). No hay score de “puntos PGO” encima. |
| **Créditos / casos 10 días hábiles** | Debería ser tickets/Planner; hoy genérico `Ticket` | Falta origen “solo WCG Créditos / Planner” y regla de 10 días hábiles. |
| **Analítica mensual / EEFF / ingresos** | **Archivos + período (año/mes o fecha de archivo)** vía Importación General / Admin PGC / Risk EEFF | No alimentan `PgoPeriodScore`; viven en PGC/Risk. |
| **Valuación / acreedores / firmas EEFF** | No hay flujo PGO dedicado | Condiciones no dadas en código. |

---

## ¿Están dadas las condiciones para una tabla de resultados (Clasifica ≥ 80)?

**No.** Falta, como mínimo:

1. Catálogo operativo de reglas alineado a la tabla de referencia (puntos + pesos por UNE), no solo schema `PgoMetricRule`.
2. Fuentes y evidencias por variable (valuación, acreedores, checklist carga ≤ día 7, EEFF firmados, casos Planner).
3. Motor de recálculo: puntaje por UNE → ponderación 50/30/15/5 → `puntaje_total` → `clasifica = total >= 80`.
4. Decisión de producto: ¿la tabla vive en `/pgo/` (hoy solo SLA) o en `/wcgone/pgo/resultados/` (schema sin motor)?
5. Calendario de días hábiles y umbrales de fecha (día 7, +5 hábiles, −3 meses).

Hoy sí hay condiciones para una **tabla operacional de tickets/SLA** (ya existe). No para la **tabla de calificación por puntos** de la referencia.

---

## Relación con PGC (no confundir)

PGC ya tiene meta vs real → puntos → `is_month_qualified` (≥ 80) en `recalc_pgc`.  
PGO de la referencia es otro scorecard (eficiencia financiera + agilidad operativa por UNE). El paralelismo visual/analítico aún no existe en el menú productivo PGO.

Ver también: `docs/pgc_vs_pgo_explicacion.md`.
