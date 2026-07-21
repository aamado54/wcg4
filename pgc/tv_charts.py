"""
Charts TV: archivo archivados con sello + copias vivas wcg-g1..g4.png.

Layout en disco (MEDIA_ROOT/tv):
  media/tv/archive/wcg-g1 YY-MM HH-MM.png
  media/tv/live/wcg-g1.png … wcg-g4.png

URL pública (televisor):
  /tv/wcg-g1.png … /tv/wcg-g4.png
"""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from pgc.admin_utils import admin_period_context, parse_admin_period

LIVE_SLOT_COUNT = 4
LIVE_NAMES = {n: f"wcg-g{n}.png" for n in range(1, LIVE_SLOT_COUNT + 1)}
# Soporta sello nuevo YY-MM-DD HH-MM y legado YY-MM HH-MM
ARCHIVE_NAME_RE = re.compile(
    r"^wcg-g([1-4]) (\d{2}-\d{2}(?:-\d{2})? \d{2}-\d{2})\.png$"
)


def tv_root() -> Path:
    root = Path(settings.MEDIA_ROOT) / "tv"
    (root / "archive").mkdir(parents=True, exist_ok=True)
    (root / "live").mkdir(parents=True, exist_ok=True)
    return root


def archive_dir() -> Path:
    return tv_root() / "archive"


def live_dir() -> Path:
    return tv_root() / "live"


def live_path(slot: int) -> Path:
    if slot not in LIVE_NAMES:
        raise ValueError(f"slot inválido: {slot}")
    return live_dir() / LIVE_NAMES[slot]


def parse_archive_name(name: str) -> tuple[int, str] | None:
    match = ARCHIVE_NAME_RE.match(name)
    if not match:
        return None
    return int(match.group(1)), match.group(2)


def is_safe_archive_name(name: str) -> bool:
    return parse_archive_name(name) is not None


@dataclass
class ArchiveFile:
    name: str
    slot: int
    stamp: str
    size: int
    mtime: float


@dataclass
class ArchiveSet:
    stamp: str
    files: dict[int, ArchiveFile]

    @property
    def complete(self) -> bool:
        return all(n in self.files for n in range(1, LIVE_SLOT_COUNT + 1))

    @property
    def slots_present(self) -> list[int]:
        return sorted(self.files)


def list_archive_files() -> list[ArchiveFile]:
    items: list[ArchiveFile] = []
    for path in sorted(archive_dir().glob("wcg-g*.png"), key=lambda p: p.stat().st_mtime, reverse=True):
        parsed = parse_archive_name(path.name)
        if not parsed:
            continue
        slot, stamp = parsed
        st = path.stat()
        items.append(
            ArchiveFile(
                name=path.name,
                slot=slot,
                stamp=stamp,
                size=st.st_size,
                mtime=st.st_mtime,
            )
        )
    return items


def group_archive_sets(files: list[ArchiveFile] | None = None) -> list[ArchiveSet]:
    files = files if files is not None else list_archive_files()
    by_stamp: dict[str, dict[int, ArchiveFile]] = {}
    order: list[str] = []
    for item in files:
        if item.stamp not in by_stamp:
            by_stamp[item.stamp] = {}
            order.append(item.stamp)
        by_stamp[item.stamp][item.slot] = item
    return [ArchiveSet(stamp=stamp, files=by_stamp[stamp]) for stamp in order]


def live_status() -> list[dict]:
    rows = []
    for slot, name in LIVE_NAMES.items():
        path = live_path(slot)
        rows.append(
            {
                "slot": slot,
                "name": name,
                "exists": path.is_file(),
                "size": path.stat().st_size if path.is_file() else 0,
                "url": f"/tv/{name}",
            }
        )
    return rows


def save_archive_upload(filename: str, raw: bytes, *, activate_live: bool = True) -> dict:
    """
    Guarda PNG con sello en archive/.
    Si activate_live=True, también copia/actualiza media/tv/live/wcg-gN.png.
    """
    parsed = parse_archive_name(filename)
    if not parsed:
        raise ValueError(
            "Nombre inválido. Use: wcg-gN YY-MM HH-MM.png (N=1..4; también acepta YY-MM-DD)."
        )
    slot, stamp = parsed
    dest = archive_dir() / filename
    dest.write_bytes(raw)
    live_name = None
    if activate_live:
        live_dest = live_path(slot)
        live_dest.write_bytes(raw)
        live_name = LIVE_NAMES[slot]
    return {
        "filename": filename,
        "slot": slot,
        "stamp": stamp,
        "live": live_name,
    }


def promote_latest_complete_set() -> list[str] | None:
    """Si hay un set g1–g4 completo, copia el más reciente a live. None si no hay."""
    for aset in group_archive_sets():
        if aset.complete:
            names = [aset.files[n].name for n in range(1, LIVE_SLOT_COUNT + 1)]
            return copy_archives_to_live(names)
    return None


def copy_archives_to_live(filenames: list[str]) -> list[str]:
    """Copia archivos de archive → live (sobrescribe). No borra el archivo con sello."""
    copied: list[str] = []
    seen_slots: set[int] = set()
    for name in filenames:
        parsed = parse_archive_name(name)
        if not parsed:
            raise ValueError(f"Nombre no permitido: {name}")
        slot, _stamp = parsed
        src = archive_dir() / name
        if not src.is_file():
            raise FileNotFoundError(f"No existe en archivo: {name}")
        if slot in seen_slots:
            raise ValueError(f"Seleccionó más de un archivo para wcg-g{slot}.")
        seen_slots.add(slot)
        dest = live_path(slot)
        shutil.copy2(src, dest)
        copied.append(LIVE_NAMES[slot])
    return copied


def delete_archives(filenames: list[str]) -> list[str]:
    deleted: list[str] = []
    for name in filenames:
        if not is_safe_archive_name(name):
            raise ValueError(f"Nombre no permitido: {name}")
        path = archive_dir() / name
        if path.is_file():
            path.unlink()
            deleted.append(name)
    return deleted


def _superuser(user) -> bool:
    return bool(user.is_superuser)


@require_GET
def tv_live_png(request, name: str):
    """Sirve wcg-g1.png … wcg-g4.png sin autenticación (TV)."""
    if name not in LIVE_NAMES.values():
        raise Http404("Archivo TV no encontrado.")
    path = live_dir() / name
    if not path.is_file():
        raise Http404("Aún no hay chart vivo para ese slot.")
    response = FileResponse(path.open("rb"), content_type="image/png")
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Pragma"] = "no-cache"
    return response


@login_required
@user_passes_test(_superuser)
@require_GET
def tv_archive_png(request, name: str):
    if not is_safe_archive_name(name):
        raise Http404("Nombre inválido.")
    path = archive_dir() / name
    if not path.is_file():
        raise Http404("Archivo no encontrado.")
    return FileResponse(path.open("rb"), content_type="image/png")


@login_required
@require_POST
def tv_charts_upload(request):
    """Recibe PNG desde Exportación 4 charts → archive/ + live/."""
    uploaded = request.FILES.get("file") or request.FILES.get("png")
    if not uploaded:
        return JsonResponse({"ok": False, "error": "Falta archivo."}, status=400)
    filename = (uploaded.name or "").strip()
    # Algunos navegadores envían solo el basename; normalizar espacios.
    filename = Path(filename).name
    activate = (request.POST.get("activate") or "1").strip() != "0"
    try:
        result = save_archive_upload(filename, uploaded.read(), activate_live=activate)
    except ValueError as exc:
        return JsonResponse({"ok": False, "error": str(exc)}, status=400)
    except OSError as exc:
        return JsonResponse(
            {"ok": False, "error": f"No se pudo escribir en media/tv/: {exc}"},
            status=500,
        )
    return JsonResponse({"ok": True, **result})


@login_required
@user_passes_test(_superuser)
def admin_tv_charts(request):
    period = parse_admin_period(request)

    if request.method == "POST":
        action = (request.POST.get("action") or "").strip()
        selected = [n.strip() for n in request.POST.getlist("files") if n.strip()]

        if action == "promote":
            if not selected:
                messages.error(request, "Seleccione al menos un archivo con sello.")
            else:
                try:
                    copied = copy_archives_to_live(selected)
                    messages.success(
                        request,
                        "Copiado a TV (vivos): " + ", ".join(copied) + ".",
                    )
                except (ValueError, FileNotFoundError) as exc:
                    messages.error(request, str(exc))
            return redirect("pgc:admin_tv_charts")

        if action == "delete":
            if not selected:
                messages.error(request, "Seleccione archivos archivados para borrar.")
            else:
                try:
                    deleted = delete_archives(selected)
                    if deleted:
                        messages.success(
                            request,
                            f"Borrados {len(deleted)} archivo(s) archivado(s).",
                        )
                    else:
                        messages.info(request, "Nada que borrar.")
                except ValueError as exc:
                    messages.error(request, str(exc))
            return redirect("pgc:admin_tv_charts")

        if action == "promote_stamp":
            stamp = (request.POST.get("stamp") or "").strip()
            sets = {s.stamp: s for s in group_archive_sets()}
            aset = sets.get(stamp)
            if not aset or not aset.complete:
                messages.error(
                    request,
                    "Ese sello no tiene los 4 PNG (g1–g4). Seleccione un set completo.",
                )
            else:
                names = [aset.files[n].name for n in range(1, LIVE_SLOT_COUNT + 1)]
                try:
                    copied = copy_archives_to_live(names)
                    messages.success(
                        request,
                        f"Set «{stamp}» copiado a TV: " + ", ".join(copied) + ".",
                    )
                except (ValueError, FileNotFoundError) as exc:
                    messages.error(request, str(exc))
            return redirect("pgc:admin_tv_charts")

        messages.error(request, "Acción no reconocida.")
        return redirect("pgc:admin_tv_charts")

    archive_sets = []
    for aset in group_archive_sets():
        slots = []
        for n in range(1, LIVE_SLOT_COUNT + 1):
            f = aset.files.get(n)
            slots.append(
                {
                    "slot": n,
                    "file": f,
                    "name": f.name if f else None,
                    "preview_url": (
                        reverse("pgc:tv_archive_png", kwargs={"name": f.name})
                        if f
                        else None
                    ),
                }
            )
        archive_sets.append(
            {
                "stamp": aset.stamp,
                "complete": aset.complete,
                "slots": slots,
            }
        )

    context = {
        **admin_period_context(period),
        "live_slots": live_status(),
        "live_all_empty": not any(s["exists"] for s in live_status()),
        "archive_sets": archive_sets,
        "supports_month_range": False,
    }
    return render(request, "pgc/admin_tv_charts.html", context)
