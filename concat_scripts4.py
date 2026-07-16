import base64
import hashlib
import json
import os
import time
from datetime import datetime

# ============================================================================
# PARÁMETROS DE CONFIGURACIÓN - EDITA AQUÍ
# ============================================================================

# Control de tipos de archivo a generar
GENERATE_PYTHON = True
GENERATE_HTML = True
GENERATE_JS = False
GENERATE_CSS = False
GENERATE_MARKDOWN = False
GENERATE_TEXT = False

# Control de archivos auxiliares
GENERATE_INDEX_FILES = True  # Activado para generar índices enriquecidos
GENERATE_DIR_LISTING = True

# Límites de tamaño
MAX_OUTPUT_CHARS_PER_PART = 295_000
MAX_FILES_PER_PART = 50

# Tipos que incluirán base64
INCLUDE_BASE64_FOR = {".py", ".html"}

# Directorios extra a listar (además de la raíz del proyecto)
EXTRA_LISTING_DIRS = []  # Ejemplo: ["../data", "../shared"]

# Archivos recientes a reportar
RECENT_FILE_EXTENSIONS = {".py", ".html"}
RECENT_HOURS = 72

# ============================================================================
# CONFIGURACIÓN INTERNA - NO EDITAR NORMALMENTE
# ============================================================================

EXCLUDE_DIRS = {
    ".git", ".hg", ".svn", "__pycache__", ".idea", ".vscode",
    "staticfiles", "media",
    "venv", "venv1", "venv2", ".venv",
    "env", "env1", "env2", "migrations",
}

TEXT_EXTENSIONS = {".py", ".js", ".html", ".css", ".md", ".txt"}
MAX_SIZE = 300 * 1024
RECORD_BOUNDARY = "========== RECORD_BOUNDARY =========="

OUTPUT_SPECS = {
    ".py": ("all_python_scripts", "python", GENERATE_PYTHON),
    ".html": ("all_html_templates", "html", GENERATE_HTML),
    ".js": ("all_js_scripts", "javascript", GENERATE_JS),
    ".css": ("all_css_styles", "css", GENERATE_CSS),
    ".md": ("all_markdown_files", "markdown", GENERATE_MARKDOWN),
    ".txt": ("all_text_files", "text", GENERATE_TEXT),
}

TIMESTAMP_SUFFIX = datetime.now().strftime("-%m-%d-%H-%M")

SELF_OUTPUT_FILES = {
    "all_other_text_files.md",
    "all_other_text_files.index.md",
    "concat_scripts.py",
    "concat_scripts0.py",
    "concat_scripts1.py",
    "concat_scripts2.py",
    "concat_scripts3.py",
    "concat_scripts_v2.py",
    "concat_scripts_v3.py",
}

for ext, (base_name, _language, enabled) in OUTPUT_SPECS.items():
    if enabled:
        SELF_OUTPUT_FILES.add(f"{base_name}.md")
        SELF_OUTPUT_FILES.add(f"{base_name}.index.md")
        SELF_OUTPUT_FILES.add(f"{base_name}{TIMESTAMP_SUFFIX}.md")
        SELF_OUTPUT_FILES.add(f"{base_name}{TIMESTAMP_SUFFIX}.index.md")
    for part_count in range(1, 50):
        for part_number in range(1, 50):
            SELF_OUTPUT_FILES.add(f"{base_name}.part-{part_number:02d}-of-{part_count:02d}.md")
            SELF_OUTPUT_FILES.add(f"{base_name}.part-{part_number:02d}-of-{part_count:02d}{TIMESTAMP_SUFFIX}.md")


def with_timestamp(filename):
    name, ext = os.path.splitext(filename)
    return f"{name}{TIMESTAMP_SUFFIX}{ext}"


def path_contains_excluded_dir(rel_path):
    parts = rel_path.replace("\\", "/").split("/")
    return any(part in EXCLUDE_DIRS for part in parts)


def should_skip_dir(dirpath, dirname, root):
    if dirname in EXCLUDE_DIRS:
        return True
    full = os.path.join(dirpath, dirname)
    rel = os.path.relpath(full, root)
    if "site-packages" in rel.split(os.sep):
        return True
    if path_contains_excluded_dir(rel):
        return True
    return False


def is_small_text_file(full_path):
    _, ext = os.path.splitext(full_path)
    if ext.lower() not in TEXT_EXTENSIONS:
        return False
    try:
        size = os.path.getsize(full_path)
    except OSError:
        return False
    return size <= MAX_SIZE


def safe_read_text(full_path):
    for encoding in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            with open(full_path, "r", encoding=encoding, newline="") as f:
                return f.read()
        except (UnicodeDecodeError, OSError):
            continue
    return None


def detect_newline_style(text):
    if "\r\n" in text:
        if "\n" in text.replace("\r\n", ""):
            return "MIXED"
        return "CRLF"
    if "\r" in text:
        return "CR"
    return "LF"


def make_numbered_lines(text):
    lines = text.splitlines(keepends=True)
    if not lines and text == "":
        return "00001|"
    return "".join(f"{idx:05d}|{line}" for idx, line in enumerate(lines, start=1))


def build_file_metadata(rel_path, content, language):
    ext = os.path.splitext(rel_path)[1].lower()
    encoded = content.encode("utf-8", errors="replace")
    line_count = len(content.splitlines())
    if content and not content.endswith(("\n", "\r")):
        line_count += 1

    return {
        "rel_path": rel_path,
        "filename": os.path.basename(rel_path),
        "ext": ext or "[none]",
        "language": language,
        "line_count": line_count,
        "size_bytes": len(encoded),
        "content_sha256": hashlib.sha256(encoded).hexdigest(),
        "ends_with_newline": content.endswith(("\n", "\r")),
        "newline_style": detect_newline_style(content),
        "encoded": encoded,
        "numbered": make_numbered_lines(content),
        "content": content,
    }


def make_file_block(rel_path, content, language):
    meta = build_file_metadata(rel_path, content, language)
    fence = "~~~~~"

    lines = [
        "BEGIN_LITERAL_FILE_RECORD",
        f"PATH_LITERAL={meta['rel_path']}",
        f"PATH_JSON={json.dumps(meta['rel_path'], ensure_ascii=False)}",
        f"FILENAME={meta['filename']}",
        f"EXTENSION={meta['ext']}",
        f"LANGUAGE_HINT={meta['language']}",
        f"LINE_COUNT={meta['line_count']}",
        f"SIZE_BYTES_UTF8={meta['size_bytes']}",
        f"CONTENT_SHA256={meta['content_sha256']}",
        f"ENDS_WITH_NEWLINE={'TRUE' if meta['ends_with_newline'] else 'FALSE'}",
        f"ORIGINAL_NEWLINE_STYLE={meta['newline_style']}",
        "CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK",
        "DO_NOT_SUMMARIZE=TRUE",
        "DO_NOT_NORMALIZE=TRUE",
        "DO_NOT_FLATTEN=TRUE",
        "PRESERVE_PUNCTUATION=TRUE",
        "PRESERVE_LINE_BREAKS=TRUE",
        "PRESERVE_INDENTATION=TRUE",
        "PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN",
        "IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.",
        "CONTENT_BEGIN",
        f"{fence}{meta['language']}",
        meta["content"],
        fence,
        "CONTENT_END",
        "",
        "CONTENT_NUMBERED_BEGIN",
        meta["numbered"],
        "CONTENT_NUMBERED_END",
    ]

    if os.path.splitext(rel_path)[1].lower() in INCLUDE_BASE64_FOR:
        b64 = base64.b64encode(meta["encoded"]).decode("ascii")
        lines.extend([
            "",
            "CONTENT_BASE64_BEGIN",
            b64,
            "CONTENT_BASE64_END",
        ])

    lines.extend([
        "",
        "END_LITERAL_FILE_RECORD",
        "",
        RECORD_BOUNDARY,
        "",
    ])
    return "\n".join(lines), meta


def collect_files(root):
    grouped = {ext: [] for ext in OUTPUT_SPECS}
    other = []

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not should_skip_dir(dirpath, d, root)]
        filenames = sorted(filenames)

        if os.path.abspath(dirpath) == os.path.abspath(root):
            filenames = []

        for name in filenames:
            if name.startswith("0-directorios-y-archivos-") or name.startswith("all_files_and_directories_"):
                continue
            if name in SELF_OUTPUT_FILES:
                continue
            if ".part-" in name and name.endswith(".md"):
                continue

            full_path = os.path.join(dirpath, name)
            if not os.path.isfile(full_path) or not is_small_text_file(full_path):
                continue

            rel_path = os.path.relpath(full_path, root).replace(os.sep, "/")
            if path_contains_excluded_dir(rel_path):
                continue

            content = safe_read_text(full_path)
            if content is None:
                continue

            ext = os.path.splitext(name)[1].lower()
            language = OUTPUT_SPECS.get(ext, (None, "text", False))[1]
            block, meta = make_file_block(rel_path, content, language)

            item = {
                "rel_path": rel_path,
                "language": language,
                "block": block,
                "char_count": len(block),
                "ext": meta["ext"],
                "line_count": meta["line_count"],
                "size_bytes": meta["size_bytes"],
                "content_sha256": meta["content_sha256"],
                "ends_with_newline": meta["ends_with_newline"],
                "newline_style": meta["newline_style"],
            }

            if ext in grouped:
                grouped[ext].append(item)
            else:
                other.append(item)

    for ext in grouped:
        grouped[ext].sort(key=lambda item: item["rel_path"])
    other.sort(key=lambda item: item["rel_path"])
    return grouped, other


def make_intro(title, part_number=None, total_parts=None):
    lines = [title, ""]
    if part_number is not None and total_parts is not None:
        lines.extend([
            f"PART_NUMBER={part_number}",
            f"TOTAL_PARTS={total_parts}",
            "",
        ])
    lines.extend([
        "DOCUMENT_MODE=LITERAL_CODE_ARCHIVE",
        "PARSING_PRIORITY=PATH_LITERAL->CONTENT_NUMBERED_BEGIN->CONTENT_BASE64_BEGIN->CONTENT_BEGIN",
        "DO_NOT_SUMMARIZE=TRUE",
        "DO_NOT_NORMALIZE=TRUE",
        "DO_NOT_FLATTEN=TRUE",
        "PRESERVE_LINE_BREAKS=TRUE",
        "PRESERVE_INDENTATION=TRUE",
        "RECORD_SEPARATOR=BEGIN_LITERAL_FILE_RECORD|END_LITERAL_FILE_RECORD",
        f"RECORD_BOUNDARY={RECORD_BOUNDARY}",
        "CONTENT_POLICY=PRESERVE_EXACT_TEXT_WITH_METADATA_AND_NUMBERED_FALLBACK",
        "READING_HINT=Prefer PATH_LITERAL first for file identity. Prefer CONTENT_NUMBERED_BEGIN for faithful line-by-line reading. Use CONTENT_BASE64_BEGIN for exact reconstruction when available. Use CONTENT_BEGIN only as a convenience view. If CONTENT_BEGIN looks compacted, flattened, or visually altered, do not use it to infer exact identifiers, variable names, paths, punctuation grouping, or spacing.",
        "",
    ])
    return "\n".join(lines)


def split_items_into_parts(items, intro_template):
    parts = []
    current = []
    current_chars = len(intro_template)

    for item in items:
        block_chars = item["char_count"]
        would_exceed_chars = current and (current_chars + block_chars > MAX_OUTPUT_CHARS_PER_PART)
        would_exceed_files = current and (len(current) >= MAX_FILES_PER_PART)

        if would_exceed_chars or would_exceed_files:
            parts.append(current)
            current = []
            current_chars = len(intro_template)

        current.append(item)
        current_chars += block_chars

    if current:
        parts.append(current)

    return parts


def write_part_files(root, base_name, title, items, generate_index):
    if not items:
        return []

    intro_template = make_intro(title)
    parts = split_items_into_parts(items, intro_template)
    total_parts = len(parts)
    written = []

    index_lines = [
        f"# INDEX FOR {base_name}",
        "",
        f"TOTAL_PARTS={total_parts}",
        f"TOTAL_FILES={len(items)}",
        "",
        "## PARTS",
        "",
    ]

    for idx, part_items in enumerate(parts, start=1):
        suffix = f".part-{idx:02d}-of-{total_parts:02d}.md" if total_parts > 1 else ".md"
        filename = with_timestamp(f"{base_name}{suffix}")
        intro = make_intro(title, part_number=idx, total_parts=total_parts) if total_parts > 1 else make_intro(title)
        body = "".join(item["block"] for item in part_items)
        out_path = os.path.join(root, filename)

        with open(out_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(intro + body)

        written.append(filename)

        first_file = part_items[0]["rel_path"]
        last_file = part_items[-1]["rel_path"]
        index_lines.append(
            f"- FILE={filename} FILES={len(part_items)} FIRST={json.dumps(first_file, ensure_ascii=False)} LAST={json.dumps(last_file, ensure_ascii=False)}"
        )

    if generate_index:
        index_lines.extend([
            "",
            "## ALL_FILES",
            "",
        ])
        for item in items:
            index_lines.append(
                " - ".join([
                    f"PATH_LITERAL={json.dumps(item['rel_path'], ensure_ascii=False)}",
                    f"EXTENSION={item['ext']}",
                    f"LINE_COUNT={item['line_count']}",
                    f"SIZE_BYTES_UTF8={item['size_bytes']}",
                    f"CONTENT_SHA256={item['content_sha256']}",
                    f"ENDS_WITH_NEWLINE={'TRUE' if item['ends_with_newline'] else 'FALSE'}",
                    f"ORIGINAL_NEWLINE_STYLE={item['newline_style']}",
                ])
            )

        index_filename = with_timestamp(f"{base_name}.index.md")
        index_path = os.path.join(root, index_filename)
        with open(index_path, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(index_lines) + "\n")
        written.append(index_filename)

    return written


def write_concat_outputs(root):
    grouped, other = collect_files(root)
    written = []

    for ext, (base_name, _language, enabled) in OUTPUT_SPECS.items():
        if not enabled:
            continue
        title = f"# CONCATENATED {ext.upper()} FILES"
        generate_index = GENERATE_INDEX_FILES and enabled
        written.extend(write_part_files(root, base_name, title, grouped[ext], generate_index))

    if other:
        generate_index = GENERATE_INDEX_FILES
        written.extend(write_part_files(root, "all_other_text_files", "# CONCATENATED OTHER TEXT FILES", other, generate_index))

    return written


def append_tree_listing(lines, base_dir, label=None, root_for_skip=None):
    if not os.path.exists(base_dir):
        lines.append(f"{label or base_dir}: [no existe]")
        lines.append("")
        return

    if label:
        lines.append(label)
        lines.append("")

    skip_root = root_for_skip or base_dir
    root_files = sorted(
        f for f in os.listdir(base_dir)
        if os.path.isfile(os.path.join(base_dir, f))
    )

    if root_files:
        lines.append(f"[archivos directos en {base_dir}]")
        for name in root_files:
            full = os.path.join(base_dir, name)
            try:
                ctime = os.path.getctime(full)
                mtime = os.path.getmtime(full)
                cts = time.strftime("%Y-%m-%d %H:%M", time.localtime(ctime))
                mts = time.strftime("%Y-%m-%d %H:%M", time.localtime(mtime))
                lines.append(f"{name} [creado: {cts}] [modificado: {mts}]")
            except OSError:
                lines.append(name)
        lines.append("")

    for dirpath, dirnames, filenames in os.walk(base_dir):
        dirnames[:] = [d for d in dirnames if not should_skip_dir(dirpath, d, skip_root)]
        rel_dir = os.path.relpath(dirpath, base_dir)
        if rel_dir == ".":
            continue
        lines.append(f"./{rel_dir}:")
        for name in sorted(filenames):
            full = os.path.join(dirpath, name)
            try:
                ctime = os.path.getctime(full)
                mtime = os.path.getmtime(full)
                cts = time.strftime("%Y-%m-%d %H:%M", time.localtime(ctime))
                mts = time.strftime("%Y-%m-%d %H:%M", time.localtime(mtime))
                lines.append(f"{name} [creado: {cts}] [modificado: {mts}]")
            except OSError:
                lines.append(name)
        lines.append("")


def list_recent_files(root, hours=RECENT_HOURS):
    cutoff = time.time() - hours * 3600
    recent = []

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not should_skip_dir(dirpath, d, root)]
        for name in filenames:
            ext = os.path.splitext(name)[1].lower()
            if ext not in RECENT_FILE_EXTENSIONS:
                continue
            full = os.path.join(dirpath, name)
            try:
                mtime = os.path.getmtime(full)
            except OSError:
                continue
            if mtime >= cutoff:
                rel = os.path.relpath(full, root)
                recent.append((mtime, rel))

    return sorted(recent, reverse=True)


def resolve_extra_listing_dirs(root):
    resolved = []
    seen = set()

    for item in EXTRA_LISTING_DIRS:
        if not item:
            continue
        path = item if os.path.isabs(item) else os.path.abspath(os.path.join(root, item))
        norm = os.path.normpath(path)
        if norm in seen or not os.path.exists(norm):
            continue
        seen.add(norm)
        resolved.append(norm)

    return resolved


def generate_dir_listing(root):
    lines = []
    append_tree_listing(lines, root, label="=== PROJECT ROOT ===", root_for_skip=root)

    extra_dirs = resolve_extra_listing_dirs(root)
    for extra_dir in extra_dirs:
        if extra_dir.startswith(root):
            extra_label = os.path.relpath(extra_dir, root)
        else:
            extra_label = extra_dir
        label = f"=== EXTRA: {extra_label} ==="
        append_tree_listing(lines, extra_dir, label=label, root_for_skip=extra_dir)

    lines.append(f"Archivos recientes ({RECENT_HOURS}h):")
    for mtime, rel in list_recent_files(root, RECENT_HOURS):
        ts = time.strftime("%Y-%m-%d %H:%M", time.localtime(mtime))
        lines.append(f"{ts} {rel}")

    filename = with_timestamp("all_files_and_directories.txt")
    out_path = os.path.join(root, filename)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    return out_path


if __name__ == "__main__":
    root_dir = os.getcwd()

    print("=" * 60)
    print("CONCAT_SCRIPTS V3 - CONFIGURACIÓN")
    print("=" * 60)
    print(f"ROOT_DIR = {root_dir}")
    print(f"TIMESTAMP_SUFFIX = {TIMESTAMP_SUFFIX}")
    print(f"MAX_OUTPUT_CHARS_PER_PART = {MAX_OUTPUT_CHARS_PER_PART:,}")
    print(f"MAX_FILES_PER_PART = {MAX_FILES_PER_PART}")
    print()
    print("TIPOS DE ARCHIVO A GENERAR:")
    print(f" Python: {'SÍ' if GENERATE_PYTHON else 'NO'}")
    print(f" HTML: {'SÍ' if GENERATE_HTML else 'NO'}")
    print(f" JS: {'SÍ' if GENERATE_JS else 'NO'}")
    print(f" CSS: {'SÍ' if GENERATE_CSS else 'NO'}")
    print(f" Markdown: {'SÍ' if GENERATE_MARKDOWN else 'NO'}")
    print(f" Text: {'SÍ' if GENERATE_TEXT else 'NO'}")
    print()
    print(f"GENERAR INDEX: {'SÍ' if GENERATE_INDEX_FILES else 'NO'}")
    print(f"GENERAR DIR LISTING: {'SÍ' if GENERATE_DIR_LISTING else 'NO'}")
    print()
    if EXTRA_LISTING_DIRS:
        print("EXTRA_LISTING_DIRS:")
        for item in resolve_extra_listing_dirs(root_dir):
            print(f" - {item}")
        print("=" * 60)
        print()

    written_files = write_concat_outputs(root_dir)

    if GENERATE_DIR_LISTING:
        listing_file = generate_dir_listing(root_dir)
        print(f"✓ Directorio: {listing_file}")

    print()
    print("ARCHIVOS GENERADOS:")
    for name in written_files:
        print(f" ✓ {name}")

    print()
    print(f"Total de archivos generados: {len(written_files) + (1 if GENERATE_DIR_LISTING else 0)}")
    print("=" * 60)
    print("COMPLETADO")