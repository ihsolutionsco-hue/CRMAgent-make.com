# Create Reservation - TrackHS PMS

Herramienta de Make.com para crear reservas en TrackHS PMS.

## Archivos

- `create reservation collection.json` - Configuración de Make.com
- `create reservation collection.md` - Documentación OpenAPI completa
- `description.md` - Descripción breve de la herramienta
- `mock_server.py` - Servidor mock para testing local
- `test_create_reservation.py` - Tests de validación
- `requirements.txt` - Dependencias de Python

## Instalación

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecutar el servidor mock

```bash
python mock_server.py
```

El servidor se iniciará en `http://localhost:5001`

## Testing

### Opción 1: Ejecutar tests automáticamente (recomendado)

```bash
python run_tests.py
```

Este script inicia el servidor mock automáticamente, ejecuta los tests y luego cierra el servidor.

### Opción 2: Ejecutar manualmente

1. En una terminal, iniciar el servidor mock:
```bash
python mock_server.py
```

2. En otra terminal, ejecutar los tests:
```bash
python test_create_reservation.py
```

## Casos de Prueba

Los tests incluyen:

1. **Caso básico válido** - Solo campos requeridos (unitId, arrivalDate, departureDate)
2. **Caso con contactId** - Usando ID de contacto existente
3. **Caso con contact** - Creando contacto nuevo con objeto JSON
4. **Caso completo** - Todos los campos opcionales incluidos
5. **Caso con breakdown** - Precios personalizados (Server Keys)
6. **Validaciones negativas** - Tests que deben fallar:
   - Falta unitId
   - Falta arrivalDate
   - Falta departureDate
   - Fecha inválida
   - departureDate antes de arrivalDate
   - Status inválido
   - Contact sin identificadores
   - PromoCode muy largo
7. **Caso con payment** - Usando tarjeta de crédito
8. **Caso con bankAccount** - Usando cuenta bancaria
9. **Reservas múltiples** - Simulación de flujo real

## Resultados

Los resultados se guardan en archivos JSON con el formato:
`test_results_YYYYMMDD_HHMMSS.json`

## Estructura del Request

La herramienta envía los datos como **query strings** (no como JSON body), siguiendo el formato de Make.com:

```
POST /api/pms/reservations?unitId=1&arrivalDate=2024-12-25&departureDate=2024-12-28&...
```

Los objetos complejos (contact, payment, breakdown, etc.) se envían como **strings JSON**:

```
contact={"firstName":"John","lastName":"Doe","primaryEmail":"john@example.com"}
payment={"amount":100,"paymentCard":{"cardNumber":"4111111111111111",...}}
```

## Campos Requeridos

- `unitId` (integer) - ID de la unidad
- `arrivalDate` (string) - Fecha de llegada en formato YYYY-MM-DD
- `departureDate` (string) - Fecha de salida en formato YYYY-MM-DD

## Campos Opcionales Importantes

- `contactId` o `contact` - Información del contacto
- `rateTypeId` - Override del rate automático
- `occupants` - Objeto JSON con ocupantes (adults, children, pets)
- `addOns` - Array JSON con add-ons
- `payment` - Objeto JSON con información de pago
- `promoCode` - Código promocional
- `status` - Estado de la reserva (Hold, Confirmed, etc.)
- `notes` - Array JSON con notas
- `breakdown` - Objeto JSON con precios personalizados (solo Server Keys)

## Notas

- El servidor mock **NO** guarda datos en la base de datos real
- Todos los tests usan autenticación Basic Auth (usuario: `test_user`, contraseña: `test_pass`)
- El servidor mock valida contra la especificación OpenAPI
- Los IDs de reserva son incrementales y se reinician al reiniciar el servidor




