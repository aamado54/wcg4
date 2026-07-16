from django.core.management.base import BaseCommand, CommandError

from pgc.income_conversion import recalc_stale_ingresos


class Command(BaseCommand):
    help = (
        "Recalcula INGRESOS con conversion_status=STALE_FX "
        "desde source_value GTQ usando el TC actual del mes."
    )

    def add_arguments(self, parser):
        parser.add_argument("--year", type=int, required=True)
        parser.add_argument("--month", type=int, required=True)

    def handle(self, *args, **options):
        year = options["year"]
        month = options["month"]
        try:
            result = recalc_stale_ingresos(year=year, month=month, only_stale=True)
        except ValueError as exc:
            raise CommandError(str(exc)) from exc

        self.stdout.write(
            self.style.SUCCESS(
                f"{year}-{month:02d}: {result['updated']} ingreso(s) recalculado(s) "
                f"con TC={result['fx']}."
            )
        )
