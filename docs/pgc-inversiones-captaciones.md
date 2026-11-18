# Inversiones PGC: captaciones vs incremento

## Conceptos (alineado con el código)

| Término | Significado en WCG |
|--------|---------------------|
| **Inversiones (AP+PG)** | Saldos dolarizados al cierre del mes: pagarés (AP) + acciones preferentes (PG), archivo `Inversiones_crecimiento`. |
| **Préstamos** | Total dolarizado de préstamos bancarios al cierre, archivo `Bancos_Fin_de_mes` (puede faltar en meses viejos). |
| **Captaciones** | Inversiones (AP+PG) + préstamos, todo en **USD completos** al cierre del mes. |
| **Δ captaciones (PGC)** | Incremento mensual de captaciones: regla en `investment_net_growth_usd()`. Es lo que puntúa el tablero, **no es un ingreso contable**. |

## Regla del incremento

**2026 (corrección org):** enero–agosto el Δ PGC incluye préstamos bancarios en captaciones cuando hay snapshots. **Septiembre 2026:** Δ AP+PG más el **puente bancario julio→agosto** (préstamos de agosto no presentes en `Bancos_Fin_de_mes.xlsx`). **Octubre 2026 en adelante:** solo **Δ AP+PG**; los archivos `Capital_Bancos` sep/oct no alimentan el incremento.

**General (código `investment_net_growth_usd`):**

1. Mes en régimen “con bancos” y **ambos** meses con snapshot bancario:  
   `Δ = captacionesₜ − captacionesₜ₋₁`
2. Mes en régimen “con bancos” y **solo uno** con bancos:  
   `Δ = (AP+PG)ₜ − (AP+PG)ₜ₋₁` (evita saltos falsos cuando faltan préstamos en un mes).
3. Mes **septiembre 2026:** `Δ = (AP+PG)_9 − (AP+PG)_8 + (Banco_ago − Banco_jul)` (puente único).
4. Mes **octubre 2026 en adelante:** `Δ = (AP+PG)ₜ − (AP+PG)ₜ₋₁`.

## Qué guarda la base para INVESTMENT

`MonthlyMetricResult.measured_value` = **miles de USD** del incremento (`growth_usd ÷ 1000`), no el saldo total.

Por eso la matriz antigua parecía “ingresos en dólares” pero eran **miles** del incremento, y en modo **Q** la celda de captura manual quedaba vacía (el valor viene calculado en USD).

## Matriz anual admin (`/admin-hub/mensual/ingresos/`)

**Unidades en pantalla:** igual que Factoraje/Leasing/Seguros, todo el score PGC usa **miles de US$** (no millones). Los saldos brutos en base están en USD completos; la matriz los divide entre 1 000 para mostrarlos.

Tres columnas solo para Inversiones (todas en miles USD):

1. Saldo AP+PG  
2. Saldo préstamos  
3. Δ captaciones (incremento mensual PGC)

**Formato:** coma miles, punto decimal, hasta 3 decimales sin ceros finales (`format_wcg_amount`).

La UI marca advertencias si el valor guardado en PGC no coincide con el recálculo o si el Δ no cuadra con la diferencia de captaciones (meses con bancos asimétricos).

## Fuentes de datos

- `InvestmentGrowthRow` — import `import_inversiones_crecimiento` (excluye AP/PG intercompañía WC; ver `pgc-clientes-nuevos-reglas-importacion.md`)  
- `BankLoanMonthSnapshot` — import `bank_loans`  
- Recálculo: `recalc_investment_ingresos_from_new_clients`

### Precisión (cálculo vs presentación)

- **Guardado:** `amount_usd`, `amount_gtq`, `total_usd` y `total_gtq` usan **6 decimales**; el import calcula USD como `Quetzalizado/TC` (sin `quantize` en Python). La columna «Dolarizado» del Excel solo se usa si no hay TC.
- **Agregación:** `Sum(amount_usd)` y deltas en `investment_ingresos.py` sin redondeo intermedio. `MonthlyMetricResult.measured_value` sigue en **6 decimales** (miles USD).
- **Presentación:** el reporte *Ingresos vs meta* redondea solo al renderizar (`wcg_num` / `format_wcg_amount`). Con `INGRESOS_DEFAULT_DECIMALS=1` las demás UNE muestran un decimal; **Inversiones** usa mínimo **3 decimales** en filas Capital/Ejecutado para evitar el patrón `.X0` cuando el dato interno es más fino.
- **Producción (wcg.lol):** tras deploy hay que **migrar**, **reimportar** `Inversiones_crecimiento` y bancos, y **recalcular** PGC; un solo `recalc` sin reimport no recupera centavos ya truncados en filas históricas.

### Formatos de archivo (2026)

**Inversiones_crecimiento_*.csv** — encabezados actuales: `Ciclo`, `Empresa`, `NumeroInversion`, `Instrumento`, `Inicio`, `Vencimiento`, `Moneda`, `Monto`, `TC`, `Quetzalizado` (sin columna `Dolarizado`; el USD se calcula). Sigue aceptándose el layout antiguo con `Cierre` / `monto_inversion` / `TipoCambio`.

**Capital_Bancos_YYYY_MM.csv** — `Ciclo`, `Banco`, `Cuenta`, `Moneda`, `Capital` (una fila por cuenta; el import agrega por banco y usa `MonthlyExchangeRate` para totales GTQ/USD). Alternativa histórica: `Bancos_Fin_de_mes.xlsx`.
