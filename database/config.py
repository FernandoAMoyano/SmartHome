"""
Configuración de base de datos para SmartHome.

Este archivo centraliza la configuración de conexión a MySQL.
Soporta variables de entorno para mayor seguridad.
"""

import os
from typing import Dict, Union
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# ============================================
# CONFIGURACIÓN DE BASE DE DATOS
# ============================================

# Nombre de la base de datos
DATABASE_NAME = "smarthome"

# Configuración de conexión
# Lee las credenciales desde el archivo .env
DB_CONFIG: Dict[str, Union[str, int]] = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD"),
    "port": int(os.getenv("DB_PORT", "3306")),
}

# Validar que el password esté configurado
if not DB_CONFIG.get("password"):
    raise ValueError(
        "❌ ERROR: DB_PASSWORD no encontrado.\n"
        "Por favor configura tu password en el archivo .env\n"
        "Ejemplo: DB_PASSWORD=tu_password_aqui"
    )

# Configuración completa (incluye el nombre de la BD)
DB_CONFIG_WITH_DATABASE: Dict[str, Union[str, int]] = {
    **DB_CONFIG,
    "database": DATABASE_NAME,
}

# ============================================
# RUTAS DE ARCHIVOS
# ============================================

# Directorio base del módulo database
BASE_DIR = Path(__file__).parent

# Directorio de schema (DDL)
SCHEMA_DIR = BASE_DIR / "schema"

# Directorio de seeds (DML)
SEEDS_DIR = BASE_DIR / "seeds"

# Archivo de schema principal
SCHEMA_FILE = SCHEMA_DIR / "create_tables.sql"

# ============================================
# FUNCIONES AUXILIARES
# ============================================


def get_db_config(include_database: bool = False) -> Dict[str, Union[str, int]]:
    """
    Obtiene la configuración de base de datos.

    Args:
        include_database: Si True, incluye el nombre de la BD en la config

    Returns:
        Diccionario con configuración de conexión
    """
    return DB_CONFIG_WITH_DATABASE if include_database else DB_CONFIG


def print_config_info():
    """Imprime información de configuración (sin mostrar password)."""
    print(" ✓ Configuración de Base de Datos:")
    print(f"   Host: {DB_CONFIG['host']}")
    print(f"   Puerto: {DB_CONFIG['port']}")
    print(f"   Usuario: {DB_CONFIG['user']}")
    print(f"   Base de datos: {DATABASE_NAME}")
    print(f"   Password: {'*' * len(DB_CONFIG['password'])}")


if __name__ == "__main__":
    print_config_info()
