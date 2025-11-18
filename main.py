"""
Programa principal del sistema SmartHome.

Este módulo implementa la interfaz de usuario por consola para:
- Registro e inicio de sesión de usuarios
- Gestión de dispositivos (CRUD) para administradores
- Consulta de datos para usuarios estándar
"""

import sys
from dao.user_dao import UserDAO
from dao.role_dao import RoleDAO
from dao.device_dao import DeviceDAO
from dao.home_dao import HomeDAO
from dao.state_dao import StateDAO
from dao.device_type_dao import DeviceTypeDAO
from dao.location_dao import LocationDAO
from dominio.user import User
from dominio.device import Device
from conn.db_connection import DatabaseConnection


class SmartHomeApp:
    """Aplicación principal del sistema SmartHome."""
    
    def __init__(self):
        """Inicializa los DAOs necesarios."""
        self.user_dao = UserDAO()
        self.role_dao = RoleDAO()
        self.device_dao = DeviceDAO()
        self.home_dao = HomeDAO()
        self.state_dao = StateDAO()
        self.device_type_dao = DeviceTypeDAO()
        self.location_dao = LocationDAO()
        self.usuario_actual = None
    
    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola."""
        print("\n" * 2)
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal."""
        print("\n" + "="*50)
        print("     SISTEMA SMARTHOME")
        print("="*50)
        print("1. Registrar nuevo usuario")
        print("2. Iniciar sesión")
        print("3. Salir")
        print("="*50)
    
    def registrar_usuario(self):
        """Registra un nuevo usuario estándar."""
        print("\n--- REGISTRO DE USUARIO ---")
        email = input("Email: ").strip()
        
        if self.user_dao.obtener_por_email(email):
            print("✗ El email ya está registrado")
            return
        
        password = input("Contraseña: ").strip()
        name = input("Nombre completo: ").strip()
        
        role = self.role_dao.obtener_por_id(2)
        if not role:
            print("✗ Error: No se encontró el rol estándar")
            return
        
        usuario = User(email, password, name, role)
        
        if self.user_dao.insertar(usuario):
            print("✓ Usuario registrado exitosamente")
        else:
            print("✗ Error al registrar usuario")
    
    def iniciar_sesion(self):
        """Permite a un usuario iniciar sesión."""
        print("\n--- INICIO DE SESIÓN ---")
        email = input("Email: ").strip()
        password = input("Contraseña: ").strip()
        
        usuario = self.user_dao.validar_credenciales(email, password)
        
        if usuario:
            self.usuario_actual = usuario
            print(f"✓ Bienvenido {usuario.name}!")
            return True
        else:
            print("✗ Credenciales inválidas")
            return False
    
    def menu_usuario_estandar(self):
        """Menú para usuarios estándar."""
        while True:
            print("\n" + "="*50)
            print(f"     USUARIO: {self.usuario_actual.name}")
            print("="*50)
            print("1. Consultar mis datos personales")
            print("2. Consultar mis dispositivos")
            print("3. Cerrar sesión")
            print("="*50)
            
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "1":
                self.consultar_datos_personales()
            elif opcion == "2":
                self.consultar_dispositivos_usuario()
            elif opcion == "3":
                self.usuario_actual = None
                print("✓ Sesión cerrada")
                break
            else:
                print("✗ Opción inválida")
    
    def menu_administrador(self):
        """Menú para usuarios administradores."""
        while True:
            print("\n" + "="*50)
            print(f"     ADMINISTRADOR: {self.usuario_actual.name}")
            print("="*50)
            print("1. Gestionar dispositivos (CRUD)")
            print("2. Cambiar rol de usuario")
            print("3. Cerrar sesión")
            print("="*50)
            
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "1":
                self.menu_crud_dispositivos()
            elif opcion == "2":
                self.cambiar_rol_usuario()
            elif opcion == "3":
                self.usuario_actual = None
                print("✓ Sesión cerrada")
                break
            else:
                print("✗ Opción inválida")
    
    def consultar_datos_personales(self):
        """Muestra los datos personales del usuario."""
        print("\n--- MIS DATOS PERSONALES ---")
        print(f"Email: {self.usuario_actual.email}")
        print(f"Nombre: {self.usuario_actual.name}")
        print(f"Rol: {self.usuario_actual.role.name}")
    
    def consultar_dispositivos_usuario(self):
        """Muestra los dispositivos asociados al usuario."""
        print("\n--- MIS DISPOSITIVOS ---")
        
        hogares = self.home_dao.obtener_hogares_usuario(self.usuario_actual.email)
        
        if not hogares:
            print("No tienes hogares asociados")
            return
        
        for hogar in hogares:
            print(f"\nHogar: {hogar.name}")
            dispositivos = self.device_dao.obtener_por_hogar(hogar.id)
            
            if dispositivos:
                for disp in dispositivos:
                    print(f"  - {disp.name} ({disp.device_type.name}) - {disp.state.name}")
            else:
                print("  No hay dispositivos en este hogar")
    
    def menu_crud_dispositivos(self):
        """Menú CRUD para dispositivos."""
        while True:
            print("\n--- GESTIÓN DE DISPOSITIVOS ---")
            print("1. Crear dispositivo")
            print("2. Ver dispositivos")
            print("3. Actualizar dispositivo")
            print("4. Eliminar dispositivo")
            print("5. Volver")
            
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "1":
                self.crear_dispositivo()
            elif opcion == "2":
                self.ver_dispositivos()
            elif opcion == "3":
                self.actualizar_dispositivo()
            elif opcion == "4":
                self.eliminar_dispositivo()
            elif opcion == "5":
                break
            else:
                print("✗ Opción inválida")
    
    def crear_dispositivo(self):
        """Crea un nuevo dispositivo."""
        print("\n--- CREAR DISPOSITIVO ---")
        
        try:
            nombre = input("Nombre del dispositivo: ").strip()
            
            hogares = self.home_dao.obtener_todos()
            if not hogares:
                print("✗ No hay hogares disponibles")
                return
            
            print("\nHogares disponibles:")
            for h in hogares:
                print(f"{h.id}. {h.name}")
            home_id = int(input("ID del hogar: "))
            home = self.home_dao.obtener_por_id(home_id)
            
            tipos = self.device_type_dao.obtener_todos()
            print("\nTipos de dispositivo:")
            for t in tipos:
                print(f"{t.id}. {t.name}")
            type_id = int(input("ID del tipo: "))
            device_type = self.device_type_dao.obtener_por_id(type_id)
            
            ubicaciones = self.location_dao.obtener_todos()
            print("\nUbicaciones:")
            for u in ubicaciones:
                print(f"{u.id}. {u.name}")
            loc_id = int(input("ID de ubicación: "))
            location = self.location_dao.obtener_por_id(loc_id)
            
            estados = self.state_dao.obtener_todos()
            print("\nEstados:")
            for e in estados:
                print(f"{e.id}. {e.name}")
            state_id = int(input("ID del estado: "))
            state = self.state_dao.obtener_por_id(state_id)
            
            if all([home, device_type, location, state]):
                dispositivo = Device(0, nombre, state, device_type, location, home)
                if self.device_dao.insertar(dispositivo):
                    print("✓ Dispositivo creado exitosamente")
                else:
                    print("✗ Error al crear dispositivo")
            else:
                print("✗ Error: Datos inválidos")
        except ValueError:
            print("✗ Error: Debe ingresar un número válido")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    def ver_dispositivos(self):
        """Muestra todos los dispositivos."""
        print("\n--- LISTA DE DISPOSITIVOS ---")
        dispositivos = self.device_dao.obtener_todos()
        
        if not dispositivos:
            print("No hay dispositivos registrados")
            return
        
        for disp in dispositivos:
            print(f"\nID: {disp.id}")
            print(f"Nombre: {disp.name}")
            print(f"Tipo: {disp.device_type.name}")
            print(f"Estado: {disp.state.name}")
            print(f"Ubicación: {disp.location.name}")
            print(f"Hogar: {disp.home.name}")
            print("-" * 40)
    
    def actualizar_dispositivo(self):
        """Actualiza un dispositivo existente."""
        print("\n--- ACTUALIZAR DISPOSITIVO ---")
        
        try:
            device_id = int(input("ID del dispositivo a actualizar: "))
            dispositivo = self.device_dao.obtener_por_id(device_id)
            
            if not dispositivo:
                print("✗ Dispositivo no encontrado")
                return
            
            print(f"\nDispositivo actual: {dispositivo.name}")
            nuevo_nombre = input("Nuevo nombre (Enter para mantener): ").strip()
            
            if nuevo_nombre:
                dispositivo.name = nuevo_nombre
            
            print("\n¿Cambiar estado?")
            estados = self.state_dao.obtener_todos()
            for e in estados:
                print(f"{e.id}. {e.name}")
            cambiar = input("ID del nuevo estado (Enter para mantener): ").strip()
            
            if cambiar:
                nuevo_estado = self.state_dao.obtener_por_id(int(cambiar))
                if nuevo_estado:
                    dispositivo.state = nuevo_estado
            
            if self.device_dao.modificar(dispositivo):
                print("✓ Dispositivo actualizado exitosamente")
            else:
                print("✗ Error al actualizar dispositivo")
        except ValueError:
            print("✗ Error: Debe ingresar un número válido")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    def eliminar_dispositivo(self):
        """Elimina un dispositivo."""
        print("\n--- ELIMINAR DISPOSITIVO ---")
        
        try:
            device_id = int(input("ID del dispositivo a eliminar: "))
            dispositivo = self.device_dao.obtener_por_id(device_id)
            
            if not dispositivo:
                print("✗ Dispositivo no encontrado")
                return
            
            print(f"\nDispositivo: {dispositivo.name}")
            confirmar = input("¿Confirmar eliminación? (s/n): ").strip().lower()
            
            if confirmar == 's':
                if self.device_dao.eliminar(device_id):
                    print("✓ Dispositivo eliminado exitosamente")
                else:
                    print("✗ Error al eliminar dispositivo")
            else:
                print("Operación cancelada")
        except ValueError:
            print("✗ Error: Debe ingresar un número válido")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    def cambiar_rol_usuario(self):
        """Cambia el rol de un usuario."""
        print("\n--- CAMBIAR ROL DE USUARIO ---")
        
        email = input("Email del usuario: ").strip()
        usuario = self.user_dao.obtener_por_email(email)
        
        if not usuario:
            print("✗ Usuario no encontrado")
            return
        
        print(f"\nUsuario: {usuario.name}")
        print(f"Rol actual: {usuario.role.name}")
        
        roles = self.role_dao.obtener_todos()
        print("\nRoles disponibles:")
        for r in roles:
            print(f"{r.id}. {r.name}")
        
        try:
            nuevo_rol_id = int(input("ID del nuevo rol: "))
            
            if self.user_dao.cambiar_rol(email, nuevo_rol_id):
                print("✓ Rol cambiado exitosamente")
            else:
                print("✗ Error al cambiar rol")
        except ValueError:
            print("✗ Error: Debe ingresar un número válido")
    
    def ejecutar(self):
        """Ejecuta la aplicación principal."""
        print("\n¡Bienvenido al Sistema SmartHome!")
        
        while True:
            self.mostrar_menu_principal()
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "1":
                self.registrar_usuario()
            elif opcion == "2":
                if self.iniciar_sesion():
                    if self.usuario_actual.is_admin():
                        self.menu_administrador()
                    else:
                        self.menu_usuario_estandar()
            elif opcion == "3":
                print("\n¡Hasta luego!")
                sys.exit(0)
            else:
                print("✗ Opción inválida")


def main():
    """Punto de entrada del programa."""
    try:
        app = SmartHomeApp()
        app.ejecutar()
    except KeyboardInterrupt:
        print("\n\n¡Programa interrumpido por el usuario!")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
 try:
    main()
 finally:
     db=DatabaseConnection()
     db.disconnect()