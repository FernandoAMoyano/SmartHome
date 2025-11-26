"""
Punto de entrada del sistema SmartHome.

Este archivo solo contiene la lógica de inicio y orquestación de alto nivel.
Toda la lógica de negocio está en la capa de servicios (services/).
Toda la lógica de presentación está en la capa de UI (ui/).

Arquitectura:
- UI Layer (ui/): Presentación e interacción con el usuario
- Service Layer (services/): Lógica de negocio
- DAO Layer (dao/): Acceso a datos
- Domain Layer (dominio/): Entidades del negocio
- Connection Layer (conn/): Gestión de conexión a BD
"""

import sys
from ui.console_ui import ConsoleUI
from conn.db_connection import DatabaseConnection


def main():
    """
    Punto de entrada del programa.

    Responsabilidades:
    - Inicializar la aplicación
    - Orquestar el flujo de menús principales
    - Manejar el cierre de la aplicación
    """
    print("\n" + "=" * 50)
    print("  ¡Bienvenido al Sistema SmartHome!")
    print("=" * 50)

    # Inicializar interfaz de usuario
    ui = ConsoleUI()

    # Bucle principal de la aplicación
    while True:
        ui.mostrar_menu_principal()
        opcion = input("Seleccione una opción: ").strip()

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
            print("\n" + "=" * 50)
            print("  ¡Hasta luego! Gracias por usar SmartHome")
            print("=" * 50)
            sys.exit(0)

        else:
            print("✗ Opción inválida. Por favor, seleccione 1, 2 o 3.")


def ejecutar_menu_administrador(ui: ConsoleUI):
    """
    Ejecuta el menú de administrador.

    Args:
        ui: Instancia de ConsoleUI
    """
    while ui.auth_service.obtener_usuario_actual():
        usuario = ui.auth_service.obtener_usuario_actual()
        ui.mostrar_menu_admin(usuario.name)
        opcion_admin = input("Seleccione una opción: ").strip()

        if opcion_admin == "1":
            # Gestionar dispositivos (CRUD)
            ejecutar_menu_crud_dispositivos(ui)

        elif opcion_admin == "2":
            # Cambiar rol de usuario
            ui.flujo_cambiar_rol_usuario()

        elif opcion_admin == "3":
            # Cerrar sesión
            ui.auth_service.cerrar_sesion()
            print("\n✓ Sesión cerrada correctamente")
            break

        else:
            print("✗ Opción inválida")


def ejecutar_menu_usuario_estandar(ui: ConsoleUI):
    """
    Ejecuta el menú de usuario estándar.

    Args:
        ui: Instancia de ConsoleUI
    """
    while ui.auth_service.obtener_usuario_actual():
        usuario = ui.auth_service.obtener_usuario_actual()
        ui.mostrar_menu_usuario(usuario.name)
        opcion_user = input("Seleccione una opción: ").strip()

        if opcion_user == "1":
            # Consultar datos personales
            ui.flujo_consultar_datos_personales()

        elif opcion_user == "2":
            # Consultar dispositivos
            ui.flujo_consultar_dispositivos_usuario()

        elif opcion_user == "3":
            # Gestionar automatizaciones
            ejecutar_menu_automatizaciones(ui)

        elif opcion_user == "4":
            # Cerrar sesión
            ui.auth_service.cerrar_sesion()
            print("\n✓ Sesión cerrada correctamente")
            break

        else:
            print("✗ Opción inválida")


def ejecutar_menu_crud_dispositivos(ui: ConsoleUI):
    """
    Ejecuta el menú CRUD de dispositivos.

    Args:
        ui: Instancia de ConsoleUI
    """
    while True:
        ui.mostrar_menu_crud_dispositivos()
        opcion_crud = input("Seleccione una opción: ").strip()

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
            print("✗ Opción inválida")


def ejecutar_menu_automatizaciones(ui: ConsoleUI):
    """
    Ejecuta el menú de automatizaciones.

    Args:
        ui: Instancia de ConsoleUI
    """
    while True:
        ui.mostrar_menu_automatizaciones()
        opcion_auto = input("Seleccione una opción: ").strip()

        if opcion_auto == "1":
            # Ver automatizaciones
            ui.flujo_ver_automatizaciones_usuario()

        elif opcion_auto == "2":
            # Crear automatización
            ui.flujo_crear_automatizacion()

        elif opcion_auto == "3":
            # Activar/Desactivar automatización
            ui.flujo_cambiar_estado_automatizacion()

        elif opcion_auto == "4":
            # Actualizar automatización
            ui.flujo_actualizar_automatizacion()

        elif opcion_auto == "5":
            # Eliminar automatización
            ui.flujo_eliminar_automatizacion()

        elif opcion_auto == "6":
            # Volver al menú anterior
            break

        else:
            print("✗ Opción inválida")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Programa interrumpido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error fatal: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
    finally:
        # Asegurar que la conexión a BD se cierre correctamente
        db = DatabaseConnection()
        db.disconnect()
