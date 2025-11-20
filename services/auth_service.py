"""Servicio de autenticación y gestión de sesión."""

from typing import Optional
from dao.user_dao import UserDAO
from dao.role_dao import RoleDAO
from dominio.user import User


class AuthService:
    """
    Servicio para autenticación y gestión de usuarios.
    
    Responsabilidades:
    - Registro de usuarios
    - Login/Logout
    - Validación de credenciales
    - Cambio de roles
    - Gestión de sesión
    """
    
    def __init__(self):
        """Inicializa el servicio de autenticación."""
        self.user_dao = UserDAO()
        self.role_dao = RoleDAO()
        self.usuario_actual: Optional[User] = None
    
    def registrar_usuario(self, email: str, password: str, name: str) -> tuple[bool, str]:
        """
        Registra un nuevo usuario estándar.
        
        Args:
            email: Email del usuario
            password: Contraseña
            name: Nombre completo
            
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        # Validar que el email no existe
        if self.user_dao.obtener_por_email(email):
            return False, "El email ya está registrado"
        
        # Validar campos vacíos
        if not email or not password or not name:
            return False, "Todos los campos son obligatorios"
        
        # Obtener rol estándar (ID=2)
        role = self.role_dao.obtener_por_id(2)
        if not role:
            return False, "Error: No se encontró el rol estándar"
        
        # Crear y registrar usuario
        usuario = User(email, password, name, role)
        
        if self.user_dao.insertar(usuario):
            return True, "Usuario registrado exitosamente"
        else:
            return False, "Error al registrar usuario"
    
    def iniciar_sesion(self, email: str, password: str) -> tuple[bool, str]:
        """
        Valida credenciales e inicia sesión.
        
        Args:
            email: Email del usuario
            password: Contraseña
            
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        # Validar campos vacíos
        if not email or not password:
            return False, "Email y contraseña son obligatorios"
        
        usuario = self.user_dao.validar_credenciales(email, password)
        
        if usuario:
            self.usuario_actual = usuario
            return True, f"Bienvenido {usuario.name}!"
        else:
            return False, "Credenciales inválidas"
    
    def cerrar_sesion(self) -> None:
        """Cierra la sesión actual."""
        self.usuario_actual = None
    
    def obtener_usuario_actual(self) -> Optional[User]:
        """
        Retorna el usuario actualmente autenticado.
        
        Returns:
            Usuario actual o None si no hay sesión activa
        """
        return self.usuario_actual
    
    def es_admin(self) -> bool:
        """
        Verifica si el usuario actual es administrador.
        
        Returns:
            True si es admin, False en caso contrario
        """
        return self.usuario_actual and self.usuario_actual.is_admin()
    
    def obtener_datos_usuario(self) -> dict:
        """
        Obtiene los datos del usuario actual.
        
        Returns:
            Diccionario con email, nombre y rol
        """
        if not self.usuario_actual:
            return {}
        
        return {
            'email': self.usuario_actual.email,
            'nombre': self.usuario_actual.name,
            'rol': self.usuario_actual.role.name
        }
    
    def cambiar_rol_usuario(self, email: str, nuevo_rol_id: int) -> tuple[bool, str]:
        """
        Cambia el rol de un usuario.
        
        Args:
            email: Email del usuario
            nuevo_rol_id: ID del nuevo rol
            
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        # Verificar que el usuario existe
        usuario = self.user_dao.obtener_por_email(email)
        
        if not usuario:
            return False, "Usuario no encontrado"
        
        # Verificar que el rol existe
        nuevo_rol = self.role_dao.obtener_por_id(nuevo_rol_id)
        if not nuevo_rol:
            return False, "Rol inválido"
        
        # Cambiar rol
        if self.user_dao.cambiar_rol(email, nuevo_rol_id):
            return True, f"Rol cambiado exitosamente a {nuevo_rol.name}"
        else:
            return False, "Error al cambiar rol"
    
    def listar_roles(self) -> list:
        """
        Obtiene todos los roles disponibles.
        
        Returns:
            Lista de objetos Role
        """
        return self.role_dao.obtener_todos()
