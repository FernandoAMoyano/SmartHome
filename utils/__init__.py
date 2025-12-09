"""Paquete de utilidades del sistema SmartHome."""

from .logger import (
    SmartHomeLogger,
    get_auth_logger,
    get_database_logger,
    get_device_logger,
    get_automation_logger,
    get_app_logger,
    log_user_action,
    log_database_error,
    log_validation_error,
    log_critical_error,
)

from .validators import (
    validar_email,
    validar_password,
    validar_password_fuerte,
    validar_nombre,
    validar_descripcion,
    validar_id_positivo,
    validar_credenciales_registro,
    validar_credenciales_login,
    limpiar_texto,
    ValidationError,
)

__all__ = [
    # Logging
    'SmartHomeLogger',
    'get_auth_logger',
    'get_database_logger',
    'get_device_logger',
    'get_automation_logger',
    'get_app_logger',
    'log_user_action',
    'log_database_error',
    'log_validation_error',
    'log_critical_error',
    # Validaciones
    'validar_email',
    'validar_password',
    'validar_password_fuerte',
    'validar_nombre',
    'validar_descripcion',
    'validar_id_positivo',
    'validar_credenciales_registro',
    'validar_credenciales_login',
    'limpiar_texto',
    'ValidationError',
]
