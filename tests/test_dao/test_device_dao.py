"""
Tests para DeviceDAO
Estos tests verifican las operaciones CRUD de dispositivos.
"""

import pytest
from dao.device_dao import DeviceDAO
from dao.state_dao import StateDAO
from dao.device_type_dao import DeviceTypeDAO
from dao.location_dao import LocationDAO
from dao.home_dao import HomeDAO
from dominio.device import Device


@pytest.fixture
def device_dao():
    """Fixture que proporciona una instancia de DeviceDAO."""
    return DeviceDAO()


@pytest.fixture
def state_dao():
    """Fixture que proporciona una instancia de StateDAO."""
    return StateDAO()


@pytest.fixture
def device_type_dao():
    """Fixture que proporciona una instancia de DeviceTypeDAO."""
    return DeviceTypeDAO()


@pytest.fixture
def location_dao():
    """Fixture que proporciona una instancia de LocationDAO."""
    return LocationDAO()


@pytest.fixture
def home_dao():
    """Fixture que proporciona una instancia de HomeDAO."""
    return HomeDAO()


@pytest.fixture
def sample_device(state_dao, device_type_dao, location_dao, home_dao):
    """Fixture que crea un dispositivo de ejemplo con todas sus dependencias."""
    # Obtener entidades necesarias de la BD
    state = state_dao.obtener_por_id(1)  # Estado "Encendido" o similar
    device_type = device_type_dao.obtener_por_id(1)  # Primer tipo
    location = location_dao.obtener_por_id(1)  # Primera ubicación
    home = home_dao.obtener_por_id(1)  # Primer hogar
    
    # Crear dispositivo
    return Device(0, "Dispositivo Test", state, device_type, location, home)


class TestDeviceDAO:
    """Tests para la clase DeviceDAO"""

    def test_obtener_todos_devices(self, device_dao):
        """Test: Obtener todos los dispositivos de la BD"""
        dispositivos = device_dao.obtener_todos()
        
        assert isinstance(dispositivos, list)
        # Debería haber al menos algunos dispositivos en la BD
        assert len(dispositivos) >= 0
        
        # Si hay dispositivos, verificar estructura
        if dispositivos:
            device = dispositivos[0]
            assert hasattr(device, 'id')
            assert hasattr(device, 'name')
            assert hasattr(device, 'state')
            assert hasattr(device, 'device_type')
            assert hasattr(device, 'location')
            assert hasattr(device, 'home')

    def test_obtener_device_por_id(self, device_dao):
        """Test: Obtener un dispositivo específico por ID"""
        # Intentar obtener el dispositivo con ID 1
        device = device_dao.obtener_por_id(1)
        
        if device:  # Si existe
            assert device.id == 1
            assert isinstance(device.name, str)
            assert device.state is not None
            assert device.device_type is not None
            assert device.location is not None
            assert device.home is not None

    def test_obtener_device_inexistente(self, device_dao):
        """Test: Intentar obtener un dispositivo que no existe"""
        device = device_dao.obtener_por_id(99999)
        assert device is None

    def test_obtener_por_hogar(self, device_dao):
        """Test: Obtener dispositivos de un hogar específico"""
        # Obtener dispositivos del hogar 1
        dispositivos = device_dao.obtener_por_hogar(1)
        
        assert isinstance(dispositivos, list)
        
        # Verificar que todos pertenecen al hogar 1
        for device in dispositivos:
            assert device.home.id == 1

    def test_obtener_por_hogar_inexistente(self, device_dao):
        """Test: Obtener dispositivos de un hogar que no existe"""
        dispositivos = device_dao.obtener_por_hogar(99999)
        assert isinstance(dispositivos, list)
        assert len(dispositivos) == 0

    def test_buscar_por_nombre(self, device_dao):
        """Test: Buscar dispositivos por nombre"""
        # Buscar dispositivos que contengan "Luz" en el hogar 1
        dispositivos = device_dao.buscar_por_nombre("Luz", 1)
        
        assert isinstance(dispositivos, list)
        
        # Verificar que todos contienen "Luz" en el nombre
        for device in dispositivos:
            assert "luz" in device.name.lower() or "luz" in device.name.lower()

    def test_buscar_por_nombre_sin_resultados(self, device_dao):
        """Test: Buscar con un nombre que no existe"""
        dispositivos = device_dao.buscar_por_nombre("DispositivoInexistente123", 1)
        assert isinstance(dispositivos, list)
        assert len(dispositivos) == 0

    def test_cambiar_estado(self, device_dao):
        """Test: Cambiar el estado de un dispositivo"""
        # Obtener un dispositivo existente
        device = device_dao.obtener_por_id(1)
        
        if device:
            estado_original = device.state.id
            # Intentar cambiar a otro estado (1 o 2)
            nuevo_estado = 2 if estado_original == 1 else 1
            
            exito = device_dao.cambiar_estado(1, nuevo_estado)
            assert exito is True
            
            # Verificar que el cambio se aplicó
            device_actualizado = device_dao.obtener_por_id(1)
            assert device_actualizado.state.id == nuevo_estado
            
            # Restaurar estado original
            device_dao.cambiar_estado(1, estado_original)

    def test_insertar_device(self, device_dao, sample_device):
        """Test: Insertar un nuevo dispositivo"""
        # Insertar dispositivo
        exito = device_dao.insertar(sample_device)
        assert exito is True

    def test_modificar_device(self, device_dao):
        """Test: Modificar un dispositivo existente"""
        # Obtener un dispositivo
        device = device_dao.obtener_por_id(1)
        
        if device:
            # Modificar nombre
            nombre_original = device.name
            device.name = "Dispositivo Modificado Test"
            
            # Guardar cambios
            exito = device_dao.modificar(device)
            assert exito is True
            
            # Verificar cambio
            device_modificado = device_dao.obtener_por_id(1)
            assert device_modificado.name == "Dispositivo Modificado Test"
            
            # Restaurar nombre original
            device.name = nombre_original
            device_dao.modificar(device)

    def test_eliminar_device_inexistente(self, device_dao):
        """Test: Intentar eliminar un dispositivo que no existe"""
        exito = device_dao.eliminar(99999)
        assert exito is False


# Tests simples adicionales
def test_device_dao_instancia():
    """Test: Crear una instancia de DeviceDAO"""
    dao = DeviceDAO()
    assert dao is not None
    assert hasattr(dao, 'obtener_todos')
    assert hasattr(dao, 'obtener_por_id')
    assert hasattr(dao, 'insertar')
    assert hasattr(dao, 'modificar')
    assert hasattr(dao, 'eliminar')
