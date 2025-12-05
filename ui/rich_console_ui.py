"""
Interfaz de usuario mejorada con Rich.

Esta es la nueva UI del sistema SmartHome utilizando la librería Rich
para una experiencia visual profesional y atractiva.
"""

from services.auth_service import AuthService
from services.device_service import DeviceService
from services.automation_service import AutomationService
from ui.rich_utils import (
    console,
    COLORS,
    ICONS,
    clear_screen,
    print_header,
    print_success,
    print_error,
    print_warning,
    print_info,
    ask_input,
    ask_confirm,
    show_loading,
    pause,
    create_menu_panel,
    create_data_table,
    get_state_icon,
    show_welcome_banner,
)
from rich.panel import Panel


class RichConsoleUI:
    """
    Interfaz de usuario mejorada con Rich.

    Características:
    - Menús coloridos y estilizados
    - Tablas formateadas de datos
    - Mensajes de éxito/error con íconos
    - Prompts interactivos
    - Progress bars para operaciones
    """

    def __init__(self):
        """Inicializa la interfaz de usuario."""
        self.auth_service = AuthService()
        self.device_service = DeviceService()
        self.automation_service = AutomationService()

    # ============================================
    # MENÚS PRINCIPALES
    # ============================================

    def mostrar_menu_principal(self):
        """Muestra el menú principal con Rich."""
        clear_screen()
        show_welcome_banner()

        options = [
            ("1", "Registrar nuevo usuario", ICONS["add"]),
            ("2", "Iniciar sesión", ICONS["user"]),
            ("3", "Salir", ICONS["exit"]),
        ]

        menu = create_menu_panel("MENÚ PRINCIPAL", options)
        console.print(menu)

    def mostrar_menu_usuario(self, nombre: str):
        """Muestra el menú de usuario estándar."""
        clear_screen()
        print_header(f"Usuario: {nombre}", "Gestión de tu Hogar Inteligente")

        options = [
            ("1", "Consultar mis datos personales", ICONS["user"]),
            ("2", "Ver mis dispositivos", ICONS["device"]),
            ("3", "Ver mis automatizaciones", ICONS["automation"]),
            ("4", "Cerrar sesión", ICONS["exit"]),
        ]

        menu = create_menu_panel("MENÚ DE USUARIO", options, ICONS["user"])
        console.print(menu)

    def mostrar_menu_admin(self, nombre: str):
        """Muestra el menú de administrador."""
        clear_screen()
        print_header(f"Administrador: {nombre}", "Panel de Control Total")

        options = [
            ("1", "Gestionar Dispositivos (CRUD)", ICONS["device"]),
            ("2", "Gestionar Automatizaciones (CRUD)", ICONS["automation"]),
            ("3", "Cambiar rol de usuario", ICONS["admin"]),
            ("4", "Cerrar sesión", ICONS["exit"]),
        ]

        menu = create_menu_panel("MENÚ DE ADMINISTRADOR", options, ICONS["admin"])
        console.print(menu)

    def mostrar_menu_crud_dispositivos(self):
        """Muestra el menú CRUD de dispositivos."""
        clear_screen()
        print_header("Gestión de Dispositivos", "Crear, Ver, Actualizar, Eliminar")

        options = [
            ("1", "Crear dispositivo", ICONS["add"]),
            ("2", "Ver dispositivos", ICONS["view"]),
            ("3", "Actualizar dispositivo", ICONS["edit"]),
            ("4", "Eliminar dispositivo", ICONS["delete"]),
            ("5", "Volver", ICONS["exit"]),
        ]

        menu = create_menu_panel("CRUD DISPOSITIVOS", options, ICONS["device"])
        console.print(menu)

    def mostrar_menu_crud_automatizaciones(self):
        """Muestra el menú CRUD de automatizaciones."""
        clear_screen()
        print_header("Gestión de Automatizaciones", "Crear, Ver, Actualizar, Eliminar")

        options = [
            ("1", "Crear automatización", ICONS["add"]),
            ("2", "Ver automatizaciones", ICONS["view"]),
            ("3", "Actualizar automatización", ICONS["edit"]),
            ("4", "Activar/Desactivar automatización", ICONS["settings"]),
            ("5", "Eliminar automatización", ICONS["delete"]),
            ("6", "Volver", ICONS["exit"]),
        ]

        menu = create_menu_panel("CRUD AUTOMATIZACIONES", options, ICONS["automation"])
        console.print(menu)

    # ============================================
    # FLUJOS DE AUTENTICACIÓN
    # ============================================

    def flujo_registro(self):
        """Maneja el flujo de registro de usuario."""
        clear_screen()
        print_header("Registro de Nuevo Usuario", "Complete los siguientes datos")

        console.print()
        email = ask_input(f"{ICONS['user']} Email")
        password = ask_input(f"{ICONS['settings']} Contraseña", password=True)
        name = ask_input(f"{ICONS['user']} Nombre completo")

        console.print()
        show_loading("Registrando usuario...", 0.8)

        exito, mensaje = self.auth_service.registrar_usuario(email, password, name)

        console.print()
        if exito:
            print_success(mensaje)
        else:
            print_error(mensaje)

        pause()

    def flujo_login(self) -> bool:
        """
        Maneja el flujo de inicio de sesión.

        Returns:
            True si el login fue exitoso, False en caso contrario
        """
        clear_screen()
        print_header("Inicio de Sesión", "Ingrese sus credenciales")

        console.print()
        email = ask_input(f"{ICONS['user']} Email")
        password = ask_input(f"{ICONS['settings']} Contraseña", password=True)

        console.print()
        show_loading("Verificando credenciales...", 0.8)

        exito, mensaje = self.auth_service.iniciar_sesion(email, password)

        console.print()
        if exito:
            print_success(mensaje)
            pause()
            return True
        else:
            print_error(mensaje)
            pause()
            return False

    def flujo_consultar_datos_personales(self):
        """Muestra los datos personales del usuario actual."""
        clear_screen()
        print_header("Mis Datos Personales", "Información de tu cuenta")

        datos = self.auth_service.obtener_datos_usuario()

        if datos:
            console.print()
            info_panel = Panel(
                f"[cyan]Email:[/cyan] [white]{datos['email']}[/white]\n"
                f"[cyan]Nombre:[/cyan] [white]{datos['nombre']}[/white]\n"
                f"[cyan]Rol:[/cyan] [white]{datos['rol']}[/white]",
                title=f"{ICONS['user']} Información de Usuario",
                border_style=COLORS["info"],
                padding=(1, 2),
            )
            console.print(info_panel)
        else:
            console.print()
            print_error("No hay sesión activa")

        console.print()
        pause()

    # ============================================
    # FLUJOS DE DISPOSITIVOS - CONSULTA
    # ============================================

    def flujo_consultar_dispositivos_usuario(self):
        """Muestra los dispositivos del usuario actual con tabla Rich."""
        clear_screen()
        print_header("Mis Dispositivos", "Dispositivos de tus hogares")

        usuario = self.auth_service.obtener_usuario_actual()
        if not usuario:
            console.print()
            print_error("No hay sesión activa")
            pause()
            return

        dispositivos_por_hogar = self.device_service.obtener_dispositivos_usuario(
            usuario.email
        )

        if not dispositivos_por_hogar:
            console.print()
            print_warning("No tienes hogares asociados")
            pause()
            return

        for hogar, dispositivos in dispositivos_por_hogar.items():
            console.print()
            console.print(f"\n{ICONS['home']} [bold cyan]Hogar: {hogar}[/bold cyan]")

            if dispositivos:
                columns = [
                    ("ID", "cyan", "center"),
                    ("Nombre", "white", "left"),
                    ("Tipo", "yellow", "left"),
                    ("Estado", "white", "center"),
                    ("Ubicación", "blue", "left"),
                ]

                rows = []
                for disp in dispositivos:
                    rows.append(
                        [
                            str(disp.id),
                            disp.name,
                            disp.device_type.name,
                            get_state_icon(disp.state.name),
                            disp.location.name,
                        ]
                    )

                table = create_data_table("", columns, rows)
                console.print(table)
            else:
                print_info("No hay dispositivos en este hogar")

        console.print()
        pause()

    def flujo_ver_dispositivos(self):
        """Muestra todos los dispositivos del sistema en tabla."""
        clear_screen()
        print_header("Lista de Dispositivos", "Todos los dispositivos del sistema")

        show_loading("Cargando dispositivos...", 0.5)
        dispositivos = self.device_service.listar_dispositivos()

        if not dispositivos:
            console.print()
            print_warning("No hay dispositivos registrados")
            pause()
            return

        columns = [
            ("ID", "cyan", "center"),
            ("Nombre", "white", "left"),
            ("Tipo", "yellow", "left"),
            ("Estado", "white", "center"),
            ("Ubicación", "blue", "left"),
            ("Hogar", "magenta", "left"),
        ]

        rows = []
        for disp in dispositivos:
            rows.append(
                [
                    str(disp.id),
                    disp.name,
                    disp.device_type.name,
                    get_state_icon(disp.state.name),
                    disp.location.name,
                    disp.home.name,
                ]
            )

        console.print()
        table = create_data_table(
            f"{ICONS['device']} Dispositivos del Sistema", columns, rows
        )
        console.print(table)

        console.print()
        pause()

    # ============================================
    # FLUJOS DE DISPOSITIVOS - CRUD
    # ============================================

    def flujo_crear_dispositivo(self):
        """Maneja el flujo de creación de dispositivo."""
        clear_screen()
        print_header("Crear Dispositivo", "Agregar nuevo dispositivo al sistema")

        try:
            console.print()
            nombre = ask_input(f"{ICONS['device']} Nombre del dispositivo")

            # Obtener opciones de configuración
            show_loading("Cargando opciones...", 0.5)
            opciones = self.device_service.obtener_opciones_configuracion()

            # Validar que hay opciones disponibles
            if not opciones["hogares"]:
                console.print()
                print_error("No hay hogares disponibles")
                pause()
                return

            if not opciones["tipos"]:
                console.print()
                print_error("No hay tipos de dispositivo disponibles")
                pause()
                return

            # Mostrar hogares en tabla
            console.print()
            console.print(f"\n{ICONS['home']} [bold cyan]Hogares disponibles:[/bold cyan]")
            for h in opciones["hogares"]:
                console.print(f"  [cyan]{h.id}[/cyan]. {h.name}")

            home_id = int(ask_input("\n  Seleccione ID del hogar"))

            # Mostrar tipos en tabla
            console.print()
            console.print(
                f"\n{ICONS['device']} [bold yellow]Tipos de dispositivo:[/bold yellow]"
            )
            for t in opciones["tipos"]:
                console.print(f"  [yellow]{t.id}[/yellow]. {t.name}")

            type_id = int(ask_input("\n  Seleccione ID del tipo"))

            # Mostrar ubicaciones
            console.print()
            console.print(f"\n{ICONS['home']} [bold blue]Ubicaciones:[/bold blue]")
            for u in opciones["ubicaciones"]:
                console.print(f"  [blue]{u.id}[/blue]. {u.name}")

            loc_id = int(ask_input("\n  Seleccione ID de ubicación"))

            # Mostrar estados
            console.print()
            console.print(f"\n{ICONS['settings']} [bold magenta]Estados:[/bold magenta]")
            for e in opciones["estados"]:
                console.print(f"  [magenta]{e.id}[/magenta]. {e.name}")

            state_id = int(ask_input("\n  Seleccione ID del estado"))

            # Crear dispositivo
            console.print()
            show_loading("Creando dispositivo...", 0.8)

            exito, mensaje = self.device_service.crear_dispositivo(
                nombre, home_id, type_id, loc_id, state_id
            )

            console.print()
            if exito:
                print_success(mensaje)
            else:
                print_error(mensaje)

        except ValueError:
            console.print()
            print_error("Error: Debe ingresar un número válido")
        except Exception as e:
            console.print()
            print_error(f"Error: {e}")

        pause()

    def flujo_actualizar_dispositivo(self):
        """Maneja el flujo de actualización de dispositivo."""
        clear_screen()
        print_header("Actualizar Dispositivo", "Modificar dispositivo existente")

        try:
            console.print()
            device_id = int(ask_input(f"{ICONS['device']} ID del dispositivo a actualizar"))

            show_loading("Buscando dispositivo...", 0.5)
            dispositivo = self.device_service.obtener_dispositivo(device_id)

            if not dispositivo:
                console.print()
                print_error("Dispositivo no encontrado")
                pause()
                return

            # Mostrar info actual
            console.print()
            info_panel = Panel(
                f"[cyan]Nombre actual:[/cyan] [white]{dispositivo.name}[/white]\n"
                f"[cyan]Estado actual:[/cyan] {get_state_icon(dispositivo.state.name)}",
                title=f"{ICONS['device']} Dispositivo Actual",
                border_style=COLORS["info"],
                padding=(1, 2),
            )
            console.print(info_panel)

            console.print()
            console.print("[yellow]¿Qué desea actualizar?[/yellow]")

            # Actualizar nombre
            console.print()
            nuevo_nombre = ask_input(
                "Nuevo nombre (presione Enter para mantener)"
            ).strip()

            # Actualizar estado
            console.print()
            opciones = self.device_service.obtener_opciones_configuracion()
            console.print(
                f"\n{ICONS['settings']} [bold magenta]Estados disponibles:[/bold magenta]"
            )
            for e in opciones["estados"]:
                console.print(f"  [magenta]{e.id}[/magenta]. {e.name}")

            estado_input = ask_input(
                "\nID del nuevo estado (presione Enter para mantener)"
            ).strip()
            nuevo_estado_id = int(estado_input) if estado_input else None

            # Validar cambios
            if not nuevo_nombre and not nuevo_estado_id:
                console.print()
                print_warning("No se realizaron cambios")
                pause()
                return

            # Actualizar
            console.print()
            show_loading("Actualizando dispositivo...", 0.8)

            exito, mensaje = self.device_service.actualizar_dispositivo(
                device_id, nuevo_nombre if nuevo_nombre else None, nuevo_estado_id
            )

            console.print()
            if exito:
                print_success(mensaje)
            else:
                print_error(mensaje)

        except ValueError:
            console.print()
            print_error("Error: Debe ingresar un número válido")
        except Exception as e:
            console.print()
            print_error(f"Error: {e}")

        pause()

    def flujo_eliminar_dispositivo(self):
        """Maneja el flujo de eliminación de dispositivo."""
        clear_screen()
        print_header("Eliminar Dispositivo", "Eliminar dispositivo del sistema")

        try:
            console.print()
            device_id = int(ask_input(f"{ICONS['device']} ID del dispositivo a eliminar"))

            show_loading("Buscando dispositivo...", 0.5)
            dispositivo = self.device_service.obtener_dispositivo(device_id)

            if not dispositivo:
                console.print()
                print_error("Dispositivo no encontrado")
                pause()
                return

            # Mostrar información del dispositivo
            console.print()
            info_panel = Panel(
                f"[cyan]Nombre:[/cyan] [white]{dispositivo.name}[/white]\n"
                f"[cyan]Tipo:[/cyan] [yellow]{dispositivo.device_type.name}[/yellow]\n"
                f"[cyan]Hogar:[/cyan] [magenta]{dispositivo.home.name}[/magenta]",
                title=f"{ICONS['warning']} Dispositivo a Eliminar",
                border_style=COLORS["error"],
                padding=(1, 2),
            )
            console.print(info_panel)

            # Confirmar eliminación
            console.print()
            if ask_confirm("¿Confirmar eliminación?"):
                show_loading("Eliminando dispositivo...", 0.8)
                exito, mensaje = self.device_service.eliminar_dispositivo(device_id)

                console.print()
                if exito:
                    print_success(mensaje)
                else:
                    print_error(mensaje)
            else:
                console.print()
                print_info("Operación cancelada")

        except ValueError:
            console.print()
            print_error("Error: Debe ingresar un número válido")
        except Exception as e:
            console.print()
            print_error(f"Error: {e}")

        pause()

    # ============================================
    # FLUJOS DE AUTOMATIZACIONES - CONSULTA
    # ============================================

    def flujo_consultar_automatizaciones_usuario(self):
        """Muestra las automatizaciones del usuario actual."""
        clear_screen()
        print_header("Mis Automatizaciones", "Automatizaciones de tus hogares")

        usuario = self.auth_service.obtener_usuario_actual()
        if not usuario:
            console.print()
            print_error("No hay sesión activa")
            pause()
            return

        show_loading("Cargando automatizaciones...", 0.5)
        automatizaciones_por_hogar = self.automation_service.obtener_automatizaciones_usuario(
            usuario.email
        )

        if not automatizaciones_por_hogar:
            console.print()
            print_warning("No tienes hogares asociados")
            pause()
            return

        # Iterar por cada hogar y sus automatizaciones
        for hogar, automatizaciones in automatizaciones_por_hogar.items():
            console.print()
            console.print(f"\n{ICONS['home']} [bold cyan]Hogar: {hogar}[/bold cyan]")

            if automatizaciones:
                # Crear tabla
                columns = [
                    ("ID", "cyan", "center"),
                    ("Nombre", "white", "left"),
                    ("Descripción", "white", "left"),
                    ("Estado", "white", "center"),
                ]

                rows = []
                for auto in automatizaciones:
                    estado = (
                        f"[{COLORS['success']}]{ICONS['active']}[/{COLORS['success']}] Activa"
                        if auto.active
                        else f"[{COLORS['error']}]{ICONS['inactive']}[/{COLORS['error']}] Inactiva"
                    )
                    rows.append(
                        [
                            str(auto.id),
                            auto.name,
                            auto.description[:50] + "..."
                            if len(auto.description) > 50
                            else auto.description,
                            estado,
                        ]
                    )

                table = create_data_table("", columns, rows)
                console.print(table)
            else:
                print_info("No hay automatizaciones en este hogar")

        console.print()
        pause()

    def flujo_ver_automatizaciones(self):
        """Muestra todas las automatizaciones del sistema."""
        clear_screen()
        print_header(
            "Lista de Automatizaciones", "Todas las automatizaciones del sistema"
        )

        show_loading("Cargando automatizaciones...", 0.5)
        automatizaciones = self.automation_service.listar_automatizaciones()

        if not automatizaciones:
            console.print()
            print_warning("No hay automatizaciones registradas")
            pause()
            return

        # Crear tabla
        columns = [
            ("ID", "cyan", "center"),
            ("Nombre", "white", "left"),
            ("Descripción", "white", "left"),
            ("Estado", "white", "center"),
            ("Hogar", "magenta", "left"),
        ]

        rows = []
        for auto in automatizaciones:
            estado = (
                f"[{COLORS['success']}]{ICONS['active']}[/{COLORS['success']}] Activa"
                if auto.active
                else f"[{COLORS['error']}]{ICONS['inactive']}[/{COLORS['error']}] Inactiva"
            )
            rows.append(
                [
                    str(auto.id),
                    auto.name,
                    auto.description[:50] + "..."
                    if len(auto.description) > 50
                    else auto.description,
                    estado,
                    auto.home.name,
                ]
            )

        console.print()
        table = create_data_table(
            f"{ICONS['automation']} Automatizaciones del Sistema", columns, rows
        )
        console.print(table)

        console.print()
        pause()

    # ============================================
    # FLUJOS DE AUTOMATIZACIONES - CRUD
    # ============================================

    def flujo_crear_automatizacion(self):
        """Maneja el flujo de creación de automatización."""
        clear_screen()
        print_header("Crear Automatización", "Agregar nueva automatización")

        try:
            console.print()
            nombre = ask_input(f"{ICONS['automation']} Nombre de la automatización")
            descripcion = ask_input(f"{ICONS['edit']} Descripción")

            # Obtener hogares
            show_loading("Cargando hogares...", 0.5)
            opciones = self.device_service.obtener_opciones_configuracion()

            if not opciones["hogares"]:
                console.print()
                print_error("No hay hogares disponibles")
                pause()
                return

            # Mostrar hogares
            console.print()
            console.print(f"\n{ICONS['home']} [bold cyan]Hogares disponibles:[/bold cyan]")
            for h in opciones["hogares"]:
                console.print(f"  [cyan]{h.id}[/cyan]. {h.name}")

            home_id = int(ask_input("\n  Seleccione ID del hogar"))

            # Crear automatización
            console.print()
            show_loading("Creando automatización...", 0.8)

            exito, mensaje = self.automation_service.crear_automatizacion(
                nombre, descripcion, home_id
            )

            console.print()
            if exito:
                print_success(mensaje)
            else:
                print_error(mensaje)

        except ValueError:
            console.print()
            print_error("Error: Debe ingresar un número válido")
        except Exception as e:
            console.print()
            print_error(f"Error: {e}")

        pause()

    def flujo_actualizar_automatizacion(self):
        """Maneja el flujo de actualización de automatización."""
        clear_screen()
        print_header("Actualizar Automatización", "Modificar automatización existente")

        try:
            console.print()
            auto_id = int(
                ask_input(f"{ICONS['automation']} ID de la automatización a actualizar")
            )

            show_loading("Buscando automatización...", 0.5)
            automatizacion = self.automation_service.obtener_automatizacion(auto_id)

            if not automatizacion:
                console.print()
                print_error("Automatización no encontrada")
                pause()
                return

            # Mostrar info actual
            console.print()
            info_panel = Panel(
                f"[cyan]Nombre actual:[/cyan] [white]{automatizacion.name}[/white]\n"
                f"[cyan]Descripción:[/cyan] [white]{automatizacion.description}[/white]",
                title=f"{ICONS['automation']} Automatización Actual",
                border_style=COLORS["info"],
                padding=(1, 2),
            )
            console.print(info_panel)

            # Actualizar
            console.print()
            nuevo_nombre = ask_input(
                "Nuevo nombre (presione Enter para mantener)"
            ).strip()
            nueva_descripcion = ask_input(
                "Nueva descripción (presione Enter para mantener)"
            ).strip()

            if not nuevo_nombre and not nueva_descripcion:
                console.print()
                print_warning("No se realizaron cambios")
                pause()
                return

            # Actualizar
            console.print()
            show_loading("Actualizando automatización...", 0.8)

            exito, mensaje = self.automation_service.actualizar_automatizacion(
                auto_id,
                nuevo_nombre if nuevo_nombre else None,
                nueva_descripcion if nueva_descripcion else None,
            )

            console.print()
            if exito:
                print_success(mensaje)
            else:
                print_error(mensaje)

        except ValueError:
            console.print()
            print_error("Error: Debe ingresar un número válido")
        except Exception as e:
            console.print()
            print_error(f"Error: {e}")

        pause()

    def flujo_activar_desactivar_automatizacion(self):
        """Maneja el flujo de activar/desactivar automatización."""
        clear_screen()
        print_header(
            "Activar/Desactivar Automatización", "Cambiar estado de automatización"
        )

        try:
            console.print()
            auto_id = int(
                ask_input(f"{ICONS['automation']} ID de la automatización")
            )

            show_loading("Buscando automatización...", 0.5)
            automatizacion = self.automation_service.obtener_automatizacion(auto_id)

            if not automatizacion:
                console.print()
                print_error("Automatización no encontrada")
                pause()
                return

            # Mostrar info
            estado_actual = "Activa" if automatizacion.active else "Inactiva"
            console.print()
            info_panel = Panel(
                f"[cyan]Nombre:[/cyan] [white]{automatizacion.name}[/white]\n"
                f"[cyan]Estado actual:[/cyan] [white]{estado_actual}[/white]",
                title=f"{ICONS['automation']} Automatización",
                border_style=COLORS["info"],
                padding=(1, 2),
            )
            console.print(info_panel)

            # Preguntar acción
            console.print()
            if automatizacion.active:
                if ask_confirm("¿Desactivar automatización?"):
                    show_loading("Desactivando...", 0.8)
                    exito, mensaje = self.automation_service.desactivar_automatizacion(
                        auto_id
                    )
                else:
                    console.print()
                    print_info("Operación cancelada")
                    pause()
                    return
            else:
                if ask_confirm("¿Activar automatización?"):
                    show_loading("Activando...", 0.8)
                    exito, mensaje = self.automation_service.activar_automatizacion(
                        auto_id
                    )
                else:
                    console.print()
                    print_info("Operación cancelada")
                    pause()
                    return

            console.print()
            if exito:
                print_success(mensaje)
            else:
                print_error(mensaje)

        except ValueError:
            console.print()
            print_error("Error: Debe ingresar un número válido")
        except Exception as e:
            console.print()
            print_error(f"Error: {e}")

        pause()

    def flujo_eliminar_automatizacion(self):
        """Maneja el flujo de eliminación de automatización."""
        clear_screen()
        print_header("Eliminar Automatización", "Eliminar automatización del sistema")

        try:
            console.print()
            auto_id = int(
                ask_input(f"{ICONS['automation']} ID de la automatización a eliminar")
            )

            show_loading("Buscando automatización...", 0.5)
            automatizacion = self.automation_service.obtener_automatizacion(auto_id)

            if not automatizacion:
                console.print()
                print_error("Automatización no encontrada")
                pause()
                return

            # Mostrar información
            console.print()
            info_panel = Panel(
                f"[cyan]Nombre:[/cyan] [white]{automatizacion.name}[/white]\n"
                f"[cyan]Descripción:[/cyan] [white]{automatizacion.description}[/white]\n"
                f"[cyan]Hogar:[/cyan] [magenta]{automatizacion.home.name}[/magenta]",
                title=f"{ICONS['warning']} Automatización a Eliminar",
                border_style=COLORS["error"],
                padding=(1, 2),
            )
            console.print(info_panel)

            # Confirmar
            console.print()
            if ask_confirm("¿Confirmar eliminación?"):
                show_loading("Eliminando automatización...", 0.8)
                exito, mensaje = self.automation_service.eliminar_automatizacion(auto_id)

                console.print()
                if exito:
                    print_success(mensaje)
                else:
                    print_error(mensaje)
            else:
                console.print()
                print_info("Operación cancelada")

        except ValueError:
            console.print()
            print_error("Error: Debe ingresar un número válido")
        except Exception as e:
            console.print()
            print_error(f"Error: {e}")

        pause()

    # ============================================
    # FLUJOS DE ADMINISTRACIÓN
    # ============================================

    def flujo_cambiar_rol_usuario(self):
        """Maneja el flujo de cambio de rol de usuario."""
        clear_screen()
        print_header("Cambiar Rol de Usuario", "Modificar permisos de usuario")

        console.print()
        email = ask_input(f"{ICONS['user']} Email del usuario")

        # Obtener roles disponibles
        show_loading("Cargando roles...", 0.5)
        roles = self.auth_service.listar_roles()

        if not roles:
            console.print()
            print_error("No hay roles disponibles")
            pause()
            return

        console.print()
        console.print(f"\n{ICONS['admin']} [bold magenta]Roles disponibles:[/bold magenta]")
        for r in roles:
            console.print(f"  [magenta]{r.id}[/magenta]. {r.name}")

        try:
            console.print()
            nuevo_rol_id = int(ask_input("Seleccione ID del nuevo rol"))

            console.print()
            show_loading("Cambiando rol...", 0.8)

            exito, mensaje = self.auth_service.cambiar_rol_usuario(email, nuevo_rol_id)

            console.print()
            if exito:
                print_success(mensaje)
            else:
                print_error(mensaje)

        except ValueError:
            console.print()
            print_error("Error: Debe ingresar un número válido")
        except Exception as e:
            console.print()
            print_error(f"Error: {e}")

        pause()
