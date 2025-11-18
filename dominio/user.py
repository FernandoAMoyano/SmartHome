"""Módulo de dominio para la entidad User."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .role import Role

class User:
    """
    Representa un usuario del sistema SmartHome.
    
    Atributos:
        email: Correo electrónico único del usuario
        password: Contraseña encriptada
        name: Nombre completo del usuario
        role: Objeto Role asociado al usuario
    """
    
    def __init__(self, email: str, password: str, name: str, role: 'Role'):
        """
        Inicializa un nuevo usuario.
        
        Args:
            email: Correo electrónico del usuario
            password: Contraseña del usuario
            name: Nombre completo
            role: Objeto Role que define los permisos
        """
        self.__email = email
        self.__password = password
        self.__name = name
        self.__role = role

    @property
    def email(self) -> str:
        """Obtiene el email del usuario."""
        return self.__email

    @property
    def password(self) -> str:
        """Obtiene el password del usuario."""
        return self.__password

    @property
    def name(self) -> str:
        """Obtiene el nombre del usuario."""
        return self.__name

    @property
    def role(self) -> 'Role':
        """Obtiene el rol del usuario."""
        return self.__role

    @name.setter
    def name(self, value: str) -> None:
        """Establece el nombre del usuario."""
        self.__name = value

    @role.setter
    def role(self, value: 'Role') -> None:
        """Cambia el rol del usuario."""
        self.__role = value

    def validate_credentials(self, email: str, password: str) -> bool:
        """
        Valida las credenciales del usuario.
        
        Args:
            email: Email a validar
            password: Contraseña a validar
            
        Returns:
            True si las credenciales coinciden, False en caso contrario
        """
        return self.__email == email and self.__password == password

    def change_password(self, new_password: str) -> None:
        """
        Cambia la contraseña del usuario.
        
        Args:
            new_password: Nueva contraseña
        """
        self.__password = new_password

    def is_admin(self) -> bool:
        """
        Verifica si el usuario tiene rol de administrador.
        
        Returns:
            True si es admin, False en caso contrario
        """
        return self.__role.name.lower() == 'admin'