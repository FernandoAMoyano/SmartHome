"""
Tests de integración para flujo completo de automatizaciones.

Estos tests validan la integración entre:
- AutomationService
- AutomationDAO
- HomeDAO
- Base de datos real

NO usan mocks - todo es real.
"""

import pytest
from services.automation_service import AutomationService
from conn.db_connection import DatabaseConnection


@pytest.mark.integration
@pytest.mark.slow
class TestAutomationFlowIntegration:
    """Tests de integración para flujo completo de automatizaciones."""
    
    def setup_method(self):
        """Setup: Preparar servicio y limpiar datos de test."""
        self.automation_service = AutomationService()
        self.db = DatabaseConnection()
        self._cleanup_test_automations()
    
    def test_crear_automatizacion_flujo_completo(self):
        """
        Test E2E: Crear automatización con BD real.
        
        Valida:
        - AutomationService.crear_automatizacion()
        - AutomationDAO.insertar()
        - HomeDAO.obtener_por_id()
        """
        # Crear automatización
        exito, mensaje = self.automation_service.crear_automatizacion(
            nombre="Test Integration Automation",
            descripcion="Automatización de prueba de integración",
            home_id=1  # Debe existir en BD
        )
        
        assert exito is True
        assert "exitosamente" in mensaje.lower()
        
        # Verificar que se creó
        automatizaciones = self.automation_service.listar_automatizaciones()
        test_auto = next(
            (a for a in automatizaciones if a.name == "Test Integration Automation"),
            None
        )
        
        assert test_auto is not None
        assert test_auto.description == "Automatización de prueba de integración"
        assert test_auto.home.id == 1
        assert test_auto.active is True  # Por defecto activa
    
    def test_listar_automatizaciones_con_relaciones(self):
        """
        Test: Listar automatizaciones carga relación con Home.
        
        Valida:
        - AutomationDAO.obtener_todos()
        - Carga de relación home
        """
        automatizaciones = self.automation_service.listar_automatizaciones()
        
        assert isinstance(automatizaciones, list)
        
        # Si hay automatizaciones, verificar relaciones
        if len(automatizaciones) > 0:
            auto = automatizaciones[0]
            
            assert auto.home is not None
            assert hasattr(auto.home, 'name')
            assert hasattr(auto, 'active')
    
    def test_actualizar_automatizacion(self):
        """
        Test: Actualizar nombre y descripción de automatización.
        
        Valida:
        - AutomationDAO.obtener_por_id()
        - AutomationDAO.modificar()
        """
        # Crear automatización
        exito, _ = self.automation_service.crear_automatizacion(
            nombre="Auto To Update",
            descripcion="Descripción original",
            home_id=1
        )
        assert exito is True
        
        # Obtener ID
        automatizaciones = self.automation_service.listar_automatizaciones()
        auto = next(
            (a for a in automatizaciones if a.name == "Auto To Update"),
            None
        )
        assert auto is not None
        auto_id = auto.id
        
        # Actualizar
        exito, mensaje = self.automation_service.actualizar_automatizacion(
            automation_id=auto_id,
            nuevo_nombre="Auto Updated",
            nueva_descripcion="Descripción actualizada"
        )
        
        assert exito is True
        
        # Verificar cambios
        auto_actualizada = self.automation_service.obtener_automatizacion(auto_id)
        assert auto_actualizada is not None
        assert auto_actualizada.name == "Auto Updated"
        assert auto_actualizada.description == "Descripción actualizada"
    
    def test_activar_y_desactivar_automatizacion(self):
        """
        Test: Cambiar estado de activación de automatización.
        
        Valida:
        - AutomationDAO.cambiar_estado()
        - AutomationDAO.obtener_por_id()
        """
        # Crear automatización (inactiva por defecto)
        exito, _ = self.automation_service.crear_automatizacion(
            nombre="Auto State Test",
            descripcion="Test de estados",
            home_id=1
        )
        assert exito is True
        
        # Obtener ID
        automatizaciones = self.automation_service.listar_automatizaciones()
        auto = next(
            (a for a in automatizaciones if a.name == "Auto State Test"),
            None
        )
        assert auto is not None
        auto_id = auto.id
        
        # Verificar que está activa por defecto
        assert auto.active is True
        
        # Desactivar primero (ya que está activa)
        exito, _ = self.automation_service.desactivar_automatizacion(auto_id)
        assert exito is True
        
        # Verificar segunda desactivación
        auto_final = self.automation_service.obtener_automatizacion(auto_id)
        assert auto_final.active is False
        
        # Activar nuevamente
        exito, _ = self.automation_service.activar_automatizacion(auto_id)
        assert exito is True
        
        # Verificar activación
        auto_activada = self.automation_service.obtener_automatizacion(auto_id)
        assert auto_activada.active is True
        
        # Desactivar nuevamente
        exito, _ = self.automation_service.desactivar_automatizacion(auto_id)
        assert exito is True
        
        # Verificar desactivación
        auto_desactivada = self.automation_service.obtener_automatizacion(auto_id)
        assert auto_desactivada.active is False
    
    def test_eliminar_automatizacion(self):
        """
        Test: Eliminar automatización de BD.
        
        Valida:
        - AutomationDAO.eliminar()
        """
        # Crear automatización
        exito, _ = self.automation_service.crear_automatizacion(
            nombre="Auto To Delete",
            descripcion="Para eliminar",
            home_id=1
        )
        assert exito is True
        
        # Obtener ID
        automatizaciones = self.automation_service.listar_automatizaciones()
        auto = next(
            (a for a in automatizaciones if a.name == "Auto To Delete"),
            None
        )
        assert auto is not None
        auto_id = auto.id
        
        # Eliminar
        exito, mensaje = self.automation_service.eliminar_automatizacion(auto_id)
        
        assert exito is True
        assert "eliminada" in mensaje.lower()
        
        # Verificar eliminación
        auto_eliminada = self.automation_service.obtener_automatizacion(auto_id)
        assert auto_eliminada is None
    
    def test_obtener_automatizaciones_por_hogar(self):
        """
        Test: Filtrar automatizaciones por hogar.
        
        Valida:
        - AutomationDAO.obtener_por_hogar()
        """
        # Crear automatización en hogar 1
        exito, _ = self.automation_service.crear_automatizacion(
            nombre="Auto Home 1",
            descripcion="Del hogar 1",
            home_id=1
        )
        assert exito is True
        
        # Obtener automatizaciones del hogar 1
        autos_home1 = self.automation_service.obtener_automatizaciones_hogar(1)
        
        assert isinstance(autos_home1, list)
        
        # Verificar que todas son del hogar 1
        for auto in autos_home1:
            assert auto.home.id == 1
    
    def _cleanup_test_automations(self):
        """Limpiar automatizaciones de test de la BD."""
        cursor = self.db.get_cursor()
        cursor.execute("""
            DELETE FROM automation 
            WHERE name LIKE '%Test Integration%'
               OR name LIKE '%Auto To%'
               OR name LIKE '%Auto State%'
               OR name LIKE '%Auto Home%'
        """)
        self.db.commit()
        cursor.close()
    
    def teardown_method(self):
        """Cleanup: Limpiar después de cada test."""
        self._cleanup_test_automations()
