"""Módulo de dominio para la entidad Event."""

from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .device import Device
    from .user import User


class Event:
    """
    Representa un evento en el sistema SmartHome.
    
    Atributos:
        id: Identificador único del evento
        date_time_value: Fecha y hora del evento
        description: Descripción del evento
        device: Dispositivo asociado (opcional)
        user: Usuario que generó el evento (opcional)
        source: Origen del evento (manual/automático)
    """
    
    def __init__(
        self,
        id: int,
        description: str,
        source: str,
        device: Optional['Device'] = None,
        user: Optional['User'] = None,
        date_time_value: Optional[datetime] = None
    ):
        """
        Inicializa un nuevo evento.
        
        Args:
            id: Identificador del evento
            description: Descripción del evento
            source: Origen del evento
            device: Dispositivo asociado (opcional)
            user: Usuario que generó el evento (opcional)
            date_time_value: Fecha/hora (por defecto: ahora)
        """
        self.__id = id
        self.__date_time_value = date_time_value or datetime.now()
        self.__description = description
        self.__device = device
        self.__user = user
        self.__source = source

    @property
    def id(self) -> int:
        """Obtiene el ID del evento."""
        return self.__id

    @property
    def date_time_value(self) -> datetime:
        """Obtiene la fecha y hora del evento."""
        return self.__date_time_value

    @property
    def description(self) -> str:
        """Obtiene la descripción del evento."""
        return self.__description

    @property
    def device(self) -> Optional['Device']:
        """Obtiene el dispositivo asociado."""
        return self.__device

    @property
    def user(self) -> Optional['User']:
        """Obtiene el usuario asociado."""
        return self.__user

    @property
    def source(self) -> str:
        """Obtiene el origen del evento."""
        return self.__source

    @description.setter
    def description(self, value: str) -> None:
        """Establece la descripción del evento."""
        self.__description = value

    def log_event(self) -> str:
        """
        Genera una representación del evento para logging.
        
        Returns:
            String formateado con la información del evento
        """
        user_info = f"Usuario: {self.__user.email}" if self.__user else "Usuario: Sistema"
        device_info = f"Dispositivo: {self.__device.name}" if self.__device else "Dispositivo: N/A"
        
        return (
            f"[{self.__date_time_value.strftime('%Y-%m-%d %H:%M:%S')}] "
            f"{self.__description} | {user_info} | {device_info} | "
            f"Origen: {self.__source}"
        )