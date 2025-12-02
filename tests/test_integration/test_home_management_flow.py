"""
Tests de integración para gestión de hogares y ubicaciones.

Estos tests validan la integración entre:
- HomeDAO
- LocationDAO
- Base de datos real

NO usan mocks - todo es real.
"""

import pytest
from dao.home_dao import HomeDAO
from dao.location_dao import LocationDAO
from conn.db_connection import DatabaseConnection


@pytest.mark.integration
@pytest.mark.slow
class TestHomeManagementIntegration:
    """Tests de integración para gestión de hogares."""
    
    def setup_method(self):
        """Setup: Preparar DAOs y limpiar datos de test."""
        self.home_dao = HomeDAO()
        self.location_dao = LocationDAO()
        self.db = DatabaseConnection()
        self._cleanup_test_data()
    
    def test_obtener_todos_los_hogares(self):
        """
        Test: Obtener lista completa de hogares desde BD.
        
        Valida:
        - HomeDAO.obtener_todos()
        - Construcción de objetos Home
        """
        hogares = self.home_dao.obtener_todos()
        
        assert isinstance(hogares, list)
        
        # Si hay hogares, verificar estructura
        if len(hogares) > 0:
            hogar = hogares[0]
            assert hasattr(hogar, 'id')
            assert hasattr(hogar, 'name')
            assert isinstance(hogar.id, int)
            assert isinstance(hogar.name, str)
    
    def test_obtener_hogar_por_id(self):
        """
        Test: Obtener hogar específico por ID.
        
        Valida:
        - HomeDAO.obtener_por_id()
        """
        # Obtener primer hogar disponible
        hogares = self.home_dao.obtener_todos()
        
        if len(hogares) > 0:
            hogar_id = hogares[0].id
            
            # Obtener por ID
            hogar = self.home_dao.obtener_por_id(hogar_id)
            
            assert hogar is not None
            assert hogar.id == hogar_id
            assert len(hogar.name) > 0
    
    def test_obtener_hogares_de_usuario(self):
        """
        Test: Obtener hogares asociados a un usuario.
        
        Valida:
        - HomeDAO.obtener_hogares_usuario()
        - JOIN con tabla user_home
        """
        # Usar email de usuario que existe en BD
        hogares = self.home_dao.obtener_hogares_usuario("admin@smarthome.com")
        
        assert isinstance(hogares, list)
        
        # Verificar estructura de hogares retornados
        for hogar in hogares:
            assert hasattr(hogar, 'id')
            assert hasattr(hogar, 'name')
    
    def test_obtener_todas_las_ubicaciones(self):
        """
        Test: Obtener lista completa de ubicaciones desde BD.
        
        Valida:
        - LocationDAO.obtener_todos()
        - Construcción de objetos Location
        """
        ubicaciones = self.location_dao.obtener_todos()
        
        assert isinstance(ubicaciones, list)
        
        # Si hay ubicaciones, verificar estructura
        if len(ubicaciones) > 0:
            ubicacion = ubicaciones[0]
            assert hasattr(ubicacion, 'id')
            assert hasattr(ubicacion, 'name')
            assert hasattr(ubicacion, 'home')
            assert isinstance(ubicacion.id, int)
            assert isinstance(ubicacion.name, str)
    
    def test_obtener_ubicacion_por_id(self):
        """
        Test: Obtener ubicación específica por ID.
        
        Valida:
        - LocationDAO.obtener_por_id()
        - Relación con Home
        """
        # Obtener primera ubicación disponible
        ubicaciones = self.location_dao.obtener_todos()
        
        if len(ubicaciones) > 0:
            ubicacion_id = ubicaciones[0].id
            
            # Obtener por ID
            ubicacion = self.location_dao.obtener_por_id(ubicacion_id)
            
            assert ubicacion is not None
            assert ubicacion.id == ubicacion_id
            assert len(ubicacion.name) > 0
            assert ubicacion.home is not None
    
    def _cleanup_test_data(self):
        """Limpiar datos de test de la BD."""
        cursor = self.db.get_cursor()
        # Limpiar hogares de test (si se agregan en el futuro)
        cursor.execute("""
            DELETE FROM home 
            WHERE name LIKE '%Test Integration%'
        """)
        # Limpiar ubicaciones de test
        cursor.execute("""
            DELETE FROM location 
            WHERE name LIKE '%Test Integration%'
        """)
        self.db.commit()
        cursor.close()
    
    def teardown_method(self):
        """Cleanup: Limpiar después de cada test."""
        self._cleanup_test_data()


@pytest.mark.integration
@pytest.mark.slow
class TestDeviceTypeIntegration:
    """Tests de integración para tipos de dispositivos."""
    
    def setup_method(self):
        """Setup: Preparar DAO."""
        from dao.device_type_dao import DeviceTypeDAO
        self.device_type_dao = DeviceTypeDAO()
    
    def test_obtener_todos_los_tipos(self):
        """
        Test: Obtener lista completa de tipos de dispositivos.
        
        Valida:
        - DeviceTypeDAO.obtener_todos()
        """
        tipos = self.device_type_dao.obtener_todos()
        
        assert isinstance(tipos, list)
        
        # Si hay tipos, verificar estructura
        if len(tipos) > 0:
            tipo = tipos[0]
            assert hasattr(tipo, 'id')
            assert hasattr(tipo, 'name')
            assert hasattr(tipo, 'characteristics')
    
    def test_obtener_tipo_por_id(self):
        """
        Test: Obtener tipo de dispositivo específico por ID.
        
        Valida:
        - DeviceTypeDAO.obtener_por_id()
        """
        # Obtener primer tipo disponible
        tipos = self.device_type_dao.obtener_todos()
        
        if len(tipos) > 0:
            tipo_id = tipos[0].id
            
            # Obtener por ID
            tipo = self.device_type_dao.obtener_por_id(tipo_id)
            
            assert tipo is not None
            assert tipo.id == tipo_id
            assert len(tipo.name) > 0
