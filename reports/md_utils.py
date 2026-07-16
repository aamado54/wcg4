"""Helpers markdown compactos y seguros para lectores GFM/CommonMark."""

from __future__ import annotations

import re
from typing import Any, Iterable, Sequence

_HEADING_RE = re.compile(r"^#{1,6}\s+")
_TABLE_ROW_RE = re.compile(r"^\|")


def h1(text: str) -> str:
    return f"# {text}"


def h2(text: str) -> str:
    return f"## {text}"


def h3(text: str) -> str:
    return f"### {text}"


def p(text: str) -> str:
    """Bloque de texto. Conserva párrafos; normaliza CRLF → LF."""
    return str(text).replace("\r\n", "\n").replace("\r", "\n").strip()


def bullets(items: Iterable[str]) -> str:
    lines = []
    for item in items:
        if item is None:
            continue
        text = _inline(item)
        if text:
            lines.append(f"- {text}")
    return "\n".join(lines) if lines else "_Sin elementos._"


def _inline(value: Any) -> str:
    """Celda/texto inline: sin saltos de línea ni pipes crudos."""
    if value is None:
        return "—"
    text = str(value).replace("\r\n", "\n").replace("\r", "\n")
    text = " ".join(text.split())
    return text.replace("|", "\\|")


def md_table(headers: Sequence[str], rows: Sequence[Sequence[Any]]) -> str:
    """Tabla GFM (filas unidas por LF; blank lines externas las pone normalize_markdown)."""
    if not headers:
        return ""
    clean_headers = [_inline(h) for h in headers]
    head = "| " + " | ".join(clean_headers) + " |"
    sep = "| " + " | ".join("---" for _ in clean_headers) + " |"
    body = []
    n = len(clean_headers)
    for row in rows:
        cells = [_inline(c) for c in row]
        if len(cells) < n:
            cells.extend(["—"] * (n - len(cells)))
        body.append("| " + " | ".join(cells[:n]) + " |")
    return "\n".join([head, sep, *body])


def ai_closing(
    hechos: Sequence[str],
    cambios: Sequence[str],
    vacios: Sequence[str],
) -> str:
    return join_sections(
        h2("Hechos observables / Cambios relevantes / Vacíos de información"),
        h3("Hechos observables"),
        bullets(hechos or ["Sin hechos suficientes en los datos disponibles."]),
        h3("Cambios relevantes vs período anterior"),
        bullets(cambios or ["Sin período anterior comparable o sin cambios medibles."]),
        h3("Vacíos de información"),
        bullets(vacios or ["No se detectaron vacíos explícitos adicionales."]),
    )


def normalize_markdown(text: str) -> str:
    """
    Garantiza línea en blanco antes de:
    - títulos ATX (# … ######)
    - inicio de tabla GFM (| …)
    También línea en blanco después de títulos cuando sigue contenido.
    """
    text = str(text).replace("\r\n", "\n").replace("\r", "\n")
    raw_lines = text.split("\n")
    out: list[str] = []

    def ends_with_blank() -> bool:
        return not out or out[-1].strip() == ""

    i = 0
    while i < len(raw_lines):
        line = raw_lines[i]
        is_heading = bool(_HEADING_RE.match(line))
        is_table_start = bool(_TABLE_ROW_RE.match(line)) and (
            not out or not _TABLE_ROW_RE.match(out[-1] if out else "")
        )

        if is_heading or is_table_start:
            if out and not ends_with_blank():
                out.append("")

        out.append(line)

        if is_heading:
            # Blank line after heading if next non-empty line is not blank already.
            nxt = raw_lines[i + 1] if i + 1 < len(raw_lines) else None
            if nxt is not None and nxt.strip() != "":
                out.append("")

        i += 1

    # Collapse 3+ consecutive blanks → 1 blank (i.e. max one empty line between blocks).
    collapsed: list[str] = []
    blank_run = 0
    for line in out:
        if line.strip() == "":
            blank_run += 1
            if blank_run <= 1:
                collapsed.append("")
        else:
            blank_run = 0
            collapsed.append(line)

    # Trim leading blanks; ensure trailing single newline.
    while collapsed and collapsed[0] == "":
        collapsed.pop(0)
    while collapsed and collapsed[-1] == "":
        collapsed.pop()
    return "\n".join(collapsed) + "\n"


def join_sections(*sections: str) -> str:
    """
    Une bloques con línea en blanco entre ellos y normaliza el markdown final.
    """
    parts: list[str] = []
    for s in sections:
        if not s:
            continue
        cleaned = str(s).replace("\r\n", "\n").replace("\r", "\n").strip()
        if cleaned:
            parts.append(cleaned)
    return normalize_markdown("\n\n".join(parts))
