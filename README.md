# Make.com Tools - TrackHS Integration

Colección de blueprints y herramientas para Make.com que integran con la API de TrackHS para sistemas CRM y PMS (Property Management System).

## 📋 Índice

- [Descripción General](#descripción-general)
- [Herramientas Disponibles](#herramientas-disponibles)
  - [CRM - Gestión de Contactos](#crm---gestión-de-contactos)
  - [PMS - Gestión de Unidades](#pms---gestión-de-unidades)
  - [PMS - Gestión de Reservas](#pms---gestión-de-reservas)
  - [PMS - Gestión de Cotizaciones](#pms---gestión-de-cotizaciones)
  - [PMS - Mantenimiento](#pms---mantenimiento)
- [Configuración General](#configuración-general)
- [Estructura del Proyecto](#estructura-del-proyecto)

## Descripción General

Este repositorio contiene una colección de blueprints para Make.com que permiten interactuar con la API de TrackHS. Las herramientas están organizadas por funcionalidad y cubren las principales operaciones de CRM y PMS.

**Requisitos de Autenticación:**
- Todas las herramientas requieren **Basic Authentication** con credenciales de TrackHS
- Username: Tu usuario de TrackHS
- Password: Tu contraseña de TrackHS

## Herramientas Disponibles

### CRM - Gestión de Contactos

#### 📝 Create Contact Collection
**Ubicación:** `create contact collection/`

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
- Blueprint: `create contact collection.json`
- Documentación: `createContact.md`
- Descripción: `description.md`
- Tests: `test_create_contact.py`

---

#### 🔍 Get Contact Collection
**Ubicación:** `get contact collection/`

Obtiene la información completa de un contacto específico en TrackHS CRM (`GET /api/crm/contacts/{contactId}`).

**Funcionalidades:**
- Devuelve datos completos del contacto
- Información personal, contacto, dirección
- Notas, tags, referencias
- Valores personalizados

**Archivos:**
- Blueprint: `get contact collection.json`
- Descripción: `description.md`

---

#### 📋 Get Contacts Collection
**Ubicación:** `get contacts collection/`

Obtiene una colección de contactos con soporte para paginación, filtros y búsqueda.

**Funcionalidades:**
- Paginación y ordenamiento
- Búsqueda por texto
- Filtros avanzados
- Múltiples resultados

**Archivos:**
- Blueprint: `get contacts collection.json`
- Documentación: `getContactsCollection.md`
- Tests: `test_api.py`

---

### PMS - Gestión de Unidades

#### 🔎 Search Units Collection
**Ubicación:** `search units collection/`

Busca unidades en TrackHS usando la API de Unit Collection (`GET /api/pms/units`). Diseñada para servicio al cliente de empresas de alquiler de casas.

**Funcionalidades:**
- Filtrar por características (dormitorios, baños, amenities)
- Filtrar por disponibilidad (fechas)
- Filtrar por estado
- Paginación y ordenamiento
- **Seguridad:** Excluye información sensible de direcciones (streetAddress, coordenadas)

**Archivos:**
- Blueprint: `search units collection.json`
- Documentación: `search units collection.md`
- Descripción: `description.md`
- Tests: `test_api.py`

---

#### 🏠 Get Unit By ID Collection
**Ubicación:** `get unit by id collection/`

Obtiene los detalles completos de una unidad específica en TrackHS (`GET /api/pms/units/{unitId}`).

**Funcionalidades:**
- Metadata completa: atributos, amenities, descripciones
- Coordenadas y políticas
- Información de check-in/out
- Datos completos de la unidad

**Archivos:**
- Blueprint: `get unit by id collection.json`
- Descripción: `description.md`
- Tests: `test_api.py`

---

#### 🏗️ Get Unit Types Collection
**Ubicación:** `get unit types collection/`

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
- Blueprint: `get unit types collection.json`
- Documentación: `get unit types.md`
- Descripción: `description.md`
- Tests: `test_api.py`

---

### PMS - Gestión de Reservas

#### 📅 Create Reservation Collection
**Ubicación:** `create reservation collection/`

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
- Blueprint: `create reservation collection.json`
- Documentación: `create reservation collection.md`
- Descripción: `description.md`
- Tests: `test_create_reservation.py`

---

#### 📊 Get Reservations Collection
**Ubicación:** `get reservations collection/`

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
- Blueprint: `get reservations collection.json`
- Documentación: `get reservations collection.md`
- Descripción: `readme.md` (contiene guía detallada de formatos de fecha)

---

### PMS - Gestión de Cotizaciones

#### 💰 Get Quote Collection
**Ubicación:** `get quote collection/`

Obtiene cotizaciones (quotes) para unidades habilitadas en TrackHS.

**Funcionalidades:**
- Paginación y ordenamiento
- Búsqueda por texto
- Filtros: contactId, unitId, unitTypeId, futureQuotes, activeQuotes
- **Validaciones:** page mínimo 1

**Archivos:**
- Blueprint: `get quote collection.json`
- Documentación: `get quote collection.md`
- Descripción: `description.md`
- Tests: `test_api.py`

---

#### 📄 Create Quote V2 Collection
**Ubicación:** `create quote v2 collection/`

Crea cotizaciones en TrackHS (versión V2).

**Archivos:**
- Blueprint: `create quote v2 collection.json`
- Documentación: `create quote V2 doc.md`

---

### PMS - Mantenimiento

#### 🔧 Create Maintenance Work Order Collection
**Ubicación:** `create maintenance work order collection/`

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
- Blueprint: `create maintenance work order collection.json`
- Documentación: `create maintenance work order doc.md`
- Descripción: `description.md`
- Tests: `test_create_maintenance_work_order.py`

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

### Testing Local

Muchas herramientas incluyen scripts de prueba en Python. Para ejecutarlos:

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar tests (si están disponibles)
python test_api.py
# o
python run_tests.py
```

Crea un archivo `.env` con tus credenciales:
```env
TRACKHS_API_URL=https://tu-dominio.trackhs.com
TRACKHS_USERNAME=tu_usuario
TRACKHS_PASSWORD=tu_contraseña
```

---

## Estructura del Proyecto

```
make.com/
├── README.md (este archivo)
│
├── create contact collection/
│   ├── create contact collection.json
│   ├── createContact.md
│   ├── description.md
│   ├── requirements.txt
│   └── test_create_contact.py
│
├── get contact collection/
│   ├── get contact collection.json
│   └── description.md
│
├── get contacts collection/
│   ├── get contacts collection.json
│   ├── getContactsCollection.md
│   ├── readme.md
│   ├── requirements.txt
│   └── test_api.py
│
├── create reservation collection/
│   ├── create reservation collection.json
│   ├── create reservation collection.md
│   ├── description.md
│   ├── requirements.txt
│   └── test_create_reservation.py
│
├── get reservations collection/
│   ├── get reservations collection.json
│   ├── get reservations collection.md
│   └── readme.md
│
├── search units collection/
│   ├── search units collection.json
│   ├── search units collection.md
│   ├── description.md
│   ├── requirements.txt
│   └── test_api.py
│
├── get unit by id collection/
│   ├── get unit by id collection.json
│   ├── description.md
│   └── test_api.py
│
├── get unit types collection/
│   ├── get unit types collection.json
│   ├── get unit types.md
│   ├── description.md
│   └── test_api.py
│
├── get quote collection/
│   ├── get quote collection.json
│   ├── get quote collection.md
│   ├── description.md
│   └── test_api.py
│
├── create quote v2 collection/
│   ├── create quote v2 collection.json
│   └── create quote V2 doc.md
│
└── create maintenance work order collection/
    ├── create maintenance work order collection.json
    ├── create maintenance work order doc.md
    ├── description.md
    └── test_create_maintenance_work_order.py
```

---

## 📝 Notas

- Cada herramienta tiene su propia carpeta con documentación específica
- Los archivos `.json` son los blueprints que se pueden importar directamente en Make.com
- Los archivos `.md` contienen documentación detallada de cada herramienta
- Algunas herramientas incluyen scripts de prueba en Python para validar la funcionalidad

---

## 🐛 Soporte

Si encuentras problemas con alguna de las herramientas o la API de TrackHS, revisa la documentación específica en cada carpeta o contacta al equipo de soporte de TrackHS con los detalles del problema.

---

**Última actualización:** 2025
