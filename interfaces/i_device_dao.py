"""Interface específica para operaciones de Device DAO."""

from abc import abstractmethod
from typing import List
from .i_dao import IDao
from dominio.device import Device


class IDeviceDao(IDao[Device]):
    """Interface para operaciones específicas de Dispositivo."""
    
    @abstractmethod
    def obtener_por_hogar(self, home_id: int) -> List[Device]:
        """
        Obtiene todos los dispositivos de un hogar.
        
        Args:
            home_id: ID del hogar
            
        Returns:
            Lista de dispositivos del hogar
        """
        pass
    
    @abstractmethod
    def buscar_por_nombre(self, nombre: str, home_id: int) -> List[Device]:
        """
        Busca dispositivos por nombre en un hogar.
        
        Args:
            nombre: Texto a buscar
            home_id: ID del hogar
            
        Returns:
            Lista de dispositivos que coinciden
        """
        pass
    
    @abstractmethod
    def cambiar_estado(self, device_id: int, nuevo_estado_id: int) -> bool:
        """
        Cambia el estado de un dispositivo.
        
        Args:
            device_id: ID del dispositivo
            nuevo_estado_id: ID del nuevo estado
            
        Returns:
            True si se cambió correctamente
        """
        pass