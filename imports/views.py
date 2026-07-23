# imports/views.py

from pathlib import Path

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.management import call_command
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from core.wcg_models import DataImportBatch
from pgc.admin_utils import parse_period

from .detection import ALL_IMPORTABLE, TYPE_LABELS, TYPE_UNKNOWN, detect_file
from .dispatch import run_import
from .duplicates import MODULE_SCANNERS, delete_duplicate_ids, scan_all_duplicates, summarize_duplicates
from .forms import GeneralImportForm
from .models import FileUpload


def _redirect_imports_to_admin(request, block: str | None = None):
    year, month = parse_period(request)
    url = f"{reverse('pgc:admin_monthly')}?year={year}&month={month}"
    if block:
        url += f"&block={block}"
    return redirect(url)


@login_required
def import_hub(request):
    """Administración → Importación General (punto único CRM / PGO / Risk / PGC)."""
    result = None
    detection_preview = None
    form = GeneralImportForm()

    if request.method == "POST":
        action = request.POST.get("action", "import")
        form = GeneralImportForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded = form.cleaned_data["archivo"]
            tipo_forzado = form.cleaned_data.get("tipo_forzado") or None
            if action == "detect":
                detection_preview = detect_file(uploaded)
                uploaded.seek(0)
                form = GeneralImportForm(
                    initial={
                        "tipo_forzado": (
                            detection_preview.tipo
                            if detection_preview.tipo != TYPE_UNKNOWN
                            else ""
                        )
                    }
                )
                level = messages.WARNING if detection_preview.ambiguous else messages.INFO
                messages.add_message(
                    request,
                    level,
                    f"Detección: {detection_preview.label} "
                    f"({int(detection_preview.confidence * 100)}% · capa {detection_preview.layer}). "
                    f"{'Seleccione el tipo manualmente — hay ambigüedad. ' if detection_preview.ambiguous else ''}"
                    f"Vuelva a seleccionar el archivo y confirme la importación.",
                )
            else:
                result = run_import(request.user, uploaded, tipo_forzado=tipo_forzado or None)
                if result.ok:
                    messages.success(request, result.message)
                    for w in result.warnings or []:
                        messages.warning(request, w)
                    if result.duplicate_extra:
                        messages.warning(
                            request,
                            f"Se detectaron {result.duplicate_extra} registro(s) posibles "
                            f"duplicados. Revíselos en Importación → Duplicados (sin borrado automático).",
                        )
                    form = GeneralImportForm()
                elif result.needs_manual:
                    messages.warning(request, result.message)
                    for w in result.warnings or []:
                        messages.warning(request, w)
                    detection_preview = result.detection
                    form = GeneralImportForm(
                        initial={
                            "tipo_forzado": (
                                result.detection.tipo
                                if result.detection.tipo != TYPE_UNKNOWN
                                else ""
                            )
                        }
                    )
                else:
                    messages.warning(request, result.message or "Importación incompleta.")
                    for w in result.warnings or []:
                        messages.warning(request, w)
                    form = GeneralImportForm()

    batches = DataImportBatch.objects.select_related("uploaded_by").order_by("-created_at")[:25]
    uploads = FileUpload.objects.order_by("-created_at")[:15]
    try:
        dup_summary = summarize_duplicates()
    except Exception:
        dup_summary = {"__total__": 0}

    return render(
        request,
        "imports/general_hub.html",
        {
            "form": form,
            "result": result,
            "detection_preview": detection_preview,
            "batches": batches,
            "uploads": uploads,
            "type_labels": TYPE_LABELS,
            "importable_types": [(t, TYPE_LABELS[t]) for t in ALL_IMPORTABLE],
            "dup_total": dup_summary.get("__total__", 0),
            "breadcrumbs": [
                {"label": "Inicio", "url": reverse("portal:home")},
                {"label": "Administración"},
                {"label": "Importación General"},
            ],
        },
    )


@login_required
def duplicates_review(request):
    """Revisión manual de posibles duplicados (sin borrado automático)."""
    module = (request.GET.get("module") or request.POST.get("module") or "").strip() or None

    if request.method == "POST":
        action = request.POST.get("action", "")
        mod = (request.POST.get("module") or "").strip()
        if action == "delete" and mod:
            raw_ids = request.POST.getlist("ids")
            ids = []
            for raw in raw_ids:
                try:
                    ids.append(int(raw))
                except (TypeError, ValueError):
                    continue
            keep_raw = (request.POST.get("keep_id") or "").strip()
            keep_id = None
            if keep_raw:
                try:
                    keep_id = int(keep_raw)
                except (TypeError, ValueError):
                    keep_id = None
            deleted = delete_duplicate_ids(mod, ids, keep_id=keep_id)
            if deleted:
                msg = f"Eliminados {deleted} registro(s) duplicado(s) en {MODULE_SCANNERS.get(mod, (mod,))[0]}."
                if mod in ("crm_nombre", "crm_entidad") and keep_id:
                    msg += f" Detalles fusionados en #{keep_id}."
                messages.success(request, msg)
            else:
                messages.warning(request, "No se eliminó ningún registro.")
            return redirect(f"{reverse('imports:duplicates_review')}?module={mod}")

    groups = scan_all_duplicates(module=module)
    return render(
        request,
        "imports/duplicates_review.html",
        {
            "groups": groups,
            "module": module or "",
            "modules": [(k, v[0]) for k, v in MODULE_SCANNERS.items()],
            "dup_total": sum(g.extra_count for g in groups),
            "breadcrumbs": [
                {"label": "Inicio", "url": reverse("portal:home")},
                {"label": "Administración", "url": reverse("imports:import_hub")},
                {"label": "Duplicados"},
            ],
        },
    )


@login_required
@user_passes_test(lambda u: u.is_superuser)
def process_new_clients(request, file_id):
    upload = get_object_or_404(FileUpload, id=file_id)

    if request.method == "POST":
        if upload.file_type_detected != FileUpload.TYPE_NEW_CLIENTS:
            messages.error(request, "Este archivo no es de tipo Clientes nuevos.")
            return _redirect_imports_to_admin(request, "new_clients")

        if not upload.stored_file:
            messages.error(request, "El archivo no tiene fichero almacenado.")
            return _redirect_imports_to_admin(request, "new_clients")

        file_path = Path(upload.stored_file.path)
        if not file_path.exists():
            messages.error(request, f"El archivo físico no existe: {file_path}")
            return _redirect_imports_to_admin(request, "new_clients")

        try:
            call_command(
                "import_clientes_nuevos",
                path=str(file_path),
                file_upload_id=upload.id,
            )
            messages.success(
                request,
                f"Clientes nuevos procesados correctamente desde {upload.original_filename}.",
            )
            upload.status = FileUpload.STATUS_PARSED_OK
            upload.save(update_fields=["status"])
        except Exception as exc:
            messages.error(request, f"Error al procesar clientes nuevos: {exc}")
            upload.status = FileUpload.STATUS_PARSED_ERROR
            upload.error_summary = str(exc)[:500]
            upload.save(update_fields=["status", "error_summary"])

    return _redirect_imports_to_admin(request, "new_clients")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def process_cross_sale(request, file_id):
    upload = get_object_or_404(FileUpload, id=file_id)

    if request.method == "POST":
        if upload.file_type_detected != FileUpload.TYPE_CROSS_SALE:
            messages.error(request, "Este archivo no es de tipo Venta cruzada.")
            return _redirect_imports_to_admin(request, "cross_sale")

        file_path = Path(upload.stored_file.path)
        if not file_path.exists():
            messages.error(request, f"El archivo físico no existe: {file_path}")
            return _redirect_imports_to_admin(request, "cross_sale")

        try:
            call_command("import_venta_cruzada", path=str(file_path))
            messages.success(
                request,
                f"Venta cruzada procesada correctamente desde {upload.original_filename}.",
            )
            upload.status = FileUpload.STATUS_PARSED_OK
            upload.save(update_fields=["status"])
        except Exception as exc:
            messages.error(request, f"Error al procesar venta cruzada: {exc}")
            upload.status = FileUpload.STATUS_PARSED_ERROR
            upload.error_summary = str(exc)[:500]
            upload.save(update_fields=["status", "error_summary"])

    return _redirect_imports_to_admin(request, "cross_sale")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def process_station_times(request, file_id):
    upload = get_object_or_404(FileUpload, id=file_id)
    if request.method == "POST":
        messages.warning(
            request,
            "El procesamiento de tiempos de estación aún no está implementado.",
        )
    return _redirect_imports_to_admin(request)
