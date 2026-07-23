"""Despacho unificado de importaciones WCG (CRM / PGO / Risk / PGC)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile
from django.core.management import call_command

from imports.detection import (
    IMPORTER_LABELS,
    TYPE_CRM_CLIENTES,
    TYPE_CROSS_SALE,
    TYPE_FINANCIAL,
    TYPE_LABELS,
    TYPE_NEW_CLIENTS,
    TYPE_PGO_CATALOGO,
    TYPE_PGO_TICKETS,
    TYPE_RISK_LEASING,
    TYPE_RISK_RENTAS,
    TYPE_UNKNOWN,
    DetectionResult,
    detect_file,
)


@dataclass
class DispatchResult:
    tipo: str
    label: str
    detection: DetectionResult
    batch: object | None = None
    message: str = ""
    ok: bool = False
    redirect_hint: str = ""
    needs_manual: bool = False
    forced: bool = False
    warnings: list[str] | None = None
    duplicate_extra: int = 0


def _batch_summary(batch) -> str:
    if batch is None:
        return ""
    if hasattr(batch, "creados"):
        return (
            f"{batch.creados} creados, {batch.actualizados} actualizados, "
            f"{batch.errores} errores (filas {getattr(batch, 'filas_leidas', '?')})"
        )
    return str(batch)


def _collect_upload_warnings(upload) -> list[str]:
    warnings: list[str] = []
    if upload is None:
        return warnings
    notes = (getattr(upload, "parsing_notes", None) or "")
    for line in notes.splitlines():
        if "WARNING" in line.upper() or "interpretada como GTQ" in line or "tratadas como GTQ" in line:
            warnings.append(line.strip())
    try:
        from imports.models import FileImportLog

        for log in FileImportLog.objects.filter(
            file_upload=upload, level=FileImportLog.LEVEL_WARNING
        ).order_by("-id")[:10]:
            if log.message and log.message not in warnings:
                warnings.append(log.message)
    except Exception:
        pass
    # Also surface currency warnings from batch log_texto
    log_texto = getattr(upload, "log_texto", None) or ""
    for line in log_texto.splitlines():
        if line.startswith("WARNING") and line not in warnings:
            warnings.append(line)
    return warnings


def _duplicate_hint_for_tipo(tipo: str) -> int:
    try:
        from imports.duplicates import scan_all_duplicates

        module_map = {
            TYPE_NEW_CLIENTS: "new_clients",
            TYPE_CROSS_SALE: "cross_sale",
            TYPE_CRM_CLIENTES: "crm_entidad",
            TYPE_PGO_TICKETS: "pgo_ticket",
            TYPE_RISK_LEASING: "risk_snapshot",
            TYPE_RISK_RENTAS: "risk_snapshot",
        }
        mod = module_map.get(tipo)
        if not mod:
            return 0
        return sum(g.extra_count for g in scan_all_duplicates(module=mod))
    except Exception:
        return 0


def _detection_log(detection: DetectionResult, tipo: str, forced: bool) -> str:
    importer = IMPORTER_LABELS.get(tipo, tipo)
    mode = "forzado" if forced else ("auto" if detection.can_auto_import else "manual")
    return (
        f"[detección] {detection.rule_summary} | importador={importer} | modo={mode}"
    )


def _annotate_batch(batch, detection: DetectionResult, tipo: str, forced: bool) -> None:
    if batch is None or not hasattr(batch, "log_texto"):
        return
    header = _detection_log(detection, tipo, forced)
    existing = (batch.log_texto or "").strip()
    batch.log_texto = (header + ("\n" + existing if existing else ""))[:8000]
    batch.save(update_fields=["log_texto"])


def run_import(user, uploaded_file: UploadedFile, tipo_forzado: str | None = None) -> DispatchResult:
    detection = detect_file(uploaded_file)
    uploaded_file.seek(0)
    forced = bool(tipo_forzado)
    tipo = tipo_forzado or detection.tipo

    if not forced and (detection.ambiguous or not detection.can_auto_import or tipo == TYPE_UNKNOWN):
        return DispatchResult(
            tipo=tipo if tipo != TYPE_UNKNOWN else TYPE_UNKNOWN,
            label=TYPE_LABELS.get(tipo, TYPE_LABELS[TYPE_UNKNOWN]),
            detection=detection,
            message=(
                "Ambigüedad en la detección. Seleccione el tipo de importación "
                "manualmente y vuelva a enviar el archivo."
                if detection.ambiguous or tipo == TYPE_UNKNOWN
                else "Confianza insuficiente para importar automáticamente. Confirme el tipo."
            ),
            ok=False,
            needs_manual=True,
        )

    if tipo == TYPE_UNKNOWN or not tipo:
        return DispatchResult(
            tipo=TYPE_UNKNOWN,
            label=TYPE_LABELS[TYPE_UNKNOWN],
            detection=detection,
            message="No se pudo identificar el tipo. Elija una opción sugerida.",
            ok=False,
            needs_manual=True,
        )

    label = TYPE_LABELS.get(tipo, tipo)

    if tipo == TYPE_CRM_CLIENTES:
        from crm import services as crm_services

        batch = crm_services.import_entidades(user, uploaded_file)
        _annotate_batch(batch, detection, tipo, forced)
        dup = _duplicate_hint_for_tipo(tipo)
        msg = f"CRM: {_batch_summary(batch)}"
        if dup:
            msg += f" · {dup} posible(s) duplicado(s) para revisión."
        return DispatchResult(
            tipo=tipo,
            label=label,
            detection=detection,
            batch=batch,
            message=msg,
            ok=batch.status in ("OK", "PARTIAL"),
            redirect_hint="crm:entidad_list",
            forced=forced,
            warnings=_collect_upload_warnings(batch),
            duplicate_extra=dup,
        )

    if tipo == TYPE_PGO_TICKETS:
        from pgo import services as pgo_services
        from pgo.periodo import recalculate_pgo_periodos

        batch = pgo_services.import_tickets(user, uploaded_file)
        recalculate_pgo_periodos()
        _annotate_batch(batch, detection, tipo, forced)
        dup = _duplicate_hint_for_tipo(tipo)
        msg = f"PGO tickets: {_batch_summary(batch)}"
        if dup:
            msg += f" · {dup} posible(s) duplicado(s) para revisión."
        return DispatchResult(
            tipo=tipo,
            label=label,
            detection=detection,
            batch=batch,
            message=msg,
            ok=batch.status in ("OK", "PARTIAL"),
            redirect_hint="pgo:dashboard",
            forced=forced,
            warnings=_collect_upload_warnings(batch),
            duplicate_extra=dup,
        )

    if tipo == TYPE_PGO_CATALOGO:
        from pgo import services as pgo_services

        batch = pgo_services.import_archivos_catalogo(user, uploaded_file)
        _annotate_batch(batch, detection, tipo, forced)
        return DispatchResult(
            tipo=tipo,
            label=label,
            detection=detection,
            batch=batch,
            message=f"Catálogo PGO registrado ({batch.filas_leidas} filas).",
            ok=True,
            redirect_hint="pgo:dashboard",
            forced=forced,
        )

    if tipo == TYPE_RISK_LEASING:
        from risk import services as risk_services

        batch = risk_services.import_leasing_database(user, uploaded_file)
        _annotate_batch(batch, detection, tipo, forced)
        dup = _duplicate_hint_for_tipo(tipo)
        msg = f"Balón leasing: {_batch_summary(batch)}"
        if dup:
            msg += f" · {dup} posible(s) duplicado(s) para revisión."
        return DispatchResult(
            tipo=tipo,
            label=label,
            detection=detection,
            batch=batch,
            message=msg,
            ok=batch.status in ("OK", "PARTIAL"),
            redirect_hint="risk:comando_balon",
            forced=forced,
            warnings=_collect_upload_warnings(batch),
            duplicate_extra=dup,
        )

    if tipo == TYPE_RISK_RENTAS:
        from risk import services as risk_services

        batch = risk_services.import_leasing_rentas(user, uploaded_file)
        _annotate_batch(batch, detection, tipo, forced)
        warns = _collect_upload_warnings(batch)
        dup = _duplicate_hint_for_tipo(tipo)
        msg = f"Rentas leasing: {_batch_summary(batch)}"
        if dup:
            msg += f" · {dup} posible(s) duplicado(s) para revisión."
        return DispatchResult(
            tipo=tipo,
            label=label,
            detection=detection,
            batch=batch,
            message=msg,
            ok=batch.status in ("OK", "PARTIAL"),
            redirect_hint="risk:comando_balon",
            forced=forced,
            warnings=warns,
            duplicate_extra=dup,
        )

    if tipo in (TYPE_NEW_CLIENTS, TYPE_CROSS_SALE, TYPE_FINANCIAL):
        from imports.models import FileImportLog, FileUpload, guess_file_format

        tmp = FileUpload(
            uploaded_by=user,
            original_filename=uploaded_file.name,
            file_format=guess_file_format(uploaded_file.name),
            file_type_detected={
                TYPE_NEW_CLIENTS: FileUpload.TYPE_NEW_CLIENTS,
                TYPE_CROSS_SALE: FileUpload.TYPE_CROSS_SALE,
                TYPE_FINANCIAL: FileUpload.TYPE_FINANCIAL,
            }[tipo],
            status=FileUpload.STATUS_UPLOADED,
            parsing_notes=_detection_log(detection, tipo, forced),
        )
        tmp.stored_file.save(uploaded_file.name, uploaded_file, save=True)
        FileImportLog.objects.create(
            file_upload=tmp,
            step_code="detect",
            level=FileImportLog.LEVEL_INFO,
            message=_detection_log(detection, tipo, forced),
            payload_json={
                "tipo": tipo,
                "layer": detection.layer,
                "confidence": detection.confidence,
                "reasons": detection.reasons,
                "forced": forced,
                "importer": IMPORTER_LABELS.get(tipo),
            },
        )
        path = Path(tmp.stored_file.path)
        try:
            if tipo == TYPE_NEW_CLIENTS:
                call_command("import_clientes_nuevos", path=str(path), file_upload_id=tmp.id)
            elif tipo == TYPE_CROSS_SALE:
                call_command("import_venta_cruzada", path=str(path))
            else:
                tmp.status = FileUpload.STATUS_UPLOADED
                tmp.parsing_notes = (
                    _detection_log(detection, tipo, forced)
                    + " | Subido vía Administración → Importación. "
                    "Procesar en Admin PGC mensual (requiere año/mes)."
                )
                tmp.save(update_fields=["status", "parsing_notes"])
                return DispatchResult(
                    tipo=tipo,
                    label=label,
                    detection=detection,
                    batch=tmp,
                    message=(
                        "Archivo financiero WC* guardado. "
                        "Complételo en Admin PGC → período mensual (requiere año/mes)."
                    ),
                    ok=True,
                    redirect_hint="pgc:admin_monthly",
                    forced=forced,
                )
            tmp.status = FileUpload.STATUS_PARSED_OK
            tmp.save(update_fields=["status"])
            FileImportLog.objects.create(
                file_upload=tmp,
                step_code="dispatch",
                level=FileImportLog.LEVEL_INFO,
                message=f"Procesado con {IMPORTER_LABELS.get(tipo, tipo)}",
            )
            warns = _collect_upload_warnings(tmp)
            dup = _duplicate_hint_for_tipo(tipo)
            msg = f"{label}: procesado correctamente."
            if dup:
                msg += f" · {dup} posible(s) duplicado(s) para revisión."
            return DispatchResult(
                tipo=tipo,
                label=label,
                detection=detection,
                batch=tmp,
                message=msg,
                ok=True,
                redirect_hint="pgc:admin_monthly" if tipo != TYPE_NEW_CLIENTS else "pgc:clientes_nuevos",
                forced=forced,
                warnings=warns,
                duplicate_extra=dup,
            )
        except Exception as exc:
            tmp.status = FileUpload.STATUS_PARSED_ERROR
            tmp.error_summary = str(exc)[:500]
            tmp.save(update_fields=["status", "error_summary"])
            FileImportLog.objects.create(
                file_upload=tmp,
                step_code="dispatch",
                level=FileImportLog.LEVEL_ERROR,
                message=str(exc)[:1000],
            )
            return DispatchResult(
                tipo=tipo,
                label=label,
                detection=detection,
                batch=tmp,
                message=f"Error al procesar: {exc}",
                ok=False,
                forced=forced,
            )

    return DispatchResult(
        tipo=tipo,
        label=label,
        detection=detection,
        message=f"Tipo '{tipo}' aún no tiene despacho automático.",
        ok=False,
    )


def run_import_path(user, path: str, tipo_forzado: str | None = None) -> DispatchResult:
    p = Path(path)
    f = SimpleUploadedFile(p.name, p.read_bytes())
    return run_import(user, f, tipo_forzado=tipo_forzado)
