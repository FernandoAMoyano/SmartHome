"""
Tests para DeviceService (Servicio de Dispositivos)

Cubre:
- Creación de dispositivos
- Listado de dispositivos
- Actualización de dispositivos
- Eliminación de dispositivos
- Búsqueda de dispositivos
- Cambio de estado
- Obtención de opciones de configuración
"""


class TestDeviceServiceCrear:
    """Tests para creación de dispositivos"""

    def test_crear_dispositivo_exitoso(
        self,
        mock_device_service,
        mock_home_dao,
        mock_device_type_dao,
        mock_location_dao,
        mock_state_dao,
        mock_device_dao,
        home_test,
        device_type_luz,
        location_sala,
        state_encendido,
    ):
        """Test: Crear dispositivo con datos válidos"""
        # Arrange
        mock_home_dao.obtener_por_id.return_value = home_test
        mock_device_type_dao.obtener_por_id.return_value = device_type_luz
        mock_location_dao.obtener_por_id.return_value = location_sala
        mock_state_dao.obtener_por_id.return_value = state_encendido
        mock_device_dao.insertar.return_value = True

        # Act
        exito, mensaje = mock_device_service.crear_dispositivo(
            "Luz Cocina", home_id=1, type_id=1, location_id=1, state_id=1
        )

        # Assert
        assert exito is True
        assert "exitosamente" in mensaje.lower()
        mock_device_dao.insertar.assert_called_once()

    def test_crear_dispositivo_nombre_vacio(self, mock_device_service):
        """Test: Validación de nombre vacío"""
        # Act
        exito, mensaje = mock_device_service.crear_dispositivo(
            "", home_id=1, type_id=1, location_id=1, state_id=1
        )

        # Assert
        assert exito is False
        assert "obligatorio" in mensaje.lower()

    def test_crear_dispositivo_nombre_solo_espacios(self, mock_device_service):
        """Test: Validación de nombre con solo espacios"""
        # Act
        exito, mensaje = mock_device_service.crear_dispositivo(
            "   ", home_id=1, type_id=1, location_id=1, state_id=1
        )

        # Assert
        assert exito is False
        assert "obligatorio" in mensaje.lower()

    def test_crear_dispositivo_hogar_no_encontrado(
        self, mock_device_service, mock_home_dao
    ):
        """Test: Error cuando hogar no existe"""
        # Arrange
        mock_home_dao.obtener_por_id.return_value = None

        # Act
        exito, mensaje = mock_device_service.crear_dispositivo(
            "Luz Test", home_id=999, type_id=1, location_id=1, state_id=1
        )

        # Assert
        assert exito is False
        assert "hogar" in mensaje.lower() and "no encontrado" in mensaje.lower()

    def test_crear_dispositivo_tipo_no_encontrado(
        self, mock_device_service, mock_home_dao, mock_device_type_dao, home_test
    ):
        """Test: Error cuando tipo de dispositivo no existe"""
        # Arrange
        mock_home_dao.obtener_por_id.return_value = home_test
        mock_device_type_dao.obtener_por_id.return_value = None

        # Act
        exito, mensaje = mock_device_service.crear_dispositivo(
            "Luz Test", home_id=1, type_id=999, location_id=1, state_id=1
        )

        # Assert
        assert exito is False
        assert "tipo" in mensaje.lower() and "no encontrado" in mensaje.lower()

    def test_crear_dispositivo_ubicacion_no_encontrada(
        self,
        mock_device_service,
        mock_home_dao,
        mock_device_type_dao,
        mock_location_dao,
        home_test,
        device_type_luz,
    ):
        """Test: Error cuando ubicación no existe"""
        # Arrange
        mock_home_dao.obtener_por_id.return_value = home_test
        mock_device_type_dao.obtener_por_id.return_value = device_type_luz
        mock_location_dao.obtener_por_id.return_value = None

        # Act
        exito, mensaje = mock_device_service.crear_dispositivo(
            "Luz Test", home_id=1, type_id=1, location_id=999, state_id=1
        )

        # Assert
        assert exito is False
        assert "ubicación" in mensaje.lower() and "no encontrada" in mensaje.lower()

    def test_crear_dispositivo_estado_no_encontrado(
        self,
        mock_device_service,
        mock_home_dao,
        mock_device_type_dao,
        mock_location_dao,
        mock_state_dao,
        home_test,
        device_type_luz,
        location_sala,
    ):
        """Test: Error cuando estado no existe"""
        # Arrange
        mock_home_dao.obtener_por_id.return_value = home_test
        mock_device_type_dao.obtener_por_id.return_value = device_type_luz
        mock_location_dao.obtener_por_id.return_value = location_sala
        mock_state_dao.obtener_por_id.return_value = None

        # Act
        exito, mensaje = mock_device_service.crear_dispositivo(
            "Luz Test", home_id=1, type_id=1, location_id=1, state_id=999
        )

        # Assert
        assert exito is False
        assert "estado" in mensaje.lower() and "no encontrado" in mensaje.lower()

    def test_crear_dispositivo_error_insercion(
        self,
        mock_device_service,
        mock_home_dao,
        mock_device_type_dao,
        mock_location_dao,
        mock_state_dao,
        mock_device_dao,
        home_test,
        device_type_luz,
        location_sala,
        state_encendido,
    ):
        """Test: Error en la inserción a BD"""
        # Arrange
        mock_home_dao.obtener_por_id.return_value = home_test
        mock_device_type_dao.obtener_por_id.return_value = device_type_luz
        mock_location_dao.obtener_por_id.return_value = location_sala
        mock_state_dao.obtener_por_id.return_value = state_encendido
        mock_device_dao.insertar.return_value = False

        # Act
        exito, mensaje = mock_device_service.crear_dispositivo(
            "Luz Test", home_id=1, type_id=1, location_id=1, state_id=1
        )

        # Assert
        assert exito is False
        assert "error" in mensaje.lower()


class TestDeviceServiceListar:
    """Tests para listado de dispositivos"""

    def test_listar_todos_los_dispositivos(
        self, mock_device_service, mock_device_dao, dispositivo_luz_sala
    ):
        """Test: Obtener lista de todos los dispositivos"""
        # Arrange
        mock_device_dao.obtener_todos.return_value = [dispositivo_luz_sala]

        # Act
        dispositivos = mock_device_service.listar_dispositivos()

        # Assert
        assert len(dispositivos) == 1
        assert dispositivos[0].name == "Luz Sala"

    def test_listar_dispositivos_vacio(self, mock_device_service, mock_device_dao):
        """Test: Listar cuando no hay dispositivos"""
        # Arrange
        mock_device_dao.obtener_todos.return_value = []

        # Act
        dispositivos = mock_device_service.listar_dispositivos()

        # Assert
        assert dispositivos == []

    def test_obtener_dispositivo_por_id(
        self, mock_device_service, mock_device_dao, dispositivo_luz_sala
    ):
        """Test: Obtener dispositivo específico por ID"""
        # Arrange
        mock_device_dao.obtener_por_id.return_value = dispositivo_luz_sala

        # Act
        dispositivo = mock_device_service.obtener_dispositivo(1)

        # Assert
        assert dispositivo is not None
        assert dispositivo.id == 1
        assert dispositivo.name == "Luz Sala"

    def test_obtener_dispositivo_no_encontrado(
        self, mock_device_service, mock_device_dao
    ):
        """Test: Buscar dispositivo que no existe"""
        # Arrange
        mock_device_dao.obtener_por_id.return_value = None

        # Act
        dispositivo = mock_device_service.obtener_dispositivo(999)

        # Assert
        assert dispositivo is None


class TestDeviceServiceActualizar:
    """Tests para actualización de dispositivos"""

    def test_actualizar_nombre_exitoso(
        self, mock_device_service, mock_device_dao, dispositivo_luz_sala
    ):
        """Test: Actualizar nombre de dispositivo"""
        # Arrange
        mock_device_dao.obtener_por_id.return_value = dispositivo_luz_sala
        mock_device_dao.modificar.return_value = True

        # Act
        exito, mensaje = mock_device_service.actualizar_dispositivo(
            device_id=1, nuevo_nombre="Luz Principal Sala"
        )

        # Assert
        assert exito is True
        assert "exitosamente" in mensaje.lower()
        mock_device_dao.modificar.assert_called_once()

    def test_actualizar_estado_exitoso(
        self,
        mock_device_service,
        mock_device_dao,
        mock_state_dao,
        dispositivo_luz_sala,
        state_apagado,
    ):
        """Test: Actualizar estado de dispositivo"""
        # Arrange
        mock_device_dao.obtener_por_id.return_value = dispositivo_luz_sala
        mock_state_dao.obtener_por_id.return_value = state_apagado
        mock_device_dao.modificar.return_value = True

        # Act
        exito, mensaje = mock_device_service.actualizar_dispositivo(
            device_id=1, nuevo_estado_id=2
        )

        # Assert
        assert exito is True
        assert "exitosamente" in mensaje.lower()

    def test_actualizar_nombre_y_estado(
        self,
        mock_device_service,
        mock_device_dao,
        mock_state_dao,
        dispositivo_luz_sala,
        state_apagado,
    ):
        """Test: Actualizar nombre y estado simultáneamente"""
        # Arrange
        mock_device_dao.obtener_por_id.return_value = dispositivo_luz_sala
        mock_state_dao.obtener_por_id.return_value = state_apagado
        mock_device_dao.modificar.return_value = True

        # Act
        exito, mensaje = mock_device_service.actualizar_dispositivo(
            device_id=1, nuevo_nombre="Nueva Luz", nuevo_estado_id=2
        )

        # Assert
        assert exito is True
        assert "exitosamente" in mensaje.lower()

    def test_actualizar_dispositivo_no_encontrado(
        self, mock_device_service, mock_device_dao
    ):
        """Test: Intentar actualizar dispositivo inexistente"""
        # Arrange
        mock_device_dao.obtener_por_id.return_value = None

        # Act
        exito, mensaje = mock_device_service.actualizar_dispositivo(
            device_id=999, nuevo_nombre="Test"
        )

        # Assert
        assert exito is False
        assert "no encontrado" in mensaje.lower()

    def test_actualizar_sin_cambios(
        self, mock_device_service, mock_device_dao, dispositivo_luz_sala
    ):
        """Test: Intentar actualizar sin proporcionar cambios"""
        # Arrange
        mock_device_dao.obtener_por_id.return_value = dispositivo_luz_sala

        # Act
        exito, mensaje = mock_device_service.actualizar_dispositivo(device_id=1)

        # Assert
        assert exito is False
        assert "no hay cambios" in mensaje.lower()

    def test_actualizar_nombre_vacio(
        self, mock_device_service, mock_device_dao, dispositivo_luz_sala
    ):
        """Test: Validación de nombre vacío en actualización"""
        # Arrange
        mock_device_dao.obtener_por_id.return_value = dispositivo_luz_sala

        # Act
        exito, mensaje = mock_device_service.actualizar_dispositivo(
            device_id=1, nuevo_nombre=""
        )

        # Assert
        assert exito is False
        # El servicio puede retornar "vacío" o "no hay cambios" dependiendo de la validación
        assert ("vacío" in mensaje.lower() or "no hay cambios" in mensaje.lower())

    def test_actualizar_estado_invalido(
        self, mock_device_service, mock_device_dao, mock_state_dao, dispositivo_luz_sala
    ):
        """Test: Intentar actualizar con estado inválido"""
        # Arrange
        mock_device_dao.obtener_por_id.return_value = dispositivo_luz_sala
        mock_state_dao.obtener_por_id.return_value = None

        # Act
        exito, mensaje = mock_device_service.actualizar_dispositivo(
            device_id=1, nuevo_estado_id=999
        )

        # Assert
        assert exito is False
        assert "inválido" in mensaje.lower()

    def test_actualizar_error_modificacion(
        self, mock_device_service, mock_device_dao, dispositivo_luz_sala
    ):
        """Test: Error al modificar en BD"""
        # Arrange
        mock_device_dao.obtener_por_id.return_value = dispositivo_luz_sala
        mock_device_dao.modificar.return_value = False

        # Act
        exito, mensaje = mock_device_service.actualizar_dispositivo(
            device_id=1, nuevo_nombre="Nuevo Nombre"
        )

        # Assert
        assert exito is False
        assert "error" in mensaje.lower()


class TestDeviceServiceEliminar:
    """Tests para eliminación de dispositivos"""

    def test_eliminar_dispositivo_exitoso(
        self, mock_device_service, mock_device_dao, dispositivo_luz_sala
    ):
        """Test: Eliminar dispositivo correctamente"""
        # Arrange
        mock_device_dao.obtener_por_id.return_value = dispositivo_luz_sala
        mock_device_dao.eliminar.return_value = True

        # Act
        exito, mensaje = mock_device_service.eliminar_dispositivo(1)

        # Assert
        assert exito is True
        assert "eliminado" in mensaje.lower()
        assert "Luz Sala" in mensaje
        mock_device_dao.eliminar.assert_called_once_with(1)

    def test_eliminar_dispositivo_no_encontrado(
        self, mock_device_service, mock_device_dao
    ):
        """Test: Intentar eliminar dispositivo inexistente"""
        # Arrange
        mock_device_dao.obtener_por_id.return_value = None

        # Act
        exito, mensaje = mock_device_service.eliminar_dispositivo(999)

        # Assert
        assert exito is False
        assert "no encontrado" in mensaje.lower()
        mock_device_dao.eliminar.assert_not_called()

    def test_eliminar_dispositivo_error_bd(
        self, mock_device_service, mock_device_dao, dispositivo_luz_sala
    ):
        """Test: Error al eliminar en BD"""
        # Arrange
        mock_device_dao.obtener_por_id.return_value = dispositivo_luz_sala
        mock_device_dao.eliminar.return_value = False

        # Act
        exito, mensaje = mock_device_service.eliminar_dispositivo(1)

        # Assert
        assert exito is False
        assert "error" in mensaje.lower()


class TestDeviceServiceBuscar:
    """Tests para búsqueda de dispositivos"""

    def test_obtener_dispositivos_por_hogar(
        self, mock_device_service, mock_device_dao, dispositivo_luz_sala
    ):
        """Test: Obtener dispositivos de un hogar específico"""
        # Arrange
        mock_device_dao.obtener_por_hogar.return_value = [dispositivo_luz_sala]

        # Act
        dispositivos = mock_device_service.obtener_dispositivos_por_hogar(1)

        # Assert
        assert len(dispositivos) == 1
        assert dispositivos[0].home.id == 1

    def test_buscar_por_nombre(
        self, mock_device_service, mock_device_dao, dispositivo_luz_sala
    ):
        """Test: Buscar dispositivos por nombre"""
        # Arrange
        mock_device_dao.buscar_por_nombre.return_value = [dispositivo_luz_sala]

        # Act
        dispositivos = mock_device_service.buscar_dispositivos_por_nombre("Luz", 1)

        # Assert
        assert len(dispositivos) == 1
        assert "Luz" in dispositivos[0].name

    def test_buscar_sin_resultados(self, mock_device_service, mock_device_dao):
        """Test: Búsqueda sin resultados"""
        # Arrange
        mock_device_dao.buscar_por_nombre.return_value = []

        # Act
        dispositivos = mock_device_service.buscar_dispositivos_por_nombre(
            "Inexistente", 1
        )

        # Assert
        assert dispositivos == []


class TestDeviceServiceEstado:
    """Tests para cambio de estado de dispositivos"""

    def test_cambiar_estado_exitoso(
        self,
        mock_device_service,
        mock_device_dao,
        mock_state_dao,
        dispositivo_luz_sala,
        state_apagado,
    ):
        """Test: Cambiar estado de dispositivo"""
        # Arrange
        mock_device_dao.obtener_por_id.return_value = dispositivo_luz_sala
        mock_state_dao.obtener_por_id.return_value = state_apagado
        mock_device_dao.cambiar_estado.return_value = True

        # Act
        exito, mensaje = mock_device_service.cambiar_estado_dispositivo(1, 2)

        # Assert
        assert exito is True
        assert "Apagado" in mensaje

    def test_cambiar_estado_dispositivo_no_encontrado(
        self, mock_device_service, mock_device_dao
    ):
        """Test: Cambiar estado de dispositivo inexistente"""
        # Arrange
        mock_device_dao.obtener_por_id.return_value = None

        # Act
        exito, mensaje = mock_device_service.cambiar_estado_dispositivo(999, 2)

        # Assert
        assert exito is False
        assert "no encontrado" in mensaje.lower()

    def test_cambiar_estado_estado_invalido(
        self, mock_device_service, mock_device_dao, mock_state_dao, dispositivo_luz_sala
    ):
        """Test: Cambiar a un estado que no existe"""
        # Arrange
        mock_device_dao.obtener_por_id.return_value = dispositivo_luz_sala
        mock_state_dao.obtener_por_id.return_value = None

        # Act
        exito, mensaje = mock_device_service.cambiar_estado_dispositivo(1, 999)

        # Assert
        assert exito is False
        assert "no encontrado" in mensaje.lower()


class TestDeviceServiceOpciones:
    """Tests para obtención de opciones de configuración"""

    def test_obtener_opciones_configuracion(
        self,
        mock_device_service,
        mock_home_dao,
        mock_device_type_dao,
        mock_location_dao,
        mock_state_dao,
        home_test,
        device_type_luz,
        location_sala,
        state_encendido,
    ):
        """Test: Obtener todas las opciones de configuración"""
        # Arrange
        mock_home_dao.obtener_todos.return_value = [home_test]
        mock_device_type_dao.obtener_todos.return_value = [device_type_luz]
        mock_location_dao.obtener_todos.return_value = [location_sala]
        mock_state_dao.obtener_todos.return_value = [state_encendido]

        # Act
        opciones = mock_device_service.obtener_opciones_configuracion()

        # Assert
        assert "hogares" in opciones
        assert "tipos" in opciones
        assert "ubicaciones" in opciones
        assert "estados" in opciones
        assert len(opciones["hogares"]) == 1
        assert len(opciones["tipos"]) == 1

    def test_obtener_dispositivos_usuario(
        self,
        mock_device_service,
        mock_home_dao,
        mock_device_dao,
        home_test,
        dispositivo_luz_sala,
    ):
        """Test: Obtener dispositivos organizados por hogar para un usuario"""
        # Arrange
        mock_home_dao.obtener_hogares_usuario.return_value = [home_test]
        mock_device_dao.obtener_por_hogar.return_value = [dispositivo_luz_sala]

        # Act
        resultado = mock_device_service.obtener_dispositivos_usuario("user@test.com")

        # Assert
        assert "Casa Test" in resultado
        assert len(resultado["Casa Test"]) == 1
        assert resultado["Casa Test"][0].name == "Luz Sala"
