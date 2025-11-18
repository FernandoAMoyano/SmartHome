"""Módulo de dominio para la entidad Location."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .home import Home


class Location:
    """
    Representa una ubicación física dentro de un hogar.
    
    Atributos:
        id: Identificador único de la ubicación
        name: Nombre de la ubicación (ej: 'Sala', 'Cocina')
        home: Hogar al que pertenece la ubicación
    """
    
    def __init__(self, id: int, name: str, home: 'Home'):
        """
        Inicializa una nueva ubicación.
        
        Args:
            id: Identificador de la ubicación
            name: Nombre descriptivo
            home: Objeto Home al que pertenece
        """
        self.__id = id
        self.__name = name
        self.__home = home

    @property
    def id(self) -> int:
        """Obtiene el ID de la ubicación."""
        return self.__id

    @property
    def name(self) -> str:
        """Obtiene el nombre de la ubicación."""
        return self.__name

    @property
    def home(self) -> 'Home':
        """Obtiene el hogar de la ubicación."""
        return self.__home

    @name.setter
    def name(self, value: str) -> None:
        """Establece el nombre de la ubicación."""
        self.__name = value