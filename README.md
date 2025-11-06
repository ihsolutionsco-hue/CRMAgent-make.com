# Make.com Tools - TrackHS Integration

Colección de blueprints y herramientas para Make.com que integran con la API de TrackHS para sistemas CRM y PMS (Property Management System).

## 📋 Índice

- [Descripción General](#descripción-general)
- [Resumen de Herramientas](#resumen-de-herramientas)
- [Herramientas Disponibles](#herramientas-disponibles)
  - [CRM - Gestión de Contactos](#crm---gestión-de-contactos)
  - [PMS - Gestión de Unidades](#pms---gestión-de-unidades)
  - [PMS - Gestión de Reservas](#pms---gestión-de-reservas)
  - [PMS - Gestión de Cotizaciones](#pms---gestión-de-cotizaciones)
  - [PMS - Gestión de Precios](#pms---gestión-de-precios)
  - [PMS - Mantenimiento](#pms---mantenimiento)
  - [PMS - Housekeeping](#pms---housekeeping)
- [Configuración General](#configuración-general)
- [Estructura del Proyecto](#estructura-del-proyecto)

## Descripción General

Este repositorio contiene una colección de blueprints para Make.com que permiten interactuar con la API de TrackHS. Las herramientas están organizadas por funcionalidad y cubren las principales operaciones de CRM y PMS.

**Requisitos de Autenticación:**
- Todas las herramientas requieren **Basic Authentication** con credenciales de TrackHS
- Username: Tu usuario de TrackHS
- Password: Tu contraseña de TrackHS

## Resumen de Herramientas

Este proyecto contiene **15 colecciones de Make.com**:

### CRM (3 herramientas)
- ✅ `create_guest` - Crear contactos
- ✅ `get_guest_profile` - Obtener contacto por ID
- ✅ `search_guests` - Buscar/listar contactos

### PMS - Unidades (6 herramientas)
- ✅ `search_properties` - Buscar unidades con filtros
- ✅ `get_property_details` - Obtener detalles de unidad
- ✅ `list_property_types` - Obtener tipos de unidades
- ✅ `get_availability_calendar` - Disponibilidad de una unidad
- ✅ `find_available_properties` - Buscar unidades disponibles por fechas
- ✅ `get_daily_pricing` - Obtener tarifas diarias de una unidad

### PMS - Reservas (2 herramientas)
- ✅ `create_booking` - Crear reservas
- ✅ `search_bookings` - Buscar/listar reservas

### PMS - Cotizaciones (2 herramientas)
- ✅ `search_quotes` - Obtener cotizaciones
- ✅ `calculate_rate` - Crear cotizaciones V2

### PMS - Mantenimiento (1 herramienta)
- ✅ `schedule_maintenance` - Crear órdenes de mantenimiento

### PMS - Housekeeping (1 herramienta)
- ✅ `schedule_housekeeping` - Crear órdenes de limpieza

---

## Herramientas Disponibles

### CRM - Gestión de Contactos

#### 📝 create_guest
**Nombre Oficial:** Create Contact  
**Ubicación:** `create_guest/`

Crea contactos en TrackHS CRM validando datos según OpenAPI. 

**Campos Requeridos:**
- Nombre (firstName)
- Apellido (lastName)
- Email

**Campos Opcionales:**
- Teléfonos
- Dirección
- Notas
- Campos personalizados

**Archivos:**
- Blueprint: `create_guest.json`
- Documentación: `Create Contact.md`
- Descripción: `description.md`

---

#### 🔍 get_guest_profile
**Nombre Oficial:** Get a Contact  
**Ubicación:** `get_guest_profile/`

Obtiene la información completa de un contacto específico en TrackHS CRM (`GET /api/crm/contacts/{contactId}`).

**Funcionalidades:**
- Devuelve datos completos del contacto
- Información personal, contacto, dirección
- Notas, tags, referencias
- Valores personalizados

**Archivos:**
- Blueprint: `get_guest_profile.json`
- Documentación: `Get a Contact.md`
- Descripción: `description.md`

---

#### 📋 search_guests
**Nombre Oficial:** Get All Contacts  
**Ubicación:** `search_guests/`

Obtiene una colección de contactos con soporte para paginación, filtros y búsqueda.

**Funcionalidades:**
- Paginación y ordenamiento
- Búsqueda por texto
- Filtros avanzados
- Múltiples resultados

**Archivos:**
- Blueprint: `search_guests.json`
- Documentación: `Get All Contacts.md`
- Readme: `readme.md`

---

### PMS - Gestión de Unidades

#### 🔎 search_properties
**Nombre Oficial:** Unit  
**Ubicación:** `search_properties/`

Busca unidades en TrackHS usando la API de Unit Collection (`GET /api/pms/units`). Diseñada para servicio al cliente de empresas de alquiler de casas.

**Funcionalidades:**
- Filtrar por características (dormitorios, baños, amenities)
- Filtrar por disponibilidad (fechas)
- Filtrar por estado
- Paginación y ordenamiento
- **Seguridad:** Excluye información sensible de direcciones (streetAddress, coordenadas)

**Archivos:**
- Blueprint: `search_properties.json`
- Documentación: `Unit.md`
- Descripción: `description.md`
- Readme: `readme.md`

---

#### 🏠 get_property_details
**Nombre Oficial:** Get Unit  
**Ubicación:** `get_property_details/`

Obtiene los detalles completos de una unidad específica en TrackHS (`GET /api/pms/units/{unitId}`).

**Funcionalidades:**
- Metadata completa: atributos, amenities, descripciones
- Coordenadas y políticas
- Información de check-in/out
- Datos completos de la unidad

**Archivos:**
- Blueprint: `get_property_details.json`
- Descripción: `description.md`

---

#### 🏗️ list_property_types
**Nombre Oficial:** Get all Unit Types  
**Ubicación:** `list_property_types/`

Obtiene todos los tipos de unidades (unit types) en TrackHS (`GET /api/pms/units/types`).

**Funcionalidades:**
- Paginación y ordenamiento
- Búsqueda por texto
- Filtros: nodeId, isActive, allowUnitRates
- **Validaciones automáticas:**
  - `page`: Si es 0 o menor, se corrige automáticamente a 1
  - `size`: Si es 0 o menor, se omite
  - Parámetros opcionales null se omiten del query string

**Nota:** Puedes llamar la herramienta con `{}` (objeto vacío) y funcionará con valores por defecto.

**Archivos:**
- Blueprint: `list_property_types.json`
- Documentación: `Get all Unit Types.md`
- Descripción: `description.md`

---

#### 📅 get_availability_calendar
**Nombre Oficial:** V2 Unit Availability  
**Ubicación:** `get_availability_calendar/`

Obtiene la disponibilidad día por día de una unidad específica en TrackHS (`GET /api/v2/pms/units/{unitId}/availability`).

**Funcionalidades:**
- Devuelve un array con fecha y conteo de disponibilidad
- Parámetros opcionales: startDate, endDate (ISO 8601), useSoftDates (0|1)
- No está afectado por tarifas, solo por bloqueos y reservas
- Información de disponibilidad granular día por día

**Archivos:**
- Blueprint: `get_availability_calendar.json`
- Documentación: `V2 Unit Availability.md`
- Descripción: `description.md`

---

#### 📊 find_available_properties
**Nombre Oficial:** Unit Availability Search  
**Ubicación:** `find_available_properties/`

Busca unidades disponibles en TrackHS para un rango de fechas (`GET /api/pms/units/search`).

**Funcionalidades:**
- Parámetros requeridos: arrival, departure (ISO 8601)
- Parámetros opcionales: useSoftDates, exclude, unitTypeId, nodeId
- Búsqueda de múltiples unidades disponibles en un rango de fechas
- Retorna información de disponibilidad y unidades

**Archivos:**
- Blueprint: `find_available_properties.json`
- Documentación: `Unit Availability Search.md`
- Descripción: `description.md`

---

#### 💰 get_daily_pricing
**Nombre Oficial:** V2 Get Daily-Pricing on Unit  
**Ubicación:** `get_daily_pricing/`

Obtiene la tarifa diaria detallada de una unidad específica, incluyendo fechas y cambios, para mejorar la gestión de precios y maximizar el ingreso.

**Funcionalidades:**
- Obtiene tarifas diarias detalladas
- Incluye información de fechas y cambios de precios
- Útil para análisis de precios y optimización de ingresos

**Archivos:**
- Blueprint: `get_daily_pricing.json`
- Documentación: `V2 Get Daily-Pricing on Unit.md`
- Descripción: `description.md`

---

### PMS - Gestión de Reservas

#### 📅 create_booking
**Nombre Oficial:** Create Reservation  
**Ubicación:** `create_booking/`

Crea una nueva reserva en TrackHS PMS.

**Campos Requeridos:**
- unitId
- arrivalDate
- departureDate

**Campos Opcionales:**
- Información de contacto
- Métodos de pago
- Breakdown de precios personalizado
- Ocupantes
- Add-ons
- Códigos promocionales
- Notas

**Funcionalidades:**
- Valida datos según OpenAPI
- Maneja políticas de garantía y cancelación automáticamente

**Archivos:**
- Blueprint: `create_booking.json`
- Documentación: `Create Reservation.md`
- Descripción: `description.md`

---

#### 📊 search_bookings
**Nombre Oficial:** Search Reservations V2  
**Ubicación:** `search_bookings/`

Blueprint para Make.com que integra la API de TrackHS Search Reservations V2 (`GET /api/v2/pms/reservations`).

**Funcionalidades:**
- Filtros por fecha (bookedStart, bookedEnd, arrivalStart, arrivalEnd, departureStart, departureEnd)
- Filtros por estado, IDs (nodeId, unitId, contactId, etc.)
- Búsqueda por texto
- Paginación (page/scroll)
- Ordenamiento

**⚠️ Importante - Formatos de Fecha:**
- `bookedStart`/`bookedEnd`: Aceptan formato ISO-8601 completo o fecha sola (YYYY-MM-DD) ✅
- `arrivalStart`/`arrivalEnd`: **SOLO funcionan con formato fecha (YYYY-MM-DD)** ⚠️
- `departureStart`/`departureEnd`: Funcionan con ambos formatos, pero se recomienda fecha sola

**Límites de Make.com:**
- Límite de tokens: 200,000 tokens por respuesta
- Tamaño de página recomendado: `size=1-5` (default: 5)
- Tamaños grandes (10+) pueden causar error 400

**Archivos:**
- Blueprint: `search_bookings.json`
- Documentación: `Search Reservations V2.md`
- Readme: `readme.md`

---

### PMS - Gestión de Cotizaciones

#### 💰 search_quotes
**Nombre Oficial:** Quote V2 Reservation  
**Ubicación:** `search_quotes/`

Obtiene cotizaciones (quotes) para unidades habilitadas en TrackHS.

**Funcionalidades:**
- Paginación y ordenamiento
- Búsqueda por texto
- Filtros: contactId, unitId, unitTypeId, futureQuotes, activeQuotes
- **Validaciones:** page mínimo 1

**Archivos:**
- Blueprint: `search_quotes.json`
- Documentación: `Quote V2 Reservation.md`
- Descripción: `description.md`

---

#### 📄 calculate_rate
**Nombre Oficial:** Create Quote V2  
**Ubicación:** `calculate_rate/`

Crea cotizaciones en TrackHS (versión V2).

**Funcionalidades:**
- Crea cotizaciones V2 para unidades
- Calcula tarifas y precios
- Incluye políticas y restricciones

**Archivos:**
- Blueprint: `calculate_rate.json`
- Documentación: `Create Quote V2.md`

---

### PMS - Mantenimiento

#### 🔧 schedule_maintenance
**Nombre Oficial:** Create Maintenance Work Order  
**Ubicación:** `schedule_maintenance/`

Crea órdenes de trabajo de mantenimiento en TrackHS PMS.

**Campos Requeridos:**
- unitId
- Fecha
- Prioridad (1-5)
- Estado
- Resumen
- Costo
- Tiempo estimado

**Funcionalidades:**
- Retorna la orden creada completa
- Incluye prioridad, estado, costos y tiempo estimados

**Archivos:**
- Blueprint: `schedule_maintenance.json`
- Documentación: `Create Maintenance Work Order.md`
- Descripción: `description.md`

---

### PMS - Housekeeping

#### 🧹 schedule_housekeeping
**Nombre Oficial:** Create Housekeeping Work Order  
**Ubicación:** `schedule_housekeeping/`

Crea órdenes de trabajo de housekeeping (limpieza e inspecciones) en TrackHS PMS.

**Campos Requeridos:**
- `scheduledAt` - Fecha programada en formato ISO 8601 (YYYY-MM-DD)
- `unitId` - ID de la unidad donde se realizará el trabajo
- `status` - Estado inicial (pending, not-started, in-progress, completed, processed, cancelled, exception)
- `isInspection` O `cleanTypeId` - Uno de los dos es obligatorio

**Campos Opcionales:**
- `unitBlockId` - ID de bloqueo de unidad
- `userId` - ID del usuario/staff asignado
- `reservationId` - ID de reserva asociada
- `vendorId` - ID del proveedor externo
- `isTurn` - Indica si es un turno (limpieza entre huéspedes)
- `chargeOwner` - Indica si se cobra al propietario
- `comments` - Comentarios adicionales
- `cost` - Costo de la orden

**Funcionalidades:**
- Soporte para inspecciones (`isInspection=true`) y tipos de limpieza (`cleanTypeId`)
- Tipos de limpieza disponibles: Inspection (ID 3), Departure Clean (ID 4), Deep Clean (ID 5), Pre-Arrival Inspection (ID 6), Refresh Clean (ID 7), Carpet Cleaning (ID 8), Guest Request (ID 9), Pack and Play (ID 10)
- Retorna información completa de la orden creada: workOrderId, status, scheduledAt, unitId, cleanTypeId, isInspection

**Archivos:**
- Blueprint: `schedule_housekeeping.json`
- Documentación: `Create Housekeeping Work Order.md`
- Readme: `README.md`

---

## Configuración General

### Autenticación en Make.com

Todas las herramientas requieren **Basic Authentication** configurada en el módulo HTTP de Make.com:

1. **Username**: Tu usuario de TrackHS
2. **Password**: Tu contraseña de TrackHS

**Si recibes error 403 Forbidden**, verifica que las credenciales estén correctamente configuradas en el módulo HTTP de Make.com.

### Límites y Recomendaciones

- **Límite de tokens de Make.com**: 200,000 tokens por respuesta
- **Tamaños de página recomendados**: `size=1-5` para respuestas grandes
- **Tamaños grandes (10+) pueden causar errores**: "This model's maximum context length is 200000 tokens"
- **Paginación**: Para grandes volúmenes de datos, implementar paginación con múltiples llamadas incrementando `page`

---

## Estructura del Proyecto

```
make.com/
├── README.md (este archivo)
│
├── create_guest/
│   ├── create_guest.json
│   ├── Create Contact.md
│   ├── description.md
│   └── README.md
│
├── get_guest_profile/
│   ├── get_guest_profile.json
│   ├── Get a Contact.md
│   └── description.md
│
├── search_guests/
│   ├── search_guests.json
│   ├── Get All Contacts.md
│   └── readme.md
│
├── search_properties/
│   ├── search_properties.json
│   ├── Unit.md
│   ├── description.md
│   └── readme.md
│
├── get_property_details/
│   ├── get_property_details.json
│   └── description.md
│
├── list_property_types/
│   ├── list_property_types.json
│   ├── Get all Unit Types.md
│   └── description.md
│
├── get_availability_calendar/
│   ├── get_availability_calendar.json
│   ├── V2 Unit Availability.md
│   └── description.md
│
├── find_available_properties/
│   ├── find_available_properties.json
│   ├── Unit Availability Search.md
│   └── description.md
│
├── get_daily_pricing/
│   ├── get_daily_pricing.json
│   ├── V2 Get Daily-Pricing on Unit.md
│   └── description.md
│
├── create_booking/
│   ├── create_booking.json
│   ├── Create Reservation.md
│   └── description.md
│
├── search_bookings/
│   ├── search_bookings.json
│   ├── Search Reservations V2.md
│   └── readme.md
│
├── search_quotes/
│   ├── search_quotes.json
│   ├── Quote V2 Reservation.md
│   └── description.md
│
├── calculate_rate/
│   ├── calculate_rate.json
│   └── Create Quote V2.md
│
├── schedule_maintenance/
│   ├── schedule_maintenance.json
│   ├── Create Maintenance Work Order.md
│   └── description.md
│
└── schedule_housekeeping/
    ├── schedule_housekeeping.json
    ├── Create Housekeeping Work Order.md
    └── README.md
```

---

## 📝 Notas

- Cada herramienta tiene su propia carpeta con documentación específica
- Los archivos `.json` son los blueprints que se pueden importar directamente en Make.com
- Los archivos `.md` con nombres oficiales contienen la documentación OpenAPI completa de TrackHS
- Los archivos `description.md` contienen descripciones resumidas de cada herramienta
- Algunas herramientas incluyen archivos `readme.md` o `README.md` con documentación adicional

---

## 🐛 Soporte

Si encuentras problemas con alguna de las herramientas o la API de TrackHS, revisa la documentación específica en cada carpeta o contacta al equipo de soporte de TrackHS con los detalles del problema.

---

**Última actualización:** Noviembre 2025

