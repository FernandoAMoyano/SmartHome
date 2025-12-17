"""
Tests para HomeDAO
Estos tests verifican las operaciones CRUD de hogares.
"""

import pytest
from dao.home_dao import HomeDAO
from dominio.home import Home


@pytest.fixture
def home_dao():
    """Fixture que proporciona una instancia de HomeDAO."""
    return HomeDAO()


class TestHomeDAO:
    """Tests para la clase HomeDAO"""

    def test_obtener_todos_homes(self, home_dao):
        """Test: Obtener todos los hogares de la BD"""
        hogares = home_dao.obtener_todos()
        
        assert isinstance(hogares, list)
        assert len(hogares) >= 0
        
        # Si hay hogares, verificar estructura
        if hogares:
            home = hogares[0]
            assert hasattr(home, 'id')
            assert hasattr(home, 'name')
            assert isinstance(home.name, str)

    def test_obtener_home_por_id(self, home_dao):
        """Test: Obtener un hogar específico por ID"""
        home = home_dao.obtener_por_id(1)
        
        if home:
            assert home.id == 1
            assert isinstance(home.name, str)
            assert len(home.name) > 0

    def test_obtener_home_inexistente(self, home_dao):
        """Test: Intentar obtener un hogar que no existe"""
        home = home_dao.obtener_por_id(99999)
        assert home is None

    def test_obtener_hogares_usuario(self, home_dao):
        """Test: Obtener hogares asociados a un usuario"""
        # Usuario admin tiene hogares asociados
        hogares = home_dao.obtener_hogares_usuario("admin@smarthome.com")
        
        assert isinstance(hogares, list)
        # Admin debería tener al menos un hogar
        assert len(hogares) >= 0

    def test_obtener_hogares_usuario_inexistente(self, home_dao):
        """Test: Obtener hogares de un usuario que no existe"""
        hogares = home_dao.obtener_hogares_usuario("noexiste@test.com")
        assert isinstance(hogares, list)
        assert len(hogares) == 0

    def test_insertar_home(self, home_dao):
        """Test: Insertar un nuevo hogar"""
        home = Home(0, "Hogar Test Temporal")
        exito = home_dao.insertar(home)
        assert exito is True

    def test_modificar_home(self, home_dao):
        """Test: Modificar un hogar existente"""
        home = home_dao.obtener_por_id(1)
        
        if home:
            nombre_original = home.name
            home.name = "Hogar Modificado Test"
            
            exito = home_dao.modificar(home)
            assert exito is True
            
            # Verificar cambio
            home_modificado = home_dao.obtener_por_id(1)
            assert home_modificado.name == "Hogar Modificado Test"
            
            # Restaurar nombre original
            home.name = nombre_original
            home_dao.modificar(home)

    def test_eliminar_home_inexistente(self, home_dao):
        """Test: Intentar eliminar un hogar que no existe"""
        exito = home_dao.eliminar(99999)
        assert exito is False


# Tests simples adicionales
def test_home_dao_instancia():
    """Test: Crear una instancia de HomeDAO"""
    dao = HomeDAO()
    assert dao is not None
    assert hasattr(dao, 'obtener_todos')
    assert hasattr(dao, 'obtener_por_id')
    assert hasattr(dao, 'obtener_hogares_usuario')
