"""Pipeline único: WC* mensuales → wcout2d → JSON combinado → Excel integrados."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

from tools.financiero.export_tabla import (
    audit_data_warnings,
    export_financiero_tabla,
    export_financiero_tabla_revision,
)
from tools.financiero.merge_wcout import merge_wcout

CANON_RE = re.compile(r"^(WCF|WCL|WCI|WCS)-(ER|BG)-(\d{4})\.xlsx$", re.I)


@dataclass
class IntegracionResult:
    periods: list[str]
    accounts: int
    wcout_final: Path
    combined_full: Path
    tabla_revision: Path
    vaciado: Path
    warnings_count: int


def default_paths(repo_root: Path | None = None) -> dict[str, Path]:
    root = repo_root or Path(__file__).resolve().parents[2]
    wcg4 = root.parent if root.name == "dashboard" else root
    hub = wcg4 / "integracion-eeff"
    return {
        "repo_root": wcg4,
        "dashboard": wcg4 / "dashboard",
        "tools": wcg4 / "dashboard" / "tools" / "financiero",
        "work_data": wcg4 / "dashboard" / "data" / "wcg" / "financiero",
        "seed": wcg4 / "dashboard" / "risk" / "financiero" / "seed",
        "hub": hub,
        "eeff_source": Path.home() / "download" / "eeff",
        "eeff_output": Path.home() / "download" / "eeff" / "other",
        "structure": hub / "activo" / "plan-cuentas" / "wcsource2512a.xlsx",
        "merge_base": hub / "activo" / "consolidado" / "wcout2d-merge-base.xlsx",
        "wcsource_mirror": wcg4 / "modelo financiero" / "lectura_de_datos_al_modelo" / "wcsource",
    }


def _filter_source_files(source_dir: Path, override_from_yymm: int) -> list[Path]:
    out: list[Path] = []
    for p in sorted(source_dir.glob("*.xlsx")):
        m = CANON_RE.match(p.name)
        if not m:
            continue
        if int(m.group(3)) >= override_from_yymm:
            out.append(p)
    return out


def _stage_source(files: list[Path]) -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="eeff_wcup_"))
    for p in files:
        shutil.copy2(p, tmp / p.name)
    return tmp


def _run_wcup2(tools_dir: Path, structure: Path, input_dir: Path, output: Path) -> None:
    config = tools_dir / "_pipeline_config.txt"
    config.write_text(f"{structure}\n{input_dir}\n{output}\n", encoding="utf-8")
    py = sys.executable
    proc = subprocess.run(
        [py, str(tools_dir / "wcup2.py"), "--config", str(config), "--skip-rename"],
        cwd=str(tools_dir),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"wcup2 falló:\n{proc.stdout}\n{proc.stderr}")


def _run_rebuild(dashboard_root: Path) -> None:
    proc = subprocess.run(
        [sys.executable, str(dashboard_root / "tools" / "financiero" / "rebuild_combined.py")],
        cwd=str(dashboard_root),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"rebuild_combined falló:\n{proc.stdout}\n{proc.stderr}")


def run_integracion(
    *,
    override_from_yymm: int = 2606,
    source_dir: Path | None = None,
    structure: Path | None = None,
    merge_base: Path | None = None,
    work_data: Path | None = None,
    seed: Path | None = None,
    out_tabla: Path | None = None,
    out_vaciado: Path | None = None,
    sync_wcsource_mirror: bool = False,
    promote_merge_base: bool = False,
    repo_root: Path | None = None,
) -> IntegracionResult:
    """Fusiona lote nuevo (yyMM >= override_from) sobre merge-base; exporta worksheets integrados."""
    paths = default_paths(repo_root)
    source_dir = (source_dir or paths["eeff_source"]).expanduser()
    structure = (structure or paths["structure"]).expanduser()
    merge_base = (merge_base or paths["merge_base"]).expanduser()
    work_data = (work_data or paths["work_data"]).expanduser()
    seed = (seed or paths["seed"]).expanduser()
    out_tabla = (out_tabla or paths["eeff_output"] / "estados_financieros_tabla.xlsx").expanduser()
    out_vaciado = (
        out_vaciado or paths["eeff_output"] / "estados-financieros-vaciado-2026-09-16.xlsx"
    ).expanduser()

    if not source_dir.is_dir():
        raise FileNotFoundError(f"Fuente EEFF no existe: {source_dir}")
    if not structure.is_file():
        raise FileNotFoundError(f"Plan de cuentas no existe: {structure}")
    if not merge_base.is_file():
        raise FileNotFoundError(f"Merge-base no existe: {merge_base}")

    files = _filter_source_files(source_dir, override_from_yymm)
    if not files:
        raise ValueError(
            f"No hay archivos WC*-{override_from_yymm}+ en {source_dir} "
            "(nombres canónicos WCF|WCL|WCI|WCS-ER|BG-yyMM.xlsx)"
        )

    work_data.mkdir(parents=True, exist_ok=True)
    staged = _stage_source(files)
    try:
        wcout_new = work_data / "wcout2d_new.xlsx"
        wcout_final = work_data / "wcout2d.xlsx"
        _run_wcup2(paths["tools"], structure, staged, wcout_new)
        merge_wcout(merge_base, wcout_new, wcout_final)
        _run_rebuild(paths["dashboard"])
    finally:
        shutil.rmtree(staged, ignore_errors=True)

    combined_full = work_data / "combined_full.json"
    data = json.loads(combined_full.read_text(encoding="utf-8"))
    warn = audit_data_warnings(data)

    seed.mkdir(parents=True, exist_ok=True)
    for name in ("combined_full.json", "combined_series.json"):
        shutil.copy2(work_data / name, seed / name)
    (seed / "data_warnings.json").write_text(
        json.dumps(warn, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    out_tabla.parent.mkdir(parents=True, exist_ok=True)
    export_financiero_tabla(combined_full, out_vaciado)
    export_financiero_tabla_revision(
        combined_full,
        out_tabla,
        structure_path=structure,
        wcout_path=wcout_final,
        warnings=warn,
    )

    mirror_wcout = (
        paths["repo_root"] / "modelo financiero" / "lectura_de_datos_al_modelo" / "wcout2d.xlsx"
    )
    mirror_wcout.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(wcout_final, mirror_wcout)

    if sync_wcsource_mirror:
        mirror = paths["wcsource_mirror"]
        mirror.mkdir(parents=True, exist_ok=True)
        for p in source_dir.glob("*.xlsx"):
            if CANON_RE.match(p.name):
                shutil.copy2(p, mirror / p.name)

    if promote_merge_base:
        shutil.copy2(wcout_final, merge_base)

    return IntegracionResult(
        periods=list(data.get("periods") or []),
        accounts=len(data.get("accounts") or []),
        wcout_final=wcout_final,
        combined_full=combined_full,
        tabla_revision=out_tabla,
        vaciado=out_vaciado,
        warnings_count=int(warn.get("count") or 0),
    )
