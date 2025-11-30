"""
Tests para UserDAO (Data Access Object de Usuarios)

Cubre:
- Insertar usuarios
- Modificar usuarios
- Eliminar usuarios
- Obtener por email
- Obtener todos
- Cambiar rol
- Validar credenciales
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from dao.user_dao import UserDAO
from dominio.user import User
from dominio.role import Role


class TestUserDAOInsertar:
    """Tests para inserción de usuarios"""
    
    def test_insertar_usuario_exitoso(self, usuario_admin):
        """Test: Insertar usuario correctamente"""
        # Arrange
        dao = UserDAO()
        mock_cursor = MagicMock()
        
        with patch.object(dao.db, 'get_cursor', return_value=mock_cursor):
            with patch.object(dao.db, 'commit'):
                # Act
                resultado = dao.insertar(usuario_admin)
                
                # Assert
                assert resultado is True
                mock_cursor.execute.assert_called_once()
                mock_cursor.close.assert_called_once()


class TestUserDAOModificar:
    """Tests para modificación de usuarios"""
    
    def test_modificar_usuario_exitoso(self, usuario_admin):
        """Test: Modificar usuario correctamente"""
        # Arrange
        dao = UserDAO()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        
        with patch.object(dao.db, 'get_cursor', return_value=mock_cursor):
            with patch.object(dao.db, 'commit'):
                # Act
                resultado = dao.modificar(usuario_admin)
                
                # Assert
                assert resultado is True
                mock_cursor.execute.assert_called_once()
    
    def test_modificar_usuario_no_encontrado(self, usuario_admin):
        """Test: Modificar usuario que no existe"""
        # Arrange
        dao = UserDAO()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0
        
        with patch.object(dao.db, 'get_cursor', return_value=mock_cursor):
            with patch.object(dao.db, 'commit'):
                # Act
                resultado = dao.modificar(usuario_admin)
                
                # Assert
                assert resultado is False


class TestUserDAOEliminar:
    """Tests para eliminación de usuarios"""
    
    def test_eliminar_usuario_exitoso(self):
        """Test: Eliminar usuario correctamente"""
        # Arrange
        dao = UserDAO()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        
        with patch.object(dao.db, 'get_cursor', return_value=mock_cursor):
            with patch.object(dao.db, 'commit'):
                # Act
                resultado = dao.eliminar("user@test.com")
                
                # Assert
                assert resultado is True
                mock_cursor.execute.assert_called_once()
    
    def test_eliminar_usuario_no_encontrado(self):
        """Test: Eliminar usuario que no existe"""
        # Arrange
        dao = UserDAO()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0
        
        with patch.object(dao.db, 'get_cursor', return_value=mock_cursor):
            with patch.object(dao.db, 'commit'):
                # Act
                resultado = dao.eliminar("noexiste@test.com")
                
                # Assert
                assert resultado is False


class TestUserDAOObtener:
    """Tests para obtención de usuarios"""
    
    def test_obtener_por_email_exitoso(self, role_admin):
        """Test: Obtener usuario por email"""
        # Arrange
        dao = UserDAO()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {
            'email': 'admin@test.com',
            'password': 'pass123',
            'name': 'Admin',
            'role_id': 1
        }
        
        with patch.object(dao.db, 'get_cursor', return_value=mock_cursor):
            with patch.object(dao.role_dao, 'obtener_por_id', return_value=role_admin):
                # Act
                usuario = dao.obtener_por_email("admin@test.com")
                
                # Assert
                assert usuario is not None
                assert usuario.email == 'admin@test.com'
                assert usuario.name == 'Admin'
    
    def test_obtener_por_email_no_encontrado(self):
        """Test: Obtener usuario que no existe"""
        # Arrange
        dao = UserDAO()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        
        with patch.object(dao.db, 'get_cursor', return_value=mock_cursor):
            # Act
            usuario = dao.obtener_por_email("noexiste@test.com")
            
            # Assert
            assert usuario is None
    
    def test_obtener_por_id_llama_obtener_por_email(self, role_admin):
        """Test: obtener_por_id usa obtener_por_email"""
        # Arrange
        dao = UserDAO()
        
        with patch.object(dao, 'obtener_por_email') as mock_obtener:
            # Act
            dao.obtener_por_id("test@test.com")
            
            # Assert
            mock_obtener.assert_called_once_with("test@test.com")
    
    def test_obtener_todos_exitoso(self, role_admin, role_standard):
        """Test: Obtener todos los usuarios"""
        # Arrange
        dao = UserDAO()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {
                'email': 'admin@test.com',
                'password': 'pass1',
                'name': 'Admin',
                'role_id': 1
            },
            {
                'email': 'user@test.com',
                'password': 'pass2',
                'name': 'User',
                'role_id': 2
            }
        ]
        
        with patch.object(dao.db, 'get_cursor', return_value=mock_cursor):
            with patch.object(dao.role_dao, 'obtener_por_id', side_effect=[role_admin, role_standard]):
                # Act
                usuarios = dao.obtener_todos()
                
                # Assert
                assert len(usuarios) == 2
                assert usuarios[0].email == 'admin@test.com'
                assert usuarios[1].email == 'user@test.com'
    
    def test_obtener_todos_vacio(self):
        """Test: Obtener todos cuando no hay usuarios"""
        # Arrange
        dao = UserDAO()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        
        with patch.object(dao.db, 'get_cursor', return_value=mock_cursor):
            # Act
            usuarios = dao.obtener_todos()
            
            # Assert
            assert usuarios == []


class TestUserDAOCambiarRol:
    """Tests para cambio de rol"""
    
    def test_cambiar_rol_exitoso(self):
        """Test: Cambiar rol correctamente"""
        # Arrange
        dao = UserDAO()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        
        with patch.object(dao.db, 'get_cursor', return_value=mock_cursor):
            with patch.object(dao.db, 'commit'):
                # Act
                resultado = dao.cambiar_rol("user@test.com", 1)
                
                # Assert
                assert resultado is True
                mock_cursor.execute.assert_called_once()
    
    def test_cambiar_rol_usuario_no_encontrado(self):
        """Test: Cambiar rol de usuario inexistente"""
        # Arrange
        dao = UserDAO()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0
        
        with patch.object(dao.db, 'get_cursor', return_value=mock_cursor):
            with patch.object(dao.db, 'commit'):
                # Act
                resultado = dao.cambiar_rol("noexiste@test.com", 1)
                
                # Assert
                assert resultado is False


class TestUserDAOValidarCredenciales:
    """Tests para validación de credenciales"""
    
    def test_validar_credenciales_correctas(self, usuario_admin):
        """Test: Credenciales válidas"""
        # Arrange
        dao = UserDAO()
        
        with patch.object(dao, 'obtener_por_email', return_value=usuario_admin):
            # Act
            resultado = dao.validar_credenciales("admin@test.com", "admin123")
            
            # Assert
            assert resultado is not None
            assert resultado.email == "admin@test.com"
    
    def test_validar_credenciales_incorrectas(self, usuario_admin):
        """Test: Credenciales inválidas"""
        # Arrange
        dao = UserDAO()
        
        with patch.object(dao, 'obtener_por_email', return_value=usuario_admin):
            # Act
            resultado = dao.validar_credenciales("admin@test.com", "wrongpass")
            
            # Assert
            assert resultado is None
    
    def test_validar_credenciales_usuario_no_existe(self):
        """Test: Usuario no existe"""
        # Arrange
        dao = UserDAO()
        
        with patch.object(dao, 'obtener_por_email', return_value=None):
            # Act
            resultado = dao.validar_credenciales("noexiste@test.com", "pass")
            
            # Assert
            assert resultado is None
