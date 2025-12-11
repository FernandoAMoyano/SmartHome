"""Servicio de autenticación y gestión de sesión."""

from typing import Optional
from dao.user_dao import UserDAO
from dao.role_dao import RoleDAO
from dominio.user import User
from utils.logger import get_auth_logger, log_user_action, log_validation_error
from utils.validators import (
    validar_credenciales_registro,
    validar_credenciales_login,
    limpiar_texto
)
from utils.exceptions import (
    DuplicateEntityException,
    EntityNotFoundException,
    InvalidCredentialsException,
    handle_exception
)

# Logger de autenticación
logger = get_auth_logger()


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
        try:
            # Limpiar datos de entrada
            email = limpiar_texto(email)
            name = limpiar_texto(name)
            
            # Validar credenciales de registro
            es_valido, mensaje = validar_credenciales_registro(email, password, name)
            if not es_valido:
                log_validation_error("registro", email, mensaje)
                return False, mensaje
            
            # Validar que el email no existe
            if self.user_dao.obtener_por_email(email):
                raise DuplicateEntityException("Usuario", email)
            
            # Obtener rol estándar (ID=2)
            role = self.role_dao.obtener_por_id(2)
            if not role:
                raise EntityNotFoundException("Rol estándar", 2)
            
            # Crear y registrar usuario
            usuario = User(email, password, name, role)
            
            if self.user_dao.insertar(usuario):
                log_user_action(email, "REGISTER", f"name={name}, role=standard")
                return True, "Usuario registrado exitosamente"
            else:
                logger.error(f"Fallo al registrar usuario: {email}")
                return False, "Error al registrar usuario en la base de datos"
                
        except (DuplicateEntityException, EntityNotFoundException) as e:
            return handle_exception(e, logger)
        except Exception as e:
            logger.error(f"Error inesperado en registro: {type(e).__name__} - {e}")
            return False, "Ha ocurrido un error inesperado durante el registro"
    
    def iniciar_sesion(self, email: str, password: str) -> tuple[bool, str]:
        """
        Valida credenciales e inicia sesión.
        
        Args:
            email: Email del usuario
            password: Contraseña
            
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        try:
            # Limpiar email
            email = limpiar_texto(email)
            
            # Validar credenciales básicas
            es_valido, mensaje = validar_credenciales_login(email, password)
            if not es_valido:
                log_validation_error("login", email, mensaje)
                return False, mensaje
            
            usuario = self.user_dao.validar_credenciales(email, password)
            
            if usuario:
                self.usuario_actual = usuario
                log_user_action(email, "LOGIN", f"role={usuario.role.name}")
                return True, f"Bienvenido {usuario.name}!"
            else:
                logger.warning(f"Intento de login fallido: {email}")
                raise InvalidCredentialsException()
                
        except InvalidCredentialsException as e:
            return handle_exception(e, logger)
        except Exception as e:
            logger.error(f"Error inesperado en login: {type(e).__name__} - {e}")
            return False, "Ha ocurrido un error inesperado durante el inicio de sesión"
    
    def cerrar_sesion(self) -> None:
        """Cierra la sesión actual."""
        if self.usuario_actual:
            log_user_action(self.usuario_actual.email, "LOGOUT", "")
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
            log_user_action(email, "ROLE_CHANGE", f"new_role={nuevo_rol.name}")
            return True, f"Rol cambiado exitosamente a {nuevo_rol.name}"
        else:
            logger.error(f"Fallo al cambiar rol de {email} a {nuevo_rol_id}")
            return False, "Error al cambiar rol"
    
    def listar_roles(self) -> list:
        """
        Obtiene todos los roles disponibles.
        
        Returns:
            Lista de objetos Role
        """
        return self.role_dao.obtener_todos()
