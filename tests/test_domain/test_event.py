"""
Tests para la clase Event
Estos tests verifican el funcionamiento del sistema de eventos.
"""

import sys
import os
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "models"))

from dominio.event import Event
from dominio.device import Device
from dominio.user import User
from dominio.role import Role
from dominio.home import Home
from dominio.location import Location
from dominio.state import State
from dominio.device_type import DeviceType


class TestEvent:
    """Tests para la clase Event"""

    def test_crear_event_login(self):
        """Test: Crear evento de login (sin objetos complejos)"""
        fecha_hora = datetime(2025, 9, 15, 10, 30, 0)
        event = Event(
            1,
            "Login Fernando",
            "user_action",
            date_time_value=fecha_hora
        )

        assert event.id == 1
        assert event.date_time_value == fecha_hora
        assert event.description == "Login Fernando"
        assert event.device is None
        assert event.user is None
        assert event.source == "user_action"

    def test_crear_event_dispositivo_cambio_estado(self):
        """Test: Crear evento de cambio de estado (sin objetos complejos)"""
        fecha_hora = datetime(2025, 9, 15, 14, 15, 30)
        event = Event(
            2,
            "Luz Sala cambió estado",
            "user_action",
            date_time_value=fecha_hora
        )

        assert event.id == 2
        assert event.description == "Luz Sala cambió estado"
        assert event.source == "user_action"

    def test_crear_event_automatizacion(self):
        """Test: Crear evento de automatización"""
        fecha_hora = datetime.now()
        event = Event(
            3,
            "Automatización ejecutada",
            "automation",
            date_time_value=fecha_hora
        )

        assert event.source == "automation"
        assert event.device is None
        assert event.user is None

    def test_crear_event_device_trigger(self):
        """Test: Crear evento disparado por dispositivo"""
        fecha_hora = datetime.now()
        event = Event(
            4,
            "Sensor detectó movimiento",
            "device_trigger",
            date_time_value=fecha_hora
        )

        assert event.source == "device_trigger"
        assert event.description == "Sensor detectó movimiento"

    def test_crear_event_system_error(self):
        """Test: Crear evento de error del sistema"""
        fecha_hora = datetime.now()
        event = Event(
            5,
            "Error de conexión",
            "system_error",
            date_time_value=fecha_hora
        )

        assert event.source == "system_error"
        assert event.description == "Error de conexión"

    def test_modificar_descripcion_event(self):
        """Test: Modificar la descripción del evento"""
        # Arrange
        fecha_hora = datetime.now()
        event = Event(
            7,
            "Descripción original",
            "user_action",
            date_time_value=fecha_hora
        )
        nueva_descripcion = "Descripción modificada"

        # Act
        event.description = nueva_descripcion

        # Assert
        assert event.description == "Descripción modificada"
        assert event.id == 7  # ID no cambia

    def test_event_con_datetime_especifico(self):
        """Test: Verificar que maneja fechas específicas correctamente"""
        fecha_especifica = datetime(2025, 12, 25, 9, 0, 0)  # Navidad 2025
        event = Event(
            8,
            "Evento navideño",
            "user_action",
            date_time_value=fecha_especifica
        )

        assert event.date_time_value.year == 2025
        assert event.date_time_value.month == 12
        assert event.date_time_value.day == 25
        assert event.date_time_value.hour == 9

    def test_event_sin_datetime_usa_now(self):
        """Test: Si no se proporciona datetime, usa datetime.now()"""
        event = Event(9, "Test event", "manual")
        
        # Verificar que tiene un datetime cercano a ahora (últimos 2 segundos)
        now = datetime.now()
        diff = (now - event.date_time_value).total_seconds()
        assert diff < 2  # Menos de 2 segundos de diferencia

    def test_types_event(self):
        """Test: Verificar tipos de datos correctos"""
        fecha_hora = datetime.now()
        event = Event(10, "Test", "user_action", date_time_value=fecha_hora)

        assert isinstance(event.id, int)
        assert isinstance(event.date_time_value, datetime)
        assert isinstance(event.description, str)
        assert isinstance(event.source, str)


class TestEventConObjetosCompletos:
    """Tests que verifican Event con objetos Device y User completos"""

    def test_crear_event_con_device_completo(self):
        """Test: Crear evento con objeto Device completo"""
        # Crear toda la cadena de objetos para Device
        home = Home(1, "Casa Principal")
        location = Location(1, "Sala", home)
        state = State(1, "Encendido")
        device_type = DeviceType(1, "Luz Inteligente", "LED controlable")
        device = Device(1, "Luz Principal Sala", state, device_type, location, home)
        
        # Crear evento con device
        event = Event(
            100,
            "Dispositivo activado",
            "device_trigger",
            device=device
        )

        assert event.id == 100
        assert event.device is not None
        assert event.device.id == 1
        assert event.device.name == "Luz Principal Sala"
        assert event.source == "device_trigger"

    def test_crear_event_con_user_completo(self):
        """Test: Crear evento con objeto User completo"""
        # Crear objetos necesarios para User
        role = Role(1, "Administrador")
        user = User("admin@smarthome.com", "password123", "Admin User", role)
        
        # Crear evento con user
        event = Event(
            101,
            "Login exitoso",
            "user_action",
            user=user
        )

        assert event.id == 101
        assert event.user is not None
        assert event.user.email == "admin@smarthome.com"
        assert event.user.name == "Admin User"
        assert event.source == "user_action"


# Tests simples
def test_event_basico():
    """Test básico: Crear un evento simple"""
    fecha = datetime.now()
    event = Event(1, "Test event", "manual", date_time_value=fecha)
    assert event.description == "Test event"


def test_event_sin_dispositivo():
    """Test: Evento sin dispositivo involucrado"""
    fecha = datetime.now()
    event = Event(2, "Login usuario", "user_action", date_time_value=fecha)
    assert event.device is None


def test_event_sin_usuario():
    """Test: Evento sin usuario (automático)"""
    fecha = datetime.now()
    event = Event(3, "Sensor activado", "device_trigger", date_time_value=fecha)
    assert event.user is None


def test_cambiar_descripcion():
    """Test: Modificar descripción de evento"""
    fecha = datetime.now()
    event = Event(4, "Original", "user_action", date_time_value=fecha)
    event.description = "Modificada"
    assert event.description == "Modificada"


def test_diferentes_sources():
    """Test: Verificar diferentes tipos de source"""
    fecha = datetime.now()

    event1 = Event(1, "Test 1", "user_action", date_time_value=fecha)
    event2 = Event(2, "Test 2", "automation", date_time_value=fecha)
    event3 = Event(3, "Test 3", "device_trigger", date_time_value=fecha)
    event4 = Event(4, "Test 4", "system_error", date_time_value=fecha)

    assert event1.source == "user_action"
    assert event2.source == "automation"
    assert event3.source == "device_trigger"
    assert event4.source == "system_error"