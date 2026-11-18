"""Export TSV compatible con plantilla verifica.tsv (filas 62–121, año 2026)."""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from core.money_precision import MONEY_STORE_PLACES, quantize_store
from pathlib import Path

from core.models import MetricDefinition, UNE
from pgc.models import (
    MonthlyExchangeRate,
    MonthlyMetricResult,
    MonthlyMetricScore,
    MonthlyModeScorecard,
    MonthlyTarget,
    PGCPlan,
)

# Fila 1 verifica.tsv (24 columnas); export solo A–J = 10 columnas operativas + puntos.
VERIFICA_HEADER_ROW = [
    "Mes",
    "UEN",
    "Clientes Nuevos (Presupuesto)",
    "Comisiones (Presupuesto Mensual)",
    "Clientes Nuevos (Ejecución Mensual)",
    "Comisiones (Ejecución Mensual)",
    "Pts Ingresos",
    "Pts Clientes Nuevos",
    "Pts Venta Cruzada",
    "Total Puntos",
]

# Índices 0-based en TSV plantilla (fila cabecera)
COL_A_MES = 0
COL_B_PRES_CLI = 1
COL_D_PRES_COM = 3
COL_F_UEN = 5
COL_G_EXEC_CLI = 6
COL_I_EXEC_COM = 8
COL_S_PTS_ING = 18
COL_T_PTS_CLI = 19
COL_U_PTS_VC = 20
COL_W_TOTAL = 22

WC_TO_UNE = {
    "WC": UNE.CODE_FACTORING,
    "WCL": UNE.CODE_LEASING,
    "WCI": UNE.CODE_INSURANCE,
    "WCINV": UNE.CODE_INVESTMENT,
    "INVESTMENTS": UNE.CODE_INVESTMENT,
    "WCG": "TOTAL_EX_INV",
}

EX_INV_UNES = (UNE.CODE_FACTORING, UNE.CODE_LEASING, UNE.CODE_INSURANCE)

MONTH_ALIASES = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}

ROW_START_2026 = 62
ROW_END_2026 = 121
EXPECTED_ROW_COUNT = ROW_END_2026 - ROW_START_2026 + 1


@dataclass
class VerificaRowSpec:
    year: int
    month: int
    wc_code: str
    label_a: str = ""
    has_points: bool = True


def normalize_wc_code(raw: str) -> str:
    wc = (raw or "").strip().upper()
    if wc == "INVESTMENTS":
        return "WCINV"
    return wc


def _parse_month_cell(cell: str) -> tuple[int, int] | None:
    if not cell:
        return None
    cell = str(cell).strip()
    m = re.match(r"([A-Za-z]{3})-(\d{2})", cell)
    if m:
        mon = MONTH_ALIASES.get(m.group(1).lower())
        if not mon:
            return None
        yr = 2000 + int(m.group(2))
        return yr, mon
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            dt = datetime.strptime(cell[:10], fmt)
            return dt.year, dt.month
        except ValueError:
            continue
    return None


def _row_has_points_columns(row: list[str]) -> bool:
    """WCG 2026 no trae columnas S–W en verifica; otras UNE sí."""
    if len(row) <= COL_S_PTS_ING:
        return False
    tail = row[COL_S_PTS_ING : COL_W_TOTAL + 1]
    return any((c or "").strip() for c in tail)


def parse_verifica_template_rows(
    path: Path,
    *,
    year: int,
    row_start: int = ROW_START_2026,
    row_end: int = ROW_END_2026,
) -> list[VerificaRowSpec]:
    specs: list[VerificaRowSpec] = []
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f, delimiter="\t")
        for i, row in enumerate(reader, start=1):
            if i < row_start or i > row_end:
                continue
            if len(row) <= COL_F_UEN:
                continue
            label_a = (row[COL_A_MES] or "").strip()
            wc = normalize_wc_code(row[COL_F_UEN])
            if not wc:
                continue
            ym = _parse_month_cell(label_a)
            if not ym or ym[0] != year:
                continue
            yr, mon = ym
            has_pts = wc != "WCG" and _row_has_points_columns(row)
            specs.append(
                VerificaRowSpec(
                    year=yr,
                    month=mon,
                    wc_code=wc,
                    label_a=label_a,
                    has_points=has_pts,
                )
            )
    return specs


def default_row_specs(year: int) -> list[VerificaRowSpec]:
    order = ("WC", "WCL", "WCI", "WCINV", "WCG")
    specs: list[VerificaRowSpec] = []
    for month in range(1, 13):
        abbr = list(MONTH_ALIASES.keys())[month - 1].title()
        label = f"{abbr}-{year % 100:02d}"
        for wc in order:
            specs.append(
                VerificaRowSpec(
                    year=year,
                    month=month,
                    wc_code=wc,
                    label_a=label,
                    has_points=wc != "WCG",
                )
            )
    return specs


def _fmt_num(val: Decimal | None) -> str:
    if val is None:
        return ""
    q = quantize_store(val, places=MONEY_STORE_PLACES) or Decimal("0")
    if q == q.to_integral_value():
        return str(int(q))
    return format(q, "f").rstrip("0").rstrip(".")


def _usd_miles_to_gtq_full(usd_miles: Decimal | None, fx: Decimal | None) -> Decimal | None:
    if usd_miles is None or fx is None or fx == 0:
        return None
    return quantize_store(usd_miles * Decimal("1000") * fx, places=MONEY_STORE_PLACES)


def _investment_exec_display(usd_miles: Decimal | None) -> str:
    """Verifica muestra crecimiento inversiones en unidades enteras (~miles × 1000)."""
    if usd_miles is None:
        return ""
    return _fmt_num((usd_miles * Decimal("1000")).quantize(Decimal("1")))


def _get_fx(year: int, month: int) -> Decimal | None:
    row = MonthlyExchangeRate.objects.filter(year=year, month=month).first()
    return row.usd_to_gtq if row else None


def _target_and_result(plan, une_code: str, metric_code: str, year: int, month: int):
    une = UNE.objects.filter(code=une_code).first()
    metric = MetricDefinition.objects.filter(code=metric_code).first()
    if not une or not metric:
        return None, None, None
    res = MonthlyMetricResult.objects.filter(
        plan=plan, une=une, metric=metric, year=year, month=month
    ).first()
    tgt = MonthlyTarget.objects.filter(
        plan=plan, une=une, metric=metric, year=year, month=month
    ).first()
    pres_gtq = getattr(tgt, "presupuesto_gtq", None) if tgt else None
    return res, tgt, pres_gtq


def _metric_points(plan, une_code: str, metric_code: str, year: int, month: int, mode: str):
    une = UNE.objects.filter(code=une_code).first()
    metric = MetricDefinition.objects.filter(code=metric_code).first()
    if not une or not metric:
        return None
    sc = MonthlyMetricScore.objects.filter(
        plan=plan,
        une=une,
        metric=metric,
        year=year,
        month=month,
        mode=mode,
    ).first()
    return sc.points_awarded if sc else None


def _scorecard_total(plan, une_code: str, year: int, month: int, mode: str):
    une = UNE.objects.filter(code=une_code).first()
    if not une:
        return None
    card = MonthlyModeScorecard.objects.filter(
        plan=plan, une=une, year=year, month=month, mode=mode
    ).first()
    return card.total_points if card else None


def _sum_decimal(values: list[Decimal | None]) -> Decimal | None:
    total = Decimal("0")
    found = False
    for v in values:
        if v is not None:
            total += v
            found = True
    return total if found else None


def _wcg_field(plan, year: int, month: int, mode: str, field: str) -> str:
    fx = _get_fx(year, month)
    pres_clis: list[Decimal | None] = []
    pres_coms: list[Decimal | None] = []
    exec_clis: list[Decimal | None] = []
    exec_coms: list[Decimal | None] = []

    for une_code in EX_INV_UNES:
        cli_res, cli_tgt, _ = _target_and_result(
            plan, une_code, MetricDefinition.CODE_CLIENTES_NUEVOS, year, month
        )
        ing_res, _, pres_gtq = _target_and_result(
            plan, une_code, MetricDefinition.CODE_INGRESOS, year, month
        )
        if cli_tgt and cli_tgt.target_value is not None:
            pres_clis.append(Decimal(str(cli_tgt.target_value)))
        if pres_gtq is not None:
            pres_coms.append(Decimal(str(pres_gtq)))
        if cli_res and cli_res.measured_value is not None:
            exec_clis.append(Decimal(str(cli_res.measured_value)))
        if ing_res and ing_res.measured_value is not None:
            gtq = _usd_miles_to_gtq_full(ing_res.measured_value, fx)
            exec_coms.append(gtq)

    mapping = {
        "pres_cli": _sum_decimal(pres_clis),
        "pres_com": _sum_decimal(pres_coms),
        "exec_cli": _sum_decimal(exec_clis),
        "exec_com": _sum_decimal(exec_coms),
    }
    val = mapping.get(field)
    return _fmt_num(val) if val is not None else ""


def build_output_row(
    spec: VerificaRowSpec,
    plan: PGCPlan,
    *,
    mode: str = "modo2",
) -> list[str]:
    """
    Salida A–J (mapa fuente → salida):
      A Mes, B←F UEN, C←B pres_cli, D←D pres_com GTQ, E←G exec_cli,
      F←I exec_com, G←S pts_ing, H←T pts_cli, I←U pts_vc, J←W total.
    """
    fx = _get_fx(spec.year, spec.month)
    une_code = WC_TO_UNE.get(spec.wc_code)

    if une_code == "TOTAL_EX_INV":
        return [
            spec.label_a,
            "WCG",
            _wcg_field(plan, spec.year, spec.month, mode, "pres_cli"),
            _wcg_field(plan, spec.year, spec.month, mode, "pres_com"),
            _wcg_field(plan, spec.year, spec.month, mode, "exec_cli"),
            _wcg_field(plan, spec.year, spec.month, mode, "exec_com"),
            "",
            "",
            "",
            "",
        ]

    if not une_code:
        return [spec.label_a, spec.wc_code, "", "", "", "", "", "", "", ""]

    cli_res, cli_tgt, _ = _target_and_result(
        plan, une_code, MetricDefinition.CODE_CLIENTES_NUEVOS, spec.year, spec.month
    )
    ing_res, ing_tgt, pres_gtq = _target_and_result(
        plan, une_code, MetricDefinition.CODE_INGRESOS, spec.year, spec.month
    )

    pres_cli = ""
    if cli_tgt and cli_tgt.target_value is not None:
        pres_cli = _fmt_num(Decimal(str(cli_tgt.target_value)))

    pres_com = ""
    if pres_gtq is not None:
        pres_com = _fmt_num(Decimal(str(pres_gtq)))

    exec_cli = ""
    if cli_res and cli_res.measured_value is not None:
        exec_cli = _fmt_num(Decimal(str(cli_res.measured_value)))

    exec_com = ""
    if une_code == UNE.CODE_INVESTMENT:
        if ing_res and ing_res.measured_value is not None:
            exec_com = _investment_exec_display(ing_res.measured_value)
    elif ing_res and ing_res.measured_value is not None:
        gtq = _usd_miles_to_gtq_full(ing_res.measured_value, fx)
        exec_com = _fmt_num(gtq) if gtq is not None else ""

    pts_ing = pts_cli = pts_vc = total = ""
    if spec.has_points:
        pts_ing = _fmt_num(_metric_points(
            plan, une_code, MetricDefinition.CODE_INGRESOS, spec.year, spec.month, mode
        ))
        pts_cli = _fmt_num(_metric_points(
            plan, une_code, MetricDefinition.CODE_CLIENTES_NUEVOS, spec.year, spec.month, mode
        ))
        pts_vc = _fmt_num(_metric_points(
            plan, une_code, MetricDefinition.CODE_VENTA_CRUZADA, spec.year, spec.month, mode
        ))
        total = _fmt_num(_scorecard_total(plan, une_code, spec.year, spec.month, mode))

    display_uen = "WCINV" if spec.wc_code in ("WCINV", "INVESTMENTS") else spec.wc_code

    return [
        spec.label_a or f"{spec.year}-{spec.month:02d}",
        display_uen,
        pres_cli,
        pres_com,
        exec_cli,
        exec_com,
        pts_ing,
        pts_cli,
        pts_vc,
        total,
    ]


def export_verifica_tsv(
    output: Path,
    *,
    year: int,
    template: Path | None = None,
    mode: str = "modo2",
    include_header: bool = True,
) -> int:
    plan = PGCPlan.objects.filter(year=year).first()
    if not plan:
        raise ValueError(f"No PGCPlan para {year}")

    if template and template.is_file():
        specs = parse_verifica_template_rows(template, year=year)
    else:
        specs = default_row_specs(year)

    if not specs:
        raise ValueError("Sin filas de verifica (plantilla vacía o año sin coincidencias)")

    rows = [build_output_row(spec, plan, mode=mode) for spec in specs]
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t")
        if include_header:
            writer.writerow(VERIFICA_HEADER_ROW)
        writer.writerows(rows)
    return len(rows)