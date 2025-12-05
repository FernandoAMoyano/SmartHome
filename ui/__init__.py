"""
Capa de Presentación (UI Layer).

Esta capa contiene toda la interfaz de usuario,
separada completamente de la lógica de negocio.

Módulos:
- console_ui: Interfaz de usuario por consola (legacy)
- rich_console_ui: Interfaz de usuario mejorada con Rich (actual)
- rich_utils: Utilidades Rich reutilizables
"""

from .rich_console_ui import RichConsoleUI

__all__ = ["RichConsoleUI"]
