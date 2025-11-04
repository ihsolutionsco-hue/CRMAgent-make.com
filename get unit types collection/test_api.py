#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de pruebas para la API de TrackHS - Get Unit Types Collection
Prueba diferentes casos de uso para validar la implementación
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

ENDPOINT = f"{API_BASE_URL}/pms/units/types"

print("=" * 80)
print("TESTING API TRACKHS - GET UNIT TYPES COLLECTION")
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
            unit_types = data.get('_embedded', {}).get('units', [])
            page = data.get('page', 'N/A')
            page_count = data.get('page_count', 'N/A')
            page_size = data.get('page_size', 'N/A')
            total_items = data.get('total_items', 'N/A')
            
            print(f"[OK] EXITO")
            print(f"     Total de unit types en respuesta: {len(unit_types)}")
            print(f"     Pagina: {page}")
            print(f"     Total de paginas: {page_count}")
            print(f"     Tamano de pagina: {page_size}")
            print(f"     Total de items: {total_items}")
            
            # Mostrar primeros 3 unit types como muestra
            if unit_types:
                print(f"\n     Primeros unit types (muestra):")
                for i, unit_type in enumerate(unit_types[:3], 1):
                    unit_type_id = unit_type.get('id', 'N/A')
                    name = unit_type.get('name', 'N/A')
                    node_id = unit_type.get('nodeId', 'N/A')
                    short_desc = unit_type.get('shortDescription', 'N/A')[:50] if unit_type.get('shortDescription') else 'N/A'
                    print(f"        {i}. ID: {unit_type_id}, Name: {name}, NodeId: {node_id}")
                    print(f"           Desc: {short_desc}...")
            
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
            
            # Validar estructura de unit types
            if unit_types:
                print(f"\n     Validacion de estructura de unit types:")
                sample_unit_type = unit_types[0]
                unit_type_fields = [
                    'id', 'name', 'nodeId', 'shortDescription', 'longDescription',
                    'lodgingTypeId', 'checkinTime', 'checkoutTime', 'timezone',
                    'maxOccupancy', 'bedrooms', 'fullBathrooms', 'petsFriendly',
                    'amenities', 'updatedAt', '_links'
                ]
                
                present_fields = []
                missing_unit_type_fields = []
                for field in unit_type_fields:
                    has_field = field in sample_unit_type
                    if has_field:
                        present_fields.append(field)
                    else:
                        missing_unit_type_fields.append(field)
                
                print(f"        Campos presentes: {len(present_fields)}/{len(unit_type_fields)}")
                if present_fields[:10]:
                    print(f"        Ejemplos: {', '.join(present_fields[:10])}")
                if missing_unit_type_fields:
                    print(f"        Campos faltantes: {', '.join(missing_unit_type_fields[:5])}")
            
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
                'unit_types_count': len(unit_types),
                'page': page,
                'total_items': total_items,
                'missing_required': missing_required
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

# Test 1: Obtener todos los unit types sin parámetros (default)
results.append(make_request(
    params=None,
    test_name="1. Obtener todos los unit types (sin parámetros, default)"
))

# Test 2: Paginación básica - página 1
results.append(make_request(
    params={'page': 1, 'size': 5},
    test_name="2. Paginación básica (page=1, size=5)"
))

# Test 3: Paginación - página 1
results.append(make_request(
    params={'page': 1, 'size': 5},
    test_name="3. Paginación (page=1, size=5)"
))

# Test 4: Ordenamiento por nombre (ascendente)
results.append(make_request(
    params={'page': 1, 'size': 5, 'sortColumn': 'name', 'sortDirection': 'asc'},
    test_name="4. Ordenamiento por nombre (ascendente)"
))

# Test 5: Ordenamiento por nombre (descendente)
results.append(make_request(
    params={'page': 1, 'size': 5, 'sortColumn': 'name', 'sortDirection': 'desc'},
    test_name="5. Ordenamiento por nombre (descendente)"
))

# Test 6: Ordenamiento por ID
results.append(make_request(
    params={'page': 1, 'size': 5, 'sortColumn': 'id', 'sortDirection': 'asc'},
    test_name="6. Ordenamiento por ID (ascendente)"
))

# Test 7: Ordenamiento por createdAt
results.append(make_request(
    params={'page': 1, 'size': 5, 'sortColumn': 'createdAt', 'sortDirection': 'desc'},
    test_name="7. Ordenamiento por createdAt (descendente)"
))

# Test 8: Búsqueda por texto (search)
results.append(make_request(
    params={'page': 1, 'size': 5, 'search': 'beach'},
    test_name="8. Búsqueda por texto (search='beach')"
))

# Test 9: Búsqueda por término (term)
results.append(make_request(
    params={'page': 1, 'size': 5, 'term': 'villa'},
    test_name="9. Búsqueda por término (term='villa')"
))

# Test 10: Filtro por nodeId (single)
# Primero necesitamos obtener un nodeId válido
first_result = None
for r in results:
    if r.get('success') and r.get('data'):
        first_result = r
        break

if first_result and first_result.get('data'):
    unit_types = first_result['data'].get('_embedded', {}).get('units', [])
    if unit_types:
        sample_node_id = unit_types[0].get('nodeId')
        if sample_node_id:
            results.append(make_request(
                params={'page': 1, 'size': 5, 'nodeId': sample_node_id},
                test_name=f"10. Filtro por nodeId (single, nodeId={sample_node_id})"
            ))

# Test 11: Filtro por isActive=1 (solo activos)
results.append(make_request(
    params={'page': 1, 'size': 5, 'isActive': 1},
    test_name="11. Filtro por isActive=1 (solo activos)"
))

# Test 12: Filtro por isActive=0 (solo inactivos)
results.append(make_request(
    params={'page': 1, 'size': 5, 'isActive': 0},
    test_name="12. Filtro por isActive=0 (solo inactivos)"
))

# Test 13: Filtro por allowUnitRates=1
results.append(make_request(
    params={'page': 1, 'size': 5, 'allowUnitRates': 1},
    test_name="13. Filtro por allowUnitRates=1 (permite tarifas de unidad)"
))

# Test 14: Filtro por allowUnitRates=0
results.append(make_request(
    params={'page': 1, 'size': 5, 'allowUnitRates': 0},
    test_name="14. Filtro por allowUnitRates=0 (no permite tarifas de unidad)"
))

# Test 15: Combinación de filtros (search + isActive)
results.append(make_request(
    params={'page': 1, 'size': 5, 'search': 'house', 'isActive': 1},
    test_name="15. Combinación de filtros (search + isActive)"
))

# Test 16: Combinación de filtros (sortColumn + sortDirection + size)
results.append(make_request(
    params={'page': 1, 'size': 10, 'sortColumn': 'name', 'sortDirection': 'asc'},
    test_name="16. Combinación (sortColumn + sortDirection + size=10)"
))

# Test 17: Filtro por shortDescription (usando sortColumn)
results.append(make_request(
    params={'page': 1, 'size': 5, 'sortColumn': 'shortDescription', 'sortDirection': 'asc'},
    test_name="17. Ordenamiento por shortDescription"
))

# Test 18: Filtro por longDescription (usando sortColumn)
results.append(make_request(
    params={'page': 1, 'size': 5, 'sortColumn': 'longDescription', 'sortDirection': 'asc'},
    test_name="18. Ordenamiento por longDescription"
))

# Test 19: Filtro por nodeName (usando sortColumn)
results.append(make_request(
    params={'page': 1, 'size': 5, 'sortColumn': 'nodeName', 'sortDirection': 'asc'},
    test_name="19. Ordenamiento por nodeName"
))

# Test 20: Parámetro deprecated updatedSince (debe funcionar aunque esté deprecated)
results.append(make_request(
    params={'page': 1, 'size': 5, 'updatedSince': '2024-01-01'},
    test_name="20. Parámetro deprecated updatedSince (debe funcionar)"
))

# Test 21: Tamaño de página grande (para verificar límites)
results.append(make_request(
    params={'page': 1, 'size': 20},
    test_name="21. Tamaño de página grande (size=20)"
))

# Test 22: Combinación completa de parámetros
results.append(make_request(
    params={
        'page': 1,
        'size': 5,
        'sortColumn': 'name',
        'sortDirection': 'asc',
        'isActive': 1,
        'allowUnitRates': 1
    },
    test_name="22. Combinación completa de parámetros"
))

# Test 23: Sin parámetros de paginación (debe usar defaults)
results.append(make_request(
    params={'sortColumn': 'id', 'sortDirection': 'desc'},
    test_name="23. Solo ordenamiento sin paginación (debe usar defaults)"
))

# Test 24: Búsqueda vacía (debe retornar todos)
results.append(make_request(
    params={'page': 1, 'size': 5, 'search': ''},
    test_name="24. Búsqueda vacía (search='')"
))

# Test 25: Validar que los valores por defecto funcionan correctamente
results.append(make_request(
    params={},  # Parámetros vacíos pero presentes
    test_name="25. Parámetros vacíos (debe usar todos los defaults)"
))

# RESUMEN DE RESULTADOS
print("\n" + "=" * 80)
print("RESUMEN DE RESULTADOS")
print("=" * 80)

successful_tests = sum(1 for r in results if r.get('success', False))
total_tests = len(results)

print(f"\n[OK] Tests exitosos: {successful_tests}/{total_tests}")
print(f"[ERROR] Tests fallidos: {total_tests - successful_tests}/{total_tests}")

# Mostrar qué tests fallaron
failed_tests = []
for i, result in enumerate(results, 1):
    if not result.get('success', False):
        failed_tests.append(i)

if failed_tests:
    print(f"\n[WARN] Tests que fallaron: {failed_tests}")
    print("       Revisar los mensajes de error arriba para más detalles")

# Estadísticas de las respuestas exitosas
if successful_tests > 0:
    print("\n[STATS] Estadísticas de respuestas exitosas:")
    total_unit_types = sum(r.get('unit_types_count', 0) for r in results if r.get('success'))
    avg_unit_types = total_unit_types / successful_tests if successful_tests > 0 else 0
    
    print(f"     Total de unit types obtenidos: {total_unit_types}")
    print(f"     Promedio por respuesta: {avg_unit_types:.2f}")
    
    # Validar estructura de respuestas exitosas
    all_missing_required = []
    for r in results:
        if r.get('success', False) and r.get('missing_required'):
            all_missing_required.extend(r.get('missing_required', []))
    
    if all_missing_required:
        unique_missing = set(all_missing_required)
        print(f"     ⚠️  Campos requeridos faltantes en alguna respuesta: {', '.join(unique_missing)}")
    else:
        print("     ✅ Todas las respuestas exitosas tienen los campos requeridos")
    
    # Verificar que los parámetros de paginación funcionan
    pagination_tests = [r for r in results if r.get('success') and r.get('data')]
    if pagination_tests:
        print(f"\n[STATS] Validación de paginación:")
        page_sizes = [r['data'].get('page_size') for r in pagination_tests if r['data'].get('page_size')]
        if page_sizes:
            print(f"     Tamaños de página usados: {set(page_sizes)}")
        
        total_items_list = [r['data'].get('total_items') for r in pagination_tests if r['data'].get('total_items')]
        if total_items_list and len(set(total_items_list)) == 1:
            print(f"     ✅ Total de items consistente: {total_items_list[0]}")
        elif total_items_list:
            print(f"     ⚠️  Total de items varía: {set(total_items_list)}")

print("\n" + "=" * 80)
print("TESTING COMPLETADO")
print("=" * 80)

# Guardar resultados en archivo JSON para análisis
output_file = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(output_file, 'w', encoding='utf-8') as f:
    # Limpiar datos para JSON (remover objetos completos de data si es muy grande)
    clean_results = []
    for r in results:
        clean_r = r.copy()
        if 'data' in clean_r:
            # Guardar solo metadata de data, no todo el contenido
            data_meta = {
                'has_embedded': '_embedded' in clean_r['data'],
                'page': clean_r['data'].get('page'),
                'page_count': clean_r['data'].get('page_count'),
                'total_items': clean_r['data'].get('total_items'),
                'unit_types_count': len(clean_r['data'].get('_embedded', {}).get('units', []))
            }
            clean_r['data_meta'] = data_meta
            del clean_r['data']
        clean_results.append(clean_r)
    
    json.dump({
        'timestamp': datetime.now().isoformat(),
        'endpoint': ENDPOINT,
        'total_tests': total_tests,
        'successful_tests': successful_tests,
        'failed_tests': total_tests - successful_tests,
        'results': clean_results
    }, f, indent=2, ensure_ascii=False)

print(f"\n[SAVE] Resultados guardados en: {output_file}")

