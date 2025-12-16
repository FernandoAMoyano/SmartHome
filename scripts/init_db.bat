@echo off
REM ==============================================================================
REM Script de inicialización de base de datos SmartHome
REM Para Windows
REM ==============================================================================

echo ==========================================
echo   SmartHome - Inicialización de BD
echo ==========================================
echo.

REM Verificar que Python esté instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python no encontrado. Por favor, instalalo primero.
    pause
    exit /b 1
)

REM Ejecutar setup completo
python database\setup_database.py --all

REM Verificar resultado
if %errorlevel% equ 0 (
    echo.
    echo OK Base de datos inicializada correctamente
    echo.
    echo Puedes ejecutar la aplicacion con:
    echo   python main.py
) else (
    echo.
    echo X Hubo un error en la inicializacion
    pause
    exit /b 1
)

pause
