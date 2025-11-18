"""Implementación DAO para la entidad Home."""

from typing import List, Optional
from mysql.connector import Error
from interfaces.i_dao import IDao
from dominio.home import Home
from conn.db_connection import DatabaseConnection


class HomeDAO(IDao[Home]):
    """Data Access Object para gestionar hogares."""
    
    def __init__(self):
        self.db = DatabaseConnection()
    
    def insertar(self, entidad: Home) -> bool:
        try:
            cursor = self.db.get_cursor()
            query = "INSERT INTO home (name) VALUES (%s)"
            cursor.execute(query, (entidad.name,))
            self.db.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error al insertar hogar: {e}")
            self.db.rollback()
            return False
    
    def modificar(self, entidad: Home) -> bool:
        try:
            cursor = self.db.get_cursor()
            query = "UPDATE home SET name = %s WHERE id = %s"
            cursor.execute(query, (entidad.name, entidad.id))
            self.db.commit()
            affected = cursor.rowcount > 0
            cursor.close()
            return affected
        except Error as e:
            print(f"Error al modificar hogar: {e}")
            self.db.rollback()
            return False
    
    def eliminar(self, id: int) -> bool:
        try:
            cursor = self.db.get_cursor()
            query = "DELETE FROM home WHERE id = %s"
            cursor.execute(query, (id,))
            self.db.commit()
            affected = cursor.rowcount > 0
            cursor.close()
            return affected
        except Error as e:
            print(f"Error al eliminar hogar: {e}")
            self.db.rollback()
            return False
    
    def obtener_por_id(self, id: int) -> Optional[Home]:
        try:
            cursor = self.db.get_cursor()
            query = "SELECT id, name FROM home WHERE id = %s"
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                return Home(row['id'], row['name'])
            return None
        except Error as e:
            print(f"Error al obtener hogar: {e}")
            return None
    
    def obtener_todos(self) -> List[Home]:
        try:
            cursor = self.db.get_cursor()
            query = "SELECT id, name FROM home"
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            
            return [Home(row['id'], row['name']) for row in rows]
        except Error as e:
            print(f"Error al obtener hogares: {e}")
            return []
    
    def obtener_hogares_usuario(self, email: str) -> List[Home]:
        """Obtiene los hogares asociados a un usuario."""
        try:
            cursor = self.db.get_cursor()
            query = """
                SELECT h.id, h.name 
                FROM home h
                INNER JOIN user_home uh ON h.id = uh.home_id
                WHERE uh.user_email = %s
            """
            cursor.execute(query, (email,))
            rows = cursor.fetchall()
            cursor.close()
            
            return [Home(row['id'], row['name']) for row in rows]
        except Error as e:
            print(f"Error al obtener hogares del usuario: {e}")
            return []