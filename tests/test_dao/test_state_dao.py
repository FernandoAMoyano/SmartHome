"""
Tests para StateDAO (Data Access Object de Estados)

Cubre:
- Insertar estados
- Modificar estados
- Eliminar estados
- Obtener por ID
- Obtener todos
"""

from unittest.mock import MagicMock, patch
from dao.state_dao import StateDAO


class TestStateDAOInsertar:
    """Tests para inserción de estados"""

    def test_insertar_estado_exitoso(self, state_encendido):
        """Test: Insertar estado correctamente"""
        # Arrange
        dao = StateDAO()
        mock_cursor = MagicMock()

        with patch.object(dao.db, "get_cursor", return_value=mock_cursor):
            with patch.object(dao.db, "commit"):
                # Act
                resultado = dao.insertar(state_encendido)

                # Assert
                assert resultado is True
                mock_cursor.execute.assert_called_once()


class TestStateDAOModificar:
    """Tests para modificación de estados"""

    def test_modificar_estado_exitoso(self, state_encendido):
        """Test: Modificar estado correctamente"""
        # Arrange
        dao = StateDAO()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1

        with patch.object(dao.db, "get_cursor", return_value=mock_cursor):
            with patch.object(dao.db, "commit"):
                # Act
                resultado = dao.modificar(state_encendido)

                # Assert
                assert resultado is True

    def test_modificar_estado_no_encontrado(self, state_encendido):
        """Test: Modificar estado que no existe"""
        # Arrange
        dao = StateDAO()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0

        with patch.object(dao.db, "get_cursor", return_value=mock_cursor):
            with patch.object(dao.db, "commit"):
                # Act
                resultado = dao.modificar(state_encendido)

                # Assert
                assert resultado is False


class TestStateDAOEliminar:
    """Tests para eliminación de estados"""

    def test_eliminar_estado_exitoso(self):
        """Test: Eliminar estado correctamente"""
        # Arrange
        dao = StateDAO()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1

        with patch.object(dao.db, "get_cursor", return_value=mock_cursor):
            with patch.object(dao.db, "commit"):
                # Act
                resultado = dao.eliminar(1)

                # Assert
                assert resultado is True

    def test_eliminar_estado_no_encontrado(self):
        """Test: Eliminar estado que no existe"""
        # Arrange
        dao = StateDAO()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0

        with patch.object(dao.db, "get_cursor", return_value=mock_cursor):
            with patch.object(dao.db, "commit"):
                # Act
                resultado = dao.eliminar(999)

                # Assert
                assert resultado is False


class TestStateDAOObtener:
    """Tests para obtención de estados"""

    def test_obtener_por_id_exitoso(self):
        """Test: Obtener estado por ID"""
        # Arrange
        dao = StateDAO()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {"id": 1, "name": "Encendido"}

        with patch.object(dao.db, "get_cursor", return_value=mock_cursor):
            # Act
            estado = dao.obtener_por_id(1)

            # Assert
            assert estado is not None
            assert estado.id == 1
            assert estado.name == "Encendido"

    def test_obtener_por_id_no_encontrado(self):
        """Test: Obtener estado que no existe"""
        # Arrange
        dao = StateDAO()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None

        with patch.object(dao.db, "get_cursor", return_value=mock_cursor):
            # Act
            estado = dao.obtener_por_id(999)

            # Assert
            assert estado is None

    def test_obtener_todos_exitoso(self):
        """Test: Obtener todos los estados"""
        # Arrange
        dao = StateDAO()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {"id": 1, "name": "Encendido"},
            {"id": 2, "name": "Apagado"},
            {"id": 3, "name": "Standby"},
        ]

        with patch.object(dao.db, "get_cursor", return_value=mock_cursor):
            # Act
            estados = dao.obtener_todos()

            # Assert
            assert len(estados) == 3
            assert estados[0].name == "Encendido"
            assert estados[1].name == "Apagado"

    def test_obtener_todos_vacio(self):
        """Test: Obtener todos cuando no hay estados"""
        # Arrange
        dao = StateDAO()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []

        with patch.object(dao.db, "get_cursor", return_value=mock_cursor):
            # Act
            estados = dao.obtener_todos()

            # Assert
            assert estados == []
