# 🏠 SmartHome - Sistema de Gestión Domótica

---

# Descripción

Sistema integral de gestión domótica que permite controlar dispositivos inteligentes en el hogar mediante una aplicación de consola. Implementa el patrón de diseño DAO (Data Access Object) para separar la lógica de negocio de la persistencia de datos.

---

# Propósito

Desarrollar un sistema completo de SmartHome que permita:

- Gestión de usuarios con diferentes roles (admin/estándar)
- Control CRUD de dispositivos inteligentes
- Automatizaciones y escenarios domóticos
- Registro de eventos y auditoría
- Gestión de múltiples hogares por usuario

---

# Contexto

Este proyecto es parte de la **Evidencia VI del Módulo Programador** del **ISPC** (Instituto Superior Politécnico Córdoba). Dicha entrega toma como punto de partida la **evidencia V** con las respectivas correcciones aplicadas.Integra conocimientos de:

- Programación Orientada a Objetos (POO)
- Bases de Datos Relacionales
- Patrones de Diseño (DAO, Singleton)
- Python y MySQL

# Alcance

---

### Funcionalidades Implementadas

#### Para Usuarios Estándar:

- ✓ Registro de nuevos usuarios
- ✓ Inicio de sesión seguro
- ✓ Consulta de datos personales
- ✓ Visualización de dispositivos asociados

#### Para Administradores:

- ✓ CRUD completo de dispositivos
  - Crear nuevos dispositivos
  - Listar todos los dispositivos
  - Actualizar información de dispositivos
  - Eliminar dispositivos
- ✓ Cambio de rol de usuarios
- ✓ Gestión de hogares

### Alcance Técnico:

- ✓ Arquitectura en capas (dominio, DAO, interfaces, conexión)
- ✓ Patrón DAO para acceso a datos
- ✓ Conexión a MySQL con mysql-connector
- ✓ Encapsulación y POO
- ✓ Type hints y documentación completa
- ✓ Manejo de excepciones

# Autores

---

- **Fernando Agustín Moyano**

- **Institución:** Instituto Superior Politécnico Córdoba (ISPC)
- **Año:** 2025
- **Módulo:** Programador I

# Tecnologías Utilizadas

---

- **Lenguaje:** Python 3.11+
- **Base de Datos:** MySQL 8.0
- **Librerías:**
  - `mysql-connector-python` - Conexión a MySQL
  - `pytest` - Testing unitario

# 📁 Estructura del Proyecto

---

```
POO-SmartHome/
│
├──📁 dominio/
│   ├── event.py
│   ├── automation.py           # Entidades del dominio
│   ├── user.py
│   ├── role.py
│   ├── device.py
│   ├── state.py
│   ├── device_type.py
│   ├── location.py
│   ├── home.py
│   └── __init__.py
│
├──📁 interfaces/                # Interfaces DAO
│   ├── i_dao.py
│   ├── i_user_dao.py
│   ├── i_device_dao.py
│   └── __init__.py
│
├──📁 dao/
│   ├── event_dao.py
│   ├── automation_dao.py        # Implementaciones DAO
│   ├── role_dao.py
│   ├── user_dao.py
│   ├── state_dao.py
│   ├── device_type_dao.py
│   ├── location_dao.py
│   ├── home_dao.py
│   ├── device_dao.py
│   └── __init__.py
│
├──📁 conn/                     # Conexión a BD
│   ├── db_connection.py
│   └── __init__.py
│
├──📁 tests/                    # Tests
├── main.py                     # Punto de entrada
└── README.md
```

# Instalación y Configuración

---

### Prerrequisitos

- Python 3.11 o superior
- MySQL 8.0 o superior
- pip (gestor de paquetes de Python)

### 1. Clonar el Repositorio

```bash
git clone [URL_DEL_REPOSITORIO]
cd POO-SmartHome
```

### 2. Instalar Dependencias

```bash
pip install mysql-connector-python
pip install pytest  # Para ejecutar tests
```

### 3. Configurar Base de Datos

1. Crear la base de datos ejecutando el DDL:

```bash
# Ubicado en: ../BD-Evidencia-5/DDL-SmartHome.sql
mysql -u root -p < ../BD-Evidencia-5/DDL-SmartHome.sql
```

2. Insertar datos iniciales:

```bash
# Ubicado en: ../BD-Evidencia-6/DML-SmartHome.sql
mysql -u root -p < ../BD-Evidencia-6/DML-SmartHome.sql
```

### 4. Configurar Conexión

Editar el archivo `conn/db_connection.py` con tus credenciales:

```python
self.host = 'localhost'
self.database = 'smarthome'
self.user = 'root'
self.password = 'tu_contraseña'  # Cambiar aquí
self.port = 3306
```

# Uso del Sistema

---

### Ejecutar la Aplicación

```bash
python main.py
```

### Menú Principal

```
==================================================
     SISTEMA SMARTHOME
==================================================
1. Registrar nuevo usuario
2. Iniciar sesión
3. Salir
==================================================
```

### Credenciales de Prueba

**Administrador:**

- Email: `admin@smarthome.com`
- Password: `admin123`

**Usuario Estándar:**

- Email: `juan.perez@email.com`
- Password: `pass123`

# Guía de Uso

---

### Para Usuarios Estándar

1. **Registrarse:**

   - Seleccionar opción 1
   - Ingresar email, contraseña y nombre
   - Se asignará automáticamente rol "standard"

2. **Iniciar Sesión:**

   - Seleccionar opción 2
   - Ingresar credenciales

3. **Consultar Datos Personales:**

   - Opción 1 del menú usuario
   - Ver email, nombre y rol

4. **Ver Dispositivos:**
   - Opción 2 del menú usuario
   - Listar dispositivos por hogar

### Para Administradores

1. **Gestionar Dispositivos:**

   - Opción 1 del menú admin
   - Submenú CRUD completo

2. **Crear Dispositivo:**

   - Ingresar nombre
   - Seleccionar hogar, tipo, ubicación y estado
   - Confirmar creación

3. **Actualizar Dispositivo:**

   - Ingresar ID del dispositivo
   - Modificar nombre y/o estado
   - Confirmar cambios

4. **Eliminar Dispositivo:**

   - Ingresar ID del dispositivo
   - Confirmar eliminación

5. **Cambiar Rol de Usuario:**
   - Opción 2 del menú admin
   - Ingresar email del usuario
   - Seleccionar nuevo rol

# Testing

---

### Ejecutar Tests Unitarios

```bash
# Todos los tests
pytest

# Tests específicos
pytest tests/test_user.py
pytest tests/test_device.py

# Con cobertura
pytest --cov=dominio tests/
```

### Tests Disponibles

- ✓ test_user.py - Validación de usuarios
- ✓ test_device.py - Funcionalidad de dispositivos
- ✓ test_role.py - Gestión de roles
- ✓ test_home.py - Operaciones de hogares
- ✓ Y más...

# Arquitectura

---

### Patrón DAO (Data Access Object)

```
┌─────────────┐
│   main.py   │  ← Interfaz de usuario
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  DAO Layer  │  ← Acceso a datos
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Database   │  ← MySQL
└─────────────┘
```

### Flujo de Comunicación

1. **main.py** → Punto de entrada, maneja UI
2. **DAO** → Intermediario entre lógica y BD
3. **Dominio** → Entidades de negocio
4. **Interfaces** → Contratos para DAOs
5. **Conexión** → Singleton para BD

---

**Última actualización:** Octubre 2025  
**Versión:** 1.0.0 (Evidencia VI)
