"""
Módulo de validaciones para el sistema SmartHome.

Proporciona funciones de validación reutilizables con mensajes
de error descriptivos para mejorar la experiencia del usuario.
"""

import re
from typing import Tuple


class ValidationError(Exception):
    """Excepción personalizada para errores de validación."""
    pass


# ============================================
# VALIDACIONES DE EMAIL
# ============================================

def validar_email(email: str) -> Tuple[bool, str]:
    """
    Valida el formato de un email.
    
    Args:
        email: Email a validar
        
    Returns:
        Tupla (es_valido: bool, mensaje_error: str)
        
    Ejemplos:
        >>> validar_email("usuario@example.com")
        (True, "")
        
        >>> validar_email("email_invalido")
        (False, "El email debe tener el formato: usuario@dominio.com")
    """
    # Verificar que no esté vacío
    if not email or not email.strip():
        return False, "El email es obligatorio"
    
    email = email.strip()
    
    # Verificar longitud mínima
    if len(email) < 5:
        return False, "El email es demasiado corto (mínimo 5 caracteres)"
    
    # Verificar longitud máxima
    if len(email) > 100:
        return False, "El email es demasiado largo (máximo 100 caracteres)"
    
    # Patrón regex para email
    # Formato: usuario@dominio.extension
    patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(patron_email, email):
        return False, "El email debe tener el formato: usuario@dominio.com"
    
    return True, ""


# ============================================
# VALIDACIONES DE PASSWORD
# ============================================

def validar_password(password: str) -> Tuple[bool, str]:
    """
    Valida la fortaleza de una contraseña.
    
    Reglas:
    - Mínimo 6 caracteres
    - Máximo 50 caracteres
    - No puede estar vacía
    - No puede contener solo espacios
    
    Args:
        password: Contraseña a validar
        
    Returns:
        Tupla (es_valido: bool, mensaje_error: str)
        
    Ejemplos:
        >>> validar_password("miPassword123")
        (True, "")
        
        >>> validar_password("123")
        (False, "La contraseña debe tener al menos 6 caracteres")
    """
    # Verificar que no esté vacía
    if not password:
        return False, "La contraseña es obligatoria"
    
    # Verificar que no sea solo espacios
    if not password.strip():
        return False, "La contraseña no puede contener solo espacios"
    
    # Verificar longitud mínima
    if len(password) < 6:
        return False, "La contraseña debe tener al menos 6 caracteres"
    
    # Verificar longitud máxima
    if len(password) > 50:
        return False, "La contraseña es demasiado larga (máximo 50 caracteres)"
    
    return True, ""


def validar_password_fuerte(password: str) -> Tuple[bool, str]:
    """
    Valida una contraseña con requisitos más estrictos.
    
    Reglas:
    - Mínimo 8 caracteres
    - Al menos una letra mayúscula
    - Al menos una letra minúscula
    - Al menos un número
    
    Args:
        password: Contraseña a validar
        
    Returns:
        Tupla (es_valido: bool, mensaje_error: str)
    """
    # Primero validar requisitos básicos
    es_valida, mensaje = validar_password(password)
    if not es_valida:
        return False, mensaje
    
    # Verificar longitud mínima para contraseña fuerte
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    
    # Verificar al menos una mayúscula
    if not re.search(r'[A-Z]', password):
        return False, "La contraseña debe contener al menos una letra mayúscula"
    
    # Verificar al menos una minúscula
    if not re.search(r'[a-z]', password):
        return False, "La contraseña debe contener al menos una letra minúscula"
    
    # Verificar al menos un número
    if not re.search(r'\d', password):
        return False, "La contraseña debe contener al menos un número"
    
    return True, ""


# ============================================
# VALIDACIONES DE NOMBRES
# ============================================

def validar_nombre(nombre: str, campo: str = "nombre") -> Tuple[bool, str]:
    """
    Valida un nombre (usuario, dispositivo, automatización, etc.).
    
    Reglas:
    - No puede estar vacío
    - Mínimo 2 caracteres
    - Máximo 100 caracteres
    - Solo letras, números, espacios y caracteres básicos
    
    Args:
        nombre: Nombre a validar
        campo: Nombre del campo (para mensajes personalizados)
        
    Returns:
        Tupla (es_valido: bool, mensaje_error: str)
    """
    # Verificar que no esté vacío
    if not nombre or not nombre.strip():
        return False, f"El {campo} es obligatorio"
    
    nombre = nombre.strip()
    
    # Verificar longitud mínima
    if len(nombre) < 2:
        return False, f"El {campo} debe tener al menos 2 caracteres"
    
    # Verificar longitud máxima
    if len(nombre) > 100:
        return False, f"El {campo} es demasiado largo (máximo 100 caracteres)"
    
    # Verificar caracteres permitidos (letras, números, espacios, guiones, puntos)
    patron_nombre = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s\.\-_]+$'
    
    if not re.match(patron_nombre, nombre):
        return False, f"El {campo} contiene caracteres no permitidos"
    
    return True, ""


# ============================================
# VALIDACIONES DE DESCRIPCIONES
# ============================================

def validar_descripcion(descripcion: str, min_length: int = 10, max_length: int = 500) -> Tuple[bool, str]:
    """
    Valida una descripción.
    
    Args:
        descripcion: Descripción a validar
        min_length: Longitud mínima (default: 10)
        max_length: Longitud máxima (default: 500)
        
    Returns:
        Tupla (es_valido: bool, mensaje_error: str)
    """
    # Verificar que no esté vacía
    if not descripcion or not descripcion.strip():
        return False, "La descripción es obligatoria"
    
    descripcion = descripcion.strip()
    
    # Verificar longitud mínima
    if len(descripcion) < min_length:
        return False, f"La descripción debe tener al menos {min_length} caracteres"
    
    # Verificar longitud máxima
    if len(descripcion) > max_length:
        return False, f"La descripción es demasiado larga (máximo {max_length} caracteres)"
    
    return True, ""


# ============================================
# VALIDACIONES NUMÉRICAS
# ============================================

def validar_id_positivo(id_valor: int, campo: str = "ID") -> Tuple[bool, str]:
    """
    Valida que un ID sea un número positivo.
    
    Args:
        id_valor: Valor del ID
        campo: Nombre del campo
        
    Returns:
        Tupla (es_valido: bool, mensaje_error: str)
    """
    try:
        id_num = int(id_valor)
        
        if id_num <= 0:
            return False, f"El {campo} debe ser un número positivo mayor a 0"
        
        return True, ""
    except (ValueError, TypeError):
        return False, f"El {campo} debe ser un número válido"


# ============================================
# VALIDACIONES COMBINADAS
# ============================================

def validar_credenciales_registro(email: str, password: str, nombre: str) -> Tuple[bool, str]:
    """
    Valida credenciales para registro de usuario.
    
    Args:
        email: Email del usuario
        password: Contraseña
        nombre: Nombre completo
        
    Returns:
        Tupla (es_valido: bool, mensaje_error: str)
    """
    # Validar email
    es_valido, mensaje = validar_email(email)
    if not es_valido:
        return False, mensaje
    
    # Validar password
    es_valido, mensaje = validar_password(password)
    if not es_valido:
        return False, mensaje
    
    # Validar nombre
    es_valido, mensaje = validar_nombre(nombre, "nombre completo")
    if not es_valido:
        return False, mensaje
    
    return True, ""


def validar_credenciales_login(email: str, password: str) -> Tuple[bool, str]:
    """
    Valida credenciales para login (validación básica).
    
    Args:
        email: Email del usuario
        password: Contraseña
        
    Returns:
        Tupla (es_valido: bool, mensaje_error: str)
    """
    # Validar que no estén vacíos
    if not email or not email.strip():
        return False, "El email es obligatorio"
    
    if not password:
        return False, "La contraseña es obligatoria"
    
    return True, ""


# ============================================
# FUNCIÓN AUXILIAR
# ============================================

def limpiar_texto(texto: str) -> str:
    """
    Limpia un texto eliminando espacios extra.
    
    Args:
        texto: Texto a limpiar
        
    Returns:
        Texto limpio
    """
    if not texto:
        return ""
    return texto.strip()
