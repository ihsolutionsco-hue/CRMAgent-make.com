#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de pruebas para la API de TrackHS - Get Unit By ID Collection
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

ENDPOINT_BASE = f"{API_BASE_URL}/pms/units"

print("=" * 80)
print("TESTING API TRACKHS - GET UNIT BY ID COLLECTION")
print("=" * 80)
print(f"Endpoint Base: {ENDPOINT_BASE}")
print(f"Usuario: {API_USERNAME[:20]}...")
print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)
print()

# Configurar autenticación
auth = HTTPBasicAuth(API_USERNAME, API_PASSWORD)

# Primero, obtener una lista de unidades para tener IDs válidos para probar
def get_sample_unit_ids():
    """Obtiene algunos IDs de unidades para usar en las pruebas"""
    try:
        print("[INFO] Obteniendo IDs de unidades de muestra...")
        response = requests.get(
            ENDPOINT_BASE,
            auth=auth,
            params={'size': 5, 'page': 1},
            headers={'Accept': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            units = data.get('_embedded', {}).get('units', [])
            unit_ids = [unit.get('id') for unit in units if unit.get('id')]
            print(f"[OK] Se encontraron {len(unit_ids)} IDs de unidades: {unit_ids}")
            return unit_ids
        else:
            print(f"[WARN] No se pudieron obtener IDs de muestra. Status: {response.status_code}")
            return []
    except Exception as e:
        print(f"[WARN] Error al obtener IDs de muestra: {str(e)}")
        return []

# Helper para hacer requests
def make_request(unit_id, params=None, test_name=""):
    """Hace una petición a la API y muestra los resultados"""
    try:
        endpoint = f"{ENDPOINT_BASE}/{unit_id}"
        print(f"\n[TEST] {test_name}")
        print(f"[REQ] URL: {endpoint}")
        if params:
            # Limpiar parámetros None/null
            clean_params = {k: v for k, v in params.items() if v is not None}
            print(f"[REQ] Query Parameters: {clean_params}")
        else:
            print(f"[REQ] Sin query parameters")
        
        response = requests.get(
            endpoint,
            auth=auth,
            params=params,
            headers={'Accept': 'application/json'},
            timeout=30
        )
        
        print(f"[RES] Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Validar campos principales
            unit_id = data.get('id', 'N/A')
            name = data.get('name', 'N/A')
            unit_code = data.get('unitCode', 'N/A')
            short_name = data.get('shortName', 'N/A')
            
            print(f"[OK] EXITO")
            print(f"     Unit ID: {unit_id}")
            print(f"     Nombre: {name}")
            print(f"     Codigo: {unit_code}")
            print(f"     Nombre Corto: {short_name}")
            
            # Validar estructura de respuesta - campos principales
            required_fields = [
                'id', 'name', 'unitCode', 'shortName', 'nodeId',
                'checkinTime', 'checkoutTime', 'timezone',
                'bedrooms', 'fullBathrooms', 'halfBathrooms',
                'maxOccupancy', 'petsFriendly', 'smokingAllowed',
                'childrenAllowed', 'isAccessible', 'amenities',
                'updatedAt'
            ]
            
            optional_fields = [
                'headline', 'shortDescription', 'longDescription', 'houseRules',
                'streetAddress', 'locality', 'region', 'postal', 'country',
                'latitude', 'longitude', 'directions',
                'checkinDetails', 'hasEarlyCheckin', 'earlyCheckinTime',
                'hasLateCheckout', 'lateCheckoutTime',
                'threeQuarterBathrooms', 'area', 'floors',
                'maxPets', 'eventsAllowed', 'minimumAgeLimit',
                'bedTypes', 'rooms', 'amenityDescription', 'custom',
                'localOffice', 'taxId', 'website', 'phone',
                'unitType', 'lodgingType', '_links'
            ]
            
            print(f"\n     Validacion de estructura:")
            missing_required = []
            for field in required_fields:
                has_field = field in data
                status = "[OK]" if has_field else "[MISS]"
                print(f"        {status} {field}: {has_field}")
                if not has_field:
                    missing_required.append(field)
            
            present_optional = []
            for field in optional_fields[:10]:  # Solo mostrar primeros 10 opcionales
                if field in data:
                    present_optional.append(field)
            
            if present_optional:
                print(f"\n     Campos opcionales presentes: {', '.join(present_optional[:10])}")
            
            # Validar tipos de datos importantes
            print(f"\n     Validacion de tipos:")
            type_validations = [
                ('id', int, data.get('id')),
                ('name', str, data.get('name')),
                ('bedrooms', int, data.get('bedrooms')),
                ('maxOccupancy', int, data.get('maxOccupancy')),
                ('petsFriendly', bool, data.get('petsFriendly')),
                ('amenities', list, data.get('amenities')),
            ]
            
            for field_name, expected_type, value in type_validations:
                if value is not None:
                    is_correct_type = isinstance(value, expected_type)
                    status = "[OK]" if is_correct_type else "[TYPE ERROR]"
                    print(f"        {status} {field_name}: {type(value).__name__} (esperado: {expected_type.__name__})")
            
            # Verificar _links si existe
            if '_links' in data:
                links = data['_links']
                print(f"\n     Enlaces disponibles:")
                for link_name, link_data in links.items():
                    if isinstance(link_data, dict) and 'href' in link_data:
                        print(f"        - {link_name}: {link_data['href']}")
            
            return {
                'success': True,
                'data': data,
                'unit_id': unit_id,
                'missing_required': missing_required
            }
        elif response.status_code == 404:
            print(f"[INFO] Unidad no encontrada (404)")
            print(f"       Esto es esperado si el ID no existe")
            return {
                'success': False,
                'status_code': 404,
                'error': 'Not Found'
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

# Obtener IDs de muestra
sample_unit_ids = get_sample_unit_ids()

if not sample_unit_ids:
    print("\n[WARN] No se pudieron obtener IDs de unidades para probar.")
    print("       Usando ID por defecto: 1")
    sample_unit_ids = [1]

# CASOS DE PRUEBA
results = []

print("\n" + "=" * 80)
print("INICIANDO CASOS DE PRUEBA")
print("=" * 80)

# Test 1: Obtener unidad básica sin parámetros opcionales
if sample_unit_ids:
    test_unit_id = sample_unit_ids[0]
    results.append(make_request(
        unit_id=test_unit_id,
        params=None,
        test_name="1. Obtener unidad básica (sin parámetros opcionales)"
    ))

# Test 2: Obtener unidad con computed=1
if sample_unit_ids:
    test_unit_id = sample_unit_ids[0]
    results.append(make_request(
        unit_id=test_unit_id,
        params={'computed': 1},
        test_name="2. Obtener unidad con computed=1 (atributos computados)"
    ))

# Test 3: Obtener unidad con inherited=1
if sample_unit_ids:
    test_unit_id = sample_unit_ids[0]
    results.append(make_request(
        unit_id=test_unit_id,
        params={'inherited': 1},
        test_name="3. Obtener unidad con inherited=1 (atributos heredados)"
    ))

# Test 4: Obtener unidad con includeDescriptions=1
if sample_unit_ids:
    test_unit_id = sample_unit_ids[0]
    results.append(make_request(
        unit_id=test_unit_id,
        params={'includeDescriptions': 1},
        test_name="4. Obtener unidad con includeDescriptions=1 (incluir descripciones)"
    ))

# Test 5: Combinación de parámetros opcionales
if sample_unit_ids:
    test_unit_id = sample_unit_ids[0]
    results.append(make_request(
        unit_id=test_unit_id,
        params={
            'computed': 1,
            'inherited': 1,
            'includeDescriptions': 1
        },
        test_name="5. Combinación de parámetros (computed + inherited + includeDescriptions)"
    ))

# Test 6: Obtener unidad con computed=0
if sample_unit_ids:
    test_unit_id = sample_unit_ids[0]
    results.append(make_request(
        unit_id=test_unit_id,
        params={'computed': 0},
        test_name="6. Obtener unidad con computed=0"
    ))

# Test 7: Obtener unidad con inherited=0
if sample_unit_ids:
    test_unit_id = sample_unit_ids[0]
    results.append(make_request(
        unit_id=test_unit_id,
        params={'inherited': 0},
        test_name="7. Obtener unidad con inherited=0"
    ))

# Test 8: Obtener unidad con includeDescriptions=0
if sample_unit_ids:
    test_unit_id = sample_unit_ids[0]
    results.append(make_request(
        unit_id=test_unit_id,
        params={'includeDescriptions': 0},
        test_name="8. Obtener unidad con includeDescriptions=0"
    ))

# Test 9: Probar con diferentes IDs de unidades
if len(sample_unit_ids) > 1:
    for i, unit_id in enumerate(sample_unit_ids[1:4], 9):  # Probar hasta 3 unidades más
        results.append(make_request(
            unit_id=unit_id,
            params=None,
            test_name=f"{i}. Obtener unidad diferente (ID: {unit_id})"
        ))

# Test 12: Probar con ID inexistente (debe retornar 404)
results.append(make_request(
    unit_id=999999,
    params=None,
    test_name="12. Probar con ID inexistente (debe retornar 404)"
))

# RESUMEN DE RESULTADOS
print("\n" + "=" * 80)
print("RESUMEN DE RESULTADOS")
print("=" * 80)

successful_tests = sum(1 for r in results if r.get('success', False))
total_tests = len(results)

print(f"\n[OK] Tests exitosos: {successful_tests}/{total_tests}")
print(f"[ERROR] Tests fallidos: {total_tests - successful_tests}/{total_tests}")

# Separar tests que fallaron por error vs tests esperados (como 404)
expected_failures = sum(1 for r in results if not r.get('success', False) and r.get('status_code') == 404)
actual_failures = total_tests - successful_tests - expected_failures

if expected_failures > 0:
    print(f"[INFO] Tests con fallo esperado (404): {expected_failures}")

if actual_failures > 0:
    print(f"[ERROR] Tests con fallos inesperados: {actual_failures}")

# Mostrar qué tests fallaron
failed_tests = []
for i, result in enumerate(results, 1):
    if not result.get('success', False) and result.get('status_code') != 404:
        failed_tests.append(i)

if failed_tests:
    print(f"\n[WARN] Tests que fallaron inesperadamente: {failed_tests}")
    print("       Revisar los mensajes de error arriba para más detalles")

# Validar estructura de respuestas exitosas
if successful_tests > 0:
    print("\n[STATS] Validación de estructura de respuestas:")
    all_missing_required = []
    for r in results:
        if r.get('success', False) and r.get('missing_required'):
            all_missing_required.extend(r.get('missing_required', []))
    
    if all_missing_required:
        unique_missing = set(all_missing_required)
        print(f"     Campos requeridos faltantes en alguna respuesta: {', '.join(unique_missing)}")
    else:
        print("     ✅ Todas las respuestas exitosas tienen los campos requeridos")

print("\n" + "=" * 80)
print("TESTING COMPLETADO")
print("=" * 80)

# Guardar resultados en archivo JSON para análisis
output_file = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump({
        'timestamp': datetime.now().isoformat(),
        'endpoint': ENDPOINT_BASE,
        'total_tests': total_tests,
        'successful_tests': successful_tests,
        'failed_tests': actual_failures,
        'expected_failures': expected_failures,
        'sample_unit_ids': sample_unit_ids,
        'results': results
    }, f, indent=2, ensure_ascii=False)

print(f"\n[SAVE] Resultados guardados en: {output_file}")

