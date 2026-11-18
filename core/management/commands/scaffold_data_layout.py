"""Crea árbol data/pgc|pgo/YYMM y carpetas otros/ sin borrar ni renombrar archivos."""

from __future__ import annotations

import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


def _repo_data_root() -> Path:
    """Raíz `data/` del monorepo (wcg4/data), no dashboard/data."""
    base = Path(settings.BASE_DIR)
    if (base.parent / "data").is_dir() or base.name == "dashboard":
        return base.parent / "data"
    return base / "data"


OTROS_PATHS = (
    "pgc/otros",
    "pgo/otros",
    "otros",
)


class Command(BaseCommand):
    help = (
        "Scaffold layout data/pgc/YYMM y data/pgo/YYMM + otros/. "
        "Nunca elimina archivos; solo crea carpetas y manifest.json vacíos."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--year",
            type=int,
            default=2026,
            help="Año para carpetas YYMM (default 2026).",
        )
        parser.add_argument(
            "--months",
            type=str,
            default="1-12",
            help="Meses: 1-12, 8,9 o 8-10.",
        )

    def handle(self, *args, **options):
        root = _repo_data_root()
        year = options["year"]
        months = self._parse_months(options["months"])

        for sub in (*OTROS_PATHS, "ref"):
            d = root.joinpath(*sub.split("/"))
            d.mkdir(parents=True, exist_ok=True)
            keep = d / ".gitkeep"
            if not keep.exists():
                keep.write_text("", encoding="utf-8")

        for month in months:
            yymm = f"{year % 100:02d}{month:02d}"
            for module in ("pgc", "pgo"):
                period_dir = root / module / yymm
                period_dir.mkdir(parents=True, exist_ok=True)
                manifest = period_dir / "manifest.json"
                if not manifest.exists():
                    manifest.write_text(
                        json.dumps(
                            {
                                "period": {"year": year, "month": month},
                                "module": module,
                                "files": [],
                                "note": "Añadir entradas sin mover archivos legados sin acuerdo.",
                            },
                            indent=2,
                            ensure_ascii=False,
                        )
                        + "\n",
                        encoding="utf-8",
                    )

        self.stdout.write(self.style.SUCCESS(f"Layout en {root}"))
        self.stdout.write(
            "Política: archivos sin YYMM/tipo claro → mover a "
            "data/pgc/otros/, data/pgo/otros/ o data/otros/ (nunca borrar)."
        )
        self.stdout.write(f"Meses creados: {', '.join(f'{year}-{m:02d}' for m in months)}")

    def _parse_months(self, raw: str) -> list[int]:
        raw = raw.strip()
        if "-" in raw and "," not in raw:
            a, b = raw.split("-", 1)
            return list(range(int(a), int(b) + 1))
        out: list[int] = []
        for part in raw.split(","):
            part = part.strip()
            if part:
                out.append(int(part))
        return sorted(set(out))