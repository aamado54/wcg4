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
                    form = GeneralImportForm()
                elif result.needs_manual:
                    messages.warning(request, result.message)
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
                    form = GeneralImportForm()

    batches = DataImportBatch.objects.select_related("uploaded_by").order_by("-created_at")[:25]
    uploads = FileUpload.objects.order_by("-created_at")[:15]

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
            "breadcrumbs": [
                {"label": "Inicio", "url": reverse("portal:home")},
                {"label": "Administración"},
                {"label": "Importación General"},
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
