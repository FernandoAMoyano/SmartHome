"""Servicio de gestión de automatizaciones."""

from typing import List, Optional, Dict
from dao.automation_dao import AutomationDAO
from dao.home_dao import HomeDAO
from dominio.automation import Automation
from utils.logger import get_automation_logger

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
        # Validar nombre no vacío
        if not nombre or not nombre.strip():
            return False, "El nombre de la automatización es obligatorio"
        
        # Validar descripción no vacía
        if not descripcion or not descripcion.strip():
            return False, "La descripción de la automatización es obligatoria"
        
        # Validar que el hogar existe
        home = self.home_dao.obtener_por_id(home_id)
        if not home:
            return False, "Hogar no encontrado"
        
        # Crear automatización
        automatizacion = Automation(
            id=0,  # Se auto-genera en BD
            name=nombre.strip(),
            description=descripcion.strip(),
            active=activar,
            home=home
        )
        
        if self.automation_dao.insertar(automatizacion):
            estado = "activa" if activar else "inactiva"
            logger.info(
                f"Automatización creada: {nombre} | home={home.name} | "
                f"active={activar} | description={descripcion[:50]}"
            )
            return True, f"Automatización creada exitosamente ({estado})"
        else:
            logger.error(f"Fallo al crear automatización: {nombre}")
            return False, "Error al crear automatización"
    
    def listar_automatizaciones(self) -> List[Automation]:
        """
        Obtiene todas las automatizaciones del sistema.
        
        Returns:
            Lista de automatizaciones
        """
        return self.automation_dao.obtener_todos()
    
    def obtener_automatizacion(self, automation_id: int) -> Optional[Automation]:
        """
        Obtiene una automatización por ID.
        
        Args:
            automation_id: ID de la automatización
            
        Returns:
            Automatización encontrada o None
        """
        return self.automation_dao.obtener_por_id(automation_id)
    
    def obtener_automatizaciones_hogar(self, home_id: int) -> List[Automation]:
        """
        Obtiene todas las automatizaciones de un hogar.
        
        Args:
            home_id: ID del hogar
            
        Returns:
            Lista de automatizaciones del hogar
        """
        return self.automation_dao.obtener_por_hogar(home_id)
    
    def obtener_automatizaciones_activas(self, home_id: int) -> List[Automation]:
        """
        Obtiene solo las automatizaciones activas de un hogar.
        
        Args:
            home_id: ID del hogar
            
        Returns:
            Lista de automatizaciones activas
        """
        return self.automation_dao.obtener_activas(home_id)
    
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
        hogares = self.home_dao.obtener_hogares_usuario(email_usuario)
        resultado = {}
        
        for hogar in hogares:
            automatizaciones = self.automation_dao.obtener_por_hogar(hogar.id)
            resultado[hogar.name] = automatizaciones
        
        return resultado
    
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
        # Obtener automatización
        automatizacion = self.automation_dao.obtener_por_id(automation_id)
        
        if not automatizacion:
            return False, "Automatización no encontrada"
        
        # Validar que al menos se actualice algo
        if not nuevo_nombre and not nueva_descripcion:
            return False, "No hay cambios para aplicar"
        
        # Actualizar nombre si se proporciona
        if nuevo_nombre:
            if not nuevo_nombre.strip():
                return False, "El nombre no puede estar vacío"
            automatizacion.name = nuevo_nombre.strip()
        
        # Actualizar descripción si se proporciona
        if nueva_descripcion:
            if not nueva_descripcion.strip():
                return False, "La descripción no puede estar vacía"
            automatizacion.description = nueva_descripcion.strip()
        
        # Guardar cambios
        if self.automation_dao.modificar(automatizacion):
            logger.info(
                f"Automatización actualizada: ID={automation_id} | "
                f"new_name={nuevo_nombre or 'sin cambios'} | "
                f"new_description={nueva_descripcion[:30] if nueva_descripcion else 'sin cambios'}"
            )
            return True, "Automatización actualizada exitosamente"
        else:
            logger.error(f"Fallo al actualizar automatización: ID={automation_id}")
            return False, "Error al actualizar automatización"
    
    def eliminar_automatizacion(self, automation_id: int) -> tuple[bool, str]:
        """
        Elimina una automatización.
        
        Args:
            automation_id: ID de la automatización a eliminar
            
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        # Verificar que la automatización existe
        automatizacion = self.automation_dao.obtener_por_id(automation_id)
        
        if not automatizacion:
            return False, "Automatización no encontrada"
        
        # Eliminar automatización
        if self.automation_dao.eliminar(automation_id):
            logger.info(
                f"Automatización eliminada: ID={automation_id} | "
                f"name={automatizacion.name} | home={automatizacion.home.name}"
            )
            return True, f"Automatización '{automatizacion.name}' eliminada exitosamente"
        else:
            logger.error(f"Fallo al eliminar automatización: ID={automation_id}")
            return False, "Error al eliminar automatización"
    
    def activar_automatizacion(self, automation_id: int) -> tuple[bool, str]:
        """
        Activa una automatización.
        
        Args:
            automation_id: ID de la automatización
            
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        # Verificar que la automatización existe
        automatizacion = self.automation_dao.obtener_por_id(automation_id)
        
        if not automatizacion:
            return False, "Automatización no encontrada"
        
        # Verificar si ya está activa
        if automatizacion.active:
            return False, f"La automatización '{automatizacion.name}' ya está activa"
        
        # Activar
        if self.automation_dao.cambiar_estado(automation_id, True):
            logger.info(
                f"Automatización activada: ID={automation_id} | "
                f"name={automatizacion.name}"
            )
            return True, f"Automatización '{automatizacion.name}' activada exitosamente"
        else:
            logger.error(f"Fallo al activar automatización: ID={automation_id}")
            return False, "Error al activar automatización"
    
    def desactivar_automatizacion(self, automation_id: int) -> tuple[bool, str]:
        """
        Desactiva una automatización.
        
        Args:
            automation_id: ID de la automatización
            
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        # Verificar que la automatización existe
        automatizacion = self.automation_dao.obtener_por_id(automation_id)
        
        if not automatizacion:
            return False, "Automatización no encontrada"
        
        # Verificar si ya está inactiva
        if not automatizacion.active:
            return False, f"La automatización '{automatizacion.name}' ya está inactiva"
        
        # Desactivar
        if self.automation_dao.cambiar_estado(automation_id, False):
            logger.info(
                f"Automatización desactivada: ID={automation_id} | "
                f"name={automatizacion.name}"
            )
            return True, f"Automatización '{automatizacion.name}' desactivada exitosamente"
        else:
            logger.error(f"Fallo al desactivar automatización: ID={automation_id}")
            return False, "Error al desactivar automatización"
    
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
        todas = self.automation_dao.obtener_por_hogar(home_id)
        activas = self.automation_dao.obtener_activas(home_id)
        
        return {
            'total': len(todas),
            'activas': len(activas),
            'inactivas': len(todas) - len(activas)
        }
