# Descripción de la Herramienta

Obtiene todos los tipos de unidades (unit types) en TrackHS usando la API de Unit Types Collection (`GET /api/pms/units/types`). Esta herramienta permite consultar la colección completa de tipos de unidades disponibles en el sistema, con soporte para filtrado, búsqueda, ordenamiento y paginación.

**Características principales:**
- Paginación (page/size) para manejar grandes volúmenes de datos
- Ordenamiento por múltiples columnas (id, name, nodeName, shortDescription, longDescription, createdAt)
- Búsqueda por texto (search, term) en nombres y descripciones
- Filtrado por nodo (nodeId), estado activo (isActive), permisos de tarifas (allowUnitRates), y más
- Respuesta completa con información detallada de cada tipo de unidad

**Seguridad:** Requiere autenticación Basic Auth con credenciales de TrackHS.

