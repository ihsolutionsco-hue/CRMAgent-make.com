#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de pruebas para la API de TrackHS - Get Units Availability
Prueba diferentes casos de uso para validar la implementación del JSON
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
    print(f"   Buscando .env en: {env_path}")
    sys.exit(1)

# Construir URL base
if not API_BASE_URL.endswith('/api'):
    API_BASE_URL = f"{API_BASE_URL.rstrip('/')}/api"

ENDPOINT = f"{API_BASE_URL}/pms/units/search"

print("=" * 80)
print("TESTING API TRACKHS - GET UNITS AVAILABILITY")
print("=" * 80)
print(f"Endpoint: {ENDPOINT}")
print(f"Usuario: {API_USERNAME[:20]}...")
print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)
print()

# Configurar autenticación
auth = HTTPBasicAuth(API_USERNAME, API_PASSWORD)

# Helper para hacer requests
def make_request(params=None, test_name="", expected_status=200):
    """Hace una petición a la API y muestra los resultados"""
    try:
        print(f"\n[TEST] {test_name}")
        # Manejar params como dict o lista de tuplas
        if params:
            if isinstance(params, list):
                # Lista de tuplas (para arrays)
                clean_params = params
                print(f"[REQ] Parametros (array): {params}")
            else:
                # Dict normal
                clean_params = {k: v for k, v in params.items() if v is not None and v != ''}
                print(f"[REQ] Parametros: {clean_params}")
        else:
            clean_params = None
            print(f"[REQ] Sin parametros")
        
        response = requests.get(
            ENDPOINT,
            auth=auth,
            params=params,
            headers={'Accept': 'application/json'},
            timeout=30
        )
        
        print(f"[RES] Status Code: {response.status_code}")
        
        if response.status_code == expected_status:
            if response.status_code == 200:
                data = response.json()
                
                # Extraer información útil
                count = data.get('count', 'N/A')
                results = data.get('results', [])
                
                print(f"[OK] EXITO")
                print(f"     Total de unidades disponibles: {count}")
                print(f"     Resultados en array: {len(results)}")
                
                # Mostrar primeros 3 resultados como muestra
                if results:
                    print(f"\n     Primeros resultados (muestra):")
                    for i, result in enumerate(results[:3], 1):
                        unit_id = result.get('id', 'N/A')
                        unit_name = result.get('name', 'N/A')
                        unit_type = result.get('type', 'N/A')
                        unit_count = result.get('count', 'N/A')
                        print(f"        {i}. ID: {unit_id} | Nombre: {unit_name} | Tipo: {unit_type} | Disponibles: {unit_count}")
                
                # Validar estructura de respuesta
                required_fields = ['count', 'results']
                print(f"\n     Validacion de estructura de respuesta:")
                missing_required = []
                for field in required_fields:
                    has_field = field in data
                    status = "[OK]" if has_field else "[MISS]"
                    print(f"        {status} {field}: {has_field}")
                    if not has_field:
                        missing_required.append(field)
                
                # Validar estructura de resultados
                if results:
                    print(f"\n     Validacion de estructura de resultados:")
                    sample_result = results[0]
                    result_fields = ['id', 'name', 'type', 'count']
                    
                    present_fields = []
                    missing_result_fields = []
                    for field in result_fields:
                        has_field = field in sample_result
                        if has_field:
                            present_fields.append(field)
                        else:
                            missing_result_fields.append(field)
                    
                    print(f"        Campos presentes: {len(present_fields)}/{len(result_fields)}")
                    if present_fields:
                        print(f"        Campos: {', '.join(present_fields)}")
                    if missing_result_fields:
                        print(f"        [WARN] Campos faltantes: {', '.join(missing_result_fields)}")
                
                return {
                    'success': True,
                    'data': data,
                    'count': count,
                    'results_count': len(results),
                    'missing_required': missing_required,
                    'params': dict(clean_params) if isinstance(clean_params, list) else (clean_params if params else {})
                }
            else:
                # Error esperado (422, 400, etc.)
                try:
                    error_data = response.json()
                    print(f"[OK] Error esperado recibido")
                    print(f"     Error: {json.dumps(error_data, indent=2, ensure_ascii=False)[:500]}")
                    return {
                        'success': True,  # Éxito porque esperábamos este error
                        'expected_error': True,
                    'status_code': response.status_code,
                    'error': error_data,
                    'params': dict(clean_params) if isinstance(clean_params, list) else (clean_params if params else {})
                }
                except:
                    print(f"[OK] Error esperado recibido")
                    print(f"     Response: {response.text[:500]}")
                    return {
                        'success': True,
                        'expected_error': True,
                    'status_code': response.status_code,
                    'error': response.text[:500],
                    'params': dict(clean_params) if isinstance(clean_params, list) else (clean_params if params else {})
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
            # Error inesperado
            print(f"[ERROR] Status Code inesperado: {response.status_code} (esperado: {expected_status})")
            try:
                error_data = response.json()
                print(f"        Error: {json.dumps(error_data, indent=2, ensure_ascii=False)[:500]}")
                return {
                    'success': False,
                    'status_code': response.status_code,
                    'expected_status': expected_status,
                    'error': error_data,
                    'params': clean_params if params else {}
                }
            except:
                print(f"        Response: {response.text[:500]}")
                return {
                    'success': False,
                    'status_code': response.status_code,
                    'expected_status': expected_status,
                    'error': response.text[:500],
                    'params': clean_params if params else {}
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

# Fechas de prueba
today = datetime.now()
next_week = today + timedelta(days=7)
next_month = today + timedelta(days=30)

date_format = '%Y-%m-%d'
arrival_date = next_week.strftime(date_format)
departure_date = next_month.strftime(date_format)

print("\n" + "=" * 80)
print("INICIANDO CASOS DE PRUEBA")
print("=" * 80)
print(f"Fechas de prueba: arrival={arrival_date}, departure={departure_date}")
print("=" * 80)

# Test 1: Caso básico - Solo fechas requeridas
results.append(make_request(
    params={'arrival': arrival_date, 'departure': departure_date},
    test_name="1. Caso básico - Solo fechas requeridas (arrival + departure)"
))

# Test 2: Sin fechas (debe fallar con 422)
results.append(make_request(
    params=None,
    test_name="2. Sin parámetros (debe fallar con 422 - fechas requeridas)",
    expected_status=422
))

# Test 3: Solo arrival (debe fallar con 422)
results.append(make_request(
    params={'arrival': arrival_date},
    test_name="3. Solo arrival (debe fallar con 422 - falta departure)",
    expected_status=422
))

# Test 4: Solo departure (debe fallar con 422)
results.append(make_request(
    params={'departure': departure_date},
    test_name="4. Solo departure (debe fallar con 422 - falta arrival)",
    expected_status=422
))

# Test 5: Fechas con formato incorrecto (debe fallar con 422)
results.append(make_request(
    params={'arrival': '2025/10/27', 'departure': departure_date},  # Formato incorrecto
    test_name="5. Fecha con formato incorrecto (debe fallar con 422)",
    expected_status=422
))

# Test 6: Fechas con useSoftDates=0
results.append(make_request(
    params={'arrival': arrival_date, 'departure': departure_date, 'useSoftDates': 0},
    test_name="6. Con useSoftDates=0 (fechas duras)"
))

# Test 7: Fechas con useSoftDates=1
results.append(make_request(
    params={'arrival': arrival_date, 'departure': departure_date, 'useSoftDates': 1},
    test_name="7. Con useSoftDates=1 (fechas suaves)"
))

# Test 8: Con exclude (CSV de reservation IDs)
results.append(make_request(
    params={'arrival': arrival_date, 'departure': departure_date, 'exclude': '123,456,789'},
    test_name="8. Con exclude (CSV de reservation IDs)"
))

# Test 9: Con unitTypeId como array (múltiples parámetros)
results.append(make_request(
    params=[
        ('arrival', arrival_date),
        ('departure', departure_date),
        ('unitTypeId', '1'),
        ('unitTypeId', '2'),
        ('unitTypeId', '3')
    ],
    test_name="9. Con unitTypeId como array (múltiples parámetros)"
))

# Test 10: Con nodeId como array (múltiples parámetros)
results.append(make_request(
    params=[
        ('arrival', arrival_date),
        ('departure', departure_date),
        ('nodeId', '1'),
        ('nodeId', '2')
    ],
    test_name="10. Con nodeId como array (múltiples parámetros)"
))

# Test 11: Combinación completa de parámetros
results.append(make_request(
    params=[
        ('arrival', arrival_date),
        ('departure', departure_date),
        ('useSoftDates', '1'),
        ('exclude', '123,456'),
        ('unitTypeId', '1'),
        ('unitTypeId', '2'),
        ('nodeId', '1')
    ],
    test_name="11. Combinación completa (todos los parámetros)"
))

# Test 12: Fechas muy cercanas (1 día)
tomorrow = (today + timedelta(days=1)).strftime(date_format)
day_after = (today + timedelta(days=2)).strftime(date_format)
results.append(make_request(
    params={'arrival': tomorrow, 'departure': day_after},
    test_name="12. Fechas muy cercanas (1 día de diferencia)"
))

# Test 13: Fechas en el pasado
past_date = (today - timedelta(days=30)).strftime(date_format)
past_date2 = (today - timedelta(days=20)).strftime(date_format)
results.append(make_request(
    params={'arrival': past_date, 'departure': past_date2},
    test_name="13. Fechas en el pasado"
))

# Test 14: Fechas muy lejanas (6 meses)
far_future = (today + timedelta(days=180)).strftime(date_format)
far_future2 = (today + timedelta(days=190)).strftime(date_format)
results.append(make_request(
    params={'arrival': far_future, 'departure': far_future2},
    test_name="14. Fechas muy lejanas (6 meses)"
))

# Test 15: Con exclude vacío (debe ignorar)
results.append(make_request(
    params={'arrival': arrival_date, 'departure': departure_date, 'exclude': ''},
    test_name="15. Con exclude vacío (debe ignorar)"
))

# RESUMEN
print("\n" + "=" * 80)
print("RESUMEN DE RESULTADOS")
print("=" * 80)

successful_tests = [r for r in results if r.get('success')]
failed_tests = [r for r in results if not r.get('success')]
expected_errors = [r for r in results if r.get('success') and r.get('expected_error')]

print(f"\nTotal de tests: {len(results)}")
print(f"Exitosos (200 OK): {len([r for r in successful_tests if not r.get('expected_error')])}")
print(f"Errores esperados (422/400): {len(expected_errors)}")
print(f"Fallidos (errores inesperados): {len(failed_tests)}")

if successful_tests and not expected_errors:
    print("\n[ANALISIS DE RESULTADOS]")
    availability_counts = []
    for result in successful_tests:
        if not result.get('expected_error') and result.get('count') != 'N/A':
            try:
                availability_counts.append(int(result.get('count', 0)))
            except:
                pass
    
    if availability_counts:
        print(f"Unidades disponibles encontradas:")
        print(f"  - Promedio: {sum(availability_counts) / len(availability_counts):.1f}")
        print(f"  - Minimo: {min(availability_counts)}")
        print(f"  - Maximo: {max(availability_counts)}")
        print(f"  - Total de tests con disponibilidad: {len(availability_counts)}")

if expected_errors:
    print("\n[ERRORES ESPERADOS (Validación Correcta)]")
    for i, result in enumerate(expected_errors, 1):
        status = result.get('status_code', 'N/A')
        error_msg = str(result.get('error', ''))[:100]
        print(f"  {i}. Status {status}: {error_msg}")

if failed_tests:
    print("\n[TESTS FALLIDOS (Errores Inesperados)]")
    for i, result in enumerate(failed_tests, 1):
        status = result.get('status_code', 'N/A')
        error = result.get('error', 'Unknown error')
        print(f"  {i}. Status {status}: {str(error)[:100]}")

# Validación del JSON
print("\n" + "=" * 80)
print("VALIDACION DEL JSON IMPLEMENTADO")
print("=" * 80)

# Verificar que los parámetros requeridos funcionan
arrival_departure_tests = [r for r in successful_tests 
                          if not r.get('expected_error') 
                          and 'arrival' in str(r.get('params', {})) 
                          and 'departure' in str(r.get('params', {}))]

if arrival_departure_tests:
    print("\n✅ Parámetros requeridos (arrival, departure) funcionan correctamente")
else:
    print("\n❌ Parámetros requeridos no funcionan correctamente")

# Verificar parámetros opcionales
optional_params = ['useSoftDates', 'exclude', 'unitTypeId', 'nodeId']
optional_tests = {}
for param in optional_params:
    param_tests = [r for r in successful_tests 
                   if not r.get('expected_error') 
                   and param in str(r.get('params', {}))]
    if param_tests:
        optional_tests[param] = True
        print(f"✅ Parámetro opcional '{param}' funciona correctamente")
    else:
        optional_tests[param] = False
        print(f"⚠️  Parámetro opcional '{param}' no probado o no funciona")

# Verificar validación de errores
if expected_errors:
    print("\n✅ Validación de errores funciona (422 cuando faltan fechas)")

# Guardar resultados
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
results_file = f"test_results_{timestamp}.json"

# Limpiar datos para guardar (remover datos completos por tamaño)
clean_results = []
for r in results:
    clean_r = {
        'success': r.get('success'),
        'status_code': r.get('status_code'),
        'expected_status': r.get('expected_status'),
        'expected_error': r.get('expected_error', False),
        'count': r.get('count'),
        'results_count': r.get('results_count', 0),
        'params': r.get('params', {})
    }
    if not r.get('success') or r.get('expected_error'):
        clean_r['error'] = str(r.get('error', ''))[:200]
    clean_results.append(clean_r)

with open(results_file, 'w', encoding='utf-8') as f:
    json.dump({
        'timestamp': datetime.now().isoformat(),
        'endpoint': ENDPOINT,
        'total_tests': len(results),
        'successful_tests': len(successful_tests),
        'expected_errors': len(expected_errors),
        'failed_tests': len(failed_tests),
        'optional_params_working': optional_tests,
        'results': clean_results
    }, f, indent=2, ensure_ascii=False)

print(f"\n[GUARDADO] Resultados guardados en: {results_file}")
print("=" * 80)

