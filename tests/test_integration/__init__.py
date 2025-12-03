"""
Paquete de tests de integración.

Los tests de integración difieren de los unit tests en que:
- NO usan mocks para DAOs
- TOCAN la base de datos real
- Validan que múltiples capas funcionan juntas
- Son más lentos de ejecutar

Para ejecutar solo tests de integración:
    pytest tests/test_integration/ -v -m integration

Para excluir tests de integración (más rápido):
    pytest tests/ -v -m "not integration"
"""
