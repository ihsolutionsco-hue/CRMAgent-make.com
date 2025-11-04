#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests de validación para Create Contact API
Valida que las requests cumplan con la documentación OpenAPI
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, Any, List
import requests
from requests.auth import HTTPBasicAuth

# Configurar encoding para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Configuración
MOCK_SERVER_URL = os.getenv('MOCK_SERVER_URL', 'http://localhost:5000')
ENDPOINT = f"{MOCK_SERVER_URL}/api/crm/contacts"

# Autenticación mock (puede ser cualquier valor en el mock)
AUTH_USER = "test_user"
AUTH_PASS = "test_pass"

print("=" * 80)
print("TESTING CREATE CONTACT API - VALIDACIÓN CONTRA DOCUMENTACIÓN")
print("=" * 80)
print(f"Mock Server: {MOCK_SERVER_URL}")
print(f"Endpoint: {ENDPOINT}")
print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)
print()

auth = HTTPBasicAuth(AUTH_USER, AUTH_PASS)

def make_request(data: Dict[str, Any], test_name: str, use_json: bool = True, expect_error: bool = False) -> Dict[str, Any]:
    """
    Hace una petición al mock server y valida la respuesta
    
    Args:
        data: Datos a enviar
        test_name: Nombre del test
        use_json: Si True, envía como JSON body; si False, como query parameters
        expect_error: Si True, espera un error 400 (test de validación negativa)
    """
    try:
        print(f"\n[TEST] {test_name}")
        print(f"[REQ] Datos: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        if use_json:
            # Enviar como JSON body
            response = requests.post(
                ENDPOINT,
                auth=auth,
                json=data,
                headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
                timeout=10
            )
        else:
            # Enviar como query parameters (como Make.com)
            response = requests.post(
                ENDPOINT,
                auth=auth,
                params=data,
                headers={'Accept': 'application/json'},
                timeout=10
            )
        
        print(f"[RES] Status Code: {response.status_code}")
        
        # Si es un test de validación negativa, esperamos un error 400
        if expect_error:
            if response.status_code == 400:
                error_data = response.json() if response.text else {}
                print(f"[OK] ✅ EXITO - Validación funcionó correctamente (rechazó datos inválidos)")
                print(f"     Error esperado: {error_data.get('error', response.text[:200])}")
                return {
                    'success': True,
                    'status_code': response.status_code,
                    'error': error_data.get('error', response.text)
                }
            else:
                print(f"[ERROR] ❌ Se esperaba error 400 pero se recibió {response.status_code}")
                if response.status_code == 201:
                    print(f"        La validación NO funcionó - se aceptaron datos inválidos")
                return {
                    'success': False,
                    'status_code': response.status_code,
                    'error': f'Expected 400 but got {response.status_code}'
                }
        
        # Test positivo - esperamos éxito 201
        if response.status_code == 201:
            data_response = response.json()
            print(f"[OK] ✅ EXITO - Contacto creado")
            print(f"     ID: {data_response.get('id')}")
            print(f"     Nombre: {data_response.get('firstName')} {data_response.get('lastName')}")
            print(f"     Email: {data_response.get('primaryEmail')}")
            print(f"     Creado: {data_response.get('createdAt')}")
            
            # Validar estructura de respuesta según OpenAPI
            required_fields = [
                'id', 'firstName', 'lastName', 'primaryEmail', 
                'createdAt', 'updatedAt', '_links'
            ]
            missing_fields = [f for f in required_fields if f not in data_response]
            
            if missing_fields:
                print(f"[WARN] ⚠️  Campos faltantes en respuesta: {missing_fields}")
            else:
                print(f"[OK] ✅ Estructura de respuesta válida según OpenAPI")
            
            return {
                'success': True,
                'data': data_response,
                'status_code': response.status_code
            }
        else:
            error_data = response.json() if response.text else {}
            print(f"[ERROR] ❌ Status Code: {response.status_code}")
            print(f"        Error: {error_data.get('error', response.text[:200])}")
            return {
                'success': False,
                'status_code': response.status_code,
                'error': error_data.get('error', response.text)
            }
            
    except requests.exceptions.ConnectionError:
        print(f"[ERROR] ❌ No se pudo conectar al servidor mock")
        print(f"        Asegúrate de que el servidor esté corriendo en {MOCK_SERVER_URL}")
        print(f"        Ejecuta: python mock_server.py")
        return {
            'success': False,
            'error': 'Connection error'
        }
    except Exception as e:
        print(f"[ERROR] ❌ Error inesperado: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

# CASOS DE PRUEBA
results: List[Dict[str, Any]] = []

print("\n" + "=" * 80)
print("INICIANDO CASOS DE PRUEBA")
print("=" * 80)

# Test 1: Caso básico válido (mínimo requerido)
results.append(make_request(
    data={
        "firstName": "Juan",
        "lastName": "Pérez",
        "primaryEmail": "juan.perez@example.com",
        "cellPhone": "+1234567890"
    },
    test_name="1. Caso básico válido (mínimo requerido)",
    use_json=True
))

# Test 2: Caso completo con todos los campos
results.append(make_request(
    data={
        "firstName": "María",
        "lastName": "González",
        "primaryEmail": "maria.gonzalez@example.com",
        "secondaryEmail": "maria.alternativo@example.com",
        "homePhone": "+1234567891",
        "cellPhone": "+1234567892",
        "workPhone": "+1234567893",
        "otherPhone": "+1234567894",
        "fax": "+1234567895",
        "streetAddress": "123 Main St",
        "country": "US",
        "postalCode": "12345",
        "region": "CA",
        "locality": "Los Angeles",
        "extendedAddress": "Apt 4B",
        "notes": "Cliente preferente",
        "anniversary": "06-15",
        "birthdate": "03-20",
        "isBlacklist": False,
        "tags": [{"id": 1}],
        "references": [{"reference": "REF001", "salesLinkId": 123, "channelId": 456}],
        "customValues": {"custom_1": "valor1", "custom_2": ["valor2", "valor3"]}
    },
    test_name="2. Caso completo con todos los campos",
    use_json=True
))

# Test 3: Validación - Email inválido
results.append(make_request(
    data={
        "firstName": "Test",
        "lastName": "User",
        "primaryEmail": "email-invalido-sin-arroba",
        "cellPhone": "+1234567890"
    },
    test_name="3. Validación - Email inválido (debe rechazar)",
    use_json=True,
    expect_error=True
))

# Test 4: Validación - Teléfono inválido
results.append(make_request(
    data={
        "firstName": "Test",
        "lastName": "User",
        "primaryEmail": "test@example.com",
        "cellPhone": "123"  # Muy corto para E.164
    },
    test_name="4. Validación - Teléfono inválido (debe rechazar)",
    use_json=True,
    expect_error=True
))

# Test 5: Validación - Faltan campos requeridos
results.append(make_request(
    data={
        "firstName": "Test",
        "lastName": "User"
        # Falta email, teléfono, etc.
    },
    test_name="5. Validación - Faltan campos requeridos (debe rechazar)",
    use_json=True,
    expect_error=True
))

# Test 6: Validación - Fecha inválida (anniversary)
results.append(make_request(
    data={
        "firstName": "Test",
        "lastName": "User",
        "primaryEmail": "test@example.com",
        "cellPhone": "+1234567890",
        "anniversary": "13-45"  # Mes inválido
    },
    test_name="6. Validación - Fecha anniversary inválida (debe rechazar)",
    use_json=True,
    expect_error=True
))

# Test 7: Validación - Country code inválido
results.append(make_request(
    data={
        "firstName": "Test",
        "lastName": "User",
        "primaryEmail": "test@example.com",
        "cellPhone": "+1234567890",
        "country": "USA"  # Debe ser 2 caracteres
    },
    test_name="7. Validación - Country code inválido (debe rechazar)",
    use_json=True,
    expect_error=True
))

# Test 8: Validación - ACH routing number inválido
results.append(make_request(
    data={
        "firstName": "Test",
        "lastName": "User",
        "primaryEmail": "test@example.com",
        "cellPhone": "+1234567890",
        "achRoutingNumber": "12345"  # Debe ser 9 dígitos
    },
    test_name="8. Validación - ACH routing number inválido (debe rechazar)",
    use_json=True,
    expect_error=True
))

# Test 9: Validación - Longitud máxima excedida (firstName)
results.append(make_request(
    data={
        "firstName": "A" * 33,  # Máximo 32
        "lastName": "User",
        "primaryEmail": "test@example.com",
        "cellPhone": "+1234567890"
    },
    test_name="9. Validación - Longitud máxima excedida (firstName) (debe rechazar)",
    use_json=True,
    expect_error=True
))

# Test 10: Caso con query parameters (como Make.com)
results.append(make_request(
    data={
        "firstName": "Pedro",
        "lastName": "Martínez",
        "primaryEmail": "pedro.martinez@example.com",
        "cellPhone": "+1234567890",
        "tags": json.dumps([{"id": 1}])  # Como string JSON
    },
    test_name="10. Caso con query parameters (formato Make.com)",
    use_json=False
))

# Test 11: Caso válido solo con email (sin teléfono)
results.append(make_request(
    data={
        "firstName": "Ana",
        "lastName": "López",
        "primaryEmail": "ana.lopez@example.com"
    },
    test_name="11. Caso válido solo con email (sin teléfono)",
    use_json=True
))

# Test 12: Caso válido solo con teléfono (sin email)
results.append(make_request(
    data={
        "firstName": "Carlos",
        "lastName": "Rodríguez",
        "cellPhone": "+1234567890"
    },
    test_name="12. Caso válido solo con teléfono (sin email)",
    use_json=True
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

