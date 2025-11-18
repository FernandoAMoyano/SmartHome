"""Paquete de interfaces DAO."""

from .i_dao import IDao
from .i_user_dao import IUserDao
from .i_device_dao import IDeviceDao

__all__ = ['IDao', 'IUserDao', 'IDeviceDao']