"""Despacho unificado de importaciones WCG (CRM / PGO / Risk / PGC)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile
from django.core.management import call_command

from imports.detection import (
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


def _batch_summary(batch) -> str:
    if batch is None:
        return ""
    if hasattr(batch, "creados"):
        return (
            f"{batch.creados} creados, {batch.actualizados} actualizados, "
            f"{batch.errores} errores (filas {getattr(batch, 'filas_leidas', '?')})"
        )
    return str(batch)


def run_import(user, uploaded_file: UploadedFile, tipo_forzado: str | None = None) -> DispatchResult:
    detection = detect_file(uploaded_file)
    uploaded_file.seek(0)
    tipo = tipo_forzado or detection.tipo

    if tipo == TYPE_UNKNOWN or not tipo:
        return DispatchResult(
            tipo=TYPE_UNKNOWN,
            label=TYPE_LABELS[TYPE_UNKNOWN],
            detection=detection,
            message="No se pudo identificar el tipo. Elija una opción sugerida.",
            ok=False,
        )

    label = TYPE_LABELS.get(tipo, tipo)

    if tipo == TYPE_CRM_CLIENTES:
        from crm import services as crm_services

        batch = crm_services.import_entidades(user, uploaded_file)
        return DispatchResult(
            tipo=tipo,
            label=label,
            detection=detection,
            batch=batch,
            message=f"CRM: {_batch_summary(batch)}",
            ok=batch.status in ("OK", "PARTIAL"),
            redirect_hint="crm:entidad_list",
        )

    if tipo == TYPE_PGO_TICKETS:
        from pgo import services as pgo_services
        from pgo.periodo import recalculate_pgo_periodos

        batch = pgo_services.import_tickets(user, uploaded_file)
        recalculate_pgo_periodos()
        return DispatchResult(
            tipo=tipo,
            label=label,
            detection=detection,
            batch=batch,
            message=f"PGO tickets: {_batch_summary(batch)}",
            ok=batch.status in ("OK", "PARTIAL"),
            redirect_hint="pgo:dashboard",
        )

    if tipo == TYPE_PGO_CATALOGO:
        from pgo import services as pgo_services

        batch = pgo_services.import_archivos_catalogo(user, uploaded_file)
        return DispatchResult(
            tipo=tipo,
            label=label,
            detection=detection,
            batch=batch,
            message=f"Catálogo PGO registrado ({batch.filas_leidas} filas).",
            ok=True,
            redirect_hint="pgo:dashboard",
        )

    if tipo == TYPE_RISK_LEASING:
        from risk import services as risk_services

        batch = risk_services.import_leasing_database(user, uploaded_file)
        return DispatchResult(
            tipo=tipo,
            label=label,
            detection=detection,
            batch=batch,
            message=f"Balón leasing: {_batch_summary(batch)}",
            ok=batch.status in ("OK", "PARTIAL"),
            redirect_hint="risk:comando_balon",
        )

    if tipo == TYPE_RISK_RENTAS:
        from risk import services as risk_services

        batch = risk_services.import_leasing_rentas(user, uploaded_file)
        return DispatchResult(
            tipo=tipo,
            label=label,
            detection=detection,
            batch=batch,
            message=f"Rentas leasing: {_batch_summary(batch)}",
            ok=batch.status in ("OK", "PARTIAL"),
            redirect_hint="risk:comando_balon",
        )

    if tipo in (TYPE_NEW_CLIENTS, TYPE_CROSS_SALE, TYPE_FINANCIAL):
        # Persistir temporalmente y usar comandos PGC existentes
        from imports.models import FileUpload, guess_file_format

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
        )
        tmp.stored_file.save(uploaded_file.name, uploaded_file, save=True)
        path = Path(tmp.stored_file.path)
        try:
            if tipo == TYPE_NEW_CLIENTS:
                call_command("import_clientes_nuevos", path=str(path), file_upload_id=tmp.id)
            elif tipo == TYPE_CROSS_SALE:
                call_command("import_venta_cruzada", path=str(path))
            else:
                # FINANCIAL requiere year/month — dejar parseado pero avisar
                tmp.status = FileUpload.STATUS_UPLOADED
                tmp.parsing_notes = "Subido vía Importación General. Procesar en Admin PGC mensual."
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
                )
            tmp.status = FileUpload.STATUS_PARSED_OK
            tmp.save(update_fields=["status"])
            return DispatchResult(
                tipo=tipo,
                label=label,
                detection=detection,
                batch=tmp,
                message=f"{label}: procesado correctamente.",
                ok=True,
                redirect_hint="pgc:admin_monthly" if tipo != TYPE_NEW_CLIENTS else "pgc:clientes_nuevos",
            )
        except Exception as exc:
            tmp.status = FileUpload.STATUS_PARSED_ERROR
            tmp.error_summary = str(exc)[:500]
            tmp.save(update_fields=["status", "error_summary"])
            return DispatchResult(
                tipo=tipo,
                label=label,
                detection=detection,
                batch=tmp,
                message=f"Error al procesar: {exc}",
                ok=False,
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
