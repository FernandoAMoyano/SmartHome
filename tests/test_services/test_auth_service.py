"""
Tests para AuthService (Servicio de Autenticación)

Cubre:
- Registro de usuarios
- Inicio de sesión
- Cierre de sesión
- Cambio de roles
- Validaciones
"""


class TestAuthServiceRegistro:
    """Tests para registro de usuarios"""

    def test_registrar_usuario_exitoso(
        self, mock_auth_service, mock_user_dao, mock_role_dao, role_standard
    ):
        """Test: Registrar usuario nuevo con datos válidos"""
        # Arrange
        mock_user_dao.obtener_por_email.return_value = None  # Email no existe
        mock_role_dao.obtener_por_id.return_value = role_standard
        mock_user_dao.insertar.return_value = True

        # Act
        exito, mensaje = mock_auth_service.registrar_usuario(
            "nuevo@test.com", "password123", "Nuevo Usuario"
        )

        # Assert
        assert exito is True
        assert "exitosamente" in mensaje.lower()
        mock_user_dao.insertar.assert_called_once()

    def test_registrar_usuario_email_duplicado(
        self, mock_auth_service, mock_user_dao, usuario_standard
    ):
        """Test: Intentar registrar email que ya existe"""
        # Arrange
        mock_user_dao.obtener_por_email.return_value = usuario_standard

        # Act
        exito, mensaje = mock_auth_service.registrar_usuario(
            "user@test.com", "password123", "Usuario"
        )

        # Assert
        assert exito is False
        assert "ya está registrado" in mensaje.lower()
        mock_user_dao.insertar.assert_not_called()

    def test_registrar_usuario_email_vacio(self, mock_auth_service, mock_user_dao):
        """Test: Validación de email vacío"""
        # Arrange
        mock_user_dao.obtener_por_email.return_value = None

        # Act
        exito, mensaje = mock_auth_service.registrar_usuario(
            "", "password123", "Usuario"
        )

        # Assert
        assert exito is False
        assert "obligatorios" in mensaje.lower()

    def test_registrar_usuario_password_vacio(self, mock_auth_service, mock_user_dao):
        """Test: Validación de password vacío"""
        # Arrange
        mock_user_dao.obtener_por_email.return_value = None

        # Act
        exito, mensaje = mock_auth_service.registrar_usuario(
            "test@test.com", "", "Usuario"
        )

        # Assert
        assert exito is False
        assert "obligatorios" in mensaje.lower()

    def test_registrar_usuario_nombre_vacio(self, mock_auth_service, mock_user_dao):
        """Test: Validación de nombre vacío"""
        # Arrange
        mock_user_dao.obtener_por_email.return_value = None

        # Act
        exito, mensaje = mock_auth_service.registrar_usuario(
            "test@test.com", "password123", ""
        )

        # Assert
        assert exito is False
        assert "obligatorios" in mensaje.lower()

    def test_registrar_usuario_rol_no_encontrado(
        self, mock_auth_service, mock_user_dao, mock_role_dao
    ):
        """Test: Error cuando rol estándar no existe"""
        # Arrange
        mock_user_dao.obtener_por_email.return_value = None
        mock_role_dao.obtener_por_id.return_value = None  # Rol no existe

        # Act
        exito, mensaje = mock_auth_service.registrar_usuario(
            "test@test.com", "password123", "Usuario"
        )

        # Assert
        assert exito is False
        assert "rol" in mensaje.lower()

    def test_registrar_usuario_error_insercion(
        self, mock_auth_service, mock_user_dao, mock_role_dao, role_standard
    ):
        """Test: Error en la inserción a BD"""
        # Arrange
        mock_user_dao.obtener_por_email.return_value = None
        mock_role_dao.obtener_por_id.return_value = role_standard
        mock_user_dao.insertar.return_value = False  # Fallo en BD

        # Act
        exito, mensaje = mock_auth_service.registrar_usuario(
            "test@test.com", "password123", "Usuario"
        )

        # Assert
        assert exito is False
        assert "error" in mensaje.lower()


class TestAuthServiceLogin:
    """Tests para inicio de sesión"""

    def test_login_exitoso(self, mock_auth_service, mock_user_dao, usuario_standard):
        """Test: Login con credenciales correctas"""
        # Arrange
        mock_user_dao.validar_credenciales.return_value = usuario_standard

        # Act
        exito, mensaje = mock_auth_service.iniciar_sesion("user@test.com", "user123")

        # Assert
        assert exito is True
        assert "bienvenido" in mensaje.lower()
        assert mock_auth_service.usuario_actual == usuario_standard

    def test_login_credenciales_invalidas(self, mock_auth_service, mock_user_dao):
        """Test: Login con credenciales incorrectas"""
        # Arrange
        mock_user_dao.validar_credenciales.return_value = None

        # Act
        exito, mensaje = mock_auth_service.iniciar_sesion(
            "user@test.com", "password_incorrecta"
        )

        # Assert
        assert exito is False
        assert "inválidas" in mensaje.lower()
        assert mock_auth_service.usuario_actual is None

    def test_login_email_vacio(self, mock_auth_service):
        """Test: Validación de email vacío en login"""
        # Act
        exito, mensaje = mock_auth_service.iniciar_sesion("", "password123")

        # Assert
        assert exito is False
        assert "obligatorios" in mensaje.lower()

    def test_login_password_vacio(self, mock_auth_service):
        """Test: Validación de password vacío en login"""
        # Act
        exito, mensaje = mock_auth_service.iniciar_sesion("test@test.com", "")

        # Assert
        assert exito is False
        assert "obligatorios" in mensaje.lower()


class TestAuthServiceSesion:
    """Tests para gestión de sesión"""

    def test_cerrar_sesion(self, mock_auth_service, usuario_standard):
        """Test: Cerrar sesión activa"""
        # Arrange
        mock_auth_service.usuario_actual = usuario_standard

        # Act
        mock_auth_service.cerrar_sesion()

        # Assert
        assert mock_auth_service.usuario_actual is None

    def test_obtener_usuario_actual_con_sesion(
        self, mock_auth_service, usuario_standard
    ):
        """Test: Obtener usuario cuando hay sesión activa"""
        # Arrange
        mock_auth_service.usuario_actual = usuario_standard

        # Act
        usuario = mock_auth_service.obtener_usuario_actual()

        # Assert
        assert usuario == usuario_standard

    def test_obtener_usuario_actual_sin_sesion(self, mock_auth_service):
        """Test: Obtener usuario cuando NO hay sesión"""
        # Arrange
        mock_auth_service.usuario_actual = None

        # Act
        usuario = mock_auth_service.obtener_usuario_actual()

        # Assert
        assert usuario is None

    def test_es_admin_usuario_admin(self, mock_auth_service, usuario_admin):
        """Test: Verificar que usuario admin es detectado"""
        # Arrange
        mock_auth_service.usuario_actual = usuario_admin

        # Act
        es_admin = mock_auth_service.es_admin()

        # Assert
        assert es_admin is True

    def test_es_admin_usuario_standard(self, mock_auth_service, usuario_standard):
        """Test: Verificar que usuario standard NO es admin"""
        # Arrange
        mock_auth_service.usuario_actual = usuario_standard

        # Act
        es_admin = mock_auth_service.es_admin()

        # Assert
        assert es_admin is False

    def test_es_admin_sin_sesion(self, mock_auth_service):
        """Test: es_admin sin sesión activa"""
        # Arrange
        mock_auth_service.usuario_actual = None

        # Act
        es_admin = mock_auth_service.es_admin()

        # Assert
        # Cuando no hay usuario, es_admin() retorna False (no None)
        assert es_admin in [False, None]
        assert not es_admin

    def test_obtener_datos_usuario_con_sesion(
        self, mock_auth_service, usuario_standard
    ):
        """Test: Obtener datos de usuario con sesión activa"""
        # Arrange
        mock_auth_service.usuario_actual = usuario_standard

        # Act
        datos = mock_auth_service.obtener_datos_usuario()

        # Assert
        assert datos["email"] == "user@test.com"
        assert datos["nombre"] == "User Test"
        assert datos["rol"] == "standard"

    def test_obtener_datos_usuario_sin_sesion(self, mock_auth_service):
        """Test: Obtener datos sin sesión activa"""
        # Arrange
        mock_auth_service.usuario_actual = None

        # Act
        datos = mock_auth_service.obtener_datos_usuario()

        # Assert
        assert datos == {}


class TestAuthServiceCambioRol:
    """Tests para cambio de rol de usuarios"""

    def test_cambiar_rol_exitoso(
        self,
        mock_auth_service,
        mock_user_dao,
        mock_role_dao,
        usuario_standard,
        role_admin,
    ):
        """Test: Cambiar rol de usuario exitosamente"""
        # Arrange
        mock_user_dao.obtener_por_email.return_value = usuario_standard
        mock_role_dao.obtener_por_id.return_value = role_admin
        mock_user_dao.cambiar_rol.return_value = True

        # Act
        exito, mensaje = mock_auth_service.cambiar_rol_usuario(
            "user@test.com",
            1,  # ID rol admin
        )

        # Assert
        assert exito is True
        assert "exitosamente" in mensaje.lower()
        mock_user_dao.cambiar_rol.assert_called_once_with("user@test.com", 1)

    def test_cambiar_rol_usuario_no_encontrado(self, mock_auth_service, mock_user_dao):
        """Test: Intentar cambiar rol de usuario inexistente"""
        # Arrange
        mock_user_dao.obtener_por_email.return_value = None

        # Act
        exito, mensaje = mock_auth_service.cambiar_rol_usuario("noexiste@test.com", 1)

        # Assert
        assert exito is False
        assert "no encontrado" in mensaje.lower()

    def test_cambiar_rol_rol_invalido(
        self, mock_auth_service, mock_user_dao, mock_role_dao, usuario_standard
    ):
        """Test: Intentar cambiar a un rol que no existe"""
        # Arrange
        mock_user_dao.obtener_por_email.return_value = usuario_standard
        mock_role_dao.obtener_por_id.return_value = None

        # Act
        exito, mensaje = mock_auth_service.cambiar_rol_usuario(
            "user@test.com",
            999,  # Rol inexistente
        )

        # Assert
        assert exito is False
        assert "inválido" in mensaje.lower()

    def test_cambiar_rol_error_bd(
        self,
        mock_auth_service,
        mock_user_dao,
        mock_role_dao,
        usuario_standard,
        role_admin,
    ):
        """Test: Error al cambiar rol en BD"""
        # Arrange
        mock_user_dao.obtener_por_email.return_value = usuario_standard
        mock_role_dao.obtener_por_id.return_value = role_admin
        mock_user_dao.cambiar_rol.return_value = False

        # Act
        exito, mensaje = mock_auth_service.cambiar_rol_usuario("user@test.com", 1)

        # Assert
        assert exito is False
        assert "error" in mensaje.lower()


class TestAuthServiceListarRoles:
    """Tests para listar roles disponibles"""

    def test_listar_roles_exitoso(
        self, mock_auth_service, mock_role_dao, role_admin, role_standard
    ):
        """Test: Obtener lista de roles"""
        # Arrange
        mock_role_dao.obtener_todos.return_value = [role_admin, role_standard]

        # Act
        roles = mock_auth_service.listar_roles()

        # Assert
        assert len(roles) == 2
        assert role_admin in roles
        assert role_standard in roles

    def test_listar_roles_vacio(self, mock_auth_service, mock_role_dao):
        """Test: Listar roles cuando no hay ninguno"""
        # Arrange
        mock_role_dao.obtener_todos.return_value = []

        # Act
        roles = mock_auth_service.listar_roles()

        # Assert
        assert roles == []
