"""Servicio de gestión de dispositivos."""

from typing import List, Optional, Dict
from dao.device_dao import DeviceDAO
from dao.home_dao import HomeDAO
from dao.state_dao import StateDAO
from dao.device_type_dao import DeviceTypeDAO
from dao.location_dao import LocationDAO
from dominio.device import Device
from utils.logger import get_device_logger, log_validation_error
from utils.validators import validar_nombre, validar_id_positivo, limpiar_texto
from utils.exceptions import (
    EntityNotFoundException,
    DeviceNotFoundException,
    DatabaseException,
    handle_exception
)

# Logger de dispositivos
logger = get_device_logger()


class DeviceService:
    """
    Servicio para gestión de dispositivos inteligentes.

    Responsabilidades:
    - CRUD de dispositivos
    - Búsqueda y filtrado
    - Cambio de estados
    - Obtención de opciones de configuración
    """

    def __init__(self):
        """Inicializa el servicio de dispositivos."""
        self.device_dao = DeviceDAO()
        self.home_dao = HomeDAO()
        self.state_dao = StateDAO()
        self.device_type_dao = DeviceTypeDAO()
        self.location_dao = LocationDAO()

    def crear_dispositivo(
        self, nombre: str, home_id: int, type_id: int, location_id: int, state_id: int
    ) -> tuple[bool, str]:
        """
        Crea un nuevo dispositivo.

        Args:
            nombre: Nombre del dispositivo
            home_id: ID del hogar
            type_id: ID del tipo de dispositivo
            location_id: ID de la ubicación
            state_id: ID del estado

        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        try:
            # Limpiar y validar nombre
            nombre = limpiar_texto(nombre)
            es_valido, mensaje = validar_nombre(nombre, "nombre del dispositivo")
            if not es_valido:
                log_validation_error("device_name", nombre, mensaje)
                return False, mensaje
            
            # Validar IDs
            es_valido, mensaje = validar_id_positivo(home_id, "home_id")
            if not es_valido:
                return False, mensaje
            
            es_valido, mensaje = validar_id_positivo(type_id, "type_id")
            if not es_valido:
                return False, mensaje
            
            es_valido, mensaje = validar_id_positivo(location_id, "location_id")
            if not es_valido:
                return False, mensaje
            
            es_valido, mensaje = validar_id_positivo(state_id, "state_id")
            if not es_valido:
                return False, mensaje

            # Obtener entidades relacionadas
            home = self.home_dao.obtener_por_id(home_id)
            if not home:
                raise EntityNotFoundException("Hogar", home_id)
            
            device_type = self.device_type_dao.obtener_por_id(type_id)
            if not device_type:
                raise EntityNotFoundException("Tipo de dispositivo", type_id)
            
            location = self.location_dao.obtener_por_id(location_id)
            if not location:
                raise EntityNotFoundException("Ubicación", location_id)
            
            state = self.state_dao.obtener_por_id(state_id)
            if not state:
                raise EntityNotFoundException("Estado", state_id)

            # Crear dispositivo
            dispositivo = Device(0, nombre, state, device_type, location, home)

            if not self.device_dao.insertar(dispositivo):
                raise DatabaseException(
                    "INSERT",
                    Exception("Fallo al insertar dispositivo"),
                    {"table": "device", "name": nombre}
                )
            
            logger.info(
                f"Dispositivo creado: {nombre} | home={home.name} | "
                f"type={device_type.name} | location={location.name}"
            )
            return True, "Dispositivo creado exitosamente"
            
        except EntityNotFoundException as e:
            return handle_exception(e, logger)
        except DatabaseException as e:
            return handle_exception(e, logger)
        except Exception as e:
            logger.error(f"Error inesperado al crear dispositivo: {e}")
            return False, "Error inesperado al crear dispositivo"

    def listar_dispositivos(self) -> List[Device]:
        """
        Obtiene todos los dispositivos.

        Returns:
            Lista de dispositivos
        """
        try:
            return self.device_dao.obtener_todos()
        except Exception as e:
            logger.error(f"Error al listar dispositivos: {e}")
            return []

    def obtener_dispositivo(self, device_id: int) -> Optional[Device]:
        """
        Obtiene un dispositivo por ID.

        Args:
            device_id: ID del dispositivo

        Returns:
            Dispositivo encontrado o None
        """
        try:
            dispositivo = self.device_dao.obtener_por_id(device_id)
            if not dispositivo:
                raise DeviceNotFoundException(device_id)
            return dispositivo
        except DeviceNotFoundException:
            # No logueamos como error, es un caso normal
            return None
        except Exception as e:
            logger.error(f"Error al obtener dispositivo {device_id}: {e}")
            return None

    def actualizar_dispositivo(
        self,
        device_id: int,
        nuevo_nombre: Optional[str] = None,
        nuevo_estado_id: Optional[int] = None,
    ) -> tuple[bool, str]:
        """
        Actualiza un dispositivo existente.

        Args:
            device_id: ID del dispositivo
            nuevo_nombre: Nuevo nombre (opcional)
            nuevo_estado_id: ID del nuevo estado (opcional)

        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        try:
            # Obtener dispositivo
            dispositivo = self.device_dao.obtener_por_id(device_id)
            if not dispositivo:
                raise DeviceNotFoundException(device_id)

            # Validar que al menos se actualice algo
            if not nuevo_nombre and not nuevo_estado_id:
                return False, "No hay cambios para aplicar"

            # Actualizar nombre si se proporciona
            if nuevo_nombre:
                nuevo_nombre = limpiar_texto(nuevo_nombre)
                es_valido, mensaje = validar_nombre(nuevo_nombre, "nombre del dispositivo")
                if not es_valido:
                    log_validation_error("device_name", nuevo_nombre, mensaje)
                    return False, mensaje
                dispositivo.name = nuevo_nombre

            # Actualizar estado si se proporciona
            if nuevo_estado_id:
                nuevo_estado = self.state_dao.obtener_por_id(nuevo_estado_id)
                if not nuevo_estado:
                    raise EntityNotFoundException("Estado", nuevo_estado_id)
                dispositivo.state = nuevo_estado

            # Guardar cambios
            if not self.device_dao.modificar(dispositivo):
                raise DatabaseException(
                    "UPDATE",
                    Exception("Fallo al actualizar dispositivo"),
                    {"table": "device", "id": device_id}
                )
            
            logger.info(
                f"Dispositivo actualizado: ID={device_id} | "
                f"new_name={nuevo_nombre or 'sin cambios'} | "
                f"new_state={nuevo_estado_id or 'sin cambios'}"
            )
            return True, "Dispositivo actualizado exitosamente"
            
        except DeviceNotFoundException as e:
            return handle_exception(e, logger)
        except EntityNotFoundException as e:
            return handle_exception(e, logger)
        except DatabaseException as e:
            return handle_exception(e, logger)
        except Exception as e:
            logger.error(f"Error inesperado al actualizar dispositivo: {e}")
            return False, "Error inesperado al actualizar dispositivo"

    def eliminar_dispositivo(self, device_id: int) -> tuple[bool, str]:
        """
        Elimina un dispositivo.

        Args:
            device_id: ID del dispositivo a eliminar

        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        try:
            # Verificar que el dispositivo existe
            dispositivo = self.device_dao.obtener_por_id(device_id)
            if not dispositivo:
                raise DeviceNotFoundException(device_id)

            # Eliminar dispositivo
            if not self.device_dao.eliminar(device_id):
                raise DatabaseException(
                    "DELETE",
                    Exception("Fallo al eliminar dispositivo"),
                    {"table": "device", "id": device_id}
                )
            
            logger.info(
                f"Dispositivo eliminado: ID={device_id} | "
                f"name={dispositivo.name} | home={dispositivo.home.name}"
            )
            return True, f"Dispositivo '{dispositivo.name}' eliminado exitosamente"
            
        except DeviceNotFoundException as e:
            return handle_exception(e, logger)
        except DatabaseException as e:
            return handle_exception(e, logger)
        except Exception as e:
            logger.error(f"Error inesperado al eliminar dispositivo: {e}")
            return False, "Error inesperado al eliminar dispositivo"

    def obtener_dispositivos_por_hogar(self, home_id: int) -> List[Device]:
        """
        Obtiene dispositivos de un hogar específico.

        Args:
            home_id: ID del hogar

        Returns:
            Lista de dispositivos del hogar
        """
        try:
            return self.device_dao.obtener_por_hogar(home_id)
        except Exception as e:
            logger.error(f"Error al obtener dispositivos del hogar {home_id}: {e}")
            return []

    def buscar_dispositivos_por_nombre(self, nombre: str, home_id: int) -> List[Device]:
        """
        Busca dispositivos por nombre en un hogar.

        Args:
            nombre: Texto a buscar
            home_id: ID del hogar

        Returns:
            Lista de dispositivos que coinciden
        """
        try:
            return self.device_dao.buscar_por_nombre(nombre, home_id)
        except Exception as e:
            logger.error(f"Error al buscar dispositivos: {e}")
            return []

    def cambiar_estado_dispositivo(
        self, device_id: int, nuevo_estado_id: int
    ) -> tuple[bool, str]:
        """
        Cambia el estado de un dispositivo.

        Args:
            device_id: ID del dispositivo
            nuevo_estado_id: ID del nuevo estado

        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        try:
            # Verificar que el dispositivo existe
            dispositivo = self.device_dao.obtener_por_id(device_id)
            if not dispositivo:
                raise DeviceNotFoundException(device_id)

            # Verificar que el estado existe
            estado = self.state_dao.obtener_por_id(nuevo_estado_id)
            if not estado:
                raise EntityNotFoundException("Estado", nuevo_estado_id)

            # Cambiar estado
            if not self.device_dao.cambiar_estado(device_id, nuevo_estado_id):
                raise DatabaseException(
                    "UPDATE",
                    Exception("Fallo al cambiar estado"),
                    {"table": "device", "id": device_id, "state_id": nuevo_estado_id}
                )
            
            logger.info(
                f"Estado cambiado: device_id={device_id} | "
                f"device={dispositivo.name} | new_state={estado.name}"
            )
            return True, f"Estado cambiado a '{estado.name}'"
            
        except DeviceNotFoundException as e:
            return handle_exception(e, logger)
        except EntityNotFoundException as e:
            return handle_exception(e, logger)
        except DatabaseException as e:
            return handle_exception(e, logger)
        except Exception as e:
            logger.error(f"Error inesperado al cambiar estado: {e}")
            return False, "Error inesperado al cambiar estado"

    def obtener_opciones_configuracion(self) -> Dict[str, List]:
        """
        Obtiene todas las opciones para configurar dispositivos.

        Returns:
            Diccionario con hogares, tipos, ubicaciones y estados
        """
        try:
            return {
                "hogares": self.home_dao.obtener_todos(),
                "tipos": self.device_type_dao.obtener_todos(),
                "ubicaciones": self.location_dao.obtener_todos(),
                "estados": self.state_dao.obtener_todos(),
            }
        except Exception as e:
            logger.error(f"Error al obtener opciones de configuración: {e}")
            return {
                "hogares": [],
                "tipos": [],
                "ubicaciones": [],
                "estados": []
            }

    def obtener_dispositivos_usuario(
        self, email_usuario: str
    ) -> Dict[str, List[Device]]:
        """
        Obtiene todos los dispositivos organizados por hogar para un usuario.

        Args:
            email_usuario: Email del usuario

        Returns:
            Diccionario con hogares como claves y listas de dispositivos como valores
        """
        try:
            hogares = self.home_dao.obtener_hogares_usuario(email_usuario)
            resultado = {}

            for hogar in hogares:
                dispositivos = self.device_dao.obtener_por_hogar(hogar.id)
                resultado[hogar.name] = dispositivos

            return resultado
        except Exception as e:
            logger.error(f"Error al obtener dispositivos del usuario {email_usuario}: {e}")
            return {}
