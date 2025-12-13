"""Servicio de gestión de automatizaciones."""

from typing import List, Optional, Dict
from dao.automation_dao import AutomationDAO
from dao.home_dao import HomeDAO
from dominio.automation import Automation
from utils.logger import get_automation_logger, log_validation_error
from utils.validators import validar_nombre, validar_descripcion, validar_id_positivo, limpiar_texto
from utils.exceptions import (
    EntityNotFoundException,
    AutomationNotFoundException,
    EntityStateException,
    DatabaseException,
    handle_exception
)

# Logger de automatizaciones
logger = get_automation_logger()


class AutomationService:
    """
    Servicio para gestión de automatizaciones domóticas.
    
    Responsabilidades:
    - CRUD de automatizaciones
    - Activación/Desactivación de automatizaciones
    - Consulta de automatizaciones por hogar
    - Gestión de automatizaciones activas
    """
    
    def __init__(self):
        """Inicializa el servicio de automatizaciones."""
        self.automation_dao = AutomationDAO()
        self.home_dao = HomeDAO()
    
    def crear_automatizacion(
        self,
        nombre: str,
        descripcion: str,
        home_id: int,
        activar: bool = True
    ) -> tuple[bool, str]:
        """
        Crea una nueva automatización.
        
        Args:
            nombre: Nombre de la automatización
            descripcion: Descripción de la función
            home_id: ID del hogar al que pertenece
            activar: Si debe estar activa inicialmente (default: True)
            
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        try:
            # Limpiar y validar nombre
            nombre = limpiar_texto(nombre)
            es_valido, mensaje = validar_nombre(nombre, "nombre de la automatización")
            if not es_valido:
                log_validation_error("automation_name", nombre, mensaje)
                return False, mensaje
            
            # Limpiar y validar descripción
            descripcion = limpiar_texto(descripcion)
            es_valido, mensaje = validar_descripcion(descripcion, min_length=10, max_length=500)
            if not es_valido:
                log_validation_error("automation_description", descripcion[:50], mensaje)
                return False, mensaje
            
            # Validar home_id
            es_valido, mensaje = validar_id_positivo(home_id, "home_id")
            if not es_valido:
                return False, mensaje
            
            # Validar que el hogar existe
            home = self.home_dao.obtener_por_id(home_id)
            if not home:
                raise EntityNotFoundException("Hogar", home_id)
            
            # Crear automatización
            automatizacion = Automation(
                id=0,  # Se auto-genera en BD
                name=nombre.strip(),
                description=descripcion.strip(),
                active=activar,
                home=home
            )
            
            if not self.automation_dao.insertar(automatizacion):
                raise DatabaseException(
                    "INSERT",
                    Exception("Fallo al insertar automatización"),
                    {"table": "automation", "name": nombre}
                )
            
            estado = "activa" if activar else "inactiva"
            logger.info(
                f"Automatización creada: {nombre} | home={home.name} | "
                f"active={activar} | description={descripcion[:50]}"
            )
            return True, f"Automatización creada exitosamente ({estado})"
            
        except EntityNotFoundException as e:
            return handle_exception(e, logger)
        except DatabaseException as e:
            return handle_exception(e, logger)
        except Exception as e:
            logger.error(f"Error inesperado al crear automatización: {e}")
            return False, "Error inesperado al crear automatización"
    
    def listar_automatizaciones(self) -> List[Automation]:
        """
        Obtiene todas las automatizaciones del sistema.
        
        Returns:
            Lista de automatizaciones
        """
        try:
            return self.automation_dao.obtener_todos()
        except Exception as e:
            logger.error(f"Error al listar automatizaciones: {e}")
            return []
    
    def obtener_automatizacion(self, automation_id: int) -> Optional[Automation]:
        """
        Obtiene una automatización por ID.
        
        Args:
            automation_id: ID de la automatización
            
        Returns:
            Automatización encontrada o None
        """
        try:
            automatizacion = self.automation_dao.obtener_por_id(automation_id)
            if not automatizacion:
                raise AutomationNotFoundException(automation_id)
            return automatizacion
        except AutomationNotFoundException:
            # No logueamos como error, es un caso normal
            return None
        except Exception as e:
            logger.error(f"Error al obtener automatización {automation_id}: {e}")
            return None
    
    def obtener_automatizaciones_hogar(self, home_id: int) -> List[Automation]:
        """
        Obtiene todas las automatizaciones de un hogar.
        
        Args:
            home_id: ID del hogar
            
        Returns:
            Lista de automatizaciones del hogar
        """
        try:
            return self.automation_dao.obtener_por_hogar(home_id)
        except Exception as e:
            logger.error(f"Error al obtener automatizaciones del hogar {home_id}: {e}")
            return []
    
    def obtener_automatizaciones_activas(self, home_id: int) -> List[Automation]:
        """
        Obtiene solo las automatizaciones activas de un hogar.
        
        Args:
            home_id: ID del hogar
            
        Returns:
            Lista de automatizaciones activas
        """
        try:
            return self.automation_dao.obtener_activas(home_id)
        except Exception as e:
            logger.error(f"Error al obtener automatizaciones activas del hogar {home_id}: {e}")
            return []
    
    def obtener_automatizaciones_usuario(
        self, 
        email_usuario: str
    ) -> Dict[str, List[Automation]]:
        """
        Obtiene todas las automatizaciones organizadas por hogar para un usuario.
        
        Args:
            email_usuario: Email del usuario
            
        Returns:
            Diccionario con hogares como claves y listas de automatizaciones como valores
        """
        try:
            hogares = self.home_dao.obtener_hogares_usuario(email_usuario)
            resultado = {}
            
            for hogar in hogares:
                automatizaciones = self.automation_dao.obtener_por_hogar(hogar.id)
                resultado[hogar.name] = automatizaciones
            
            return resultado
        except Exception as e:
            logger.error(f"Error al obtener automatizaciones del usuario {email_usuario}: {e}")
            return {}
    
    def actualizar_automatizacion(
        self,
        automation_id: int,
        nuevo_nombre: Optional[str] = None,
        nueva_descripcion: Optional[str] = None
    ) -> tuple[bool, str]:
        """
        Actualiza una automatización existente.
        
        Args:
            automation_id: ID de la automatización
            nuevo_nombre: Nuevo nombre (opcional)
            nueva_descripcion: Nueva descripción (opcional)
            
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        try:
            # Obtener automatización
            automatizacion = self.automation_dao.obtener_por_id(automation_id)
            if not automatizacion:
                raise AutomationNotFoundException(automation_id)
            
            # Validar que al menos se actualice algo
            if not nuevo_nombre and not nueva_descripcion:
                return False, "No hay cambios para aplicar"
            
            # Actualizar nombre si se proporciona
            if nuevo_nombre:
                nuevo_nombre = limpiar_texto(nuevo_nombre)
                es_valido, mensaje = validar_nombre(nuevo_nombre, "nombre de la automatización")
                if not es_valido:
                    log_validation_error("automation_name", nuevo_nombre, mensaje)
                    return False, mensaje
                automatizacion.name = nuevo_nombre
            
            # Actualizar descripción si se proporciona
            if nueva_descripcion:
                nueva_descripcion = limpiar_texto(nueva_descripcion)
                es_valido, mensaje = validar_descripcion(nueva_descripcion, min_length=10, max_length=500)
                if not es_valido:
                    log_validation_error("automation_description", nueva_descripcion[:50], mensaje)
                    return False, mensaje
                automatizacion.description = nueva_descripcion
            
            # Guardar cambios
            if not self.automation_dao.modificar(automatizacion):
                raise DatabaseException(
                    "UPDATE",
                    Exception("Fallo al actualizar automatización"),
                    {"table": "automation", "id": automation_id}
                )
            
            logger.info(
                f"Automatización actualizada: ID={automation_id} | "
                f"new_name={nuevo_nombre or 'sin cambios'} | "
                f"new_description={nueva_descripcion[:30] if nueva_descripcion else 'sin cambios'}"
            )
            return True, "Automatización actualizada exitosamente"
            
        except AutomationNotFoundException as e:
            return handle_exception(e, logger)
        except DatabaseException as e:
            return handle_exception(e, logger)
        except Exception as e:
            logger.error(f"Error inesperado al actualizar automatización: {e}")
            return False, "Error inesperado al actualizar automatización"
    
    def eliminar_automatizacion(self, automation_id: int) -> tuple[bool, str]:
        """
        Elimina una automatización.
        
        Args:
            automation_id: ID de la automatización a eliminar
            
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        try:
            # Verificar que la automatización existe
            automatizacion = self.automation_dao.obtener_por_id(automation_id)
            if not automatizacion:
                raise AutomationNotFoundException(automation_id)
            
            # Eliminar automatización
            if not self.automation_dao.eliminar(automation_id):
                raise DatabaseException(
                    "DELETE",
                    Exception("Fallo al eliminar automatización"),
                    {"table": "automation", "id": automation_id}
                )
            
            logger.info(
                f"Automatización eliminada: ID={automation_id} | "
                f"name={automatizacion.name} | home={automatizacion.home.name}"
            )
            return True, f"Automatización '{automatizacion.name}' eliminada exitosamente"
            
        except AutomationNotFoundException as e:
            return handle_exception(e, logger)
        except DatabaseException as e:
            return handle_exception(e, logger)
        except Exception as e:
            logger.error(f"Error inesperado al eliminar automatización: {e}")
            return False, "Error inesperado al eliminar automatización"
    
    def activar_automatizacion(self, automation_id: int) -> tuple[bool, str]:
        """
        Activa una automatización.
        
        Args:
            automation_id: ID de la automatización
            
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        try:
            # Verificar que la automatización existe
            automatizacion = self.automation_dao.obtener_por_id(automation_id)
            if not automatizacion:
                raise AutomationNotFoundException(automation_id)
            
            # Verificar si ya está activa
            if automatizacion.active:
                raise EntityStateException(
                    "Automatización",
                    "Ya está activa"
                )
            
            # Activar
            if not self.automation_dao.cambiar_estado(automation_id, True):
                raise DatabaseException(
                    "UPDATE",
                    Exception("Fallo al activar automatización"),
                    {"table": "automation", "id": automation_id, "action": "activate"}
                )
            
            logger.info(
                f"Automatización activada: ID={automation_id} | "
                f"name={automatizacion.name}"
            )
            return True, f"Automatización '{automatizacion.name}' activada exitosamente"
            
        except AutomationNotFoundException as e:
            return handle_exception(e, logger)
        except EntityStateException as e:
            return handle_exception(e, logger)
        except DatabaseException as e:
            return handle_exception(e, logger)
        except Exception as e:
            logger.error(f"Error inesperado al activar automatización: {e}")
            return False, "Error inesperado al activar automatización"
    
    def desactivar_automatizacion(self, automation_id: int) -> tuple[bool, str]:
        """
        Desactiva una automatización.
        
        Args:
            automation_id: ID de la automatización
            
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        try:
            # Verificar que la automatización existe
            automatizacion = self.automation_dao.obtener_por_id(automation_id)
            if not automatizacion:
                raise AutomationNotFoundException(automation_id)
            
            # Verificar si ya está inactiva
            if not automatizacion.active:
                raise EntityStateException(
                    "Automatización",
                    "Ya está inactiva"
                )
            
            # Desactivar
            if not self.automation_dao.cambiar_estado(automation_id, False):
                raise DatabaseException(
                    "UPDATE",
                    Exception("Fallo al desactivar automatización"),
                    {"table": "automation", "id": automation_id, "action": "deactivate"}
                )
            
            logger.info(
                f"Automatización desactivada: ID={automation_id} | "
                f"name={automatizacion.name}"
            )
            return True, f"Automatización '{automatizacion.name}' desactivada exitosamente"
            
        except AutomationNotFoundException as e:
            return handle_exception(e, logger)
        except EntityStateException as e:
            return handle_exception(e, logger)
        except DatabaseException as e:
            return handle_exception(e, logger)
        except Exception as e:
            logger.error(f"Error inesperado al desactivar automatización: {e}")
            return False, "Error inesperado al desactivar automatización"
    
    def cambiar_estado_automatizacion(
        self, 
        automation_id: int, 
        activar: bool
    ) -> tuple[bool, str]:
        """
        Cambia el estado de una automatización (activar o desactivar).
        
        Args:
            automation_id: ID de la automatización
            activar: True para activar, False para desactivar
            
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        if activar:
            return self.activar_automatizacion(automation_id)
        else:
            return self.desactivar_automatizacion(automation_id)
    
    def obtener_resumen_automatizaciones(self, home_id: int) -> Dict[str, int]:
        """
        Obtiene un resumen estadístico de las automatizaciones de un hogar.
        
        Args:
            home_id: ID del hogar
            
        Returns:
            Diccionario con estadísticas
        """
        try:
            todas = self.automation_dao.obtener_por_hogar(home_id)
            activas = self.automation_dao.obtener_activas(home_id)
            
            return {
                'total': len(todas),
                'activas': len(activas),
                'inactivas': len(todas) - len(activas)
            }
        except Exception as e:
            logger.error(f"Error al obtener resumen de automatizaciones del hogar {home_id}: {e}")
            return {
                'total': 0,
                'activas': 0,
                'inactivas': 0
            }
