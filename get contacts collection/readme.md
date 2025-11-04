# TrackHS CRM API - Get Contacts Collection

Blueprint para Make.com que integra la API de TrackHS CRM (`GET /api/crm/contacts`).

## Archivo Principal

- **Blueprint JSON**: `get contacts collection.json`
- **Documentación OpenAPI**: `getContactsCollection.md`

## 📋 Configuración Importante

### 1. Autenticación en Make.com

El módulo HTTP debe tener configurado **Basic Authentication**:

- **Username**: Tu usuario de TrackHS
- **Password**: Tu contraseña de TrackHS

**Si recibes error 403 Forbidden**, verifica que las credenciales estén correctamente configuradas en el módulo HTTP de Make.com.

### 2. Límites de Make.com

- ⚠️ **Límite de tokens**: Make.com tiene un límite de **200,000 tokens por respuesta**
- 📦 **Tamaño de página recomendado**: `size=1-5` (default: 5)
- ❌ **Tamaños grandes (10+) pueden causar error 400**: "This model's maximum context length is 200000 tokens"

### 3. Paginación

- **`page`**: Página basada en 1 (mínimo 1)
- **`size`**: Tamaño de página (recomendado: 1-5, máximo API: según límites de la API)
- **Para grandes volúmenes**: Usar paginación (múltiples llamadas con `page` incrementando)

## 🔧 Parámetros Disponibles

### Búsqueda y Filtros

#### Parámetro Search (Búsqueda Avanzada)

El parámetro `search` tiene un comportamiento especial:

- **Separa por espacios**: Divide la búsqueda en palabras y hace AND entre ellas
- **Busca en múltiples campos**: first name, last name, email, mobile phone, home phone, other phone
- **Wildcard a la derecha**: Busca coincidencias que comiencen con el texto
- **Búsqueda numérica especial**:
  - Si el número empieza con `1`, busca ese número exacto
  - Si el número NO empieza con `1`, busca número con prefijo `1` (números guardados con 1 al inicio)

**Ejemplos**:
- `search=Griselda Peters` → Busca contactos que tengan "Griselda" en algún campo Y "Peters" en algún campo (no necesariamente el mismo)
- `search=1234567890` → Si empieza con 1, busca "1234567890"; si no, busca "11234567890"

**Nota**: Esta búsqueda puede tener falsos positivos. Por ejemplo, `search=Peter James` podría coincidir con:
- First name: "James", Last name: "Peter"
- First name: "Peter", Last name: "James"

Para reducir falsos positivos, incluye también el número de teléfono en la búsqueda.

#### Otros Parámetros de Búsqueda

- **`term`**: Localizar contacto basado en un valor preciso como ID o nombre
- **`email`**: Buscar contacto por email primario o secundario

### Filtros de Fecha

- **`updatedSince`**: Filtrar por actualizaciones desde fecha
  - ⚠️ **Formato requerido**: `YYYY-MM-DD` (formato date ISO 8601, NO date-time)
  - ✅ **Ejemplo válido**: `updatedSince=2025-01-01`
  - ❌ **Ejemplo inválido**: `updatedSince=2025-01-01T00:00:00Z` (no usar formato date-time)

### Ordenamiento

- **`sortColumn`**: Columna para ordenar
  - Valores permitidos: `id`, `name`, `email`, `cellPhone`, `homePhone`, `otherPhone`, `vip`
  - Default: `id`

- **`sortDirection`**: Dirección de ordenamiento
  - Valores: `asc` (ascendente) o `desc` (descendente)
  - Default: `asc`

### Paginación

- **`page`**: Número de página (default: 1)
- **`size`**: Tamaño de página (default: 5, recomendado: 1-5)

## 📊 Estructura de Respuesta

La respuesta incluye:

- **`contacts`**: Array de objetos contacto con información completa:
  - Información personal: `firstName`, `lastName`, `primaryEmail`, `secondaryEmail`
  - Teléfonos: `homePhone`, `cellPhone`, `workPhone`, `otherPhone`, `fax`
  - Dirección: `streetAddress`, `extendedAddress`, `locality`, `region`, `postalCode`, `country`
  - Información adicional: `notes`, `anniversary`, `birthdate`
  - Flags: `isVip`, `isBlacklist`, `noIdentity`
  - Tags: Array de tags asociados
  - Referencias: Array de referencias
  - Valores personalizados: `customValues`
  - Metadatos: `createdAt`, `updatedAt`, `createdBy`, `updatedBy`

- **`page`**: Página actual
- **`page_count`**: Total de páginas
- **`page_size`**: Tamaño de página
- **`total_items`**: Total de contactos
- **`next_href`**: Enlace para la siguiente página (si existe)

## 🔍 Testing Local

Si necesitas probar la API localmente, puedes crear un script Python simple:

```bash
# Instalar dependencias
pip install -r requirements.txt
```

Crea un archivo `.env` con:
```env
TRACKHS_API_URL=https://tu-dominio.trackhs.com
TRACKHS_USERNAME=tu_usuario
TRACKHS_PASSWORD=tu_contraseña
```

Luego crea un script de prueba para hacer llamadas a la API usando la librería `requests` con Basic Authentication.

## 📝 Notas de Implementación

- El blueprint está optimizado para evitar exceder el límite de tokens de Make.com
- Se recomienda usar `size=1-5` para respuestas grandes
- El parámetro `search` tiene comportamiento especial de búsqueda AND entre palabras
- Para grandes volúmenes de datos, implementar paginación en Make.com con múltiples llamadas
- El formato de fecha `updatedSince` debe ser `YYYY-MM-DD` (solo fecha, sin hora)

## 🐛 Reporte de Problemas

Si encuentras problemas con la API de TrackHS, contacta al equipo de soporte de TrackHS con los detalles de las pruebas realizadas.

## 🔗 Referencias

- **Endpoint**: `GET /api/crm/contacts`
- **API Base**: `https://ihmvacations.trackhs.com/api`
- **Documentación OpenAPI**: Ver `getContactsCollection.md`
- **Soporte TrackHS**: support@trackhs.com

