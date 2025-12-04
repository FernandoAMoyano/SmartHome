"""
Utilidades Rich para la interfaz de usuario.

Este módulo centraliza todas las configuraciones y funciones
relacionadas con Rich para mantener consistencia visual.
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich import box
from rich.progress import Progress, SpinnerColumn, TextColumn
import time


# ============================================
# CONFIGURACIÓN GLOBAL
# ============================================

console = Console()

# Colores del tema SmartHome
COLORS = {
    "primary": "cyan",
    "success": "green",
    "error": "red",
    "warning": "yellow",
    "info": "blue",
    "accent": "magenta",
    "muted": "bright_black",
}

# Iconos
ICONS = {
    "home": "🏠",
    "device": "📱",
    "automation": "🤖",
    "user": "👤",
    "admin": "👑",
    "settings": "⚙️",
    "success": "✅",
    "error": "❌",
    "warning": "⚠️",
    "info": "ℹ️",
    "exit": "🚪",
    "edit": "✏️",
    "delete": "🗑️",
    "add": "➕",
    "view": "👁️",
    "active": "🟢",
    "inactive": "🔴",
    "standby": "🟡",
}


# ============================================
# FUNCIONES DE UTILIDAD
# ============================================


def clear_screen():
    """Limpia la pantalla de forma elegante."""
    console.clear()


def print_header(title: str, subtitle: str = ""):
    """
    Imprime un encabezado estilizado.

    Args:
        title: Título principal
        subtitle: Subtítulo opcional
    """
    content = f"[bold white]{title}[/bold white]"
    if subtitle:
        content += f"\n[dim]{subtitle}[/dim]"

    panel = Panel(
        content, border_style=COLORS["primary"], box=box.DOUBLE, padding=(1, 2)
    )
    console.print(panel)


def print_divider(char: str = "─", color: str = "cyan"):
    """Imprime un divisor visual."""
    console.print(f"[{color}]{char * console.width}[/{color}]")


def print_success(message: str):
    """Imprime mensaje de éxito."""
    console.print(
        f"{ICONS['success']} [bold {COLORS['success']}]{message}[/bold {COLORS['success']}]"
    )


def print_error(message: str):
    """Imprime mensaje de error."""
    console.print(
        f"{ICONS['error']} [bold {COLORS['error']}]{message}[/bold {COLORS['error']}]"
    )


def print_warning(message: str):
    """Imprime mensaje de advertencia."""
    console.print(
        f"{ICONS['warning']} [bold {COLORS['warning']}]{message}[/bold {COLORS['warning']}]"
    )


def print_info(message: str):
    """Imprime mensaje informativo."""
    console.print(
        f"{ICONS['info']} [bold {COLORS['info']}]{message}[/bold {COLORS['info']}]"
    )


def ask_input(prompt: str, password: bool = False) -> str:
    """
    Solicita input del usuario con estilo.

    Args:
        prompt: Texto del prompt
        password: Si es True, oculta el input (para contraseñas)

    Returns:
        String ingresado por el usuario
    """
    if password:
        return Prompt.ask(
            f"[bold {COLORS['primary']}]{prompt}[/bold {COLORS['primary']}]",
            password=True,
        )
    else:
        return Prompt.ask(
            f"[bold {COLORS['primary']}]{prompt}[/bold {COLORS['primary']}]"
        )


def ask_choice(prompt: str, choices: list, default: str = None) -> str:
    """
    Solicita una opción del usuario con validación.

    Args:
        prompt: Texto del prompt
        choices: Lista de opciones válidas
        default: Opción por defecto

    Returns:
        Opción seleccionada
    """
    return Prompt.ask(
        f"[bold {COLORS['accent']}]{prompt}[/bold {COLORS['accent']}]",
        choices=choices,
        default=default,
    )


def ask_confirm(prompt: str, default: bool = False) -> bool:
    """
    Solicita confirmación del usuario.

    Args:
        prompt: Texto del prompt
        default: Valor por defecto

    Returns:
        True si confirma, False si no
    """
    return Confirm.ask(
        f"[bold {COLORS['warning']}]{prompt}[/bold {COLORS['warning']}]",
        default=default,
    )


def show_loading(message: str, duration: float = 1.0):
    """
    Muestra un spinner de carga.

    Args:
        message: Mensaje a mostrar
        duration: Duración en segundos
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description=message, total=None)
        time.sleep(duration)


def pause(message: str = "Presione Enter para continuar..."):
    """Pausa la ejecución hasta que el usuario presione Enter."""
    console.input(f"\n[dim]{message}[/dim]")


def create_menu_panel(title: str, options: list, icon: str = ICONS["home"]) -> Panel:
    """
    Crea un panel de menú estilizado.

    Args:
        title: Título del menú
        options: Lista de tuplas (número, texto, icono)
        icon: Icono del título

    Returns:
        Panel de Rich con el menú
    """
    # Construir contenido del menú
    menu_lines = []
    for num, text, opt_icon in options:
        menu_lines.append(
            f"[{COLORS['accent']}][{num}][/{COLORS['accent']}] {opt_icon} {text}"
        )

    content = "\n".join(menu_lines)

    return Panel(
        content,
        title=f"{icon} {title}",
        border_style=COLORS["primary"],
        box=box.ROUNDED,
        padding=(1, 2),
    )


def create_data_table(
    title: str, columns: list, rows: list, show_header: bool = True
) -> Table:
    """
    Crea una tabla de datos estilizada.

    Args:
        title: Título de la tabla
        columns: Lista de tuplas (nombre, estilo, justify)
        rows: Lista de listas con los datos
        show_header: Si mostrar encabezado

    Returns:
        Tabla de Rich
    """
    table = Table(
        title=title,
        box=box.ROUNDED,
        show_header=show_header,
        header_style=f"bold {COLORS['accent']}",
    )

    # Agregar columnas
    for col_name, col_style, col_justify in columns:
        table.add_column(col_name, style=col_style, justify=col_justify)

    # Agregar filas
    for row in rows:
        table.add_row(*row)

    return table


def get_state_icon(state_name: str) -> str:
    """
    Retorna el icono y color según el estado.

    Args:
        state_name: Nombre del estado

    Returns:
        String con icono coloreado
    """
    state_lower = state_name.lower()

    if "encendido" in state_lower or "activo" in state_lower or "on" in state_lower:
        return f"[{COLORS['success']}]●[/{COLORS['success']}] {state_name}"
    elif "apagado" in state_lower or "inactivo" in state_lower or "off" in state_lower:
        return f"[{COLORS['error']}]●[/{COLORS['error']}] {state_name}"
    else:
        return f"[{COLORS['warning']}]●[/{COLORS['warning']}] {state_name}"


def show_welcome_banner():
    """Muestra un banner de bienvenida al sistema."""
    clear_screen()

    banner = f"""
[bold {COLORS["primary"]}]╔═══════════════════════════════════════════════════════════════════════════════╗[/bold {COLORS["primary"]}]
[bold {COLORS["primary"]}]║                                                                               ║[/bold {COLORS["primary"]}]
[bold {COLORS["primary"]}]║                             {ICONS["home"]}SISTEMA SMARTHOME{ICONS["home"]}                             ║[/bold {COLORS["primary"]}]                                                                                 
[bold {COLORS["primary"]}]║                          Gestión Inteligente del Hogar                        ║[/bold {COLORS["primary"]}]
[bold {COLORS["primary"]}]║                                                                               ║[/bold {COLORS["primary"]}]
[bold {COLORS["primary"]}]╚═══════════════════════════════════════════════════════════════════════════════╝[/bold {COLORS["primary"]}]
    """

    console.print(banner)
    console.print()


# ============================================
# EXPORTACIONES
# ============================================

__all__ = [
    "console",
    "COLORS",
    "ICONS",
    "clear_screen",
    "print_header",
    "print_divider",
    "print_success",
    "print_error",
    "print_warning",
    "print_info",
    "ask_input",
    "ask_choice",
    "ask_confirm",
    "show_loading",
    "pause",
    "create_menu_panel",
    "create_data_table",
    "get_state_icon",
    "show_welcome_banner",
]
