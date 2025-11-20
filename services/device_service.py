"""Servicio de gestión de dispositivos."""

from typing import List, Optional, Dict
from dao.device_dao import DeviceDAO
from dao.home_dao import HomeDAO
from dao.state_dao import StateDAO
from dao.device_type_dao import DeviceTypeDAO
from dao.location_dao import LocationDAO
from dominio.device import Device


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
        self,
        nombre: str,
        home_id: int,
        type_id: int,
        location_id: int,
        state_id: int
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
        # Validar nombre no vacío
        if not nombre or not nombre.strip():
            return False, "El nombre del dispositivo es obligatorio"
        
        # Obtener entidades relacionadas
        home = self.home_dao.obtener_por_id(home_id)
        device_type = self.device_type_dao.obtener_por_id(type_id)
        location = self.location_dao.obtener_por_id(location_id)
        state = self.state_dao.obtener_por_id(state_id)
        
        # Validar que todas las entidades existan
        if not home:
            return False, "Hogar no encontrado"
        if not device_type:
            return False, "Tipo de dispositivo no encontrado"
        if not location:
            return False, "Ubicación no encontrada"
        if not state:
            return False, "Estado no encontrado"
        
        # Crear dispositivo
        dispositivo = Device(0, nombre, state, device_type, location, home)
        
        if self.device_dao.insertar(dispositivo):
            return True, "Dispositivo creado exitosamente"
        else:
            return False, "Error al crear dispositivo"
    
    def listar_dispositivos(self) -> List[Device]:
        """
        Obtiene todos los dispositivos.
        
        Returns:
            Lista de dispositivos
        """
        return self.device_dao.obtener_todos()
    
    def obtener_dispositivo(self, device_id: int) -> Optional[Device]:
        """
        Obtiene un dispositivo por ID.
        
        Args:
            device_id: ID del dispositivo
            
        Returns:
            Dispositivo encontrado o None
        """
        return self.device_dao.obtener_por_id(device_id)
    
    def actualizar_dispositivo(
        self,
        device_id: int,
        nuevo_nombre: Optional[str] = None,
        nuevo_estado_id: Optional[int] = None
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
        # Obtener dispositivo
        dispositivo = self.device_dao.obtener_por_id(device_id)
        
        if not dispositivo:
            return False, "Dispositivo no encontrado"
        
        # Validar que al menos se actualice algo
        if not nuevo_nombre and not nuevo_estado_id:
            return False, "No hay cambios para aplicar"
        
        # Actualizar nombre si se proporciona
        if nuevo_nombre:
            if not nuevo_nombre.strip():
                return False, "El nombre no puede estar vacío"
            dispositivo.name = nuevo_nombre.strip()
        
        # Actualizar estado si se proporciona
        if nuevo_estado_id:
            nuevo_estado = self.state_dao.obtener_por_id(nuevo_estado_id)
            if not nuevo_estado:
                return False, "Estado inválido"
            dispositivo.state = nuevo_estado
        
        # Guardar cambios
        if self.device_dao.modificar(dispositivo):
            return True, "Dispositivo actualizado exitosamente"
        else:
            return False, "Error al actualizar dispositivo"
    
    def eliminar_dispositivo(self, device_id: int) -> tuple[bool, str]:
        """
        Elimina un dispositivo.
        
        Args:
            device_id: ID del dispositivo a eliminar
            
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        # Verificar que el dispositivo existe
        dispositivo = self.device_dao.obtener_por_id(device_id)
        
        if not dispositivo:
            return False, "Dispositivo no encontrado"
        
        # Eliminar dispositivo
        if self.device_dao.eliminar(device_id):
            return True, f"Dispositivo '{dispositivo.name}' eliminado exitosamente"
        else:
            return False, "Error al eliminar dispositivo"
    
    def obtener_dispositivos_por_hogar(self, home_id: int) -> List[Device]:
        """
        Obtiene dispositivos de un hogar específico.
        
        Args:
            home_id: ID del hogar
            
        Returns:
            Lista de dispositivos del hogar
        """
        return self.device_dao.obtener_por_hogar(home_id)
    
    def buscar_dispositivos_por_nombre(self, nombre: str, home_id: int) -> List[Device]:
        """
        Busca dispositivos por nombre en un hogar.
        
        Args:
            nombre: Texto a buscar
            home_id: ID del hogar
            
        Returns:
            Lista de dispositivos que coinciden
        """
        return self.device_dao.buscar_por_nombre(nombre, home_id)
    
    def cambiar_estado_dispositivo(self, device_id: int, nuevo_estado_id: int) -> tuple[bool, str]:
        """
        Cambia el estado de un dispositivo.
        
        Args:
            device_id: ID del dispositivo
            nuevo_estado_id: ID del nuevo estado
            
        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        # Verificar que el dispositivo existe
        dispositivo = self.device_dao.obtener_por_id(device_id)
        if not dispositivo:
            return False, "Dispositivo no encontrado"
        
        # Verificar que el estado existe
        estado = self.state_dao.obtener_por_id(nuevo_estado_id)
        if not estado:
            return False, "Estado no encontrado"
        
        # Cambiar estado
        if self.device_dao.cambiar_estado(device_id, nuevo_estado_id):
            return True, f"Estado cambiado a '{estado.name}'"
        else:
            return False, "Error al cambiar estado"
    
    def obtener_opciones_configuracion(self) -> Dict[str, List]:
        """
        Obtiene todas las opciones para configurar dispositivos.
        
        Returns:
            Diccionario con hogares, tipos, ubicaciones y estados
        """
        return {
            'hogares': self.home_dao.obtener_todos(),
            'tipos': self.device_type_dao.obtener_todos(),
            'ubicaciones': self.location_dao.obtener_todos(),
            'estados': self.state_dao.obtener_todos()
        }
    
    def obtener_dispositivos_usuario(self, email_usuario: str) -> Dict[str, List[Device]]:
        """
        Obtiene todos los dispositivos organizados por hogar para un usuario.
        
        Args:
            email_usuario: Email del usuario
            
        Returns:
            Diccionario con hogares como claves y listas de dispositivos como valores
        """
        hogares = self.home_dao.obtener_hogares_usuario(email_usuario)
        resultado = {}
        
        for hogar in hogares:
            dispositivos = self.device_dao.obtener_por_hogar(hogar.id)
            resultado[hogar.name] = dispositivos
        
        return resultado
