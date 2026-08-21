"""Repara is_achieved / points_awarded en MonthlyMetricResult de INGRESOS."""

from django.core.management.base import BaseCommand

from pgc.income_conversion import sync_ingresos_achievements


class Command(BaseCommand):
    help = (
        "Sincroniza Cumple y puntos de INGRESOS en MonthlyMetricResult "
        "con la regla real >= meta (modo1)."
    )

    def add_arguments(self, parser):
        parser.add_argument("--year", type=int, default=None)

    def handle(self, *args, **options):
        year = options.get("year")
        result = sync_ingresos_achievements(year=year)
        self.stdout.write(
            self.style.SUCCESS(
                f"Revisados={result['checked']} actualizados={result['updated']}"
            )
        )
        for item in result.get("mismatches", [])[:40]:
            self.stdout.write(
                f"  {item['une']} {item['period']}: "
                f"measured={item['measured']} "
                f"{item['before']} -> {item['after']}"
            )
        if len(result.get("mismatches", [])) > 40:
            self.stdout.write(f"  ... y {len(result['mismatches']) - 40} más")
