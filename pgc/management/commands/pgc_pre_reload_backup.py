"""Guía y export lógico PGC antes de recarga (opciones A+B aprobadas)."""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core import serializers
from django.core.management.base import BaseCommand, CommandError


# Tablas núcleo PGC + importaciones que alimentan score (orden dumpdata)
PGC_DUMP_LABELS = [
    "core.une",
    "core.unedalias",
    "core.metricdefinition",
    "pgc.pgcplan",
    "pgc.pgcmode",
    "pgc.monthlyexchangerate",
    "pgc.monthlytarget",
    "pgc.monthlymetricresult",
    "pgc.monthlymetricscore",
    "pgc.monthlymodescorecard",
    "pgc.manualrequirementscompliance",
    "pgc.metricreserve",
    "imports.fileupload",
    "imports.newclientimportrow",
    "imports.newclientimportheader",
    "imports.crosssaleimportrow",
    "imports.crosssaleimportheader",
    "imports.investmentgrowthrow",
    "imports.bankloanmonthsnapshot",
    "imports.financialstatementimportheader",
    "imports.importauditevent",
]


class Command(BaseCommand):
    help = (
        "Opción B: export JSON PGC a media/audit. "
        "Con --instructions imprime pasos Railway (opción A pg_dump) sin ejecutar en prod."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--output-dir",
            type=str,
            default="",
            help="Directorio salida (default MEDIA_ROOT/audit/pgc-backup-YYYYMMDD-HHMM).",
        )
        parser.add_argument(
            "--instructions",
            action="store_true",
            help="Solo muestra checklist A+B para ejecutar en Railway (no escribe dump).",
        )
        parser.add_argument(
            "--pg-dump-hint",
            action="store_true",
            help="Imprime comando pg_dump sugerido (requiere DATABASE_URL en shell Railway).",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Con export JSON: no escribe archivos.",
        )

    def _default_out_dir(self) -> Path:
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        return Path(settings.MEDIA_ROOT) / "audit" / f"pgc-backup-{stamp}"

    def _print_instructions(self) -> None:
        lines = [
            "# Respaldo A+B antes de recarga PGC (aprobado coordinador)",
            "",
            "## A — Snapshot Railway (infra)",
            "1. Panel Railway → servicio **PostgreSQL** → **Backups** → crear backup manual",
            "   **o** duplicar environment (fork) con la misma base.",
            "2. Anotar timestamp y ID del backup en ticket de recarga.",
            "3. Probar restore en environment **no prod** antes del GO.",
            "",
            "## B — Export lógico (este repo)",
            "```bash",
            "cd dashboard",
            "python manage.py pgc_pre_reload_backup",
            "```",
            "Genera `media/audit/pgc-backup-*/pgc_data.json` + `manifest.json`.",
            "Descargar carpeta completa desde Railway volume o `railway run` + copia.",
            "",
            "## A en CLI (PostgreSQL service shell)",
            "Con `DATABASE_URL` en el entorno del contenedor web o plugin Postgres:",
            "```bash",
            "pg_dump \"$DATABASE_URL\" -Fc -f /tmp/wcg_pgc_full_$(date +%Y%m%d).dump",
            "```",
            "Alternativa solo apps Django (más lento, portable): usar solo paso B.",
            "",
            "## Después del backup",
            "- No ejecutar delete/reload hasta confirmar restore de prueba.",
            "- Archivar: dump A + JSON B + `export_verifica_tsv` del día.",
            "",
            "## GO / NO-GO",
            "- GO solo si A **o** B verificado restaurable + coordinador escribe OK.",
        ]
        self.stdout.write("\n".join(lines))

    def _print_pg_dump_hint(self) -> None:
        db_url = os.environ.get("DATABASE_URL", "${DATABASE_URL}")
        self.stdout.write("Comando sugerido en shell Railway (opción A):")
        self.stdout.write(
            f'pg_dump "{db_url}" -Fc --no-owner --no-acl '
            f"-f /tmp/wcg_pre_reload_$(date +%Y%m%d_%H%M).dump"
        )
        self.stdout.write(
            "Tablas críticas PGC (referencia): pgc_*, imports_* ligados a PGC, "
            "core_une, core_metricdefinition."
        )

    def handle(self, *args, **options):
        if options["instructions"]:
            self._print_instructions()
            return

        if options["pg_dump_hint"]:
            self._print_pg_dump_hint()
            return

        out_dir = Path(options["output_dir"]).expanduser() if options["output_dir"] else self._default_out_dir()
        dry = options["dry_run"]

        missing = []
        for label in PGC_DUMP_LABELS:
            app_label, model_name = label.split(".")
            try:
                from django.apps import apps

                apps.get_model(app_label, model_name)
            except LookupError:
                missing.append(label)

        if missing:
            self.stderr.write(f"Modelos omitidos (no instalados): {', '.join(missing)}")

        labels_ok = [lb for lb in PGC_DUMP_LABELS if lb not in missing]
        data_path = out_dir / "pgc_data.json"
        manifest_path = out_dir / "manifest.json"

        if dry:
            self.stdout.write(f"[dry-run] Escribiría {data_path} ({len(labels_ok)} modelos)")
            return

        out_dir.mkdir(parents=True, exist_ok=True)

        objects = self._collect_objects(labels_ok)
        with data_path.open("w", encoding="utf-8") as f:
            serializers.serialize(
                "json",
                objects,
                stream=f,
                indent=2,
                use_natural_foreign_keys=True,
            )

        manifest = {
            "created_at": datetime.now().isoformat(),
            "django_settings": os.environ.get("DJANGO_SETTINGS_MODULE", ""),
            "labels": labels_ok,
            "bytes": data_path.stat().st_size,
            "backup_options": "A+B approved",
            "note": "Restaurar con loaddata en staging; validar FK order.",
        }
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

        self.stdout.write(self.style.SUCCESS(f"Backup B: {data_path} ({manifest['bytes']} bytes)"))
        self.stdout.write(self.style.SUCCESS(f"Manifiesto: {manifest_path}"))
        self.stdout.write("Ejecute también opción A en Railway antes de cualquier recarga.")

    def _collect_objects(self, labels: list[str]) -> list:
        from django.apps import apps

        items = []
        for label in labels:
            app_label, model_name = label.split(".")
            model = apps.get_model(app_label, model_name)
            items.extend(model.objects.all())
        return items