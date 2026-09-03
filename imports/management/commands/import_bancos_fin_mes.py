from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from imports.investment_growth_parse import parse_bancos_fin_mes_xlsx
from imports.models import BankLoanMonthSnapshot, FileUpload


class Command(BaseCommand):
    help = (
        "Importa Bancos_Fin_de_mes.xlsx (préstamos bancarios al cierre). "
        "Detecta rangos USD/GTQ desde la fórmula de la columna Quetzalizado."
    )

    def add_arguments(self, parser):
        parser.add_argument("--path", type=str, required=True)
        parser.add_argument("--file-upload-id", type=int, default=None)

    @transaction.atomic
    def handle(self, *args, **options):
        path = Path(options["path"])
        if not path.exists():
            raise CommandError(f"Archivo no encontrado: {path}")

        snapshots = parse_bancos_fin_mes_xlsx(path)
        if not snapshots:
            raise CommandError("No se leyeron períodos válidos del archivo de bancos.")

        upload = None
        if options.get("file_upload_id"):
            upload = FileUpload.objects.filter(pk=options["file_upload_id"]).first()
            if not upload:
                raise CommandError(f"FileUpload id={options['file_upload_id']} no encontrado.")

        upserted = 0
        for snap in snapshots:
            BankLoanMonthSnapshot.objects.update_or_create(
                year=snap.year,
                month=snap.month,
                defaults={
                    "file_upload": upload,
                    "exchange_rate": snap.exchange_rate,
                    "total_gtq": snap.total_gtq,
                    "total_usd": snap.total_usd,
                    "bank_amounts_json": {
                        name: str(amount) for name, amount in snap.bank_amounts.items()
                    },
                },
            )
            upserted += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Actualizados {upserted} cierres bancarios: "
                + ", ".join(f"{s.year}-{s.month:02d}" for s in snapshots)
            )
        )
