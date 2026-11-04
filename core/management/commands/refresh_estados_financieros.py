"""Comando único: integración EEFF (wcup2 + fusión + JSON + Excel de revisión y vaciado)."""

from __future__ import annotations

from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from tools.financiero.pipeline_integracion import default_paths, run_integracion


class Command(BaseCommand):
    help = (
        "Integra estados financieros WCG: archivos WC* en ~/download/eeff, "
        "sustituye meses yyMM >= --override-from sobre merge-base, "
        "regenera JSON y los dos Excel en ~/download/eeff/other."
    )

    def add_arguments(self, parser):
        p = default_paths()
        parser.add_argument(
            "--override-from",
            type=int,
            default=2606,
            help="Primer yyMM a tomar del source-dir (default 2606 = jun 2026).",
        )
        parser.add_argument(
            "--source-dir",
            type=str,
            default=str(p["eeff_source"]),
            help="Directorio con WCF|WCL|WCI|WCS-ER|BG-yyMM.xlsx",
        )
        parser.add_argument(
            "--structure",
            type=str,
            default=str(p["structure"]),
            help="Plan de cuentas (wcsource2512a.xlsx).",
        )
        parser.add_argument(
            "--merge-base",
            type=str,
            default=str(p["merge_base"]),
            help="wcout2d con meses que NO se pisan (hasta mayo 2026 si base Jul-2026).",
        )
        parser.add_argument(
            "--out-tabla",
            type=str,
            default=str(p["eeff_output"] / "estados_financieros_tabla.xlsx"),
        )
        parser.add_argument(
            "--out-vaciado",
            type=str,
            default=str(p["eeff_output"] / "estados-financieros-vaciado-2026-09-16.xlsx"),
        )
        parser.add_argument(
            "--sync-wcsource",
            action="store_true",
            help="Copiar fuentes canónicas a modelo financiero/.../wcsource.",
        )
        parser.add_argument(
            "--promote-merge-base",
            action="store_true",
            help="Tras validar salida, guardar wcout2d fusionado como nuevo merge-base.",
        )

    def handle(self, *args, **options):
        try:
            result = run_integracion(
                override_from_yymm=options["override_from"],
                source_dir=Path(options["source_dir"]),
                structure=Path(options["structure"]),
                merge_base=Path(options["merge_base"]),
                out_tabla=Path(options["out_tabla"]),
                out_vaciado=Path(options["out_vaciado"]),
                sync_wcsource_mirror=options["sync_wcsource"],
                promote_merge_base=options["promote_merge_base"],
            )
        except (FileNotFoundError, ValueError, RuntimeError) as exc:
            raise CommandError(str(exc)) from exc

        self.stdout.write(
            self.style.SUCCESS(
                f"OK cuentas={result.accounts} períodos={len(result.periods)} "
                f"advertencias={result.warnings_count}\n"
                f"  tabla: {result.tabla_revision}\n"
                f"  vaciado: {result.vaciado}\n"
                f"  wcout2d: {result.wcout_final}"
            )
        )
        if result.periods:
            self.stdout.write(f"  últimos meses: {', '.join(result.periods[-4:])}")
