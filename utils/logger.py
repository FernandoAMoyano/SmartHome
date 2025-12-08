"""
Sistema de Logging Profesional para SmartHome.

Registra todas las acciones importantes del sistema en archivos rotativos.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


class SmartHomeLogger:
    """
    Configurador de logging para el sistema SmartHome.

    Características:
    - Logs rotativos (max 5MB por archivo)
    - Múltiples niveles (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    - Formato profesional con timestamp
    - Logs separados por categoría (app, db, errors)
    """

    # Directorio de logs
    LOG_DIR = Path("logs")

    # Formato de logs
    LOG_FORMAT = "[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    # Configuración de rotación
    MAX_BYTES = 5 * 1024 * 1024  # 5 MB
    BACKUP_COUNT = 5  # Mantener 5 archivos históricos

    _initialized = False

    @classmethod
    def setup(cls):
        """Inicializa el sistema de logging."""
        if cls._initialized:
            return

        # Crear directorio de logs si no existe
        cls.LOG_DIR.mkdir(exist_ok=True)

        # Configurar logging raíz
        logging.basicConfig(
            level=logging.INFO, format=cls.LOG_FORMAT, datefmt=cls.DATE_FORMAT
        )

        cls._initialized = True

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """
        Obtiene un logger configurado.

        Args:
            name: Nombre del logger (ej: 'auth', 'database', 'devices')

        Returns:
            Logger configurado con handlers
        """
        cls.setup()

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # Evitar duplicar handlers
        if logger.handlers:
            return logger

        # Handler para archivo general (app.log)
        app_handler = RotatingFileHandler(
            cls.LOG_DIR / "app.log",
            maxBytes=cls.MAX_BYTES,
            backupCount=cls.BACKUP_COUNT,
            encoding="utf-8",
        )
        app_handler.setLevel(logging.INFO)
        app_handler.setFormatter(logging.Formatter(cls.LOG_FORMAT, cls.DATE_FORMAT))

        # Handler para errores (errors.log)
        error_handler = RotatingFileHandler(
            cls.LOG_DIR / "errors.log",
            maxBytes=cls.MAX_BYTES,
            backupCount=cls.BACKUP_COUNT,
            encoding="utf-8",
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(logging.Formatter(cls.LOG_FORMAT, cls.DATE_FORMAT))

        # Handler para consola (solo errores)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))

        # Agregar handlers
        logger.addHandler(app_handler)
        logger.addHandler(error_handler)
        logger.addHandler(console_handler)

        return logger


# ============================================
# LOGGERS ESPECÍFICOS DEL SISTEMA
# ============================================


def get_auth_logger():
    """Logger para autenticación y usuarios."""
    return SmartHomeLogger.get_logger("auth")


def get_database_logger():
    """Logger para operaciones de base de datos."""
    return SmartHomeLogger.get_logger("database")


def get_device_logger():
    """Logger para gestión de dispositivos."""
    return SmartHomeLogger.get_logger("devices")


def get_automation_logger():
    """Logger para automatizaciones."""
    return SmartHomeLogger.get_logger("automations")


def get_app_logger():
    """Logger general de la aplicación."""
    return SmartHomeLogger.get_logger("app")


# ============================================
# FUNCIONES DE CONVENIENCIA
# ============================================


def log_user_action(user_email: str, action: str, details: str = ""):
    """
    Registra una acción de usuario.

    Args:
        user_email: Email del usuario
        action: Acción realizada (LOGIN, CREATE_DEVICE, etc.)
        details: Detalles adicionales
    """
    logger = get_auth_logger()
    message = f"USER_ACTION | {user_email} | {action}"
    if details:
        message += f" | {details}"
    logger.info(message)


def log_database_error(operation: str, error: Exception, details: str = ""):
    """
    Registra un error de base de datos.

    Args:
        operation: Operación que falló (INSERT, UPDATE, etc.)
        error: Excepción capturada
        details: Detalles adicionales
    """
    logger = get_database_logger()
    message = f"DB_ERROR | {operation} | {str(error)}"
    if details:
        message += f" | {details}"
    logger.error(message, exc_info=True)


def log_validation_error(field: str, value: str, reason: str):
    """
    Registra un error de validación.

    Args:
        field: Campo que falló
        value: Valor que se intentó validar
        reason: Razón del fallo
    """
    logger = get_app_logger()
    logger.warning(f"VALIDATION_ERROR | {field} | {value} | {reason}")


def log_critical_error(component: str, error: Exception, context: str = ""):
    """
    Registra un error crítico del sistema.

    Args:
        component: Componente donde ocurrió el error
        error: Excepción capturada
        context: Contexto adicional
    """
    logger = get_app_logger()
    message = f"CRITICAL_ERROR | {component} | {str(error)}"
    if context:
        message += f" | {context}"
    logger.critical(message, exc_info=True)


# Inicializar logging al importar el módulo
SmartHomeLogger.setup()
