# Create Housekeeping Work Order Collection

Esta colección contiene el blueprint y herramientas de testing para crear órdenes de trabajo de housekeeping en TrackHS PMS.

## Archivos

- `Create Housekeeping Work Order (TrackHS PMS).blueprint.json` - Blueprint de Make.com
- `create housekeeping work order doc.md` - Documentación OpenAPI oficial
- `test_create_housekeeping.py` - Script de testing contra la API real
- `requirements.txt` - Dependencias de Python

## Testing

Para ejecutar los tests contra la API real:

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Configurar variables de entorno:
```bash
# Windows PowerShell
$env:TRACKHS_USER='tu_usuario'
$env:TRACKHS_PASSWORD='tu_password'

# Linux/Mac
export TRACKHS_USER='tu_usuario'
export TRACKHS_PASSWORD='tu_password'
```

3. Ejecutar tests:
```bash
python test_create_housekeeping.py
```

Los tests incluyen 5 casos de prueba con diferentes combinaciones de campos:
- Test 1: Caso básico con inspección
- Test 2: Caso con cleanTypeId
- Test 3: Caso con campos opcionales (comments, cost)
- Test 4: Caso con isTurn y chargeOwner
- Test 5: Caso completo con todos los campos

## Notas

- Ajusta los valores de `unitId`, `cleanTypeId`, `userId`, etc. según los datos disponibles en tu instancia de TrackHS.
- Los resultados de los tests se guardan automáticamente en un archivo JSON con timestamp.

