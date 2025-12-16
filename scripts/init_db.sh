#!/bin/bash
# ==============================================================================
# Script de inicialización de base de datos SmartHome
# Para Linux / macOS
# ==============================================================================

echo "=========================================="
echo "  SmartHome - Inicialización de BD"
echo "=========================================="
echo ""

# Verificar que Python esté instalado
if ! command -v python3 &> /dev/null; then
    echo "✗ Python3 no encontrado. Por favor, instálalo primero."
    exit 1
fi

# Ejecutar setup completo
python3 database/setup_database.py --all

# Verificar resultado
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Base de datos inicializada correctamente"
    echo ""
    echo "Puedes ejecutar la aplicación con:"
    echo "  python3 main.py"
else
    echo ""
    echo "✗ Hubo un error en la inicialización"
    exit 1
fi
