# Search Reservations V2

Blueprint para Make.com que integra la API de TrackHS Search Reservations V2 (`GET /api/v2/pms/reservations`).

## Archivo Principal

- **Blueprint JSON**: `search_bookings.json`
- **Documentación OpenAPI**: `Search Reservations V2.md`

## ✅ Guía Rápida: Formatos de Fecha

### Tabla Comparativa de Formatos

| Parámetro | Formato ISO-8601 Completo | Formato Fecha Solo (YYYY-MM-DD) | Recomendación |
|-----------|---------------------------|--------------------------------|---------------|
| `bookedStart` / `bookedEnd` | ✅ Funciona | ✅ Funciona | **RECOMENDADO** - Usar cualquiera de los dos formatos |
| `arrivalStart` / `arrivalEnd` | ❌ **NO funciona** (API ignora) | ✅ Funciona | **SOLO usar formato fecha** (YYYY-MM-DD) |
| `departureStart` / `departureEnd` | ⚠️ Puede funcionar | ✅ Funciona | Si hay problemas, usar formato fecha |

### Resumen

**Los filtros `arrivalStart` y `arrivalEnd` SÍ funcionan, pero requieren formato de fecha sola (YYYY-MM-DD).**

- ✅ **Formato que FUNCIONA**: `YYYY-MM-DD` (solo fecha, sin hora)
  - Ejemplo: `arrivalStart=2025-10-27&arrivalEnd=2025-10-31`
  - Resultado: Filtra correctamente (495 items en pruebas)

- ❌ **Formato que NO funciona**: `YYYY-MM-DDTHH:MM:SSZ` (ISO-8601 completo)
  - Ejemplo: `arrivalStart=2025-10-27T00:00:00Z&arrivalEnd=2025-10-31T23:59:59Z`
  - Resultado: API ignora parámetros, devuelve todas las reservas (35,417 items en pruebas)

**Solución**: Si necesitas filtrar por hora específica, usa `bookedStart`/`bookedEnd` que aceptan ambos formatos.

### Ejemplos de Prueba Realizados

```bash
# Test 1: arrivalStart/arrivalEnd con ISO-8601 completo (NO funciona)
GET /api/v2/pms/reservations?arrivalStart=2025-10-05T15:32:41Z&arrivalEnd=2025-11-04T15:32:41Z
# Resultado: 35,417 items (ignora completamente los parámetros)

# Test 2: arrivalStart/arrivalEnd con formato fecha solo (SÍ funciona)
GET /api/v2/pms/reservations?arrivalStart=2025-10-05&arrivalEnd=2025-11-04
# Resultado: 495 items (filtra correctamente)

# Test 3: bookedStart/bookedEnd con ISO-8601 completo (SÍ funciona)
GET /api/v2/pms/reservations?bookedStart=2025-10-05T00:00:00Z&bookedEnd=2025-11-04T23:59:59Z
# Resultado: 751 items (funciona correctamente)

# Test 4: bookedStart/bookedEnd con formato fecha solo (SÍ funciona)
GET /api/v2/pms/reservations?bookedStart=2025-10-05&bookedEnd=2025-11-04
# Resultado: 767 items (funciona correctamente)
```

Ver `RESULTADOS_TEST_ARRIVAL.md` para más detalles de las pruebas realizadas.

## 📋 Configuración Importante

### 1. Autenticación en Make.com

El módulo HTTP debe tener configurado **Basic Authentication**:

- **Username**: Tu usuario de TrackHS
- **Password**: Tu contraseña de TrackHS

**Si recibes error 403 Forbidden**, verifica que las credenciales estén correctamente configuradas en el módulo HTTP de Make.com.

### 2. Límites de Make.com - CRÍTICO PARA AGENTES IA

- ⚠️ **Límite de tokens**: Make.com tiene un límite de **200,000 tokens por respuesta**
- 🚨 **CRÍTICO para agentes IA**: Usar `size=1-2` máximo (default: 2)
- 📦 **Tamaño de página recomendado**: 
  - Para agentes IA: `size=1-2` (default: 2)
  - Para uso directo: `size=1-5` (default: 5)
- ❌ **Tamaños grandes (3+) pueden causar error 400**: "This model's maximum context length is 200000 tokens"
- 💡 **Configuración del agente**:
  - Reducir "Maximum number of agent runs in thread history" a 3-5
  - Dejar Thread ID vacío si no necesitas historial
  - Establecer Max output tokens a 4,000-8,000

### 2.1 Optimización de Tokens para Agentes IA

Si estás usando esta herramienta con un agente de IA y recibes el error:
```
400 This model's maximum context length is 200000 tokens
```

**Soluciones inmediatas:**

1. **Reducir tamaño de página**:
   - Cambiar `size` de 5 a 1 o 2
   - Ejemplo: `size=1` o `size=2`

2. **Configurar el agente correctamente**:
   - En "Agent settings" → "Maximum number of agent runs in thread history": establecer a 3-5
   - En "Thread ID": dejar vacío si no necesitas historial
   - En "Max output tokens": establecer a 4,000-8,000

3. **Usar paginación**:
   - En lugar de `size=10`, usar múltiples llamadas con `size=2` y `page` incrementando
   - Ejemplo: `page=1&size=2`, luego `page=2&size=2`, etc.

4. **Filtrar antes de pasar al agente**:
   - Usar filtros específicos (fechas, estados, contactos) para reducir resultados
   - Ejemplo: `status=Confirmed&arrivalStart=2025-10-01&arrivalEnd=2025-10-31`

### 3. Paginación

- **`page`**: Página basada en 1 (mínimo 1). `page=0` devuelve 400 Bad Request
- **`size`**: Tamaño de página (recomendado: 1-2 para agentes IA, 1-5 para uso directo, máximo API: 100)
- **Para grandes volúmenes**: Usar paginación (múltiples llamadas con `page` incrementando)

## 🔧 Parámetros Disponibles

### Filtros de Fecha

#### Filtros Recomendados ✅

- **`bookedStart`**: Fecha inicio de reserva
  - Acepta: ISO-8601 completo (`2025-10-27T00:00:00Z`) o fecha sola (`2025-10-27`)
  - Funciona correctamente con ambos formatos
  - Ejemplo: `bookedStart=2025-10-27T00:00:00Z` o `bookedStart=2025-10-27`

- **`bookedEnd`**: Fecha fin de reserva
  - Acepta: ISO-8601 completo (`2025-10-31T23:59:59Z`) o fecha sola (`2025-10-31`)
  - Funciona correctamente con ambos formatos
  - Ejemplo: `bookedEnd=2025-10-31T23:59:59Z` o `bookedEnd=2025-10-31`

#### Filtros con Restricciones de Formato ⚠️

- **`arrivalStart`**: Fecha inicio de llegada
  - ⚠️ **SOLO funciona con formato fecha (YYYY-MM-DD)**
  - ✅ Correcto: `arrivalStart=2025-10-27`
  - ❌ Incorrecto: `arrivalStart=2025-10-27T00:00:00Z` (la API ignora este formato)
  - Si necesitas filtrar por hora, usa `bookedStart` en su lugar

- **`arrivalEnd`**: Fecha fin de llegada
  - ⚠️ **SOLO funciona con formato fecha (YYYY-MM-DD)**
  - ✅ Correcto: `arrivalEnd=2025-10-31`
  - ❌ Incorrecto: `arrivalEnd=2025-10-31T23:59:59Z` (la API ignora este formato)
  - Si necesitas filtrar por hora, usa `bookedEnd` en su lugar

- **`departureStart`** / **`departureEnd`**: Fechas de salida
  - Pueden tener comportamiento similar a `arrivalStart`/`arrivalEnd`
  - Si hay problemas, probar con formato fecha sola (YYYY-MM-DD)

### Otros Filtros

- **`search`**: Búsqueda por subcadena en nombre o descripciones
- **`status`**: Estado(s) de reserva. Valores: `Hold`, `Confirmed`, `Checked Out`, `Checked In`, `Cancelled`. CSV para múltiples valores
- **`updatedSince`**: Filtrar por actualizaciones desde fecha (ISO-8601). Ej: `2025-01-01T00:00:00Z`
- **`inHouseToday`**: Filtrar por in house hoy. Valores: `1` (Sí) o `0` (No)

### Filtros por ID (CSV para múltiples valores)

- `nodeId`: Node ID(s)
- `unitId`: Unit ID(s)
- `contactId`: Contact ID(s)
- `reservationTypeId`: Tipo de reserva ID(s)
- `travelAgentId`: Travel Agent ID(s)
- `userId`: User ID(s)
- `unitTypeId`: Unit Type ID(s)
- `rateTypeId`: Rate Type ID(s)
- `tags`: Tag ID(s)

### Paginación

- `mode`: `"page"` o `"scroll"` (default: `"page"`)
- `page`: Número de página cuando `mode=page` (default: 1)
- `size`: Tamaño de página cuando `mode=page` (default: 5)
- `scroll`: Token/índice para scroll pagination cuando `mode=scroll`
- `sortColumn`: Columna para ordenar (solo `mode=page`)
- `sortDirection`: `"asc"` o `"desc"` (solo `mode=page`)

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
- Los filtros `bookedStart`/`bookedEnd` son la alternativa recomendada a `arrivalStart`/`arrivalEnd`
- Para grandes volúmenes de datos, implementar paginación en Make.com con múltiples llamadas

## 🐛 Reporte de Problemas

Si encuentras problemas con la API de TrackHS, especialmente con los filtros `arrivalStart`/`arrivalEnd`, contacta al equipo de soporte de TrackHS con los detalles de las pruebas realizadas.
