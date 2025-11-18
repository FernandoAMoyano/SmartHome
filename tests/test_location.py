"""
Tests para la clase Location
Estos tests verifican las ubicaciones dentro de los hogares.
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "models"))

from dominio.location import Location
from dominio.home import Home


class TestLocation:
    """Tests para la clase Location"""

    def test_crear_location_sala(self):
        """Test: Crear ubicación 'Sala de Estar'"""
        home = Home(1, "Casa Principal")
        location = Location(1, "Sala de Estar", home)
        assert location.id == 1
        assert location.name == "Sala de Estar"
        assert location.home.id == 1

    def test_crear_location_cocina(self):
        """Test: Crear ubicación 'Cocina'"""
        home = Home(1, "Casa Principal")
        location = Location(2, "Cocina", home)
        assert location.id == 2
        assert location.name == "Cocina"

    def test_crear_location_dormitorio(self):
        """Test: Crear ubicación 'Dormitorio Principal'"""
        home = Home(1, "Casa Principal")
        location = Location(3, "Dormitorio Principal", home)
        assert location.id == 3
        assert location.name == "Dormitorio Principal"

    def test_modificar_nombre_location(self):
        """Test: Cambiar el nombre de una ubicación"""
        # Arrange
        home = Home(1, "Casa Principal")
        location = Location(1, "Sala", home)
        nuevo_nombre = "Sala de Estar"

        # Act
        location.name = nuevo_nombre

        # Assert
        assert location.name == "Sala de Estar"
        assert location.id == 1  # El ID permanece igual

    def test_location_con_espacios(self):
        """Test: Verificar que maneja nombres con espacios"""
        home = Home(1, "Casa Principal")
        location = Location(5, "Baño Principal", home)
        assert location.name == "Baño Principal"

    def test_types_location(self):
        """Test: Verificar tipos de datos"""
        home = Home(1, "Casa Principal")
        location = Location(8, "Oficina", home)
        assert isinstance(location.id, int)
        assert isinstance(location.name, str)
        assert isinstance(location.home.id, int)


# Tests simples
def test_location_simple():
    """Test básico: Crear una ubicación"""
    home = Home(1, "Casa Principal")
    location = Location(1, "Jardín", home)
    assert location.name == "Jardín"


def test_cambiar_nombre_location():
    """Test: Modificar nombre de ubicación"""
    home = Home(1, "Casa Principal")
    location = Location(2, "Garaje", home)
    location.name = "Cochera"
    assert location.name == "Cochera"


def test_multiples_locations():
    """Test: Crear múltiples ubicaciones"""
    home = Home(1, "Casa Principal")
    sala = Location(1, "Sala", home)
    cocina = Location(2, "Cocina", home)

    assert sala.name == "Sala"
    assert cocina.name == "Cocina"
    assert sala.id != cocina.id