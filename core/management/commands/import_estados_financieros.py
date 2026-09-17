"""Importa estados financieros WC* → wcout2d → combined JSON → seed + Excel de revisión."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

ROOT = Path(settings.BASE_DIR)
TOOLS = ROOT / "tools" / "financiero"
DATA_FIN = ROOT / "data" / "wcg" / "financiero"
SEED = ROOT / "risk" / "financiero" / "seed"
DEFAULT_SOURCE = ROOT.parent / "data" / "now" / "estados-financieros"
DEFAULT_STRUCTURE = Path(
    "/home/caa/download/wcg4/lectura_de_datos_al_modelo/wcsource2512a.xlsx"
)
DEFAULT_MERGE_BASE = Path(
    "/home/caa/download/wcg4/lectura_de_datos_al_modelo/wcout2d.xlsx"
)


class Command(BaseCommand):
    help = (
        "Consolida archivos WC* (BG/ER) con wcup2, fusiona con wcout2d previo, "
        "regenera combined_series/full, sincroniza seed y exporta Excel de revisión."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--source-dir",
            type=str,
            default=str(DEFAULT_SOURCE),
            help="Directorio con archivos WCF|WCL|WCI|WCS BG/ER yyMM.xlsx",
        )
        parser.add_argument(
            "--structure",
            type=str,
            default=str(DEFAULT_STRUCTURE),
            help="Archivo de estructura (chart of accounts).",
        )
        parser.add_argument(
            "--merge-base",
            type=str,
            default=str(DEFAULT_MERGE_BASE),
            help="wcout2d previo para conservar períodos no presentes en source-dir.",
        )
        parser.add_argument(
            "--no-merge",
            action="store_true",
            help="No fusionar con wcout2d previo (solo archivos del source-dir).",
        )
        parser.add_argument(
            "--export-xlsx",
            type=str,
            default="",
            help="Ruta del Excel de volcado (default: seed/estados_financieros_tabla.xlsx).",
        )
        parser.add_argument(
            "--skip-rename",
            action="store_true",
            default=True,
            help="No renombrar archivos en source-dir (default: sí omitir).",
        )

    def handle(self, *args, **options):
        source_dir = Path(options["source_dir"]).expanduser()
        structure = Path(options["structure"]).expanduser()
        merge_base = Path(options["merge_base"]).expanduser()
        export_xlsx = (
            Path(options["export_xlsx"])
            if options["export_xlsx"]
            else SEED / "estados_financieros_tabla.xlsx"
        )

        if not source_dir.is_dir():
            raise CommandError(f"source-dir no existe: {source_dir}")
        if not structure.is_file():
            raise CommandError(f"structure no existe: {structure}")

        DATA_FIN.mkdir(parents=True, exist_ok=True)
        wcout_new = DATA_FIN / "wcout2d_new.xlsx"
        wcout_final = DATA_FIN / "wcout2d.xlsx"

        config_lines = f"{structure}\n{source_dir}\n{wcout_new}\n"
        config_path = TOOLS / "_import_config.txt"
        config_path.write_text(config_lines, encoding="utf-8")

        py = sys.executable
        wcup2 = TOOLS / "wcup2.py"
        self.stdout.write(f"1/4 wcup2 ← {source_dir}")
        cmd = [py, str(wcup2), "--config", str(config_path)]
        if options["skip_rename"]:
            cmd.append("--skip-rename")
        proc = subprocess.run(cmd, cwd=str(TOOLS), capture_output=True, text=True)
        if proc.returncode != 0:
            raise CommandError(f"wcup2 falló:\n{proc.stdout}\n{proc.stderr}")
        self.stdout.write(proc.stdout)

        if options["no_merge"]:
            shutil.copy2(wcout_new, wcout_final)
            self.stdout.write("2/4 sin fusión (solo períodos del source-dir)")
        elif merge_base.is_file():
            from tools.financiero.merge_wcout import merge_wcout

            periods = merge_wcout(merge_base, wcout_new, wcout_final)
            self.stdout.write(f"2/4 fusionado con {merge_base.name} → períodos {periods}")
        else:
            shutil.copy2(wcout_new, wcout_final)
            self.stdout.write(f"2/4 merge-base no encontrado; usando solo nuevo")

        rebuild = TOOLS / "rebuild_combined.py"
        self.stdout.write("3/4 rebuild_combined.py")
        proc = subprocess.run([py, str(rebuild)], cwd=str(ROOT), capture_output=True, text=True)
        if proc.returncode != 0:
            raise CommandError(f"rebuild_combined falló:\n{proc.stdout}\n{proc.stderr}")
        self.stdout.write(proc.stdout)

        SEED.mkdir(parents=True, exist_ok=True)
        for name in ("combined_series.json", "combined_full.json"):
            src = DATA_FIN / name
            dst = SEED / name
            shutil.copy2(src, dst)
            self.stdout.write(f"   seed ← {name}")

        from tools.financiero.export_tabla import export_financiero_tabla

        info = export_financiero_tabla(SEED / "combined_full.json", export_xlsx)
        self.stdout.write(
            self.style.SUCCESS(
                f"4/4 Excel revisión: {info['output']} "
                f"({info['accounts']} cuentas × {info['periods']} períodos)"
            )
        )
        self.stdout.write(self.style.SUCCESS("Importación estados financieros completada."))
