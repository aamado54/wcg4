import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from . import calc as engine
from .models import GerenciaScenario


def _bu(request) -> str:
    bu = (request.GET.get("bu") or "T").upper()
    return bu if bu in ("T", "F", "L") else "T"


def _nav(active: str) -> list[dict]:
    items = [
        ("intermediacion", "Intermediación", "gerencia:intermediacion"),
        ("liquidez", "Liquidez", "gerencia:liquidez"),
        ("estructura", "Estructura", "gerencia:estructura"),
        ("comando", "Comando", "gerencia:comando"),
        ("indices", "Índices", "gerencia:indices"),
        ("whatif", "What-if", "gerencia:whatif"),
        ("detalle", "Detalle", "gerencia:detalle"),
    ]
    return [
        {"key": k, "label": lab, "url_name": u, "active": k == active}
        for k, lab, u in items
    ]


def _crumbs(*labels):
    crumbs = [{"label": "Panel principal", "url": "/panel/"}, {"label": "Centro Gerencial", "url": "/gerencia/"}]
    for lab in labels:
        crumbs.append({"label": lab})
    return crumbs


@login_required
def home(request):
    return redirect("gerencia:intermediacion")


@login_required
def intermediacion(request):
    bu = _bu(request)
    months = int(request.GET.get("months") or 12)
    months = max(1, min(24, months))
    mode = request.GET.get("mode") or "gerencial"
    end = request.GET.get("end") or None
    board = engine.board_intermediacion(bu=bu, months=months, end_period=end, mode=mode)
    return render(
        request,
        "gerencia/intermediacion.html",
        {
            "board": board,
            "nav": _nav("intermediacion"),
            "bu": bu,
            "months": months,
            "mode": mode,
            "end": end or (board.get("end_period") if board else None),
            "chart_json": json.dumps(board.get("chart") or {}),
            "breadcrumbs": _crumbs("Intermediación"),
        },
    )


@login_required
def liquidez(request):
    bu = _bu(request)
    board = engine.board_liquidez(bu=bu)
    return render(
        request,
        "gerencia/liquidez.html",
        {
            "board": board,
            "nav": _nav("liquidez"),
            "bu": bu,
            "chart_json": json.dumps(board.get("chart") or {}),
            "z_json": json.dumps(board.get("z_series") or {}),
            "breadcrumbs": _crumbs("Liquidez"),
        },
    )


@login_required
def estructura(request):
    bu = _bu(request)
    board = engine.board_estructura(bu=bu)
    return render(
        request,
        "gerencia/estructura.html",
        {
            "board": board,
            "nav": _nav("estructura"),
            "bu": bu,
            "chart_fondeo_json": json.dumps(board.get("chart_fondeo") or {}),
            "chart_activos_json": json.dumps(board.get("chart_activos") or {}),
            "chart_deuda_json": json.dumps(board.get("chart_deuda") or {}),
            "breadcrumbs": _crumbs("Estructura"),
        },
    )


@login_required
def comando(request):
    board = engine.board_comando()
    return render(
        request,
        "gerencia/comando.html",
        {
            "board": board,
            "nav": _nav("comando"),
            "breadcrumbs": _crumbs("Comando"),
        },
    )


@login_required
def indices(request):
    bu = _bu(request)
    board = engine.board_indices(bu=bu)
    return render(
        request,
        "gerencia/indices.html",
        {
            "board": board,
            "nav": _nav("indices"),
            "bu": bu,
            "series_json": json.dumps(board.get("series") or {}),
            "breadcrumbs": _crumbs("Índices"),
        },
    )


@login_required
@require_http_methods(["GET", "POST"])
def whatif(request):
    bu = _bu(request)
    drivers = dict(engine.DEFAULT_DRIVERS)
    saved = request.session.pop("gerencia_whatif", None)
    if isinstance(saved, dict):
        drivers.update({k: float(v) for k, v in saved.items() if k in drivers})
    if request.method == "POST":
        for k in drivers:
            if k in request.POST:
                try:
                    drivers[k] = float(request.POST.get(k))
                except (TypeError, ValueError):
                    pass
        if request.POST.get("action") == "save":
            name = (request.POST.get("scenario_name") or "").strip() or "Escenario"
            sc = GerenciaScenario(
                name=name,
                notes=request.POST.get("notes") or "",
                growth_cartera_f=drivers["growth_cartera_f"],
                growth_cartera_l=drivers["growth_cartera_l"],
                rate_activa_f=drivers["rate_activa_f"],
                rate_activa_l=drivers["rate_activa_l"],
                rate_pasiva_inv=drivers["rate_pasiva_inv"],
                rate_pasiva_bancos=drivers["rate_pasiva_bancos"],
                growth_overhead=drivers["growth_overhead"],
                created_by=request.user,
            )
            result = engine.board_whatif(drivers=drivers, bu=bu)
            sc.result_snapshot = {
                "projected": result.get("projected"),
                "deltas": result.get("deltas"),
                "bu": bu,
            }
            sc.save()
            messages.success(request, f"Escenario «{sc.name}» guardado.")
            return redirect("gerencia:whatif")

    board = engine.board_whatif(drivers=drivers, bu=bu)
    scenarios = GerenciaScenario.objects.all()[:12]
    return render(
        request,
        "gerencia/whatif.html",
        {
            "board": board,
            "nav": _nav("whatif"),
            "bu": bu,
            "drivers": drivers,
            "scenarios": scenarios,
            "breadcrumbs": _crumbs("What-if"),
        },
    )


@login_required
def load_scenario(request, pk: int):
    sc = get_object_or_404(GerenciaScenario, pk=pk)
    # Redirect to whatif with query — actually POST-less: store in session
    request.session["gerencia_whatif"] = {
        "growth_cartera_f": sc.growth_cartera_f,
        "growth_cartera_l": sc.growth_cartera_l,
        "rate_activa_f": sc.rate_activa_f,
        "rate_activa_l": sc.rate_activa_l,
        "rate_pasiva_inv": sc.rate_pasiva_inv,
        "rate_pasiva_bancos": sc.rate_pasiva_bancos,
        "growth_overhead": sc.growth_overhead,
    }
    messages.info(request, f"Cargado escenario «{sc.name}».")
    return redirect("gerencia:whatif")


@login_required
def detalle(request):
    bu = _bu(request)
    mode = request.GET.get("mode") or "gerencial"
    trim = engine.board_trimestral(bu=bu, mode=mode)
    idx = engine.board_indices(bu=bu, periods=18)
    inter = engine.board_intermediacion(bu=bu, months=18, mode=mode)
    return render(
        request,
        "gerencia/detalle.html",
        {
            "trim": trim,
            "idx": idx,
            "inter": inter,
            "nav": _nav("detalle"),
            "bu": bu,
            "mode": mode,
            "breadcrumbs": _crumbs("Detalle"),
        },
    )
