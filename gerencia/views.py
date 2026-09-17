import json

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from core.access import risk_gerencia_required

from . import calc as engine
from .calc.money import fmt_money, latest_usd_gtq, unit_label
from .models import GerenciaScenario, GerenciaSettings


def _bu(request) -> str:
    bu = (request.GET.get("bu") or request.POST.get("bu") or "T").upper()
    return bu if bu in ("T", "F", "L") else "T"


def _vista(request) -> str:
    v = (request.GET.get("vista") or "contable").lower()
    return "gerencial" if v == "gerencial" else "contable"


def _ccy(request) -> str:
    c = (request.session.get("gerencia_ccy") or "GTQ").upper()
    return "USD" if c == "USD" else "GTQ"


def _fx(period: str | None = None) -> float | None:
    return latest_usd_gtq(period)


def _strict() -> bool:
    try:
        return bool(GerenciaSettings.get().strict_gerencial)
    except Exception:
        return False


def _nav(active: str) -> list[dict]:
    items = [
        ("intermediacion", "Intermediación", "gerencia:intermediacion", None),
        ("liquidez", "Liquidez", "gerencia:liquidez", None),
        ("estructura", "Estructura", "gerencia:estructura", None),
        ("indices", "Índices", "gerencia:indices", None),
        ("whatif", "What-if", "gerencia:whatif", None),
        ("detalle", "Detalle", "gerencia:detalle", None),
        ("escenarios", "Escenarios", "gerencia:escenarios", "secondary"),
        ("comando", "✦ Comando", "gerencia:comando", "primary"),
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


def _page(request, active: str, **extra):
    ccy = _ccy(request)
    fx = _fx()
    ctx = {
        "nav": _nav(active),
        "ccy": ccy,
        "fx": fx,
        "unit_label": unit_label(ccy),
        "strict_gerencial": _strict(),
        **extra,
    }
    return ctx


@risk_gerencia_required
def home(request):
    return redirect("gerencia:intermediacion")


@risk_gerencia_required
def set_ccy(request):
    ccy = (request.GET.get("ccy") or "GTQ").upper()
    request.session["gerencia_ccy"] = "USD" if ccy == "USD" else "GTQ"
    nxt = request.META.get("HTTP_REFERER") or reverse("gerencia:intermediacion")
    return redirect(nxt)


@risk_gerencia_required
@require_http_methods(["GET", "POST"])
def config(request):
    settings_obj = GerenciaSettings.get()
    if request.method == "POST":
        settings_obj.strict_gerencial = request.POST.get("strict_gerencial") == "on"
        settings_obj.updated_by = request.user
        settings_obj.save()
        messages.success(
            request,
            "Vista gerencial estricta "
            + ("activada." if settings_obj.strict_gerencial else "desactivada."),
        )
        return redirect("gerencia:config")
    return render(
        request,
        "gerencia/config.html",
        _page(
            request,
            "config",
            settings_obj=settings_obj,
            breadcrumbs=_crumbs("Ajustes"),
        ),
    )


@risk_gerencia_required
def intermediacion(request):
    bu = _bu(request)
    months = int(request.GET.get("months") or 12)
    months = max(1, min(36, months))
    mode = request.GET.get("mode") or "gerencial"
    end = request.GET.get("end") or None
    ccy = _ccy(request)
    board = engine.board_intermediacion(
        bu=bu, months=months, end_period=end, mode=mode, ccy=ccy, fx=_fx(end)
    )
    pasivas = engine.board_pasivas_growth(end_period=end or board.get("end_period"), months=months)
    return render(
        request,
        "gerencia/intermediacion.html",
        _page(
            request,
            "intermediacion",
            board=board,
            pasivas_board=pasivas,
            bu=bu,
            months=months,
            mode=mode,
            end=end or (board.get("end_period") if board else None),
            chart_json=json.dumps(board.get("chart") or {}),
            chart_q_json=json.dumps(board.get("chart_quarterly") or {}),
            chart_a_json=json.dumps(board.get("chart_annual") or {}),
            breadcrumbs=_crumbs("Intermediación"),
        ),
    )


@risk_gerencia_required
def liquidez(request):
    bu = _bu(request)
    vista = _vista(request)
    ccy = _ccy(request)
    board = engine.board_liquidez(
        bu=bu, vista=vista, strict=_strict(), ccy=ccy, fx=_fx()
    )
    return render(
        request,
        "gerencia/liquidez.html",
        _page(
            request,
            "liquidez",
            board=board,
            bu=bu,
            vista=vista,
            chart_json=json.dumps(board.get("chart") or {}),
            z_json=json.dumps(board.get("z_series") or {}),
            breadcrumbs=_crumbs("Liquidez"),
        ),
    )


@risk_gerencia_required
def estructura(request):
    bu = _bu(request)
    vista = _vista(request)
    ccy = _ccy(request)
    board = engine.board_estructura(
        bu=bu, vista=vista, strict=_strict(), ccy=ccy, fx=_fx()
    )
    return render(
        request,
        "gerencia/estructura.html",
        _page(
            request,
            "estructura",
            board=board,
            bu=bu,
            vista=vista,
            chart_fondeo_json=json.dumps(board.get("chart_fondeo") or {}),
            chart_activos_json=json.dumps(board.get("chart_activos") or {}),
            chart_deuda_json=json.dumps(board.get("chart_deuda") or {}),
            breadcrumbs=_crumbs("Estructura"),
        ),
    )


@risk_gerencia_required
def escenarios(request):
    return render(
        request,
        "gerencia/escenarios.html",
        _page(
            request,
            "escenarios",
            breadcrumbs=_crumbs("Escenarios"),
        ),
    )


def _parse_escenario_shocks(request) -> dict[str, float]:
    from .calc.escenarios import default_shocks, parse_shock

    base = default_shocks()
    g = request.GET
    return {
        "fx_pct": parse_shock(g.get("fx_pct"), base["fx_pct"]),
        "rates_bp": parse_shock(g.get("rates_bp"), base["rates_bp"]),
        "mora_pct": parse_shock(g.get("mora_pct"), base["mora_pct"]),
        "withdrawals_pct": parse_shock(g.get("withdrawals_pct"), base["withdrawals_pct"]),
        "remittances_pct": parse_shock(g.get("remittances_pct"), base["remittances_pct"]),
        "recovery_pct": parse_shock(g.get("recovery_pct"), base["recovery_pct"]),
        "factoraje_mom_pct": parse_shock(g.get("factoraje_mom_pct"), base["factoraje_mom_pct"]),
    }


@risk_gerencia_required
def escenario_nov2026(request):
    preset = (request.GET.get("preset") or "").strip().lower()
    shocks = _parse_escenario_shocks(request)
    if preset in engine.ESCENARIO_PRESETS:
        for k in shocks:
            if k in engine.ESCENARIO_PRESETS[preset]:
                shocks[k] = float(engine.ESCENARIO_PRESETS[preset][k])
    ccy = _ccy(request)
    fx = _fx("2026-08")
    board = engine.board_escenario_nov2026(shocks=shocks, bu="T", ccy=ccy, fx=fx)
    return render(
        request,
        "gerencia/escenario_nov2026.html",
        _page(
            request,
            "escenarios",
            board=board,
            shocks=shocks,
            preset=preset,
            chart_json=json.dumps(board.get("chart_projection") or {}),
            breadcrumbs=_crumbs("Escenarios", "Noviembre 2026"),
        ),
    )


@risk_gerencia_required
def comando(request):
    board = engine.board_comando()
    return render(
        request,
        "gerencia/comando.html",
        _page(
            request,
            "comando",
            board=board,
            breadcrumbs=_crumbs("Comando"),
        ),
    )


@risk_gerencia_required
def indices(request):
    bu = _bu(request)
    vista = _vista(request)
    board = engine.board_indices(bu=bu, vista=vista, strict=_strict())
    return render(
        request,
        "gerencia/indices.html",
        _page(
            request,
            "indices",
            board=board,
            bu=bu,
            vista=vista,
            series_json=json.dumps(board.get("series") or {}),
            breadcrumbs=_crumbs("Índices"),
        ),
    )


def _whatif_numeric(board: dict) -> list[dict]:
    return list(board.get("raw_rows") or [])


def _compare_rows(prev: dict | None, cur: dict, ccy: str, fx: float | None) -> list[dict]:
    if not prev:
        return []
    prev_map = {r["key"]: r for r in prev.get("raw_rows") or []}
    out = []
    for row in cur.get("raw_rows") or []:
        old = prev_map.get(row["key"]) or {}
        b0, b1 = old.get("base"), row.get("base")
        p0, p1 = old.get("proj"), row.get("proj")
        money = row.get("money")
        if money:
            d_proj = (p1 - p0) if p0 is not None and p1 is not None else None
            out.append(
                {
                    "label": row["label"],
                    "prev_base": fmt_money(b0, ccy, fx),
                    "prev_proj": fmt_money(p0, ccy, fx),
                    "cur_base": fmt_money(b1, ccy, fx),
                    "cur_proj": fmt_money(p1, ccy, fx),
                    "delta_proj": fmt_money(d_proj, ccy, fx) if d_proj is not None else "—",
                }
            )
        else:
            def rx(v):
                return f"{v:.2f}×" if v is not None else "—"

            d_proj = (p1 - p0) if p0 is not None and p1 is not None else None
            out.append(
                {
                    "label": row["label"],
                    "prev_base": rx(b0),
                    "prev_proj": rx(p0),
                    "cur_base": rx(b1),
                    "cur_proj": rx(p1),
                    "delta_proj": f"{d_proj:+.2f}×" if d_proj is not None else "—",
                }
            )
    return out


@risk_gerencia_required
@require_http_methods(["GET", "POST"])
def whatif(request):
    bu = _bu(request)
    ccy = _ccy(request)
    fx = _fx()
    drivers = dict(engine.DEFAULT_DRIVERS)
    saved = request.session.pop("gerencia_whatif", None)
    if isinstance(saved, dict):
        drivers.update({k: float(v) for k, v in saved.items() if k in drivers})
    show_compare = False
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
            result = engine.board_whatif(drivers=drivers, bu=bu, ccy=ccy, fx=fx)
            sc.result_snapshot = {
                "projected": result.get("projected"),
                "deltas": result.get("deltas"),
                "bu": bu,
            }
            sc.save()
            messages.success(request, f"Escenario «{sc.name}» guardado.")
            return redirect("gerencia:whatif")
        if request.POST.get("action") == "run":
            last = request.session.get("gerencia_whatif_last")
            if isinstance(last, dict) and last.get("raw_rows"):
                request.session["gerencia_whatif_prev"] = last
        if request.POST.get("action") == "compare":
            show_compare = True

    board = engine.board_whatif(drivers=drivers, bu=bu, ccy=ccy, fx=fx)
    request.session["gerencia_whatif_last"] = {
        "drivers": drivers,
        "raw_rows": _whatif_numeric(board),
        "bu": bu,
    }
    prev = request.session.get("gerencia_whatif_prev")
    if request.GET.get("compare") == "1":
        show_compare = True
    compare_rows = _compare_rows(prev if isinstance(prev, dict) else None, board, ccy, fx)
    scenarios = GerenciaScenario.objects.all()[:12]
    return render(
        request,
        "gerencia/whatif.html",
        _page(
            request,
            "whatif",
            board=board,
            bu=bu,
            drivers=drivers,
            drivers_pct={k: engine.format_pct(v) for k, v in drivers.items()},
            scenarios=scenarios,
            compare_rows=compare_rows,
            show_compare=show_compare and bool(compare_rows),
            has_prev=bool(compare_rows),
            breadcrumbs=_crumbs("What-if"),
        ),
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
    ccy = _ccy(request)
    fx = _fx()
    trim = engine.board_trimestral(bu=bu, mode=mode)
    idx = engine.board_indices(bu=bu, periods=18, vista=vista, strict=_strict())
    inter = engine.board_intermediacion(bu=bu, months=18, mode=mode, ccy=ccy, fx=fx)
    return render(
        request,
        "gerencia/detalle.html",
        _page(
            request,
            "detalle",
            trim=trim,
            idx=idx,
            inter=inter,
            bu=bu,
            mode=mode,
            vista=vista,
            breadcrumbs=_crumbs("Detalle"),
        ),
    )
