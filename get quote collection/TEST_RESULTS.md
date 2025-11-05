# Resultados de Testing - Get Quote Collection V2

**Fecha:** 2025-11-04  
**Endpoint:** `GET /api/v2/pms/quotes`

## 🔍 Hallazgos Principales

### ❌ Errores en la Documentación OpenAPI

La documentación OpenAPI proporcionada tiene **errores importantes** que fueron detectados mediante testing con la API real:

#### 1. Parámetro `page`

**Documentación OpenAPI dice:**
- `minimum: 0`
- `maximum: 0`
- Solo acepta valor `0`

**Realidad de la API:**
- ❌ Rechaza `page=0` con error: `"Page must be a positive integer; received \"0\""`
- ✅ Acepta valores `page >= 1`
- ✅ Default: `page=1` (cuando no se envía)

**Corrección aplicada:**
- Validación: `if(page < 1) → page = 1`
- Default: `1` (no `0`)

#### 2. Campo de Respuesta `_embedded`

**Documentación OpenAPI dice:**
- Campo: `_embedded.amenities`

**Realidad de la API:**
- ✅ Campo real: `_embedded.quotes`
- ❌ No existe `_embedded.amenities`

**Corrección aplicada:**
- Cambiado de `_embedded.amenities` a `_embedded.quotes`

## ✅ Tests Exitosos

### Paginación
- ✅ `page=1` - Funciona correctamente
- ✅ `page=2` - Funciona correctamente (paginación)
- ❌ `page=0` - Rechazado con error 400
- ❌ `page=-1` - Rechazado con error 400

### Otros Parámetros
- ✅ `size` - Funciona correctamente
- ✅ `sortColumn` - Funciona (valores probados: `id`, `order`)
- ✅ `sortDirection` - Funciona (`asc`, `desc`)
- ✅ `search` - Funciona correctamente
- ✅ `contactId` - Funciona (aunque retornó 0 resultados)
- ✅ `futureQuotes` - Funciona (valores `1` y `0`)
- ✅ `activeQuotes` - Funciona

## 📊 Estadísticas de Tests

- **Total de tests:** 14
- **Exitosos:** 11
- **Fallidos:** 3 (todos relacionados con `page=0`)

## 🔧 Correcciones Implementadas

1. **Validación de `page`:**
   ```json
   "page": "{{if(var.input.page; if(var.input.page < 1; 1; var.input.page); 1)}}"
   ```

2. **Campo de respuesta:**
   ```json
   "quotes": "{{1.data.`_embedded`.quotes}}"
   ```

3. **Default de `page`:**
   - Cambiado de `0` a `1`

4. **Documentación actualizada:**
   - Notas sobre errores en OpenAPI
   - Help text corregido
   - Descripción actualizada

## 📝 Notas Importantes

1. **La API funciona correctamente** con valores estándar de paginación (1-based)
2. **La documentación OpenAPI tiene errores** que fueron corregidos basándose en el comportamiento real
3. **El campo `_embedded.quotes`** contiene el array de quotes (no `amenities`)
4. **Todos los parámetros opcionales** funcionan correctamente cuando se omiten

## 🎯 Conclusión

La implementación ha sido corregida para reflejar el comportamiento real de la API, corrigiendo los errores presentes en la documentación OpenAPI proporcionada.

