"""
Tests para la clase User
Estos tests verifican el funcionamiento de los usuarios del sistema.
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "dominio"))

from dominio.user import User
from dominio.role import Role


class TestUser:
    """Tests para la clase User"""

    def test_crear_user_administrador(self):
        """Test: Crear usuario administrador"""
        role_admin = Role(1, "Administrador")
        user = User("admin@smarthome.com", "password123", "Administrador", role_admin)

        assert user.email == "admin@smarthome.com"
        assert user.name == "Administrador"
        assert user.role.id == 1

    def test_crear_user_normal(self):
        """Test: Crear usuario normal"""
        role_user = Role(2, "Usuario")
        user = User("usuario@gmail.com", "secreto456", "Usuario Normal", role_user)

        assert user.email == "usuario@gmail.com"
        assert user.name == "Usuario Normal"
        assert user.role.id == 2

    def test_crear_user_visitante(self):
        """Test: Crear usuario visitante"""
        role_visitante = Role(3, "Visitante")
        user = User("invitado@smarthome.com", "temp789", "Usuario Invitado", role_visitante)

        assert user.email == "invitado@smarthome.com"
        assert user.name == "Usuario Invitado"
        assert user.role.id == 3

    def test_cambiar_nombre_user(self):
        """Test: Modificar el nombre del usuario"""
        # Arrange
        role = Role(2, "Usuario")
        user = User("test@test.com", "pass", "Nombre Original", role)
        nuevo_nombre = "Nombre Modificado"

        # Act
        user.name = nuevo_nombre

        # Assert
        assert user.name == "Nombre Modificado"
        assert user.email == "test@test.com"  # Email no cambia

    def test_cambiar_password_user(self):
        """Test: Cambiar la contraseña del usuario"""
        # Arrange
        role = Role(2, "Usuario")
        user = User("user@test.com", "password_vieja", "Usuario", role)
        nueva_password = "password_nueva"

        # Act
        user.change_password(nueva_password)

        # Assert
        assert user.name == "Usuario"  # Otros datos no cambian
        # Verificamos que la contraseña cambió validando credenciales
        assert user.validate_credentials("user@test.com", "password_nueva")

    def test_validar_credenciales_correctas(self):
        """Test: Validar credenciales correctas"""
        # Arrange
        email = "usuario@test.com"
        password = "mi_password"
        role = Role(2, "Usuario")
        user = User(email, password, "Test User", role)

        # Act & Assert
        assert user.validate_credentials(email, password)

    def test_validar_credenciales_incorrectas_email(self):
        """Test: Validar credenciales con email incorrecto"""
        role = Role(2, "Usuario")
        user = User("correcto@test.com", "password123", "Usuario", role)

        # Email incorrecto
        assert not user.validate_credentials("incorrecto@test.com", "password123")

    def test_validar_credenciales_incorrectas_password(self):
        """Test: Validar credenciales con password incorrecta"""
        role = Role(2, "Usuario")
        user = User("usuario@test.com", "password_correcta", "Usuario", role)

        # Password incorrecta
        assert not user.validate_credentials("usuario@test.com", "password_incorrecta")

    def test_types_user(self):
        """Test: Verificar tipos de datos correctos"""
        role = Role(1, "Administrador")
        user = User("test@test.com", "pass", "Test", role)

        assert isinstance(user.email, str)
        assert isinstance(user.name, str)
        assert isinstance(user.role.id, int)


# Tests simples
def test_user_basico():
    """Test básico: Crear un usuario"""
    role = Role(1, "Administrador")
    user = User("test@test.com", "123", "Test", role)
    assert user.email == "test@test.com"


def test_login_exitoso():
    """Test: Login exitoso"""
    role = Role(1, "Administrador")
    user = User("fernando@gmail.com", "mi_clave", "Fernando", role)
    assert user.validate_credentials("fernando@gmail.com", "mi_clave")


def test_login_fallido():
    """Test: Login fallido"""
    role = Role(2, "Usuario")
    user = User("santiago@gmail.com", "clave_secreta", "Santiago", role)
    assert not user.validate_credentials("santiago@gmail.com", "clave_incorrecta")


def test_cambio_nombre():
    """Test: Cambiar nombre de usuario"""
    role = Role(2, "Usuario")
    user = User("maria@test.com", "pass", "María Original", role)
    user.name = "María Modificada"
    assert user.name == "María Modificada"


def test_is_admin_true():
    """Test: Verificar que is_admin() retorna True para administradores"""
    role_admin = Role(1, "admin")
    user = User("admin@test.com", "pass", "Admin", role_admin)
    assert user.is_admin() is True


def test_is_admin_false():
    """Test: Verificar que is_admin() retorna False para usuarios normales"""
    role_user = Role(2, "Usuario")
    user = User("user@test.com", "pass", "User", role_user)
    assert user.is_admin() is False


def test_is_admin_case_insensitive():
    """Test: Verificar que is_admin() funciona sin importar mayúsculas"""
    role_admin = Role(1, "ADMIN")
    user = User("admin@test.com", "pass", "Admin", role_admin)
    assert user.is_admin() is True


def test_change_password():
    """Test: Cambiar contraseña del usuario"""
    role = Role(2, "Usuario")
    user = User("test@test.com", "old_password", "Test", role)
    
    # Cambiar password
    user.change_password("new_password")
    
    # Verificar que la nueva password funciona
    assert user.validate_credentials("test@test.com", "new_password")
    # Verificar que la vieja password ya no funciona
    assert not user.validate_credentials("test@test.com", "old_password")


def test_cambiar_rol_usuario():
    """Test: Cambiar el rol de un usuario"""
    role_user = Role(2, "Usuario")
    role_admin = Role(1, "admin")
    user = User("test@test.com", "pass", "Test", role_user)
    
    # Verificar rol inicial
    assert not user.is_admin()
    
    # Cambiar rol
    user.role = role_admin
    
    # Verificar nuevo rol
    assert user.is_admin()
    assert user.role.id == 1