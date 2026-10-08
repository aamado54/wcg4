# Inversiones PGC: captaciones vs incremento

## Conceptos (alineado con el código)

| Término | Significado en WCG |
|--------|---------------------|
| **Inversiones (AP+PG)** | Saldos dolarizados al cierre del mes: pagarés (AP) + acciones preferentes (PG), archivo `Inversiones_crecimiento`. |
| **Préstamos** | Total dolarizado de préstamos bancarios al cierre, archivo `Bancos_Fin_de_mes` (puede faltar en meses viejos). |
| **Captaciones** | Inversiones (AP+PG) + préstamos, todo en **USD completos** al cierre del mes. |
| **Δ captaciones (PGC)** | Incremento mensual de captaciones: regla en `investment_net_growth_usd()`. Es lo que puntúa el tablero, **no es un ingreso contable**. |

## Regla del incremento

1. Si **ambos** meses (actual y anterior) tienen snapshot bancario:  
   `Δ = captacionesₜ − captacionesₜ₋₁`
2. Si **solo uno** de los dos meses tiene bancos:  
   `Δ = (AP+PG)ₜ − (AP+PG)ₜ₋₁` (evita saltos falsos cuando faltan préstamos en un mes).

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

- `InvestmentGrowthRow` — import `investment_growth`  
- `BankLoanMonthSnapshot` — import `bank_loans`  
- Recálculo: `recalc_investment_ingresos_from_new_clients`
