"""Pasivas de inversión (AP/PG/bancos) para reportes gerenciales."""

from __future__ import annotations

from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal
from typing import Any

from imports.models import BankLoanMonthSnapshot, InvestmentGrowthRow
from pgc.investment_ingresos import (
    investment_gross_usd,
    investment_net_growth_usd,
    investment_periods_with_data,
)


def _period_key(year: int, month: int) -> str:
    return f"{year}-{month:02d}"


def _parse_period_key(key: str) -> tuple[int, int]:
    year, month = key.split("-")
    return int(year), int(month)


def build_pasivas_growth_board(
    *,
    end_period: str | None = None,
    months: int = 12,
) -> dict[str, Any]:
    periods = investment_periods_with_data()
    if not periods:
        return {"status": "empty", "rows": [], "latest": None}

    period_keys = [_period_key(y, m) for y, m in periods]
    if end_period and end_period in period_keys:
        end_idx = period_keys.index(end_period)
    else:
        end_idx = len(period_keys) - 1
    start_idx = max(0, end_idx - months + 1)
    window = period_keys[start_idx : end_idx + 1]

    rows: list[dict[str, Any]] = []
    for key in window:
        year, month = _parse_period_key(key)
        gross = investment_gross_usd(year, month)
        growth = investment_net_growth_usd(year, month)
        bank = BankLoanMonthSnapshot.objects.filter(year=year, month=month).first()
        rows.append(
            {
                "period": key,
                "ap_usd": gross.get("ap_usd"),
                "pg_usd": gross.get("pg_usd"),
                "banks_usd": gross.get("banks_usd"),
                "total_usd": gross.get("total_usd"),
                "growth_usd": growth,
                "fx": bank.exchange_rate if bank else None,
                "operations": InvestmentGrowthRow.objects.filter(
                    year=year, month=month
                ).count(),
            }
        )

    latest = rows[-1] if rows else None
    end_year, end_month = _parse_period_key(window[-1])
    horizon = date(end_year, end_month, 28) + timedelta(days=120)

    maturities = (
        InvestmentGrowthRow.objects.filter(
            year=end_year,
            month=end_month,
            maturity_date__isnull=False,
            maturity_date__lte=horizon,
        )
        .order_by("maturity_date", "instrument", "operation_code")[:20]
    )
    maturity_rows = [
        {
            "period": window[-1],
            "instrument": row.instrument,
            "operation_code": row.operation_code,
            "company": row.company,
            "maturity_date": row.maturity_date.isoformat() if row.maturity_date else "",
            "amount_usd": row.amount_usd,
            "currency_code": row.currency_code,
        }
        for row in maturities
    ]

    currency_split = defaultdict(lambda: {"ap": Decimal("0"), "pg": Decimal("0")})
    if latest:
        y, m = _parse_period_key(latest["period"])
        for row in InvestmentGrowthRow.objects.filter(year=y, month=m):
            bucket = currency_split[row.currency_code or "—"]
            if row.instrument == "AP":
                bucket["ap"] += row.amount_usd
            else:
                bucket["pg"] += row.amount_usd

    quarterly: dict[str, dict[str, Decimal]] = defaultdict(
        lambda: {"growth_usd": Decimal("0"), "months": 0}
    )
    for row in rows:
        year, month = _parse_period_key(row["period"])
        q = f"{year}-Q{(month - 1) // 3 + 1}"
        if row["growth_usd"] is not None:
            quarterly[q]["growth_usd"] += row["growth_usd"]
            quarterly[q]["months"] += 1

    return {
        "status": "ok",
        "rows": rows,
        "latest": latest,
        "maturities": maturity_rows,
        "currency_split": [
            {
                "currency": code,
                "ap_usd": vals["ap"],
                "pg_usd": vals["pg"],
                "total_usd": vals["ap"] + vals["pg"],
            }
            for code, vals in sorted(currency_split.items())
        ],
        "quarterly_growth": [
            {"quarter": q, "growth_usd": vals["growth_usd"], "months": vals["months"]}
            for q, vals in sorted(quarterly.items())
        ],
        "end_period": window[-1],
        "start_period": window[0],
    }
