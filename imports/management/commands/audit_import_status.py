"""Estado de auditoría de importaciones (dispatch y eventos registrados)."""

from __future__ import annotations

from django.core.management.base import BaseCommand
from django.db.models import Count

from imports.audit import audit_summary_counts, latest_events_for_path
from imports.models import FileUpload, ImportAuditEvent


class Command(BaseCommand):
    help = "Muestra eventos ImportAuditEvent y resumen FileUpload (--detailed | --checklist)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--detailed",
            action="store_true",
            help="Lista eventos recientes con detalle.",
        )
        parser.add_argument(
            "--checklist",
            action="store_true",
            help="Salida markdown tipo checklist para cierre ops.",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=50,
            help="Máximo de eventos en --detailed (default 50).",
        )
        parser.add_argument(
            "--path",
            type=str,
            default="",
            help="Filtra eventos por file_path_key (coincidencia o nombre de archivo).",
        )

    def handle(self, *args, **options):
        detailed = options["detailed"]
        checklist = options["checklist"]
        limit = options["limit"]
        path_filter = (options.get("path") or "").strip()

        if not detailed and not checklist:
            detailed = True

        summary = audit_summary_counts()
        total = summary["total"]
        fail_count = summary["fail"]
        ok_count = summary["ok"]
        by_tipo = summary["by_tipo"]

        evt_qs = ImportAuditEvent.objects.select_related("user", "file_upload")
        if path_filter:
            evt_qs = latest_events_for_path(path_filter, limit=10000)
            total = evt_qs.count()
            fail_count = evt_qs.filter(success=False).count()
            ok_count = total - fail_count
            by_tipo = list(
                evt_qs.exclude(import_tipo="")
                .values("import_tipo")
                .annotate(n=Count("id"))
                .order_by("-n")[:15]
            )

        upload_errors = FileUpload.objects.filter(
            status=FileUpload.STATUS_PARSED_ERROR
        ).count()
        upload_pending = FileUpload.objects.filter(
            status=FileUpload.STATUS_UPLOADED
        ).count()

        if checklist:
            lines = [
                "# Checklist auditoría importaciones",
                "",
                f"- [ ] Revisar **{fail_count}** eventos FAIL (de {total} registrados)",
                f"- [ ] FileUpload E1 (parsed error): **{upload_errors}**",
                f"- [ ] FileUpload P1 (sin procesar): **{upload_pending}**",
                "",
                "## Por tipo (ImportAuditEvent)",
            ]
            for row in by_tipo:
                lines.append(f"- [ ] `{row['import_tipo']}`: {row['n']} eventos")
            lines.extend(
                [
                    "",
                    "## Comandos",
                    "- `python manage.py audit_import_status --detailed`",
                    "- Reimportar solo tras corregir fuente (ver `dispatch.py`)",
                ]
            )
            self.stdout.write("\n".join(lines))
            return

        if path_filter:
            self.stdout.write(f"Filtro path: {path_filter}")
        self.stdout.write(f"ImportAuditEvent: total={total} ok={ok_count} fail={fail_count}")
        self.stdout.write(
            f"FileUpload: errors={upload_errors} pending_parse={upload_pending}"
        )
        if by_tipo:
            self.stdout.write("Por import_tipo:")
            for row in by_tipo:
                self.stdout.write(f"  {row['import_tipo']}: {row['n']}")

        if detailed:
            self.stdout.write("")
            self.stdout.write("Últimos eventos:")
            for ev in evt_qs[:limit]:
                user = ev.user.username if ev.user else "—"
                flag = "OK" if ev.success else "FAIL"
                self.stdout.write(
                    f"  [{flag}] {ev.loaded_at:%Y-%m-%d %H:%M} "
                    f"{ev.import_tipo or '?'} {ev.file_path_key[:80]} "
                    f"user={user} avail={ev.file_available}"
                )
                if ev.error_message and not ev.success:
                    self.stdout.write(f"       err: {ev.error_message[:200]}")