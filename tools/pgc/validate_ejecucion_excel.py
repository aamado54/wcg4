#!/usr/bin/env python3
"""Cuadra PGC en DB vs archivo Excel de validación (hoja Objetivos)."""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from decimal import Decimal
from pathlib import Path

import django
import openpyxl

# Bootstrap Django when run as script
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from core.models import MetricDefinition, UNE
from pgc.models import MonthlyMetricResult, MonthlyTarget, PGCPlan, MonthlyExchangeRate

UEN_MAP = {
    "WC": "FACTORING",
    "WCL": "LEASING",
    "WCI": "INSURANCE",
    "WCINV": "INVESTMENT",
    "WCG": "TOTAL",
}

METRIC_MAP = {
    "clientes": MetricDefinition.CODE_CLIENTES_NUEVOS,
    "comisiones": MetricDefinition.CODE_INGRESOS,
}


def _read_objetivos(path: Path, year: int, month: int) -> list[dict]:
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb["Objetivos"]
    rows = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        dt, pres_cli, pres_cli_ac, pres_com, pres_com_ac, uen, exec_cli, exec_cli_ac, exec_com, exec_com_ac = row[:10]
        if not dt or not hasattr(dt, "year"):
            continue
        if dt.year != year or dt.month != month:
            continue
        rows.append(
            {
                "uen": str(uen).strip().upper(),
                "pres_cli": pres_cli,
                "exec_cli": exec_cli,
                "pres_com_gtq": pres_com,
                "exec_com_gtq": exec_com,
            }
        )
    wb.close()
    return rows


def _gtq_comisiones_to_usd_miles(gtq: Decimal, fx: Decimal) -> Decimal:
    """Excel comisiones en GTQ completos → miles USD (como PGC)."""
    if not gtq or not fx:
        return Decimal("0")
    return (gtq / Decimal("1000")) / fx


def _db_value(plan, une_code: str, metric_code: str, year: int, month: int):
    une = UNE.objects.filter(code=une_code).first()
    metric = MetricDefinition.objects.filter(code=metric_code).first()
    if not une or not metric:
        return None, None
    res = MonthlyMetricResult.objects.filter(
        plan=plan, une=une, metric=metric, year=year, month=month
    ).first()
    tgt = MonthlyTarget.objects.filter(
        plan=plan, une=une, metric=metric, year=year, month=month
    ).first()
    return (
        res.measured_value if res else None,
        tgt.target_value if tgt else None,
    )


def compare(path: Path, year: int, month: int) -> list[dict]:
    plan = PGCPlan.objects.filter(year=year).first()
    if not plan:
        raise SystemExit(f"No hay PGCPlan para {year}")

    fx_row = MonthlyExchangeRate.objects.filter(year=year, month=month).first()
    fx = fx_row.usd_to_gtq if fx_row else None

    findings = []
    for rec in _read_objetivos(path, year, month):
        uen = rec["uen"]
        if uen == "WCG":
            continue
        une_code = UEN_MAP.get(uen)
        if not une_code:
            findings.append({"uen": uen, "issue": "UEN no mapeada"})
            continue

        db_cli, tgt_cli = _db_value(
            plan, une_code, METRIC_MAP["clientes"], year, month
        )
        excel_cli = rec["exec_cli"]
        if excel_cli is not None and db_cli is not None:
            if Decimal(str(excel_cli)) != Decimal(str(db_cli)):
                findings.append(
                    {
                        "metric": "CLIENTES_NUEVOS",
                        "uen": uen,
                        "excel": excel_cli,
                        "db": db_cli,
                        "target": tgt_cli,
                        "excel_target": rec["pres_cli"],
                    }
                )

        if rec["exec_com_gtq"] is not None and une_code != "INVESTMENT":
            db_ing, tgt_ing = _db_value(
                plan, une_code, METRIC_MAP["comisiones"], year, month
            )
            excel_ing_usd = None
            if fx:
                excel_ing_usd = _gtq_comisiones_to_usd_miles(
                    Decimal(str(rec["exec_com_gtq"])), fx
                )
            if db_ing is None:
                findings.append(
                    {
                        "metric": "INGRESOS",
                        "uen": uen,
                        "excel_gtq": rec["exec_com_gtq"],
                        "excel_usd_miles": excel_ing_usd,
                        "db": None,
                        "target": tgt_ing,
                        "note": "Sin measured_value en DB",
                    }
                )
            elif excel_ing_usd is not None:
                diff = abs(Decimal(str(db_ing)) - excel_ing_usd)
                if diff > Decimal("0.05"):
                    findings.append(
                        {
                            "metric": "INGRESOS",
                            "uen": uen,
                            "excel_gtq": rec["exec_com_gtq"],
                            "excel_usd_miles": float(excel_ing_usd),
                            "db": float(db_ing),
                            "diff_usd": float(diff),
                            "target": float(tgt_ing) if tgt_ing else None,
                            "fx": float(fx),
                        }
                    )

    return findings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True)
    parser.add_argument("--year", type=int, default=2026)
    parser.add_argument("--month", type=int, default=8)
    args = parser.parse_args()

    findings = compare(Path(args.path), args.year, args.month)
    if not findings:
        print(f"OK — sin diferencias materializadas para {args.year}-{args.month:02d}")
        return 0

    print(f"Diferencias {args.year}-{args.month:02d} ({len(findings)}):")
    for f in findings:
        print(" -", f)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
