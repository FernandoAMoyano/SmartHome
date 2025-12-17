"""
Tests para AutomationDAO
Estos tests verifican las operaciones CRUD de automatizaciones.
"""

import pytest
from dao.automation_dao import AutomationDAO
from dao.home_dao import HomeDAO
from dominio.automation import Automation


@pytest.fixture
def automation_dao():
    """Fixture que proporciona una instancia de AutomationDAO."""
    return AutomationDAO()


@pytest.fixture
def home_dao():
    """Fixture que proporciona una instancia de HomeDAO."""
    return HomeDAO()


class TestAutomationDAO:
    """Tests para la clase AutomationDAO"""

    def test_obtener_todas_automations(self, automation_dao):
        """Test: Obtener todas las automatizaciones de la BD"""
        automatizaciones = automation_dao.obtener_todos()
        
        assert isinstance(automatizaciones, list)
        assert len(automatizaciones) >= 0
        
        # Si hay automatizaciones, verificar estructura
        if automatizaciones:
            automation = automatizaciones[0]
            assert hasattr(automation, 'id')
            assert hasattr(automation, 'name')
            assert hasattr(automation, 'description')
            assert hasattr(automation, 'active')
            assert hasattr(automation, 'home')

    def test_obtener_automation_por_id(self, automation_dao):
        """Test: Obtener una automatización específica por ID"""
        automation = automation_dao.obtener_por_id(1)
        
        if automation:
            assert automation.id == 1
            assert isinstance(automation.name, str)
            assert isinstance(automation.description, str)
            assert isinstance(automation.active, bool)
            assert automation.home is not None

    def test_obtener_automation_inexistente(self, automation_dao):
        """Test: Intentar obtener una automatización que no existe"""
        automation = automation_dao.obtener_por_id(99999)
        assert automation is None

    def test_obtener_por_hogar(self, automation_dao):
        """Test: Obtener automatizaciones de un hogar específico"""
        automatizaciones = automation_dao.obtener_por_hogar(1)
        
        assert isinstance(automatizaciones, list)
        
        # Verificar que todas pertenecen al hogar 1
        for automation in automatizaciones:
            assert automation.home.id == 1

    def test_obtener_por_hogar_inexistente(self, automation_dao):
        """Test: Obtener automatizaciones de un hogar que no existe"""
        automatizaciones = automation_dao.obtener_por_hogar(99999)
        assert isinstance(automatizaciones, list)
        assert len(automatizaciones) == 0

    def test_obtener_activas(self, automation_dao):
        """Test: Obtener solo las automatizaciones activas de un hogar"""
        automatizaciones = automation_dao.obtener_activas(1)
        
        assert isinstance(automatizaciones, list)
        
        # Verificar que todas están activas
        for automation in automatizaciones:
            assert automation.active is True
            assert automation.home.id == 1

    def test_cambiar_estado_activar(self, automation_dao):
        """Test: Activar una automatización"""
        # Obtener una automatización
        automation = automation_dao.obtener_por_id(1)
        
        if automation:
            # Desactivar primero para asegurar el estado
            automation_dao.cambiar_estado(1, False)
            
            # Activar
            exito = automation_dao.cambiar_estado(1, True)
            assert exito is True
            
            # Verificar que está activa
            automation_actualizada = automation_dao.obtener_por_id(1)
            assert automation_actualizada.active is True

    def test_cambiar_estado_desactivar(self, automation_dao):
        """Test: Desactivar una automatización"""
        # Obtener una automatización
        automation = automation_dao.obtener_por_id(1)
        
        if automation:
            estado_original = automation.active
            
            # Desactivar
            exito = automation_dao.cambiar_estado(1, False)
            assert exito is True
            
            # Verificar que está inactiva
            automation_actualizada = automation_dao.obtener_por_id(1)
            assert automation_actualizada.active is False
            
            # Restaurar estado original
            automation_dao.cambiar_estado(1, estado_original)

    def test_insertar_automation(self, automation_dao, home_dao):
        """Test: Insertar una nueva automatización"""
        home = home_dao.obtener_por_id(1)
        
        if home:
            automation = Automation(0, "Test Automation", "Descripción test", True, home)
            exito = automation_dao.insertar(automation)
            assert exito is True

    def test_modificar_automation(self, automation_dao):
        """Test: Modificar una automatización existente"""
        automation = automation_dao.obtener_por_id(1)
        
        if automation:
            nombre_original = automation.name
            automation.name = "Automatización Modificada Test"
            
            exito = automation_dao.modificar(automation)
            assert exito is True
            
            # Verificar cambio
            automation_modificada = automation_dao.obtener_por_id(1)
            assert automation_modificada.name == "Automatización Modificada Test"
            
            # Restaurar nombre original
            automation.name = nombre_original
            automation_dao.modificar(automation)

    def test_eliminar_automation_inexistente(self, automation_dao):
        """Test: Intentar eliminar una automatización que no existe"""
        exito = automation_dao.eliminar(99999)
        assert exito is False


# Tests simples adicionales
def test_automation_dao_instancia():
    """Test: Crear una instancia de AutomationDAO"""
    dao = AutomationDAO()
    assert dao is not None
    assert hasattr(dao, 'obtener_todos')
    assert hasattr(dao, 'obtener_por_id')
    assert hasattr(dao, 'obtener_por_hogar')
    assert hasattr(dao, 'obtener_activas')
    assert hasattr(dao, 'cambiar_estado')
