"""
Tests de integración básicos para SmartHome.

NOTA: Estos tests usan la BD REAL, no mocks.
Se requiere tener MySQL corriendo con la BD 'smarthome' configurada.
"""

import pytest
from services.auth_service import AuthService
from services.device_service import DeviceService
from conn.db_connection import DatabaseConnection


@pytest.mark.integration
@pytest.mark.slow
class TestAuthIntegrationBasic:
    """Tests de integración básicos para autenticación."""
    
    def setup_method(self):
        """Setup: Preparar servicio con BD real."""
        self.auth_service = AuthService()
        self.db = DatabaseConnection()
    
    def test_login_con_bd_real(self):
        """
        Test de integración: Login usando BD real.
        
        Este test:
        - NO usa mocks
        - Toca la BD real
        - Valida que Service + DAO + BD funcionan juntos
        """
        # Usar credencial que existe en la BD
        # (del DML que ya tienes cargado)
        exito, mensaje = self.auth_service.iniciar_sesion(
            email="admin@smarthome.com",
            password="admin123"
        )
        
        assert exito is True
        assert "Bienvenido" in mensaje
        assert self.auth_service.obtener_usuario_actual() is not None
        
        # Verificar datos del usuario
        datos = self.auth_service.obtener_datos_usuario()
        assert datos['email'] == "admin@smarthome.com"
        assert datos['rol'] == "admin"
        
        # Limpiar
        self.auth_service.cerrar_sesion()
    
    def test_login_credenciales_incorrectas_bd_real(self):
        """Test: Login fallido con BD real."""
        exito, mensaje = self.auth_service.iniciar_sesion(
            email="admin@smarthome.com",
            password="password_incorrecta"
        )
        
        assert exito is False
        # Puede decir "inválida(s)" o "incorrecta(s)" o "credencial(es)"
        assert any(word in mensaje.lower() for word in ["inválid", "incorrec", "credencial"])


@pytest.mark.integration
@pytest.mark.slow
class TestDeviceIntegrationBasic:
    """Tests de integración básicos para dispositivos."""
    
    def setup_method(self):
        """Setup: Preparar servicio con BD real."""
        self.device_service = DeviceService()
    
    def test_listar_dispositivos_bd_real(self):
        """
        Test de integración: Listar dispositivos desde BD real.
        
        Este test valida que:
        - DeviceService se conecta a DeviceDAO
        - DeviceDAO consulta la BD real
        - Se construyen objetos Device correctamente
        """
        dispositivos = self.device_service.listar_dispositivos()
        
        # Verificar que retorna una lista
        assert isinstance(dispositivos, list)
        
        # Si hay dispositivos en la BD, verificar estructura
        if len(dispositivos) > 0:
            primer_dispositivo = dispositivos[0]
            assert hasattr(primer_dispositivo, 'id')
            assert hasattr(primer_dispositivo, 'name')
            assert hasattr(primer_dispositivo, 'state')
            assert hasattr(primer_dispositivo, 'device_type')
            assert hasattr(primer_dispositivo, 'location')
            assert hasattr(primer_dispositivo, 'home')
    
    def test_obtener_opciones_configuracion_bd_real(self):
        """Test: Obtener opciones de configuración desde BD real."""
        opciones = self.device_service.obtener_opciones_configuracion()
        
        # Verificar estructura
        assert 'hogares' in opciones
        assert 'tipos' in opciones
        assert 'ubicaciones' in opciones
        assert 'estados' in opciones
        
        # Verificar que retorna listas
        assert isinstance(opciones['hogares'], list)
        assert isinstance(opciones['tipos'], list)
        assert isinstance(opciones['ubicaciones'], list)
        assert isinstance(opciones['estados'], list)


# ============================================
# CÓMO EJECUTAR ESTOS TESTS
# ============================================

"""
Ejecutar SOLO tests de integración:
    pytest tests/test_integration/ -v -m integration

Ejecutar todos MENOS integración:
    pytest tests/ -v -m "not integration"

Ejecutar todo (incluye integración):
    pytest tests/ -v
"""
