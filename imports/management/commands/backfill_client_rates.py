"""Corrige rate_basis e interest_rate en todo el histórico de clientes nuevos."""

from __future__ import annotations

from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import Currency
from imports.client_rates import clean_cell, match_key, source_row_index
from imports.currency_normalize import normalize_currency_code
from imports.models import FileUpload, NewClientImportRow


class Command(BaseCommand):
    help = (
        "Investment/inversiones → tasa anual; Leasing/Factoraje → mensual. "
        "Aplica a todas las filas existentes y recupera Porcentaje/Monto "
        "desde los CSV de origen cuando estén vacíos."
    )

    def handle(self, *args, **options):
        currencies = {c.code: c for c in Currency.objects.filter(is_active=True)}
        source_maps: list[dict] = []
        for upload in FileUpload.objects.filter(
            file_type_detected=FileUpload.TYPE_NEW_CLIENTS
        ).order_by("id"):
            try:
                path = Path(upload.stored_file.path) if upload.stored_file else None
            except Exception:
                path = None
            if not path or not path.exists():
                continue
            idx = source_row_index(path)
            if idx:
                source_maps.append(idx)
                self.stdout.write(f"Fuente {upload.original_filename}: {len(idx)} fila(s).")

        basis_n = rate_n = amount_n = name_n = 0
        qs = NewClientImportRow.objects.select_related("une", "currency", "header")
        with transaction.atomic():
            for row in qs.iterator():
                fields: list[str] = []

                cleaned_name = clean_cell(row.client_name)
                cleaned_nit = clean_cell(row.nit)
                cleaned_op = clean_cell(row.operation_code)
                if cleaned_name != (row.client_name or ""):
                    row.client_name = cleaned_name
                    fields.append("client_name")
                    name_n += 1
                if cleaned_nit != (row.nit or ""):
                    row.nit = cleaned_nit
                    fields.append("nit")
                if cleaned_op != (row.operation_code or ""):
                    row.operation_code = cleaned_op
                    fields.append("operation_code")

                key = match_key(row.nit, row.operation_code, row.year, row.month)
                payload = None
                for idx in source_maps:
                    payload = idx.get(key)
                    if payload:
                        break

                if payload:
                    if row.interest_rate is None and payload["interest_rate"] is not None:
                        row.interest_rate = payload["interest_rate"]
                        fields.append("interest_rate")
                        rate_n += 1
                    if row.amount is None and payload["amount"] is not None:
                        row.amount = payload["amount"]
                        fields.append("amount")
                        amount_n += 1
                    if not row.currency_id and payload["currency"]:
                        code, _ = normalize_currency_code(payload["currency"])
                        currency = currencies.get(code) if code else None
                        if currency:
                            row.currency = currency
                            fields.append("currency")
                    if not (row.raw_une_value or "").strip() and payload["raw_une"]:
                        row.raw_une_value = payload["raw_une"]
                        fields.append("raw_une_value")

                old_basis = row.rate_basis
                row.save()
                if row.rate_basis and row.rate_basis != old_basis:
                    basis_n += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"OK rate_basis={basis_n} tasas={rate_n} montos={amount_n} "
                f"nombres={name_n} filas={qs.count()}"
            )
        )
