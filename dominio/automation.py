"""Módulo de dominio para la entidad Automation."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .home import Home


class Automation:
    """
    Representa una automatización en el sistema SmartHome.
    
    Atributos:
        id: Identificador único de la automatización
        name: Nombre de la automatización
        description: Descripción de la automatización
        active: Estado de activación
        home: Hogar al que pertenece
    """
    
    def __init__(
        self,
        id: int,
        name: str,
        description: str,
        active: bool,
        home: 'Home'
    ):
        """
        Inicializa una nueva automatización.
        
        Args:
            id: Identificador de la automatización
            name: Nombre descriptivo
            description: Descripción de la función
            active: Si está activa o no
            home: Objeto Home al que pertenece
        """
        self.__id = id
        self.__name = name
        self.__description = description
        self.__active = active
        self.__home = home

    @property
    def id(self) -> int:
        """Obtiene el ID de la automatización."""
        return self.__id

    @property
    def name(self) -> str:
        """Obtiene el nombre de la automatización."""
        return self.__name

    @property
    def description(self) -> str:
        """Obtiene la descripción de la automatización."""
        return self.__description

    @property
    def active(self) -> bool:
        """Obtiene el estado de activación."""
        return self.__active

    @property
    def home(self) -> 'Home':
        """Obtiene el hogar de la automatización."""
        return self.__home

    @name.setter
    def name(self, value: str) -> None:
        """Establece el nombre de la automatización."""
        self.__name = value

    @description.setter
    def description(self, value: str) -> None:
        """Establece la descripción de la automatización."""
        self.__description = value

    def activate(self) -> None:
        """Activa la automatización."""
        self.__active = True

    def deactivate(self) -> None:
        """Desactiva la automatización."""
        self.__active = False

    def execute(self) -> None:
        """Ejecuta la automatización sobre los dispositivos asociados."""
        if self.__active:
            # Lógica de ejecución según dispositivos asociados
            pass