#!/usr/bin/env python3
"""Compara export_verifica_tsv (prod) vs data/ref/verifica.tsv filas 62–121."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

# Índices alineados con pgc/verifica_export.py (sin Django).
ROW_START_2026 = 62
ROW_END_2026 = 121
COL_B_PRES_CLI = 1
COL_D_PRES_COM = 3
COL_F_UEN = 5
COL_G_EXEC_CLI = 6
COL_I_EXEC_COM = 8
COL_S_PTS_ING = 18
COL_T_PTS_CLI = 19
COL_U_PTS_VC = 20
COL_W_TOTAL = 22


def normalize_wc_code(raw: str) -> str:
    wc = (raw or "").strip().upper()
    if wc == "INVESTMENTS":
        return "WCINV"
    return wc

FIELDS = (
    ("pres_cli", COL_B_PRES_CLI, "Clientes presupuesto"),
    ("pres_com", COL_D_PRES_COM, "Comisiones presupuesto"),
    ("exec_cli", COL_G_EXEC_CLI, "Clientes ejecución"),
    ("exec_com", COL_I_EXEC_COM, "Comisiones ejecución"),
    ("pts_ing", COL_S_PTS_ING, "Pts ingresos"),
    ("pts_cli", COL_T_PTS_CLI, "Pts clientes"),
    ("pts_vc", COL_U_PTS_VC, "Pts VC"),
    ("total", COL_W_TOTAL, "Total puntos"),
)

EXPORT_COL = {
    "pres_cli": 2,
    "pres_com": 3,
    "exec_cli": 4,
    "exec_com": 5,
    "pts_ing": 6,
    "pts_cli": 7,
    "pts_vc": 8,
    "total": 9,
}


def parse_num(raw: str) -> Decimal | None:
    if raw is None:
        return None
    s = str(raw).strip()
    if not s or s in ("-", "—", "NO APLICA"):
        return None
    s = re.sub(r"\s+", "", s)
    s = s.replace(",", "")
    if s.startswith("-"):
        neg = True
        s = s[1:].strip()
    else:
        neg = False
    if not s:
        return None
    try:
        v = Decimal(s)
        return -v if neg else v
    except InvalidOperation:
        return None


def nums_close(a: Decimal | None, b: Decimal | None, *, money: bool = False) -> bool:
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    tol = Decimal("0.02") if not money else max(Decimal("1"), abs(a) * Decimal("0.0001"))
    return abs(a - b) <= tol


def ref_row_to_record(row: list[str]) -> dict[str, Decimal | None | str]:
    mes = (row[0] or "").strip()
    uen = normalize_wc_code(row[COL_F_UEN] if len(row) > COL_F_UEN else "")
    rec: dict[str, Decimal | None | str] = {"mes": mes, "uen": uen}
    for key, col, _ in FIELDS:
        rec[key] = parse_num(row[col]) if len(row) > col else None
    return rec


def export_row_to_record(row: list[str]) -> dict[str, Decimal | None | str]:
    mes = (row[0] or "").strip()
    uen = normalize_wc_code(row[1] if len(row) > 1 else "")
    rec: dict[str, Decimal | None | str] = {"mes": mes, "uen": uen}
    for key in EXPORT_COL:
        col_idx = EXPORT_COL[key]
        rec[key] = parse_num(row[col_idx]) if len(row) > col_idx else None
    return rec


def load_ref(path: Path) -> dict[tuple[str, str], dict]:
    out: dict[tuple[str, str], dict] = {}
    with path.open(newline="", encoding="utf-8-sig") as f:
        for i, row in enumerate(csv.reader(f, delimiter="\t"), start=1):
            if i < ROW_START_2026 or i > ROW_END_2026:
                continue
            rec = ref_row_to_record(row)
            key = (str(rec["mes"]), str(rec["uen"]))
            out[key] = rec
    return out


def load_export(path: Path) -> dict[tuple[str, str], dict]:
    out: dict[tuple[str, str], dict] = {}
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader, None)
        if not header:
            raise SystemExit("Export vacío")
        for row in reader:
            if not row or not (row[0] or "").strip():
                continue
            rec = export_row_to_record(row)
            key = (str(rec["mes"]), str(rec["uen"]))
            out[key] = rec
    return out


def month_num(mes: str) -> int | None:
    m = re.match(r"([A-Za-z]{3})-(\d{2})", mes.strip())
    if not m:
        return None
    abbr = m.group(1).lower()
    return {
        "jan": 1,
        "feb": 2,
        "mar": 3,
        "apr": 4,
        "may": 5,
        "jun": 6,
        "jul": 7,
        "aug": 8,
        "sep": 9,
        "oct": 10,
        "nov": 11,
        "dec": 12,
    }.get(abbr)


def classify_field(name: str, ref_v: Decimal | None, exp_v: Decimal | None, month: int | None) -> str:
    if nums_close(ref_v, exp_v, money=name in ("pres_com", "exec_com")):
        return "ok"
    if ref_v is not None and exp_v is not None:
        # Mismo orden de magnitud, solo formato redondeo
        if ref_v != 0 and exp_v != 0:
            ratio = abs(ref_v / exp_v - 1)
            if ratio < Decimal("0.001"):
                return "formato"
        if name in ("pres_com", "exec_com"):
            return "drift_bd_comisiones"
        if month and month >= 10:
            return "mes_vacio_o_futuro"
        return "drift_bd"
    if ref_v is None and exp_v is None:
        return "ok"
    if month and month >= 10:
        return "mes_vacio_o_futuro"
    if ref_v is None and exp_v is not None:
        return "solo_en_bd"
    return "solo_en_ref"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--ref",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "data/ref/verifica.tsv",
    )
    ap.add_argument(
        "--export",
        type=Path,
        required=True,
    )
    args = ap.parse_args()

    ref = load_ref(args.ref)
    exp = load_export(args.export)
    keys = sorted(set(ref) | set(exp), key=lambda k: (month_num(k[0]) or 99, k[1]))

    if len(ref) != 60:
        print(f"AVISO: ref tiene {len(ref)} filas (esperadas 60)", file=sys.stderr)
    if len(exp) != 60:
        print(f"AVISO: export tiene {len(exp)} filas (esperadas 60)", file=sys.stderr)

    match_rows = 0
    mismatch_rows = 0
    causes: dict[str, int] = {}

    print("=== Resumen fila a fila (Mes+UEN) ===\n")
    for key in keys:
        mes, uen = key
        r = ref.get(key)
        e = exp.get(key)
        if r is None or e is None:
            print(f"MISMATCH\t{mes}\t{uen}\tFalta en {'ref' if r is None else 'export'}")
            mismatch_rows += 1
            continue

        mon = month_num(mes)
        uen_no_pts = uen == "WCG"
        bad: list[str] = []
        for key_f, _, label in FIELDS:
            if uen_no_pts and (key_f.startswith("pts_") or key_f == "total"):
                continue
            rv, ev = r[key_f], e[key_f]
            cl = classify_field(key_f, rv, ev, mon)
            if cl != "ok":
                bad.append(f"{label}({cl}: ref={rv} exp={ev})")
                causes[cl] = causes.get(cl, 0) + 1

        if not bad:
            print(f"MATCH\t{mes}\t{uen}")
            match_rows += 1
        else:
            primary = bad[0].split("(")[1].split(":")[0] if "(" in bad[0] else "varios"
            print(f"MISMATCH\t{mes}\t{uen}\t{'; '.join(bad[:4])}")
            mismatch_rows += 1

    print("\n=== Totales ===")
    print(f"MATCH: {match_rows}  MISMATCH: {mismatch_rows}  (ref={len(ref)} export={len(exp)})")
    if causes:
        print("\nCausas (conteo campos):")
        for c, n in sorted(causes.items(), key=lambda x: -x[1]):
            print(f"  {c}: {n}")

    com_only = causes and all(
        k in ("formato", "drift_bd_comisiones", "mes_vacio_o_futuro", "ok") for k in causes
    ) and not any(k.startswith("drift_bd") and k != "drift_bd_comisiones" for k in causes)
    pts_drift = any(k in causes for k in ("drift_bd", "solo_en_bd", "solo_en_ref"))

    print("\n=== Recomendación ===")
    if mismatch_rows == 0:
        print("Cuadre completo. Puedes pasar a Fase 2 / GO con evidencia adjunta.")
    elif com_only and not pts_drift:
        print(
            "Diferencias principalmente en comisiones/formato o meses Oct–Dic vacíos. "
            "Aceptar BD como fuente de verdad para GO, o actualizar data/ref desde este export."
        )
    else:
        print(
            "Hay desvíos en puntos y/o ejecución vs plantilla ref — revisar BD y origen ER "
            "antes de GO; no parece solo formato de comisiones."
        )
    return 0 if mismatch_rows == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())