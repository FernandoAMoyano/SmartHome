"""Interfaz de usuario por consola."""

from services.auth_service import AuthService
from services.device_service import DeviceService


class ConsoleUI:
    """
    Maneja la interfaz de usuario por consola.

    Responsabilidad: Solo presentación, sin lógica de negocio.
    Toda la lógica de negocio está delegada a los servicios.
    """

    def __init__(self):
        """Inicializa la interfaz de usuario."""
        self.auth_service = AuthService()
        self.device_service = DeviceService()

    # ============================================
    # MÉTODOS DE PRESENTACIÓN (UI)
    # ============================================

    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola."""
        print("\n" * 2)

    def mostrar_menu_principal(self):
        """Muestra el menú principal."""
        print("\n" + "=" * 50)
        print("     SISTEMA SMARTHOME")
        print("=" * 50)
        print("1. Registrar nuevo usuario")
        print("2. Iniciar sesión")
        print("3. Salir")
        print("=" * 50)

    def mostrar_menu_usuario(self, nombre: str):
        """Muestra el menú de usuario estándar."""
        print("\n" + "=" * 50)
        print(f"     USUARIO: {nombre}")
        print("=" * 50)
        print("1. Consultar mis datos personales")
        print("2. Consultar mis dispositivos")
        print("3. Cerrar sesión")
        print("=" * 50)

    def mostrar_menu_admin(self, nombre: str):
        """Muestra el menú de administrador."""
        print("\n" + "=" * 50)
        print(f"     ADMINISTRADOR: {nombre}")
        print("=" * 50)
        print("1. Gestionar dispositivos (CRUD)")
        print("2. Cambiar rol de usuario")
        print("3. Cerrar sesión")
        print("=" * 50)

    def mostrar_menu_crud_dispositivos(self):
        """Muestra el menú CRUD de dispositivos."""
        print("\n--- GESTIÓN DE DISPOSITIVOS ---")
        print("1. Crear dispositivo")
        print("2. Ver dispositivos")
        print("3. Actualizar dispositivo")
        print("4. Eliminar dispositivo")
        print("5. Volver")

    # ============================================
    # FLUJOS DE AUTENTICACIÓN
    # ============================================

    def flujo_registro(self):
        """Maneja el flujo de registro de usuario."""
        print("\n--- REGISTRO DE USUARIO ---")
        email = input("Email: ").strip()
        password = input("Contraseña: ").strip()
        name = input("Nombre completo: ").strip()

        exito, mensaje = self.auth_service.registrar_usuario(email, password, name)
        print(f"{'✓' if exito else '✗'} {mensaje}")

    def flujo_login(self) -> bool:
        """
        Maneja el flujo de inicio de sesión.

        Returns:
            True si el login fue exitoso, False en caso contrario
        """
        print("\n--- INICIO DE SESIÓN ---")
        email = input("Email: ").strip()
        password = input("Contraseña: ").strip()

        exito, mensaje = self.auth_service.iniciar_sesion(email, password)
        print(f"{'✓' if exito else '✗'} {mensaje}")
        return exito

    def flujo_consultar_datos_personales(self):
        """Muestra los datos personales del usuario actual."""
        print("\n--- MIS DATOS PERSONALES ---")
        datos = self.auth_service.obtener_datos_usuario()

        if datos:
            print(f"Email: {datos['email']}")
            print(f"Nombre: {datos['nombre']}")
            print(f"Rol: {datos['rol']}")
        else:
            print("✗ No hay sesión activa")

    def flujo_consultar_dispositivos_usuario(self):
        """Muestra los dispositivos del usuario actual."""
        print("\n--- MIS DISPOSITIVOS ---")

        usuario = self.auth_service.obtener_usuario_actual()
        if not usuario:
            print("✗ No hay sesión activa")
            return

        dispositivos_por_hogar = self.device_service.obtener_dispositivos_usuario(
            usuario.email
        )

        if not dispositivos_por_hogar:
            print("No tienes hogares asociados")
            return

        for hogar, dispositivos in dispositivos_por_hogar.items():
            print(f"\n🏠 Hogar: {hogar}")

            if dispositivos:
                for disp in dispositivos:
                    print(
                        f"  • {disp.name} ({disp.device_type.name}) - {disp.state.name}"
                    )
                    print(f"    📍 Ubicación: {disp.location.name}")
            else:
                print("  No hay dispositivos en este hogar")

    # ============================================
    # FLUJOS DE GESTIÓN DE DISPOSITIVOS (CRUD)
    # ============================================

    def flujo_crear_dispositivo(self):
        """Maneja el flujo de creación de dispositivo."""
        print("\n--- CREAR DISPOSITIVO ---")

        try:
            nombre = input("Nombre del dispositivo: ").strip()

            # Obtener opciones de configuración
            opciones = self.device_service.obtener_opciones_configuracion()

            # Validar que hay opciones disponibles
            if not opciones["hogares"]:
                print("✗ No hay hogares disponibles")
                return

            if not opciones["tipos"]:
                print("✗ No hay tipos de dispositivo disponibles")
                return

            # Mostrar hogares
            print("\n🏠 Hogares disponibles:")
            for h in opciones["hogares"]:
                print(f"  {h.id}. {h.name}")
            home_id = int(input("Seleccione ID del hogar: "))

            # Mostrar tipos
            print("\n📱 Tipos de dispositivo:")
            for t in opciones["tipos"]:
                print(f"  {t.id}. {t.name}")
            type_id = int(input("Seleccione ID del tipo: "))

            # Mostrar ubicaciones
            print("\n📍 Ubicaciones:")
            for u in opciones["ubicaciones"]:
                print(f"  {u.id}. {u.name}")
            loc_id = int(input("Seleccione ID de ubicación: "))

            # Mostrar estados
            print("\n⚡ Estados:")
            for e in opciones["estados"]:
                print(f"  {e.id}. {e.name}")
            state_id = int(input("Seleccione ID del estado: "))

            # Crear dispositivo
            exito, mensaje = self.device_service.crear_dispositivo(
                nombre, home_id, type_id, loc_id, state_id
            )
            print(f"\n{'✓' if exito else '✗'} {mensaje}")

        except ValueError:
            print("✗ Error: Debe ingresar un número válido")
        except Exception as e:
            print(f"✗ Error: {e}")

    def flujo_ver_dispositivos(self):
        """Muestra todos los dispositivos del sistema."""
        print("\n--- LISTA DE DISPOSITIVOS ---")
        dispositivos = self.device_service.listar_dispositivos()

        if not dispositivos:
            print("No hay dispositivos registrados")
            return

        for disp in dispositivos:
            print(f"\n{'=' * 40}")
            print(f"ID: {disp.id}")
            print(f"📱 Nombre: {disp.name}")
            print(f"🔧 Tipo: {disp.device_type.name}")
            print(f"⚡ Estado: {disp.state.name}")
            print(f"📍 Ubicación: {disp.location.name}")
            print(f"🏠 Hogar: {disp.home.name}")

    def flujo_actualizar_dispositivo(self):
        """Maneja el flujo de actualización de dispositivo."""
        print("\n--- ACTUALIZAR DISPOSITIVO ---")

        try:
            device_id = int(input("ID del dispositivo a actualizar: "))
            dispositivo = self.device_service.obtener_dispositivo(device_id)

            if not dispositivo:
                print("✗ Dispositivo no encontrado")
                return

            print(f"\n📱 Dispositivo actual: {dispositivo.name}")
            print(f"   Estado actual: {dispositivo.state.name}")
            print("\n¿Qué desea actualizar?")

            # Actualizar nombre
            nuevo_nombre = input("Nuevo nombre (Enter para mantener): ").strip()

            # Actualizar estado
            print("\n¿Cambiar estado?")
            opciones = self.device_service.obtener_opciones_configuracion()
            print("\n⚡ Estados disponibles:")
            for e in opciones["estados"]:
                print(f"  {e.id}. {e.name}")

            estado_input = input("ID del nuevo estado (Enter para mantener): ").strip()
            nuevo_estado_id = int(estado_input) if estado_input else None

            # Actualizar dispositivo
            if not nuevo_nombre and not nuevo_estado_id:
                print("✗ No se realizaron cambios")
                return

            exito, mensaje = self.device_service.actualizar_dispositivo(
                device_id, nuevo_nombre if nuevo_nombre else None, nuevo_estado_id
            )
            print(f"\n{'✓' if exito else '✗'} {mensaje}")

        except ValueError:
            print("✗ Error: Debe ingresar un número válido")
        except Exception as e:
            print(f"✗ Error: {e}")

    def flujo_eliminar_dispositivo(self):
        """Maneja el flujo de eliminación de dispositivo."""
        print("\n--- ELIMINAR DISPOSITIVO ---")

        try:
            device_id = int(input("ID del dispositivo a eliminar: "))
            dispositivo = self.device_service.obtener_dispositivo(device_id)

            if not dispositivo:
                print("✗ Dispositivo no encontrado")
                return

            # Mostrar información del dispositivo
            print(f"\n📱 Dispositivo: {dispositivo.name}")
            print(f"   Tipo: {dispositivo.device_type.name}")
            print(f"   Hogar: {dispositivo.home.name}")

            # Confirmar eliminación
            confirmar = input("\n⚠️  ¿Confirmar eliminación? (s/n): ").strip().lower()

            if confirmar == "s":
                exito, mensaje = self.device_service.eliminar_dispositivo(device_id)
                print(f"\n{'✓' if exito else '✗'} {mensaje}")
            else:
                print("Operación cancelada")

        except ValueError:
            print("✗ Error: Debe ingresar un número válido")
        except Exception as e:
            print(f"✗ Error: {e}")

    # ============================================
    # FLUJOS DE ADMINISTRACIÓN
    # ============================================

    def flujo_cambiar_rol_usuario(self):
        """Maneja el flujo de cambio de rol de usuario."""
        print("\n--- CAMBIAR ROL DE USUARIO ---")

        email = input("Email del usuario: ").strip()

        # Obtener roles disponibles
        roles = self.auth_service.listar_roles()

        if not roles:
            print("✗ No hay roles disponibles")
            return

        print("\n👥 Roles disponibles:")
        for r in roles:
            print(f"  {r.id}. {r.name}")

        try:
            nuevo_rol_id = int(input("\nSeleccione ID del nuevo rol: "))

            exito, mensaje = self.auth_service.cambiar_rol_usuario(email, nuevo_rol_id)
            print(f"\n{'✓' if exito else '✗'} {mensaje}")

        except ValueError:
            print("✗ Error: Debe ingresar un número válido")
        except Exception as e:
            print(f"✗ Error: {e}")
