Obtiene una cotización (quote) para las unidades que han sido habilitadas para tu channel key en TrackHS (`GET /api/v2/pms/quotes`). Incluye paginación, ordenamiento, búsqueda y filtros (contactId, unitId, unitTypeId, futureQuotes, activeQuotes). Requiere autenticación Basic Auth.

**Validaciones automáticas:**
- `page`: Si es menor a 1, se corrige automáticamente a 1 (la API rechaza page=0)
- `size`: Si es 0 o menor, se omite (null = sin límite)
- Parámetros opcionales: Si no se proporcionan o son null, se omiten del query string

**Uso sin parámetros:** Puedes llamar la herramienta con `{}` (objeto vacío) y funcionará correctamente usando los valores por defecto (page=1, sortColumn=order, sortDirection=asc).

**Nota importante:** La documentación OpenAPI tiene errores:
- Dice que `page` acepta solo 0, pero la API rechaza 0 y requiere valores >= 1
- Dice que el campo es `_embedded.amenities`, pero en realidad es `_embedded.quotes`

