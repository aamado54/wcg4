# File: import_clientes_nuevos.py

import csv

from core.models import UNE, UNEAlias, MetricDefinition, Currency
from core.services.une_resolve import resolve_une_from_text
from decimal import Decimal
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from imports.models import FileUpload, NewClientImportHeader, NewClientImportRow
from pathlib import Path
from pgc.models import PGCPlan, MonthlyTarget, MonthlyMetricResult


def _resolve_file_upload(path: Path, file_upload_id: int | None) -> FileUpload | None:
    if file_upload_id:
        upload = FileUpload.objects.filter(pk=file_upload_id).first()
        if not upload:
            raise CommandError(f"FileUpload id={file_upload_id} no encontrado.")
        return upload

    path = path.resolve()
    candidates = FileUpload.objects.filter(
        file_type_detected=FileUpload.TYPE_NEW_CLIENTS,
    ).order_by("-id")[:80]
    for upload in candidates:
        try:
            if upload.stored_file and Path(upload.stored_file.path).resolve() == path:
                return upload
        except Exception:
            continue

    by_name = (
        FileUpload.objects.filter(
            file_type_detected=FileUpload.TYPE_NEW_CLIENTS,
            original_filename=path.name,
        )
        .order_by("-id")
        .first()
    )
    return by_name


def _ensure_header(year: int, month: int, upload: FileUpload | None) -> NewClientImportHeader:
    header = NewClientImportHeader.objects.filter(year=year, month=month).first()
    if header:
        return header

    if not upload:
        raise CommandError(
            f"No existe NewClientImportHeader para {year}-{month:02d} y no hay "
            "FileUpload de origen para crearlo. Sube el archivo vía Administración."
        )

    header, _ = NewClientImportHeader.objects.get_or_create(
        year=year,
        month=month,
        defaults={"file_upload": upload},
    )
    return header


class Command(BaseCommand):
    help = (
        "Importa ClientesNuevos (csv/tsv). Cada fila se guarda en su AnioMes; "
        "un solo archivo puede contener varios meses."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            type=str,
            required=True,
            help="Ruta al archivo ClientesNuevos (csv/tsv)",
        )
        parser.add_argument(
            "--file-upload-id",
            type=int,
            default=None,
            help="Id de FileUpload origen (opcional; se infiere por ruta si falta)",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        path = Path(options["path"])
        if not path.exists():
            raise CommandError(f"Archivo no encontrado: {path}")

        self.stdout.write(self.style.WARNING(f"Leyendo {path} ..."))

        imported_file_name = path.name
        source_upload = _resolve_file_upload(path, options.get("file_upload_id"))

        metric = MetricDefinition.objects.get(code=MetricDefinition.CODE_CLIENTES_NUEVOS)
        currencies = {c.code.upper(): c for c in Currency.objects.all()}
        headers_cache: dict[tuple[int, int], NewClientImportHeader] = {}

        aliases = {
            a.raw_value.strip().upper(): a.une
            for a in UNEAlias.objects.select_related("une").filter(is_active=True)
        }
        unes_by_code = {u.code: u for u in UNE.objects.all()}

        # clave: (year, month, une_id) -> conteo clientes nuevos
        counts: dict[tuple[int, int, int], int] = {}
        rows_written = 0
        rows_skipped = 0
        months_touched: set[tuple[int, int]] = set()

        with path.open("r", encoding="utf-8-sig") as f:
            sample = f.read(4096)
            f.seek(0)
            dialect = csv.Sniffer().sniff(sample, delimiters=[",", "\t", ";"])
            reader = csv.DictReader(f, dialect=dialect)

            for line_no, row in enumerate(reader, start=2):
                anio_mes = row.get("AnioMes") or row.get("aniomes")
                contratos_previos = row.get("ContratosPrevios") or row.get("contratosprevios")
                une_raw = row.get("UNE") or row.get("une")

                if not anio_mes or not une_raw:
                    rows_skipped += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"Fila {line_no}: omitida (falta AnioMes o UNE)."
                        )
                    )
                    continue

                try:
                    year_str, month_str = anio_mes.replace("-", "/").split("/")
                    year = int(year_str)
                    month = int(month_str)
                except Exception:
                    rows_skipped += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"Fila {line_no}: AnioMes no válido ({anio_mes!r})."
                        )
                    )
                    continue

                if month < 1 or month > 12:
                    rows_skipped += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"Fila {line_no}: mes inválido ({month})."
                        )
                    )
                    continue

                try:
                    prev = int(contratos_previos) if contratos_previos not in (None, "") else 0
                except ValueError:
                    prev = 0

                counts_as_new = prev == 0

                une = resolve_une_from_text(une_raw, aliases, unes_by_code)
                if not une:
                    rows_skipped += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"Fila {line_no}: UNE no reconocida ({une_raw!r})."
                        )
                    )
                    continue

                header_key = (year, month)
                header = headers_cache.get(header_key)
                if header is None:
                    header = _ensure_header(year, month, source_upload)
                    headers_cache[header_key] = header
                months_touched.add(header_key)

                client_name = (
                    row.get("Cliente")
                    or row.get("CLIENTE")
                    or row.get("cliente")
                    or ""
                ).strip()

                nit = (
                    row.get("NIT")
                    or row.get("Nit")
                    or row.get("nit")
                    or ""
                ).strip()

                operation_code = (
                    row.get("Operacion")
                    or row.get("Operación")
                    or row.get("OPERACION")
                    or row.get("operation_code")
                    or ""
                ).strip()

                currency_code = (
                    row.get("Moneda")
                    or row.get("MONEDA")
                    or row.get("moneda")
                    or ""
                ).strip().upper()

                amount_raw = (
                    row.get("Monto")
                    or row.get("MONTO")
                    or row.get("monto")
                    or ""
                ).strip()

                amount = None
                if amount_raw:
                    try:
                        # PGC expresa montos de ingresos en miles de US$;
                        # el archivo trae unidades → guardar ya dividido entre 1000.
                        amount = Decimal(str(amount_raw).replace(",", "")) / Decimal(
                            "1000"
                        )
                    except Exception:
                        amount = None

                currency = currencies.get(currency_code)

                NewClientImportRow.objects.create(
                    header=header,
                    une=une,
                    year=year,
                    month=month,
                    client_name=client_name,
                    nit=nit,
                    operation_code=operation_code,
                    previous_contracts=prev,
                    counts_as_new=counts_as_new,
                    currency=currency,
                    amount=amount,
                    source_row_number=line_no,
                    raw_une_value=une_raw,
                    observations="",
                )
                rows_written += 1

                if counts_as_new:
                    key = (year, month, une.id)
                    counts[key] = counts.get(key, 0) + 1

        if months_touched:
            months_label = ", ".join(
                f"{y}-{m:02d}" for y, m in sorted(months_touched)
            )
            self.stdout.write(
                f"Meses del archivo: {months_label}. "
                f"Filas guardadas: {rows_written}. Omitidas: {rows_skipped}."
            )

        years_in_file = sorted({year for (year, _, _), _ in counts.items()})
        if not years_in_file:
            # Puede haber filas guardadas sin counts_as_new; no es error duro.
            if rows_written:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Import completado: {rows_written} fila(s) almacenada(s); "
                        "ninguna contó como cliente nuevo (ContratosPrevios≠0)."
                    )
                )
                return
            self.stdout.write(
                self.style.WARNING("No se encontraron filas importables en el archivo.")
            )
            return
        if len(years_in_file) > 1:
            raise CommandError(
                f"El archivo contiene múltiples años {years_in_file}. "
                "Por ahora se espera un año por archivo."
            )
        year_for_plan = years_in_file[0]
        try:
            plan = PGCPlan.objects.get(year=year_for_plan)
        except PGCPlan.DoesNotExist:
            raise CommandError(f"No existe PGCPlan para año {year_for_plan}.")

        total_updated = 0
        for (year, month, une_id), count in counts.items():
            une = UNE.objects.get(id=une_id)
            try:
                target = MonthlyTarget.objects.get(
                    plan=plan,
                    une=une,
                    metric=metric,
                    year=year,
                    month=month,
                )
            except MonthlyTarget.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f"Sin MonthlyTarget para {une.code} {year}-{month:02d}"
                    )
                )
                continue

            mmr, _ = MonthlyMetricResult.objects.get_or_create(
                plan=plan,
                une=une,
                metric=metric,
                year=year,
                month=month,
                defaults={"target_value": target.target_value},
            )
            mmr.target_value = target.target_value
            mmr.measured_value = Decimal(str(count))
            mmr.calculation_note = (
                f"{count} clientes nuevos contados desde {imported_file_name}"
            )
            mmr.save()
            total_updated += 1
            self.stdout.write(
                f"Actualizado CLIENTES_NUEVOS {une.code} {year}-{month:02d}: {count}"
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Import CLIENTES_NUEVOS completado. "
                f"{rows_written} fila(s), {total_updated} métrica(s), "
                f"{len(months_touched)} mes(es)."
            )
        )
