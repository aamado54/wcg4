"""Rehidrata charts TV desde Postgres / siembra DB desde disco."""

from django.core.management.base import BaseCommand

from pgc.tv_charts import bootstrap_tv_persistence, db_backup_status, live_status


class Command(BaseCommand):
    help = (
        "Asegura charts TV vivos: siembra Postgres desde disco si falta, "
        "y rehidrata live/ desde Postgres si el disco está vacío."
    )

    def handle(self, *args, **options):
        result = bootstrap_tv_persistence()
        status = db_backup_status()
        live = live_status()
        live_ok = sum(1 for s in live for v in s["variants"] if v["exists"])
        self.stdout.write(
            self.style.SUCCESS(
                f"TV charts bootstrap: seeded={result['seeded']} "
                f"restored={result['restored']} "
                f"db_rows={status['count']} live_files={live_ok}/8"
            )
        )
