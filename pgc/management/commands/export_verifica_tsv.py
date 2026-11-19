"""Exporta CSV/TSV verificación PGC desde BD (prod o local)."""

from __future__ import annotations

from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from pgc.verifica_export import export_verifica


class Command(BaseCommand):
    help = (
        "Genera CSV (default) o TSV alineado a plantilla verifica.tsv (filas 62–121). "
        "Sin --template: 60 filas en bloques WC→WCL→WCI→WCINV→WCG (12 meses c/u). "
        "Requiere PGCPlan."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--format",
            type=str,
            default="csv",
            choices=("csv", "tsv"),
            help="Delimitador de salida (default csv).",
        )
        parser.add_argument(
            "--output",
            type=str,
            default="",
            help="Ruta salida (default data/done/verifica-export-2026.csv o .tsv).",
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
        fmt = options["format"]
        out_s = (options["output"] or "").strip()
        if not out_s:
            out_s = f"data/done/verifica-export-2026.{fmt}"
        out = Path(out_s).expanduser()
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
                    "export con orden plantilla por defecto (5 UNE × 12 meses)."
                )
            )
            template = None

        try:
            n = export_verifica(
                out,
                year=options["year"],
                template=template,
                mode=options["mode"],
                include_header=not options["no_header"],
                file_format=fmt,
            )
        except ValueError as exc:
            raise CommandError(str(exc)) from exc

        self.stdout.write(
            self.style.SUCCESS(
                f"Escritas {n} filas en {out} "
                f"(year={options['year']}, mode={options['mode']}, format={fmt})"
            )
        )