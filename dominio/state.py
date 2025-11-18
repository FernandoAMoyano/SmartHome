"""Módulo de dominio para la entidad State."""


class State:
    """
    Representa un estado posible para un dispositivo.
    
    Atributos:
        id: Identificador único del estado
        name: Nombre del estado (ej: 'encendido', 'apagado')
    """
    
    def __init__(self, id: int, name: str):
        """
        Inicializa un nuevo estado.
        
        Args:
            id: Identificador del estado
            name: Nombre descriptivo del estado
        """
        self.__id = id
        self.__name = name

    @property
    def id(self) -> int:
        """Obtiene el ID del estado."""
        return self.__id

    @property
    def name(self) -> str:
        """Obtiene el nombre del estado."""
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        """Establece el nombre del estado."""
        self.__name = value