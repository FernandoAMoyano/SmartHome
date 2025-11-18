"""Implementación DAO para la entidad Automation."""

from typing import List, Optional
from mysql.connector import Error
from interfaces.i_dao import IDao
from dominio.automation import Automation
from conn.db_connection import DatabaseConnection
from dao.home_dao import HomeDAO


class AutomationDAO(IDao[Automation]):
    """Data Access Object para gestionar automatizaciones."""
    
    def __init__(self):
        """Inicializa el DAO con la conexión a BD."""
        self.db = DatabaseConnection()
        self.home_dao = HomeDAO()
    
    def insertar(self, entidad: Automation) -> bool:
        """Inserta una nueva automatización."""
        try:
            cursor = self.db.get_cursor()
            query = """
                INSERT INTO automation (name, description, active, home_id)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (
                entidad.name,
                entidad.description,
                entidad.active,
                entidad.home.id
            ))
            self.db.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error al insertar automatización: {e}")
            self.db.rollback()
            return False
    
    def modificar(self, entidad: Automation) -> bool:
        """Modifica una automatización existente."""
        try:
            cursor = self.db.get_cursor()
            query = """
                UPDATE automation 
                SET name = %s, description = %s, active = %s, home_id = %s
                WHERE id = %s
            """
            cursor.execute(query, (
                entidad.name,
                entidad.description,
                entidad.active,
                entidad.home.id,
                entidad.id
            ))
            self.db.commit()
            affected = cursor.rowcount > 0
            cursor.close()
            return affected
        except Error as e:
            print(f"Error al modificar automatización: {e}")
            self.db.rollback()
            return False
    
    def eliminar(self, id: int) -> bool:
        """Elimina una automatización por ID."""
        try:
            cursor = self.db.get_cursor()
            query = "DELETE FROM automation WHERE id = %s"
            cursor.execute(query, (id,))
            self.db.commit()
            affected = cursor.rowcount > 0
            cursor.close()
            return affected
        except Error as e:
            print(f"Error al eliminar automatización: {e}")
            self.db.rollback()
            return False
    
    def obtener_por_id(self, id: int) -> Optional[Automation]:
        """Obtiene una automatización por ID."""
        try:
            cursor = self.db.get_cursor()
            query = """
                SELECT id, name, description, active, home_id
                FROM automation WHERE id = %s
            """
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                home = self.home_dao.obtener_por_id(row['home_id'])
                if home:
                    return Automation(
                        row['id'],
                        row['name'],
                        row['description'],
                        bool(row['active']),
                        home
                    )
            return None
        except Error as e:
            print(f"Error al obtener automatización: {e}")
            return None
    
    def obtener_todos(self) -> List[Automation]:
        """Obtiene todas las automatizaciones."""
        try:
            cursor = self.db.get_cursor()
            query = """
                SELECT id, name, description, active, home_id
                FROM automation
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            
            automatizaciones = []
            for row in rows:
                home = self.home_dao.obtener_por_id(row['home_id'])
                if home:
                    automatizaciones.append(Automation(
                        row['id'],
                        row['name'],
                        row['description'],
                        bool(row['active']),
                        home
                    ))
            return automatizaciones
        except Error as e:
            print(f"Error al obtener automatizaciones: {e}")
            return []
    
    def obtener_por_hogar(self, home_id: int) -> List[Automation]:
        """
        Obtiene todas las automatizaciones de un hogar.
        
        Args:
            home_id: ID del hogar
            
        Returns:
            Lista de automatizaciones del hogar
        """
        try:
            cursor = self.db.get_cursor()
            query = """
                SELECT id, name, description, active, home_id
                FROM automation
                WHERE home_id = %s
            """
            cursor.execute(query, (home_id,))
            rows = cursor.fetchall()
            cursor.close()
            
            automatizaciones = []
            home = self.home_dao.obtener_por_id(home_id)
            if home:
                for row in rows:
                    automatizaciones.append(Automation(
                        row['id'],
                        row['name'],
                        row['description'],
                        bool(row['active']),
                        home
                    ))
            return automatizaciones
        except Error as e:
            print(f"Error al obtener automatizaciones del hogar: {e}")
            return []
    
    def obtener_activas(self, home_id: int) -> List[Automation]:
        """
        Obtiene las automatizaciones activas de un hogar.
        
        Args:
            home_id: ID del hogar
            
        Returns:
            Lista de automatizaciones activas
        """
        try:
            cursor = self.db.get_cursor()
            query = """
                SELECT id, name, description, active, home_id
                FROM automation
                WHERE home_id = %s AND active = TRUE
            """
            cursor.execute(query, (home_id,))
            rows = cursor.fetchall()
            cursor.close()
            
            automatizaciones = []
            home = self.home_dao.obtener_por_id(home_id)
            if home:
                for row in rows:
                    automatizaciones.append(Automation(
                        row['id'],
                        row['name'],
                        row['description'],
                        bool(row['active']),
                        home
                    ))
            return automatizaciones
        except Error as e:
            print(f"Error al obtener automatizaciones activas: {e}")
            return []
    
    def cambiar_estado(self, automation_id: int, activar: bool) -> bool:
        """
        Cambia el estado de activación de una automatización.
        
        Args:
            automation_id: ID de la automatización
            activar: True para activar, False para desactivar
            
        Returns:
            True si se cambió correctamente
        """
        try:
            cursor = self.db.get_cursor()
            query = "UPDATE automation SET active = %s WHERE id = %s"
            cursor.execute(query, (activar, automation_id))
            self.db.commit()
            affected = cursor.rowcount > 0
            cursor.close()
            return affected
        except Error as e:
            print(f"Error al cambiar estado de automatización: {e}")
            self.db.rollback()
            return False