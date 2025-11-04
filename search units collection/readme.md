# TrackHS API - Make.com Blueprint

Blueprint para Make.com que integra la API de TrackHS Unit Collection (`GET /api/pms/units`).

## Archivo Principal

- **Blueprint JSON**: `search units collection.json`
- **Documentación OpenAPI**: `search units collection.md`

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

- **`page`**: Página basada en 1 (mínimo 1). `page=0` devuelve 400 Bad Request
- **`size`**: Tamaño de página (recomendado: 1-5, máximo API: 100)
- **Para grandes volúmenes**: Usar paginación (múltiples llamadas con `page` incrementando)

## 🔧 Parámetros Disponibles

### Filtros de Búsqueda

- **`search`**: Búsqueda por subcadena en nombre o descripciones
- **`term`**: Búsqueda por subcadena en término
- **`unitCode`**: Búsqueda por código de unidad. Coincidencia exacta o agregar `%` para wildcard
- **`shortName`**: Búsqueda por nombre corto. Coincidencia exacta o agregar `%` para wildcard

### Filtros por IDs (CSV para múltiples valores)

- **`nodeId`**: Node ID(s) - Devuelve unidades descendientes del nodo específico
- **`amenityId`**: Amenity ID(s) - Devuelve unidades con estos amenity IDs
- **`unitTypeId`**: Unit Type ID(s) - Devuelve unidades del tipo específico
- **`id`**: Unit ID(s) - Array de IDs de unidades específicas
- **`calendarId`**: Calendar ID - Devuelve unidades del tipo que coinciden con este calendar group id
- **`roleId`**: Role ID - Devuelve unidades por roleId específico

### Filtros de Fecha

- **`contentUpdatedSince`**: Fecha en formato ISO 8601 (date-time)
  - Ejemplo: `contentUpdatedSince=2025-01-01T00:00:00Z`
  - Devuelve unidades con cambios de contenido desde esta fecha
- **`arrival`**: Fecha en formato YYYY-MM-DD (solo fecha, no date-time)
  - Ejemplo: `arrival=2025-10-27`
  - Devuelve unidades disponibles entre `arrival` y `departure`
- **`departure`**: Fecha en formato YYYY-MM-DD (solo fecha, no date-time)
  - Ejemplo: `departure=2025-10-31`
  - Devuelve unidades disponibles entre `arrival` y `departure`

⚠️ **IMPORTANTE**: `arrival` y `departure` usan formato `date` (YYYY-MM-DD), no `date-time`. La API puede ignorar formatos ISO-8601 completos para estos parámetros.

### Filtros de Características

#### Dormitorios

- **`minBedrooms`**: Devuelve unidades con este número o más de dormitorios
- **`maxBedrooms`**: Devuelve unidades con este número o menos de dormitorios
- **`bedrooms`**: Devuelve unidades con este número exacto de dormitorios

#### Baños

- **`minBathrooms`**: Devuelve unidades con este número o más de baños
- **`maxBathrooms`**: Devuelve unidades con este número o menos de baños
- **`bathrooms`**: Devuelve unidades con este número exacto de baños

### Filtros Booleanos

Los valores booleanos en la API de units aceptan `1` o `0` (no `true`/`false`):

- **`petsFriendly`**: Devuelve unidades que permiten mascotas. Valores: `1` (sí) o `0` (no)
- **`allowUnitRates`**: Devuelve unidades cuyo tipo permite tarifas de unidad. Valores: `1` (sí) o `0` (no)
- **`computed`**: Devuelve atributos adicionales computados basados en atributos heredados. Valores: `1` (sí) o `0` (no)
- **`inherited`**: Devuelve atributos adicionales heredados. Valores: `1` (sí) o `0` (no)
- **`limited`**: Devuelve atributos muy limitados (id, name, longitude, latitude, isActive). Valores: `1` (sí) o `0` (no)
- **`isBookable`**: Devuelve unidades reservables. Valores: `1` (sí) o `0` (no)
- **`includeDescriptions`**: Devuelve descripciones de unidades, pueden ser heredadas del nodo si se establece en inherited. Valores: `1` (sí) o `0` (no). Si se usan channel keys, las descripciones siempre se devuelven
- **`isActive`**: Devuelve unidades activas (`1`), inactivas (`0`), o todas (`null`)

### Filtros de Estado

- **`unitStatus`**: Filtrar por estado de unidad
  - Valores permitidos: `clean`, `dirty`, `occupied`, `inspection`, `inprogress`

### Paginación

- **`mode`**: `"page"` o `"scroll"` (default: `"page"`)
- **`page`**: Número de página cuando `mode=page` (default: 1)
- **`size`**: Tamaño de página cuando `mode=page` (default: 5)
- **`scroll`**: Token/índice para scroll pagination cuando `mode=scroll`
- **`sortColumn`**: Columna para ordenar (solo `mode=page`)
  - Valores permitidos: `id`, `name`, `nodeName`, `unitTypeName`
- **`sortDirection`**: `"asc"` o `"desc"` (solo `mode=page`, default: `"asc"`)

## 📊 Estructura de Respuesta

La respuesta incluye:

- **`units`**: Array de unidades con información detallada
- **`page`**: Página actual
- **`page_count`**: Total de páginas
- **`page_size`**: Tamaño de página
- **`total_items`**: Total de items
- **`next_href`**: Siguiente enlace (para scroll/paginación)

### Campos Disponibles en Cada Unidad

#### ✅ Campos Seguros para Servicio al Cliente

**Información básica:**
- `id`, `name`, `shortName`, `unitCode`, `headline`

**Ubicación general (sin direcciones específicas):**
- `locality` (ciudad)
- `region` (estado/provincia)
- `country` (país)
- `timezone`

**Características físicas:**
- `bedrooms`, `fullBathrooms`, `halfBathrooms`, `maxOccupancy`, `area`, `floors`

**Información de check-in/checkout:**
- `checkinTime`, `checkoutTime`, `timezone`
- `hasEarlyCheckin`, `earlyCheckinTime`
- `hasLateCheckout`, `lateCheckoutTime`

**Políticas y reglas:**
- `petsFriendly`, `maxPets`, `smokingAllowed`, `childrenAllowed`
- `minimumAgeLimit`, `isAccessible`, `houseRules`

**Amenities:**
- `amenities` (array con objetos `{id, name, group}`)
- `amenityDescription`

**Descripciones:**
- `shortDescription`, `longDescription`, `headline`

**Estado y disponibilidad:**
- `isBookable`, `isActive`, `unitStatus`

**Información de contacto:**
- `phone`, `website` (si es público)

**Tipos:**
- `lodgingType` (objeto con `id`, `name`)
- `unitType` (objeto con `id`, `name`)

#### ⚠️ Campos Excluidos por Seguridad

**NO usar estos campos en servicio al cliente:**
- `streetAddress` - Dirección exacta de la calle
- `extendedAddress` - Dirección extendida
- `postal` - Código postal
- `latitude`, `longitude` - Coordenadas exactas
- `directions` - Instrucciones de cómo llegar
- `localOffice` - Información de oficina local

Estos campos están presentes en la respuesta de la API pero **NO deben ser utilizados ni mostrados a clientes** por razones de seguridad y privacidad.

## 🔍 Ejemplos de Uso

### Ejemplo 1: Buscar unidades activas con 3 dormitorios

```
GET /api/pms/units?isActive=1&bedrooms=3&page=1&size=5
```

### Ejemplo 2: Buscar unidades disponibles en un rango de fechas

```
GET /api/pms/units?arrival=2025-10-27&departure=2025-10-31&isBookable=1
```

### Ejemplo 3: Buscar unidades que permiten mascotas en un nodo específico

```
GET /api/pms/units?nodeId=81&petsFriendly=1&page=1&size=10
```

### Ejemplo 4: Buscar unidades con amenities específicas

```
GET /api/pms/units?amenityId=4,16,120&includeDescriptions=1
```

### Ejemplo 5: Buscar unidades por código o nombre corto

```
GET /api/pms/units?unitCode=TH444
GET /api/pms/units?shortName=TH%
```

## 📝 Notas de Implementación

- El blueprint está optimizado para evitar exceder el límite de tokens de Make.com
- Se recomienda usar `size=1-5` para respuestas grandes
- Los filtros booleanos usan `1` o `0`, no `true`/`false`
- Los filtros `arrival` y `departure` usan formato fecha (YYYY-MM-DD), no date-time
- Para grandes volúmenes de datos, implementar paginación en Make.com con múltiples llamadas
- El parámetro `limited=1` puede ser útil para obtener solo información básica de unidades

## 🐛 Solución de Problemas

### Error 403 Forbidden

- Verifica que las credenciales de autenticación estén correctamente configuradas en Make.com
- Asegúrate de que tu usuario de TrackHS tenga permisos para acceder a la API de units

### Error 400 Bad Request

- Verifica que `page` no sea 0 (debe ser >= 1)
- Verifica que `size` no exceda 100
- Verifica que los formatos de fecha sean correctos (YYYY-MM-DD para `arrival`/`departure`)

### Error de límite de tokens

- Reduce el valor de `size` a 1-5
- Considera usar `limited=1` para obtener solo información básica
- Implementa paginación para procesar grandes volúmenes en múltiples llamadas

## 📚 Referencias

- Documentación OpenAPI completa: `search units collection.md`
- API de TrackHS: https://support.trackhs.com

