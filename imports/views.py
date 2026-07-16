# imports/views.py

from pathlib import Path

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.management import call_command
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from pgc.admin_utils import parse_period

from .models import FileUpload


def _redirect_imports_to_admin(request, block: str | None = None):
    year, month = parse_period(request)
    url = f"{reverse('pgc:admin_monthly')}?year={year}&month={month}"
    if block:
        url += f"&block={block}"
    return redirect(url)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def import_hub(request):
    """Flujo legado: redirige al tablero mensual de Administración."""
    return _redirect_imports_to_admin(request)


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
