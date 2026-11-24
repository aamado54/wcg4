from core.models import UNE, UNEAlias, MetricDefinition, Currency
from core.services.une_resolve import resolve_une_from_text
from datetime import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand, CommandError
from imports.management.import_audit_mixin import ImportAuditCommandMixin
from django.db import transaction
from imports.currency_normalize import normalize_currency_code
from imports.models import CrossSaleImportHeader, CrossSaleImportRow
from imports.venta_cruzada_parse import (
    cross_sale_row_exists,
    iter_cross_sale_rows,
    parse_cross_sale_date,
    parse_cross_sale_period,
)
from pathlib import Path
from pgc.models import PGCPlan, MonthlyTarget, MonthlyMetricResult


class Command(ImportAuditCommandMixin, BaseCommand):
    import_audit_tipo = "cross_sale"
    help = "Importa archivo de Venta Cruzada y actualiza métricas de VENTA_CRUZADA"

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            type=str,
            required=True,
            help="Ruta al archivo de Venta Cruzada (csv/tsv/xlsx->tsv)",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        path = Path(options["path"])
        if not path.exists():
            raise CommandError(f"Archivo no encontrado: {path}")

        self.stdout.write(self.style.WARNING(f"Leyendo Venta Cruzada desde {path} ..."))

        aliases = {
            a.raw_value.strip().upper(): a.une
            for a in UNEAlias.objects.select_related("une").all()
        }
        unes_by_code = {u.code: u for u in UNE.objects.all()}

        plan = PGCPlan.objects.get(year=2026)
        metric = MetricDefinition.objects.get(code=MetricDefinition.CODE_VENTA_CRUZADA)

        headers_cache = {}
        affected_months: set[tuple[int, int]] = set()
        rows_created = 0
        q_alias_count = 0
        currency_warnings: list[str] = []
        currencies = {c.code.upper(): c for c in Currency.objects.all()}
        skipped_duplicate = 0
        skipped_period = 0

        for row in iter_cross_sale_rows(path):
                periodo = (
                    row.get("Período")
                    or row.get("Periodo")
                    or row.get("PERIODO")
                    or row.get("periodo")
                )
                if not periodo:
                    continue

                parsed_period = parse_cross_sale_period(periodo)
                if not parsed_period:
                    skipped_period += 1
                    continue
                year, month = parsed_period
                affected_months.add((year, month))

                cliente = (
                    row.get("Cliente")
                    or row.get("CLIENTE")
                    or row.get("cliente")
                    or ""
                ).strip()

                operacion = (
                    row.get("Operación")
                    or row.get("Operacion")
                    or row.get("OPERACION")
                    or row.get("operacion")
                    or ""
                ).strip()

                fecha_cell = (
                    row.get("Fecha")
                    or row.get("FECHA")
                    or row.get("fecha")
                )
                fecha_raw = (
                    ""
                    if fecha_cell is None
                    else (fecha_cell if isinstance(fecha_cell, str) else str(fecha_cell))
                ).strip()

                moneda_raw = (
                    row.get("Moneda")
                    or row.get("MONEDA")
                    or row.get("moneda")
                    or ""
                )

                une_dest_raw = (
                    row.get("UNE")
                    or row.get("une")
                    or ""
                ).strip()

                une_origin_raw = (
                    row.get("UNE que refiere")
                    or row.get("UNE QUE REFIERE")
                    or row.get("une que refiere")
                    or ""
                ).strip()

                if not une_dest_raw:
                    continue

                une_destination = resolve_une_from_text(
                    une_dest_raw,
                    aliases=aliases,
                    unes_by_code=unes_by_code,
                )

                une_origin = resolve_une_from_text(
                    une_origin_raw,
                    aliases=aliases,
                    unes_by_code=unes_by_code,
                )

                currency = None
                moneda_code, currency_warn = normalize_currency_code(moneda_raw)
                if currency_warn:
                    q_alias_count += 1
                    if len(currency_warnings) < 8:
                        currency_warnings.append(currency_warn)
                if moneda_code:
                    currency = currencies.get(moneda_code)

                header_key = (year, month)
                header = headers_cache.get(header_key)
                if header is None:
                    header = CrossSaleImportHeader.objects.filter(
                        year=year, month=month
                    ).first()
                    if header is None:
                        from imports.models import FileUpload, guess_file_format

                        upload = FileUpload.objects.filter(
                            file_type_detected=FileUpload.TYPE_CROSS_SALE,
                            detected_year=year,
                            detected_month=month,
                        ).order_by("-id").first()
                        if upload is None:
                            upload = FileUpload.objects.create(
                                original_filename=path.name,
                                file_format=guess_file_format(path.name),
                                file_type_detected=FileUpload.TYPE_CROSS_SALE,
                                detected_year=year,
                                detected_month=month,
                                status=FileUpload.STATUS_UPLOADED,
                            )
                            # Adjuntar archivo existente si la ruta es local
                            try:
                                from django.core.files import File as DjFile

                                with path.open("rb") as fh:
                                    upload.stored_file.save(path.name, DjFile(fh), save=True)
                            except Exception:
                                upload.save()
                        header = CrossSaleImportHeader.objects.create(
                            file_upload=upload,
                            year=year,
                            month=month,
                        )
                    headers_cache[header_key] = header

                parsed_date = parse_cross_sale_date(fecha_cell)

                if cross_sale_row_exists(
                    year=year,
                    month=month,
                    client_name=cliente,
                    operation_code=operacion,
                    row_date=parsed_date,
                    currency_id=currency.id if currency else None,
                    une_destination_id=une_destination.id if une_destination else None,
                    une_origin_id=une_origin.id if une_origin else None,
                ):
                    skipped_duplicate += 1
                    continue

                CrossSaleImportRow.objects.create(
                    header=header,
                    year=year,
                    month=month,
                    client_name=cliente,
                    operation_code=operacion,
                    date=parsed_date,
                    currency=currency,
                    une_destination=une_destination,
                    une_origin=une_origin,
                    raw_une_destination=une_dest_raw,
                    raw_une_origin=une_origin_raw,
                )
                rows_created += 1

        counts_by_origin: dict[tuple[int, int, int], int] = {}
        for year, month in affected_months:
            qs = CrossSaleImportRow.objects.filter(year=year, month=month).only(
                "une_origin_id", "une_destination_id"
            )
            for cs_row in qs.iterator():
                if cs_row.une_origin_id and cs_row.une_destination_id:
                    key_origin = (year, month, cs_row.une_origin_id)
                    counts_by_origin[key_origin] = counts_by_origin.get(key_origin, 0) + 1

        for (year, month, une_origin_id), count in counts_by_origin.items():
            une_origin = UNE.objects.get(id=une_origin_id)
        
            target = MonthlyTarget.objects.filter(
                plan=plan,
                une=une_origin,
                metric=metric,
                year=year,
                month=month,
            ).first()
        
            target_value = target.target_value if target else Decimal("1")
            is_achieved = Decimal(str(count)) >= target_value
        
            MonthlyMetricResult.objects.update_or_create(
                plan=plan,
                metric=metric,
                une=une_origin,
                year=year,
                month=month,
                defaults={
                    "measured_value": Decimal(str(count)),
                    "target_value": target_value,
                    "is_achieved": is_achieved,
                    "points_awarded": 0,
                    "calculation_note": f"{count} referencias válidas de venta cruzada en el mes",
                },
            )

        if skipped_period:
            self.stdout.write(
                self.style.WARNING(
                    f"Omitidas {skipped_period} fila(s) con período no reconocido."
                )
            )
        if skipped_duplicate:
            self.stdout.write(
                self.style.WARNING(
                    f"Omitidas {skipped_duplicate} fila(s) ya existentes (sin duplicar)."
                )
            )
        if rows_created:
            self.stdout.write(
                self.style.SUCCESS(f"Filas nuevas guardadas: {rows_created}.")
            )

        if q_alias_count:
            for w in currency_warnings:
                self.stdout.write(self.style.WARNING(w))
            self.stdout.write(
                self.style.WARNING(
                    f"WARNING moneda: {q_alias_count} fila(s) con 'Q' (u alias) "
                    f"tratadas como GTQ. Corrija el archivo fuente a GTQ."
                )
            )

        self.stdout.write(self.style.SUCCESS("Venta cruzada importada correctamente."))

        try:
            from pgc.admin_recalc import maybe_auto_recalc

            auto = maybe_auto_recalc(source="import_venta_cruzada")
            if auto and auto.get("ran"):
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Auto-recalcular: {auto.get('periods_processed', 0)} período(s)."
                    )
                )
        except Exception as exc:
            self.stdout.write(
                self.style.WARNING(f"Auto-recalcular no completó: {exc}")
            )

