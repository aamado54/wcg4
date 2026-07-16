# File: find_inconsist.py
# Genera un script Python que haga lo siguiente:
# 1. Que lea de un archivo input.txt para escribir los resultados en un archivo output.txt ambos en el mismo directorio donde se encuentra el programa y que además contiene una lista simple de nombres (c/u = string) sin espacios enmedio, uno por línea
# 2. Que empiece un loop donde para cada string hará lo siguiente
# 3. Busca ese string en cada uno de todos los archivos .txt en el mismo directorio con nombres que empiezan con “all”, cada vez que se encuentre el string, en el archivo y punto donde se encuentra empieza a dar marcha atrás buscando la instancia más próxima de “FILENAME=” antes, y copia el contenido de esa línea después de “FILENAME=” y sin incluir “FILENAME=”.
# 4. Termina y repite el loop hasta terminar con todos los string en la lista.


from pathlib import Path

INPUT_FILE = "input.txt"
OUTPUT_FILE = "output.txt"


def read_input_strings(base_dir: Path):
    text = (base_dir / INPUT_FILE).read_text(encoding="utf-8", errors="ignore")
    return [line.strip() for line in text.splitlines() if line.strip()]


def discover_all_files(base_dir: Path):
    files = []
    for p in base_dir.iterdir():
        if p.is_file() and p.name.startswith("all") and p.suffix.lower() in {".txt", ".md"}:
            files.append(p)
    files.sort(key=lambda x: x.name.lower())
    return files


def find_nearest_filename(lines, start_line_index):
    """
    start_line_index: índice de línea (0-based).
    Recorre hacia arriba hasta encontrar una línea con FILENAME=...
    """
    marker = "FILENAME="
    for i in range(start_line_index, -1, -1):
        line = lines[i]
        pos = line.find(marker)
        if pos != -1:
            return line[pos + len(marker):].strip()
    return "FILENAME_NO_ENCONTRADO"


def main():
    base_dir = Path(__file__).resolve().parent
    needles = read_input_strings(base_dir)
    all_files = discover_all_files(base_dir)

    out_lines = []
    out_lines.append(f"BASE_DIR={base_dir}")
    out_lines.append("ARCHIVOS_ANALIZADOS:")
    for f in all_files:
        out_lines.append(f"  {f.name}")
    out_lines.append("")

    for needle in needles:
        needle_lower = needle.lower()
        out_lines.append(f"STRING={needle}")
        total_matches = 0

        for file_path in all_files:
            text = file_path.read_text(encoding="utf-8", errors="ignore")
            lines = text.splitlines(keepends=False)

            for idx, line in enumerate(lines):
                line_lower = line.lower()
                if needle_lower in line_lower:
                    total_matches += 1
                    filename_value = find_nearest_filename(lines, idx)

                    out_lines.append(f"  OCURRENCIA#{total_matches}")
                    out_lines.append(f"    ARCHIVO_ALL={file_path.name}")
                    out_lines.append(f"    FILENAME={filename_value}")
                    out_lines.append(f"    LINEA={idx + 1}")
                    out_lines.append(f"    TEXTO={line.rstrip()}")
                    out_lines.append("")

        if total_matches == 0:
            out_lines.append("  SIN_COINCIDENCIAS")
            out_lines.append("")

    (base_dir / OUTPUT_FILE).write_text("\n".join(out_lines), encoding="utf-8")


if __name__ == "__main__":
    main()

