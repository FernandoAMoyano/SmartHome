"""Implementación DAO para la entidad Device."""

from typing import List, Optional
from mysql.connector import Error
from interfaces.i_device_dao import IDeviceDao
from dominio.device import Device
from conn.db_connection import DatabaseConnection
from dao.state_dao import StateDAO
from dao.device_type_dao import DeviceTypeDAO
from dao.location_dao import LocationDAO
from dao.home_dao import HomeDAO


class DeviceDAO(IDeviceDao):
    """Data Access Object para gestionar dispositivos."""
    
    def __init__(self):
        self.db = DatabaseConnection()
        self.state_dao = StateDAO()
        self.device_type_dao = DeviceTypeDAO()
        self.location_dao = LocationDAO()
        self.home_dao = HomeDAO()
    
    def insertar(self, entidad: Device) -> bool:
        """Inserta un nuevo dispositivo."""
        try:
            cursor = self.db.get_cursor()
            query = """
                INSERT INTO device (name, state_id, device_type_id, location_id, home_id)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                entidad.name,
                entidad.state.id,
                entidad.device_type.id,
                entidad.location.id,
                entidad.home.id
            ))
            self.db.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error al insertar dispositivo: {e}")
            self.db.rollback()
            return False
    
    def modificar(self, entidad: Device) -> bool:
        """Modifica un dispositivo existente."""
        try:
            cursor = self.db.get_cursor()
            query = """
                UPDATE device 
                SET name = %s, state_id = %s, device_type_id = %s, 
                    location_id = %s, home_id = %s
                WHERE id = %s
            """
            cursor.execute(query, (
                entidad.name,
                entidad.state.id,
                entidad.device_type.id,
                entidad.location.id,
                entidad.home.id,
                entidad.id
            ))
            self.db.commit()
            affected = cursor.rowcount > 0
            cursor.close()
            return affected
        except Error as e:
            print(f"Error al modificar dispositivo: {e}")
            self.db.rollback()
            return False
    
    def eliminar(self, id: int) -> bool:
        """Elimina un dispositivo por ID."""
        try:
            cursor = self.db.get_cursor()
            query = "DELETE FROM device WHERE id = %s"
            cursor.execute(query, (id,))
            self.db.commit()
            affected = cursor.rowcount > 0
            cursor.close()
            return affected
        except Error as e:
            print(f"Error al eliminar dispositivo: {e}")
            self.db.rollback()
            return False
    
    def obtener_por_id(self, id: int) -> Optional[Device]:
        """Obtiene un dispositivo por ID."""
        try:
            cursor = self.db.get_cursor()
            query = """
                SELECT id, name, state_id, device_type_id, location_id, home_id
                FROM device WHERE id = %s
            """
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                state = self.state_dao.obtener_por_id(row['state_id'])
                device_type = self.device_type_dao.obtener_por_id(row['device_type_id'])
                location = self.location_dao.obtener_por_id(row['location_id'])
                home = self.home_dao.obtener_por_id(row['home_id'])
                
                if all([state, device_type, location, home]):
                    return Device(
                        row['id'],
                        row['name'],
                        state,
                        device_type,
                        location,
                        home
                    )
            return None
        except Error as e:
            print(f"Error al obtener dispositivo: {e}")
            return None
    
    def obtener_todos(self) -> List[Device]:
        """Obtiene todos los dispositivos."""
        try:
            cursor = self.db.get_cursor()
            query = """
                SELECT id, name, state_id, device_type_id, location_id, home_id
                FROM device
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            
            dispositivos = []
            for row in rows:
                state = self.state_dao.obtener_por_id(row['state_id'])
                device_type = self.device_type_dao.obtener_por_id(row['device_type_id'])
                location = self.location_dao.obtener_por_id(row['location_id'])
                home = self.home_dao.obtener_por_id(row['home_id'])
                
                if all([state, device_type, location, home]):
                    dispositivos.append(Device(
                        row['id'],
                        row['name'],
                        state,
                        device_type,
                        location,
                        home
                    ))
            return dispositivos
        except Error as e:
            print(f"Error al obtener dispositivos: {e}")
            return []
    
    def obtener_por_hogar(self, home_id: int) -> List[Device]:
        """Obtiene todos los dispositivos de un hogar."""
        try:
            cursor = self.db.get_cursor()
            query = """
                SELECT id, name, state_id, device_type_id, location_id, home_id
                FROM device WHERE home_id = %s
            """
            cursor.execute(query, (home_id,))
            rows = cursor.fetchall()
            cursor.close()
            
            dispositivos = []
            for row in rows:
                state = self.state_dao.obtener_por_id(row['state_id'])
                device_type = self.device_type_dao.obtener_por_id(row['device_type_id'])
                location = self.location_dao.obtener_por_id(row['location_id'])
                home = self.home_dao.obtener_por_id(row['home_id'])
                
                if all([state, device_type, location, home]):
                    dispositivos.append(Device(
                        row['id'],
                        row['name'],
                        state,
                        device_type,
                        location,
                        home
                    ))
            return dispositivos
        except Error as e:
            print(f"Error al obtener dispositivos del hogar: {e}")
            return []
    
    def buscar_por_nombre(self, nombre: str, home_id: int) -> List[Device]:
        """Busca dispositivos por nombre en un hogar."""
        try:
            cursor = self.db.get_cursor()
            query = """
                SELECT id, name, state_id, device_type_id, location_id, home_id
                FROM device 
                WHERE home_id = %s AND name LIKE %s
            """
            cursor.execute(query, (home_id, f"%{nombre}%"))
            rows = cursor.fetchall()
            cursor.close()
            
            dispositivos = []
            for row in rows:
                state = self.state_dao.obtener_por_id(row['state_id'])
                device_type = self.device_type_dao.obtener_por_id(row['device_type_id'])
                location = self.location_dao.obtener_por_id(row['location_id'])
                home = self.home_dao.obtener_por_id(row['home_id'])
                
                if all([state, device_type, location, home]):
                    dispositivos.append(Device(
                        row['id'],
                        row['name'],
                        state,
                        device_type,
                        location,
                        home
                    ))
            return dispositivos
        except Error as e:
            print(f"Error al buscar dispositivos: {e}")
            return []
    
    def cambiar_estado(self, device_id: int, nuevo_estado_id: int) -> bool:
        """Cambia el estado de un dispositivo."""
        try:
            cursor = self.db.get_cursor()
            query = "UPDATE device SET state_id = %s WHERE id = %s"
            cursor.execute(query, (nuevo_estado_id, device_id))
            self.db.commit()
            affected = cursor.rowcount > 0
            cursor.close()
            return affected
        except Error as e:
            print(f"Error al cambiar estado: {e}")
            self.db.rollback()
            return False