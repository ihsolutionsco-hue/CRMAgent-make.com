# Create Contact Collection - Mock Testing

Este proyecto incluye un servidor mock y tests de validación para la API de TrackHS CRM - Create Contact, permitiendo testear localmente sin afectar la base de datos real.

## 🎯 Objetivo

Validar que las requests y respuestas cumplan con la documentación OpenAPI sin hacer llamadas a la API real.

## 📋 Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## 🚀 Instalación

1. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## 🧪 Uso

### Opción 1: Ejecutar todo automáticamente (Recomendado)

Ejecuta el script que inicia el servidor y los tests automáticamente:

```bash
python run_tests.py
```

Este script:
- Inicia el servidor mock automáticamente
- Espera a que esté listo
- Ejecuta todos los tests
- Detiene el servidor al finalizar

### Opción 2: Manual (dos terminales)

#### 1. Iniciar el Servidor Mock

En una terminal, ejecuta:

```bash
python mock_server.py
```

El servidor se iniciará en `http://localhost:5000`

#### 2. Ejecutar Tests

En otra terminal, ejecuta:

```bash
python test_create_contact.py
```

Los tests validarán:
- ✅ Casos válidos según la documentación
- ❌ Validaciones de campos (emails, teléfonos, fechas, etc.)
- ✅ Estructura de respuestas según OpenAPI
- ✅ Diferentes formatos de envío (JSON body y query parameters)

## 📁 Estructura de Archivos

```
create contact collection/
├── create contact collection.json  # Configuración de Make.com
├── createContact.md                 # Documentación OpenAPI
├── mock_server.py                   # Servidor mock Flask
├── test_create_contact.py          # Tests de validación
├── run_tests.py                     # Script para ejecutar todo automáticamente
├── requirements.txt                 # Dependencias Python
└── README.md                        # Este archivo
```

## 🔍 Validaciones Implementadas

El servidor mock valida:

### Campos Requeridos
- Al menos uno de: `cellPhone`, `homePhone`, `otherPhone`, `primaryEmail`, `secondaryEmail`

### Validaciones de Formato
- **Emails**: Formato válido y máximo 100 caracteres
- **Teléfonos**: Formato E.164 y máximo 16 caracteres
- **Fechas** (anniversary, birthdate): Formato MM-DD
- **Country**: Código ISO de 2 caracteres
- **ACH Routing Number**: Exactamente 9 dígitos

### Validaciones de Longitud
- `firstName`, `lastName`: Máximo 32 caracteres
- `streetAddress`, `extendedAddress`: Máximo 255 caracteres
- `postalCode`: Máximo 16 caracteres
- `notes`: Máximo 4000 caracteres
- `taxId`: Máximo 16 caracteres

### Validaciones de Estructura
- `tags`: Array de objetos con campo `id` numérico
- `references`: Array de objetos
- `customValues`: Objeto con valores string o array

## 📊 Respuesta Mock

El servidor genera respuestas que cumplen con el esquema OpenAPI:

```json
{
  "id": 1,
  "firstName": "Juan",
  "lastName": "Pérez",
  "primaryEmail": "juan.perez@example.com",
  "createdAt": "2024-01-15T10:30:00Z",
  "updatedAt": "2024-01-15T10:30:00Z",
  "_links": {
    "self": {
      "href": "/api/crm/contacts/1"
    }
  },
  ...
}
```

## ⚠️ Notas Importantes

1. **No se persisten datos**: El servidor mock es solo para testing. Los datos se generan en memoria y no se guardan.

2. **IDs incrementales**: Cada contacto creado recibe un ID incremental (1, 2, 3...).

3. **Autenticación**: El servidor mock acepta cualquier usuario/contraseña para facilitar testing.

4. **Formato Make.com**: El servidor soporta tanto JSON body como query parameters (como lo usa Make.com).

## 🔧 Configuración

Puedes cambiar el puerto del servidor mock editando `mock_server.py`:

```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

Y actualizar la URL en `test_create_contact.py`:

```python
MOCK_SERVER_URL = os.getenv('MOCK_SERVER_URL', 'http://localhost:5000')
```

## 📝 Casos de Prueba

Los tests incluyen:

1. ✅ Caso básico válido
2. ✅ Caso completo con todos los campos
3. ❌ Email inválido
4. ❌ Teléfono inválido
5. ❌ Faltan campos requeridos
6. ❌ Fecha inválida
7. ❌ Country code inválido
8. ❌ ACH routing number inválido
9. ❌ Longitud máxima excedida
10. ✅ Query parameters (formato Make.com)
11. ✅ Solo email (sin teléfono)
12. ✅ Solo teléfono (sin email)

## 🐛 Troubleshooting

### Error: "No se pudo conectar al servidor mock"
- Asegúrate de que el servidor mock esté corriendo (`python mock_server.py`)
- Verifica que el puerto 5000 esté disponible

### Error: "ModuleNotFoundError"
- Ejecuta `pip install -r requirements.txt` para instalar las dependencias

## 📚 Referencias

- Documentación OpenAPI: `createContact.md`
- Especificación Make.com: `create contact collection.json`

