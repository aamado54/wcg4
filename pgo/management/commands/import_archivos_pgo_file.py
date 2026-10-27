"""Importa un CSV ArchivosPGO_* y recalcula el tablero por puntos."""

from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand, CommandError

from pgo import services as pgo_services

User = get_user_model()

_DEFAULT_CANDIDATES = [
    "ArchivosPGO-2026-09.csv",
    "ArchivosPGO_2026-09-.csv",
    "ArchivosPGO_2026-08-.csv",
]


def _resolve_path(explicit: str | None) -> Path:
    if explicit:
        p = Path(explicit).expanduser()
        if not p.is_file():
            raise CommandError(f"No existe el archivo: {p}")
        return p
    from django.conf import settings

    bases = [
        settings.BASE_DIR.parent / "data" / "done",
        settings.BASE_DIR / "data" / "done",
    ]
    for base in bases:
        if not base.is_dir():
            continue
        for name in _DEFAULT_CANDIDATES:
            p = base / name
            if p.is_file():
                return p
    raise CommandError(
        "Indique --path al CSV ArchivosPGO. "
        f"Buscado en data/done: {', '.join(_DEFAULT_CANDIDATES)}"
    )


class Command(BaseCommand):
    help = "Importa ArchivosPGO (catálogo PGO) y recalcula snapshot del tablero por puntos."

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            type=str,
            default="",
            help="Ruta al CSV (p. ej. ../data/done/ArchivosPGO-2026-09.csv).",
        )

    def handle(self, *args, **options):
        path = _resolve_path(options["path"] or None)
        user = User.objects.filter(is_superuser=True).first() or User.objects.first()
        if not user:
            raise CommandError("No hay usuario en BD.")

        upload = SimpleUploadedFile(path.name, path.read_bytes())
        batch = pgo_services.import_archivos_catalogo(user, upload)
        self.stdout.write(
            f"{path.name}: {batch.status} — creados={batch.creados} errores={batch.errores}"
        )
        if batch.log_texto:
            self.stdout.write(batch.log_texto[:1200])
        if batch.creados == 0 and batch.errores == 0:
            self.stdout.write(
                self.style.WARNING(
                    "Sin filas nuevas (¿reimport duplicado por hash? Renombre el archivo o borre el lote previo)."
                )
            )
        elif batch.creados > 0:
            self.stdout.write(self.style.SUCCESS("Tablero PGO recalculado (scorecard cache)."))
