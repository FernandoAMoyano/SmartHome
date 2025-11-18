"""Implementación DAO para la entidad DeviceType."""

from typing import List, Optional
from mysql.connector import Error
from interfaces.i_dao import IDao
from dominio.device_type import DeviceType
from conn.db_connection import DatabaseConnection


class DeviceTypeDAO(IDao[DeviceType]):
    """Data Access Object para gestionar tipos de dispositivos."""
    
    def __init__(self):
        self.db = DatabaseConnection()
    
    def insertar(self, entidad: DeviceType) -> bool:
        try:
            cursor = self.db.get_cursor()
            query = "INSERT INTO device_type (id, name, characteristic) VALUES (%s, %s, %s)"
            cursor.execute(query, (entidad.id, entidad.name, entidad.characteristics))
            self.db.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error al insertar tipo de dispositivo: {e}")
            self.db.rollback()
            return False
    
    def modificar(self, entidad: DeviceType) -> bool:
        try:
            cursor = self.db.get_cursor()
            query = "UPDATE device_type SET name = %s, characteristic = %s WHERE id = %s"
            cursor.execute(query, (entidad.name, entidad.characteristics, entidad.id))
            self.db.commit()
            affected = cursor.rowcount > 0
            cursor.close()
            return affected
        except Error as e:
            print(f"Error al modificar tipo de dispositivo: {e}")
            self.db.rollback()
            return False
    
    def eliminar(self, id: int) -> bool:
        try:
            cursor = self.db.get_cursor()
            query = "DELETE FROM device_type WHERE id = %s"
            cursor.execute(query, (id,))
            self.db.commit()
            affected = cursor.rowcount > 0
            cursor.close()
            return affected
        except Error as e:
            print(f"Error al eliminar tipo de dispositivo: {e}")
            self.db.rollback()
            return False
    
    def obtener_por_id(self, id: int) -> Optional[DeviceType]:
        try:
            cursor = self.db.get_cursor()
            query = "SELECT id, name, characteristic FROM device_type WHERE id = %s"
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                return DeviceType(row['id'], row['name'], row['characteristic'] or "")
            return None
        except Error as e:
            print(f"Error al obtener tipo de dispositivo: {e}")
            return None
    
    def obtener_todos(self) -> List[DeviceType]:
        try:
            cursor = self.db.get_cursor()
            query = "SELECT id, name, characteristic FROM device_type"
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            
            return [DeviceType(row['id'], row['name'], row['characteristic'] or "") for row in rows]
        except Error as e:
            print(f"Error al obtener tipos de dispositivos: {e}")
            return []