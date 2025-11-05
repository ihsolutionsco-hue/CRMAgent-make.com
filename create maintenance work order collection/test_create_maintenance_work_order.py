#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de pruebas para la API de TrackHS - Create Maintenance Work Order
Prueba 3 casos de uso diferentes para validar la implementación
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

ENDPOINT = f"{API_BASE_URL}/pms/maintenance/work-orders"

print("=" * 80)
print("TESTING API TRACKHS - CREATE MAINTENANCE WORK ORDER")
print("=" * 80)
print(f"Endpoint: {ENDPOINT}")
print(f"Usuario: {API_USERNAME[:20]}...")
print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)
print()

# Configurar autenticación
auth = HTTPBasicAuth(API_USERNAME, API_PASSWORD)

# Helper para obtener un unitId válido
def get_valid_unit_id():
    """Obtiene un unitId válido de la API"""
    try:
        units_url = f"{API_BASE_URL}/pms/units?size=1"
        response = requests.get(units_url, auth=auth, timeout=10)
        if response.status_code == 200:
            data = response.json()
            items = data.get('_embedded', {}).get('items', [])
            if items:
                unit_id = items[0].get('id')
                print(f"[INFO] Unit ID obtenido: {unit_id}")
                return unit_id
        print("[WARN] No se pudo obtener unitId, usando valor por defecto")
        return None
    except Exception as e:
        print(f"[WARN] Error al obtener unitId: {e}")
        return None

# Helper para hacer requests
def make_request(json_data=None, test_name=""):
    """Hace una petición a la API y muestra los resultados"""
    try:
        print(f"\n[TEST] {test_name}")
        print("-" * 80)
        
        if json_data:
            print(f"[REQ] JSON Body: {json.dumps(json_data, indent=2, ensure_ascii=False)}")
        
        # Enviar como JSON body (la API espera application/json según la documentación)
        response = requests.post(
            ENDPOINT,
            auth=auth,
            json=json_data,
            headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"[RES] Status Code: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"[OK] ✅ EXITO - Orden de trabajo creada")
            print(f"     ID: {data.get('id')}")
            print(f"     Summary: {data.get('summary')}")
            print(f"     Priority: {data.get('priority')} (1=trivial, 2=low, 3=medium, 4=high, 5=critical)")
            print(f"     Status: {data.get('status')}")
            print(f"     Estimated Cost: {data.get('estimatedCost')}")
            print(f"     Estimated Time: {data.get('estimatedTime')} minutos")
            print(f"     Date Received: {data.get('dateReceived')}")
            if data.get('unitId'):
                print(f"     Unit ID: {data.get('unitId')}")
            if data.get('vendorId'):
                print(f"     Vendor ID: {data.get('vendorId')}")
            print(f"     Created At: {data.get('createdAt')}")
            
            # Validar campos obligatorios en respuesta
            required_fields = ['id', 'dateReceived', 'priority', 'status', 'summary', 'estimatedCost', 'estimatedTime']
            missing_fields = [f for f in required_fields if f not in data]
            
            if missing_fields:
                print(f"[WARN] ⚠️  Campos faltantes en respuesta: {missing_fields}")
            else:
                print(f"[OK] ✅ Todos los campos obligatorios presentes en respuesta")
            
            return {
                'success': True,
                'data': data,
                'status_code': response.status_code
            }
        else:
            error_data = {}
            try:
                error_data = response.json()
            except:
                error_data = {'detail': response.text[:500]}
            
            print(f"[ERROR] ❌ Status Code: {response.status_code}")
            if 'validation_messages' in error_data:
                print(f"        Validation Errors: {error_data.get('validation_messages')}")
            if 'detail' in error_data:
                print(f"        Detail: {error_data.get('detail')}")
            if 'title' in error_data:
                print(f"        Title: {error_data.get('title')}")
            
            return {
                'success': False,
                'status_code': response.status_code,
                'error': error_data
            }
            
    except requests.exceptions.ConnectionError:
        print(f"[ERROR] ❌ No se pudo conectar al servidor")
        return {
            'success': False,
            'error': 'Connection error'
        }
    except Exception as e:
        print(f"[ERROR] ❌ Error inesperado: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'error': str(e)
        }

# CASOS DE PRUEBA
results = []

print("\n" + "=" * 80)
print("INICIANDO CASOS DE PRUEBA")
print("=" * 80)

# Obtener un unitId válido
print("\n[INFO] Obteniendo unitId válido...")
unit_id = get_valid_unit_id()
if not unit_id:
    print("[ERROR] No se pudo obtener un unitId válido. Los tests pueden fallar.")
    unit_id = 1  # Valor por defecto para intentar

# Obtener fecha actual en formato ISO 8601
today = datetime.now().date()
date_received = today.isoformat()
date_scheduled = (today + timedelta(days=7)).isoformat()

# TEST 1: Caso básico válido (mínimo requerido)
print("\n" + "=" * 80)
results.append(make_request(
    json_data={
        "dateReceived": date_received,
        "priority": 3,  # medium (Media)
        "status": "open",
        "summary": "Reparación de aire acondicionado - Test básico",
        "estimatedCost": 150.00,
        "estimatedTime": 120,  # 2 horas en minutos
        "unitId": unit_id  # Requerido por la API
    },
    test_name="1. Caso básico válido (mínimo requerido)"
))

# TEST 2: Caso completo con campos opcionales
print("\n" + "=" * 80)
results.append(make_request(
    json_data={
        "dateReceived": date_received,
        "priority": 4,  # high (Alta)
        "status": "not-started",
        "summary": "Mantenimiento completo de unidad - Test completo",
        "estimatedCost": 500.75,
        "estimatedTime": 240,  # 4 horas
        "unitId": unit_id,
        "dateScheduled": date_scheduled,
        "description": "Descripción detallada del trabajo a realizar. Incluye revisión de sistemas eléctricos, plomería y limpieza profunda.",
        "source": "API Test",
        "sourceName": "Sistema de Pruebas",
        "sourcePhone": "+1234567890",
        "referenceNumber": f"WO-TEST-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "blockCheckin": False
    },
    test_name="2. Caso completo con campos opcionales"
))

# TEST 3: Caso con prioridad baja y estado in-progress
print("\n" + "=" * 80)
results.append(make_request(
    json_data={
        "dateReceived": date_received,
        "priority": 2,  # low (Baja)
        "status": "in-progress",
        "summary": "Limpieza rutinaria - Test prioridad baja",
        "estimatedCost": 50.00,
        "estimatedTime": 60,  # 1 hora
        "unitId": unit_id,
        "description": "Limpieza general de la unidad después de la salida del huésped.",
        "workPerformed": "Trabajo ya iniciado - limpieza en progreso",
        "actualTime": 30,  # 30 minutos ya gastados
        "source": "Front Desk"
    },
    test_name="3. Caso con prioridad baja y estado in-progress"
))

# RESUMEN DE RESULTADOS
print("\n" + "=" * 80)
print("RESUMEN DE RESULTADOS")
print("=" * 80)

successful_tests = sum(1 for r in results if r.get('success', False))
total_tests = len(results)
failed_tests = total_tests - successful_tests

print(f"\n[OK] Tests exitosos: {successful_tests}/{total_tests}")
if failed_tests > 0:
    print(f"[ERROR] Tests fallidos: {failed_tests}/{total_tests}")
    # Mostrar qué tests fallaron
    for i, result in enumerate(results, 1):
        if not result.get('success', False):
            print(f"        - Test {i} falló")
            if 'error' in result:
                print(f"          Error: {result.get('error')}")
else:
    print(f"[OK] ✅ TODOS LOS TESTS PASARON EXITOSAMENTE")

print("\n" + "=" * 80)
print("TESTING COMPLETADO")
print("=" * 80)

# Guardar resultados
output_file = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump({
        'timestamp': datetime.now().isoformat(),
        'endpoint': ENDPOINT,
        'total_tests': total_tests,
        'successful_tests': successful_tests,
        'results': results
    }, f, indent=2, ensure_ascii=False)

print(f"\n[SAVE] Resultados guardados en: {output_file}")

