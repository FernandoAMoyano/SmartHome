"""Implementación DAO para la entidad Role."""

from typing import List, Optional
from mysql.connector import Error
from interfaces.i_dao import IDao
from dominio.role import Role
from conn.db_connection import DatabaseConnection


class RoleDAO(IDao[Role]):
    """Data Access Object para gestionar roles."""
    
    def __init__(self):
        """Inicializa el DAO con la conexión a BD."""
        self.db = DatabaseConnection()
    
    def insertar(self, entidad: Role) -> bool:
        """Inserta un nuevo rol."""
        try:
            cursor = self.db.get_cursor()
            query = "INSERT INTO role (id, name) VALUES (%s, %s)"
            cursor.execute(query, (entidad.id, entidad.name))
            self.db.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error al insertar rol: {e}")
            self.db.rollback()
            return False
    
    def modificar(self, entidad: Role) -> bool:
        """Modifica un rol existente."""
        try:
            cursor = self.db.get_cursor()
            query = "UPDATE role SET name = %s WHERE id = %s"
            cursor.execute(query, (entidad.name, entidad.id))
            self.db.commit()
            cursor.close()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error al modificar rol: {e}")
            self.db.rollback()
            return False
    
    def eliminar(self, id: int) -> bool:
        """Elimina un rol por ID."""
        try:
            cursor = self.db.get_cursor()
            query = "DELETE FROM role WHERE id = %s"
            cursor.execute(query, (id,))
            self.db.commit()
            cursor.close()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error al eliminar rol: {e}")
            self.db.rollback()
            return False
    
    def obtener_por_id(self, id: int) -> Optional[Role]:
        """Obtiene un rol por ID."""
        try:
            cursor = self.db.get_cursor()
            query = "SELECT id, name FROM role WHERE id = %s"
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                return Role(row['id'], row['name'])
            return None
        except Error as e:
            print(f"Error al obtener rol: {e}")
            return None
    
    def obtener_todos(self) -> List[Role]:
        """Obtiene todos los roles."""
        try:
            cursor = self.db.get_cursor()
            query = "SELECT id, name FROM role"
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            
            return [Role(row['id'], row['name']) for row in rows]
        except Error as e:
            print(f"Error al obtener roles: {e}")
            return []