"""
Módulo de excepciones personalizadas para el sistema SmartHome.

Define excepciones específicas para diferentes tipos de errores
del sistema, permitiendo un manejo más granular y preciso.
"""


# ============================================
# EXCEPCIONES BASE
# ============================================

class SmartHomeException(Exception):
    """Excepción base para todas las excepciones del sistema SmartHome."""
    
    def __init__(self, message: str, details: str = ""):
        """
        Inicializa la excepción.
        
        Args:
            message: Mensaje principal de error
            details: Detalles adicionales opcionales
        """
        self.message = message
        self.details = details
        super().__init__(self.message)
    
    def __str__(self):
        """Representación en string de la excepción."""
        if self.details:
            return f"{self.message} | Detalles: {self.details}"
        return self.message


# ============================================
# EXCEPCIONES DE VALIDACIÓN
# ============================================

class ValidationException(SmartHomeException):
    """Excepción para errores de validación de datos."""
    pass


class InvalidEmailException(ValidationException):
    """Excepción cuando el formato de email es inválido."""
    
    def __init__(self, email: str):
        super().__init__(
            f"Email inválido: {email}",
            "El email debe tener el formato: usuario@dominio.com"
        )


class InvalidPasswordException(ValidationException):
    """Excepción cuando la contraseña no cumple los requisitos."""
    
    def __init__(self, reason: str = "La contraseña no cumple los requisitos"):
        super().__init__(reason)


class InvalidNameException(ValidationException):
    """Excepción cuando un nombre es inválido."""
    
    def __init__(self, field: str, reason: str):
        super().__init__(
            f"Nombre inválido en campo '{field}'",
            reason
        )


# ============================================
# EXCEPCIONES DE BASE DE DATOS
# ============================================

class DatabaseException(SmartHomeException):
    """Excepción base para errores relacionados con la base de datos."""
    pass


class ConnectionException(DatabaseException):
    """Excepción cuando no se puede conectar a la base de datos."""
    
    def __init__(self, details: str = ""):
        super().__init__(
            "No se pudo establecer conexión con la base de datos",
            details
        )


class QueryException(DatabaseException):
    """Excepción cuando falla una consulta a la base de datos."""
    
    def __init__(self, operation: str, details: str = ""):
        super().__init__(
            f"Error al ejecutar operación: {operation}",
            details
        )


class TransactionException(DatabaseException):
    """Excepción cuando falla una transacción."""
    
    def __init__(self, details: str = ""):
        super().__init__(
            "Error en la transacción de base de datos",
            details
        )


# ============================================
# EXCEPCIONES DE ENTIDADES
# ============================================

class EntityException(SmartHomeException):
    """Excepción base para errores relacionados con entidades."""
    pass


class EntityNotFoundException(EntityException):
    """Excepción cuando no se encuentra una entidad."""
    
    def __init__(self, entity_type: str, entity_id):
        super().__init__(
            f"{entity_type} no encontrado",
            f"ID: {entity_id}"
        )


class DuplicateEntityException(EntityException):
    """Excepción cuando se intenta crear una entidad duplicada."""
    
    def __init__(self, entity_type: str, identifier: str):
        super().__init__(
            f"{entity_type} duplicado",
            f"Ya existe: {identifier}"
        )


class EntityStateException(EntityException):
    """Excepción cuando el estado de una entidad no permite la operación."""
    
    def __init__(self, entity_type: str, reason: str):
        super().__init__(
            f"Estado inválido para {entity_type}",
            reason
        )


# ============================================
# EXCEPCIONES DE AUTENTICACIÓN
# ============================================

class AuthenticationException(SmartHomeException):
    """Excepción base para errores de autenticación."""
    pass


class InvalidCredentialsException(AuthenticationException):
    """Excepción cuando las credenciales son inválidas."""
    
    def __init__(self):
        super().__init__("Email o contraseña incorrectos")


class UnauthorizedException(AuthenticationException):
    """Excepción cuando el usuario no tiene permisos."""
    
    def __init__(self, action: str):
        super().__init__(
            "Acceso denegado",
            f"No tienes permisos para: {action}"
        )


class SessionExpiredException(AuthenticationException):
    """Excepción cuando la sesión ha expirado."""
    
    def __init__(self):
        super().__init__("La sesión ha expirado. Por favor, inicia sesión nuevamente")


# ============================================
# EXCEPCIONES DE DISPOSITIVOS
# ============================================

class DeviceException(SmartHomeException):
    """Excepción base para errores de dispositivos."""
    pass


class DeviceNotFoundException(DeviceException):
    """Excepción cuando no se encuentra un dispositivo."""
    
    def __init__(self, device_id: int):
        super().__init__(
            "Dispositivo no encontrado",
            f"ID: {device_id}"
        )


class DeviceStateException(DeviceException):
    """Excepción cuando el estado del dispositivo no permite la operación."""
    
    def __init__(self, device_name: str, reason: str):
        super().__init__(
            f"No se puede operar el dispositivo '{device_name}'",
            reason
        )


class DeviceConnectionException(DeviceException):
    """Excepción cuando falla la conexión con un dispositivo físico."""
    
    def __init__(self, device_name: str, details: str = ""):
        super().__init__(
            f"Error de conexión con dispositivo '{device_name}'",
            details
        )


# ============================================
# EXCEPCIONES DE AUTOMATIZACIONES
# ============================================

class AutomationException(SmartHomeException):
    """Excepción base para errores de automatizaciones."""
    pass


class AutomationNotFoundException(AutomationException):
    """Excepción cuando no se encuentra una automatización."""
    
    def __init__(self, automation_id: int):
        super().__init__(
            "Automatización no encontrada",
            f"ID: {automation_id}"
        )


class AutomationExecutionException(AutomationException):
    """Excepción cuando falla la ejecución de una automatización."""
    
    def __init__(self, automation_name: str, details: str = ""):
        super().__init__(
            f"Error al ejecutar automatización '{automation_name}'",
            details
        )


# ============================================
# EXCEPCIONES DE CONFIGURACIÓN
# ============================================

class ConfigurationException(SmartHomeException):
    """Excepción para errores de configuración."""
    pass


class MissingConfigException(ConfigurationException):
    """Excepción cuando falta configuración requerida."""
    
    def __init__(self, config_key: str):
        super().__init__(
            f"Configuración faltante: {config_key}",
            "Verifica tu archivo .env"
        )


class InvalidConfigException(ConfigurationException):
    """Excepción cuando la configuración es inválida."""
    
    def __init__(self, config_key: str, reason: str):
        super().__init__(
            f"Configuración inválida: {config_key}",
            reason
        )


# ============================================
# FUNCIONES AUXILIARES
# ============================================

def handle_exception(exception: Exception, logger=None) -> tuple[bool, str]:
    """
    Maneja una excepción de forma centralizada.
    
    Args:
        exception: Excepción a manejar
        logger: Logger opcional para registrar el error
        
    Returns:
        Tupla (éxito: False, mensaje_usuario: str)
    """
    # Si es una excepción personalizada de SmartHome
    if isinstance(exception, SmartHomeException):
        if logger:
            logger.error(f"{exception.message} | {exception.details}")
        return False, exception.message
    
    # Si es una excepción estándar de Python
    error_message = "Ha ocurrido un error inesperado"
    
    if logger:
        logger.error(f"Excepción no controlada: {type(exception).__name__} - {str(exception)}")
    
    return False, error_message


def raise_if_none(value, exception: Exception):
    """
    Lanza una excepción si el valor es None.
    
    Args:
        value: Valor a verificar
        exception: Excepción a lanzar si value es None
        
    Raises:
        Exception: La excepción proporcionada si value es None
    """
    if value is None:
        raise exception
    return value
