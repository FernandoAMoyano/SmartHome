"""Interface específica para operaciones de User DAO."""

from abc import abstractmethod
from typing import Optional
from .i_dao import IDao
from dominio.user import User


class IUserDao(IDao[User]):
    """Interface para operaciones específicas de Usuario."""
    
    @abstractmethod
    def obtener_por_email(self, email: str) -> Optional[User]:
        """
        Obtiene un usuario por su email.
        
        Args:
            email: Email del usuario
            
        Returns:
            Usuario encontrado o None
        """
        pass
    
    @abstractmethod
    def cambiar_rol(self, email: str, nuevo_rol_id: int) -> bool:
        """
        Cambia el rol de un usuario.
        
        Args:
            email: Email del usuario
            nuevo_rol_id: ID del nuevo rol
            
        Returns:
            True si se cambió correctamente
        """
        pass
    
    @abstractmethod
    def validar_credenciales(self, email: str, password: str) -> Optional[User]:
        """
        Valida las credenciales de un usuario.
        
        Args:
            email: Email del usuario
            password: Contraseña del usuario
            
        Returns:
            Usuario si las credenciales son válidas, None en caso contrario
        """
        pass