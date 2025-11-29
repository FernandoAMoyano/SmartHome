"""
Tests para la clase Device
Estos tests verifican el funcionamiento de los dispositivos inteligentes.
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "models"))

from dominio.device import Device
from dominio.state import State
from dominio.device_type import DeviceType
from dominio.location import Location
from dominio.home import Home


class TestDevice:
    """Tests para la clase Device"""

    def test_crear_device_luz_sala(self):
        """Test: Crear dispositivo 'Luz Principal Sala'"""
        # Crear objetos necesarios
        home = Home(1, "Casa Principal")
        location = Location(1, "Sala", home)
        state = State(1, "Encendido")
        device_type = DeviceType(1, "Luz Inteligente", "LED controlable")
        
        device = Device(1, "Luz Principal Sala", state, device_type, location, home)

        assert device.id == 1
        assert device.name == "Luz Principal Sala"
        assert device.state.id == 1
        assert device.device_type.id == 1
        assert device.location.id == 1
        assert device.home.id == 1

    def test_crear_device_termostato(self):
        """Test: Crear dispositivo 'Termostato Central'"""
        home = Home(1, "Casa Principal")
        location = Location(1, "Sala", home)
        state = State(2, "Apagado")
        device_type = DeviceType(2, "Termostato", "Control temperatura")
        
        device = Device(2, "Termostato Central", state, device_type, location, home)

        assert device.id == 2
        assert device.name == "Termostato Central"
        assert device.state.id == 2  # Apagado
        assert device.device_type.id == 2  # Termostato

    def test_cambiar_nombre_device(self):
        """Test: Modificar el nombre del dispositivo"""
        # Arrange
        home = Home(1, "Casa Principal")
        location = Location(2, "Cocina", home)
        state = State(1, "Encendido")
        device_type = DeviceType(1, "Luz", "LED")
        device = Device(3, "Luz Cocina", state, device_type, location, home)
        nuevo_nombre = "Luz Principal Cocina"

        # Act
        device.name = nuevo_nombre

        # Assert
        assert device.name == "Luz Principal Cocina"
        assert device.id == 3  # ID no cambia

    def test_cambiar_estado_device(self):
        """Test: Cambiar el estado del dispositivo"""
        # Arrange
        home = Home(1, "Casa")
        location = Location(1, "Sala", home)
        state_apagado = State(2, "Apagado")
        state_encendido = State(1, "Encendido")
        device_type = DeviceType(3, "Ventilador", "Aire")
        device = Device(4, "Ventilador", state_apagado, device_type, location, home)

        # Act
        device.state = state_encendido

        # Assert
        assert device.state.id == 1
        assert device.name == "Ventilador"  # Nombre no cambia

    def test_buscar_device_por_nombre_encontrado(self):
        """Test: Buscar dispositivo por nombre - caso exitoso"""
        # Arrange
        home = Home(1, "Casa")
        location = Location(1, "Entrada", home)
        state = State(1, "Activo")
        device_type = DeviceType(5, "Cámara", "Vigilancia")
        device = Device(5, "Cámara Entrada Principal", state, device_type, location, home)

        # Act & Assert
        assert device.search_device_by_name("Cámara")
        assert device.search_device_by_name("Entrada")
        assert device.search_device_by_name("Principal")

    def test_buscar_device_por_nombre_no_encontrado(self):
        """Test: Buscar dispositivo por nombre - caso no encontrado"""
        # Arrange
        home = Home(1, "Casa")
        location = Location(3, "Dormitorio", home)
        state = State(2, "Apagado")
        device_type = DeviceType(1, "Luz", "LED")
        device = Device(6, "Luz Dormitorio", state, device_type, location, home)

        # Act & Assert
        assert not device.search_device_by_name("Cocina")
        assert not device.search_device_by_name("Garaje")

    def test_buscar_device_case_insensitive(self):
        """Test: Búsqueda insensible a mayúsculas/minúsculas"""
        # Arrange
        home = Home(1, "Casa")
        location = Location(3, "Pasillo", home)
        state = State(1, "Activo")
        device_type = DeviceType(6, "Sensor", "Movimiento")
        device = Device(7, "Sensor Movimiento", state, device_type, location, home)

        # Act & Assert
        assert device.search_device_by_name("sensor")
        assert device.search_device_by_name("MOVIMIENTO")
        assert device.search_device_by_name("SeNsOr")

    def test_buscar_device_string_vacio(self):
        """Test: Búsqueda con string vacío"""
        home = Home(1, "Casa")
        location = Location(1, "Entrada", home)
        state = State(1, "Activo")
        device_type = DeviceType(4, "Cerradura", "Biométrica")
        device = Device(8, "Cerradura Principal", state, device_type, location, home)

        assert not device.search_device_by_name("")
        assert not device.search_device_by_name("   ")  # Solo espacios

    def test_types_device(self):
        """Test: Verificar tipos de datos correctos"""
        home = Home(1, "Casa")
        location = Location(1, "Test", home)
        state = State(1, "On")
        device_type = DeviceType(1, "Test", "Test")
        device = Device(9, "Test Device", state, device_type, location, home)

        assert isinstance(device.id, int)
        assert isinstance(device.name, str)
        assert isinstance(device.state.id, int)
        assert isinstance(device.device_type.id, int)
        assert isinstance(device.location.id, int)
        assert isinstance(device.home.id, int)


# Tests simples
def test_device_basico():
    """Test básico: Crear un dispositivo"""
    home = Home(1, "Casa")
    location = Location(1, "Test", home)
    state = State(1, "On")
    device_type = DeviceType(1, "Test", "Test")
    device = Device(1, "Test Device", state, device_type, location, home)
    assert device.name == "Test Device"


def test_encender_dispositivo():
    """Test: Simular encender un dispositivo (cambiar a estado 1)"""
    home = Home(1, "Casa")
    location = Location(1, "Test", home)
    state_apagado = State(2, "Apagado")
    state_encendido = State(1, "Encendido")
    device_type = DeviceType(1, "Luz", "LED")
    device = Device(2, "Luz Test", state_apagado, device_type, location, home)
    device.state = state_encendido
    assert device.state.id == 1


def test_buscar_nombre_parcial():
    """Test: Buscar por nombre parcial"""
    home = Home(1, "Casa")
    location = Location(1, "Sala", home)
    state = State(1, "On")
    device_type = DeviceType(1, "Luz", "LED")
    device = Device(3, "Luz Inteligente Sala", state, device_type, location, home)
    assert device.search_device_by_name("Inteligente")


def test_cambiar_ubicacion():
    """Test: Simular mover dispositivo a otra ubicación"""
    home = Home(1, "Casa")
    location_original = Location(1, "Sala", home)
    state = State(1, "On")
    device_type = DeviceType(3, "Ventilador", "Portátil")
    device = Device(4, "Ventilador Portátil", state, device_type, location_original, home)
    # Nota: En un sistema real, mover ubicación requeriría otro método
    assert device.location.id == 1  # Verificar que mantiene la ubicación original