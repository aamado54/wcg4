from core.models import UNE, UNEAlias, MetricDefinition, Currency
from core.services.une_resolve import resolve_une_from_text
from datetime import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from imports.models import CrossSaleImportHeader, CrossSaleImportRow
from pathlib import Path
from pgc.models import PGCPlan, MonthlyTarget, MonthlyMetricResult
import csv


class Command(BaseCommand):
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
        counts_by_pair = {}
        counts_by_origin = {}  # (year, month, une_origin_id) -> int

        with path.open("r", encoding="utf-8-sig") as f:
            sample = f.read(4096)
            f.seek(0)

            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=[",", "\t", ";"])
            except csv.Error:
                delimiter = "\t" if "\t" in sample else ","
                dialect = csv.excel_tab if delimiter == "\t" else csv.excel
          
            reader = csv.DictReader(f, dialect=dialect)

            for row in reader:
                periodo = (
                    row.get("Período")
                    or row.get("Periodo")
                    or row.get("PERIODO")
                    or row.get("periodo")
                )
                if not periodo:
                    continue

                try:
                    year_str, month_str = str(periodo).replace("-", "/").split("/")
                    year = int(year_str)
                    month = int(month_str)
                except Exception:
                    continue

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

                fecha_raw = (
                    row.get("Fecha")
                    or row.get("FECHA")
                    or row.get("fecha")
                    or ""
                ).strip()

                moneda_raw = (
                    row.get("Moneda")
                    or row.get("MONEDA")
                    or row.get("moneda")
                    or ""
                ).strip().upper()

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
                if moneda_raw:
                    currency = Currency.objects.filter(code__iexact=moneda_raw).first()

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

                parsed_date = None
                if fecha_raw:
                    try:
                        parsed_date = datetime.fromisoformat(
                            fecha_raw.replace("Z", "+00:00")
                        ).date()
                    except Exception:
                        try:
                            parsed_date = datetime.strptime(
                                fecha_raw[:10], "%Y-%m-%d"
                            ).date()
                        except Exception:
                            parsed_date = None

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

                if une_origin and une_destination:
                    key_pair = (year, month, une_origin.id, une_destination.id)
                    counts_by_pair[key_pair] = counts_by_pair.get(key_pair, 0) + 1
                
                    key_origin = (year, month, une_origin.id)
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

        self.stdout.write(self.style.SUCCESS("Venta cruzada importada correctamente."))