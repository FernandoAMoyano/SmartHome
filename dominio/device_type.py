"""Módulo de dominio para la entidad DeviceType."""


class DeviceType:
    """
    Representa un tipo de dispositivo.
    
    Atributos:
        id: Identificador único del tipo
        name: Nombre del tipo (ej: 'Luz', 'Termostato')
        characteristics: Características del tipo de dispositivo
    """
    
    def __init__(self, id: int, name: str, characteristics: str = ""):
        """
        Inicializa un nuevo tipo de dispositivo.
        
        Args:
            id: Identificador del tipo
            name: Nombre del tipo
            characteristics: Características opcionales
        """
        self.__id = id
        self.__name = name
        self.__characteristics = characteristics

    @property
    def id(self) -> int:
        """Obtiene el ID del tipo."""
        return self.__id

    @property
    def name(self) -> str:
        """Obtiene el nombre del tipo."""
        return self.__name

    @property
    def characteristics(self) -> str:
        """Obtiene las características del tipo."""
        return self.__characteristics

    @name.setter
    def name(self, value: str) -> None:
        """Establece el nombre del tipo."""
        self.__name = value

    @characteristics.setter
    def characteristics(self, value: str) -> None:
        """Establece las características del tipo."""
        self.__characteristics = value