"""
Capa de Servicios (Service Layer).

Esta capa contiene la lógica de negocio de la aplicación,
separada de la presentación (UI) y del acceso a datos (DAO).

Módulos:
- auth_service: Autenticación y gestión de usuarios
- device_service: Gestión de dispositivos inteligentes
- home_service: Gestión de hogares
"""

from .auth_service import AuthService
from .device_service import DeviceService

__all__ = ['AuthService', 'DeviceService']
