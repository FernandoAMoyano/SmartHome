"""
Script para configurar la base de datos SmartHome.

Funcionalidades:
- Crear base de datos si no existe
- Crear todas las tablas (schema)
- Insertar datos iniciales (seeds)
- Verificar conexión y estado

Uso:
    python database/setup_database.py --all
    python database/setup_database.py --create-db --schema --seed
    python database/setup_database.py --reset --all
    python database/setup_database.py --verify
"""

import sys
import mysql.connector
from pathlib import Path
from typing import Tuple

# Agregar el directorio padre al path para importar desde ui
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import DB_CONFIG, DATABASE_NAME, SCHEMA_FILE
from ui.rich_utils import (
    show_db_setup_banner,
    show_db_config_table,
    show_verification_table,
    show_seed_progress,
    print_success,
    print_error,
    print_warning,
    print_step,
    show_reset_warning,
    console,
)


class DatabaseSetup:
    """Gestiona la creación y configuración de la BD."""

    def __init__(self):
        """Inicializa el gestor de setup."""
        self.base_path = Path(__file__).parent
        self.schema_path = self.base_path / "schema"
        self.seeds_path = self.base_path / "seeds"

    def create_database(self) -> bool:
        """Crea la base de datos si no existe."""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
            print_success(f"Base de datos '{DATABASE_NAME}' creada/verificada")

            cursor.close()
            conn.close()
            return True

        except mysql.connector.Error as e:
            print_error(f"Error al crear base de datos: {e}")
            return False

    def execute_sql_file(self, filepath: Path) -> bool:
        """Ejecuta un archivo SQL."""
        try:
            config = {**DB_CONFIG, "database": DATABASE_NAME}
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()

            with open(filepath, "r", encoding="utf-8") as f:
                sql_content = f.read()

            # Limpiar comentarios y dividir en statements
            statements = []
            for line in sql_content.split("\n"):
                # Ignorar líneas de comentarios
                if line.strip().startswith("--") or line.strip().startswith("#"):
                    continue
                statements.append(line)
            
            # Unir las líneas y dividir por punto y coma
            clean_sql = "\n".join(statements)
            
            # Ejecutar cada statement
            for statement in clean_sql.split(";"):
                statement = statement.strip()
                if statement:  # Solo ejecutar si hay contenido
                    try:
                        cursor.execute(statement)
                    except mysql.connector.Error as stmt_error:
                        print_warning(f"Error en statement: {stmt_error}")
                        # Continuar con el siguiente statement
                        continue

            conn.commit()
            cursor.close()
            conn.close()
            return True

        except mysql.connector.Error as e:
            print_error(f"Error en {filepath.name}: {e}")
            return False
        except FileNotFoundError:
            print_error(f"Archivo no encontrado: {filepath}")
            return False
        except Exception as e:
            print_error(f"Error inesperado en {filepath.name}: {e}")
            return False

    def create_schema(self) -> bool:
        """Crea todas las tablas del schema."""
        console.print()
        print_step(1, 3, "Creando schema (tablas)...")

        if not SCHEMA_FILE.exists():
            print_error(f"No se encontró {SCHEMA_FILE}")
            return False

        success = self.execute_sql_file(SCHEMA_FILE)
        if success:
            print_success("Schema creado correctamente")
        return success

    def seed_database(self) -> bool:
        """Inserta datos iniciales en orden."""
        seed_files = sorted(self.seeds_path.glob("*.sql"))

        if not seed_files:
            print_warning("No se encontraron archivos de seeds")
            return True

        console.print()
        print_step(2, 3, f"Insertando datos iniciales ({len(seed_files)} archivos)...")
        
        # Usar la barra de progreso de Rich
        show_seed_progress(seed_files, self.execute_sql_file)
        
        return True

    def verify_setup(self) -> Tuple[bool, dict]:
        """Verifica que todo esté correctamente configurado."""
        try:
            console.print()
            print_step(3, 3, "Verificando configuración...")
            
            config = {**DB_CONFIG, "database": DATABASE_NAME}
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()

            # Contar tablas
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            table_count = len(tables)

            # Contar registros en tablas principales
            counts = {}
            main_tables = ["role", "user", "home", "device", "automation", "event"]

            for table_name in main_tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    counts[table_name] = cursor.fetchone()[0]
                except mysql.connector.Error:
                    counts[table_name] = 0

            cursor.close()
            conn.close()

            # Mostrar tabla de verificación con Rich
            console.print()
            show_verification_table({"tables": table_count, "counts": counts})

            return True, {"tables": table_count, "counts": counts}

        except mysql.connector.Error as e:
            print_error(f"Error en verificación: {e}")
            return False, {}

    def reset_database(self) -> bool:
        """Elimina y recrea la base de datos (útil en desarrollo)."""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            console.print()
            print_warning(f"Eliminando base de datos '{DATABASE_NAME}'...")
            cursor.execute(f"DROP DATABASE IF EXISTS {DATABASE_NAME}")

            cursor.close()
            conn.close()

            print_success("Base de datos eliminada")
            return True

        except mysql.connector.Error as e:
            print_error(f"Error al resetear: {e}")
            return False


def main():
    """Función principal del script."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Setup de base de datos SmartHome",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python database/setup_database.py --all
  python database/setup_database.py --create-db --schema --seed
  python database/setup_database.py --verify
  python database/setup_database.py --reset --all
        """,
    )

    parser.add_argument("--create-db", action="store_true", help="Crear base de datos")
    parser.add_argument("--schema", action="store_true", help="Crear schema (tablas)")
    parser.add_argument("--seed", action="store_true", help="Insertar datos iniciales")
    parser.add_argument("--verify", action="store_true", help="Verificar configuración")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Resetear BD (CUIDADO: Elimina todos los datos)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Ejecutar todo (create-db + schema + seed + verify)",
    )

    args = parser.parse_args()

    # Si no se pasa ningún argumento, mostrar ayuda
    if not any(vars(args).values()):
        parser.print_help()
        return

    setup = DatabaseSetup()

    # Mostrar banner con Rich
    show_db_setup_banner()
    
    # Mostrar configuración con Rich
    show_db_config_table(DB_CONFIG, DATABASE_NAME)

    # Resetear si se solicita
    if args.reset:
        if show_reset_warning():
            if not setup.reset_database():
                print_error("Fallo al resetear. Abortando.")
                sys.exit(1)
        else:
            print_warning("Operación cancelada")
            return

    # Ejecutar todas las operaciones
    if args.all:
        args.create_db = args.schema = args.seed = args.verify = True

    # Crear BD
    if args.create_db:
        console.print()
        if not setup.create_database():
            print_error("Fallo al crear base de datos. Abortando.")
            sys.exit(1)

    # Crear schema
    if args.schema:
        if not setup.create_schema():
            print_error("Fallo al crear schema. Abortando.")
            sys.exit(1)

    # Insertar seeds
    if args.seed:
        if not setup.seed_database():
            print_error("Fallo al insertar seeds. Abortando.")
            sys.exit(1)

    # Verificar
    if args.verify or args.all:
        success, stats = setup.verify_setup()
        if not success:
            sys.exit(1)

    # Mensaje final con Rich
    console.print()
    from rich.panel import Panel
    from ui.rich_utils import COLORS
    success_panel = Panel(
        "[bold green]✓ CONFIGURACIÓN COMPLETADA EXITOSAMENTE[/bold green]",
        border_style=COLORS["success"],
        padding=(1, 2),
    )
    console.print(success_panel)
    console.print()


if __name__ == "__main__":
    main()
