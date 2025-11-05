#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de pruebas para la API de TrackHS - Get Quote Collection V2
Prueba diferentes casos de uso para validar la implementación y verificar
qué valores acepta realmente la API
"""

import os
import sys
import json
from datetime import datetime
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

ENDPOINT = f"{API_BASE_URL}/v2/pms/quotes"

print("=" * 80)
print("TESTING API TRACKHS - GET QUOTE COLLECTION V2")
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
            
            # Extraer información útil - NOTA: Según OpenAPI el campo es "amenities"
            embedded_data = data.get('_embedded', {})
            quotes = embedded_data.get('amenities', [])
            page = data.get('page', 'N/A')
            page_count = data.get('page_count', 'N/A')
            page_size = data.get('page_size', 'N/A')
            total_items = data.get('total_items', 'N/A')
            
            print(f"[OK] EXITO")
            print(f"     Total de quotes en respuesta: {len(quotes)}")
            print(f"     Pagina: {page}")
            print(f"     Total de paginas: {page_count}")
            print(f"     Tamano de pagina: {page_size}")
            print(f"     Total de items: {total_items}")
            
            # Mostrar estructura de _embedded para debug
            print(f"\n     Campos en _embedded: {list(embedded_data.keys())}")
            
            # Mostrar primeros 2 quotes como muestra
            if quotes:
                print(f"\n     Primeros quotes (muestra):")
                for i, quote in enumerate(quotes[:2], 1):
                    quote_id = quote.get('reservationId', 'N/A')
                    unit_id = quote.get('unitId', 'N/A')
                    arrival = quote.get('arrivalDate', 'N/A')
                    departure = quote.get('departureDate', 'N/A')
                    is_valid = quote.get('isValid', 'N/A')
                    is_available = quote.get('isAvailable', 'N/A')
                    print(f"        {i}. ReservationId: {quote_id}, UnitId: {unit_id}")
                    print(f"           Arrival: {arrival}, Departure: {departure}")
                    print(f"           Valid: {is_valid}, Available: {is_available}")
            
            # Validar estructura de respuesta
            required_fields = [
                '_embedded', 'page', 'page_count', 'page_size', 
                'total_items', '_links'
            ]
            
            print(f"\n     Validacion de estructura de respuesta:")
            missing_required = []
            for field in required_fields:
                has_field = field in data
                status = "[OK]" if has_field else "[MISS]"
                print(f"        {status} {field}: {has_field}")
                if not has_field:
                    missing_required.append(field)
            
            # Validar estructura de quotes
            if quotes:
                print(f"\n     Validacion de estructura de quotes:")
                sample_quote = quotes[0]
                quote_fields = [
                    'isValid', 'isAvailable', 'reservationId', 'arrivalDate', 
                    'departureDate', 'unitId', 'unitTypeId', 'currency',
                    'grossRent', 'netRent', 'total', 'guaranteePolicy', 
                    'cancellationPolicy', 'rates', 'occupants', 'guestFees'
                ]
                
                present_fields = []
                missing_quote_fields = []
                for field in quote_fields:
                    has_field = field in sample_quote
                    if has_field:
                        present_fields.append(field)
                    else:
                        missing_quote_fields.append(field)
                
                print(f"        Campos presentes: {len(present_fields)}/{len(quote_fields)}")
                if present_fields[:10]:
                    print(f"        Ejemplos: {', '.join(present_fields[:10])}")
                if missing_quote_fields:
                    print(f"        Campos faltantes: {', '.join(missing_quote_fields[:5])}")
            
            # Validar _links
            if '_links' in data:
                links = data['_links']
                print(f"\n     Enlaces de paginacion:")
                for link_name in ['self', 'first', 'last', 'next', 'prev']:
                    if link_name in links and links[link_name] and 'href' in links[link_name]:
                        print(f"        - {link_name}: ✓")
                    elif link_name in ['next', 'prev']:
                        # next y prev pueden no estar presentes si no hay página siguiente/anterior
                        pass
            
            return {
                'success': True,
                'data': data,
                'quotes_count': len(quotes),
                'page': page,
                'total_items': total_items,
                'missing_required': missing_required,
                'embedded_keys': list(embedded_data.keys())
            }
        elif response.status_code == 401:
            print(f"[ERROR] No autorizado (401)")
            print(f"        Verificar credenciales")
            return {
                'success': False,
                'status_code': 401,
                'error': 'Unauthorized'
            }
        elif response.status_code == 403:
            print(f"[ERROR] Prohibido (403)")
            print(f"        Verificar permisos")
            return {
                'success': False,
                'status_code': 403,
                'error': 'Forbidden'
            }
        elif response.status_code == 400:
            print(f"[ERROR] Bad Request (400)")
            try:
                error_data = response.json()
                print(f"        Error: {json.dumps(error_data, indent=2, ensure_ascii=False)[:500]}")
                return {
                    'success': False,
                    'status_code': 400,
                    'error': error_data
                }
            except:
                print(f"        Response: {response.text[:500]}")
                return {
                    'success': False,
                    'status_code': 400,
                    'error': response.text[:500]
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

# Test 1: Sin parámetros (default)
results.append(make_request(
    params=None,
    test_name="1. Sin parámetros (default)"
))

# Test 2: page=0 (según OpenAPI minimum: 0, maximum: 0)
results.append(make_request(
    params={'page': 0},
    test_name="2. page=0 (según OpenAPI)"
))

# Test 3: page=1 (probar si acepta valores > 0)
results.append(make_request(
    params={'page': 1, 'size': 5},
    test_name="3. page=1, size=5 (probar si acepta page > 0)"
))

# Test 4: page=2 (probar paginación)
results.append(make_request(
    params={'page': 2, 'size': 5},
    test_name="4. page=2, size=5 (probar paginación)"
))

# Test 5: page=-1 (probar valor negativo)
results.append(make_request(
    params={'page': -1},
    test_name="5. page=-1 (probar valor negativo)"
))

# Test 6: size pequeño
results.append(make_request(
    params={'size': 3},
    test_name="6. size=3"
))

# Test 7: Ordenamiento
results.append(make_request(
    params={'sortColumn': 'id', 'sortDirection': 'asc', 'size': 5},
    test_name="7. Ordenamiento por id (asc)"
))

# Test 8: Ordenamiento descendente
results.append(make_request(
    params={'sortColumn': 'order', 'sortDirection': 'desc', 'size': 5},
    test_name="8. Ordenamiento por order (desc)"
))

# Test 9: Búsqueda
results.append(make_request(
    params={'search': 'test', 'size': 5},
    test_name="9. Búsqueda con search='test'"
))

# Test 10: Filtros por IDs
results.append(make_request(
    params={'contactId': 1, 'size': 5},
    test_name="10. Filtrar por contactId=1"
))

# Test 11: futureQuotes
results.append(make_request(
    params={'futureQuotes': 1, 'size': 5},
    test_name="11. futureQuotes=1"
))

# Test 12: futureQuotes=0
results.append(make_request(
    params={'futureQuotes': 0, 'size': 5},
    test_name="12. futureQuotes=0"
))

# Test 13: activeQuotes
results.append(make_request(
    params={'activeQuotes': 1, 'size': 5},
    test_name="13. activeQuotes=1"
))

# Test 14: Combinación de parámetros
results.append(make_request(
    params={'page': 0, 'size': 3, 'sortColumn': 'order', 'sortDirection': 'asc'},
    test_name="14. Combinación: page=0, size=3, sortColumn=order, sortDirection=asc"
))

# RESUMEN
print("\n" + "=" * 80)
print("RESUMEN DE RESULTADOS")
print("=" * 80)

successful_tests = [r for r in results if r.get('success')]
failed_tests = [r for r in results if not r.get('success')]

print(f"\nTotal de tests: {len(results)}")
print(f"Exitosos: {len(successful_tests)}")
print(f"Fallidos: {len(failed_tests)}")

if successful_tests:
    print("\n[ANALISIS DE PAGINACION]")
    page_results = {}
    for i, result in enumerate(successful_tests, 1):
        if result.get('success') and 'page' in result:
            page_val = result.get('page', 'N/A')
            if page_val not in page_results:
                page_results[page_val] = []
            page_results[page_val].append(f"Test {i}")
    
    print("Valores de 'page' que acepta la API:")
    for page_val, tests in sorted(page_results.items()):
        print(f"  - page={page_val}: {', '.join(tests)}")
    
    print("\n[ANALISIS DE ESTRUCTURA _embedded]")
    embedded_keys_set = set()
    for result in successful_tests:
        if result.get('embedded_keys'):
            embedded_keys_set.update(result['embedded_keys'])
    print(f"Campos encontrados en _embedded: {list(embedded_keys_set)}")

if failed_tests:
    print("\n[TESTS FALLIDOS]")
    for i, result in enumerate(failed_tests, 1):
        status = result.get('status_code', 'N/A')
        error = result.get('error', 'Unknown error')
        print(f"  {i}. Status {status}: {str(error)[:100]}")

# Guardar resultados
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
results_file = f"test_results_{timestamp}.json"

# Limpiar datos para guardar (remover datos completos por tamaño)
clean_results = []
for r in results:
    clean_r = {
        'success': r.get('success'),
        'status_code': r.get('status_code'),
        'quotes_count': r.get('quotes_count', 0),
        'page': r.get('page'),
        'total_items': r.get('total_items'),
        'embedded_keys': r.get('embedded_keys', []),
        'missing_required': r.get('missing_required', [])
    }
    if not r.get('success'):
        clean_r['error'] = str(r.get('error', ''))[:200]
    clean_results.append(clean_r)

with open(results_file, 'w', encoding='utf-8') as f:
    json.dump(clean_results, f, indent=2, ensure_ascii=False)

print(f"\n[GUARDADO] Resultados guardados en: {results_file}")
print("=" * 80)

