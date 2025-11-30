"""
Tests para RoleDAO (Data Access Object de Roles)

Cubre:
- Insertar roles
- Modificar roles
- Eliminar roles
- Obtener por ID
- Obtener todos
"""

from unittest.mock import MagicMock, patch
from dao.role_dao import RoleDAO


class TestRoleDAOInsertar:
    """Tests para inserción de roles"""

    def test_insertar_rol_exitoso(self, role_admin):
        """Test: Insertar rol correctamente"""
        # Arrange
        dao = RoleDAO()
        mock_cursor = MagicMock()

        with patch.object(dao.db, "get_cursor", return_value=mock_cursor):
            with patch.object(dao.db, "commit"):
                # Act
                resultado = dao.insertar(role_admin)

                # Assert
                assert resultado is True
                mock_cursor.execute.assert_called_once()
                mock_cursor.close.assert_called_once()


class TestRoleDAOModificar:
    """Tests para modificación de roles"""

    def test_modificar_rol_exitoso(self, role_admin):
        """Test: Modificar rol correctamente"""
        # Arrange
        dao = RoleDAO()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1

        with patch.object(dao.db, "get_cursor", return_value=mock_cursor):
            with patch.object(dao.db, "commit"):
                # Act
                resultado = dao.modificar(role_admin)

                # Assert
                assert resultado is True

    def test_modificar_rol_no_encontrado(self, role_admin):
        """Test: Modificar rol que no existe"""
        # Arrange
        dao = RoleDAO()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0

        with patch.object(dao.db, "get_cursor", return_value=mock_cursor):
            with patch.object(dao.db, "commit"):
                # Act
                resultado = dao.modificar(role_admin)

                # Assert
                assert resultado is False


class TestRoleDAOEliminar:
    """Tests para eliminación de roles"""

    def test_eliminar_rol_exitoso(self):
        """Test: Eliminar rol correctamente"""
        # Arrange
        dao = RoleDAO()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1

        with patch.object(dao.db, "get_cursor", return_value=mock_cursor):
            with patch.object(dao.db, "commit"):
                # Act
                resultado = dao.eliminar(1)

                # Assert
                assert resultado is True

    def test_eliminar_rol_no_encontrado(self):
        """Test: Eliminar rol que no existe"""
        # Arrange
        dao = RoleDAO()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0

        with patch.object(dao.db, "get_cursor", return_value=mock_cursor):
            with patch.object(dao.db, "commit"):
                # Act
                resultado = dao.eliminar(999)

                # Assert
                assert resultado is False


class TestRoleDAOObtener:
    """Tests para obtención de roles"""

    def test_obtener_por_id_exitoso(self):
        """Test: Obtener rol por ID"""
        # Arrange
        dao = RoleDAO()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {"id": 1, "name": "Admin"}

        with patch.object(dao.db, "get_cursor", return_value=mock_cursor):
            # Act
            rol = dao.obtener_por_id(1)

            # Assert
            assert rol is not None
            assert rol.id == 1
            assert rol.name == "Admin"

    def test_obtener_por_id_no_encontrado(self):
        """Test: Obtener rol que no existe"""
        # Arrange
        dao = RoleDAO()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None

        with patch.object(dao.db, "get_cursor", return_value=mock_cursor):
            # Act
            rol = dao.obtener_por_id(999)

            # Assert
            assert rol is None

    def test_obtener_todos_exitoso(self):
        """Test: Obtener todos los roles"""
        # Arrange
        dao = RoleDAO()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {"id": 1, "name": "Admin"},
            {"id": 2, "name": "Standard"},
            {"id": 3, "name": "Guest"},
        ]

        with patch.object(dao.db, "get_cursor", return_value=mock_cursor):
            # Act
            roles = dao.obtener_todos()

            # Assert
            assert len(roles) == 3
            assert roles[0].name == "Admin"
            assert roles[1].name == "Standard"
            assert roles[2].name == "Guest"

    def test_obtener_todos_vacio(self):
        """Test: Obtener todos cuando no hay roles"""
        # Arrange
        dao = RoleDAO()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []

        with patch.object(dao.db, "get_cursor", return_value=mock_cursor):
            # Act
            roles = dao.obtener_todos()

            # Assert
            assert roles == []
