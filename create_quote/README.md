# Create Quote - TrackHS PMS Integration

## 🎯 Descripción Rápida
Crea cotizaciones de reserva en TrackHS PMS con precios, tarifas, impuestos y políticas. Genera quotes detallados para unidades específicas con fechas de entrada/salida y configuración de ocupantes.

## 📁 Archivos

1. **create_quote.json** - Blueprint de Make.com (herramienta completa)
2. **create_quote.md** - Documentación oficial detallada
3. **descripcion.txt** - Descripción breve (<240 caracteres)

## 🐛 Error Solucionado

### Problema Original
```
Cannot initialize the scenario because of the reason 'Invalid value "" of variable rateTypeId. Type number expected.'
```

### Causa
Los campos opcionales usaban `{{ifempty(var.input.campo; null)}}` que convertía valores vacíos en cadenas `""` en lugar de omitirlos.

### Solución Aplicada ✅
Cambio de:
```javascript
"value": "{{ifempty(var.input.rateTypeId; null)}}"
```

A:
```javascript
"value": "{{var.input.rateTypeId}}"
```

**Resultado**: Make.com ahora omite automáticamente los parámetros vacíos en los query strings, evitando errores de tipo.

## 🚀 Uso Rápido

### Entrada Mínima
```json
{
  "unitId": 199,
  "arrivalDate": "2024-12-25",
  "departureDate": "2024-12-28"
}
```

### Salida Esperada
```json
{
  "isValid": true,
  "isAvailable": true,
  "total": "1250.00",
  "currency": "USD",
  "grossRent": "1000.00",
  "totalTaxes": "150.00",
  "totalGuestFees": "100.00",
  ...
}
```

## 🔧 Integración en Make.com

1. Importar el blueprint desde `create_quote.json`
2. Configurar las credenciales de autenticación (var.auth.user y var.auth.pass)
3. Conectar con el flujo existente
4. Los campos opcionales se omitirán automáticamente si están vacíos

## 📋 Campos Principales

### Obligatorios
- `unitId` (number) - ID de la unidad
- `arrivalDate` (text) - Fecha de llegada (YYYY-MM-DD)
- `departureDate` (text) - Fecha de salida (YYYY-MM-DD)

### Opcionales Comunes
- `rateTypeId` (number) - Tipo de tarifa
- `occupants` (JSON string) - Configuración de ocupantes
- `channelId` (number) - Canal de venta
- `contactId` (number) - Contacto asociado
- `discount` (number) - Descuento aplicado

## ⚠️ Notas Importantes

1. **Formato de Fechas**: Usar ISO 8601 (YYYY-MM-DD)
2. **Arrays JSON**: Pasar como strings con JSON válido
3. **Tipos de Datos**: Respetar los tipos declarados en la especificación
4. **Campos Vacíos**: NO usar `ifempty` - dejar que Make.com los maneje
5. **Validación**: Siempre verificar `isValid` en la respuesta

## 🔗 API Endpoint
```
POST https://ihmvacations.trackhs.com/api/v2/pms/quotes
```

## 📚 Documentación Completa
Ver `create_quote.md` para la documentación detallada de todos los parámetros y respuestas.

