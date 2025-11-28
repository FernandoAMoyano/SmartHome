"""
Configuración y fixtures compartidos para todos los tests.

Este archivo contiene fixtures reutilizables que estarán disponibles
para todos los tests del proyecto.
"""

import pytest
from unittest.mock import Mock
from datetime import datetime

# ============================================
# FIXTURES DE ENTIDADES DE DOMINIO
# ============================================


@pytest.fixture
def role_admin():
    """Fixture: Rol de administrador"""
    from dominio.role import Role

    return Role(1, "admin")


@pytest.fixture
def role_standard():
    """Fixture: Rol de usuario estándar"""
    from dominio.role import Role

    return Role(2, "standard")


@pytest.fixture
def usuario_admin(role_admin):
    """Fixture: Usuario administrador de prueba"""
    from dominio.user import User

    return User(
        email="admin@test.com", password="admin123", name="Admin Test", role=role_admin
    )


@pytest.fixture
def usuario_standard(role_standard):
    """Fixture: Usuario estándar de prueba"""
    from dominio.user import User

    return User(
        email="user@test.com", password="user123", name="User Test", role=role_standard
    )


@pytest.fixture
def home_test():
    """Fixture: Hogar de prueba"""
    from dominio.home import Home

    return Home(1, "Casa Test")


@pytest.fixture
def state_encendido():
    """Fixture: Estado 'Encendido'"""
    from dominio.state import State

    return State(1, "Encendido")


@pytest.fixture
def state_apagado():
    """Fixture: Estado 'Apagado'"""
    from dominio.state import State

    return State(2, "Apagado")


@pytest.fixture
def device_type_luz():
    """Fixture: Tipo de dispositivo 'Luz'"""
    from dominio.device_type import DeviceType

    return DeviceType(1, "Luz Inteligente", "LED controlable")


@pytest.fixture
def location_sala(home_test):
    """Fixture: Ubicación 'Sala'"""
    from dominio.location import Location

    return Location(1, "Sala", home_test)


@pytest.fixture
def dispositivo_luz_sala(state_encendido, device_type_luz, location_sala, home_test):
    """Fixture: Dispositivo 'Luz de Sala' completo"""
    from dominio.device import Device

    return Device(
        id=1,
        name="Luz Sala",
        state=state_encendido,
        device_type=device_type_luz,
        location=location_sala,
        home=home_test,
    )


@pytest.fixture
def automatizacion_test(home_test):
    """Fixture: Automatización de prueba"""
    from dominio.automation import Automation

    return Automation(
        id=1,
        name="Modo Nocturno",
        description="Apaga todas las luces",
        active=True,
        home=home_test,
    )


# ============================================
# FIXTURES DE MOCKS DE DAOs
# ============================================


@pytest.fixture
def mock_user_dao():
    """Mock del UserDAO"""
    return Mock()


@pytest.fixture
def mock_role_dao():
    """Mock del RoleDAO"""
    return Mock()


@pytest.fixture
def mock_device_dao():
    """Mock del DeviceDAO"""
    return Mock()


@pytest.fixture
def mock_home_dao():
    """Mock del HomeDAO"""
    return Mock()


@pytest.fixture
def mock_state_dao():
    """Mock del StateDAO"""
    return Mock()


@pytest.fixture
def mock_device_type_dao():
    """Mock del DeviceTypeDAO"""
    return Mock()


@pytest.fixture
def mock_location_dao():
    """Mock del LocationDAO"""
    return Mock()


@pytest.fixture
def mock_automation_dao():
    """Mock del AutomationDAO"""
    return Mock()


# ============================================
# FIXTURES DE DATOS DE PRUEBA
# ============================================


@pytest.fixture
def datos_registro_validos():
    """Datos válidos para registro de usuario"""
    return {
        "email": "nuevo@test.com",
        "password": "password123",
        "name": "Nuevo Usuario",
    }


@pytest.fixture
def datos_login_validos():
    """Datos válidos para login"""
    return {"email": "user@test.com", "password": "user123"}


@pytest.fixture
def datos_dispositivo_validos():
    """Datos válidos para crear dispositivo"""
    return {
        "nombre": "Luz Cocina",
        "home_id": 1,
        "type_id": 1,
        "location_id": 2,
        "state_id": 1,
    }


@pytest.fixture
def datos_automatizacion_validos():
    """Datos válidos para crear automatización"""
    return {
        "nombre": "Modo Ahorro",
        "descripcion": "Reduce consumo energético",
        "home_id": 1,
        "activar": True,
    }


# ============================================
# FIXTURES DE SERVICIOS MOCKEADOS
# ============================================


@pytest.fixture
def mock_auth_service(mock_user_dao, mock_role_dao):
    """Mock completo de AuthService con DAOs"""
    from services.auth_service import AuthService

    service = AuthService()
    service.user_dao = mock_user_dao
    service.role_dao = mock_role_dao

    return service


@pytest.fixture
def mock_device_service(
    mock_device_dao,
    mock_home_dao,
    mock_state_dao,
    mock_device_type_dao,
    mock_location_dao,
):
    """Mock completo de DeviceService con DAOs"""
    from services.device_service import DeviceService

    service = DeviceService()
    service.device_dao = mock_device_dao
    service.home_dao = mock_home_dao
    service.state_dao = mock_state_dao
    service.device_type_dao = mock_device_type_dao
    service.location_dao = mock_location_dao

    return service


@pytest.fixture
def mock_automation_service(mock_automation_dao, mock_home_dao):
    """Mock completo de AutomationService con DAOs"""
    from services.automation_service import AutomationService

    service = AutomationService()
    service.automation_dao = mock_automation_dao
    service.home_dao = mock_home_dao

    return service


# ============================================
# FIXTURES HELPERS
# ============================================


@pytest.fixture
def capturar_salida(capsys):
    """Helper para capturar salida de print()"""

    def _capturar():
        captured = capsys.readouterr()
        return captured.out, captured.err

    return _capturar


@pytest.fixture
def fecha_hora_test():
    """Fecha y hora fija para tests"""
    return datetime(2024, 11, 28, 14, 30, 0)


# ============================================
# HOOKS DE PYTEST
# ============================================


def pytest_configure(config):
    """Configuración inicial de pytest"""
    config.addinivalue_line("markers", "unit: Tests unitarios")
    config.addinivalue_line("markers", "integration: Tests de integración")
    config.addinivalue_line("markers", "slow: Tests lentos")
    config.addinivalue_line("markers", "db: Tests que requieren BD")


def pytest_report_header(config):
    """Header personalizado para reporte de pytest"""
    return [
        "SmartHome Test Suite",
        "=" * 60,
        "Testing: Services, DAOs, and Integration",
    ]
