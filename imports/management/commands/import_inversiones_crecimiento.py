from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from imports.investment_growth_parse import parse_inversiones_crecimiento_csv
from imports.models import FileUpload, InvestmentGrowthRow


class Command(BaseCommand):
    help = (
        "Importa Inversiones_crecimiento (CSV). Puede traer varios meses; "
        "reemplaza los saldos AP/PG de cada período incluido."
    )

    def add_arguments(self, parser):
        parser.add_argument("--path", type=str, required=True)
        parser.add_argument("--file-upload-id", type=int, default=None)
        parser.add_argument(
            "--replace-periods",
            action="store_true",
            default=True,
            help="Borra saldos previos de los meses presentes en el archivo (default).",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        path = Path(options["path"])
        if not path.exists():
            raise CommandError(f"Archivo no encontrado: {path}")

        parsed = parse_inversiones_crecimiento_csv(path)
        if not parsed:
            raise CommandError("No se leyeron filas válidas del archivo.")

        upload = None
        if options.get("file_upload_id"):
            upload = FileUpload.objects.filter(pk=options["file_upload_id"]).first()
            if not upload:
                raise CommandError(f"FileUpload id={options['file_upload_id']} no encontrado.")

        periods = sorted({(row.year, row.month) for row in parsed})
        if options.get("replace_periods", True):
            period_q = None
            for year, month in periods:
                clause = {"year": year, "month": month}
                if period_q is None:
                    from django.db.models import Q

                    period_q = Q(**clause)
                else:
                    period_q |= Q(**clause)
            deleted, _ = InvestmentGrowthRow.objects.filter(period_q).delete()
            self.stdout.write(f"Eliminados {deleted} saldos previos en {len(periods)} período(s).")

        created = 0
        for row in parsed:
            InvestmentGrowthRow.objects.create(
                file_upload=upload,
                year=row.year,
                month=row.month,
                instrument=row.instrument,
                company=row.company,
                operation_code=row.operation_code,
                currency_code=row.currency_code,
                amount_original=row.amount_original,
                start_date=row.start_date,
                maturity_date=row.maturity_date,
                exchange_rate=row.exchange_rate,
                amount_gtq=row.amount_gtq,
                amount_usd=row.amount_usd,
                source_row_number=row.source_row_number,
            )
            created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Importados {created} saldos AP/PG en {len(periods)} período(s): "
                + ", ".join(f"{y}-{m:02d}" for y, m in periods)
            )
        )
