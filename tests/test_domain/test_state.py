"""
Tests para la clase State
Estos tests verifican el funcionamiento de los estados de dispositivos.
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "models"))

from dominio.state import State


class TestState:
    """Tests para la clase State"""

    def test_crear_state_encendido(self):
        """Test: Crear estado 'Encendido'"""
        # Arrange
        state_id = 1
        state_name = "Encendido"

        # Act
        state = State(state_id, state_name)

        # Assert
        assert state.id == 1
        assert state.name == "Encendido"

    def test_crear_state_apagado(self):
        """Test: Crear estado 'Apagado'"""
        state = State(2, "Apagado")
        assert state.id == 2
        assert state.name == "Apagado"

    def test_crear_state_mantenimiento(self):
        """Test: Crear estado 'En Mantenimiento'"""
        state = State(3, "En Mantenimiento")
        assert state.id == 3
        assert state.name == "En Mantenimiento"

    def test_crear_state_error(self):
        """Test: Crear estado 'Error'"""
        state = State(4, "Error")
        assert state.id == 4
        assert state.name == "Error"

    def test_modificar_nombre_state(self):
        """Test: Verificar que se puede cambiar el nombre del estado"""
        # Arrange
        state = State(1, "Encendido")
        nuevo_nombre = "Activo"

        # Act
        state.name = nuevo_nombre

        # Assert
        assert state.name == "Activo"
        assert state.id == 1  # El ID no debe cambiar

    def test_types_state(self):
        """Test: Verificar tipos de datos correctos"""
        state = State(5, "Standby")
        assert isinstance(state.id, int)
        assert isinstance(state.name, str)


# Tests simples para principiantes
def test_state_basico():
    """Test básico: Crear un estado simple"""
    state = State(1, "Test")
    assert state.name == "Test"


def test_cambiar_nombre_state():
    """Test: Cambiar nombre de un estado"""
    state = State(2, "Original")
    state.name = "Modificado"
    assert state.name == "Modificado"