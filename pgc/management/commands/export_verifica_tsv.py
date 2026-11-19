"""Exporta TSV verificación PGC desde BD (prod o local)."""

from __future__ import annotations

from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from pgc.verifica_export import export_verifica_tsv


class Command(BaseCommand):
    help = (
        "Genera TSV alineado a plantilla verifica.tsv (filas 62–121). "
        "Sin --template usa 12×5 filas WC*. Requiere PGCPlan."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            type=str,
            default="data/done/verifica-export-2026.tsv",
            help="Ruta salida TSV (default data/done/verifica-export-2026.tsv).",
        )
        parser.add_argument(
            "--template",
            type=str,
            default="../data/ref/verifica.tsv",
            help="Plantilla verifica.tsv (default ../data/ref/verifica.tsv).",
        )
        parser.add_argument(
            "--no-header",
            action="store_true",
            help="No escribir fila de cabecera.",
        )
        parser.add_argument(
            "--year",
            type=int,
            default=2026,
        )
        parser.add_argument(
            "--mode",
            type=str,
            default="modo2",
            help="Modalidad score para columnas de puntos (default modo2).",
        )

    def handle(self, *args, **options):
        out = Path(options["output"]).expanduser()
        if not out.is_absolute():
            out = Path.cwd() / out

        template_s = (options["template"] or "").strip()
        template = Path(template_s).expanduser() if template_s else None
        if template and not template.is_absolute():
            template = Path.cwd() / template
        if template and not template.is_file():
            self.stdout.write(
                self.style.WARNING(
                    f"Plantilla no encontrada: {template}; "
                    "export con filas 12×5 por defecto (mismas columnas A–J)."
                )
            )
            template = None

        try:
            n = export_verifica_tsv(
                out,
                year=options["year"],
                template=template,
                mode=options["mode"],
                include_header=not options["no_header"],
            )
        except ValueError as exc:
            raise CommandError(str(exc)) from exc

        self.stdout.write(
            self.style.SUCCESS(
                f"Escritas {n} filas en {out} (year={options['year']}, mode={options['mode']})"
            )
        )