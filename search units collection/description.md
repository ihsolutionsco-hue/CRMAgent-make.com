# Descripción de la Herramienta

Busca unidades en TrackHS usando la API de Unit Collection (`GET /api/pms/units`). Diseñada para servicio al cliente de empresas de alquiler de casas. Permite filtrar por características (dormitorios, baños, amenities), disponibilidad (fechas), estado, y más. 

**Seguridad:** El output excluye información sensible de direcciones (streetAddress, coordenadas, etc.) para proteger la privacidad. Solo incluye información general de ubicación (ciudad, estado, país) y datos relevantes para asistir a clientes.

Incluye soporte para paginación (page/scroll) y ordenamiento. Requiere autenticación Basic Auth con credenciales de TrackHS.

