"""
Tests de integración para flujo completo de dispositivos.

Estos tests validan la integración entre:
- DeviceService
- DeviceDAO
- HomeDAO
- LocationDAO
- DeviceTypeDAO
- StateDAO
- Base de datos real

NO usan mocks - todo es real.
"""

import pytest
from services.device_service import DeviceService
from services.auth_service import AuthService
from conn.db_connection import DatabaseConnection


@pytest.mark.integration
@pytest.mark.slow
class TestDeviceFlowIntegration:
    """Tests de integración para flujo completo de dispositivos."""
    
    def setup_method(self):
        """Setup: Preparar servicios y limpiar datos de test."""
        self.device_service = DeviceService()
        self.auth_service = AuthService()
        self.db = DatabaseConnection()
        self._cleanup_test_devices()
    
    def test_crear_dispositivo_flujo_completo(self):
        """
        Test E2E: Crear dispositivo con todas las dependencias reales.
        
        Valida:
        - DeviceService.crear_dispositivo()
        - DeviceDAO.insertar()
        - HomeDAO.obtener_por_id()
        - DeviceTypeDAO.obtener_por_id()
        - LocationDAO.obtener_por_id()
        - StateDAO.obtener_por_id()
        """
        # Crear dispositivo
        exito, mensaje = self.device_service.crear_dispositivo(
            nombre="Test Integration Device",
            home_id=1,      # Debe existir en BD
            type_id=1,      # Debe existir en BD
            location_id=1,  # Debe existir en BD
            state_id=1      # Debe existir en BD
        )
        
        assert exito is True
        assert "exitosamente" in mensaje.lower()
        
        # Verificar que se creó consultando la BD
        dispositivos = self.device_service.listar_dispositivos()
        test_device = next(
            (d for d in dispositivos if d.name == "Test Integration Device"),
            None
        )
        
        assert test_device is not None
        assert test_device.home.id == 1
        assert test_device.device_type.id == 1
        assert test_device.location.id == 1
        assert test_device.state.id == 1
    
    def test_listar_dispositivos_con_relaciones(self):
        """
        Test: Listar dispositivos carga todas las relaciones correctamente.
        
        Valida:
        - DeviceDAO.obtener_todos()
        - Carga de relaciones (home, type, location, state)
        - Construcción correcta de objetos Device
        """
        dispositivos = self.device_service.listar_dispositivos()
        
        # Debe retornar lista
        assert isinstance(dispositivos, list)
        
        # Si hay dispositivos, verificar relaciones
        if len(dispositivos) > 0:
            device = dispositivos[0]
            
            # Verificar que todas las relaciones están cargadas
            assert device.home is not None
            assert device.device_type is not None
            assert device.location is not None
            assert device.state is not None
            
            # Verificar que las relaciones tienen datos
            assert hasattr(device.home, 'name')
            assert hasattr(device.device_type, 'name')
            assert hasattr(device.location, 'name')
            assert hasattr(device.state, 'name')
    
    def test_actualizar_dispositivo_nombre_y_estado(self):
        """
        Test: Actualizar nombre y estado de dispositivo.
        
        Valida:
        - DeviceDAO.obtener_por_id()
        - DeviceDAO.modificar()
        - StateDAO.obtener_por_id()
        """
        # Crear dispositivo de prueba
        exito, _ = self.device_service.crear_dispositivo(
            nombre="Device To Update",
            home_id=1,
            type_id=1,
            location_id=1,
            state_id=1  # Estado inicial: Encendido
        )
        assert exito is True
        
        # Obtener el dispositivo creado
        dispositivos = self.device_service.listar_dispositivos()
        device = next(
            (d for d in dispositivos if d.name == "Device To Update"),
            None
        )
        assert device is not None
        device_id = device.id
        
        # Actualizar nombre y estado
        exito, mensaje = self.device_service.actualizar_dispositivo(
            device_id=device_id,
            nuevo_nombre="Device Updated",
            nuevo_estado_id=2  # Cambiar a Apagado
        )
        
        assert exito is True
        assert "exitosamente" in mensaje.lower()
        
        # Verificar cambios en BD
        device_actualizado = self.device_service.obtener_dispositivo(device_id)
        assert device_actualizado is not None
        assert device_actualizado.name == "Device Updated"
        assert device_actualizado.state.id == 2
    
    def test_eliminar_dispositivo(self):
        """
        Test: Eliminar dispositivo de la BD.
        
        Valida:
        - DeviceDAO.obtener_por_id()
        - DeviceDAO.eliminar()
        """
        # Crear dispositivo de prueba
        exito, _ = self.device_service.crear_dispositivo(
            nombre="Device To Delete",
            home_id=1,
            type_id=1,
            location_id=1,
            state_id=1
        )
        assert exito is True
        
        # Obtener ID del dispositivo
        dispositivos = self.device_service.listar_dispositivos()
        device = next(
            (d for d in dispositivos if d.name == "Device To Delete"),
            None
        )
        assert device is not None
        device_id = device.id
        
        # Eliminar dispositivo
        exito, mensaje = self.device_service.eliminar_dispositivo(device_id)
        
        assert exito is True
        assert "eliminado" in mensaje.lower()
        
        # Verificar que ya no existe
        device_eliminado = self.device_service.obtener_dispositivo(device_id)
        assert device_eliminado is None
    
    def test_obtener_dispositivos_por_hogar(self):
        """
        Test: Obtener dispositivos filtrados por hogar.
        
        Valida:
        - DeviceDAO.obtener_por_hogar()
        - Filtrado correcto por home_id
        """
        # Crear dispositivo en hogar específico
        exito, _ = self.device_service.crear_dispositivo(
            nombre="Device Home 1",
            home_id=1,
            type_id=1,
            location_id=1,
            state_id=1
        )
        assert exito is True
        
        # Obtener dispositivos del hogar 1
        dispositivos_home1 = self.device_service.obtener_dispositivos_por_hogar(1)
        
        # Verificar que retorna lista
        assert isinstance(dispositivos_home1, list)
        
        # Verificar que todos pertenecen al hogar 1
        for device in dispositivos_home1:
            assert device.home.id == 1
    
    def test_buscar_dispositivos_por_nombre(self):
        """
        Test: Buscar dispositivos por nombre parcial.
        
        Valida:
        - DeviceDAO.buscar_por_nombre()
        - Búsqueda con LIKE en BD
        """
        # Crear dispositivo con nombre único
        exito, _ = self.device_service.crear_dispositivo(
            nombre="Unique Search Device XYZ",
            home_id=1,
            type_id=1,
            location_id=1,
            state_id=1
        )
        assert exito is True
        
        # Buscar por nombre parcial
        resultados = self.device_service.buscar_dispositivos_por_nombre(
            nombre="Search Device",
            home_id=1
        )
        
        # Verificar que encuentra el dispositivo
        assert len(resultados) > 0
        assert any(d.name == "Unique Search Device XYZ" for d in resultados)
    
    def test_cambiar_estado_dispositivo(self):
        """
        Test: Cambiar estado de dispositivo directamente.
        
        Valida:
        - DeviceDAO.cambiar_estado()
        - StateDAO.obtener_por_id()
        """
        # Crear dispositivo
        exito, _ = self.device_service.crear_dispositivo(
            nombre="Device State Change",
            home_id=1,
            type_id=1,
            location_id=1,
            state_id=1  # Encendido
        )
        assert exito is True
        
        # Obtener dispositivo
        dispositivos = self.device_service.listar_dispositivos()
        device = next(
            (d for d in dispositivos if d.name == "Device State Change"),
            None
        )
        assert device is not None
        device_id = device.id
        
        # Cambiar estado
        exito, mensaje = self.device_service.cambiar_estado_dispositivo(
            device_id=device_id,
            nuevo_estado_id=2  # Apagado
        )
        
        assert exito is True
        
        # Verificar cambio
        device_actualizado = self.device_service.obtener_dispositivo(device_id)
        assert device_actualizado.state.id == 2
    
    def test_obtener_opciones_configuracion(self):
        """
        Test: Obtener todas las opciones de configuración.
        
        Valida:
        - HomeDAO.obtener_todos()
        - DeviceTypeDAO.obtener_todos()
        - LocationDAO.obtener_todos()
        - StateDAO.obtener_todos()
        """
        opciones = self.device_service.obtener_opciones_configuracion()
        
        # Verificar estructura
        assert 'hogares' in opciones
        assert 'tipos' in opciones
        assert 'ubicaciones' in opciones
        assert 'estados' in opciones
        
        # Verificar que retorna datos
        assert isinstance(opciones['hogares'], list)
        assert isinstance(opciones['tipos'], list)
        assert isinstance(opciones['ubicaciones'], list)
        assert isinstance(opciones['estados'], list)
        
        # Verificar que hay datos (asumiendo BD con datos iniciales)
        assert len(opciones['hogares']) > 0
        assert len(opciones['tipos']) > 0
        assert len(opciones['ubicaciones']) > 0
        assert len(opciones['estados']) > 0
    
    def _cleanup_test_devices(self):
        """Limpiar dispositivos de test de la BD."""
        cursor = self.db.get_cursor()
        cursor.execute("""
            DELETE FROM device 
            WHERE name LIKE '%Test Integration%' 
               OR name LIKE '%Device To%'
               OR name LIKE '%Unique Search%'
               OR name LIKE '%Device Home%'
               OR name LIKE '%Device State%'
        """)
        self.db.commit()
        cursor.close()
    
    def teardown_method(self):
        """Cleanup: Limpiar después de cada test."""
        self._cleanup_test_devices()
