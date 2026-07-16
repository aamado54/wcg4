from pathlib import Path
import re
from collections import defaultdict

from pathlib import Path
import re
import shutil
from collections import defaultdict

OUTDIR = Path("output")

def reset_output_dir():
    if OUTDIR.exists():
        shutil.rmtree(OUTDIR)
    OUTDIR.mkdir(parents=True, exist_ok=True)
  
def is_root_level_path(path_str: str) -> bool:
    return len(Path(path_str).parts) == 1

def is_migration_path(path_str: str) -> bool:
    parts = Path(path_str).parts
    return "migrations" in parts

# --- Descubrimiento dinámico de inputs --- #

def discover_inputs():
    paths = []

    # Todas las partes de python
    python_parts = sorted(Path(".").glob("all_python_scripts.part-*.md"))
    paths.extend(python_parts)

    # Todas las partes de HTML (nuevo esquema)
    html_parts = sorted(Path(".").glob("all_html_templates.part-*.md"))
    if html_parts:
        paths.extend(html_parts)
    else:
        # Fallback a nombre viejo monolítico
        old = Path("all_html_templates.md")
        if old.exists():
            paths.append(old)

    if not paths:
        print("ADVERTENCIA: no se encontraron archivos all_*_scripts / all_*_templates")
    else:
        print("Archivos de entrada detectados:")
        for p in paths:
            print(f" - {p}")

    return paths

INPUTS = discover_inputs()

# --- Expresiones regulares y configuración --- #

record_re = re.compile(
    r"BEGIN_LITERAL_FILE_RECORD\n(.*?)\nEND_LITERAL_FILE_RECORD", re.S
)
path_re = re.compile(r"^PATH_LITERAL=(.+)$", re.M)
content_py_re = re.compile(
    r"CONTENT_BEGIN\n~~~~~python\n(.*?)\n~~~~~\nCONTENT_END", re.S
)
content_html_re = re.compile(
    r"CONTENT_BEGIN\n~~~~~html\n(.*?)\n~~~~~\nCONTENT_END", re.S
)
identifier_re = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\b")
file_token_re = re.compile(
    r"[A-Za-z0-9_./:-]+\.(?:py|html|md|txt|csv|tsv|xlsx|css|js)"
)

py_keywords = {
    "False", "None", "True", "and", "as", "assert", "async", "await",
    "break", "class", "continue", "def", "del", "elif", "else", "except",
    "finally", "for", "from", "global", "if", "import", "in", "is",
    "lambda", "nonlocal", "not", "or", "pass", "raise", "return",
    "try", "while", "with", "yield", "match", "case",
}

html_noise = {
    "html", "head", "body", "div", "span", "table", "thead", "tbody",
    "tr", "td", "th", "form", "input", "select", "option", "button",
    "script", "style", "label", "p", "a", "h1", "h2", "h3", "h4",
    "h5", "h6", "nav", "main", "header", "footer", "section",
    "article", "title", "meta", "link", "doctype",
}

common_noise = py_keywords | {"self", "cls"}

# --- Utilidades --- #

def strip_specials(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "", value).lower()

def add_ident(name, source, ident_sources):
    if not name or len(name) < 2:
        return
    if name in common_noise:
        return
    ident_sources[name].add(source)

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")

def has_internal_specials_lowercase(name: str) -> bool:
    return bool(re.fullmatch(r"[a-z0-9]+(?:[^A-Za-z0-9]+[a-z0-9]+)+", name))

def is_plain_lowercase_alnum(name: str) -> bool:
    return bool(re.fullmatch(r"[a-z0-9]+", name))

def is_priority_group(entries) -> bool:
    values = [name for _, name in entries]
    has_plain = any(is_plain_lowercase_alnum(name) for name in values)
    has_internal_special = any(has_internal_specials_lowercase(name) for name in values)
    return has_plain and has_internal_special

# --- Núcleo: construir inventario --- #

def build_inventory():
    file_names = set()
    ident_sources = defaultdict(set)

    for fp in INPUTS:
        if not fp.exists():
            print(f"ADVERTENCIA: no existe {fp}")
            continue

        text = read_text(fp)

        is_python_bundle = fp.name.startswith("all_python_scripts")
        is_html_bundle = (
            fp.name.startswith("all_html_templates")
            or "html_templates" in fp.name
        )

        for recm in record_re.finditer(text):
            rec = recm.group(1)
            pm = path_re.search(rec)

            if not pm:
                continue

            record_path = pm.group(1).strip()
            if is_migration_path(record_path):
                continue
            if is_root_level_path(record_path):
                continue

            file_names.add(record_path)

            if is_python_bundle:
                cm = content_py_re.search(rec)
                if not cm:
                    continue
                content = cm.group(1)

                for tok in file_token_re.findall(content):
                    file_names.add(tok)

                for name in identifier_re.findall(content):
                    if name not in py_keywords:
                        add_ident(name, "python", ident_sources)

            elif is_html_bundle:
                cm = content_html_re.search(rec)
                if not cm:
                    continue
                content = cm.group(1)

                for tok in file_token_re.findall(content):
                    file_names.add(tok)

                for expr in re.findall(r"\{\{\s*([^}]+?)\s*\}\}", content):
                    root = re.split(r"[\.|\|: ]", expr.strip())[0]
                    if root:
                        add_ident(root, "html", ident_sources)

                for expr in re.findall(r"\{%\s*url\s+[\"']([^\"']+)[\"']", content):
                    add_ident(expr, "html", ident_sources)

                for _, val in re.findall(
                    r"\b(?:id|name|class)=([\"'])(.*?)\1", content
                ):
                    for part in re.split(r"\s+", val.strip()):
                        if re.match(r"^[A-Za-z_][A-Za-z0-9_-]*$", part):
                            add_ident(part, "html", ident_sources)

                for name in identifier_re.findall(content):
                    if name.lower() not in html_noise:
                        add_ident(name, "html", ident_sources)

            else:
                continue

    all_idents = sorted(ident_sources.keys(), key=lambda s: s.lower())
    all_files = sorted(file_names, key=lambda s: s.lower())

    constants = []
    identifiers = []
    for name in all_idents:
        if re.fullmatch(r"[A-Z][A-Z0-9_]*", name):
            constants.append(name)
        else:
            identifiers.append(name)

    return all_files, constants, identifiers

def number_lines(items):
    return [f"{i:04d}. {item}" for i, item in enumerate(items, start=1)]

def find_suspects(items):
    groups = defaultdict(list)
    for idx, item in enumerate(items, start=1):
        key = strip_specials(item)
        if key:
            groups[key].append((idx, item))
    return dict(
        sorted(
            (k, v) for k, v in groups.items() if len(v) > 1
        )
    )

def write_text(path: Path, lines):
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

def append_group_lines(target_lines, normalized, entries):
    target_lines.append(f"- {normalized}")
    for idx, name in entries:
        target_lines.append(f" - {idx:04d}. {name}")

def append_suspect_section(target_lines, title, suspects):
    target_lines.append(title)
    if suspects:
        for normalized, entries in suspects.items():
            append_group_lines(target_lines, normalized, entries)
    else:
        target_lines.append("- Ninguno")
    target_lines.append("")

def filter_priority_suspects(suspects):
    return {
        normalized: entries
        for normalized, entries in suspects.items()
        if is_priority_group(entries)
    }

# --- main --- #

def main():
    reset_output_dir()
    files, constants, identifiers = build_inventory()
  
    files_numbered = number_lines(files)
    constants_numbered = number_lines(constants)
    identifiers_numbered = number_lines(identifiers)

    write_text(OUTDIR / "files_sorted_numbered.txt", files_numbered)
    write_text(OUTDIR / "constants_sorted_numbered.txt", constants_numbered)
    write_text(OUTDIR / "identifiers_sorted_numbered.txt", identifiers_numbered)

    file_suspects = find_suspects(files)
    constant_suspects = find_suspects(constants)
    identifier_suspects = find_suspects(identifiers)

    priority_file_suspects = filter_priority_suspects(file_suspects)
    priority_constant_suspects = filter_priority_suspects(constant_suspects)
    priority_identifier_suspects = filter_priority_suspects(identifier_suspects)

    suspect_lines = []
    suspect_lines.append("# Sospechosos por normalización")
    suspect_lines.append("")

    suspect_lines.append("## PRIORIDAD")
    suspect_lines.append("")
    append_suspect_section(suspect_lines, "### Archivos", priority_file_suspects)
    append_suspect_section(suspect_lines, "### Constantes", priority_constant_suspects)
    append_suspect_section(suspect_lines, "### Identificadores", priority_identifier_suspects)

    suspect_lines.append("## TODOS")
    suspect_lines.append("")
    append_suspect_section(suspect_lines, "### Archivos", file_suspects)
    append_suspect_section(suspect_lines, "### Constantes", constant_suspects)
    append_suspect_section(suspect_lines, "### Identificadores", identifier_suspects)

    write_text(OUTDIR / "sospechosos_normalizados.txt", suspect_lines)

    print("Listo.")
    print(f"Archivos: {len(files)}")
    print(f"Constantes: {len(constants)}")
    print(f"Identificadores: {len(identifiers)}")
    print(f"Sospechosos archivos: {len(file_suspects)}")
    print(f"Sospechosos constantes: {len(constant_suspects)}")
    print(f"Sospechosos identificadores: {len(identifier_suspects)}")
    print(f"Prioridad archivos: {len(priority_file_suspects)}")
    print(f"Prioridad constantes: {len(priority_constant_suspects)}")
    print(f"Prioridad identificadores: {len(priority_identifier_suspects)}")
    print("Salida en output/")

if __name__ == "__main__":
    main()
    