from django.core.management.base import BaseCommand

from pgc.tv_charts_generate import regenerate_tv_live_charts


class Command(BaseCommand):
    help = "Regenera wcg-g1..g4.png (ingresos YTD) en live/ y respaldo Postgres."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Regenerar aunque la huella de datos no haya cambiado.",
        )

    def handle(self, *args, **options):
        result = regenerate_tv_live_charts(force=bool(options["force"]))
        if not result.get("ran"):
            self.stdout.write(
                self.style.WARNING(
                    f"Sin cambios ({result.get('reason', '?')}). "
                    f"Huella={result.get('fingerprint', '')[:16]}…"
                )
            )
            return
        self.stdout.write(
            self.style.SUCCESS(
                f"Charts TV actualizados: {', '.join(result.get('files') or [])} "
                f"(rango {result.get('range')})."
            )
        )
