#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests de integración para Create Housekeeping Work Order API
Realiza pruebas reales contra la API de TrackHS PMS
"""

import os
import sys
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import requests
from requests.auth import HTTPBasicAuth

# Configurar encoding para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Configuración de la API
API_URL = os.getenv('TRACKHS_API_URL', 'https://ihmvacations.trackhs.com/api/pms/housekeeping/work-orders')
AUTH_USER = os.getenv('TRACKHS_USER', '')
AUTH_PASS = os.getenv('TRACKHS_PASSWORD', '')

# Validar credenciales
if not AUTH_USER or not AUTH_PASS:
    print("=" * 80)
    print("ERROR: Credenciales no configuradas")
    print("=" * 80)
    print("Por favor, configura las variables de entorno:")
    print("  TRACKHS_USER: Usuario de la API")
    print("  TRACKHS_PASSWORD: Contraseña de la API")
    print("  TRACKHS_API_URL: (Opcional) URL de la API (default: https://ihmvacations.trackhs.com/api/pms/housekeeping/work-orders)")
    print()
    print("Ejemplo en Windows PowerShell:")
    print("  $env:TRACKHS_USER='tu_usuario'")
    print("  $env:TRACKHS_PASSWORD='tu_password'")
    print()
    print("Ejemplo en Linux/Mac:")
    print("  export TRACKHS_USER='tu_usuario'")
    print("  export TRACKHS_PASSWORD='tu_password'")
    sys.exit(1)

print("=" * 80)
print("TESTING CREATE HOUSEKEEPING WORK ORDER API - PRUEBAS REALES")
print("=" * 80)
print(f"API URL: {API_URL}")
print(f"Usuario: {AUTH_USER}")
print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)
print()

auth = HTTPBasicAuth(AUTH_USER, AUTH_PASS)

def build_payload(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Construye el payload JSON siguiendo la lógica del blueprint de Make.com
    """
    payload = {
        "scheduledAt": input_data["scheduledAt"],
        "unitId": input_data["unitId"]
    }
    
    # Campos opcionales - solo se agregan si tienen valor
    if input_data.get("unitBlockId") is not None:
        payload["unitBlockId"] = input_data["unitBlockId"]
    
    if input_data.get("isInspection") is not None and input_data["isInspection"]:
        payload["isInspection"] = input_data["isInspection"]
    
    if input_data.get("cleanTypeId") is not None:
        payload["cleanTypeId"] = input_data["cleanTypeId"]
    
    if input_data.get("userId") is not None:
        payload["userId"] = input_data["userId"]
    
    if input_data.get("reservationId") is not None:
        payload["reservationId"] = input_data["reservationId"]
    
    if input_data.get("vendorId") is not None:
        payload["vendorId"] = input_data["vendorId"]
    
    if input_data.get("isTurn") is not None:
        payload["isTurn"] = input_data["isTurn"]
    
    if input_data.get("chargeOwner") is not None:
        payload["chargeOwner"] = input_data["chargeOwner"]
    
    if input_data.get("comments"):
        # Escapar comillas y saltos de línea como en el blueprint
        comments = input_data["comments"].replace('"', '\\"').replace('\n', ' ').replace('\r', ' ')
        payload["comments"] = comments
    
    if input_data.get("cost") is not None:
        payload["cost"] = input_data["cost"]
    
    return payload

def make_request(input_data: Dict[str, Any], test_name: str) -> Dict[str, Any]:
    """
    Hace una petición real a la API de TrackHS
    
    Args:
        input_data: Datos de entrada según el blueprint
        test_name: Nombre del test
    """
    try:
        print(f"\n[TEST] {test_name}")
        
        # Construir payload
        payload = build_payload(input_data)
        print(f"[REQ] Payload: {json.dumps(payload, indent=2, ensure_ascii=False)}")
        
        # Hacer petición
        response = requests.post(
            API_URL,
            auth=auth,
            json=payload,
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            timeout=120
        )
        
        print(f"[RES] Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data_response = response.json()
            print(f"[OK] ✅ EXITO - Orden de trabajo creada")
            print(f"     ID: {data_response.get('id')}")
            print(f"     Status: {data_response.get('status')}")
            print(f"     Scheduled At: {data_response.get('scheduledAt')}")
            print(f"     Unit ID: {data_response.get('unitId')}")
            print(f"     Is Inspection: {data_response.get('isInspection')}")
            print(f"     Clean Type ID: {data_response.get('cleanTypeId')}")
            
            # Validar campos esperados según la documentación
            expected_fields = ['id', 'scheduledAt', 'unitId', 'status']
            missing_fields = [f for f in expected_fields if f not in data_response]
            
            if missing_fields:
                print(f"[WARN] ⚠️  Campos faltantes en respuesta: {missing_fields}")
            else:
                print(f"[OK] ✅ Estructura de respuesta válida")
            
            return {
                'success': True,
                'data': data_response,
                'status_code': response.status_code,
                'work_order_id': data_response.get('id')
            }
        else:
            error_text = response.text
            try:
                error_data = response.json()
                error_msg = error_data.get('detail', error_data.get('error', error_data.get('message', error_text)))
            except:
                error_msg = error_text[:500]
            
            print(f"[ERROR] ❌ Status Code: {response.status_code}")
            print(f"        Error: {error_msg}")
            
            return {
                'success': False,
                'status_code': response.status_code,
                'error': error_msg
            }
            
    except requests.exceptions.ConnectionError:
        print(f"[ERROR] ❌ No se pudo conectar a la API")
        print(f"        Verifica la URL: {API_URL}")
        return {
            'success': False,
            'error': 'Connection error'
        }
    except requests.exceptions.Timeout:
        print(f"[ERROR] ❌ Timeout esperando respuesta de la API")
        return {
            'success': False,
            'error': 'Timeout'
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
results: List[Dict[str, Any]] = []

print("\n" + "=" * 80)
print("INICIANDO CASOS DE PRUEBA")
print("=" * 80)

# Fechas para los tests
today = datetime.now()
scheduled_date = (today + timedelta(days=1)).strftime('%Y-%m-%d')

# Test 1: Caso básico con inspección (mínimo requerido)
print("\n" + "-" * 80)
results.append(make_request(
    input_data={
        "scheduledAt": scheduled_date,
        "unitId": 1,  # Ajustar según unidades disponibles
        "isInspection": True
    },
    test_name="1. Caso básico con inspección (mínimo requerido: scheduledAt, unitId, isInspection)"
))

# Test 2: Caso con cleanTypeId (en lugar de isInspection)
print("\n" + "-" * 80)
results.append(make_request(
    input_data={
        "scheduledAt": (today + timedelta(days=2)).strftime('%Y-%m-%d'),
        "unitId": 1,  # Ajustar según unidades disponibles
        "cleanTypeId": 1  # Ajustar según clean types disponibles
    },
    test_name="2. Caso con cleanTypeId (en lugar de isInspection)"
))

# Test 3: Caso con campos opcionales básicos
print("\n" + "-" * 80)
results.append(make_request(
    input_data={
        "scheduledAt": (today + timedelta(days=3)).strftime('%Y-%m-%d'),
        "unitId": 1,  # Ajustar según unidades disponibles
        "cleanTypeId": 1,  # Ajustar según clean types disponibles
        "comments": "Limpieza de prueba - comentarios de testing",
        "cost": 150.50
    },
    test_name="3. Caso con campos opcionales (comments, cost)"
))

# Test 4: Caso con isTurn y chargeOwner
print("\n" + "-" * 80)
results.append(make_request(
    input_data={
        "scheduledAt": (today + timedelta(days=4)).strftime('%Y-%m-%d'),
        "unitId": 1,  # Ajustar según unidades disponibles
        "isInspection": True,
        "isTurn": True,
        "chargeOwner": True,
        "comments": "Limpieza de turno - debe cobrarse al propietario"
    },
    test_name="4. Caso con isTurn y chargeOwner (limpieza de turno)"
))

# Test 5: Caso completo con todos los campos opcionales
print("\n" + "-" * 80)
results.append(make_request(
    input_data={
        "scheduledAt": (today + timedelta(days=5)).strftime('%Y-%m-%d'),
        "unitId": 1,  # Ajustar según unidades disponibles
        "cleanTypeId": 1,  # Ajustar según clean types disponibles
        "userId": 1,  # Ajustar según usuarios disponibles
        "reservationId": None,  # Opcional, puede ser None
        "vendorId": None,  # Opcional, puede ser None
        "isTurn": False,
        "chargeOwner": False,
        "comments": "Limpieza completa de prueba con todos los campos opcionales.\nSegunda línea de comentarios.",
        "cost": 250.75
    },
    test_name="5. Caso completo con todos los campos opcionales"
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
    print("\nDetalles de tests fallidos:")
    for i, result in enumerate(results, 1):
        if not result.get('success', False):
            print(f"  - Test {i}: {result.get('error', 'Unknown error')}")
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
        'endpoint': API_URL,
        'total_tests': total_tests,
        'successful_tests': successful_tests,
        'failed_tests': failed_tests,
        'results': results
    }, f, indent=2, ensure_ascii=False)

print(f"\n[SAVE] Resultados guardados en: {output_file}")

