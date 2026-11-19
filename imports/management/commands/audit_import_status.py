"""Estado de auditoría de importaciones (dispatch y eventos registrados)."""

from __future__ import annotations

from django.core.management.base import BaseCommand
from django.db.models import Count, Q
from django.utils import timezone

from imports.audit import audit_summary_counts, latest_events_for_path
from imports.audit_cli_registry import (
    CLI_IMPORT_COMMANDS,
    DISPATCH_IMPORT_TIPOS,
    cli_audit_coverage_ratio,
    missing_cli_mixin_commands,
)
from imports.detection import TYPE_LABELS
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
        parser.add_argument(
            "--fail-only",
            action="store_true",
            help="En --detailed, solo eventos con success=False.",
        )
        parser.add_argument(
            "--since",
            type=str,
            default="",
            help="YYYY-MM-DD; eventos desde esa fecha (inclusive).",
        )
        parser.add_argument(
            "--coverage",
            action="store_true",
            help="Muestra cobertura CLI mixin + tipos hub dispatch.",
        )
        parser.add_argument(
            "--repository",
            action="store_true",
            help="Ejecuta audit_data_repository (carpetas 1-pgc…5-plal) y muestra ruta del .md.",
        )

    def handle(self, *args, **options):
        if options.get("repository"):
            from core.services.data_repository_audit import run_data_repository_audit

            rows, report_path = run_data_repository_audit()
            flagged = sum(1 for r in rows if r.flags)
            self.stdout.write(
                f"Data repository: {len(rows)} archivos, {flagged} con alertas."
            )
            if report_path:
                self.stdout.write(f"Reporte: {report_path}")
            return

        detailed = options["detailed"]
        checklist = options["checklist"]
        limit = options["limit"]
        path_filter = (options.get("path") or "").strip()
        fail_only = options.get("fail_only")
        since_raw = (options.get("since") or "").strip()

        if options.get("coverage"):
            with_mixin, total, pct = cli_audit_coverage_ratio()
            self.stdout.write(
                f"CLI import_* con mixin: {with_mixin}/{total} ({pct:.0f}%)"
            )
            missing = missing_cli_mixin_commands()
            if missing:
                self.stdout.write("Sin mixin (consciente):")
                for name in missing:
                    self.stdout.write(f"  - {name}")
            self.stdout.write(f"Hub dispatch tipos auditados: {len(DISPATCH_IMPORT_TIPOS)}")
            for tipo in DISPATCH_IMPORT_TIPOS:
                lab = TYPE_LABELS.get(tipo, tipo)
                self.stdout.write(f"  - {tipo}: {lab}")
            self.stdout.write("")
            self.stdout.write("Registro CLI:")
            for row in CLI_IMPORT_COMMANDS:
                flag = "OK" if row.get("mixin") else "—"
                note = row.get("note") or ""
                extra = f" ({note})" if note else ""
                self.stdout.write(
                    f"  [{flag}] {row.get('app')}.{row['command']} "
                    f"tipo={row.get('tipo') or '—'}{extra}"
                )
            if not detailed and not checklist:
                return

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
        if since_raw:
            try:
                from datetime import datetime

                dt = datetime.strptime(since_raw, "%Y-%m-%d")
                dt = timezone.make_aware(dt, timezone.get_current_timezone())
                evt_qs = evt_qs.filter(loaded_at__gte=dt)
            except ValueError:
                self.stderr.write(f"Fecha --since inválida: {since_raw}")
        if fail_only:
            evt_qs = evt_qs.filter(success=False)

        if path_filter or since_raw or fail_only:
            total = evt_qs.count()
            fail_count = evt_qs.filter(success=False).count()
            ok_count = total - fail_count
            by_tipo = list(
                evt_qs.exclude(import_tipo="")
                .values("import_tipo")
                .annotate(n=Count("id"), fails=Count("id", filter=Q(success=False)))
                .order_by("-n")[:20]
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
                "## Por tipo (quién / cuándo / éxito en UI)",
            ]
            for row in by_tipo:
                tipo = row["import_tipo"]
                lab = TYPE_LABELS.get(tipo, tipo)
                fails = row.get("fails", 0)
                extra = f", **{fails} fallos**" if fails else ""
                lines.append(f"- [ ] `{tipo}` — {lab}: {row['n']} eventos{extra}")
            if fail_count:
                lines.extend(["", "## Últimos FAIL (resumen)"])
                for ev in evt_qs.filter(success=False).order_by("-loaded_at")[:10]:
                    user = ev.user.username if ev.user else "—"
                    lines.append(
                        f"- [ ] {ev.loaded_at:%Y-%m-%d %H:%M} · {ev.import_tipo or '?'} · "
                        f"user={user} · `{ev.file_path_key[:72]}`"
                    )
            with_mixin, total, pct = cli_audit_coverage_ratio()
            lines.extend(
                [
                    "",
                    f"## Cobertura hooks CLI ({with_mixin}/{total}, {pct:.0f}%)",
                ]
            )
            for row in CLI_IMPORT_COMMANDS:
                mark = "x" if row.get("mixin") else " "
                note = row.get("note") or ""
                suf = f" — {note}" if note else ""
                lines.append(
                    f"- [{mark}] `{row.get('app')}.{row['command']}` "
                    f"({row.get('tipo') or 'n/a'}){suf}"
                )
            lines.extend(
                [
                    "",
                    "## Hub dispatch (auditoría automática)",
                ]
            )
            for tipo in DISPATCH_IMPORT_TIPOS:
                lines.append(f"- [x] `{tipo}` — {TYPE_LABELS.get(tipo, tipo)}")
            lines.extend(
                [
                    "",
                    "## Comandos / UI",
                    "- `python manage.py audit_import_status --detailed --fail-only`",
                    "- `python manage.py audit_import_status --coverage`",
                    "- Staff: Importaciones → **Auditoría** (`/importaciones/auditoria/`)",
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
            title = "Últimos eventos"
            if fail_only:
                title += " (solo FAIL)"
            if since_raw:
                title += f" desde {since_raw}"
            self.stdout.write(title + ":")
            for ev in evt_qs.order_by("-loaded_at")[:limit]:
                user = ev.user.username if ev.user else "—"
                flag = "OK" if ev.success else "FAIL"
                src = ev.source or "—"
                self.stdout.write(
                    f"  [{flag}] id={ev.pk} {ev.loaded_at:%Y-%m-%d %H:%M:%S} "
                    f"tipo={ev.import_tipo or '?'} source={src} "
                    f"user={user} avail={ev.file_available}"
                )
                self.stdout.write(f"       path: {ev.file_path_key[:120]}")
                if ev.error_message and not ev.success:
                    self.stdout.write(f"       err: {ev.error_message[:300]}")
                elif ev.detail_json:
                    keys = ", ".join(sorted(ev.detail_json.keys())[:8])
                    if keys:
                        self.stdout.write(f"       detail keys: {keys}")