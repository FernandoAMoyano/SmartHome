"""Implementación DAO para la entidad State."""

from typing import List, Optional
from mysql.connector import Error
from interfaces.i_dao import IDao
from dominio.state import State
from conn.db_connection import DatabaseConnection


class StateDAO(IDao[State]):
    """Data Access Object para gestionar estados."""
    
    def __init__(self):
        """Inicializa el DAO con la conexión a BD."""
        self.db = DatabaseConnection()
    
    def insertar(self, entidad: State) -> bool:
        """Inserta un nuevo estado."""
        try:
            cursor = self.db.get_cursor()
            query = "INSERT INTO state (id, name) VALUES (%s, %s)"
            cursor.execute(query, (entidad.id, entidad.name))
            self.db.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error al insertar estado: {e}")
            self.db.rollback()
            return False
    
    def modificar(self, entidad: State) -> bool:
        """Modifica un estado existente."""
        try:
            cursor = self.db.get_cursor()
            query = "UPDATE state SET name = %s WHERE id = %s"
            cursor.execute(query, (entidad.name, entidad.id))
            self.db.commit()
            affected = cursor.rowcount > 0
            cursor.close()
            return affected
        except Error as e:
            print(f"Error al modificar estado: {e}")
            self.db.rollback()
            return False
    
    def eliminar(self, id: int) -> bool:
        """Elimina un estado por ID."""
        try:
            cursor = self.db.get_cursor()
            query = "DELETE FROM state WHERE id = %s"
            cursor.execute(query, (id,))
            self.db.commit()
            affected = cursor.rowcount > 0
            cursor.close()
            return affected
        except Error as e:
            print(f"Error al eliminar estado: {e}")
            self.db.rollback()
            return False
    
    def obtener_por_id(self, id: int) -> Optional[State]:
        """Obtiene un estado por ID."""
        try:
            cursor = self.db.get_cursor()
            query = "SELECT id, name FROM state WHERE id = %s"
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                return State(row['id'], row['name'])
            return None
        except Error as e:
            print(f"Error al obtener estado: {e}")
            return None
    
    def obtener_todos(self) -> List[State]:
        """Obtiene todos los estados."""
        try:
            cursor = self.db.get_cursor()
            query = "SELECT id, name FROM state"
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            
            return [State(row['id'], row['name']) for row in rows]
        except Error as e:
            print(f"Error al obtener estados: {e}")
            return []