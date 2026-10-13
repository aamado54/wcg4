"""Importa ejecución PGC (clientes + comisiones) desde hoja Objetivos de Excel."""

from __future__ import annotations

import argparse
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

import openpyxl
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from core.models import MetricDefinition, UNE
from pgc.excel_import_guard import assert_pgc_objetivos_import_allowed
from pgc.income_conversion import apply_result_achievement
from pgc.models import (
    ManualRequirementsCompliance,
    MonthlyExchangeRate,
    MonthlyMetricResult,
    MonthlyTarget,
    PGCPlan,
)

UEN_TO_UNE = {
    "WC": "FACTORING",
    "WCL": "LEASING",
    "WCI": "INSURANCE",
    "WCINV": "INVESTMENT",
}

# Índices 0-based en fila hoja Objetivos (ver encabezados Sep26).
COL_PRES_CLI = 1
COL_PRES_COM = 3
COL_EXEC_CLI = 6
COL_EXEC_COM = 8
COL_PRES_VC = 12
COL_EXEC_VC = 13
COL_PTS_ING = 14
COL_PTS_CLI = 15
COL_PTS_VC = 16
COL_PTS_REQ = 17
COL_PTS_EXEC_REQ = 21


def _gtq_comisiones_to_usd_miles(gtq: Decimal, fx: Decimal) -> Decimal:
    """Comisiones en GTQ completos → miles USD (convención PGC tablero)."""
    if not gtq or not fx:
        return Decimal("0")
    return (gtq / Decimal("1000")) / fx


def _cell_decimal(val) -> Decimal | None:
    if val is None:
        return None
    try:
        return Decimal(str(val))
    except (InvalidOperation, ValueError):
        return None


def _points_int(val) -> int | None:
    d = _cell_decimal(val)
    if d is None:
        return None
    return int(d.quantize(Decimal("1")))


def _read_objetivos_rows(path: Path, year: int, month: int) -> list[dict]:
    wb = openpyxl.load_workbook(path, data_only=True)
    if "Objetivos" not in wb.sheetnames:
        wb.close()
        raise CommandError(f"{path.name}: falta hoja Objetivos")

    ws = wb["Objetivos"]
    rows: list[dict] = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row or len(row) < 10:
            continue
        dt = row[0]
        if not isinstance(dt, datetime):
            continue
        if dt.year != year or dt.month != month:
            continue
        uen_code = str(row[5] or "").strip().upper()
        if uen_code not in UEN_TO_UNE:
            continue
        rows.append(
            {
                "uen": uen_code,
                "pres_cli": row[COL_PRES_CLI] if len(row) > COL_PRES_CLI else None,
                "pres_com_gtq": row[COL_PRES_COM] if len(row) > COL_PRES_COM else None,
                "exec_cli": row[COL_EXEC_CLI] if len(row) > COL_EXEC_CLI else None,
                "exec_com_gtq": row[COL_EXEC_COM] if len(row) > COL_EXEC_COM else None,
                "pres_vc": row[COL_PRES_VC] if len(row) > COL_PRES_VC else None,
                "exec_vc": row[COL_EXEC_VC] if len(row) > COL_EXEC_VC else None,
                "pts_ing": row[COL_PTS_ING] if len(row) > COL_PTS_ING else None,
                "pts_cli": row[COL_PTS_CLI] if len(row) > COL_PTS_CLI else None,
                "pts_vc": row[COL_PTS_VC] if len(row) > COL_PTS_VC else None,
                "pts_req": row[COL_PTS_REQ] if len(row) > COL_PTS_REQ else None,
                "pts_exec_req": row[COL_PTS_EXEC_REQ] if len(row) > COL_PTS_EXEC_REQ else None,
            }
        )
    wb.close()
    return rows


def _sync_monthly_target_points(
    tgt: MonthlyTarget | None, points_raw, *, skip_zero: bool = False
) -> None:
    if not tgt:
        return
    if points_raw is not None and str(points_raw).strip().upper() in (
        "NO APLICA",
        "NOAPLICA",
        "N/A",
    ):
        return
    pts = _points_int(points_raw)
    if pts is None:
        return
    if skip_zero and pts <= 0:
        return
    if tgt.points_if_achieved != pts:
        tgt.points_if_achieved = pts
        tgt.save(update_fields=["points_if_achieved", "updated_at"])


class Command(BaseCommand):
    help = (
        "Carga ejecución Tablero (proporción) desde la hoja Objetivos: "
        "clientes y puntos P_ing/P_cli. Comisiones (ingresos) preferir import_ingresos. "
        "VC y reqs no se cargan desde Excel salvo --sync-vc / --sync-reqs."
    )

    def add_arguments(self, parser):
        parser.add_argument("--path", type=str, required=True, help="Ruta al .xlsx")
        parser.add_argument("--year", type=int, required=True)
        parser.add_argument("--month", type=int, required=True)
        parser.add_argument(
            "--skip-venta-cruzada",
            action=argparse.BooleanOptionalAction,
            default=True,
            help="No escribir VC desde Excel (default). Equivalente a omitir --sync-vc.",
        )
        parser.add_argument(
            "--skip-requisitos",
            action=argparse.BooleanOptionalAction,
            default=True,
            help="No escribir cumplimiento reqs desde Excel (default). Use --sync-reqs.",
        )
        parser.add_argument(
            "--sync-vc",
            action="store_true",
            help="Importar venta cruzada (ejecución/meta puntos VC) desde Objetivos.",
        )
        parser.add_argument(
            "--sync-reqs",
            action="store_true",
            help="Importar ManualRequirementsCompliance desde Objetivos.",
        )
        parser.add_argument(
            "--sync-targets",
            action="store_true",
            help=(
                "OBSOLETO — no usar. Las metas oficiales vienen de PGC-metas-YYYY.tsv "
                "(comando import_pgc_metas). El Excel Objetivos es solo para ejecución."
            ),
        )
        parser.add_argument(
            "--force-legacy-excel",
            action="store_true",
            help=(
                "Permite este import sin ALLOW_PGC_EXCEL_IMPORT=1 (solo dev/migración; "
                "muestra advertencia)."
            ),
        )

    @transaction.atomic
    def handle(self, *args, **options):
        assert_pgc_objetivos_import_allowed(
            self, force_legacy_excel=options.get("force_legacy_excel", False)
        )
        path = Path(options["path"]).expanduser()
        year = options["year"]
        month = options["month"]

        if not path.is_file():
            raise CommandError(f"Archivo no encontrado: {path}")

        try:
            plan = PGCPlan.objects.get(year=year)
        except PGCPlan.DoesNotExist:
            raise CommandError(f"No existe PGCPlan para {year}")

        fx_row = MonthlyExchangeRate.objects.filter(year=year, month=month).first()
        if not fx_row or not fx_row.usd_to_gtq:
            raise CommandError(
                f"Falta MonthlyExchangeRate para {year}-{month:02d}"
            )
        fx = fx_row.usd_to_gtq

        metric_cli = MetricDefinition.objects.get(code=MetricDefinition.CODE_CLIENTES_NUEVOS)
        metric_ing = MetricDefinition.objects.get(code=MetricDefinition.CODE_INGRESOS)
        metric_vc = MetricDefinition.objects.get(code=MetricDefinition.CODE_VENTA_CRUZADA)
        metric_req = MetricDefinition.objects.get(code=MetricDefinition.CODE_RESPUESTA_REQS)

        records = _read_objetivos_rows(path, year, month)
        if not records:
            raise CommandError(f"Sin filas Objetivos para {year}-{month:02d}")

        if options.get("sync_targets"):
            raise CommandError(
                "La opción --sync-targets está deshabilitada. "
                "Use import_pgc_metas con el TSV oficial (PGC-metas-2026.tsv)."
            )

        sync_vc = options["sync_vc"] or not options["skip_venta_cruzada"]
        sync_reqs = options["sync_reqs"] or not options["skip_requisitos"]

        for rec in records:
            une = UNE.objects.get(code=UEN_TO_UNE[rec["uen"]])

            tgt_cli = MonthlyTarget.objects.filter(
                plan=plan, une=une, metric=metric_cli, year=year, month=month
            ).first()
            tgt_ing = MonthlyTarget.objects.filter(
                plan=plan, une=une, metric=metric_ing, year=year, month=month
            ).first()
            tgt_vc = MonthlyTarget.objects.filter(
                plan=plan, une=une, metric=metric_vc, year=year, month=month
            ).first()
            tgt_req = MonthlyTarget.objects.filter(
                plan=plan, une=une, metric=metric_req, year=year, month=month
            ).first()

            _sync_monthly_target_points(tgt_ing, rec["pts_ing"])
            _sync_monthly_target_points(tgt_cli, rec["pts_cli"])
            if sync_vc:
                _sync_monthly_target_points(tgt_vc, rec["pts_vc"])
            if sync_reqs:
                _sync_monthly_target_points(tgt_req, rec["pts_req"], skip_zero=True)

            pres_cli = _cell_decimal(rec["pres_cli"])
            if pres_cli is not None and tgt_cli:
                if tgt_cli.target_value != pres_cli:
                    tgt_cli.target_value = pres_cli
                    tgt_cli.save(update_fields=["target_value", "updated_at"])

            if sync_vc:
                pres_vc = _cell_decimal(rec["pres_vc"])
                if pres_vc is not None and tgt_vc:
                    if pres_vc > 0 and tgt_vc.target_value != pres_vc:
                        tgt_vc.target_value = pres_vc
                        tgt_vc.save(update_fields=["target_value", "updated_at"])

            if rec["exec_cli"] is not None:
                if not tgt_cli:
                    raise CommandError(
                        f"Sin meta CLIENTES_NUEVOS {une.code} {year}-{month:02d}"
                    )
                mmr_cli, _ = MonthlyMetricResult.objects.get_or_create(
                    plan=plan,
                    une=une,
                    metric=metric_cli,
                    year=year,
                    month=month,
                    defaults={"target_value": tgt_cli.target_value},
                )
                mmr_cli.target_value = tgt_cli.target_value
                mmr_cli.measured_value = Decimal(str(rec["exec_cli"]))
                mmr_cli.calculation_note = (
                    f"Importado desde {path.name} Objetivos "
                    f"(clientes ejecución mensual)."
                )
                apply_result_achievement(mmr_cli, tgt_cli)
                mmr_cli.save()

            if rec["exec_com_gtq"] is not None:
                if not tgt_ing:
                    raise CommandError(
                        f"Sin meta INGRESOS {une.code} {year}-{month:02d}"
                    )
                gtq = Decimal(str(rec["exec_com_gtq"]))
                usd_miles = _gtq_comisiones_to_usd_miles(gtq, fx)
                mmr_ing, _ = MonthlyMetricResult.objects.get_or_create(
                    plan=plan,
                    une=une,
                    metric=metric_ing,
                    year=year,
                    month=month,
                    defaults={"target_value": tgt_ing.target_value},
                )
                mmr_ing.target_value = tgt_ing.target_value
                mmr_ing.source_currency = MonthlyMetricResult.CURRENCY_GTQ
                mmr_ing.source_value = gtq
                mmr_ing.exchange_rate_used = fx
                mmr_ing.conversion_status = MonthlyMetricResult.CONVERSION_CONVERTED
                mmr_ing.measured_value = usd_miles
                mmr_ing.calculation_note = (
                    f"Importado desde {path.name} Objetivos "
                    f"(comisiones ejecución mensual GTQ={gtq}, FX={fx}, "
                    f"USD miles={usd_miles})."
                )
                apply_result_achievement(mmr_ing, tgt_ing)
                mmr_ing.save()

            if rec.get("pres_com_gtq") is not None and tgt_ing:
                tgt_ing.presupuesto_gtq = Decimal(str(rec["pres_com_gtq"]))
                tgt_ing.save(update_fields=["presupuesto_gtq", "updated_at"])

            if sync_vc:
                exec_vc = _cell_decimal(rec["exec_vc"])
                if exec_vc is not None and tgt_vc:
                    mmr_vc, _ = MonthlyMetricResult.objects.get_or_create(
                        plan=plan,
                        une=une,
                        metric=metric_vc,
                        year=year,
                        month=month,
                        defaults={"target_value": tgt_vc.target_value},
                    )
                    mmr_vc.target_value = tgt_vc.target_value
                    mmr_vc.measured_value = exec_vc
                    mmr_vc.calculation_note = (
                        f"Importado desde {path.name} Objetivos (referidos VC ejecución)."
                    )
                    apply_result_achievement(mmr_vc, tgt_vc)
                    mmr_vc.save()

            pts_req_exec = _cell_decimal(rec["pts_exec_req"])
            if sync_reqs and tgt_req and pts_req_exec is not None:
                if une.code == UNE.CODE_INSURANCE:
                    # Hoja: NO APLICA / 0 pts ejecución → no cumple (cuadra modo2 con Excel).
                    compliant = pts_req_exec > 0
                    ManualRequirementsCompliance.objects.update_or_create(
                        plan=plan,
                        une=une,
                        year=year,
                        month=month,
                        defaults={
                            "is_compliant": compliant,
                            "incident_note": (
                                ""
                                if compliant
                                else "Sincronizado desde Excel Objetivos (WCI reqs NO APLICA)."
                            ),
                        },
                    )
                else:
                    if pts_req_exec > 0 and int(tgt_req.points_if_achieved or 0) <= 0:
                        tgt_req.points_if_achieved = int(pts_req_exec)
                        tgt_req.save(update_fields=["points_if_achieved", "updated_at"])
                    compliant = pts_req_exec > 0
                    ManualRequirementsCompliance.objects.update_or_create(
                        plan=plan,
                        une=une,
                        year=year,
                        month=month,
                        defaults={
                            "is_compliant": compliant,
                            "incident_note": (
                                ""
                                if compliant
                                else "Sincronizado desde Excel Objetivos: no cumple reqs."
                            ),
                        },
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    f"{rec['uen']} → clientes={rec['exec_cli']} "
                    f"comisiones_gtq={rec['exec_com_gtq']} vc={rec['exec_vc']}"
                )
            )

        from django.core.management import call_command

        for mode in ("modo1", "modo2"):
            call_command("recalc_pgc", year=year, month=month, mode=mode)
        self.stdout.write(
            self.style.SUCCESS(f"Score PGC recalculado para {year}-{month:02d}.")
        )

        self.stdout.write(self.style.SUCCESS("Import PGC Objetivos completado."))
