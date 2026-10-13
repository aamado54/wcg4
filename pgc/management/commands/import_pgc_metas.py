"""Importa metas mensuales PGC desde TSV oficial (clientes + ingresos)."""

from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from core.models import MetricDefinition, UNE
from pgc.income_conversion import apply_result_achievement
from pgc.models import MonthlyMetricResult, MonthlyTarget, PGCPlan

MONTH_LABELS = (
    "ene",
    "feb",
    "mar",
    "abr",
    "may",
    "jun",
    "jul",
    "ago",
    "sep",
    "oct",
    "nov",
    "dic",
)
MONTH_NUM = {label: idx + 1 for idx, label in enumerate(MONTH_LABELS)}

UNE_SECTIONS = {
    "METAS FACTORING": "FACTORING",
    "METAS LEASING": "LEASING",
    "METAS INVESTMENT": "INVESTMENT",
}


def _parse_decimal(raw: str) -> Decimal:
    text = (raw or "").strip().replace(",", "")
    if not text:
        return Decimal("0")
    try:
        return Decimal(text)
    except InvalidOperation as exc:
        raise ValueError(f"Valor numérico inválido: {raw!r}") from exc


def _parse_tsv(path: Path) -> dict[str, dict[str, dict[int, Decimal]]]:
    """
    Retorna {UNE_CODE: {"CLIENTES_NUEVOS": {month: val}, "INGRESOS": {month: val}}}.
    Insurance suma Personas + Empresas por mes.
    """
    lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    out: dict[str, dict[str, dict[int, Decimal]]] = {}
    insurance_parts: list[dict[str, dict[int, Decimal]]] = []

    i = 0
    while i < len(lines):
        line = lines[i]
        header = line.strip()

        if header.startswith("METAS INSURANCE PERSONAS") or header.startswith(
            "METAS INSURANCE EMPRESAS"
        ):
            i += 1
            cli_row = [c.strip() for c in lines[i].split("\t")]
            i += 1
            ing_row = [c.strip() for c in lines[i].split("\t")]
            i += 1
            part = {"CLIENTES_NUEVOS": {}, "INGRESOS": {}}
            for label in MONTH_LABELS:
                col = MONTH_NUM[label] + 1  # col 0=label, 1=total
                month = MONTH_NUM[label]
                part["CLIENTES_NUEVOS"][month] = _parse_decimal(cli_row[col])
                part["INGRESOS"][month] = _parse_decimal(ing_row[col])
            insurance_parts.append(part)
            continue

        une_code = None
        for prefix, code in UNE_SECTIONS.items():
            if header.startswith(prefix):
                une_code = code
                break
        if not une_code:
            i += 1
            continue

        i += 1
        cli_row = [c.strip() for c in lines[i].split("\t")]
        i += 1
        ing_row = [c.strip() for c in lines[i].split("\t")]
        i += 1

        out[une_code] = {"CLIENTES_NUEVOS": {}, "INGRESOS": {}}
        for label in MONTH_LABELS:
            col = MONTH_NUM[label] + 1
            month = MONTH_NUM[label]
            out[une_code]["CLIENTES_NUEVOS"][month] = _parse_decimal(cli_row[col])
            out[une_code]["INGRESOS"][month] = _parse_decimal(ing_row[col])

    if len(insurance_parts) != 2:
        raise ValueError(
            "Se esperaban secciones METAS INSURANCE PERSONAS y METAS INSURANCE EMPRESAS."
        )

    out["INSURANCE"] = {"CLIENTES_NUEVOS": {}, "INGRESOS": {}}
    for month in range(1, 13):
        out["INSURANCE"]["CLIENTES_NUEVOS"][month] = sum(
            p["CLIENTES_NUEVOS"][month] for p in insurance_parts
        )
        out["INSURANCE"]["INGRESOS"][month] = sum(
            p["INGRESOS"][month] for p in insurance_parts
        )
    return out


def _default_tsv_path() -> Path:
    return Path(__file__).resolve().parents[4] / "data" / "now" / "PGC-metas-2026.tsv"


class Command(BaseCommand):
    help = (
        "Carga metas mensuales PGC (CLIENTES_NUEVOS e INGRESOS) desde el TSV oficial. "
        "Valores en miles de US$; no son acumulados."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            type=str,
            default=str(_default_tsv_path()),
            help="Ruta al TSV oficial (p. ej. PGC-metas-2026.tsv).",
        )
        parser.add_argument("--year", type=int, default=2026)
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Solo muestra cambios sin guardar.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        path = Path(options["path"]).expanduser()
        year = options["year"]
        dry_run = options["dry_run"]

        if not path.is_file():
            raise CommandError(f"Archivo no encontrado: {path}")

        if not re.search(r"20\d{2}", path.name):
            self.stdout.write(
                self.style.WARNING(f"Nombre de archivo sin año explícito: {path.name}")
            )

        try:
            parsed = _parse_tsv(path)
        except Exception as exc:
            raise CommandError(f"Error leyendo TSV: {exc}") from exc

        try:
            plan = PGCPlan.objects.get(year=year)
        except PGCPlan.DoesNotExist:
            raise CommandError(f"No existe PGCPlan para {year}")

        metric_cli = MetricDefinition.objects.get(code=MetricDefinition.CODE_CLIENTES_NUEVOS)
        metric_ing = MetricDefinition.objects.get(code=MetricDefinition.CODE_INGRESOS)

        updated_targets = 0
        updated_results = 0
        months_touched: set[int] = set()

        for une_code, metrics in parsed.items():
            try:
                une = UNE.objects.get(code=une_code)
            except UNE.DoesNotExist:
                raise CommandError(f"UNE no encontrada: {une_code}")

            for metric_code, month_values in metrics.items():
                metric = metric_cli if metric_code == "CLIENTES_NUEVOS" else metric_ing
                for month, new_value in month_values.items():
                    tgt = MonthlyTarget.objects.filter(
                        plan=plan,
                        une=une,
                        metric=metric,
                        year=year,
                        month=month,
                    ).first()
                    if not tgt:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Sin MonthlyTarget {une_code} {metric_code} {year}-{month:02d}"
                            )
                        )
                        continue

                    old_value = tgt.target_value
                    if old_value == new_value:
                        continue

                    self.stdout.write(
                        f"{une_code} {metric_code} {year}-{month:02d}: "
                        f"{old_value} → {new_value}"
                    )
                    if not dry_run:
                        tgt.target_value = new_value
                        tgt.save(update_fields=["target_value", "updated_at"])
                    updated_targets += 1
                    months_touched.add(month)

                    if dry_run:
                        continue

                    for result in MonthlyMetricResult.objects.filter(
                        plan=plan,
                        une=une,
                        metric=metric,
                        year=year,
                        month=month,
                    ):
                        changed = apply_result_achievement(result, tgt)
                        if changed:
                            result.save(update_fields=changed + ["updated_at"])
                            updated_results += 1

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f"Dry-run: {updated_targets} metas cambiarían; "
                    f"sin recalcular score."
                )
            )
            return

        if months_touched:
            from django.core.management import call_command

            for month in sorted(months_touched):
                for mode in ("modo1", "modo2"):
                    call_command("recalc_pgc", year=year, month=month, mode=mode)

        self.stdout.write(
            self.style.SUCCESS(
                f"Metas actualizadas: {updated_targets}; "
                f"resultados re-sincronizados: {updated_results}; "
                f"meses recalculados: {len(months_touched)}."
            )
        )
