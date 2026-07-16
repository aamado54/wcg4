"""
Vistas del área de Administración rediseñada.
"""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.management import call_command
from django.shortcuts import redirect, render
from django.urls import reverse

logger = logging.getLogger("pgc.admin_ingresos")

from imports.forms import FileUploadForm
from imports.models import FileUpload, guess_file_type_and_period

from .admin_manual import (
    get_manual_edit_context,
    save_alias,
    save_aliases_bulk,
    save_fx,
    save_import_rows,
    save_period_note,
    save_requirements,
    save_results,
    save_targets,
)
from .income_conversion import recalc_stale_ingresos
from .admin_period import (
    BLOCK_CROSS_SALE,
    BLOCK_FINANCIAL,
    BLOCK_META,
    BLOCK_NEW_CLIENTS,
    BLOCK_ORDER,
    BLOCK_REVIEW,
    discard_pending_upload,
    get_admin_period_snapshot,
    list_period_log,
    recalculate_block,
    recalculate_period,
    remove_duplicate_new_client_rows,
)
from .admin_new_clients_browse import (
    browse_context,
    save_browse_rows,
    save_une_reassignments,
)
from .admin_ingresos_year import get_ingresos_year_context, save_ingresos_year
from .admin_recalc import run_smart_recalc_all
from .admin_utils import (
    admin_period_context,
    parse_admin_period,
    parse_period,
    redirect_admin_ingresos_year,
    redirect_admin_manual,
    redirect_admin_monthly,
    redirect_admin_new_clients_browse,
    redirect_admin_new_clients_une,
)


def _save_upload(request, year: int, month: int, expected_type: str | None = None) -> FileUpload | None:
    uploaded = request.FILES.get("stored_file")
    if not uploaded:
        messages.error(request, "Debe seleccionar un archivo.")
        return None

    hasher = hashlib.sha256()
    for chunk in uploaded.chunks():
        hasher.update(chunk)
    uploaded_sha256 = hasher.hexdigest()
    uploaded.seek(0)

    original_filename = uploaded.name
    file_type, detected_year, detected_month = guess_file_type_and_period(original_filename)

    if expected_type and file_type != expected_type:
        messages.warning(
            request,
            f"El archivo parece ser de tipo distinto al bloque ({file_type} vs {expected_type}).",
        )

    if detected_year and detected_month and (detected_year != year or detected_month != month):
        messages.warning(
            request,
            f"El archivo sugiere período {detected_year}-{detected_month:02d}, "
            f"pero trabaja en {year}-{month:02d}.",
        )

    obj = FileUpload(
        uploaded_by=request.user,
        stored_file=uploaded,
        original_filename=original_filename,
        mime_type=getattr(uploaded, "content_type", "") or "",
        sha256=uploaded_sha256,
        detected_year=detected_year or year,
        detected_month=detected_month or month,
        file_type_detected=file_type if file_type != FileUpload.TYPE_UNKNOWN else (expected_type or file_type),
    )
    obj.save()
    messages.success(request, f"Archivo recibido: {obj.original_filename}.")
    return obj


def _process_upload(request, upload: FileUpload, year: int, month: int, block: str) -> None:
    path = Path(upload.stored_file.path)
    if not path.exists():
        messages.error(request, "El archivo físico no existe en el servidor.")
        return

    try:
        if block == BLOCK_NEW_CLIENTS:
            if upload.status == FileUpload.STATUS_PARSED_OK:
                messages.warning(
                    request,
                    "Este archivo ya fue procesado. Para evitar duplicados no se importó de nuevo. "
                    "Si necesita reprocesar, suba el archivo otra vez.",
                )
                return
            call_command(
                "import_clientes_nuevos",
                path=str(path),
                file_upload_id=upload.id,
            )
            upload.status = FileUpload.STATUS_PARSED_OK
            upload.save(update_fields=["status"])
            messages.success(request, "Clientes nuevos procesados correctamente.")
        elif block == BLOCK_CROSS_SALE:
            if upload.status == FileUpload.STATUS_PARSED_OK:
                messages.warning(
                    request,
                    "Este archivo ya fue procesado. Para evitar duplicados no se importó de nuevo. "
                    "Si necesita reprocesar, suba el archivo otra vez.",
                )
                return
            call_command("import_venta_cruzada", path=str(path))
            upload.status = FileUpload.STATUS_PARSED_OK
            upload.save(update_fields=["status"])
            messages.success(request, "Venta cruzada procesada correctamente.")
        elif block == BLOCK_FINANCIAL:
            call_command("import_ingresos", path=str(path), year=year, month=month)
            upload.status = FileUpload.STATUS_PARSED_OK
            upload.save(update_fields=["status"])
            messages.success(request, "Estado de resultados importado correctamente.")
        else:
            messages.error(request, "Este bloque no admite procesamiento de archivo.")
    except Exception as exc:
        upload.status = FileUpload.STATUS_PARSED_ERROR
        upload.error_summary = str(exc)[:500]
        upload.save(update_fields=["status", "error_summary"])
        messages.error(request, f"Error al procesar: {exc}")


def _admin_period_context(year: int, month: int) -> dict:
    # Compat legacy; prefer admin_period_context(period).
    from .admin_utils import AdminPeriod

    return admin_period_context(AdminPeriod(year=year, month_from=month, month_to=month))


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_smart_recalc(request):
    """Botón único: recalcula en orden todo lo pendiente (todos los períodos)."""
    period = parse_admin_period(request)
    next_url = (request.POST.get("next") or "").strip()

    if request.method != "POST":
        return redirect_admin_monthly(period=period)

    try:
        result = run_smart_recalc_all(user=request.user, force_all=False)
        if not result["ran"]:
            messages.info(request, result["messages"][0] if result["messages"] else "Nada pendiente.")
        else:
            messages.success(
                request,
                f"Recálculo inteligente: {result['periods_processed']} período(s) procesado(s).",
            )
            for msg in result["messages"][:40]:
                messages.success(request, msg)
            if len(result["messages"]) > 40:
                messages.info(
                    request,
                    f"… y {len(result['messages']) - 40} mensaje(s) más.",
                )
            after = result["status_after"]
            if after["is_pending"]:
                messages.warning(
                    request,
                    f"Aún quedan {after['pending_count']} período(s) con pendientes "
                    "(p.ej. falta tipo de cambio para convertir STALE).",
                )
            else:
                messages.success(request, "Estado global: al día (verde).")
    except Exception as exc:
        messages.error(request, f"Error en recálculo inteligente: {exc}")

    if next_url.startswith("/"):
        return redirect(next_url)
    return redirect_admin_monthly(period=period)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_hub(request):
    """Punto de entrada legado: redirige al tablero mensual."""
    period = parse_admin_period(request)
    return redirect(f"{reverse('pgc:admin_monthly')}?{period.querystring()}")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_monthly(request):
    period = parse_admin_period(request)
    year, month = period.year, period.month
    selected_block = (request.GET.get("block") or request.POST.get("block") or BLOCK_ORDER[0]).strip()

    if request.method == "POST":
        action = (request.POST.get("action") or "").strip()

        if action == "recalculate_period":
            try:
                for msg in recalculate_period(year, month):
                    messages.success(request, msg)
            except Exception as exc:
                messages.error(request, f"Error al recalcular período: {exc}")
            return redirect_admin_monthly(period=period, block=selected_block)

        if action == "recalculate_block":
            block = request.POST.get("block") or selected_block
            try:
                for msg in recalculate_block(year, month, block):
                    messages.success(request, msg)
            except Exception as exc:
                messages.error(request, f"Error al recalcular bloque: {exc}")
            return redirect_admin_monthly(period=period, block=block)

        if action == "upload":
            block = request.POST.get("block") or selected_block
            type_map = {
                BLOCK_FINANCIAL: FileUpload.TYPE_FINANCIAL,
                BLOCK_NEW_CLIENTS: FileUpload.TYPE_NEW_CLIENTS,
                BLOCK_CROSS_SALE: FileUpload.TYPE_CROSS_SALE,
            }
            _save_upload(request, year, month, type_map.get(block))
            return redirect_admin_monthly(period=period, block=block)

        if action == "process":
            block = request.POST.get("block") or selected_block
            try:
                file_id = int(request.POST.get("file_id") or "0")
            except (TypeError, ValueError):
                file_id = 0
            upload = FileUpload.objects.filter(id=file_id).first()
            if not upload:
                messages.error(request, "Archivo no encontrado.")
            else:
                _process_upload(request, upload, year, month, block)
            return redirect_admin_monthly(period=period, block=block)

        if action == "discard_pending":
            block = request.POST.get("block") or selected_block
            try:
                file_id = int(request.POST.get("file_id") or "0")
            except (TypeError, ValueError):
                file_id = 0
            upload = FileUpload.objects.filter(id=file_id).first()
            if not upload:
                messages.error(request, "Archivo no encontrado.")
            else:
                try:
                    result = discard_pending_upload(upload)
                    messages.success(
                        request,
                        f"Se quitó de la cola: {result['filename']}. "
                        "Los datos ya procesados no se modificaron.",
                    )
                except ValueError as exc:
                    messages.error(request, str(exc))
                except Exception as exc:
                    messages.error(request, f"No se pudo quitar el archivo de la cola: {exc}")
            return redirect_admin_monthly(period=period, block=block)

        if action == "dedup_new_clients":
            try:
                result = remove_duplicate_new_client_rows(year, month, user=request.user)
                if result["removed"]:
                    messages.success(
                        request,
                        f"Se eliminaron {result['removed']} registro(s) duplicado(s) "
                        f"y se actualizaron {result['metrics_updated']} métrica(s) de clientes nuevos.",
                    )
                else:
                    messages.info(request, "No se encontraron duplicados en el detalle de clientes.")
            except Exception as exc:
                messages.error(request, f"Error al eliminar duplicados: {exc}")
            return redirect_admin_monthly(period=period, block=BLOCK_NEW_CLIENTS)

    snapshot = get_admin_period_snapshot(year, month)
    if selected_block not in snapshot["blocks_by_id"]:
        selected_block = BLOCK_ORDER[0]

    context = {
        **admin_period_context(period),
        "snapshot": snapshot,
        "selected_block": selected_block,
        "block_detail": snapshot["blocks_by_id"][selected_block],
        "block_order": BLOCK_ORDER,
        "block_meta": BLOCK_META,
        "upload_form": FileUploadForm(),
        "recent_log": list_period_log(year, month, limit=8, month_from=period.month_from),
        "supports_month_range": False,
        "single_month_ops": True,
    }
    return render(request, "pgc/admin_monthly.html", context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_manual_edit(request):
    period = parse_admin_period(request)
    year, month = period.year, period.month
    tab = (request.GET.get("tab") or request.POST.get("tab") or "targets").strip()

    if request.method == "POST":
        action = (request.POST.get("action") or "").strip()
        reason = (request.POST.get("reason") or "").strip()
        recalc_after = request.POST.get("recalc_after") == "1"

        try:
            changes = 0
            if action == "save_targets":
                changes = save_targets(request.user, year, month, request.POST, reason)
            elif action == "save_results":
                changes = save_results(request.user, year, month, request.POST, reason)
            elif action == "recalc_stale_ingresos":
                result = recalc_stale_ingresos(
                    year=year,
                    month=month,
                    user=request.user,
                    reason=reason or "Recálculo de ingresos STALE desde admin",
                )
                changes = result["updated"]
                if changes:
                    messages.success(
                        request,
                        f"Se recalcularon {changes} ingreso(s) con TC={result['fx']}.",
                    )
                    if recalc_after:
                        try:
                            for msg in recalculate_period(year, month):
                                messages.success(request, msg)
                        except Exception as exc:
                            messages.warning(
                                request,
                                f"Recálculo de ingresos listo, pero falló el score: {exc}",
                            )
                    return redirect_admin_manual(period=period, tab=tab)
                messages.info(request, "No hay ingresos STALE para recalcular.")
                return redirect_admin_manual(period=period, tab=tab)
            elif action == "save_requirements":
                changes = save_requirements(request.user, year, month, request.POST, reason)
            elif action == "save_fx":
                changes = save_fx(
                    request.user,
                    year,
                    month,
                    request.POST,
                    reason,
                    month_from=period.month_from,
                )
            elif action == "save_alias":
                changes = save_alias(request.user, year, month, request.POST, reason)
            elif action == "save_aliases_bulk":
                changes = save_aliases_bulk(request.user, year, month, request.POST, reason)
            elif action == "save_imports":
                changes = save_import_rows(
                    request.user,
                    year,
                    month,
                    request.POST,
                    reason,
                    month_from=period.month_from,
                )
            elif action == "save_notes":
                changes = save_period_note(request.user, year, month, request.POST, reason)
            else:
                messages.error(request, "Acción no reconocida.")
                return redirect_admin_manual(period=period, tab=tab)

            if changes:
                messages.success(request, f"Se guardaron {changes} cambio(s).")
                if recalc_after:
                    try:
                        for msg in recalculate_period(year, month):
                            messages.success(request, msg)
                    except Exception as exc:
                        messages.warning(request, f"Cambios guardados, pero falló el recálculo: {exc}")
            else:
                messages.info(request, "No hubo cambios que guardar.")
        except ValueError as exc:
            messages.error(request, str(exc))
        except Exception as exc:
            messages.error(request, f"Error al guardar: {exc}")

        return redirect_admin_manual(period=period, tab=tab)

    context = {
        **admin_period_context(period),
        **get_manual_edit_context(year, month, tab, month_from=period.month_from),
    }
    return render(request, "pgc/admin_manual_edit.html", context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_ingresos_year(request):
    """Matriz anual: 12 meses × 4 UNEs + TC (captura de ingresos reales)."""
    period = parse_admin_period(request)
    year = period.year
    capture_currency = (request.GET.get("curr") or request.POST.get("capture_currency") or "GTQ").strip()

    if request.method == "POST":
        action = (request.POST.get("action") or "").strip()
        reason = (request.POST.get("reason") or "").strip()
        recalc_after = request.POST.get("recalc_after") == "1"
        capture_currency = (request.POST.get("capture_currency") or capture_currency).strip()

        if action == "save_ingresos_year":
            ing_keys = sorted(k for k in request.POST if k.startswith("ing_"))
            fx_keys = sorted(k for k in request.POST if k.startswith("fx_"))
            logger.warning(
                "ingresos_year POST year=%s curr=%s reason_len=%s "
                "ing_nonempty=%s fx_nonempty=%s ing_sample=%s fx_sample=%s",
                year,
                capture_currency,
                len(reason),
                sum(1 for k in ing_keys if (request.POST.get(k) or "").strip()),
                sum(1 for k in fx_keys if (request.POST.get(k) or "").strip()),
                [(k, request.POST.get(k)) for k in ing_keys if (request.POST.get(k) or "").strip()][:8],
                [(k, request.POST.get(k)) for k in fx_keys if (request.POST.get(k) or "").strip()][:8],
            )
            try:
                result = save_ingresos_year(request.user, year, request.POST, reason)
                income_n = result["income_changes"]
                fx_n = result["fx_changes"]
                logger.warning(
                    "ingresos_year result year=%s income_changes=%s fx_changes=%s currency=%s",
                    year,
                    income_n,
                    fx_n,
                    result["currency"],
                )
                if income_n:
                    messages.success(
                        request,
                        f"Guardado: {income_n} ingreso(s), {fx_n} TC; "
                        f"moneda captura={result['currency']}.",
                    )
                    if recalc_after:
                        # Recalcula score del mes foco del selector (no los 12).
                        try:
                            for msg in recalculate_period(year, period.month):
                                messages.success(request, msg)
                        except Exception as exc:
                            messages.warning(
                                request,
                                f"Ingresos guardados, pero falló el score de "
                                f"{year}-{period.month:02d}: {exc}",
                            )
                elif fx_n:
                    messages.warning(
                        request,
                        f"Solo se guardaron {fx_n} tipo(s) de cambio. "
                        "No llegó ningún valor de ingreso en el POST "
                        "(celdas vacías o no enviadas). Complete ingresos y vuelva a Guardar.",
                    )
                else:
                    messages.warning(
                        request,
                        "Sin cambios: no se recibieron ingresos ni tipos de cambio "
                        "con valor nuevo. Revise el formulario y el motivo, luego reintente.",
                    )
            except Exception as exc:
                logger.warning("ingresos_year save failed year=%s err=%s", year, exc)
                messages.error(request, str(exc))
            return redirect_admin_ingresos_year(
                period=period, curr=capture_currency
            )

    context = {
        **admin_period_context(period),
        **get_ingresos_year_context(year, capture_currency=capture_currency),
        "supports_month_range": False,
        "single_month_ops": False,
    }
    return render(request, "pgc/admin_ingresos_year.html", context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_monthly_log(request):
    period = parse_admin_period(request)
    year, month = period.year, period.month
    entries = list_period_log(year, month, limit=150, month_from=period.month_from)
    snapshot = get_admin_period_snapshot(year, month)

    context = {
        **admin_period_context(period),
        "period_label": period.label,
        "entries": entries,
        "snapshot": snapshot,
        "supports_month_range": True,
        "single_month_ops": False,
    }
    return render(request, "pgc/admin_monthly_log.html", context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_new_clients_browse(request):
    period = parse_admin_period(request)

    if request.method == "POST":
        reason = (request.POST.get("reason") or "").strip()
        recalc_after = request.POST.get("recalc_after") == "1"
        try:
            result = save_browse_rows(request.user, period, request.POST, reason)
            if result["total"]:
                parts = []
                if result["updated"]:
                    parts.append(f"{result['updated']} editado(s)")
                if result["deleted"]:
                    parts.append(f"{result['deleted']} eliminado(s)")
                if result["created"]:
                    parts.append(f"{result['created']} creado(s)")
                messages.success(
                    request,
                    f"Guardado: {', '.join(parts)}. "
                    f"Métricas actualizadas: {result['metrics_updated']}.",
                )
                if recalc_after:
                    try:
                        for msg in recalculate_block(
                            period.year, period.month, BLOCK_NEW_CLIENTS
                        ):
                            messages.success(request, msg)
                    except Exception as exc:
                        messages.warning(
                            request,
                            f"Cambios guardados, pero falló el recálculo: {exc}",
                        )
            else:
                messages.info(request, "No hubo cambios que guardar.")
        except ValueError as exc:
            messages.error(request, str(exc))
        except Exception as exc:
            messages.error(request, f"Error al guardar: {exc}")
        return redirect_admin_new_clients_browse(period=period)

    context = {
        **admin_period_context(period),
        **browse_context(period),
        "adm_nav_active": "clients_browse",
    }
    return render(request, "pgc/admin_new_clients_browse.html", context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_new_clients_une(request):
    period = parse_admin_period(request)

    if request.method == "POST":
        reason = (request.POST.get("reason") or "").strip()
        recalc_after = request.POST.get("recalc_after") == "1"
        try:
            result = save_une_reassignments(
                request.user, period, request.POST, reason
            )
            if result["changed"]:
                messages.success(
                    request,
                    f"Se reasignaron {result['changed']} registro(s). "
                    f"Métricas actualizadas: {result['metrics_updated']}.",
                )
                if recalc_after:
                    try:
                        for msg in recalculate_block(
                            period.year, period.month, BLOCK_NEW_CLIENTS
                        ):
                            messages.success(request, msg)
                    except Exception as exc:
                        messages.warning(
                            request,
                            f"Cambios guardados, pero falló el recálculo: {exc}",
                        )
            else:
                messages.info(request, "No hubo cambios de UNE.")
        except ValueError as exc:
            messages.error(request, str(exc))
        except Exception as exc:
            messages.error(request, f"Error al guardar: {exc}")
        return redirect_admin_new_clients_une(period=period)

    context = {
        **admin_period_context(period),
        **browse_context(period),
        "adm_nav_active": "clients_une",
    }
    return render(request, "pgc/admin_new_clients_une.html", context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def legacy_run_recalc_pgc(request):
    """Compatibilidad con URLs/formularios antiguos de recálculo."""
    year, month = parse_period(request)
    if request.method != "POST":
        messages.error(request, "Método no permitido.")
        return redirect_admin_monthly(year, month, BLOCK_REVIEW)

    year_raw = (request.POST.get("year") or "").strip()
    month_raw = (request.POST.get("month") or "").strip()
    try:
        year = int(year_raw)
        month = int(month_raw)
        if month < 1 or month > 12:
            raise ValueError
    except (TypeError, ValueError):
        messages.error(request, "Debes indicar año y mes válidos.")
        return redirect_admin_monthly(year, month, BLOCK_REVIEW)

    try:
        for msg in recalculate_period(year, month):
            messages.success(request, msg)
    except Exception as exc:
        messages.error(request, f"Error al ejecutar recalc PGC: {exc}")

    return redirect_admin_monthly(year, month, BLOCK_REVIEW)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def legacy_run_recalc_investment(request):
    """Compatibilidad con URLs/formularios antiguos de recálculo Investment."""
    year, month = parse_period(request)
    if request.method != "POST":
        messages.error(request, "Método no permitido.")
        return redirect_admin_monthly(year, month, BLOCK_NEW_CLIENTS)

    year_raw = (request.POST.get("year") or "").strip()
    month_raw = (request.POST.get("month") or "").strip()
    try:
        year = int(year_raw)
        month = int(month_raw)
        if month < 1 or month > 12:
            raise ValueError
    except (TypeError, ValueError):
        messages.error(request, "Debes indicar año y mes válidos.")
        return redirect_admin_monthly(year, month, BLOCK_NEW_CLIENTS)

    try:
        for msg in recalculate_block(year, month, BLOCK_NEW_CLIENTS):
            messages.success(request, msg)
    except Exception as exc:
        messages.error(request, f"Error al ejecutar recalc Investment: {exc}")

    return redirect_admin_monthly(year, month, BLOCK_NEW_CLIENTS)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def redirect_manual_results(request):
    """Legacy URL: /admin-hub/ingresos-manual-capture → matriz anual de ingresos."""
    period = parse_admin_period(request)
    return redirect_admin_ingresos_year(period=period)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def redirect_manual_fx(request):
    year, month = parse_period(request)
    return redirect_admin_manual(year, month, "fx")
