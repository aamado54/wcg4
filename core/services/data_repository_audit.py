"""Auditoría rápida de archivos bajo data/1-pgc … data/5-plal (sin borrar ni mover)."""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from imports.detection import TYPE_LABELS
from core.services.data_layout import (
    YYMM_RANGE,
    classify_file,
    repo_data_root,
    resolve_yymm,
)

AUDIT_MODULE_DIRS: dict[str, str] = {
    "1-pgc": "pgc",
    "2-pgo": "pgo",
    "3-ger": "ger",
    "4-plaf": "plaf",
    "5-plal": "plal",
}

SKIP_NAME_PARTS = ("ejemplo", "ejemplos", "sample")
SKIP_FILENAMES = frozenset({"manifest.json", ".gitkeep", "README.txt", "README.md"})

PGC_HINTS: list[tuple[str, str]] = [
    ("cross_sale", r"venta.*cruzada|ventacruzada"),
    ("new_clients", r"clientes.*nuevo|nuevos.*cliente"),
    ("bank_loans", r"bancos.*fin|capital.*bancos|capitalbancos"),
    ("investment_growth", r"inversiones|crecimiento.*neto|captacion"),
    ("ingresos_pgc", r"ingresos|pga\s*mensual"),
    ("tipo_cambio", r"tipo.*cambio|tipocambio"),
]
PGO_HINTS: list[tuple[str, str]] = [
    ("pgo_catalogo", r"archivos.*pgo|archivospgo"),
    ("pgo_tickets", r"tickets"),
]
GER_HINTS: list[tuple[str, str]] = [
    ("financial", r"\bwc[fils]\b.*\b(er|bg)\b|estados.?financieros"),
    ("risk_leasing", r"baseleasing|base.?leasing"),
    ("risk_rentas", r"leasingrentas|rentas.*leasing"),
    ("gerencial", r"reporte\s*comercial|pga\s*mensual|riesgo|evaluacion"),
    ("crm_clientes", r"crm|wcf\s|wci\s|wcl\s|wcs\s"),
]


@dataclass
class AuditFileRow:
    relpath: str
    module_key: str
    module_logical: str
    folder_yymm: str | None
    import_tipo: str
    tipo_label: str
    yymm: str | None
    yymm_source: str
    expected_tipo: str | None
    flags: list[str] = field(default_factory=list)


def _normalize_compact(text: str) -> str:
    return re.sub(r"[\s_\-\.]+", "", text.lower())


def _should_skip(path: Path) -> bool:
    name = path.name
    if name in SKIP_FILENAMES:
        return True
    lower = name.lower()
    if any(p in lower for p in SKIP_NAME_PARTS):
        return True
    if name.startswith("data-audit-report-"):
        return True
    return False


def expected_tipo_from_name(filename: str, module_logical: str) -> str | None:
    compact = _normalize_compact(filename)
    hints = {
        "pgc": PGC_HINTS,
        "pgo": PGO_HINTS,
        "ger": GER_HINTS,
    }.get(module_logical, [])
    for tipo, pattern in hints:
        if re.search(pattern, compact, re.IGNORECASE):
            return tipo
    if module_logical in ("plaf", "plal"):
        if path_has_institution(filename):
            return "plantilla_institucion"
    return None


def path_has_institution(filename: str) -> bool:
    """PLAF/PLAL: plantillas con nombre de institución."""
    lower = filename.lower()
    if "plantilla" in lower or "planilla" in lower or "analisis-" in lower:
        return True
    if re.search(
        r"\b(banco|banrural|gyt|industrial|agricola|promerica|corporacion|corp\.)\b",
        lower,
    ):
        return True
    return False


def folder_yymm_from_rel(rel_parts: tuple[str, ...]) -> str | None:
    if len(rel_parts) < 2:
        return None
    bucket = rel_parts[1]
    if bucket in YYMM_RANGE:
        return bucket
    return None


def iter_audit_files(root: Path) -> list[AuditFileRow]:
    rows: list[AuditFileRow] = []
    for dir_name, logical in AUDIT_MODULE_DIRS.items():
        module_root = root / dir_name
        if not module_root.is_dir():
            continue
        for path in sorted(module_root.rglob("*")):
            if not path.is_file() or _should_skip(path):
                continue
            rel = path.relative_to(root).parts
            tipo, _module, _lk = classify_file(path.name, rel)
            label = TYPE_LABELS.get(tipo, tipo)
            yymm, yymm_src = resolve_yymm(path)
            folder_yymm = folder_yymm_from_rel(rel)
            expected = expected_tipo_from_name(path.name, logical)
            flags: list[str] = []
            if folder_yymm and yymm and folder_yymm != yymm:
                flags.append(f"carpeta={folder_yymm} ≠ detectado={yymm}")
            elif folder_yymm == "otros" and yymm and yymm in YYMM_RANGE:
                flags.append("organizar: en otros/ pero con YYMM claro")
            if expected and tipo != expected and tipo != "unknown":
                if not (expected == "plantilla_institucion" and tipo == "plantilla"):
                    flags.append(f"tipo: buscado {expected}, hallado {tipo}")
            elif (
                expected
                and tipo == "unknown"
                and expected not in ("plantilla_institucion",)
            ):
                flags.append(f"tipo: buscado {expected}, hallado unknown")
            rows.append(
                AuditFileRow(
                    relpath=path.relative_to(root).as_posix(),
                    module_key=dir_name,
                    module_logical=logical,
                    folder_yymm=folder_yymm,
                    import_tipo=tipo,
                    tipo_label=label,
                    yymm=yymm,
                    yymm_source=yymm_src,
                    expected_tipo=expected,
                    flags=flags,
                )
            )
    return rows


def _is_format_variant(a: str, b: str) -> bool:
    """Mismo archivo en distinto formato (csv vs tsv vs xlsx)."""
    stem_a = Path(a).stem.lower()
    stem_b = Path(b).stem.lower()
    if stem_a == stem_b:
        return True
    na = _normalize_compact(stem_a)
    nb = _normalize_compact(stem_b)
    if na == nb:
        return True
    if na in nb or nb in na:
        return min(len(na), len(nb)) >= 8
    return False


def _group_is_format_variants_only(group: list[AuditFileRow]) -> bool:
    names = [Path(g.relpath).name for g in group]
    if len(names) < 2:
        return False
    base = names[0]
    return all(_is_format_variant(base, other) for other in names[1:])


def find_duplicate_groups(rows: list[AuditFileRow]) -> list[dict]:
    buckets: dict[tuple[str, str, str], list[AuditFileRow]] = defaultdict(list)
    for r in rows:
        key_yymm = r.yymm or r.folder_yymm or "?"
        logical = r.expected_tipo or r.import_tipo
        buckets[(r.module_logical, logical, key_yymm)].append(r)

    dupes: list[dict] = []
    for (mod, logical, yymm), group in sorted(buckets.items()):
        if len(group) < 2:
            continue
        if _group_is_format_variants_only(group):
            continue
        dupes.append(
            {
                "module": mod,
                "logical_tipo": logical,
                "yymm": yymm,
                "files": [g.relpath for g in group],
                "note": "organizar",
            }
        )
    return dupes


def build_audit_markdown(rows: list[AuditFileRow], *, root: Path) -> str:
    dupes = find_duplicate_groups(rows)
    flagged = [r for r in rows if r.flags]
    by_module: dict[str, list[AuditFileRow]] = defaultdict(list)
    for r in rows:
        by_module[r.module_key].append(r)

    today = date.today().isoformat()
    lines = [
        f"# Auditoría data repository — {today}",
        "",
        f"Raíz: `{root}` · Solo módulos: {', '.join(AUDIT_MODULE_DIRS)}",
        "",
        f"| Métrica | Valor |",
        f"| --- | --- |",
        f"| Archivos auditados | {len(rows)} |",
        f"| Con alertas | {len(flagged)} |",
        f"| Grupos duplicados/confusos | {len(dupes)} |",
        "",
    ]

    for mod_key in AUDIT_MODULE_DIRS:
        mod_rows = by_module.get(mod_key, [])
        if not mod_rows:
            lines.extend([f"## `{mod_key}`", "", "_Sin archivos._", ""])
            continue
        by_yymm: dict[str, list[AuditFileRow]] = defaultdict(list)
        for r in mod_rows:
            slot = r.yymm or r.folder_yymm or "sin-yymm"
            by_yymm[slot].append(r)
        lines.append(f"## `{mod_key}` ({len(mod_rows)} archivos)")
        lines.append("")
        for yymm in sorted(by_yymm.keys()):
            chunk = by_yymm[yymm]
            lines.append(f"### {yymm}")
            lines.append("")
            lines.append("| Archivo | Tipo | YYMM (fuente) | Alertas |")
            lines.append("| --- | --- | --- | --- |")
            for r in sorted(chunk, key=lambda x: x.relpath):
                yinfo = f"{r.yymm or '—'} ({r.yymm_source})" if r.yymm else "—"
                alert = "; ".join(r.flags) if r.flags else ""
                lines.append(
                    f"| `{r.relpath}` | {r.import_tipo} | {yinfo} | {alert} |"
                )
            lines.append("")

    if dupes:
        lines.extend(["## Duplicados / copias confusas (organizar)", ""])
        for d in dupes:
            lines.append(
                f"- **{d['module']}** · `{d['logical_tipo']}` · **{d['yymm']}**: "
                + ", ".join(f"`{f}`" for f in d["files"])
            )
        lines.append("")

    if flagged:
        lines.extend(["## Resumen alertas", ""])
        for r in flagged:
            lines.append(f"- `{r.relpath}`: {'; '.join(r.flags)}")
        lines.append("")

    lines.extend(
        [
            "## Comandos útiles",
            "",
            "- `python manage.py audit_data_repository`",
            "- `python manage.py audit_import_status --checklist`",
            "- Importar: hub `/importaciones/` o `import_* --path data/...`",
            "",
        ]
    )
    return "\n".join(lines)


def run_data_repository_audit(
    *,
    root: Path | None = None,
    write_report: bool = True,
    report_date: date | None = None,
) -> tuple[list[AuditFileRow], Path | None]:
    data_root = root or repo_data_root()
    rows = iter_audit_files(data_root)
    report_path = None
    if write_report:
        d = report_date or date.today()
        out_dir = data_root / "done"
        out_dir.mkdir(parents=True, exist_ok=True)
        report_path = out_dir / f"data-audit-report-{d.strftime('%Y%m%d')}.md"
        report_path.write_text(build_audit_markdown(rows, root=data_root), encoding="utf-8")
    return rows, report_path


def data_repository_fingerprint(root: Path) -> tuple[int, float]:
    """Recuento de archivos auditables y mtime máximo (invalidación de caché)."""
    total = 0
    max_mtime = 0.0
    for dir_name in AUDIT_MODULE_DIRS:
        module_root = root / dir_name
        if not module_root.is_dir():
            continue
        for path in module_root.rglob("*"):
            if not path.is_file() or _should_skip(path):
                continue
            total += 1
            try:
                max_mtime = max(max_mtime, path.stat().st_mtime)
            except OSError:
                pass
    return total, max_mtime


def disposition_for_row(
    row: AuditFileRow,
    *,
    duplicate_paths: frozenset[str],
) -> str:
    if row.flags:
        return "Alerta"
    if row.relpath in duplicate_paths:
        return "Organizar"
    return "OK"


def audit_row_to_dict(
    row: AuditFileRow,
    *,
    duplicate_paths: frozenset[str],
) -> dict:
    return {
        "relpath": row.relpath,
        "module_key": row.module_key,
        "module_logical": row.module_logical,
        "folder_yymm": row.folder_yymm or "",
        "import_tipo": row.import_tipo,
        "tipo_label": row.tipo_label,
        "yymm": row.yymm or "",
        "yymm_source": row.yymm_source,
        "expected_tipo": row.expected_tipo or "",
        "flags_text": "; ".join(row.flags),
        "flagged": bool(row.flags),
        "disposition": disposition_for_row(row, duplicate_paths=duplicate_paths),
    }


def build_data_audit_snapshot(root: Path | None = None) -> dict:
    """Datos en memoria para la vista web (sin escribir .md)."""
    data_root = root or repo_data_root()
    rows, _ = run_data_repository_audit(root=data_root, write_report=False)
    dupes = find_duplicate_groups(rows)
    duplicate_paths = frozenset(f for d in dupes for f in d["files"])
    row_dicts = [
        audit_row_to_dict(r, duplicate_paths=duplicate_paths)
        for r in sorted(rows, key=lambda x: x.relpath)
    ]
    flagged = sum(1 for r in rows if r.flags)
    fingerprint = data_repository_fingerprint(data_root)
    return {
        "fingerprint": fingerprint,
        "root": str(data_root),
        "file_count": len(rows),
        "flagged_count": flagged,
        "duplicate_groups_count": len(dupes),
        "rows": row_dicts,
        "dupes": dupes,
        "module_dirs": list(AUDIT_MODULE_DIRS.keys()),
    }