"""Módulo de dominio para la entidad Home."""

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .device import Device


class Home:
    """
    Representa un hogar en el sistema SmartHome.
    
    Atributos:
        id: Identificador único del hogar
        name: Nombre del hogar
    """
    
    def __init__(self, id: int, name: str):
        """
        Inicializa un nuevo hogar.
        
        Args:
            id: Identificador del hogar
            name: Nombre descriptivo del hogar
        """
        self.__id = id
        self.__name = name
        self.__devices: List['Device'] = []

    @property
    def id(self) -> int:
        """Obtiene el ID del hogar."""
        return self.__id

    @property
    def name(self) -> str:
        """Obtiene el nombre del hogar."""
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        """Establece el nombre del hogar."""
        self.__name = value

    def add_device(self, device: 'Device') -> None:
        """
        Agrega un dispositivo al hogar.
        
        Args:
            device: Dispositivo a agregar
        """
        if device not in self.__devices:
            self.__devices.append(device)

    def remove_device(self, device: 'Device') -> None:
        """
        Elimina un dispositivo del hogar.
        
        Args:
            device: Dispositivo a eliminar
        """
        if device in self.__devices:
            self.__devices.remove(device)

    def get_devices(self) -> List['Device']:
        """
        Obtiene la lista de dispositivos del hogar.
        
        Returns:
            Lista de dispositivos
        """
        return self.__devices.copy()