"""Módulo de conexión a la base de datos MySQL."""

import mysql.connector
from mysql.connector import Error
from typing import Optional


class DatabaseConnection:
    """
    - Gestiona la conexión con la base de datos MySQL.
    - Implementa el patrón Singleton para mantener una única conexión.
    """
    
    _instance: Optional['DatabaseConnection'] = None
    _connection: Optional[mysql.connector.MySQLConnection] = None
    
    def __new__(cls):
        """Implementa Singleton."""
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Inicializa la configuración de conexión."""
        self.host = 'localhost'
        self.database = 'smarthome'
        self.user = 'root'
        self.password = 'Holalola324'  # Configurar según entorno
        self.port = 3306
    
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
                    port=self.port
                )
                if self._connection.is_connected():
                    print("✓ Conexión exitosa a la base de datos")
            return self._connection
        except Error as e:
            print(f"✗ Error al conectar a la base de datos: {e}")
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