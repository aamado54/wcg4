"""Recalcula PgoPeriodScore desde PgoResultadoPeriodo + PgoMetricRule."""

from decimal import Decimal, InvalidOperation

from django.core.management.base import BaseCommand, CommandError

from apps.pgo.services import DEFAULT_QUALIFY_THRESHOLD, recalculate_pgo_scores


class Command(BaseCommand):
    help = (
        "Recalcula la tabla de resultados PGO (PgoPeriodScore.puntaje_total / clasifica) "
        "a partir de PgoResultadoPeriodo y PgoMetricRule. Umbral default: 80."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--periodo",
            type=str,
            default="",
            help="Filtrar período YYYY-MM (opcional).",
        )
        parser.add_argument(
            "--threshold",
            type=str,
            default=str(DEFAULT_QUALIFY_THRESHOLD),
            help="Umbral de clasificación (default 80).",
        )
        parser.add_argument(
            "--no-ensure-rules",
            action="store_true",
            help="No sembrar reglas default si el catálogo está vacío.",
        )

    def handle(self, *args, **options):
        periodo = (options.get("periodo") or "").strip() or None
        try:
            threshold = Decimal(str(options["threshold"]))
        except (InvalidOperation, TypeError) as exc:
            raise CommandError(f"threshold inválido: {options['threshold']}") from exc

        result = recalculate_pgo_scores(
            periodo=periodo,
            threshold=threshold,
            ensure_rules=not options["no_ensure_rules"],
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"PGO scores OK — fuente={result['periodos_fuente']} "
                f"escritos={result['scores_escritos']} "
                f"reglas_nuevas={result['rules_created']} "
                f"umbral={result['threshold']}"
            )
        )
        for score in result["scores"][:20]:
            un = score.unidad_negocio.codigo if score.unidad_negocio_id else "—"
            flag = "Sí" if score.clasifica else "No"
            self.stdout.write(
                f"  {score.periodo} · {un} · {score.puntaje_total} · Clasifica={flag}"
            )
