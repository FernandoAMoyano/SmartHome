"""Interface base para el patrón DAO."""

from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic

T = TypeVar('T')


class IDao(ABC, Generic[T]):
    """
    Interface genérica para Data Access Objects.
    
    Define las operaciones CRUD estándar.
    """
    
    @abstractmethod
    def insertar(self, entidad: T) -> bool:
        """
        Inserta una nueva entidad.
        
        Args:
            entidad: Objeto a insertar
            
        Returns:
            True si se insertó correctamente
        """
        pass
    
    @abstractmethod
    def modificar(self, entidad: T) -> bool:
        """
        Modifica una entidad existente.
        
        Args:
            entidad: Objeto con los datos actualizados
            
        Returns:
            True si se modificó correctamente
        """
        pass
    
    @abstractmethod
    def eliminar(self, id) -> bool:
        """
        Elimina una entidad por su identificador.
        
        Args:
            id: Identificador de la entidad
            
        Returns:
            True si se eliminó correctamente
        """
        pass
    
    @abstractmethod
    def obtener_por_id(self, id) -> Optional[T]:
        """
        Obtiene una entidad por su identificador.
        
        Args:
            id: Identificador de la entidad
            
        Returns:
            Objeto encontrado o None
        """
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[T]:
        """
        Obtiene todas las entidades.
        
        Returns:
            Lista de entidades
        """
        pass