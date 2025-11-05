#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests de validación para Create Reservation API
Valida que las requests cumplan con la documentación OpenAPI
"""

import os
import sys
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List
import requests
from requests.auth import HTTPBasicAuth

# Configurar encoding para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Configuración
MOCK_SERVER_URL = os.getenv('MOCK_SERVER_URL', 'http://localhost:5001')
ENDPOINT = f"{MOCK_SERVER_URL}/api/pms/reservations"

# Autenticación mock (puede ser cualquier valor en el mock)
AUTH_USER = "test_user"
AUTH_PASS = "test_pass"

print("=" * 80)
print("TESTING CREATE RESERVATION API - VALIDACIÓN CONTRA DOCUMENTACIÓN")
print("=" * 80)
print(f"Mock Server: {MOCK_SERVER_URL}")
print(f"Endpoint: {ENDPOINT}")
print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)
print()

auth = HTTPBasicAuth(AUTH_USER, AUTH_PASS)

def make_request(data: Dict[str, Any], test_name: str, expect_error: bool = False) -> Dict[str, Any]:
    """
    Hace una petición al mock server usando query strings (como Make.com)
    
    Args:
        data: Datos a enviar
        test_name: Nombre del test
        expect_error: Si True, espera un error 422 (test de validación negativa)
    """
    try:
        print(f"\n[TEST] {test_name}")
        print(f"[REQ] Datos: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        # Enviar como query parameters (como Make.com)
        response = requests.post(
            ENDPOINT,
            auth=auth,
            params=data,
            headers={'Accept': 'application/json'},
            timeout=10
        )
        
        print(f"[RES] Status Code: {response.status_code}")
        
        # Si es un test de validación negativa, esperamos un error 422
        if expect_error:
            if response.status_code in [400, 422]:
                error_data = response.json() if response.text else {}
                print(f"[OK] ✅ EXITO - Validación funcionó correctamente (rechazó datos inválidos)")
                print(f"     Error esperado: {error_data.get('detail', error_data.get('error', response.text[:200]))}")
                return {
                    'success': True,
                    'status_code': response.status_code,
                    'error': error_data.get('detail', error_data.get('error', response.text))
                }
            else:
                print(f"[ERROR] ❌ Se esperaba error 400/422 pero se recibió {response.status_code}")
                if response.status_code == 200:
                    print(f"        La validación NO funcionó - se aceptaron datos inválidos")
                return {
                    'success': False,
                    'status_code': response.status_code,
                    'error': f'Expected 400/422 but got {response.status_code}'
                }
        
        # Test positivo - esperamos éxito 200
        if response.status_code == 200:
            data_response = response.json()
            print(f"[OK] ✅ EXITO - Reserva creada")
            print(f"     ID: {data_response.get('id')}")
            print(f"     Unit ID: {data_response.get('unitId')}")
            print(f"     Arrival: {data_response.get('arrivalDate')}")
            print(f"     Departure: {data_response.get('departureDate')}")
            print(f"     Nights: {data_response.get('nights')}")
            print(f"     Status: {data_response.get('status')}")
            print(f"     UUID: {data_response.get('uuid')}")
            
            # Validar estructura de respuesta según OpenAPI
            required_fields = [
                'id', 'unitId', 'arrivalDate', 'departureDate', 
                'nights', 'status', 'uuid', 'contactId', 'folioId',
                'quoteBreakdown', 'createdAt', '_links'
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
            print(f"        Error: {error_data.get('detail', error_data.get('error', response.text[:200]))}")
            return {
                'success': False,
                'status_code': response.status_code,
                'error': error_data.get('detail', error_data.get('error', response.text))
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
arrival_date = (today + timedelta(days=7)).strftime('%Y-%m-%d')
departure_date = (today + timedelta(days=10)).strftime('%Y-%m-%d')

# Test 1: Caso básico válido (mínimo requerido)
results.append(make_request(
    data={
        "unitId": "1",
        "arrivalDate": arrival_date,
        "departureDate": departure_date
    },
    test_name="1. Caso básico válido (mínimo requerido - solo fechas y unitId)"
))

# Test 2: Caso con contactId
results.append(make_request(
    data={
        "unitId": "2",
        "arrivalDate": arrival_date,
        "departureDate": departure_date,
        "contactId": "123"
    },
    test_name="2. Caso con contactId existente"
))

# Test 3: Caso con contact (objeto JSON como string)
contact_json = json.dumps({
    "firstName": "María",
    "lastName": "González",
    "primaryEmail": "maria.gonzalez@example.com",
    "cellPhone": "+1234567890"
})
results.append(make_request(
    data={
        "unitId": "3",
        "arrivalDate": arrival_date,
        "departureDate": departure_date,
        "contact": contact_json
    },
    test_name="3. Caso con contact (objeto JSON como string)"
))

# Test 4: Caso completo con todos los campos opcionales
full_contact_json = json.dumps({
    "firstName": "Juan",
    "lastName": "Pérez",
    "primaryEmail": "juan.perez@example.com",
    "cellPhone": "+1234567891",
    "homePhone": "+1234567892",
    "streetAddress": "123 Main St",
    "country": "US",
    "postalCode": "12345",
    "region": "CA",
    "locality": "Los Angeles"
})
occupants_json = json.dumps({"adults": 2, "children": 1, "pets": 0})
addons_json = json.dumps([{"id": 1, "quantity": 2}, {"id": 2, "quantity": 1}])
notes_json = json.dumps([
    {"note": "Cliente preferente", "isPublic": False},
    {"note": "Llegada tardía", "isPublic": True}
])
payment_json = json.dumps({
    "amount": 500.0,
    "paymentCard": {
        "cardNumber": "4111111111111111",
        "cardName": "Juan Pérez",
        "cardExp": "12-2024",
        "cardCvv": "123",
        "saveCard": True
    }
})

results.append(make_request(
    data={
        "unitId": "4",
        "arrivalDate": arrival_date,
        "departureDate": departure_date,
        "contact": full_contact_json,
        "rateTypeId": "5",
        "guaranteePolicyId": "8",
        "ignoreLos": "false",
        "occupants": occupants_json,
        "addOns": addons_json,
        "promoCode": "SUMMER2024",
        "confirmationNumber": "CONF-12345",
        "travelInsurance": "true",
        "notes": notes_json,
        "payment": payment_json,
        "isTaxable": "true",
        "campaignId": "10",
        "status": "Confirmed",
        "subChannel": "online",
        "clientIPAddress": "192.168.1.1",
        "session": "mock-session-data"
    },
    test_name="4. Caso completo con todos los campos opcionales"
))

# Test 5: Caso con breakdown (solo Server Keys)
breakdown_json = json.dumps({
    "rates": [
        {"date": arrival_date, "rate": 150.0, "nights": 1},
        {"date": (today + timedelta(days=8)).strftime('%Y-%m-%d'), "rate": 175.0, "nights": 1},
        {"date": (today + timedelta(days=9)).strftime('%Y-%m-%d'), "rate": 200.0, "nights": 1}
    ],
    "fees": [
        {"id": 1, "quantity": 1, "rate": 50.0}
    ],
    "total": 575.0
})
results.append(make_request(
    data={
        "unitId": "5",
        "arrivalDate": arrival_date,
        "departureDate": departure_date,
        "contactId": "456",
        "breakdown": breakdown_json
    },
    test_name="5. Caso con breakdown personalizado (Server Keys)"
))

# Test 6: Validación - Falta unitId
results.append(make_request(
    data={
        "arrivalDate": arrival_date,
        "departureDate": departure_date
    },
    test_name="6. Validación - Falta unitId (debe rechazar)",
    expect_error=True
))

# Test 7: Validación - Falta arrivalDate
results.append(make_request(
    data={
        "unitId": "6",
        "departureDate": departure_date
    },
    test_name="7. Validación - Falta arrivalDate (debe rechazar)",
    expect_error=True
))

# Test 8: Validación - Falta departureDate
results.append(make_request(
    data={
        "unitId": "7",
        "arrivalDate": arrival_date
    },
    test_name="8. Validación - Falta departureDate (debe rechazar)",
    expect_error=True
))

# Test 9: Validación - Fecha inválida
results.append(make_request(
    data={
        "unitId": "8",
        "arrivalDate": "2024-13-45",  # Fecha inválida
        "departureDate": departure_date
    },
    test_name="9. Validación - Fecha inválida (debe rechazar)",
    expect_error=True
))

# Test 10: Validación - departureDate antes de arrivalDate
results.append(make_request(
    data={
        "unitId": "9",
        "arrivalDate": departure_date,
        "departureDate": arrival_date  # Invertido
    },
    test_name="10. Validación - departureDate antes de arrivalDate (debe rechazar)",
    expect_error=True
))

# Test 11: Validación - Status inválido
results.append(make_request(
    data={
        "unitId": "10",
        "arrivalDate": arrival_date,
        "departureDate": departure_date,
        "status": "InvalidStatus"  # Status no válido
    },
    test_name="11. Validación - Status inválido (debe rechazar)",
    expect_error=True
))

# Test 12: Validación - Contact sin identificadores únicos
invalid_contact_json = json.dumps({
    "firstName": "Test",
    "lastName": "User"
    # Falta email, teléfono, etc.
})
results.append(make_request(
    data={
        "unitId": "11",
        "arrivalDate": arrival_date,
        "departureDate": departure_date,
        "contact": invalid_contact_json
    },
    test_name="12. Validación - Contact sin identificadores únicos (debe rechazar)",
    expect_error=True
))

# Test 13: Validación - PromoCode muy largo
results.append(make_request(
    data={
        "unitId": "12",
        "arrivalDate": arrival_date,
        "departureDate": departure_date,
        "promoCode": "A" * 17  # Máximo 16 caracteres
    },
    test_name="13. Validación - PromoCode muy largo (debe rechazar)",
    expect_error=True
))

# Test 14: Caso con payment usando bankAccount
bank_payment_json = json.dumps({
    "amount": 300.0,
    "bankAccount": {
        "routingNumber": "021000021",
        "accountNumber": "9876543210",
        "accountType": "personal-checking",
        "saveAccount": True
    }
})
results.append(make_request(
    data={
        "unitId": "13",
        "arrivalDate": arrival_date,
        "departureDate": departure_date,
        "contactId": "789",
        "payment": bank_payment_json
    },
    test_name="14. Caso con payment usando bankAccount"
))

# Test 15: Caso con múltiples reservas (simulando flujo real)
for i in range(3):
    test_date = today + timedelta(days=14 + i*7)
    test_arrival = test_date.strftime('%Y-%m-%d')
    test_departure = (test_date + timedelta(days=3)).strftime('%Y-%m-%d')
    
    results.append(make_request(
        data={
            "unitId": str(14 + i),
            "arrivalDate": test_arrival,
            "departureDate": test_departure,
            "contactId": str(100 + i),
            "status": "Hold",
            "promoCode": f"PROMO{i+1}"
        },
        test_name=f"15.{i+1}. Reserva múltiple {i+1} - Simulación de flujo real"
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
            print(f"        - Test {i} falló: {result.get('error', 'Unknown error')}")
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
        'failed_tests': failed_tests,
        'results': results
    }, f, indent=2, ensure_ascii=False)

print(f"\n[SAVE] Resultados guardados en: {output_file}")

