#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de pruebas para la API de TrackHS - Search Units Collection
Prueba diferentes casos de uso para validar la implementación
"""

import os
import sys
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth

# Configurar encoding para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Cargar variables de entorno (buscar en directorio raíz del proyecto)
import pathlib
project_root = pathlib.Path(__file__).parent.parent
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

# Configuración
API_BASE_URL = os.getenv('TRACKHS_API_URL', 'https://ihmvacations.trackhs.com')
API_USERNAME = os.getenv('TRACKHS_USERNAME')
API_PASSWORD = os.getenv('TRACKHS_PASSWORD')

if not API_USERNAME or not API_PASSWORD:
    print("❌ ERROR: TRACKHS_USERNAME y TRACKHS_PASSWORD deben estar configurados en el archivo .env")
    sys.exit(1)

# Construir URL base
if not API_BASE_URL.endswith('/api'):
    API_BASE_URL = f"{API_BASE_URL.rstrip('/')}/api"

ENDPOINT = f"{API_BASE_URL}/pms/units"

print("=" * 80)
print("TESTING API TRACKHS - SEARCH UNITS COLLECTION")
print("=" * 80)
print(f"Endpoint: {ENDPOINT}")
print(f"Usuario: {API_USERNAME[:20]}...")
print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)
print()

# Configurar autenticación
auth = HTTPBasicAuth(API_USERNAME, API_PASSWORD)

# Helper para hacer requests
def make_request(params=None, test_name=""):
    """Hace una petición a la API y muestra los resultados"""
    try:
        print(f"\n[TEST] {test_name}")
        if params:
            # Limpiar parámetros None/null
            clean_params = {k: v for k, v in params.items() if v is not None}
            print(f"[REQ] Parametros: {clean_params}")
        else:
            print(f"[REQ] Sin parametros")
        
        response = requests.get(
            ENDPOINT,
            auth=auth,
            params=params,
            headers={'Accept': 'application/json'},
            timeout=30
        )
        
        print(f"[RES] Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Extraer información útil
            units = data.get('_embedded', {}).get('units', [])
            page = data.get('page', 'N/A')
            page_count = data.get('page_count', 'N/A')
            page_size = data.get('page_size', 'N/A')
            total_items = data.get('total_items', 'N/A')
            
            print(f"[OK] EXITO")
            print(f"     Total de unidades en respuesta: {len(units)}")
            print(f"     Pagina: {page}")
            print(f"     Total de paginas: {page_count}")
            print(f"     Tamano de pagina: {page_size}")
            print(f"     Total de items: {total_items}")
            
            # Mostrar primeras 3 unidades como muestra
            if units:
                print(f"\n     Primeras unidades (muestra):")
                for i, unit in enumerate(units[:3], 1):
                    unit_id = unit.get('id', 'N/A')
                    name = unit.get('name', 'N/A')
                    unit_code = unit.get('unitCode', 'N/A')
                    bedrooms = unit.get('bedrooms', 'N/A')
                    max_occupancy = unit.get('maxOccupancy', 'N/A')
                    print(f"        {i}. ID: {unit_id} | Nombre: {name} | Codigo: {unit_code} | Dormitorios: {bedrooms} | Ocupacion: {max_occupancy}")
            
            # Verificar estructura de respuesta
            has_embedded = '_embedded' in data
            has_units = 'units' in data.get('_embedded', {})
            has_links = '_links' in data
            
            print(f"\n     Validacion de estructura:")
            print(f"        [OK] _embedded: {has_embedded}")
            print(f"        [OK] units array: {has_units}")
            print(f"        [OK] _links: {has_links}")
            
            return {
                'success': True,
                'data': data,
                'units_count': len(units),
                'total_items': total_items
            }
        else:
            print(f"[ERROR] Status Code: {response.status_code}")
            try:
                error_data = response.json()
                print(f"        Error: {json.dumps(error_data, indent=2, ensure_ascii=False)[:500]}")
            except:
                print(f"        Response: {response.text[:500]}")
            return {
                'success': False,
                'status_code': response.status_code,
                'error': response.text[:500]
            }
            
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Error de conexion")
        print(f"        {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }
    except json.JSONDecodeError as e:
        print(f"[ERROR] Error de parsing JSON")
        print(f"        {str(e)}")
        print(f"        Response: {response.text[:500]}")
        return {
            'success': False,
            'error': 'JSON decode error'
        }

# CASOS DE PRUEBA
results = []

print("\n" + "=" * 80)
print("INICIANDO CASOS DE PRUEBA")
print("=" * 80)

# Test 1: Búsqueda básica sin parámetros
results.append(make_request(
    params=None,
    test_name="1. Búsqueda básica (sin parámetros)"
))

# Test 2: Paginación - Primera página pequeña
results.append(make_request(
    params={'page': 1, 'size': 3},
    test_name="2. Paginación - Primera página (size=3)"
))

# Test 3: Ordenamiento por nombre
results.append(make_request(
    params={'sortColumn': 'name', 'sortDirection': 'asc', 'size': 5},
    test_name="3. Ordenamiento por nombre (ascendente)"
))

# Test 4: Ordenamiento por ID
results.append(make_request(
    params={'sortColumn': 'id', 'sortDirection': 'desc', 'size': 5},
    test_name="4. Ordenamiento por ID (descendente)"
))

# Test 5: Ordenamiento por nodeName
results.append(make_request(
    params={'sortColumn': 'nodeName', 'sortDirection': 'asc', 'size': 5},
    test_name="5. Ordenamiento por nodeName (ascendente)"
))

# Test 6: Ordenamiento por unitTypeName
results.append(make_request(
    params={'sortColumn': 'unitTypeName', 'sortDirection': 'asc', 'size': 5},
    test_name="6. Ordenamiento por unitTypeName (ascendente)"
))

# Test 7: Búsqueda por término search
results.append(make_request(
    params={'search': 'Townhome', 'size': 5},
    test_name="7. Búsqueda con parámetro 'search'"
))

# Test 8: Búsqueda por term
results.append(make_request(
    params={'term': 'TH', 'size': 5},
    test_name="8. Búsqueda con parámetro 'term'"
))

# Test 9: Búsqueda por unitCode (exacto)
results.append(make_request(
    params={'unitCode': 'TH444', 'size': 5},
    test_name="9. Búsqueda por unitCode (coincidencia exacta)"
))

# Test 10: Búsqueda por unitCode con wildcard
results.append(make_request(
    params={'unitCode': 'TH%', 'size': 5},
    test_name="10. Búsqueda por unitCode con wildcard (TH%)"
))

# Test 11: Búsqueda por shortName
results.append(make_request(
    params={'shortName': 'TH%', 'size': 5},
    test_name="11. Búsqueda por shortName con wildcard"
))

# Test 12: Filtro por número de dormitorios (exacto)
results.append(make_request(
    params={'bedrooms': 3, 'size': 5},
    test_name="12. Filtro por dormitorios (exacto: 3)"
))

# Test 13: Filtro por mínimo de dormitorios
results.append(make_request(
    params={'minBedrooms': 2, 'size': 5},
    test_name="13. Filtro por mínimo de dormitorios (minBedrooms: 2)"
))

# Test 14: Filtro por máximo de dormitorios
results.append(make_request(
    params={'maxBedrooms': 2, 'size': 5},
    test_name="14. Filtro por máximo de dormitorios (maxBedrooms: 2)"
))

# Test 15: Filtro por baños (exacto)
results.append(make_request(
    params={'bathrooms': 2, 'size': 5},
    test_name="15. Filtro por baños (exacto: 2)"
))

# Test 16: Filtro por mínimo de baños
results.append(make_request(
    params={'minBathrooms': 2, 'size': 5},
    test_name="16. Filtro por mínimo de baños (minBathrooms: 2)"
))

# Test 17: Filtro por máximo de baños
results.append(make_request(
    params={'maxBathrooms': 2, 'size': 5},
    test_name="17. Filtro por máximo de baños (maxBathrooms: 2)"
))

# Test 18: Filtro por petsFriendly (1 = sí)
results.append(make_request(
    params={'petsFriendly': 1, 'size': 5},
    test_name="18. Filtro por petsFriendly (1 = permite mascotas)"
))

# Test 19: Filtro por petsFriendly (0 = no)
results.append(make_request(
    params={'petsFriendly': 0, 'size': 5},
    test_name="19. Filtro por petsFriendly (0 = no permite mascotas)"
))

# Test 20: Filtro por isActive (1 = activo)
results.append(make_request(
    params={'isActive': 1, 'size': 5},
    test_name="20. Filtro por isActive (1 = activo)"
))

# Test 21: Filtro por isBookable (1 = reservable)
results.append(make_request(
    params={'isBookable': 1, 'size': 5},
    test_name="21. Filtro por isBookable (1 = reservable)"
))

# Test 22: Filtro por computed (1 = incluir atributos computados)
results.append(make_request(
    params={'computed': 1, 'size': 3},
    test_name="22. Filtro por computed (1 = incluir atributos computados)"
))

# Test 23: Filtro por inherited (1 = incluir atributos heredados)
results.append(make_request(
    params={'inherited': 1, 'size': 3},
    test_name="23. Filtro por inherited (1 = incluir atributos heredados)"
))

# Test 24: Filtro por limited (1 = atributos limitados)
results.append(make_request(
    params={'limited': 1, 'size': 10},
    test_name="24. Filtro por limited (1 = atributos limitados)"
))

# Test 25: Filtro por includeDescriptions (1 = incluir descripciones)
results.append(make_request(
    params={'includeDescriptions': 1, 'size': 3},
    test_name="25. Filtro por includeDescriptions (1 = incluir descripciones)"
))

# Test 26: Filtro por unitStatus
results.append(make_request(
    params={'unitStatus': 'clean', 'size': 5},
    test_name="26. Filtro por unitStatus (clean)"
))

# Test 27: Filtro por fechas (arrival y departure) - formato date
future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
departure_date = (datetime.now() + timedelta(days=37)).strftime('%Y-%m-%d')
results.append(make_request(
    params={'arrival': future_date, 'departure': departure_date, 'size': 5},
    test_name=f"27. Filtro por disponibilidad (arrival={future_date}, departure={departure_date})"
))

# Test 28: Filtro por contentUpdatedSince (formato date-time)
one_month_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%dT00:00:00Z')
results.append(make_request(
    params={'contentUpdatedSince': one_month_ago, 'size': 5},
    test_name=f"28. Filtro por contentUpdatedSince (desde {one_month_ago})"
))

# Test 29: Combinación de filtros (dormitorios + petsFriendly)
results.append(make_request(
    params={
        'bedrooms': 3,
        'petsFriendly': 1,
        'isActive': 1,
        'size': 5
    },
    test_name="29. Combinación de filtros (3 dormitorios + permite mascotas + activo)"
))

# Test 30: Combinación de filtros (rango de dormitorios + baños)
results.append(make_request(
    params={
        'minBedrooms': 2,
        'maxBedrooms': 4,
        'minBathrooms': 2,
        'size': 5
    },
    test_name="30. Combinación de filtros (2-4 dormitorios + mínimo 2 baños)"
))

# Test 31: Búsqueda + ordenamiento + paginación
results.append(make_request(
    params={
        'search': 'Townhome',
        'sortColumn': 'name',
        'sortDirection': 'asc',
        'page': 1,
        'size': 3
    },
    test_name="31. Combinación completa (search + sort + pagination)"
))

# Test 32: Filtro por nodeId (si tenemos datos)
# Nota: Este test puede fallar si no hay nodeId válidos, pero lo dejamos para probar
results.append(make_request(
    params={'nodeId': 1, 'size': 5},
    test_name="32. Filtro por nodeId (nodeId=1)"
))

# RESUMEN DE RESULTADOS
print("\n" + "=" * 80)
print("RESUMEN DE RESULTADOS")
print("=" * 80)

successful_tests = sum(1 for r in results if r.get('success', False))
total_tests = len(results)

print(f"\n[OK] Tests exitosos: {successful_tests}/{total_tests}")
print(f"[ERROR] Tests fallidos: {total_tests - successful_tests}/{total_tests}")

if successful_tests > 0:
    print("\n[STATS] Estadisticas de unidades encontradas:")
    unit_counts = [r.get('units_count', 0) for r in results if r.get('success', False)]
    if unit_counts:
        print(f"     - Promedio de unidades por respuesta: {sum(unit_counts) / len(unit_counts):.1f}")
        print(f"     - Minimo: {min(unit_counts)}")
        print(f"     - Maximo: {max(unit_counts)}")
    
    # Mostrar total_items de la primera respuesta exitosa
    first_success = next((r for r in results if r.get('success', False)), None)
    if first_success and first_success.get('total_items'):
        print(f"     - Total de unidades disponibles: {first_success.get('total_items')}")

# Mostrar qué tests fallaron
failed_tests = []
for i, result in enumerate(results, 1):
    if not result.get('success', False):
        failed_tests.append(i)

if failed_tests:
    print(f"\n[WARN] Tests que fallaron: {failed_tests}")
    print("       Revisar los mensajes de error arriba para más detalles")

print("\n" + "=" * 80)
print("TESTING COMPLETADO")
print("=" * 80)

# Guardar resultados en archivo JSON para análisis
output_file = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump({
        'timestamp': datetime.now().isoformat(),
        'endpoint': ENDPOINT,
        'total_tests': total_tests,
        'successful_tests': successful_tests,
        'failed_tests': failed_tests,
        'results': results
    }, f, indent=2, ensure_ascii=False)

print(f"\n[SAVE] Resultados guardados en: {output_file}")

