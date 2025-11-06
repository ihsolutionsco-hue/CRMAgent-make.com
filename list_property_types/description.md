# Get all Unit Types

Obtiene todos los tipos de unidades (unit types) en TrackHS (`GET /api/pms/units/types`). Incluye paginación, ordenamiento, búsqueda por texto y filtros (nodeId, isActive, allowUnitRates). Requiere autenticación Basic Auth.

**Validaciones automáticas:**
- `page`: Si es 0 o menor, se corrige automáticamente a 1 (mínimo permitido por la API)
- `size`: Si es 0 o menor, se omite (null = sin límite)
- Parámetros opcionales: Si no se proporcionan o son null, se omiten del query string

**Uso sin parámetros:** Puedes llamar la herramienta con `{}` (objeto vacío) y funcionará correctamente usando los valores por defecto (page=1, sortColumn=name, sortDirection=asc).