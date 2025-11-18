"""Implementación DAO para la entidad Event."""

from typing import List, Optional
from datetime import datetime
from mysql.connector import Error
from interfaces.i_dao import IDao
from dominio.event import Event
from conn.db_connection import DatabaseConnection
from dao.device_dao import DeviceDAO
from dao.user_dao import UserDAO


class EventDAO(IDao[Event]):
    """Data Access Object para gestionar eventos del sistema."""
    
    def __init__(self):
        """Inicializa el DAO con la conexión a BD."""
        self.db = DatabaseConnection()
        self.device_dao = DeviceDAO()
        self.user_dao = UserDAO()
    
    def insertar(self, entidad: Event) -> bool:
        """Inserta un nuevo evento."""
        try:
            cursor = self.db.get_cursor()
            query = """
                INSERT INTO event (description, device_id, user_email, source, date_time_value)
                VALUES (%s, %s, %s, %s, %s)
            """
            device_id = entidad.device.id if entidad.device else None
            user_email = entidad.user.email if entidad.user else None
            
            cursor.execute(query, (
                entidad.description,
                device_id,
                user_email,
                entidad.source,
                entidad.date_time_value
            ))
            self.db.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error al insertar evento: {e}")
            self.db.rollback()
            return False
    
    def modificar(self, entidad: Event) -> bool:
        """Modifica un evento existente."""
        try:
            cursor = self.db.get_cursor()
            query = """
                UPDATE event 
                SET description = %s, device_id = %s, user_email = %s, 
                    source = %s, date_time_value = %s
                WHERE id = %s
            """
            device_id = entidad.device.id if entidad.device else None
            user_email = entidad.user.email if entidad.user else None
            
            cursor.execute(query, (
                entidad.description,
                device_id,
                user_email,
                entidad.source,
                entidad.date_time_value,
                entidad.id
            ))
            self.db.commit()
            affected = cursor.rowcount > 0
            cursor.close()
            return affected
        except Error as e:
            print(f"Error al modificar evento: {e}")
            self.db.rollback()
            return False
    
    def eliminar(self, id: int) -> bool:
        """Elimina un evento por ID."""
        try:
            cursor = self.db.get_cursor()
            query = "DELETE FROM event WHERE id = %s"
            cursor.execute(query, (id,))
            self.db.commit()
            affected = cursor.rowcount > 0
            cursor.close()
            return affected
        except Error as e:
            print(f"Error al eliminar evento: {e}")
            self.db.rollback()
            return False
    
    def obtener_por_id(self, id: int) -> Optional[Event]:
        """Obtiene un evento por ID."""
        try:
            cursor = self.db.get_cursor()
            query = """
                SELECT id, date_time_value, description, device_id, user_email, source
                FROM event WHERE id = %s
            """
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                device = self.device_dao.obtener_por_id(row['device_id']) if row['device_id'] else None
                user = self.user_dao.obtener_por_email(row['user_email']) if row['user_email'] else None
                
                return Event(
                    row['id'],
                    row['description'],
                    row['source'],
                    device,
                    user,
                    row['date_time_value']
                )
            return None
        except Error as e:
            print(f"Error al obtener evento: {e}")
            return None
    
    def obtener_todos(self) -> List[Event]:
        """Obtiene todos los eventos."""
        try:
            cursor = self.db.get_cursor()
            query = """
                SELECT id, date_time_value, description, device_id, user_email, source
                FROM event
                ORDER BY date_time_value DESC
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            
            eventos = []
            for row in rows:
                device = self.device_dao.obtener_por_id(row['device_id']) if row['device_id'] else None
                user = self.user_dao.obtener_por_email(row['user_email']) if row['user_email'] else None
                
                eventos.append(Event(
                    row['id'],
                    row['description'],
                    row['source'],
                    device,
                    user,
                    row['date_time_value']
                ))
            return eventos
        except Error as e:
            print(f"Error al obtener eventos: {e}")
            return []
    
    def obtener_por_dispositivo(self, device_id: int, limite: int = 50) -> List[Event]:
        """
        Obtiene los eventos de un dispositivo específico.
        
        Args:
            device_id: ID del dispositivo
            limite: Cantidad máxima de eventos a retornar
            
        Returns:
            Lista de eventos del dispositivo
        """
        try:
            cursor = self.db.get_cursor()
            query = """
                SELECT id, date_time_value, description, device_id, user_email, source
                FROM event
                WHERE device_id = %s
                ORDER BY date_time_value DESC
                LIMIT %s
            """
            cursor.execute(query, (device_id, limite))
            rows = cursor.fetchall()
            cursor.close()
            
            eventos = []
            device = self.device_dao.obtener_por_id(device_id)
            
            for row in rows:
                user = self.user_dao.obtener_por_email(row['user_email']) if row['user_email'] else None
                
                eventos.append(Event(
                    row['id'],
                    row['description'],
                    row['source'],
                    device,
                    user,
                    row['date_time_value']
                ))
            return eventos
        except Error as e:
            print(f"Error al obtener eventos del dispositivo: {e}")
            return []
    
    def obtener_por_usuario(self, user_email: str, limite: int = 50) -> List[Event]:
        """
        Obtiene los eventos generados por un usuario.
  
        Args:
            user_email: Email del usuario
            limite: Cantidad máxima de eventos a retornar
            
        Returns:
            Lista de eventos del usuario
        """
        try:
            cursor = self.db.get_cursor()
            query = """
                SELECT id, date_time_value, description, device_id, user_email, source
                FROM event
                WHERE user_email = %s
                ORDER BY date_time_value DESC
                LIMIT %s
            """
            cursor.execute(query, (user_email, limite))
            rows = cursor.fetchall()
            cursor.close()
            
            eventos = []
            user = self.user_dao.obtener_por_email(user_email)
            
            for row in rows:
                device = self.device_dao.obtener_por_id(row['device_id']) if row['device_id'] else None
                
                eventos.append(Event(
                    row['id'],
                    row['description'],
                    row['source'],
                    device,
                    user,
                    row['date_time_value']
                ))
            return eventos
        except Error as e:
            print(f"Error al obtener eventos del usuario: {e}")
            return []
    
    def obtener_recientes(self, limite: int = 100) -> List[Event]:
        """
        Obtiene los eventos más recientes del sistema.
        
        Args:
            limite: Cantidad máxima de eventos a retornar
            
        Returns:
            Lista de eventos recientes
        """
        try:
            cursor = self.db.get_cursor()
            query = """
                SELECT id, date_time_value, description, device_id, user_email, source
                FROM event
                ORDER BY date_time_value DESC
                LIMIT %s
            """
            cursor.execute(query, (limite,))
            rows = cursor.fetchall()
            cursor.close()
            
            eventos = []
            for row in rows:
                device = self.device_dao.obtener_por_id(row['device_id']) if row['device_id'] else None
                user = self.user_dao.obtener_por_email(row['user_email']) if row['user_email'] else None
                
                eventos.append(Event(
                    row['id'],
                    row['description'],
                    row['source'],
                    device,
                    user,
                    row['date_time_value']
                ))
            return eventos
        except Error as e:
            print(f"Error al obtener eventos recientes: {e}")
            return []
    
    def obtener_por_fecha(self, fecha_inicio: datetime, fecha_fin: datetime) -> List[Event]:
        """
        Obtiene eventos en un rango de fechas.
        
        Args:
            fecha_inicio: Fecha inicial del rango
            fecha_fin: Fecha final del rango
            
        Returns:
            Lista de eventos en el rango
        """
        try:
            cursor = self.db.get_cursor()
            query = """
                SELECT id, date_time_value, description, device_id, user_email, source
                FROM event
                WHERE date_time_value BETWEEN %s AND %s
                ORDER BY date_time_value DESC
            """
            cursor.execute(query, (fecha_inicio, fecha_fin))
            rows = cursor.fetchall()
            cursor.close()
            
            eventos = []
            for row in rows:
                device = self.device_dao.obtener_por_id(row['device_id']) if row['device_id'] else None
                user = self.user_dao.obtener_por_email(row['user_email']) if row['user_email'] else None
                
                eventos.append(Event(
                    row['id'],
                    row['description'],
                    row['source'],
                    device,
                    user,
                    row['date_time_value']
                ))
            return eventos
        except Error as e:
            print(f"Error al obtener eventos por fecha: {e}")
            return []