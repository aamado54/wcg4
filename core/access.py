"""Reglas de acceso WCG: Balón/Gerencia vs operación PGC/PGO/CRM."""

from __future__ import annotations

from functools import wraps

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


def risk_gerencia_usernames() -> set[str]:
    raw = getattr(
        settings,
        "WCG_RISK_GERENCIA_USERNAMES",
        ("caa", "gsoler"),
    )
    return {str(u).strip().lower() for u in raw if str(u).strip()}


def can_access_risk_gerencia(user) -> bool:
    if user is None or not getattr(user, "is_authenticated", False):
        return False
    if not getattr(user, "is_active", False):
        return False
    return user.username.lower() in risk_gerencia_usernames()


def can_access_ops(user) -> bool:
    """PGC / PGO / CRM / importaciones operativas: cualquier usuario activo."""
    return bool(
        user is not None
        and getattr(user, "is_authenticated", False)
        and getattr(user, "is_active", False)
    )


def risk_gerencia_required(view_func):
    """Login + allowlist Balón de Riesgo / Centro Gerencial."""

    @login_required
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not can_access_risk_gerencia(request.user):
            messages.error(
                request,
                "No tiene acceso al Balón de Riesgo ni al Centro Gerencial.",
            )
            return redirect("portal:home")
        return view_func(request, *args, **kwargs)

    return _wrapped


class RiskGerenciaRequiredMixin(UserPassesTestMixin):
    """Mixin para CBVs de risk/gerencia."""

    raise_exception = False

    def test_func(self):
        return can_access_risk_gerencia(self.request.user)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.error(
            self.request,
            "No tiene acceso al Balón de Riesgo ni al Centro Gerencial.",
        )
        return redirect("portal:home")


def wcg_access(request):
    """Context processor para plantillas."""
    user = getattr(request, "user", None)
    return {
        "can_access_risk_gerencia": can_access_risk_gerencia(user),
        "can_access_ops": can_access_ops(user),
    }
