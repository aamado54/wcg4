"""Detección inteligente de duplicados por módulo (revisión manual, sin borrado auto)."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

from django.db import transaction


@dataclass
class DuplicateGroup:
    module: str
    module_label: str
    natural_key_desc: str
    key_display: str
    keep_id: int
    duplicate_ids: list[int] = field(default_factory=list)
    sample_labels: list[str] = field(default_factory=list)

    @property
    def extra_count(self) -> int:
        return len(self.duplicate_ids)

    @property
    def total_count(self) -> int:
        return 1 + len(self.duplicate_ids)


def _groups_from_rows(
    module: str,
    module_label: str,
    natural_key_desc: str,
    rows: list[tuple[tuple, int, str]],
    *,
    keep_chooser=None,
) -> list[DuplicateGroup]:
    """
    rows: (key, id, label).
    Por defecto conserva el id más antiguo.
    ``keep_chooser(items)`` opcional: recibe list[(id, label)] y devuelve keep_id.
    """
    buckets: dict[tuple, list[tuple[int, str]]] = defaultdict(list)
    for key, pk, label in rows:
        buckets[key].append((pk, label))

    groups: list[DuplicateGroup] = []
    for key, items in buckets.items():
        if len(items) < 2:
            continue
        if keep_chooser:
            keep_id = keep_chooser(items)
            items_by_id = {pk: lab for pk, lab in items}
            keep_label = items_by_id.get(keep_id, items[0][1])
            dup_ids = [pk for pk, _ in items if pk != keep_id]
        else:
            keep_id, keep_label = items[0]
            dup_ids = [pk for pk, _ in items[1:]]
        labels = [keep_label] + [lab for pk, lab in items if pk != keep_id][:3]
        key_display = " | ".join(str(p) for p in key if p not in ("", None))[:180]
        groups.append(
            DuplicateGroup(
                module=module,
                module_label=module_label,
                natural_key_desc=natural_key_desc,
                key_display=key_display or "(vacío)",
                keep_id=keep_id,
                duplicate_ids=dup_ids,
                sample_labels=labels,
            )
        )
    groups.sort(key=lambda g: (-g.extra_count, g.key_display))
    return groups


def _crm_entidad_richness(ent) -> int:
    """Puntaje de información útil (NIT, contactos, productos, CRM, notas)."""
    from core.wcg_models import Contacto, RelacionEntidadProducto
    from crm.models import Interaccion, Tarea

    score = 0
    if (ent.nit or "").strip():
        score += 100
    if (ent.notas or "").strip():
        score += 10
    if ent.unidad_negocio_id:
        score += 5
    score += Contacto.objects.filter(entidad=ent).count() * 20
    score += RelacionEntidadProducto.objects.filter(entidad=ent).count() * 15
    score += Interaccion.objects.filter(entidad=ent).count() * 10
    score += Tarea.objects.filter(entidad=ent).count() * 10
    return score


def _choose_richest_crm_entidad(items: list[tuple[int, str]]) -> int:
    """Conserva la entidad con más detalle; empate → id más bajo (más antigua)."""
    from core.wcg_models import Entidad

    ids = [pk for pk, _ in items]
    best_id = ids[0]
    best_score = -1
    for ent in Entidad.objects.filter(id__in=ids):
        score = _crm_entidad_richness(ent)
        if score > best_score or (score == best_score and ent.id < best_id):
            best_score = score
            best_id = ent.id
    return best_id


def _crm_entidad_label(ent) -> str:
    score = _crm_entidad_richness(ent)
    nit = (ent.nit or "").strip() or "—"
    return f"{ent.codigo} · {ent.nombre} · NIT {nit} · info={score}"


def merge_crm_entidades_into(keep_id: int, loser_ids: list[int]) -> int:
    """
    Fusiona detalles de loser → keep y luego borra losers.
    Reasigna contactos, productos, interacciones, tareas y vínculos Risk/PGO.
    Completa campos vacíos del keep (NIT, notas, unidad).
    """
    from core.wcg_models import Contacto, Entidad, RelacionEntidadProducto
    from crm.models import Interaccion, Tarea

    keep = Entidad.objects.filter(pk=keep_id).first()
    if not keep:
        return 0

    deleted = 0
    for loser_id in loser_ids:
        if loser_id == keep_id:
            continue
        loser = Entidad.objects.filter(pk=loser_id).first()
        if not loser:
            continue

        # Completar campos vacíos del registro conservado.
        changed = False
        if not (keep.nit or "").strip() and (loser.nit or "").strip():
            keep.nit = loser.nit
            changed = True
        if not (keep.notas or "").strip() and (loser.notas or "").strip():
            keep.notas = loser.notas
            changed = True
        if not keep.unidad_negocio_id and loser.unidad_negocio_id:
            keep.unidad_negocio_id = loser.unidad_negocio_id
            changed = True
        if changed:
            keep.save()

        # Contactos: reasignar si no hay homónimo; si hay, conservar el del keep.
        for c in list(Contacto.objects.filter(entidad=loser)):
            exists = Contacto.objects.filter(entidad=keep).filter(
                nombre__iexact=(c.nombre or "").strip()
            ).exists()
            if exists:
                c.delete()
            else:
                c.entidad = keep
                c.save(update_fields=["entidad"])

        for rel in list(RelacionEntidadProducto.objects.filter(entidad=loser)):
            if RelacionEntidadProducto.objects.filter(
                entidad=keep, producto_id=rel.producto_id
            ).exists():
                rel.delete()
            else:
                rel.entidad = keep
                rel.save(update_fields=["entidad"])

        Interaccion.objects.filter(entidad=loser).update(entidad=keep)
        Tarea.objects.filter(entidad=loser).update(entidad=keep)

        # Risk / PGO productivos (si existen vínculos).
        try:
            from risk.models import (
                ContactoCobranza,
                EstadoFinanciero,
                PagoRealizado,
                ProgramacionPago,
                RiskOperationSnapshot,
            )

            for snap in list(RiskOperationSnapshot.objects.filter(entidad=loser)):
                conflict = RiskOperationSnapshot.objects.filter(
                    entidad=keep,
                    referencia_operacion=snap.referencia_operacion,
                    fecha_snapshot=snap.fecha_snapshot,
                ).exists()
                if conflict:
                    snap.delete()
                else:
                    snap.entidad = keep
                    snap.save(update_fields=["entidad"])
            for model in (ProgramacionPago, PagoRealizado):
                for row in list(model.objects.filter(entidad=loser)):
                    if model.objects.filter(entidad=keep, referencia=row.referencia).exists():
                        row.delete()
                    else:
                        row.entidad = keep
                        row.save(update_fields=["entidad"])
            EstadoFinanciero.objects.filter(entidad=loser).update(entidad=keep)
            ContactoCobranza.objects.filter(entidad=loser).update(entidad=keep)
        except Exception:
            pass

        try:
            from pgo.models import Ticket

            Ticket.objects.filter(entidad=loser).update(entidad=keep)
        except Exception:
            pass

        loser.delete()
        deleted += 1

    return deleted


def scan_new_client_duplicates(year: int | None = None, month: int | None = None) -> list[DuplicateGroup]:
    from imports.models import NewClientImportRow

    qs = NewClientImportRow.objects.select_related("une", "currency").order_by("id")
    if year:
        qs = qs.filter(year=year)
    if month:
        qs = qs.filter(month=month)

    rows = []
    for row in qs.iterator(chunk_size=500):
        key = (
            row.year,
            row.month,
            row.une_id,
            (row.client_name or "").strip().casefold(),
            (row.nit or "").strip(),
            (row.operation_code or "").strip(),
            row.previous_contracts,
            row.currency_id,
            str(row.amount) if row.amount is not None else "",
        )
        label = f"{row.year}-{row.month:02d} · {row.client_name or '—'} · {row.operation_code or '—'}"
        rows.append((key, row.id, label))
    return _groups_from_rows(
        "new_clients",
        "PGC — Clientes nuevos",
        "año/mes + UNE + cliente + NIT + operación + contratos + moneda + monto",
        rows,
    )


def scan_cross_sale_duplicates(year: int | None = None, month: int | None = None) -> list[DuplicateGroup]:
    from imports.models import CrossSaleImportRow

    qs = CrossSaleImportRow.objects.select_related(
        "une_destination", "une_origin", "currency"
    ).order_by("id")
    if year:
        qs = qs.filter(year=year)
    if month:
        qs = qs.filter(month=month)

    rows = []
    for row in qs.iterator(chunk_size=500):
        key = (
            row.year,
            row.month,
            (row.client_name or "").strip().casefold(),
            (row.operation_code or "").strip(),
            str(row.date) if row.date else "",
            row.currency_id,
            row.une_destination_id,
            row.une_origin_id,
        )
        label = f"{row.year}-{row.month:02d} · {row.client_name or '—'} · {row.operation_code or '—'}"
        rows.append((key, row.id, label))
    return _groups_from_rows(
        "cross_sale",
        "PGC — Venta cruzada",
        "año/mes + cliente + operación + fecha + moneda + UNE origen/destino",
        rows,
    )


def scan_crm_entity_duplicates() -> list[DuplicateGroup]:
    """Duplicados por NIT: conserva la entidad con más detalle."""
    from core.wcg_models import Entidad

    rows = []
    for ent in Entidad.objects.order_by("id").iterator(chunk_size=500):
        nit = (getattr(ent, "nit", None) or "").strip()
        if not nit:
            continue
        key = (nit.casefold(),)
        rows.append((key, ent.id, _crm_entidad_label(ent)))
    return _groups_from_rows(
        "crm_entidad",
        "CRM — Entidades (mismo NIT)",
        "NIT · se conserva el registro con más información (detalle fusionado)",
        rows,
        keep_chooser=_choose_richest_crm_entidad,
    )


def scan_crm_nombre_duplicates() -> list[DuplicateGroup]:
    """Mismo nombre: conserva el registro más completo y fusiona detalles al borrar."""
    from core.wcg_models import Entidad

    rows = []
    for ent in Entidad.objects.order_by("id").iterator(chunk_size=500):
        nombre = (ent.nombre or "").strip()
        if not nombre:
            continue
        key = (nombre.casefold(),)
        rows.append((key, ent.id, _crm_entidad_label(ent)))
    return _groups_from_rows(
        "crm_nombre",
        "CRM — Entidades (mismo nombre)",
        "nombre · se conserva el de mayor info=NIT/contactos/productos/CRM",
        rows,
        keep_chooser=_choose_richest_crm_entidad,
    )


def scan_pgo_ticket_duplicates() -> list[DuplicateGroup]:
    """Tickets con mismo código (no debería ocurrir con upsert; se reporta si hay)."""
    from pgo.models import Ticket

    rows = []
    for t in Ticket.objects.order_by("id").iterator(chunk_size=500):
        codigo = (t.codigo or "").strip().casefold()
        if not codigo:
            continue
        key = (codigo,)
        label = f"{t.codigo} · {(t.titulo or '')[:40]}"
        rows.append((key, t.id, label))
    return _groups_from_rows(
        "pgo_ticket",
        "PGO — Tickets",
        "codigo (clave natural upsert)",
        rows,
    )


def scan_risk_snapshot_duplicates() -> list[DuplicateGroup]:
    """Misma entidad+referencia+fecha (violación lógica de unique_together)."""
    from risk.models import RiskOperationSnapshot

    rows = []
    for snap in RiskOperationSnapshot.objects.select_related("entidad").order_by("id").iterator(
        chunk_size=500
    ):
        key = (
            snap.entidad_id,
            (snap.referencia_operacion or "").strip().casefold(),
            str(snap.fecha_snapshot),
        )
        nombre = snap.entidad.nombre if snap.entidad_id else "—"
        label = f"{nombre} · {snap.referencia_operacion} · {snap.fecha_snapshot}"
        rows.append((key, snap.id, label))
    return _groups_from_rows(
        "risk_snapshot",
        "Riesgo — Snapshots exactos",
        "entidad + referencia_operacion + fecha_snapshot",
        rows,
    )


def scan_risk_referencia_report_duplicates() -> list[DuplicateGroup]:
    """
    Misma referencia de operación bajo distintas entidades (líneas duplicadas en Balón).
    Conserva snapshots de la entidad más antigua; marca el resto para borrado manual.
    """
    from risk.models import RiskOperationSnapshot

    by_ref: dict[str, dict[int, list[tuple[int, str]]]] = defaultdict(lambda: defaultdict(list))
    for snap in RiskOperationSnapshot.objects.select_related("entidad").order_by("id").iterator(
        chunk_size=500
    ):
        ref = (snap.referencia_operacion or "").strip()
        if not ref or not snap.entidad_id:
            continue
        nombre = snap.entidad.nombre if snap.entidad_id else "—"
        codigo = snap.entidad.codigo if snap.entidad_id else "—"
        label = f"{codigo} · {nombre} · {ref} · {snap.fecha_snapshot}"
        by_ref[ref.casefold()][snap.entidad_id].append((snap.id, label))

    groups: list[DuplicateGroup] = []
    for ref_key, entidades in by_ref.items():
        if len(entidades) < 2:
            continue
        # Conservar la entidad con el snapshot id más bajo (más antigua).
        ordered_ents = sorted(
            entidades.items(),
            key=lambda item: min(sid for sid, _ in item[1]),
        )
        keep_ent_id, keep_snaps = ordered_ents[0]
        keep_id = keep_snaps[0][0]
        dup_ids: list[int] = []
        labels = [keep_snaps[0][1]]
        for ent_id, snaps in ordered_ents[1:]:
            for sid, lab in snaps:
                dup_ids.append(sid)
                if len(labels) < 4:
                    labels.append(lab)
        if not dup_ids:
            continue
        groups.append(
            DuplicateGroup(
                module="risk_referencia",
                module_label="Balón — Misma operación / otra entidad",
                natural_key_desc="referencia_operacion compartida entre entidades distintas",
                key_display=ref_key[:180],
                keep_id=keep_id,
                duplicate_ids=dup_ids,
                sample_labels=labels,
            )
        )
    groups.sort(key=lambda g: (-g.extra_count, g.key_display))
    return groups


def scan_file_upload_duplicates() -> list[DuplicateGroup]:
    """Mismo nombre de archivo + tipo detectado (reimportaciones)."""
    from imports.models import FileUpload

    rows = []
    for up in FileUpload.objects.order_by("id").iterator(chunk_size=200):
        name = (up.original_filename or "").strip().casefold()
        if not name:
            continue
        key = (name, up.file_type_detected or "")
        label = f"{up.original_filename} · {up.get_file_type_detected_display()} · #{up.id}"
        rows.append((key, up.id, label))
    return _groups_from_rows(
        "file_upload",
        "Importaciones — Archivos (nombre + tipo)",
        "nombre de archivo + tipo detectado",
        rows,
    )


def scan_batch_duplicates() -> list[DuplicateGroup]:
    """Lotes con mismo módulo + tipo + nombre de archivo."""
    from core.wcg_models import DataImportBatch

    rows = []
    for b in DataImportBatch.objects.order_by("id").iterator(chunk_size=200):
        name = (b.archivo_nombre or "").strip().casefold()
        if not name:
            continue
        key = (b.modulo or "", b.tipo_importacion or "", name)
        label = f"{b.modulo}/{b.tipo_importacion} · {b.archivo_nombre} · #{b.id}"
        rows.append((key, b.id, label))
    return _groups_from_rows(
        "import_batch",
        "Importaciones — Lotes (módulo + tipo + archivo)",
        "modulo + tipo_importacion + archivo_nombre",
        rows,
    )


MODULE_SCANNERS = {
    # Reportes operativos primero (lo que ve gerencia en CRM / Balón).
    "crm_nombre": ("CRM — Entidades (mismo nombre)", scan_crm_nombre_duplicates),
    "crm_entidad": ("CRM — Entidades (mismo NIT)", scan_crm_entity_duplicates),
    "risk_referencia": ("Balón — Misma operación / otra entidad", scan_risk_referencia_report_duplicates),
    "risk_snapshot": ("Balón — Snapshots exactos", scan_risk_snapshot_duplicates),
    "new_clients": ("PGC — Clientes nuevos", scan_new_client_duplicates),
    "cross_sale": ("PGC — Venta cruzada", scan_cross_sale_duplicates),
    "pgo_ticket": ("PGO — Tickets", scan_pgo_ticket_duplicates),
    "file_upload": ("Archivos subidos", scan_file_upload_duplicates),
    "import_batch": ("Lotes de importación", scan_batch_duplicates),
}


def scan_all_duplicates(module: str | None = None) -> list[DuplicateGroup]:
    groups: list[DuplicateGroup] = []
    scanners = MODULE_SCANNERS
    if module:
        if module not in scanners:
            return []
        scanners = {module: scanners[module]}
    for _key, (_label, fn) in scanners.items():
        try:
            groups.extend(fn())
        except Exception:
            # Módulo opcional / tabla ausente: no tumbar la revisión.
            continue
    return groups


def summarize_duplicates(groups: list[DuplicateGroup] | None = None) -> dict[str, int]:
    groups = groups if groups is not None else scan_all_duplicates()
    by_module: dict[str, int] = defaultdict(int)
    for g in groups:
        by_module[g.module] += g.extra_count
    by_module["__total__"] = sum(by_module.values())
    return dict(by_module)


@transaction.atomic
def delete_duplicate_ids(module: str, ids: list[int], keep_id: int | None = None) -> int:
    """
    Borra solo los IDs indicados (revisión manual).
    En CRM: fusiona detalles hacia keep_id antes de borrar.
    """
    ids = [int(i) for i in ids if i]
    if not ids:
        return 0

    if module == "new_clients":
        from imports.models import NewClientImportRow
        from pgc.admin_period import _sync_clientes_nuevos_metrics_from_rows

        qs = NewClientImportRow.objects.filter(id__in=ids)
        periods = list(qs.values_list("year", "month").distinct())
        deleted = qs.delete()[0]
        for year, month in periods:
            _sync_clientes_nuevos_metrics_from_rows(year, month)
        return deleted

    if module == "cross_sale":
        from imports.models import CrossSaleImportRow

        return CrossSaleImportRow.objects.filter(id__in=ids).delete()[0]

    if module in ("crm_entidad", "crm_nombre"):
        if keep_id:
            return merge_crm_entidades_into(int(keep_id), ids)
        from core.wcg_models import Entidad

        return Entidad.objects.filter(id__in=ids).delete()[0]

    if module == "pgo_ticket":
        from pgo.models import Ticket

        return Ticket.objects.filter(id__in=ids).delete()[0]

    if module in ("risk_snapshot", "risk_referencia"):
        from risk.models import RiskOperationSnapshot

        return RiskOperationSnapshot.objects.filter(id__in=ids).delete()[0]

    if module == "file_upload":
        from imports.models import FileUpload

        return FileUpload.objects.filter(id__in=ids).delete()[0]

    if module == "import_batch":
        from core.wcg_models import DataImportBatch

        return DataImportBatch.objects.filter(id__in=ids).delete()[0]

    return 0
