from django.core.management.base import BaseCommand

from pgo.scorecard_cache import rebuild_scorecard_cache


class Command(BaseCommand):
    help = "Recalcula y persiste el tablero PGO por puntos (snapshot en BD)."

    def handle(self, *args, **options):
        meta = rebuild_scorecard_cache()
        self.stdout.write(
            self.style.SUCCESS(
                f"Tablero PGO guardado: {meta.computed_at:%Y-%m-%d %H:%M} "
                f"({len(meta.years)} año(s), huella {meta.fingerprint[:12]}…)"
            )
        )
