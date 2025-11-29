"""
Tests para la clase Home
Estos tests verifican el funcionamiento de los hogares en el sistema.
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "models"))

from dominio.home import Home


class TestHome:
    """Tests para la clase Home"""

    def test_crear_home_casa_principal(self):
        """Test: Crear 'Casa Principal'"""
        home = Home(1, "Casa Principal")

        assert home.id == 1
        assert home.name == "Casa Principal"

    def test_crear_home_casa_campo(self):
        """Test: Crear 'Casa de Campo'"""
        home = Home(2, "Casa de Campo")

        assert home.id == 2
        assert home.name == "Casa de Campo"

    def test_crear_home_departamento(self):
        """Test: Crear 'Departamento'"""
        home = Home(3, "Departamento")

        assert home.id == 3
        assert home.name == "Departamento"

    def test_modificar_nombre_home(self):
        """Test: Cambiar el nombre del hogar"""
        # Arrange
        home = Home(1, "Casa")
        nuevo_nombre = "Casa Renovada"

        # Act
        home.name = nuevo_nombre

        # Assert
        assert home.name == "Casa Renovada"
        assert home.id == 1  # El ID no cambia

    def test_home_con_nombre_largo(self):
        """Test: Verificar que maneja nombres largos"""
        nombre_largo = "Casa de Vacaciones en la Montaña"
        home = Home(4, nombre_largo)

        assert home.name == nombre_largo

    def test_types_home(self):
        """Test: Verificar tipos de datos correctos"""
        home = Home(5, "Oficina")

        assert isinstance(home.id, int)
        assert isinstance(home.name, str)


# Tests simples
def test_home_simple():
    """Test básico: Crear un hogar"""
    home = Home(1, "Mi Casa")
    assert home.name == "Mi Casa"


def test_cambiar_nombre_home():
    """Test: Modificar nombre del hogar"""
    home = Home(2, "Casa Vieja")
    home.name = "Casa Nueva"
    assert home.name == "Casa Nueva"


def test_multiples_homes():
    """Test: Crear múltiples hogares"""
    casa1 = Home(1, "Casa 1")
    casa2 = Home(2, "Casa 2")

    assert casa1.name == "Casa 1"
    assert casa2.name == "Casa 2"
    assert casa1.id != casa2.id


def test_home_con_caracteres_especiales():
    """Test: Hogar con caracteres especiales"""
    home = Home(3, "Casa de María & José")
    assert home.name == "Casa de María & José"