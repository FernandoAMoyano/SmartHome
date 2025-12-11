"""Módulo de conexión a la base de datos MySQL."""

import mysql.connector
from mysql.connector import Error
from typing import Optional
import os
from dotenv import load_dotenv
from utils.logger import get_database_logger, log_database_error
from utils.exceptions import ConnectionException, QueryException

# Cargar variables de entorno
load_dotenv()

# Logger de base de datos
logger = get_database_logger()


class DatabaseConnection:
    """
    - Gestiona la conexión con la base de datos MySQL.
    - Implementa el patrón Singleton para mantener una única conexión.
    - Lee configuración desde variables de entorno (.env)
    - Registra todas las operaciones en logs
    - Maneja excepciones de forma específica
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

    def connect(self) -> mysql.connector.MySQLConnection:
        """
        Establece conexión con la base de datos.

        Returns:
            Objeto de conexión
            
        Raises:
            ConnectionException: Si no se puede conectar a la base de datos
        """
        try:
            if self._connection is None or not self._connection.is_connected():
                logger.info(f"Intentando conectar a BD: {self.database}@{self.host}")
                
                self._connection = mysql.connector.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password,
                    port=self.port,
                )
                
                if self._connection.is_connected():
                    print("✓ Conexión exitosa a la base de datos")
                    logger.info(f"Conexión exitosa a {self.database}")
                    
            return self._connection
            
        except Error as e:
            error_msg = str(e)
            
            # Log detallado del error
            log_database_error(
                "CONNECTION",
                e,
                f"host={self.host}, db={self.database}, user={self.user}"
            )
            
            # Mensaje para el usuario
            print(f"✗ Error al conectar a la base de datos: {error_msg}")
            print(f"  Host: {self.host}")
            print(f"  Database: {self.database}")
            print(f"  User: {self.user}")
            print("  ⚠️  Verifica tu archivo .env")
            
            # Lanzar excepción personalizada
            raise ConnectionException(
                f"No se pudo conectar a la base de datos. {error_msg}"
            ) from e
            
        except Exception as e:
            logger.error(f"Error inesperado al conectar: {type(e).__name__} - {e}")
            print(f"✗ Error inesperado: {e}")
            
            raise ConnectionException(
                "Error inesperado al conectar a la base de datos"
            ) from e

    def disconnect(self) -> None:
        """Cierra la conexión con la base de datos."""
        try:
            if self._connection and self._connection.is_connected():
                self._connection.close()
                print("✓ Conexión cerrada")
                logger.info("Conexión a BD cerrada correctamente")
        except Exception as e:
            logger.warning(f"Error al cerrar conexión: {e}")

    def get_cursor(self):
        """
        Obtiene un cursor para ejecutar consultas.

        Returns:
            Cursor de MySQL
            
        Raises:
            ConnectionException: Si no se puede obtener el cursor
        """
        try:
            connection = self.connect()
            if connection:
                return connection.cursor(dictionary=True)
            else:
                raise ConnectionException("No hay conexión activa")
        except Error as e:
            logger.error(f"Error al obtener cursor: {e}")
            raise QueryException("get_cursor", str(e)) from e

    def commit(self) -> None:
        """
        Confirma los cambios en la base de datos.
        
        Raises:
            QueryException: Si falla el commit
        """
        try:
            if self._connection and self._connection.is_connected():
                self._connection.commit()
                logger.debug("Cambios confirmados en BD (COMMIT)")
            else:
                raise ConnectionException("No hay conexión activa para commit")
        except Error as e:
            logger.error(f"Error en commit: {e}")
            raise QueryException("commit", str(e)) from e

    def rollback(self) -> None:
        """
        Revierte los cambios en la base de datos.
        
        Raises:
            QueryException: Si falla el rollback
        """
        try:
            if self._connection and self._connection.is_connected():
                self._connection.rollback()
                logger.warning("Cambios revertidos en BD (ROLLBACK)")
            else:
                logger.warning("No hay conexión activa para rollback")
        except Error as e:
            logger.error(f"Error en rollback: {e}")
            raise QueryException("rollback", str(e)) from e
