"""
Tests para la clase Automation
Estos tests verifican el funcionamiento de las automatizaciones del sistema.
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "models"))

from dominio.automation import Automation
from dominio.home import Home


class TestAutomation:
    """Tests para la clase Automation"""

    def test_crear_automation_luces_salon(self):
        """Test: Crear automatización 'Encender Luces Salón'"""
        home = Home(1, "Casa Principal")
        automation = Automation(
            1, "Encender Luces Salón", "Enciende luces del salón", True, home
        )

        assert automation.id == 1
        assert automation.name == "Encender Luces Salón"
        assert automation.description == "Enciende luces del salón"
        assert automation.active
        assert automation.home.id == 1

    def test_crear_automation_modo_nocturno(self):
        """Test: Crear automatización 'Modo Nocturno'"""
        home = Home(1, "Casa Principal")
        automation = Automation(3, "Modo Nocturno", "Configuración nocturna", True, home)

        assert automation.id == 3
        assert automation.name == "Modo Nocturno"
        assert automation.description == "Configuración nocturna"
        assert automation.active

    def test_crear_automation_inactiva(self):
        """Test: Crear automatización inactiva"""
        home = Home(1, "Casa Principal")
        automation = Automation(7, "Ventilación Auto", "Control automático", False, home)

        assert automation.id == 7
        assert automation.name == "Ventilación Auto"
        assert not automation.active

    def test_cambiar_nombre_automation(self):
        """Test: Modificar el nombre de la automatización"""
        # Arrange
        home = Home(1, "Casa")
        automation = Automation(1, "Luces", "Descripción", True, home)
        nuevo_nombre = "Luces Inteligentes"

        # Act
        automation.name = nuevo_nombre

        # Assert
        assert automation.name == "Luces Inteligentes"
        assert automation.id == 1  # ID no cambia

    def test_cambiar_descripcion_automation(self):
        """Test: Modificar la descripción de la automatización"""
        # Arrange
        home = Home(1, "Casa")
        automation = Automation(2, "Test", "Descripción original", True, home)
        nueva_descripcion = "Nueva descripción detallada"

        # Act
        automation.description = nueva_descripcion

        # Assert
        assert automation.description == "Nueva descripción detallada"
        assert automation.name == "Test"  # Nombre no cambia

    def test_activar_automation(self):
        """Test: Activar una automatización inactiva"""
        # Arrange
        home = Home(2, "Casa 2")
        automation = Automation(4, "Seguridad", "Modo seguridad", False, home)

        # Act
        automation.activate()

        # Assert
        assert automation.active

    def test_desactivar_automation(self):
        """Test: Desactivar una automatización activa"""
        # Arrange
        home = Home(3, "Casa 3")
        automation = Automation(5, "Ahorro", "Ahorro energía", True, home)

        # Act
        automation.deactivate()

        # Assert
        assert not automation.active

    def test_str_automation(self):
        """Test: Verificar que la automatización tiene los atributos correctos"""
        home = Home(1, "Casa")
        automation = Automation(1, "Test Auto", "Descripción test", True, home)

        # Verificar atributos clave
        assert automation.name == "Test Auto"
        assert automation.description == "Descripción test"
        assert automation.active

    def test_types_automation(self):
        """Test: Verificar tipos de datos correctos"""
        home = Home(2, "Casa 2")
        automation = Automation(6, "Test", "Desc", False, home)

        assert isinstance(automation.id, int)
        assert isinstance(automation.name, str)
        assert isinstance(automation.description, str)
        assert isinstance(automation.active, bool)
        assert isinstance(automation.home.id, int)


# Tests simples
def test_automation_basica():
    """Test básico: Crear una automatización"""
    home = Home(1, "Casa")
    automation = Automation(1, "Test", "Descripción test", True, home)
    assert automation.name == "Test"


def test_automation_activa():
    """Test: Verificar automatización activa"""
    home = Home(1, "Casa")
    automation = Automation(2, "Activa", "Test", True, home)
    assert automation.active


def test_automation_inactiva():
    """Test: Verificar automatización inactiva"""
    home = Home(1, "Casa")
    automation = Automation(3, "Inactiva", "Test", False, home)
    assert not automation.active


def test_cambiar_estado_automation():
    """Test: Cambiar estado de activa a inactiva"""
    home = Home(1, "Casa")
    automation = Automation(4, "Cambio", "Test", True, home)
    automation.deactivate()
    assert not automation.active


def test_automation_descripcion_larga():
    """Test: Automatización con descripción larga"""
    descripcion_larga = (
        "Esta es una automatización muy compleja que realiza múltiples acciones"
    )
    home = Home(1, "Casa")
    automation = Automation(5, "Compleja", descripcion_larga, True, home)
    assert automation.description == descripcion_larga


def test_activate_automation():
    """Test: Activar una automatización inactiva"""
    home = Home(1, "Casa")
    automation = Automation(6, "Test", "Descripción", False, home)
    
    # Verificar que está inactiva
    assert not automation.active
    
    # Activar
    automation.activate()
    
    # Verificar que está activa
    assert automation.active


def test_deactivate_automation():
    """Test: Desactivar una automatización activa"""
    home = Home(1, "Casa")
    automation = Automation(7, "Test", "Descripción", True, home)
    
    # Verificar que está activa
    assert automation.active
    
    # Desactivar
    automation.deactivate()
    
    # Verificar que está inactiva
    assert not automation.active


def test_toggle_automation_state():
    """Test: Alternar estado de automatización múltiples veces"""
    home = Home(1, "Casa")
    automation = Automation(8, "Toggle", "Test", True, home)
    
    # Inicial: activa
    assert automation.active
    
    # Desactivar
    automation.deactivate()
    assert not automation.active
    
    # Activar nuevamente
    automation.activate()
    assert automation.active
    
    # Desactivar nuevamente
    automation.deactivate()
    assert not automation.active