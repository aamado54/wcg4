import json

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from core.access import risk_gerencia_required

from . import calc as engine
from .models import GerenciaScenario


def _bu(request) -> str:
    bu = (request.GET.get("bu") or request.POST.get("bu") or "T").upper()
    return bu if bu in ("T", "F", "L") else "T"


def _vista(request) -> str:
    v = (request.GET.get("vista") or "contable").lower()
    return "gerencial" if v == "gerencial" else "contable"


def _nav(active: str) -> list[dict]:
    items = [
        ("intermediacion", "Intermediación", "gerencia:intermediacion", False),
        ("liquidez", "Liquidez", "gerencia:liquidez", False),
        ("estructura", "Estructura", "gerencia:estructura", False),
        ("indices", "Índices", "gerencia:indices", False),
        ("whatif", "What-if", "gerencia:whatif", False),
        ("detalle", "Detalle", "gerencia:detalle", False),
        ("comando", "✦ Comando", "gerencia:comando", True),
    ]
    return [
        {"key": k, "label": lab, "url_name": u, "active": k == active, "launch": launch}
        for k, lab, u, launch in items
    ]


def _crumbs(*labels):
    crumbs = [
        {"label": "Panel principal", "url": "/panel/"},
        {"label": "Centro Gerencial", "url": "/gerencia/"},
    ]
    for lab in labels:
        crumbs.append({"label": lab})
    return crumbs


@risk_gerencia_required
def home(request):
    return redirect("gerencia:intermediacion")


@risk_gerencia_required
def intermediacion(request):
    bu = _bu(request)
    months = int(request.GET.get("months") or 12)
    months = max(1, min(36, months))
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
            "chart_q_json": json.dumps(board.get("chart_quarterly") or {}),
            "chart_a_json": json.dumps(board.get("chart_annual") or {}),
            "breadcrumbs": _crumbs("Intermediación"),
        },
    )


@risk_gerencia_required
def liquidez(request):
    bu = _bu(request)
    vista = _vista(request)
    board = engine.board_liquidez(bu=bu, vista=vista)
    return render(
        request,
        "gerencia/liquidez.html",
        {
            "board": board,
            "nav": _nav("liquidez"),
            "bu": bu,
            "vista": vista,
            "chart_json": json.dumps(board.get("chart") or {}),
            "z_json": json.dumps(board.get("z_series") or {}),
            "breadcrumbs": _crumbs("Liquidez"),
        },
    )


@risk_gerencia_required
def estructura(request):
    bu = _bu(request)
    vista = _vista(request)
    board = engine.board_estructura(bu=bu, vista=vista)
    return render(
        request,
        "gerencia/estructura.html",
        {
            "board": board,
            "nav": _nav("estructura"),
            "bu": bu,
            "vista": vista,
            "chart_fondeo_json": json.dumps(board.get("chart_fondeo") or {}),
            "chart_activos_json": json.dumps(board.get("chart_activos") or {}),
            "chart_deuda_json": json.dumps(board.get("chart_deuda") or {}),
            "breadcrumbs": _crumbs("Estructura"),
        },
    )


@risk_gerencia_required
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


@risk_gerencia_required
def indices(request):
    bu = _bu(request)
    vista = _vista(request)
    board = engine.board_indices(bu=bu, vista=vista)
    return render(
        request,
        "gerencia/indices.html",
        {
            "board": board,
            "nav": _nav("indices"),
            "bu": bu,
            "vista": vista,
            "series_json": json.dumps(board.get("series") or {}),
            "breadcrumbs": _crumbs("Índices"),
        },
    )


@risk_gerencia_required
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
                drivers[k] = engine.parse_pct(request.POST.get(k), drivers[k])
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
            "drivers_pct": {k: engine.format_pct(v) for k, v in drivers.items()},
            "scenarios": scenarios,
            "breadcrumbs": _crumbs("What-if"),
        },
    )


@risk_gerencia_required
def load_scenario(request, pk: int):
    sc = get_object_or_404(GerenciaScenario, pk=pk)
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


@risk_gerencia_required
def detalle(request):
    bu = _bu(request)
    mode = request.GET.get("mode") or "gerencial"
    vista = _vista(request)
    trim = engine.board_trimestral(bu=bu, mode=mode)
    idx = engine.board_indices(bu=bu, periods=18, vista=vista)
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
            "vista": vista,
            "breadcrumbs": _crumbs("Detalle"),
        },
    )
