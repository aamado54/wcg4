"""Inventario y clasificación de archivos bajo data/ (PGC, PGO, GER, PLA, dudas).

Política: nunca borrar; solo mover conservando nombre original.
YYMM = último período detectado en nombre o contenido (no mtime).
"""

from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterator

from django.conf import settings

from imports.detection import TYPE_LABELS, detect_from_name

REORG_YYMM = frozenset(f"26{m:02d}" for m in range(1, 11))  # ene–oct 2026
YYMM_RANGE = frozenset(f"26{m:02d}" for m in range(1, 13))
LAYOUT_MODULES = frozenset({"pgc", "pgo", "ger", "pla", "dudas", "otros"})
YYMM_MODULES = frozenset({"pgc", "pgo", "ger", "pla"})
ROOT_OTROS_MODULE = "otros"
PLANTILLA_STAY_ROOTS = frozenset({"pla", "plaf", "plal"})

MOVE_SKIP_DIR_PARTS = frozenset(
    {
        "audit",
        "reportes",
        "bak",
        "pcg-cierre-ago2026-para-cuadrar",
    }
)

MOVE_SOURCE_ROOTS = frozenset({"now", "done", "new", "tmp"})

PGC_TIPOS = frozenset(
    {
        "new_clients",
        "cross_sale",
        "investment_growth",
        "bank_loans",
        "ingresos_pgc",
        "tipo_cambio",
        "pgc_clientes",
    }
)
PGO_TIPOS = frozenset(
    {
        "pgo_tickets",
        "pgo_catalogo",
        "pgo_expedientes",
    }
)
GER_TIPOS = frozenset(
    {
        "crm_clientes",
        "risk_leasing",
        "risk_rentas",
        "gerencial",
        "financial",
    }
)

LOGICAL_KEYS = {
    "financial": "estados_financieros_er_bg",
    "new_clients": "clientes_nuevos",
    "cross_sale": "venta_cruzada",
    "investment_growth": "inversiones_crecimiento",
    "bank_loans": "bancos_fin_mes",
    "pgo_tickets": "pgo_tickets",
    "pgo_catalogo": "pgo_catalogo",
    "pgo_expedientes": "pgo_expedientes",
    "risk_leasing": "risk_leasing",
    "risk_rentas": "risk_rentas",
    "crm_clientes": "crm_clientes",
    "gerencial": "gerencial",
    "plantilla": "plantilla_externa",
}

YYMM_TOKEN = re.compile(r"(?<!\d)(26(?:0[1-9]|1[0-2]))(?!\d)")
YYYY_MM = re.compile(r"2026[-_](0[1-9]|1[0-2])(?!\d)", re.IGNORECASE)
MONTH_NAME_YY = re.compile(
    r"\b(ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic)(\d{2})\b",
    re.IGNORECASE,
)
EEFF_DASH = re.compile(
    r"wc[flis][\s\-_]*(er|bg)[\s\-_]*26(0[1-9]|1[0-2])",
    re.IGNORECASE,
)
MONTH_MAP = {
    "ene": 1,
    "feb": 2,
    "mar": 3,
    "abr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "ago": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dic": 12,
}
CONTENT_YYYY_MM = re.compile(
    r"20(?:26)[\-_/](0[1-9]|1[0-2])(?!\d)",
    re.IGNORECASE,
)
CONTENT_YYMM = re.compile(r"(?<!\d)(26(?:0[1-9]|1[0-2]))(?!\d)")
SPANISH_MONTHS_IN_TEXT = re.compile(
    r"\b(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|setiembre|"
    r"octubre|noviembre|diciembre)\s*[/\-]?\s*2026\b",
    re.IGNORECASE,
)
SPANISH_MONTH_INDEX = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "setiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12,
}


def repo_data_root() -> Path:
    base = Path(settings.BASE_DIR)
    if (base.parent / "data").is_dir() or base.name == "dashboard":
        return base.parent / "data"
    return base / "data"


def _rel_parts(root: Path, path: Path) -> tuple[str, ...]:
    try:
        return path.relative_to(root).parts
    except ValueError:
        return ()


def is_layout_scaffold_only(rel_parts: tuple[str, ...]) -> bool:
    if not rel_parts:
        return False
    name = rel_parts[-1]
    if name in (".gitkeep", "README.txt", "README.md"):
        return True
    if name == "manifest.json" and len(rel_parts) >= 2 and rel_parts[0] in LAYOUT_MODULES:
        return True
    if name.startswith("data-layout-inventory-"):
        return True
    if name.startswith("data-layout-reorg-"):
        return True
    return False


def should_skip_inventory_path(root: Path, path: Path) -> bool:
    rel = _rel_parts(root, path)
    if not rel:
        return True
    if is_layout_scaffold_only(rel):
        return True
    if rel[0] == "ref":
        return True
    if rel[0] == "done":
        return True
    return False


def _months_from_text(sample: str) -> set[str]:
    found: set[str] = set()
    for m in YYYY_MM.finditer(sample):
        found.add(f"26{int(m.group(1)):02d}")
    for m in CONTENT_YYYY_MM.finditer(sample):
        found.add(f"26{int(m.group(1)):02d}")
    for m in CONTENT_YYMM.finditer(sample):
        y = m.group(1)
        if y in YYMM_RANGE:
            found.add(y)
    for m in YYMM_TOKEN.finditer(sample):
        y = m.group(1)
        if y in YYMM_RANGE:
            found.add(y)
    for m in MONTH_NAME_YY.finditer(sample):
        mon = MONTH_MAP.get(m.group(1).lower())
        if mon and int(m.group(2)) == 26:
            found.add(f"26{mon:02d}")
    for m in SPANISH_MONTHS_IN_TEXT.finditer(sample):
        mon = SPANISH_MONTH_INDEX.get(m.group(1).lower())
        if mon:
            found.add(f"26{mon:02d}")
    return found


def extract_yymm_from_filename(filename: str) -> tuple[str | None, str]:
    name = filename
    compact = re.sub(r"[\s_\-]+", "", name.lower())

    m = EEFF_DASH.search(name)
    if m:
        y = f"26{m.group(2)}"
        if y in YYMM_RANGE:
            return y, "eeff_token"

    m = YYMM_TOKEN.search(name)
    if m:
        y = m.group(1)
        if y in YYMM_RANGE:
            return y, "token_YYMM"

    for m in YYYY_MM.finditer(name):
        mm = int(m.group(1))
        y = f"26{mm:02d}"
        if y in YYMM_RANGE:
            return y, "2026-MM"

    m = re.search(r"baseleasing(?:20)?26(0[1-9]|1[0-2])", compact, re.I)
    if m:
        return f"26{m.group(1)}", "BaseLeasingYYMM"

    m = re.search(r"baseleasing(26(?:0[1-9]|1[0-2]))", compact, re.I)
    if m:
        return m.group(1).lower(), "BaseLeasingYYMM"

    m = re.search(r"baseleasing20(0[1-9]|1[0-2])", compact, re.I)
    if m:
        return f"26{m.group(1)}", "BaseLeasingYYMM"

    m = MONTH_NAME_YY.search(name)
    if m:
        mon = MONTH_MAP.get(m.group(1).lower())
        yr = int(m.group(2))
        if mon and yr == 26:
            return f"26{mon:02d}", "mes_abrev+26"

    m = re.search(r"agosto\s*2026", name, re.I)
    if m:
        return "2608", "mes_nombre"

    m = re.search(r"findemesagosto2026", compact, re.I)
    if m:
        return "2608", "FinDeMes_agosto"

    m = re.search(r"finde?mes(\w+)?2026", compact, re.I)
    if m:
        word = (m.group(1) or "").lower()
        if word in MONTH_MAP:
            return f"26{MONTH_MAP[word]:02d}", "FinDeMes_nombre"

    return None, "sin_YYMM_detectable"


DATE_CELL_2026 = re.compile(
    r"20(?:26)[\-/](0[1-9]|1[0-2])(?:[\-/](0[1-9]|[12]\d|3[01]))?",
    re.IGNORECASE,
)


def _tabular_sample_text(path: Path, max_bytes: int = 256_000) -> str:
    suffix = path.suffix.lower()
    if suffix == ".xlsx":
        try:
            from openpyxl import load_workbook

            wb = load_workbook(path, read_only=True, data_only=True)
            lines: list[str] = []
            for ws in wb.worksheets[:4]:
                for i, row in enumerate(ws.iter_rows(max_row=180, values_only=True)):
                    if i >= 180:
                        break
                    cells = [str(c) for c in row if c is not None]
                    if cells:
                        lines.append(" ".join(cells))
            wb.close()
            return "\n".join(lines)
        except Exception:
            pass
    try:
        raw = path.read_bytes()[:max_bytes]
    except OSError:
        return ""
    if suffix in (".xlsx", ".xls"):
        return raw.decode("latin-1", errors="ignore")
    return raw.decode("utf-8-sig", errors="replace")


def extract_yymm_from_content(path: Path, max_bytes: int = 256_000) -> tuple[str | None, str]:
    """Alias público: yymm_from_content."""
    return yymm_from_content(path, max_bytes=max_bytes)


def yymm_from_content(path: Path, max_bytes: int = 256_000) -> tuple[str | None, str]:
    suffix = path.suffix.lower()
    if suffix not in (".csv", ".tsv", ".txt", ".md", ".xlsx", ".xls"):
        return None, ""
    sample = _tabular_sample_text(path, max_bytes=max_bytes)
    if not sample:
        return None, ""
    months = _months_from_text(sample)
    for m in DATE_CELL_2026.finditer(sample):
        months.add(f"26{int(m.group(1)):02d}")
    months = {m for m in months if m in YYMM_RANGE}
    if not months:
        return None, ""
    last = max(months)
    return last, "contenido_ultimo_periodo"


def resolve_yymm(path: Path) -> tuple[str | None, str]:
    y_fn, src_fn = extract_yymm_from_filename(path.name)
    y_ct, src_ct = yymm_from_content(path)
    candidates: list[tuple[str, str]] = []
    if y_fn:
        candidates.append((y_fn, src_fn))
    if y_ct:
        candidates.append((y_ct, src_ct))
    if not candidates:
        return None, "sin_YYMM_detectable"
    yymm, source = max(candidates, key=lambda t: t[0])
    if y_fn and y_ct and y_fn != y_ct:
        source = f"max({src_fn},{src_ct})"
    return yymm, source


def name_is_verifica_ref(lower: str) -> bool:
    return (
        lower.startswith("verifica")
        or "verifica-export" in lower
        or "verifica-compare" in lower
    )


def _path_is_plantillas(rel: tuple[str, ...]) -> bool:
    return any(p == "plantillas" for p in rel)


def _plantilla_leave_in_place(rel: tuple[str, ...]) -> bool:
    if not rel:
        return False
    if rel[0] in PLANTILLA_STAY_ROOTS:
        return True
    return any(p == "plantillas2026" for p in rel)


def _home_module(tipo: str, module: str) -> str:
    if tipo in PGC_TIPOS:
        return "pgc"
    if tipo in PGO_TIPOS:
        return "pgo"
    if tipo in GER_TIPOS or tipo in ("financial", "gerencial"):
        return "ger"
    if module in YYMM_MODULES:
        return module
    return ROOT_OTROS_MODULE


def _dest_root_otros(filename: str) -> str:
    return f"{ROOT_OTROS_MODULE}/{filename}"


def _is_ops_stay(rel: tuple[str, ...], filename: str) -> bool:
    if rel and rel[0] == "now":
        lower = filename.lower()
        if lower.startswith("_prod_") and lower.endswith(".py"):
            return True
        if lower.endswith((".log",)) and not lower.startswith("import"):
            return True
        if lower in {
            "verifica.tsv",
            "inv_pipeline_jan_aug_rounding.md",
            "sep2026_growth_explain.md",
        }:
            return True
    if "reportes" in rel:
        return True
    return False


def detect_type(
    path: Path,
    rel_parts: tuple[str, ...] | None = None,
) -> tuple[str, str, str | None]:
    """Tipo + módulo destino; prioridad reglas usuario sobre detect_from_name."""
    rel = rel_parts if rel_parts is not None else _rel_parts(repo_data_root(), path)
    return classify_file(path.name, rel)


def classify_file(filename: str, rel_parts: tuple[str, ...] = ()) -> tuple[str, str, str | None]:
    lower = filename.lower()
    compact = re.sub(r"[\s_\-\.]+", "", lower)

    if _plantilla_leave_in_place(rel_parts):
        return "plantilla", "stay", LOGICAL_KEYS["plantilla"]

    if rel_parts and rel_parts[0] == "pla":
        return "plantilla", "stay", LOGICAL_KEYS["plantilla"]

    if _path_is_plantillas(rel_parts) or (
        "plantilla" in lower and lower.endswith((".xlsx", ".zip", ".txt", ".md"))
    ):
        return "plantilla", "pla", LOGICAL_KEYS["plantilla"]

    if "cumplimiento" in lower and "objetivos" in lower:
        return "objetivos_validacion", "stay", "objetivos"

    if name_is_verifica_ref(lower):
        return "verifica", "stay", "verifica"

    if _is_ops_stay(rel_parts, filename):
        return "ops_aux", "stay", None

    if "archivospgo" in compact or (
        "archivos" in lower and "pgo" in lower and lower.endswith((".csv", ".tsv", ".xlsx"))
    ):
        return "pgo_catalogo", "pgo", LOGICAL_KEYS["pgo_catalogo"]

    det = detect_from_name(filename)
    tipo = det.tipo if det else "unknown"

    if "tipocambio" in compact or ("tipo" in lower and "cambio" in lower):
        return "tipo_cambio", "pgc", "tipo_cambio"
    if "ingresos" in lower and "acum" not in lower and not lower.startswith("wc"):
        return "ingresos_pgc", "pgc", "ingresos_pgc"
    if "clientes" in lower and "nuevo" not in lower and "crm" not in lower and "reporte" in lower:
        return "pgc_clientes", "pgc", "pgc_clientes"

    if "evaluacion" in lower and "riesgo" in lower:
        return "gerencial", "ger", "gerencial"
    if "pga mensuales" in lower or "reporte comercial pgo" in lower:
        return "gerencial", "ger", "gerencial"
    if "ingresos acum" in lower or "ejecucion-vs-presupuesto" in lower:
        return "gerencial", "ger", "gerencial"
    if "inversionesfindemes" in compact or "inversiones_finde" in re.sub(r"[\s_]+", "", lower):
        return "investment_growth", "pgc", LOGICAL_KEYS["investment_growth"]
    if "estadosfinancieros" in compact or "estados_financieros" in lower:
        return "financial", "ger", LOGICAL_KEYS["financial"]

    if tipo in PGC_TIPOS:
        if "brief ejecutivo" in lower or "evaluacion-riesgo-clientes-2025" in lower:
            return "gerencial", "ger", "gerencial"
        return tipo, "pgc", LOGICAL_KEYS.get(tipo)
    if tipo in PGO_TIPOS:
        return tipo, "pgo", LOGICAL_KEYS.get(tipo)
    if tipo in GER_TIPOS or (
        tipo == "unknown"
        and any(
            k in lower
            for k in (
                "crm datos",
                "balon datos",
                "leasingrentas",
                "baseleasing",
                "base_leasing",
            )
        )
    ):
        if tipo == "financial":
            return "financial", "ger", LOGICAL_KEYS["financial"]
        if "crm" in lower:
            return "crm_clientes", "ger", LOGICAL_KEYS["crm_clientes"]
        if "rentas" in lower or "leasingrentas" in re.sub(r"[\s_\-]+", "", lower):
            return "risk_rentas", "ger", LOGICAL_KEYS["risk_rentas"]
        if "leasing" in lower:
            return "risk_leasing", "ger", LOGICAL_KEYS["risk_leasing"]
        return "gerencial", "ger", "gerencial"

    if lower.startswith("tickets-") or (
        re.search(r"\btickets\b", lower) and ("2026" in lower or "ticket" in lower)
    ):
        return "pgo_tickets", "pgo", "pgo_tickets"

    if "venta" in lower and "cruzada" in lower:
        return "cross_sale", "pgc", "venta_cruzada"

    if re.match(r"^wc[a-z]?\s", lower) or re.search(r"\bwc[flis]\s+(er|bg)\s+", lower):
        return "financial", "ger", LOGICAL_KEYS["financial"]

    if EEFF_DASH.search(filename):
        return "financial", "ger", LOGICAL_KEYS["financial"]

    if lower.endswith((".py", ".png")) and rel_parts and rel_parts[0] == "now":
        return "ops_aux", "stay", None

    if lower.endswith((".md", ".pdf")) and rel_parts[:1] == ("ref",):
        return "ops_aux", "stay", None

    if tipo == "risk_leasing" or tipo == "risk_rentas" or tipo == "crm_clientes":
        return tipo, "ger", LOGICAL_KEYS.get(tipo, tipo)

    return "unknown", ROOT_OTROS_MODULE, None


def _path_allowed_for_move(rel: tuple[str, ...]) -> bool:
    for part in rel:
        if part in MOVE_SKIP_DIR_PARTS:
            return False
    if "temp" in rel:
        return False
    if "plantillas" in rel:
        return True
    return True


def _dest_bucket(module: str, yymm: str | None, filename: str) -> str:
    bucket = yymm if yymm and yymm in YYMM_RANGE else "otros"
    return f"{module}/{bucket}/{filename}"


def _already_under_layout(rel: tuple[str, ...]) -> tuple[str, str] | None:
    if len(rel) >= 3 and rel[0] in YYMM_MODULES and rel[1] in YYMM_RANGE:
        return rel[0], rel[1]
    if len(rel) >= 3 and rel[0] in YYMM_MODULES and rel[1] == "otros":
        return rel[0], "otros"
    if len(rel) >= 2 and rel[0] in ("pgc", "pgo") and rel[1] in YYMM_RANGE:
        return rel[0], rel[1]
    return None


@dataclass
class InventoryRow:
    relpath: str
    filename: str
    import_tipo: str
    tipo_label: str
    module: str
    yymm: str | None
    yymm_source: str
    action: str
    dest_relpath: str
    ambiguous: bool
    notes: str


def decide_action(
    root: Path,
    path: Path,
    tipo: str,
    module: str,
    yymm: str | None,
    yymm_source: str,
) -> tuple[str, str, bool, list[str]]:
    rel = _rel_parts(root, path)
    notes: list[str] = []
    ambig = False

    if module == "stay":
        return "stay", "", False, ["política: no mover"]

    if path.name.startswith("manifest_") and path.suffix == ".json":
        return "stay", "", False, ["manifest_ops"]

    if module == ROOT_OTROS_MODULE:
        dest = _dest_root_otros(path.name)
        placed = _already_under_layout(rel)
        if rel and rel[0] == ROOT_OTROS_MODULE and len(rel) == 2:
            return "already_yymm", "/".join(rel), False, ["ya_en_otros"]
        if placed and placed[0] in YYMM_MODULES:
            return "move_otros", dest, False, notes + ["sin_clasificar_en_módulo"]
        if rel and rel[0] == "dudas":
            return "move_otros", dest, False, notes + ["dudas→otros"]
        if rel and rel[0] in MOVE_SOURCE_ROOTS:
            return "move_otros", dest, False, notes + ["revisión_humana"]
        if placed:
            return "move_otros", dest, False, notes + ["reclasificar"]
        return "inventory_only", dest, False, notes

    if module == "pla":
        if "plantillas" in rel:
            idx = rel.index("plantillas")
            sub = "/".join(rel[idx + 1 :])
            dest = f"pla/otros/{sub}" if sub else f"pla/otros/{path.name}"
        elif yymm:
            dest = _dest_bucket("pla", yymm, path.name)
        else:
            dest = f"pla/otros/{path.name}"
        if rel and (rel[0] in MOVE_SOURCE_ROOTS or "plantillas" in rel):
            if rel[0] == "pla" and dest.endswith(path.name):
                return "already_yymm", "/".join(rel), False, notes + ["ya_en_pla"]
            return "move_pla", dest, False, notes + ["plantilla_externa"]
        return "inventory_only", dest, False, notes

    if yymm and yymm not in REORG_YYMM:
        if rel[0] in YYMM_MODULES and rel[1] not in REORG_YYMM:
            return "already_yymm", "/".join(rel), False, ["fuera_paso_ene-oct"]
        notes.append(f"YYMM={yymm}_fuera_paso")
        if module in YYMM_MODULES:
            dest = _dest_bucket(module, yymm, path.name)
            return "move_yymm", dest, True, notes

    if not yymm or yymm not in YYMM_RANGE:
        notes.append(yymm_source)
        if path.suffix.lower() in (".csv", ".tsv", ".xlsx", ".xls"):
            notes.append("content_scan_recomendado")
        if module == "dudas" or ambig:
            return "move_dudas", f"dudas/{path.name}", True, notes
        if module == ROOT_OTROS_MODULE:
            return "move_otros", _dest_root_otros(path.name), False, notes
        if module in YYMM_MODULES:
            return "move_otros", f"{module}/otros/{path.name}", not bool(yymm), notes

    if yymm_source == "mes_abrev+26":
        ambig = True
        notes.append("mes en texto; revisar")

    all_tokens = YYMM_TOKEN.findall(path.name)
    unique = sorted(set(all_tokens))
    if len(unique) > 1:
        ambig = True
        notes.append(f"multi_YYMM={','.join(unique)}")

    if yymm_source.startswith("contenido") and extract_yymm_from_filename(path.name)[0]:
        fn_y, _ = extract_yymm_from_filename(path.name)
        if fn_y and fn_y != yymm:
            notes.append(f"contenido({yymm})!=nombre({fn_y})")

    placed = _already_under_layout(rel)
    home = _home_module(tipo, module)
    if placed and rel[-1] == path.name:
        if home == ROOT_OTROS_MODULE and placed[0] in YYMM_MODULES:
            return (
                "move_otros",
                _dest_root_otros(path.name),
                False,
                notes + [f"no_encaja_en_{placed[0]}"],
            )
        if (
            yymm
            and placed[1] == yymm
            and home in YYMM_MODULES
            and placed[0] != home
            and not ambig
        ):
            dest = _dest_bucket(home, yymm, path.name)
            return (
                "move_yymm",
                dest,
                False,
                notes + [f"corrección_módulo_{placed[0]}→{home}"],
            )
        if placed[1] == yymm and placed[0] == home:
            return "already_yymm", "/".join(rel), False, notes + ["ya_en_YYMM"]

    movable = (
        tipo in PGC_TIPOS
        or tipo in PGO_TIPOS
        or tipo in GER_TIPOS
        or tipo == "plantilla"
        or tipo == "gerencial"
    )
    if (
        placed
        and len(rel) >= 2
        and rel[-1] == path.name
        and placed[1] == "otros"
        and yymm
        and yymm in REORG_YYMM
        and home == placed[0]
        and movable
        and not ambig
    ):
        dest = _dest_bucket(home, yymm, path.name)
        return "move_yymm", dest, False, notes + ["bucket_otros→YYMM"]

    if rel and rel[0] == ROOT_OTROS_MODULE and len(rel) == 2:
        if (
            home in YYMM_MODULES
            and yymm
            and yymm in REORG_YYMM
            and movable
            and not ambig
        ):
            dest = _dest_bucket(home, yymm, path.name)
            return "move_yymm", dest, False, notes + ["data_otros→módulo"]

    in_source = rel and rel[0] in MOVE_SOURCE_ROOTS and _path_allowed_for_move(rel)
    in_eeff = "eeff" in rel and "bak" not in rel
    in_tmp_eeff = rel[:2] == ("tmp", "eeff-source-2026") if len(rel) >= 2 else False
    in_wrong_bucket = bool(
        placed and home in YYMM_MODULES and placed[0] != home and yymm
    )
    in_dudas_nested = rel[:2] == ("dudas", "otros") if len(rel) >= 2 else False

    if yymm and not ambig and movable and (
        in_source or in_eeff or in_tmp_eeff or in_wrong_bucket or in_dudas_nested
    ):
        dest = _dest_bucket(home, yymm, path.name)
        if home == "pla":
            return "move_pla", dest, False, notes
        return "move_yymm", dest, False, notes

    if rel and rel[0] == "dudas":
        if in_dudas_nested and module == ROOT_OTROS_MODULE:
            return (
                "move_otros",
                _dest_root_otros(path.name),
                False,
                notes + ["dudas_otros→data_otros"],
            )
        if (
            yymm
            and home in YYMM_MODULES
            and not ambig
            and tipo in (PGC_TIPOS | PGO_TIPOS | GER_TIPOS | {"gerencial", "financial"})
        ):
            dest = _dest_bucket(home, yymm, path.name)
            return "move_yymm", dest, False, notes + ["dudas→módulo"]
        if len(rel) == 2 and rel[1] != "otros":
            if module == ROOT_OTROS_MODULE:
                return "move_otros", _dest_root_otros(path.name), False, notes
            return "inventory_only", "/".join(rel), False, notes + ["cola_revision"]
        if len(rel) >= 3 and rel[1] == "otros":
            if module == ROOT_OTROS_MODULE:
                return "move_otros", _dest_root_otros(path.name), False, notes
            if yymm and home in YYMM_MODULES and not ambig and movable:
                dest = _dest_bucket(home, yymm, path.name)
                return "move_yymm", dest, False, notes + ["dudas_otros→módulo"]
            return "inventory_only", "/".join(rel), False, notes + ["cola_revision"]
        if len(rel) >= 3 and rel[1] in YYMM_RANGE:
            flat = f"dudas/{path.name}"
            if "/".join(rel) == flat:
                return "inventory_only", flat, False, notes
            return "move_dudas", flat, False, notes + ["dudas_sin_YYMM"]

    if ambig and yymm:
        dest = f"dudas/{path.name}"
        if in_source or in_eeff or in_tmp_eeff:
            return "move_dudas", dest, True, notes + ["ambiguo"]
        return "inventory_only", dest, True, notes

    if in_source and tipo not in ("objetivos_validacion", "verifica", "ops_aux"):
        if module == "ger" and yymm:
            return "move_yymm", _dest_bucket("ger", yymm, path.name), False, notes
        if module == "ger":
            return "move_yymm", f"ger/otros/{path.name}", True, notes + ["ger_sin_YYMM"]

    return "inventory_only", "", ambig, notes + ["sin_mv_automático"]


def iter_data_files(root: Path) -> Iterator[Path]:
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        if should_skip_inventory_path(root, p):
            continue
        yield p


def inventory_rows(root: Path) -> list[InventoryRow]:
    rows: list[InventoryRow] = []
    for path in iter_data_files(root):
        rel = path.relative_to(root)
        relpath = rel.as_posix()
        rel_parts = rel.parts
        tipo, module, _lk = classify_file(path.name, rel_parts)
        label = TYPE_LABELS.get(tipo, tipo)
        yymm, yymm_src = resolve_yymm(path)
        action, dest, ambig, note_list = decide_action(root, path, tipo, module, yymm, yymm_src)
        rows.append(
            InventoryRow(
                relpath=relpath,
                filename=path.name,
                import_tipo=tipo,
                tipo_label=label,
                module=module,
                yymm=yymm,
                yymm_source=yymm_src,
                action=action,
                dest_relpath=dest,
                ambiguous=ambig,
                notes="; ".join(note_list),
            )
        )
    return rows


def write_inventory_report(
    rows: list[InventoryRow],
    base_path: Path,
    fmt: str = "both",
) -> list[Path]:
    base_path.parent.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    tsv_path = base_path if base_path.suffix == ".tsv" else base_path.with_suffix(".tsv")
    if fmt in ("tsv", "both"):
        lines = [
            "\t".join(
                [
                    "relpath",
                    "filename",
                    "import_tipo",
                    "module",
                    "yymm",
                    "yymm_source",
                    "action",
                    "dest_relpath",
                    "ambiguous",
                    "notes",
                ]
            )
        ]
        for r in rows:
            lines.append(
                "\t".join(
                    [
                        r.relpath,
                        r.filename,
                        r.import_tipo,
                        r.module,
                        r.yymm or "",
                        r.yymm_source,
                        r.action,
                        r.dest_relpath,
                        "yes" if r.ambiguous else "no",
                        r.notes.replace("\t", " "),
                    ]
                )
            )
        tsv_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        written.append(tsv_path)

    if fmt in ("md", "both"):
        md_path = tsv_path.with_suffix(".md")
        move_actions = {"move_yymm", "move_pla", "move_dudas"}
        chunks = [
            f"# Inventario layout data — {date.today().isoformat()}",
            "",
            f"Total archivos: **{len(rows)}**",
            "",
            f"| move_yymm/pla claro | {sum(1 for r in rows if r.action in ('move_yymm', 'move_pla') and not r.ambiguous)} |",
            f"| move_dudas | {sum(1 for r in rows if r.action == 'move_dudas')} |",
            f"| move_otros | {sum(1 for r in rows if r.action == 'move_otros')} |",
            f"| stay | {sum(1 for r in rows if r.action == 'stay')} |",
            "",
        ]
        chunks.append("## Movimientos YYMM propuestos (no ambiguos)")
        chunks.append("")
        chunks.append("| origen | destino | tipo | módulo | YYMM |")
        chunks.append("|--------|---------|------|--------|------|")
        for r in rows:
            if r.ambiguous or r.action not in ("move_yymm", "move_pla"):
                continue
            chunks.append(
                f"| `{r.relpath}` | `data/{r.dest_relpath}` | {r.import_tipo} | {r.module} | {r.yymm} |"
            )
        md_path.write_text("\n".join(chunks) + "\n", encoding="utf-8")
        written.append(md_path)
    return written


def _manifest_entry(row: InventoryRow, *, previous_relpath: str) -> dict:
    year = 2000 + int(row.yymm[0:2]) if row.yymm else 2026
    month = int(row.yymm[2:4]) if row.yymm else 1
    rel_dest = row.dest_relpath
    return {
        "logical_key": LOGICAL_KEYS.get(row.import_tipo, row.import_tipo),
        "path": f"data/{rel_dest}",
        "original_name": row.filename,
        "file_type": row.import_tipo.upper(),
        "covers_months": [[year, month]],
        "previous_path": f"data/{previous_relpath}",
        "imported_at": None,
        "file_upload_id": None,
    }


def _remove_manifest_entry(root: Path, module: str, yymm: str, filename: str) -> None:
    manifest_path = root / module / yymm / "manifest.json"
    if not manifest_path.is_file():
        return
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return
    files = data.get("files", [])
    new_files = [f for f in files if f.get("original_name") != filename]
    if len(new_files) == len(files):
        return
    data["files"] = new_files
    manifest_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _update_manifest_after_move(
    root: Path, row: InventoryRow, *, previous_relpath: str, extra_note: str = ""
) -> None:
    parts = Path(row.dest_relpath).parts
    if len(parts) < 2 or parts[0] not in ("pgc", "pgo", "ger"):
        return
    yymm = parts[1]
    if yymm not in YYMM_RANGE:
        return
    manifest_path = root / parts[0] / yymm / "manifest.json"
    if not manifest_path.is_file():
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(
            json.dumps(
                {
                    "period": {"year": 2000 + int(yymm[:2]), "month": int(yymm[2:])},
                    "module": parts[0],
                    "files": [],
                },
                indent=2,
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    files = data.setdefault("files", [])
    entry = _manifest_entry(row, previous_relpath=previous_relpath)
    if extra_note:
        entry["layout_note"] = extra_note
    keys = {f.get("original_name") for f in files}
    if row.filename not in keys:
        files.append(entry)
    else:
        for f in files:
            if f.get("original_name") == row.filename:
                f.setdefault("layout_note", extra_note or "duplicado_manifest")
                f["previous_path"] = f"data/{previous_relpath}"
    manifest_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _collision_dest(root: Path, row: InventoryRow, existing: Path) -> Path:
    rel = Path(row.relpath)
    parent_tag = rel.parent.name.replace(" ", "_")
    if parent_tag in YYMM_RANGE:
        parent_tag = rel.parent.parent.name.replace(" ", "_") if len(rel.parts) > 1 else ""
    alt_name = f"dup_{parent_tag}__{row.filename}" if parent_tag else f"dup__{row.filename}"
    candidate = root / "dudas" / alt_name
    n = 0
    while candidate.exists():
        n += 1
        candidate = root / "dudas" / f"dup{n}__{row.filename}"
    return candidate


MOVABLE_ACTIONS = frozenset({"move_yymm", "move_pla", "move_dudas", "move_otros"})
DEFAULT_APPLY_ACTIONS = frozenset({"move_yymm", "move_pla", "move_otros"})


def apply_moves(
    root: Path,
    rows: list[InventoryRow] | None = None,
    *,
    dry_run: bool = True,
    include_ambiguous: bool = False,
    limit: int | None = None,
) -> dict:
    if rows is None:
        rows = inventory_rows(root)
    done = 0
    skipped = 0
    errors: list[str] = []
    collisions: list[str] = []
    moved: list[tuple[str, str]] = []

    candidates = [
        r
        for r in rows
        if r.action in DEFAULT_APPLY_ACTIONS and not r.ambiguous
    ]
    if include_ambiguous:
        candidates += [
            r
            for r in rows
            if r.action in MOVABLE_ACTIONS and r not in candidates
        ]

    for row in candidates:
        if limit is not None and done >= limit:
            break
        if not row.dest_relpath:
            skipped += 1
            continue
        src = root / row.relpath
        dest = root / row.dest_relpath
        if not src.is_file():
            skipped += 1
            continue
        try:
            if src.resolve() == dest.resolve():
                skipped += 1
                continue
        except OSError:
            pass
        final_dest = dest
        note = ""
        if dest.exists():
            final_dest = _collision_dest(root, row, dest)
            note = f"colisión con data/{row.dest_relpath}"
            collisions.append(f"{row.relpath} → {final_dest.relative_to(root)} ({note})")
            row = InventoryRow(
                **{**row.__dict__, "dest_relpath": final_dest.relative_to(root).as_posix(), "module": "dudas"}
            )
        final_dest.parent.mkdir(parents=True, exist_ok=True)
        if dry_run:
            done += 1
            moved.append((row.relpath, row.dest_relpath))
            continue
        prev = row.relpath
        prev_parts = Path(prev).parts
        if (
            len(prev_parts) >= 2
            and prev_parts[0] in YYMM_MODULES
            and prev_parts[1] in YYMM_RANGE
        ):
            dest_parts = Path(row.dest_relpath).parts
            if len(dest_parts) >= 2 and (
                dest_parts[0] != prev_parts[0] or dest_parts[1] != prev_parts[1]
            ):
                _remove_manifest_entry(
                    root, prev_parts[0], prev_parts[1], src.name
                )
        shutil.move(str(src), str(final_dest))
        if row.action in ("move_yymm", "move_pla") or note:
            _update_manifest_after_move(root, row, previous_relpath=prev, extra_note=note)
        done += 1
        moved.append((prev, row.dest_relpath))

    return {
        "done": done,
        "skipped": skipped,
        "errors": errors,
        "collisions": collisions,
        "moved": moved,
    }


def _collision_count(apply_result: dict) -> int:
    coll = apply_result.get("collisions", [])
    return coll if isinstance(coll, int) else len(coll)


def write_reorg_summary(root: Path, rows: list[InventoryRow], apply_result: dict) -> Path:
    out = root / "done" / f"data-layout-reorg-{date.today().strftime('%Y%m%d')}.md"
    counts: dict[str, int] = {}
    for mod in ("pgc", "pgo", "ger", "pla", "dudas"):
        mod_root = root / mod
        if mod_root.is_dir():
            counts[mod] = sum(1 for p in mod_root.rglob("*") if p.is_file() and p.name != "manifest.json")
    dudas_files = sorted(
        p.relative_to(root).as_posix()
        for p in (root / "dudas").rglob("*")
        if p.is_file() and p.name != "manifest.json"
    ) if (root / "dudas").is_dir() else []

    lines = [
        f"# Reorganización layout data — {date.today().isoformat()}",
        "",
        "Alcance **2601–2610** (ene–oct 2026). Política: solo `mv`, sin borrar.",
        "",
        "## Conteo por módulo (archivos, sin manifest.json)",
        "",
    ]
    for mod, n in sorted(counts.items()):
        lines.append(f"- **{mod}/**: {n}")
    lines.extend(
        [
            "",
            f"## Aplicación ({'dry-run' if apply_result.get('dry_run') else 'apply'})",
            "",
            f"- Movimientos planificados/ejecutados: **{apply_result.get('done', 0)}**",
            f"- Omitidos: **{apply_result.get('skipped', 0)}**",
            f"- Colisiones → dudas/: **{_collision_count(apply_result)}**",
            "",
        ]
    )
    if apply_result.get("collisions"):
        lines.append("### Colisiones")
        lines.append("")
        for c in apply_result["collisions"][:80]:
            lines.append(f"- {c}")
        lines.append("")

    amb = [r for r in rows if r.action == "move_dudas" or r.ambiguous]
    lines.append(f"## Inventario ambiguo / dudas ({len(amb)} filas)")
    lines.append("")
    for r in amb[:60]:
        lines.append(f"- `{r.relpath}` → `{r.dest_relpath or '—'}` ({r.notes})")
    if len(amb) > 60:
        lines.append(f"- … y {len(amb) - 60} más")
    lines.extend(["", "## Archivos en data/dudas/", ""])
    if dudas_files:
        for p in dudas_files[:100]:
            lines.append(f"- `{p}`")
    else:
        lines.append("- (vacío)")
    lines.append("")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def _count_by_month(root: Path, module: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    mod_root = root / module
    if not mod_root.is_dir():
        return counts
    for p in mod_root.rglob("*"):
        if not p.is_file() or p.name == "manifest.json":
            continue
        if p.name == "README.txt":
            continue
        rel = p.relative_to(mod_root).parts
        if module == ROOT_OTROS_MODULE and len(rel) == 1:
            counts["(raíz)"] = counts.get("(raíz)", 0) + 1
            continue
        if not rel:
            continue
        bucket = rel[0]
        if bucket in YYMM_RANGE or bucket == "otros":
            counts[bucket] = counts.get(bucket, 0) + 1
    return counts


def write_reclass_report(
    root: Path,
    rows: list[InventoryRow],
    apply_result: dict,
    *,
    report_name: str | None = None,
) -> Path:
    stem = report_name or f"data-layout-reclass-{date.today().strftime('%Y%m%d')}"
    out = root / "done" / f"{stem}.md"
    out.parent.mkdir(parents=True, exist_ok=True)

    by_module_month: dict[str, dict[str, int]] = {}
    for mod in ("pgc", "pgo", "ger", ROOT_OTROS_MODULE):
        by_module_month[mod] = _count_by_month(root, mod)

    content_scan = [
        r
        for r in rows
        if "content_scan_recomendado" in r.notes
        or r.yymm_source.startswith("contenido")
        or (
            not r.yymm
            and r.filename.lower().endswith((".csv", ".tsv", ".xlsx", ".xls"))
        )
    ]

    lines = [
        f"# Reclasificación layout data — {date.today().isoformat()}",
        "",
        "Política: PGC (clientes, nuevos, ingresos, TC, bancos, venta cruzada); "
        "PGO (ArchivosPGO*); GER (ER/BG/WCF estados); no clasificados → `data/otros/`. "
        "YYMM = máximo entre nombre y contenido (no mtime). Plantillas `pla/`, `plaf`, `plal`, "
        "`plantillas2026` sin mover.",
        "",
        "## Conteo por módulo y mes (sin manifest.json)",
        "",
        "| Módulo | Bucket | Archivos |",
        "|--------|--------|----------|",
    ]
    for mod in ("pgc", "pgo", "ger", ROOT_OTROS_MODULE):
        buckets = by_module_month.get(mod, {})
        if not buckets:
            lines.append(f"| {mod}/ | — | 0 |")
            continue
        for bucket, n in sorted(buckets.items()):
            lines.append(f"| {mod}/ | {bucket} | {n} |")

    lines.extend(
        [
            "",
            "## Aplicación",
            "",
            f"- Modo: **{'dry-run' if apply_result.get('dry_run') else 'apply'}**",
            f"- Movimientos: **{apply_result.get('done', 0)}**",
            f"- Omitidos: **{apply_result.get('skipped', 0)}**",
            f"- Colisiones: **{_collision_count(apply_result)}**",
            "",
            "### Acciones en inventario",
            "",
        ]
    )
    action_counts: dict[str, int] = {}
    for r in rows:
        action_counts[r.action] = action_counts.get(r.action, 0) + 1
    for action, n in sorted(action_counts.items()):
        lines.append(f"- `{action}`: {n}")

    lines.extend(["", "## Archivos con YYMM desde contenido o scan pendiente", ""])
    if content_scan:
        for r in content_scan[:80]:
            lines.append(
                f"- `{r.relpath}` — yymm={r.yymm or '—'} ({r.yymm_source}) [{r.notes}]"
            )
        if len(content_scan) > 80:
            lines.append(f"- … y {len(content_scan) - 80} más")
    else:
        lines.append("- (ninguno)")

    lines.append("")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out