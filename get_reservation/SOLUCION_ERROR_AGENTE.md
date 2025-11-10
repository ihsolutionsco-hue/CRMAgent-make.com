# Solución: Error "Array must contain at least 1 element(s)" en outputParserFormat.schema

## Problema

Cuando intentas usar el agente de reservas (`s3398847_reservations_agent_booking_operations`) en Make.com, recibes el siguiente error:

```json
{
  "error": {
    "message": "400 | Validation error",
    "code": "too_small",
    "minimum": 1,
    "type": "array",
    "path": ["config", "outputParserFormat", "schema"],
    "detail": "Array must contain at least 1 element(s)"
  }
}
```

**Causa**: El agente tiene configurado un `outputParserFormat` con un schema vacío. Make.com requiere que el schema sea un array con al menos 1 elemento.

## Solución

### Opción A: Configurar Schema Estructurado (Recomendado)

1. Abre tu scenario en Make.com: `s3398847_reservations_agent_booking_operations`

2. Localiza el módulo **"Run an AI Agent"** (módulo del agente de reservas)

3. En la configuración del módulo, busca la sección **"Output Parser Format"** o **"Output Schema"**

4. Configura el schema con la siguiente estructura:

```json
{
  "outputParserFormat": {
    "type": "structured",
    "schema": [
      {
        "name": "reservation_id",
        "type": "string",
        "description": "ID de la reserva"
      },
      {
        "name": "guest_name",
        "type": "string",
        "description": "Nombre del huésped principal"
      },
      {
        "name": "check_in",
        "type": "string",
        "description": "Fecha de check-in en formato YYYY-MM-DD"
      },
      {
        "name": "check_out",
        "type": "string",
        "description": "Fecha de check-out en formato YYYY-MM-DD"
      },
      {
        "name": "status",
        "type": "string",
        "description": "Estado de la reserva: Hold, Confirmed, Checked In, Checked Out, Cancelled"
      },
      {
        "name": "total_amount",
        "type": "number",
        "description": "Monto total de la reserva"
      },
      {
        "name": "unit_id",
        "type": "integer",
        "description": "ID de la unidad reservada"
      },
      {
        "name": "nights",
        "type": "number",
        "description": "Número de noches de la reserva"
      },
      {
        "name": "currency",
        "type": "string",
        "description": "Moneda de la reserva (ej: USD, EUR)"
      }
    ]
  }
}
```

5. **En la interfaz de Make.com**, esto se configura así:
   - En el campo **"Output schema"**, selecciona **"Make Schema"**
   - En **"Output structure"**, agrega los siguientes campos:
     - `reservation_id` (text)
     - `guest_name` (text)
     - `check_in` (text)
     - `check_out` (text)
     - `status` (text)
     - `total_amount` (number)
     - `unit_id` (number)
     - `nights` (number)
     - `currency` (text)

6. Guarda los cambios y prueba el agente nuevamente.

### Opción B: Schema Mínimo (Solución Rápida)

Si solo necesitas que el agente funcione sin estructura específica, configura un schema mínimo:

```json
{
  "outputParserFormat": {
    "type": "structured",
    "schema": [
      {
        "name": "response",
        "type": "string",
        "description": "Respuesta del agente sobre la reserva"
      }
    ]
  }
}
```

En Make.com:
- **Output schema**: "Make Schema"
- **Output structure**: Agregar un campo `response` de tipo `text`

### Opción C: Remover Output Parser (No Recomendado)

Si no necesitas parseo estructurado:

1. En el módulo **"Run an AI Agent"**, cambia **"Output schema"** a **"Text"**
2. Esto eliminará la validación del schema, pero perderás la estructura de datos

**Nota**: Esta opción no es recomendada porque dificulta el procesamiento posterior de la respuesta.

## Verificación

Después de aplicar la solución:

1. **Test con reserva conocida**: `37166708`
2. **Verificar respuesta**: Debe incluir los campos configurados en el schema
3. **Validar threadID**: Debe persistir para conversaciones de seguimiento
4. **Medir latencia**: Target <5 segundos

## Schema Completo (Opcional)

Si necesitas más campos de la reserva, puedes expandir el schema con:

```json
{
  "name": "contact_id",
  "type": "integer",
  "description": "ID del contacto/huésped"
},
{
  "name": "arrival_time",
  "type": "string",
  "description": "Hora de llegada en formato ISO 8601"
},
{
  "name": "departure_time",
  "type": "string",
  "description": "Hora de salida en formato ISO 8601"
},
{
  "name": "occupants",
  "type": "text",
  "description": "Información de ocupantes (adultos, niños, mascotas)"
},
{
  "name": "balance",
  "type": "number",
  "description": "Saldo pendiente de la reserva"
},
{
  "name": "payment_status",
  "type": "string",
  "description": "Estado de los pagos"
}
```

## Referencias

- Archivo de schema completo: `reservation_agent_schema.json`
- Documentación de la API: `get reservation v2.md`
- Blueprint del agente: `Reservations Agent con webhook.blueprint.json`

## Prevención

Para evitar este error en el futuro:

1. **Validar schemas antes de deploy**: Asegúrate de que todos los agentes tengan schemas válidos
2. **Testing**: Prueba cada agente después de cambios de configuración
3. **Documentación**: Mantén documentación actualizada de la configuración de cada agente


