"""Módulo de dominio para la entidad Role."""


class Role:
    """
    Representa un rol de usuario en el sistema.
    
    Atributos:
        id: Identificador único del rol
        name: Nombre del rol (ej: 'admin', 'standard')
    """
    
    def __init__(self, id: int, name: str):
        """
        Inicializa un nuevo rol.
        
        Args:
            id: Identificador del rol
            name: Nombre descriptivo del rol
        """
        self.__id = id
        self.__name = name

    @property
    def id(self) -> int:
        """Obtiene el ID del rol."""
        return self.__id

    @property
    def name(self) -> str:
        """Obtiene el nombre del rol."""
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        """Establece el nombre del rol."""
        self.__name = value