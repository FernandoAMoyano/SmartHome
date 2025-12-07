"""Módulo de conexión a la base de datos MySQL."""

import mysql.connector
from mysql.connector import Error
from typing import Optional
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class DatabaseConnection:
    """
    - Gestiona la conexión con la base de datos MySQL.
    - Implementa el patrón Singleton para mantener una única conexión.
    - Lee configuración desde variables de entorno (.env)
    """

    _instance: Optional["DatabaseConnection"] = None
    _connection: Optional[mysql.connector.MySQLConnection] = None

    def __new__(cls):
        """Implementa Singleton."""
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Inicializa la configuración de conexión desde .env"""
        # Leer variables de entorno con valores por defecto
        self.host = os.getenv("DB_HOST", "localhost")
        self.database = os.getenv("DB_DATABASE", "smarthome")
        self.user = os.getenv("DB_USER", "root")
        self.password = os.getenv("DB_PASSWORD", "")
        self.port = int(os.getenv("DB_PORT", "3306"))

    def connect(self) -> Optional[mysql.connector.MySQLConnection]:
        """
        Establece conexión con la base de datos.

        Returns:
            Objeto de conexión o None si falla
        """
        try:
            if self._connection is None or not self._connection.is_connected():
                self._connection = mysql.connector.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password,
                    port=self.port,
                )
                if self._connection.is_connected():
                    print("✓ Conexión exitosa a la base de datos")
            return self._connection
        except Error as e:
            print(f"✗ Error al conectar a la base de datos: {e}")
            print(f"  Host: {self.host}")
            print(f"  Database: {self.database}")
            print(f"  User: {self.user}")
            print("  ⚠️  Verifica tu archivo .env")
            return None

    def disconnect(self) -> None:
        """Cierra la conexión con la base de datos."""
        if self._connection and self._connection.is_connected():
            self._connection.close()
            print("✓ Conexión cerrada")

    def get_cursor(self):
        """
        Obtiene un cursor para ejecutar consultas.

        Returns:
            Cursor de MySQL o None si falla
        """
        connection = self.connect()
        if connection:
            return connection.cursor(dictionary=True)
        return None

    def commit(self) -> None:
        """Confirma los cambios en la base de datos."""
        if self._connection and self._connection.is_connected():
            self._connection.commit()

    def rollback(self) -> None:
        """Revierte los cambios en la base de datos."""
        if self._connection and self._connection.is_connected():
            self._connection.rollback()
