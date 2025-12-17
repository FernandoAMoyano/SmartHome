"""
Tests para la clase Role
Estos tests verifican que la clase Role funcione correctamente.
"""

# Importar pytest y la clase a testear
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "models"))

from dominio.role import Role


class TestRole:
    """Clase que contiene todos los tests para Role"""

    def test_crear_role_basico(self):
        """Test básico: Crear un rol y verificar que se creó correctamente"""
        # Arrange (Preparar) - Crear datos de prueba
        role_id = 1
        role_name = "Administrador"

        # Act (Actuar) - Ejecutar la acción que queremos testear
        role = Role(role_id, role_name)

        # Assert (Afirmar) - Verificar que el resultado es el esperado
        assert role.id == role_id
        assert role.name == role_name

    def test_crear_role_usuario(self):
        """Test: Crear un rol de Usuario"""
        # Arrange
        role_id = 2
        role_name = "Usuario"

        # Act
        role = Role(role_id, role_name)

        # Assert
        assert role.id == 2
        assert role.name == "Usuario"

    def test_crear_role_visitante(self):
        """Test: Crear un rol de Visitante"""
        # Arrange
        role_id = 3
        role_name = "Visitante"

        # Act
        role = Role(role_id, role_name)

        # Assert
        assert role.id == 3
        assert role.name == "Visitante"

    def test_types_correctos(self):
        """Test: Verificar que los métodos devuelven los tipos correctos"""
        # Arrange
        role = Role(1, "Admin")

        # Act & Assert
        assert isinstance(role.id, int)
        assert isinstance(role.name, str)


def test_role_simple():
    """Test simple para entender pytest - Crear un rol básico"""
    role = Role(1, "Test")
    assert role.id == 1
    assert role.name == "Test"


def test_role_con_numeros():
    """Test: Verificar que funciona con IDs diferentes"""
    role = Role(99, "RolEspecial")
    assert role.id == 99
    assert role.name == "RolEspecial"


def test_modificar_nombre_role():
    """Test: Modificar el nombre del rol usando el setter"""
    # Arrange
    role = Role(1, "Admin")

    # Act
    role.name = "Administrador"

    # Assert
    assert role.name == "Administrador"
    assert role.id == 1  # ID no debe cambiar
