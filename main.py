"""
Punto de entrada del sistema SmartHome con UI Rich.

Este archivo solo contiene la lógica de inicio y orquestación de alto nivel.
Toda la lógica de negocio está en la capa de servicios (services/).
Toda la lógica de presentación está en la capa de UI (ui/).

Arquitectura:
- UI Layer (ui/): Presentación e interacción con Rich
- Service Layer (services/): Lógica de negocio
- DAO Layer (dao/): Acceso a datos
- Domain Layer (dominio/): Entidades del negocio
- Connection Layer (conn/): Gestión de conexión a BD
"""

import sys
from ui.rich_console_ui import RichConsoleUI
from ui.rich_utils import console, print_header, ICONS
from conn.db_connection import DatabaseConnection


def main():
    """
    Punto de entrada del programa.

    Responsabilidades:
    - Inicializar la aplicación
    - Orquestar el flujo de menús principales
    - Manejar el cierre de la aplicación
    """
    # Inicializar interfaz de usuario Rich
    ui = RichConsoleUI()

    # Bucle principal de la aplicación
    while True:
        ui.mostrar_menu_principal()
        opcion = console.input("\n[cyan]➤[/cyan] Seleccione una opción: ").strip()

        if opcion == "1":
            # Registrar nuevo usuario
            ui.flujo_registro()

        elif opcion == "2":
            # Iniciar sesión
            if ui.flujo_login():
                # Verificar rol y mostrar menú correspondiente
                if ui.auth_service.es_admin():
                    ejecutar_menu_administrador(ui)
                else:
                    ejecutar_menu_usuario_estandar(ui)

        elif opcion == "3":
            # Salir del sistema
            console.clear()
            print_header("¡Hasta luego!", "Gracias por usar SmartHome")
            console.print(
                f"\n[cyan]{ICONS['exit']}[/cyan] Sistema cerrado correctamente\n"
            )
            sys.exit(0)

        else:
            console.print(
                f"\n[red]{ICONS['error']}[/red] Opción inválida. "
                "Por favor, seleccione 1, 2 o 3.\n"
            )
            console.input("[dim]Presione Enter para continuar...[/dim]")


def ejecutar_menu_administrador(ui: RichConsoleUI):
    """
    Ejecuta el menú de administrador.

    Args:
        ui: Instancia de RichConsoleUI
    """
    while ui.auth_service.obtener_usuario_actual():
        usuario = ui.auth_service.obtener_usuario_actual()
        ui.mostrar_menu_admin(usuario.name)
        opcion_admin = console.input(
            "\n[magenta]➤[/magenta] Seleccione una opción: "
        ).strip()

        if opcion_admin == "1":
            # Gestionar dispositivos (CRUD)
            ejecutar_menu_crud_dispositivos(ui)

        elif opcion_admin == "2":
            # Gestionar automatizaciones (CRUD)
            ejecutar_menu_crud_automatizaciones(ui)

        elif opcion_admin == "3":
            # Cambiar rol de usuario
            ui.flujo_cambiar_rol_usuario()

        elif opcion_admin == "4":
            # Cerrar sesión
            ui.auth_service.cerrar_sesion()
            console.print(
                f"\n[green]{ICONS['success']}[/green] Sesión cerrada correctamente\n"
            )
            console.input("[dim]Presione Enter para continuar...[/dim]")
            break

        else:
            console.print(f"\n[red]{ICONS['error']}[/red] Opción inválida\n")
            console.input("[dim]Presione Enter para continuar...[/dim]")


def ejecutar_menu_usuario_estandar(ui: RichConsoleUI):
    """
    Ejecuta el menú de usuario estándar.

    Args:
        ui: Instancia de RichConsoleUI
    """
    while ui.auth_service.obtener_usuario_actual():
        usuario = ui.auth_service.obtener_usuario_actual()
        ui.mostrar_menu_usuario(usuario.name)
        opcion_user = console.input("\n[cyan]➤[/cyan] Seleccione una opción: ").strip()

        if opcion_user == "1":
            # Consultar datos personales
            ui.flujo_consultar_datos_personales()

        elif opcion_user == "2":
            # Consultar dispositivos
            ui.flujo_consultar_dispositivos_usuario()

        elif opcion_user == "3":
            # Consultar automatizaciones
            ui.flujo_consultar_automatizaciones_usuario()

        elif opcion_user == "4":
            # Cerrar sesión
            ui.auth_service.cerrar_sesion()
            console.print(
                f"\n[green]{ICONS['success']}[/green] Sesión cerrada correctamente\n"
            )
            console.input("[dim]Presione Enter para continuar...[/dim]")
            break

        else:
            console.print(f"\n[red]{ICONS['error']}[/red] Opción inválida\n")
            console.input("[dim]Presione Enter para continuar...[/dim]")


def ejecutar_menu_crud_dispositivos(ui: RichConsoleUI):
    """
    Ejecuta el menú CRUD de dispositivos.

    Args:
        ui: Instancia de RichConsoleUI
    """
    while True:
        ui.mostrar_menu_crud_dispositivos()
        opcion_crud = console.input("\n[cyan]➤[/cyan] Seleccione una opción: ").strip()

        if opcion_crud == "1":
            # Crear dispositivo
            ui.flujo_crear_dispositivo()

        elif opcion_crud == "2":
            # Ver todos los dispositivos
            ui.flujo_ver_dispositivos()

        elif opcion_crud == "3":
            # Actualizar dispositivo
            ui.flujo_actualizar_dispositivo()

        elif opcion_crud == "4":
            # Eliminar dispositivo
            ui.flujo_eliminar_dispositivo()

        elif opcion_crud == "5":
            # Volver al menú anterior
            break

        else:
            console.print(f"\n[red]{ICONS['error']}[/red] Opción inválida\n")
            console.input("[dim]Presione Enter para continuar...[/dim]")


def ejecutar_menu_crud_automatizaciones(ui: RichConsoleUI):
    """
    Ejecuta el menú CRUD de automatizaciones.

    Args:
        ui: Instancia de RichConsoleUI
    """
    while True:
        ui.mostrar_menu_crud_automatizaciones()
        opcion_crud = console.input("\n[cyan]➤[/cyan] Seleccione una opción: ").strip()

        if opcion_crud == "1":
            # Crear automatización
            ui.flujo_crear_automatizacion()

        elif opcion_crud == "2":
            # Ver todas las automatizaciones
            ui.flujo_ver_automatizaciones()

        elif opcion_crud == "3":
            # Actualizar automatización
            ui.flujo_actualizar_automatizacion()

        elif opcion_crud == "4":
            # Activar/Desactivar automatización
            ui.flujo_activar_desactivar_automatizacion()

        elif opcion_crud == "5":
            # Eliminar automatización
            ui.flujo_eliminar_automatizacion()

        elif opcion_crud == "6":
            # Volver al menú anterior
            break

        else:
            console.print(f"\n[red]{ICONS['error']}[/red] Opción inválida\n")
            console.input("[dim]Presione Enter para continuar...[/dim]")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.clear()
        console.print("\n[yellow]⚠️  Programa interrumpido por el usuario[/yellow]\n")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]✗ Error fatal: {e}[/red]")
        import traceback

        traceback.print_exc()
        sys.exit(1)
    finally:
        # Asegurar que la conexión a BD se cierre correctamente
        db = DatabaseConnection()
        db.disconnect()
