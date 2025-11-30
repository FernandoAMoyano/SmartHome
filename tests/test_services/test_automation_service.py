"""
Tests para AutomationService (Servicio de Automatizaciones)

Cubre:
- Creación de automatizaciones
- Listado de automatizaciones
- Actualización de automatizaciones
- Eliminación de automatizaciones
- Activación/Desactivación
- Obtención por hogar
"""

import pytest
from unittest.mock import Mock
from services.automation_service import AutomationService
from dominio.automation import Automation
from dominio.home import Home


class TestAutomationServiceCrear:
    """Tests para creación de automatizaciones"""
    
    def test_crear_automatizacion_exitosa(self, mock_automation_service,
                                          mock_automation_dao, mock_home_dao,
                                          home_test):
        """Test: Crear automatización con datos válidos"""
        # Arrange
        mock_home_dao.obtener_por_id.return_value = home_test
        mock_automation_dao.insertar.return_value = True
        
        # Act
        exito, mensaje = mock_automation_service.crear_automatizacion(
            nombre="Modo Nocturno",
            descripcion="Apaga todas las luces",
            home_id=1,
            activar=True
        )
        
        # Assert
        assert exito is True
        assert "exitosamente" in mensaje.lower()
        mock_automation_dao.insertar.assert_called_once()
    
    def test_crear_automatizacion_nombre_vacio(self, mock_automation_service,
                                               mock_home_dao):
        """Test: Validación de nombre vacío"""
        # Arrange
        mock_home_dao.obtener_por_id.return_value = None
        
        # Act
        exito, mensaje = mock_automation_service.crear_automatizacion(
            nombre="",
            descripcion="Test",
            home_id=1
        )
        
        # Assert
        assert exito is False
        assert "nombre" in mensaje.lower()
    
    def test_crear_automatizacion_descripcion_vacia(self, mock_automation_service,
                                                    mock_home_dao):
        """Test: Validación de descripción vacía"""
        # Arrange
        mock_home_dao.obtener_por_id.return_value = None
        
        # Act
        exito, mensaje = mock_automation_service.crear_automatizacion(
            nombre="Test",
            descripcion="",
            home_id=1
        )
        
        # Assert
        assert exito is False
        assert "descripción" in mensaje.lower()
    
    def test_crear_automatizacion_hogar_no_encontrado(self, mock_automation_service,
                                                      mock_home_dao):
        """Test: Error cuando hogar no existe"""
        # Arrange
        mock_home_dao.obtener_por_id.return_value = None
        
        # Act
        exito, mensaje = mock_automation_service.crear_automatizacion(
            nombre="Test",
            descripcion="Test description",
            home_id=999
        )
        
        # Assert
        assert exito is False
        assert "hogar" in mensaje.lower() and "no encontrado" in mensaje.lower()
    
    def test_crear_automatizacion_error_insercion(self, mock_automation_service,
                                                  mock_automation_dao, mock_home_dao,
                                                  home_test):
        """Test: Error en la inserción a BD"""
        # Arrange
        mock_home_dao.obtener_por_id.return_value = home_test
        mock_automation_dao.insertar.return_value = False
        
        # Act
        exito, mensaje = mock_automation_service.crear_automatizacion(
            nombre="Test",
            descripcion="Test description",
            home_id=1
        )
        
        # Assert
        assert exito is False
        assert "error" in mensaje.lower()
    
    def test_crear_automatizacion_inactiva_por_defecto(self, mock_automation_service,
                                                       mock_automation_dao, mock_home_dao,
                                                       home_test):
        """Test: Crear automatización inactiva por defecto"""
        # Arrange
        mock_home_dao.obtener_por_id.return_value = home_test
        mock_automation_dao.insertar.return_value = True
        
        # Act
        exito, mensaje = mock_automation_service.crear_automatizacion(
            nombre="Test",
            descripcion="Test description",
            home_id=1,
            activar=False
        )
        
        # Assert
        assert exito is True
        assert "exitosamente" in mensaje.lower()


class TestAutomationServiceListar:
    """Tests para listado de automatizaciones"""
    
    def test_listar_todas_las_automatizaciones(self, mock_automation_service,
                                               mock_automation_dao,
                                               automatizacion_test):
        """Test: Obtener lista de todas las automatizaciones"""
        # Arrange
        mock_automation_dao.obtener_todos.return_value = [automatizacion_test]
        
        # Act
        automatizaciones = mock_automation_service.listar_automatizaciones()
        
        # Assert
        assert len(automatizaciones) == 1
        assert automatizaciones[0].name == "Modo Nocturno"
    
    def test_listar_automatizaciones_vacio(self, mock_automation_service,
                                          mock_automation_dao):
        """Test: Listar cuando no hay automatizaciones"""
        # Arrange
        mock_automation_dao.obtener_todos.return_value = []
        
        # Act
        automatizaciones = mock_automation_service.listar_automatizaciones()
        
        # Assert
        assert automatizaciones == []
    
    def test_obtener_automatizacion_por_id(self, mock_automation_service,
                                           mock_automation_dao,
                                           automatizacion_test):
        """Test: Obtener automatización específica por ID"""
        # Arrange
        mock_automation_dao.obtener_por_id.return_value = automatizacion_test
        
        # Act
        automatizacion = mock_automation_service.obtener_automatizacion(1)
        
        # Assert
        assert automatizacion is not None
        assert automatizacion.id == 1
        assert automatizacion.name == "Modo Nocturno"
    
    def test_obtener_automatizacion_no_encontrada(self, mock_automation_service,
                                                  mock_automation_dao):
        """Test: Buscar automatización que no existe"""
        # Arrange
        mock_automation_dao.obtener_por_id.return_value = None
        
        # Act
        automatizacion = mock_automation_service.obtener_automatizacion(999)
        
        # Assert
        assert automatizacion is None
    
    def test_obtener_automatizaciones_por_hogar(self, mock_automation_service,
                                                mock_automation_dao,
                                                automatizacion_test):
        """Test: Obtener automatizaciones de un hogar"""
        # Arrange
        mock_automation_dao.obtener_por_hogar.return_value = [automatizacion_test]
        
        # Act
        automatizaciones = mock_automation_service.obtener_automatizaciones_hogar(1)
        
        # Assert
        assert len(automatizaciones) == 1
        assert automatizaciones[0].home.id == 1
    
    def test_obtener_automatizaciones_activas(self, mock_automation_service,
                                              mock_automation_dao,
                                              automatizacion_test):
        """Test: Obtener solo automatizaciones activas"""
        # Arrange
        mock_automation_dao.obtener_activas.return_value = [automatizacion_test]
        
        # Act
        automatizaciones = mock_automation_service.obtener_automatizaciones_activas(1)
        
        # Assert
        assert len(automatizaciones) == 1
        assert automatizaciones[0].active is True
    
    def test_obtener_automatizaciones_usuario(self, mock_automation_service,
                                              mock_home_dao, mock_automation_dao,
                                              home_test, automatizacion_test):
        """Test: Obtener automatizaciones organizadas por hogar"""
        # Arrange
        mock_home_dao.obtener_hogares_usuario.return_value = [home_test]
        mock_automation_dao.obtener_por_hogar.return_value = [automatizacion_test]
        
        # Act
        resultado = mock_automation_service.obtener_automatizaciones_usuario("user@test.com")
        
        # Assert
        assert "Casa Test" in resultado
        assert len(resultado["Casa Test"]) == 1


class TestAutomationServiceActualizar:
    """Tests para actualización de automatizaciones"""
    
    def test_actualizar_nombre_exitoso(self, mock_automation_service,
                                       mock_automation_dao, automatizacion_test):
        """Test: Actualizar nombre de automatización"""
        # Arrange
        mock_automation_dao.obtener_por_id.return_value = automatizacion_test
        mock_automation_dao.modificar.return_value = True
        
        # Act
        exito, mensaje = mock_automation_service.actualizar_automatizacion(
            automation_id=1,
            nuevo_nombre="Modo Nocturno Mejorado"
        )
        
        # Assert
        assert exito is True
        assert "exitosamente" in mensaje.lower()
    
    def test_actualizar_descripcion_exitoso(self, mock_automation_service,
                                           mock_automation_dao, automatizacion_test):
        """Test: Actualizar descripción de automatización"""
        # Arrange
        mock_automation_dao.obtener_por_id.return_value = automatizacion_test
        mock_automation_dao.modificar.return_value = True
        
        # Act
        exito, mensaje = mock_automation_service.actualizar_automatizacion(
            automation_id=1,
            nueva_descripcion="Nueva descripción"
        )
        
        # Assert
        assert exito is True
        assert "exitosamente" in mensaje.lower()
    
    def test_actualizar_nombre_y_descripcion(self, mock_automation_service,
                                            mock_automation_dao, automatizacion_test):
        """Test: Actualizar ambos campos simultáneamente"""
        # Arrange
        mock_automation_dao.obtener_por_id.return_value = automatizacion_test
        mock_automation_dao.modificar.return_value = True
        
        # Act
        exito, mensaje = mock_automation_service.actualizar_automatizacion(
            automation_id=1,
            nuevo_nombre="Nuevo nombre",
            nueva_descripcion="Nueva descripción"
        )
        
        # Assert
        assert exito is True
        assert "exitosamente" in mensaje.lower()
    
    def test_actualizar_automatizacion_no_encontrada(self, mock_automation_service,
                                                     mock_automation_dao):
        """Test: Intentar actualizar automatización inexistente"""
        # Arrange
        mock_automation_dao.obtener_por_id.return_value = None
        
        # Act
        exito, mensaje = mock_automation_service.actualizar_automatizacion(
            automation_id=999,
            nuevo_nombre="Test"
        )
        
        # Assert
        assert exito is False
        assert "no encontrada" in mensaje.lower()
    
    def test_actualizar_sin_cambios(self, mock_automation_service,
                                    mock_automation_dao, automatizacion_test):
        """Test: Intentar actualizar sin proporcionar cambios"""
        # Arrange
        mock_automation_dao.obtener_por_id.return_value = automatizacion_test
        
        # Act
        exito, mensaje = mock_automation_service.actualizar_automatizacion(
            automation_id=1
        )
        
        # Assert
        assert exito is False
        assert "no hay cambios" in mensaje.lower() or "al menos un campo" in mensaje.lower()
    
    def test_actualizar_error_modificacion(self, mock_automation_service,
                                          mock_automation_dao, automatizacion_test):
        """Test: Error al modificar en BD"""
        # Arrange
        mock_automation_dao.obtener_por_id.return_value = automatizacion_test
        mock_automation_dao.modificar.return_value = False
        
        # Act
        exito, mensaje = mock_automation_service.actualizar_automatizacion(
            automation_id=1,
            nuevo_nombre="Test"
        )
        
        # Assert
        assert exito is False
        assert "error" in mensaje.lower()


class TestAutomationServiceEliminar:
    """Tests para eliminación de automatizaciones"""
    
    def test_eliminar_automatizacion_exitosa(self, mock_automation_service,
                                             mock_automation_dao, automatizacion_test):
        """Test: Eliminar automatización correctamente"""
        # Arrange
        mock_automation_dao.obtener_por_id.return_value = automatizacion_test
        mock_automation_dao.eliminar.return_value = True
        
        # Act
        exito, mensaje = mock_automation_service.eliminar_automatizacion(1)
        
        # Assert
        assert exito is True
        assert "eliminada" in mensaje.lower()
        mock_automation_dao.eliminar.assert_called_once_with(1)
    
    def test_eliminar_automatizacion_no_encontrada(self, mock_automation_service,
                                                   mock_automation_dao):
        """Test: Intentar eliminar automatización inexistente"""
        # Arrange
        mock_automation_dao.obtener_por_id.return_value = None
        
        # Act
        exito, mensaje = mock_automation_service.eliminar_automatizacion(999)
        
        # Assert
        assert exito is False
        assert "no encontrada" in mensaje.lower()
        mock_automation_dao.eliminar.assert_not_called()
    
    def test_eliminar_automatizacion_error_bd(self, mock_automation_service,
                                              mock_automation_dao, automatizacion_test):
        """Test: Error al eliminar en BD"""
        # Arrange
        mock_automation_dao.obtener_por_id.return_value = automatizacion_test
        mock_automation_dao.eliminar.return_value = False
        
        # Act
        exito, mensaje = mock_automation_service.eliminar_automatizacion(1)
        
        # Assert
        assert exito is False
        assert "error" in mensaje.lower()


class TestAutomationServiceEstado:
    """Tests para activación/desactivación de automatizaciones"""
    
    def test_activar_automatizacion_exitosa(self, mock_automation_service,
                                            mock_automation_dao, automatizacion_test):
        """Test: Activar automatización inactiva"""
        # Arrange
        automatizacion_test.deactivate()  # Asegurar que está inactiva
        mock_automation_dao.obtener_por_id.return_value = automatizacion_test
        mock_automation_dao.cambiar_estado.return_value = True
        
        # Act
        exito, mensaje = mock_automation_service.activar_automatizacion(1)
        
        # Assert
        assert exito is True
        assert "activada" in mensaje.lower()
    
    def test_activar_automatizacion_ya_activa(self, mock_automation_service,
                                              mock_automation_dao, automatizacion_test):
        """Test: Intentar activar automatización ya activa"""
        # Arrange
        automatizacion_test.activate()  # Asegurar que está activa
        mock_automation_dao.obtener_por_id.return_value = automatizacion_test
        
        # Act
        exito, mensaje = mock_automation_service.activar_automatizacion(1)
        
        # Assert
        assert exito is False
        assert "ya está activa" in mensaje.lower()
    
    def test_desactivar_automatizacion_exitosa(self, mock_automation_service,
                                               mock_automation_dao, automatizacion_test):
        """Test: Desactivar automatización activa"""
        # Arrange
        automatizacion_test.activate()  # Asegurar que está activa
        mock_automation_dao.obtener_por_id.return_value = automatizacion_test
        mock_automation_dao.cambiar_estado.return_value = True
        
        # Act
        exito, mensaje = mock_automation_service.desactivar_automatizacion(1)
        
        # Assert
        assert exito is True
        assert "desactivada" in mensaje.lower()
    
    def test_desactivar_automatizacion_ya_inactiva(self, mock_automation_service,
                                                   mock_automation_dao, automatizacion_test):
        """Test: Intentar desactivar automatización ya inactiva"""
        # Arrange
        automatizacion_test.deactivate()  # Asegurar que está inactiva
        mock_automation_dao.obtener_por_id.return_value = automatizacion_test
        
        # Act
        exito, mensaje = mock_automation_service.desactivar_automatizacion(1)
        
        # Assert
        assert exito is False
        assert "ya está inactiva" in mensaje.lower()
    
    def test_activar_automatizacion_no_encontrada(self, mock_automation_service,
                                                  mock_automation_dao):
        """Test: Activar automatización inexistente"""
        # Arrange
        mock_automation_dao.obtener_por_id.return_value = None
        
        # Act
        exito, mensaje = mock_automation_service.activar_automatizacion(999)
        
        # Assert
        assert exito is False
        assert "no encontrada" in mensaje.lower()
    
    def test_cambiar_estado_exitoso(self, mock_automation_service,
                                    mock_automation_dao, automatizacion_test):
        """Test: Cambiar estado genérico"""
        # Arrange
        automatizacion_test.deactivate()  # Comenzar inactiva
        mock_automation_dao.obtener_por_id.return_value = automatizacion_test
        mock_automation_dao.cambiar_estado.return_value = True
        
        # Act
        exito, mensaje = mock_automation_service.cambiar_estado_automatizacion(1, True)
        
        # Assert
        assert exito is True
        assert "exitosamente" in mensaje.lower() or "cambiado" in mensaje.lower()


class TestAutomationServiceResumen:
    """Tests para obtención de resumen de automatizaciones"""
    
    def test_obtener_resumen_automatizaciones(self, mock_automation_service,
                                              mock_automation_dao, automatizacion_test,
                                              home_test):
        """Test: Obtener resumen con estadísticas"""
        # Arrange
        auto_inactiva = Automation(2, "Test Inactiva", "Desc", False, home_test)
        automatizaciones = [automatizacion_test, auto_inactiva]
        mock_automation_dao.obtener_por_hogar.return_value = automatizaciones
        # Mock para obtener_activas (lista filtrada)
        mock_automation_dao.obtener_activas.return_value = [automatizacion_test]
        
        # Act
        resumen = mock_automation_service.obtener_resumen_automatizaciones(1)
        
        # Assert
        assert 'total' in resumen
        assert 'activas' in resumen
        assert 'inactivas' in resumen
        assert resumen['total'] == 2
        assert resumen['activas'] == 1
        assert resumen['inactivas'] == 1
