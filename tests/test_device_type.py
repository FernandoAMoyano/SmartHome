"""
Tests para la clase DeviceType
Estos tests verifican los tipos de dispositivos inteligentes.
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "models"))

from dominio.device_type import DeviceType


class TestDeviceType:
    """Tests para la clase DeviceType"""

    def test_crear_device_type_luz(self):
        """Test: Crear tipo de dispositivo 'Luz Inteligente'"""
        device_type = DeviceType(1, "Luz Inteligente", "Iluminación LED controlable")

        assert device_type.id == 1
        assert device_type.name == "Luz Inteligente"
        assert device_type.characteristics == "Iluminación LED controlable"

    def test_crear_device_type_termostato(self):
        """Test: Crear tipo 'Termostato'"""
        device_type = DeviceType(2, "Termostato", "Control de temperatura")

        assert device_type.id == 2
        assert device_type.name == "Termostato"
        assert device_type.characteristics == "Control de temperatura"

    def test_crear_device_type_camara(self):
        """Test: Crear tipo 'Cámara de Seguridad'"""
        device_type = DeviceType(5, "Cámara de Seguridad", "Vigilancia remota")

        assert device_type.id == 5
        assert device_type.name == "Cámara de Seguridad"
        assert device_type.characteristics == "Vigilancia remota"

    def test_modificar_nombre_device_type(self):
        """Test: Cambiar el nombre del tipo de dispositivo"""
        # Arrange
        device_type = DeviceType(3, "Ventilador", "Circulación de aire")
        nuevo_nombre = "Ventilador Inteligente"

        # Act
        device_type.name = nuevo_nombre

        # Assert
        assert device_type.name == "Ventilador Inteligente"
        assert device_type.characteristics == "Circulación de aire"  # No cambia

    def test_modificar_characteristics(self):
        """Test: Cambiar las características del dispositivo"""
        # Arrange
        device_type = DeviceType(4, "Cerradura", "Control básico")
        nuevas_characteristics = "Control de acceso biométrico"

        # Act
        device_type.characteristics = nuevas_characteristics

        # Assert
        assert device_type.characteristics == "Control de acceso biométrico"
        assert device_type.name == "Cerradura"  # No cambia

    def test_types_device_type(self):
        """Test: Verificar tipos de datos correctos"""
        device_type = DeviceType(6, "Sensor", "Detección de movimiento")

        assert isinstance(device_type.id, int)
        assert isinstance(device_type.name, str)
        assert isinstance(device_type.characteristics, str)


# Tests simples
def test_device_type_basico():
    """Test básico: Crear un tipo de dispositivo"""
    device_type = DeviceType(1, "Test Device", "Características de prueba")
    assert device_type.name == "Test Device"


def test_cambiar_ambos_campos():
    """Test: Modificar tanto nombre como características"""
    device_type = DeviceType(2, "Original", "Características originales")

    device_type.name = "Modificado"
    device_type.characteristics = "Nuevas características"

    assert device_type.name == "Modificado"
    assert device_type.characteristics == "Nuevas características"


def test_characteristics_largas():
    """Test: Verificar que maneja características largas"""
    características_largas = (
        "Este es un dispositivo muy complejo con múltiples funcionalidades avanzadas"
    )
    device_type = DeviceType(3, "Dispositivo Complejo", características_largas)

    assert device_type.characteristics == características_largas
    