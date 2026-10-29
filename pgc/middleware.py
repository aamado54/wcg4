"""Recálculo PGC automático al servir pantallas que muestran scores."""

from __future__ import annotations

import logging
import re

from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

# GET en estas rutas dispara recálculo silencioso si hay pendientes.
_AUTO_RECALC_PATHS = (
    re.compile(r"^/admin-hub"),
    re.compile(r"^/tablero/?"),
    re.compile(r"^/ingresos/?"),
    re.compile(r"^/clientes-nuevos/?"),
    re.compile(r"^/venta-cruzada/?"),
    re.compile(r"^/respuesta-reqs/?"),
)


class PgcAutoRecalcMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method != "GET":
            return None
        user = getattr(request, "user", None)
        if user is None or not getattr(user, "is_authenticated", False):
            return None
        path = request.path or ""
        if not any(p.match(path) for p in _AUTO_RECALC_PATHS):
            return None
        try:
            from pgc.admin_recalc import maybe_auto_recalc

            maybe_auto_recalc(user=user, source=f"http_get:{path}")
        except Exception:
            logger.exception("Recálculo automático PGC falló en %s", path)
        if path.startswith("/tablero"):
            try:
                from pgc.tv_charts_generate import schedule_tv_charts_refresh

                last = request.session.get("pgc_tv_charts_refresh_ts")
                now_ts = timezone.now().timestamp()
                if last is None or (now_ts - float(last)) >= 3600:
                    request.session["pgc_tv_charts_refresh_ts"] = now_ts
                    schedule_tv_charts_refresh(reason="tablero_session")
            except Exception:
                logger.exception("Refresh charts TV (tablero) falló")
        return None
