Obtiene la disponibilidad día por día de una unidad específica en TrackHS (GET /api/v2/pms/units/{unitId}/availability). Devuelve un array con fecha y conteo de disponibilidad. Parámetros opcionales: startDate, endDate (ISO 8601), useSoftDates (0|1). Requiere Basic Auth. No está afectado por tarifas, solo por bloqueos y reservas.

