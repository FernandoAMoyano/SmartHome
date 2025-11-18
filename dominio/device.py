"""Módulo de dominio para la entidad Device."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .state import State
    from .device_type import DeviceType
    from .location import Location
    from .home import Home


class Device:
    """
    Representa un dispositivo inteligente en el sistema.
    
    Atributos:
        id: Identificador único del dispositivo
        name: Nombre del dispositivo
        state: Estado actual del dispositivo
        device_type: Tipo de dispositivo
        location: Ubicación física del dispositivo
        home: Hogar al que pertenece
    """
    
    def __init__(
        self,
        id: int,
        name: str,
        state: 'State',
        device_type: 'DeviceType',
        location: 'Location',
        home: 'Home'
    ):
        """
        Inicializa un nuevo dispositivo.
        
        Args:
            id: Identificador del dispositivo
            name: Nombre descriptivo
            state: Objeto State con el estado actual
            device_type: Objeto DeviceType con el tipo
            location: Objeto Location con la ubicación
            home: Objeto Home al que pertenece
        """
        self.__id = id
        self.__name = name
        self.__state = state
        self.__device_type = device_type
        self.__location = location
        self.__home = home

    @property
    def id(self) -> int:
        """Obtiene el ID del dispositivo."""
        return self.__id

    @property
    def name(self) -> str:
        """Obtiene el nombre del dispositivo."""
        return self.__name

    @property
    def state(self) -> 'State':
        """Obtiene el estado del dispositivo."""
        return self.__state

    @property
    def device_type(self) -> 'DeviceType':
        """Obtiene el tipo del dispositivo."""
        return self.__device_type

    @property
    def location(self) -> 'Location':
        """Obtiene la ubicación del dispositivo."""
        return self.__location

    @property
    def home(self) -> 'Home':
        """Obtiene el hogar del dispositivo."""
        return self.__home

    @name.setter
    def name(self, value: str) -> None:
        """Establece el nombre del dispositivo."""
        self.__name = value

    @state.setter
    def state(self, value: 'State') -> None:
        """Cambia el estado del dispositivo."""
        self.__state = value

    @location.setter
    def location(self, value: 'Location') -> None:
        """Cambia la ubicación del dispositivo."""
        self.__location = value

    def search_device_by_name(self, search_name: str) -> bool:
        """
        Busca el dispositivo por nombre parcial.
        
        Args:
            search_name: Texto a buscar en el nombre
            
        Returns:
            True si el nombre contiene el texto buscado
        """
        if not search_name.strip():
            return False
        return search_name.lower() in self.__name.lower()

    def turn_on(self) -> None:
        """Enciende el dispositivo cambiando su estado."""
        # La lógica específica dependerá del tipo de dispositivo
        pass

    def turn_off(self) -> None:
        """Apaga el dispositivo cambiando su estado."""
        # La lógica específica dependerá del tipo de dispositivo
        pass