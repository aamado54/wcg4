"""
Charts TV: archivo archivados con sello + copias vivas wcg-g1..g4.png|.svg.

Layout en disco (MEDIA_ROOT/tv):
  media/tv/archive/wcg-g1 YY-MM HH-MM.png
  media/tv/archive/wcg-g1 YY-MM HH-MM.svg
  media/tv/live/wcg-g1.png … wcg-g4.png
  media/tv/live/wcg-g1.svg … wcg-g4.svg

URL pública (televisor / capturador):
  /tv/wcg-g1.png … /tv/wcg-g4.png
  /tv/wcg-g1.svg … /tv/wcg-g4.svg
"""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from core.access import can_access_ops
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from pgc.admin_utils import admin_period_context, parse_admin_period

LIVE_SLOT_COUNT = 4
LIVE_EXTS = ("png", "svg")
LIVE_NAMES = {
    ext: {n: f"wcg-g{n}.{ext}" for n in range(1, LIVE_SLOT_COUNT + 1)}
    for ext in LIVE_EXTS
}
# Soporta sello nuevo YY-MM-DD HH-MM y legado YY-MM HH-MM; PNG o SVG.
ARCHIVE_NAME_RE = re.compile(
    r"^wcg-g([1-4]) (\d{2}-\d{2}(?:-\d{2})? \d{2}-\d{2})\.(png|svg)$"
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


def live_path(slot: int, ext: str = "png") -> Path:
    if ext not in LIVE_NAMES:
        raise ValueError(f"ext inválida: {ext}")
    if slot not in LIVE_NAMES[ext]:
        raise ValueError(f"slot inválido: {slot}")
    return live_dir() / LIVE_NAMES[ext][slot]


def parse_archive_name(name: str) -> tuple[int, str, str] | None:
    match = ARCHIVE_NAME_RE.match(name)
    if not match:
        return None
    return int(match.group(1)), match.group(2), match.group(3)


def is_safe_archive_name(name: str) -> bool:
    return parse_archive_name(name) is not None


def sibling_archive_name(name: str, new_ext: str) -> str | None:
    parsed = parse_archive_name(name)
    if not parsed or new_ext not in LIVE_EXTS:
        return None
    slot, stamp, _ext = parsed
    return f"wcg-g{slot} {stamp}.{new_ext}"


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
    """Lista solo PNG: agrupan los sets de selección TV (SVG viaja como hermano)."""
    items: list[ArchiveFile] = []
    for path in sorted(archive_dir().glob("wcg-g*.png"), key=lambda p: p.stat().st_mtime, reverse=True):
        parsed = parse_archive_name(path.name)
        if not parsed:
            continue
        slot, stamp, _ext = parsed
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
    for slot in range(1, LIVE_SLOT_COUNT + 1):
        variants = []
        for ext in LIVE_EXTS:
            name = LIVE_NAMES[ext][slot]
            path = live_path(slot, ext)
            variants.append(
                {
                    "ext": ext,
                    "name": name,
                    "exists": path.is_file(),
                    "size": path.stat().st_size if path.is_file() else 0,
                    "url": f"/tv/{name}",
                }
            )
        rows.append(
            {
                "slot": slot,
                "name": LIVE_NAMES["png"][slot],
                "variants": variants,
                "exists": any(v["exists"] for v in variants),
                "png": variants[0],
                "svg": variants[1],
            }
        )
    return rows


def save_archive_upload(filename: str, raw: bytes, *, activate_live: bool = True) -> dict:
    """
    Guarda PNG o SVG con sello en archive/.
    Si activate_live=True, también actualiza media/tv/live/wcg-gN.{png|svg}.
    """
    parsed = parse_archive_name(filename)
    if not parsed:
        raise ValueError(
            "Nombre inválido. Use: wcg-gN YY-MM HH-MM.png|.svg "
            "(N=1..4; también acepta YY-MM-DD)."
        )
    slot, stamp, ext = parsed
    dest = archive_dir() / filename
    dest.write_bytes(raw)
    live_name = None
    if activate_live:
        live_dest = live_path(slot, ext)
        live_dest.write_bytes(raw)
        live_name = LIVE_NAMES[ext][slot]
    return {
        "filename": filename,
        "slot": slot,
        "stamp": stamp,
        "ext": ext,
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
    """
    Copia PNG de archive → live (sobrescribe).
    Si existe el SVG hermano del mismo sello, también lo copia a live/wcg-gN.svg.
    """
    copied: list[str] = []
    seen_slots: set[int] = set()
    for name in filenames:
        parsed = parse_archive_name(name)
        if not parsed:
            raise ValueError(f"Nombre no permitido: {name}")
        slot, _stamp, ext = parsed
        if ext != "png":
            raise ValueError(
                f"Seleccione PNG para activar en TV (inválido: {name})."
            )
        src = archive_dir() / name
        if not src.is_file():
            raise FileNotFoundError(f"No existe en archivo: {name}")
        if slot in seen_slots:
            raise ValueError(f"Seleccionó más de un archivo para wcg-g{slot}.")
        seen_slots.add(slot)
        dest = live_path(slot, "png")
        shutil.copy2(src, dest)
        copied.append(LIVE_NAMES["png"][slot])

        svg_name = sibling_archive_name(name, "svg")
        if svg_name:
            svg_src = archive_dir() / svg_name
            if svg_src.is_file():
                shutil.copy2(svg_src, live_path(slot, "svg"))
                copied.append(LIVE_NAMES["svg"][slot])
    return copied


def delete_archives(filenames: list[str]) -> list[str]:
    """Borra los nombres dados; si es PNG, también borra el SVG hermano del mismo sello."""
    deleted: list[str] = []
    to_delete: list[str] = []
    for name in filenames:
        if not is_safe_archive_name(name):
            raise ValueError(f"Nombre no permitido: {name}")
        to_delete.append(name)
        sib = sibling_archive_name(name, "svg")
        if sib and sib not in to_delete:
            to_delete.append(sib)
    for name in to_delete:
        path = archive_dir() / name
        if path.is_file():
            path.unlink()
            deleted.append(name)
    return deleted


def _ops_user(user) -> bool:
    return can_access_ops(user)


@require_GET
def tv_live_png(request, name: str):
    """Sirve wcg-g1.png|.svg … wcg-g4.png|.svg sin autenticación (TV / capturador)."""
    allowed = {
        LIVE_NAMES[ext][n] for ext in LIVE_EXTS for n in range(1, LIVE_SLOT_COUNT + 1)
    }
    if name not in allowed:
        raise Http404("Archivo TV no encontrado.")
    path = live_dir() / name
    if not path.is_file():
        raise Http404("Aún no hay chart vivo para ese slot/formato.")
    content_type = "image/svg+xml" if name.endswith(".svg") else "image/png"
    response = FileResponse(path.open("rb"), content_type=content_type)
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Pragma"] = "no-cache"
    return response


@login_required
@user_passes_test(_ops_user)
@require_GET
def tv_archive_png(request, name: str):
    if not is_safe_archive_name(name):
        raise Http404("Nombre inválido.")
    path = archive_dir() / name
    if not path.is_file():
        raise Http404("Archivo no encontrado.")
    parsed = parse_archive_name(name)
    content_type = "image/svg+xml" if parsed and parsed[2] == "svg" else "image/png"
    return FileResponse(path.open("rb"), content_type=content_type)


@login_required
@require_POST
def tv_charts_upload(request):
    """Recibe PNG/SVG desde Exportación 4 charts → archive/ (+ live/ si activate)."""
    uploaded = request.FILES.get("file") or request.FILES.get("png")
    if not uploaded:
        return JsonResponse({"ok": False, "error": "Falta archivo."}, status=400)
    filename = (uploaded.name or "").strip()
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
@user_passes_test(_ops_user)
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
                            f"Borrados {len(deleted)} archivo(s) archivado(s) "
                            f"(PNG y SVG hermano si existía).",
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
            svg_name = sibling_archive_name(f.name, "svg") if f else None
            svg_exists = bool(svg_name and (archive_dir() / svg_name).is_file())
            slots.append(
                {
                    "slot": n,
                    "file": f,
                    "name": f.name if f else None,
                    "svg_name": svg_name if svg_exists else None,
                    "svg_exists": svg_exists,
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

    live_slots = live_status()
    context = {
        **admin_period_context(period),
        "live_slots": live_slots,
        "live_all_empty": not any(s["exists"] for s in live_slots),
        "archive_sets": archive_sets,
        "supports_month_range": False,
    }
    return render(request, "pgc/admin_tv_charts.html", context)
