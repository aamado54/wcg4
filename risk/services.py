"""
Importadores Risk / Balón.

Archivo referencia leasing:
  `balon datos - Ejemplo de datos Riesgo al 31-mayo para una operacion - Base de datos Leasing.xlsx`

Columnas mínimas (alias):
  - cliente / nombre + nit (crea Entidad si no existe)
  - operacion / referencia_operacion / contrato
  - fecha_snapshot / fecha_corte / al_31_mayo
  - saldo, dias_mora / dias_atraso, monto_exigible / exigible

Clave natural snapshot: (entidad, referencia_operacion, fecha_snapshot)
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

import pandas as pd

from core.services.column_map import normalize_columns, pick, pick_decimal, pick_int, require_any
from core.services.import_base import read_dataframe, run_import_batch
from core.wcg_models import DataImportBatch, Entidad, Producto, UnidadNegocio
from crm.services import _entidad_codigo_from_row, _resolve_unidad, _slug_codigo
from imports.currency_normalize import normalize_currency_code
from risk.models import (
    EstadoFinanciero,
    PagoRealizado,
    ProgramacionPago,
    RiskOperationSnapshot,
)


def _normalize_moneda_field(raw: str | None, default: str = "GTQ") -> tuple[str, str | None]:
    """Normaliza moneda de fila Risk; Q→GTQ con warning opcional."""
    code, warning = normalize_currency_code(raw)
    if not code:
        return default, None
    return code, warning


def _parse_date(value: str) -> date | None:
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(value[:19], fmt).date()
        except ValueError:
            continue
    try:
        return pd.to_datetime(value).date()
    except Exception:
        return None


def _ensure_entidad_from_row(row: pd.Series, errors: list[str]) -> Entidad | None:
    nombre = pick(
        row,
        "cliente",
        "nombre",
        "razon_social",
        "nombre_cliente",
        "client_name",
    )
    nit = pick(row, "nit", "nit_cliente")
    client_id = pick(row, "client_id", "cliente_id")
    codigo = (
        pick(row, "entidad_codigo", "codigo_cliente")
        or (f"CLI{client_id}" if client_id else "")
        or _entidad_codigo_from_row(row)
    )
    if not nombre and not codigo:
        errors.append("falta cliente o identificador")
        return None
    if not nombre:
        nombre = codigo
    if not codigo:
        codigo = _slug_codigo(nombre[:20])
    unidad = _resolve_unidad(
        pick(row, "unidad", "une", "unidad_negocio", "owning_business_unit", "financial_entity")
        or "LEASING"
    )
    if unidad is None:
        unidad = UnidadNegocio.objects.filter(code="LEASING").first()
    entidad, _ = Entidad.objects.update_or_create(
        codigo=codigo,
        defaults={"nombre": nombre, "nit": nit, "unidad_negocio": unidad, "activa": True},
    )
    return entidad


def _nivel_from_mora(dias: int) -> str:
    if dias >= 90:
        return RiskOperationSnapshot.NIVEL_CRITICO
    if dias >= 60:
        return RiskOperationSnapshot.NIVEL_ALTO
    if dias >= 30:
        return RiskOperationSnapshot.NIVEL_MEDIO
    return RiskOperationSnapshot.NIVEL_BAJO


def import_leasing_database(user, uploaded_file) -> DataImportBatch:
    from core.services.import_base import read_dataframe

    df = normalize_columns(read_dataframe(uploaded_file))
    require_any(
        df,
        [
            ["cliente", "nombre", "razon_social", "client_name", "nombre_cliente"],
            [
                "operacion",
                "referencia_operacion",
                "contrato",
                "no_operacion",
                "contract_number",
                "no_contrato",
            ],
        ],
    )
    uploaded_file.seek(0)

    def handler(row: pd.Series, errors: list[str]):
        entidad = _ensure_entidad_from_row(row, errors)
        if not entidad:
            return None
        referencia = pick(
            row,
            "operacion",
            "referencia_operacion",
            "contrato",
            "no_operacion",
            "no_contrato",
            "contract_number",
        )
        if not referencia:
            errors.append("falta referencia de operación")
            return None
        fecha_raw = pick(
            row,
            "fecha_snapshot",
            "fecha_corte",
            "al_31_mayo",
            "fecha",
            "corte",
            "balance_until",
            "final_validity",
        )
        fecha = _parse_date(fecha_raw) or date(2026, 6, 30)
        dias = pick_int(
            row,
            "dias_mora",
            "dias_atraso",
            "dias_de_mora",
            "mora_dias",
            "duedays",
            "due_days",
        )
        saldo = pick_decimal(
            row,
            "saldo",
            "saldo_total",
            "saldo_operacion",
            "capital_balance",
            "total_capital",
        )
        exigible = pick_decimal(
            row,
            "monto_exigible",
            "exigible",
            "monto_vencido",
            "vencido",
            "past_due_balance",
        )
        if exigible == 0 and saldo > 0 and dias > 0:
            exigible = saldo
        nivel = pick(row, "nivel_riesgo", "categoria_riesgo").upper() or _nivel_from_mora(dias)
        if nivel not in dict(RiskOperationSnapshot.NIVEL_CHOICES):
            nivel = _nivel_from_mora(dias)
        alerta_raw = pick(row, "alerta", "en_alerta", "status")
        alerta = dias >= 30 or alerta_raw.lower() in ("1", "si", "sí", "true", "yes", "vencido", "mora")
        prod_raw = pick(row, "producto", "producto_codigo") or "LEASING"
        prod_code = _slug_codigo(prod_raw)[:50] or "LEASING"
        producto, _ = Producto.objects.get_or_create(
            codigo=prod_code,
            defaults={"nombre": prod_raw[:200] or "Leasing", "activo": True},
        )
        detalle_parts = [
            pick(row, "detalle", "observaciones", "notas"),
            f"Status={pick(row, 'status')}" if pick(row, "status") else "",
            f"Advisor={pick(row, 'advisor_name')}" if pick(row, "advisor_name") else "",
            f"Cuotas pend.={pick(row, 'outstanding_installments')}"
            if pick(row, "outstanding_installments")
            else "",
        ]
        detalle = " | ".join(p for p in detalle_parts if p)
        _, created = RiskOperationSnapshot.objects.update_or_create(
            entidad=entidad,
            referencia_operacion=referencia,
            fecha_snapshot=fecha,
            defaults={
                "producto": producto,
                "nivel_riesgo": nivel,
                "dias_mora": dias,
                "saldo": saldo,
                "monto_exigible": exigible,
                "alerta": alerta,
                "detalle": detalle,
            },
        )
        periodo = fecha.strftime("%Y-%m")
        EstadoFinanciero.objects.update_or_create(
            entidad=entidad,
            periodo=periodo,
            defaults={
                "saldo_total": saldo,
                "mora_dias": dias,
                "exposicion": saldo,
            },
        )
        return created, not created

    uploaded_file.seek(0)
    return run_import_batch(
        user=user,
        modulo=DataImportBatch.MODULO_RISK,
        tipo_importacion="leasing_database",
        uploaded_file=uploaded_file,
        required_columns=[],
        row_handler=handler,
    )


def import_leasing_rentas(user, uploaded_file) -> DataImportBatch:
    """
    Enriquecimiento Balón: cuotas/rentas por contrato.
    Archivo: LeasingRentasYYYY-MM-DD.csv
    Matching: NoContrato → Entidad vía RiskOperationSnapshot.referencia_operacion
              o creación de ProgramacionPago / PagoRealizado.
    """
    df = normalize_columns(read_dataframe(uploaded_file))
    require_any(
        df,
        [
            ["no_contrato", "contrato", "contract_number", "referencia"],
            ["vencimiento", "fecha_programada", "fecha_vencimiento"],
        ],
    )
    uploaded_file.seek(0)
    currency_warnings: list[str] = []

    def handler(row: pd.Series, errors: list[str]):
        contrato = pick(row, "no_contrato", "contrato", "contract_number", "referencia", "operacion")
        if not contrato:
            errors.append("falta NoContrato")
            return None
        snap = (
            RiskOperationSnapshot.objects.filter(referencia_operacion__iexact=contrato)
            .select_related("entidad")
            .order_by("-fecha_snapshot")
            .first()
        )
        if snap:
            entidad = snap.entidad
        else:
            # Crear entidad mínima si el contrato aún no está en snapshots
            entidad, _ = Entidad.objects.get_or_create(
                codigo=_slug_codigo(contrato),
                defaults={
                    "nombre": f"Contrato {contrato}",
                    "unidad_negocio": UnidadNegocio.objects.filter(code="LEASING").first(),
                    "activa": True,
                    "tipo": Entidad.TIPO_CLIENTE,
                },
            )
        nro = pick(row, "no", "numero", "cuota", "nro") or "0"
        referencia = f"{contrato}-C{nro}"
        fecha = _parse_date(pick(row, "vencimiento", "fecha_programada", "fecha_vencimiento"))
        if not fecha:
            errors.append("falta fecha vencimiento")
            return None
        monto = pick_decimal(row, "renta_total", "valor_renta_con_mora", "valor_renta", "monto")
        estado = pick(row, "estado", "status").lower()
        moneda, mon_warn = _normalize_moneda_field(pick(row, "moneda"), "GTQ")
        if mon_warn:
            currency_warnings.append(mon_warn)
        _, created_prog = ProgramacionPago.objects.update_or_create(
            entidad=entidad,
            referencia=referencia,
            defaults={
                "fecha_programada": fecha,
                "monto": monto,
                "moneda": moneda,
            },
        )
        created = created_prog
        updated = not created_prog
        fecha_pago = _parse_date(pick(row, "fecha_pago"))
        if fecha_pago or estado in ("pagada", "pagado", "paid"):
            _, created_pago = PagoRealizado.objects.update_or_create(
                entidad=entidad,
                referencia=referencia,
                defaults={
                    "fecha_pago": fecha_pago or fecha,
                    "monto": monto,
                    "moneda": moneda,
                },
            )
            created = created or created_pago
            updated = updated or (not created_pago)
        return created, updated and not created

    uploaded_file.seek(0)
    batch = run_import_batch(
        user=user,
        modulo=DataImportBatch.MODULO_RISK,
        tipo_importacion="leasing_rentas",
        uploaded_file=uploaded_file,
        required_columns=[],
        row_handler=handler,
    )
    if currency_warnings:
        warn_line = (
            f"WARNING moneda: {len(currency_warnings)} fila(s) con 'Q' (u alias) "
            f"tratadas como GTQ. Corrija el archivo fuente a GTQ."
        )
        batch.log_texto = (warn_line + "\n" + (batch.log_texto or ""))[:8000]
        batch.save(update_fields=["log_texto"])
    return batch


def import_estados_financieros(user, uploaded_file) -> DataImportBatch:
    df = normalize_columns(read_dataframe(uploaded_file))
    require_any(df, [["entidad_codigo", "nit", "cliente"], ["periodo"]])

    def handler(row: pd.Series, errors: list[str]):
        entidad = _ensure_entidad_from_row(row, errors)
        if not entidad:
            return None
        periodo = pick(row, "periodo", "anio_mes", "mes")
        if not periodo:
            errors.append("periodo obligatorio")
            return None
        periodo = periodo.replace("/", "-")[:7]
        _, created = EstadoFinanciero.objects.update_or_create(
            entidad=entidad,
            periodo=periodo,
            defaults={
                "saldo_total": pick_decimal(row, "saldo_total", "saldo"),
                "mora_dias": pick_int(row, "mora_dias", "dias_mora"),
                "exposicion": pick_decimal(row, "exposicion"),
                "notas": pick(row, "notas"),
            },
        )
        return created, not created

    uploaded_file.seek(0)
    return run_import_batch(
        user=user,
        modulo=DataImportBatch.MODULO_RISK,
        tipo_importacion="estados_financieros",
        uploaded_file=uploaded_file,
        required_columns=[],
        row_handler=handler,
    )


def import_programacion_pagos(user, uploaded_file) -> DataImportBatch:
    df = normalize_columns(read_dataframe(uploaded_file))
    require_any(df, [["referencia", "operacion"], ["fecha_programada", "fecha_pago_programada"], ["monto"]])

    def handler(row: pd.Series, errors: list[str]):
        entidad = _ensure_entidad_from_row(row, errors)
        if not entidad:
            return None
        referencia = pick(row, "referencia", "operacion", "cuota")
        fecha = _parse_date(pick(row, "fecha_programada", "fecha_vencimiento"))
        if not referencia or not fecha:
            errors.append("referencia y fecha_programada obligatorias")
            return None
        _, created = ProgramacionPago.objects.update_or_create(
            entidad=entidad,
            referencia=referencia,
            defaults={
                "fecha_programada": fecha,
                "monto": pick_decimal(row, "monto"),
                "moneda": _normalize_moneda_field(pick(row, "moneda"), "GTQ")[0],
            },
        )
        return created, not created

    uploaded_file.seek(0)
    return run_import_batch(
        user=user,
        modulo=DataImportBatch.MODULO_RISK,
        tipo_importacion="programacion_pagos",
        uploaded_file=uploaded_file,
        required_columns=[],
        row_handler=handler,
    )


def import_pagos_realizados(user, uploaded_file) -> DataImportBatch:
    df = normalize_columns(read_dataframe(uploaded_file))
    require_any(df, [["referencia", "operacion"], ["fecha_pago"], ["monto"]])

    def handler(row: pd.Series, errors: list[str]):
        entidad = _ensure_entidad_from_row(row, errors)
        if not entidad:
            return None
        referencia = pick(row, "referencia", "operacion", "cuota")
        fecha = _parse_date(pick(row, "fecha_pago"))
        if not referencia or not fecha:
            errors.append("referencia y fecha_pago obligatorias")
            return None
        _, created = PagoRealizado.objects.update_or_create(
            entidad=entidad,
            referencia=referencia,
            defaults={
                "fecha_pago": fecha,
                "monto": pick_decimal(row, "monto"),
                "moneda": _normalize_moneda_field(pick(row, "moneda"), "GTQ")[0],
            },
        )
        return created, not created

    uploaded_file.seek(0)
    return run_import_batch(
        user=user,
        modulo=DataImportBatch.MODULO_RISK,
        tipo_importacion="pagos_realizados",
        uploaded_file=uploaded_file,
        required_columns=[],
        row_handler=handler,
    )


def import_snapshots(user, uploaded_file) -> DataImportBatch:
    """CSV genérico de snapshots — mismo mapeo que leasing en formato plano."""
    return import_leasing_database(user, uploaded_file)
