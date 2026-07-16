import sqlite3
import os
import sys

DB_FILENAME = "db.sqlite3"

def ensure_db_exists(db_filename: str) -> str:
    """Verifica que exista db.sqlite3 en el directorio actual."""
    if not os.path.isfile(db_filename):
        print(f"Error: La base de datos '{db_filename}' no existe en este directorio.")
        sys.exit(1)
    return db_filename

def generate_output_filename(db_filename: str) -> str:
    """Genera el nombre del archivo de salida basado en el nombre de la BD."""
    if db_filename.endswith(".sqlite3"):
        base_name = db_filename[:-8]  # quita ".sqlite3"
    elif db_filename.endswith(".db"):
        base_name = db_filename[:-3]  # quita ".db"
    else:
        base_name = db_filename
    return f"{base_name}_dbcontents.txt"

def export_database_contents(db_paths, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        for db_path in db_paths:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            f.write(f"\nTITLE: CONTENTS OF DATABASE: {db_path}\n\n")

            # Listar todas las tablas (excluyendo tablas internas de sqlite)
            cursor.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
                ORDER BY name
            """)
            tables = [row[0] for row in cursor.fetchall()]

            if not tables:
                f.write("(No hay tablas en esta base de datos)\n\n")
                conn.close()
                continue

            for table in tables:
                f.write(f"TABLE: {table.upper()}\n")

                # Información de columnas
                cursor.execute(f"PRAGMA table_info({table})")
                columns_info = cursor.fetchall()
                columns = [col[1] for col in columns_info]

                # Todos los registros de la tabla
                cursor.execute(f"SELECT * FROM {table}")
                rows = cursor.fetchall()

                if not columns:
                    f.write("(La tabla no tiene columnas visibles)\n\n")
                    continue

                header_line = " | ".join(columns)
                f.write(header_line + "\n")
                f.write("-" * len(header_line) + "\n")

                if not rows:
                    f.write("(Sin registros)\n\n")
                    continue

                for row in rows:
                    f.write(" | ".join(str(value) if value is not None else "NULL" for value in row) + "\n")

                f.write("\n")

            conn.close()

if __name__ == "__main__":
    db_filename = ensure_db_exists(DB_FILENAME)
    output_file = generate_output_filename(db_filename)
    db_paths = [db_filename]

    export_database_contents(db_paths, output_file)
    print(f"Database contents exported to {output_file}")
    