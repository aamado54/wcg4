"""Consolida plantillas Excel de clientes en workbook de evaluación de riesgo."""

from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from risk.evaluacion import load_evaluacion
from risk.evaluacion.plantillas import consolidate_templates


class Command(BaseCommand):
    help = (
        "Lee plantillas Excel individuales de clientes y genera un workbook "
        "compatible con /risk/evaluacion/ (Caratula + Altman + intermedias)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--source-dir",
            type=str,
            default=str(
                Path(settings.BASE_DIR).parent / "data" / "now" / "plantillas" / "ejemplos"
            ),
            help="Directorio con archivos .xlsx/.xlsm de plantillas.",
        )
        parser.add_argument(
            "--output",
            type=str,
            default="",
            help="Ruta del .xlsx de salida (default: data/now/evaluacion-desde-plantillas.xlsx).",
        )
        parser.add_argument(
            "--reference",
            type=str,
            default=str(
                Path(settings.BASE_DIR).parent
                / "data"
                / "now"
                / "WCG-evaluacion-riesgo-clientes-2025.xlsx"
            ),
            help="Workbook de referencia para copiar hoja Altman.",
        )
        parser.add_argument(
            "--validate",
            action="store_true",
            help="Ejecutar load_evaluacion() sobre el archivo generado.",
        )

    def handle(self, *args, **options):
        source = Path(options["source_dir"]).expanduser()
        if not source.is_dir():
            raise CommandError(f"source-dir no existe: {source}")

        output = (
            Path(options["output"])
            if options["output"]
            else Path(settings.BASE_DIR).parent
            / "data"
            / "now"
            / "evaluacion-desde-plantillas.xlsx"
        )
        reference = Path(options["reference"]).expanduser()
        if not reference.is_file():
            self.stdout.write(
                self.style.WARNING(f"Referencia no encontrada: {reference} (Altman mínimo)")
            )
            reference = None

        self.stdout.write(f"Fuente: {source}")
        result = consolidate_templates(source, output, reference_workbook=reference)

        self.stdout.write(
            self.style.SUCCESS(
                f"OK → {result.output_path} | archivos={result.files_processed} "
                f"empresas Caratula={result.companies_in_caratula} "
                f"hojas={', '.join(result.sheets)}"
            )
        )
        if result.alerts:
            self.stdout.write(self.style.WARNING(f"Alertas ({len(result.alerts)}):"))
            for a in result.alerts[:30]:
                self.stdout.write(f"  · {a}")
            if len(result.alerts) > 30:
                self.stdout.write(f"  … +{len(result.alerts) - 30} más")

        if options["validate"]:
            ds = load_evaluacion(path=output)
            self.stdout.write(
                f"Validación load_evaluacion: status={ds.status} "
                f"empresas={len(ds.companies)} errores={len(ds.errors)}"
            )
            for c in ds.companies:
                latest = c.latest()
                self.stdout.write(
                    f"  · {c.code} {c.name} períodos={len(c.periods)} "
                    f"último={latest.year if latest else '—'} "
                    f"z={latest.z_label if latest else '—'}"
                )
            for err in ds.errors[:10]:
                self.stdout.write(self.style.WARNING(f"  ! {err}"))
