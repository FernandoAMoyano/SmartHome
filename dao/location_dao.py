"""Implementación DAO para la entidad Location."""

from typing import List, Optional
from mysql.connector import Error
from interfaces.i_dao import IDao
from dominio.location import Location
from conn.db_connection import DatabaseConnection
from dao.home_dao import HomeDAO


class LocationDAO(IDao[Location]):
    """Data Access Object para gestionar ubicaciones."""
    
    def __init__(self):
        self.db = DatabaseConnection()
        self.home_dao = HomeDAO()
    
    def insertar(self, entidad: Location) -> bool:
        try:
            cursor = self.db.get_cursor()
            query = "INSERT INTO location (name) VALUES (%s)"
            cursor.execute(query, (entidad.name,))
            self.db.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error al insertar ubicación: {e}")
            self.db.rollback()
            return False
    
    def modificar(self, entidad: Location) -> bool:
        try:
            cursor = self.db.get_cursor()
            query = "UPDATE location SET name = %s WHERE id = %s"
            cursor.execute(query, (entidad.name, entidad.id))
            self.db.commit()
            affected = cursor.rowcount > 0
            cursor.close()
            return affected
        except Error as e:
            print(f"Error al modificar ubicación: {e}")
            self.db.rollback()
            return False
    
    def eliminar(self, id: int) -> bool:
        try:
            cursor = self.db.get_cursor()
            query = "DELETE FROM location WHERE id = %s"
            cursor.execute(query, (id,))
            self.db.commit()
            affected = cursor.rowcount > 0
            cursor.close()
            return affected
        except Error as e:
            print(f"Error al eliminar ubicación: {e}")
            self.db.rollback()
            return False
    
    def obtener_por_id(self, id: int) -> Optional[Location]:
        try:
            cursor = self.db.get_cursor()
            query = "SELECT id, name FROM location WHERE id = %s"
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                # Por simplicidad, creamos un Home vacío
                # En producción, se debería obtener el home real
                from dominio.home import Home
                home = Home(0, "Default")
                return Location(row['id'], row['name'], home)
            return None
        except Error as e:
            print(f"Error al obtener ubicación: {e}")
            return None
    
    def obtener_todos(self) -> List[Location]:
        try:
            cursor = self.db.get_cursor()
            query = "SELECT id, name FROM location"
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            
            from dominio.home import Home
            home = Home(0, "Default")
            return [Location(row['id'], row['name'], home) for row in rows]
        except Error as e:
            print(f"Error al obtener ubicaciones: {e}")
            return []