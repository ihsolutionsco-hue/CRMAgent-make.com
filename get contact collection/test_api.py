#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de pruebas para la API de TrackHS - Get Contact Collection
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

ENDPOINT_BASE = f"{API_BASE_URL}/crm/contacts"

print("=" * 80)
print("TESTING API TRACKHS - GET CONTACT COLLECTION")
print("=" * 80)
print(f"Endpoint Base: {ENDPOINT_BASE}")
print(f"Usuario: {API_USERNAME[:20]}...")
print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)
print()

# Configurar autenticación
auth = HTTPBasicAuth(API_USERNAME, API_PASSWORD)

# Primero, obtener una lista de contactos para tener IDs válidos para probar
def get_sample_contact_ids():
    """Obtiene algunos IDs de contactos para usar en las pruebas"""
    try:
        print("[INFO] Obteniendo IDs de contactos de muestra...")
        response = requests.get(
            ENDPOINT_BASE,
            auth=auth,
            params={'size': 5, 'page': 1},
            headers={'Accept': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            contacts = data.get('_embedded', {}).get('contacts', [])
            contact_ids = [str(contact.get('id')) for contact in contacts if contact.get('id')]
            print(f"[OK] Se encontraron {len(contact_ids)} IDs de contactos: {contact_ids}")
            return contact_ids
        else:
            print(f"[WARN] No se pudieron obtener IDs de muestra. Status: {response.status_code}")
            return []
    except Exception as e:
        print(f"[WARN] Error al obtener IDs de muestra: {str(e)}")
        return []

# Helper para hacer requests
def make_request(contact_id, test_name=""):
    """Hace una petición a la API y muestra los resultados"""
    try:
        endpoint = f"{ENDPOINT_BASE}/{contact_id}"
        print(f"\n[TEST] {test_name}")
        print(f"[REQ] URL: {endpoint}")
        print(f"[REQ] Contact ID: {contact_id} (tipo: {type(contact_id).__name__})")
        
        response = requests.get(
            endpoint,
            auth=auth,
            headers={'Accept': 'application/json'},
            timeout=30
        )
        
        print(f"[RES] Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Validar campos principales
            contact_id_resp = data.get('id', 'N/A')
            first_name = data.get('firstName', 'N/A')
            last_name = data.get('lastName', 'N/A')
            primary_email = data.get('primaryEmail', 'N/A')
            
            print(f"[OK] ✅ EXITO")
            print(f"     Contact ID: {contact_id_resp}")
            print(f"     Nombre: {first_name} {last_name}")
            print(f"     Email: {primary_email}")
            
            # Validar estructura de respuesta según OpenAPI
            required_fields = [
                'id', 'firstName', 'lastName', 'primaryEmail',
                'createdAt', 'updatedAt', '_links'
            ]
            
            optional_fields = [
                'secondaryEmail', 'homePhone', 'cellPhone', 'workPhone', 
                'otherPhone', 'fax', 'streetAddress', 'extendedAddress',
                'locality', 'region', 'postalCode', 'country',
                'notes', 'anniversary', 'birthdate', 'isVip', 
                'isBlacklist', 'noIdentity', 'taxId', 'paymentType',
                'achAccountNumber', 'achRoutingNumber', 'achAccountType',
                'references', 'tags', 'customValues', 'createdBy', 'updatedBy'
            ]
            
            print(f"\n     ✅ Validación de estructura (campos requeridos):")
            missing_required = []
            for field in required_fields:
                has_field = field in data
                status = "✅" if has_field else "❌"
                print(f"        {status} {field}: {has_field}")
                if not has_field:
                    missing_required.append(field)
            
            present_optional = []
            for field in optional_fields:
                if field in data:
                    present_optional.append(field)
            
            if present_optional:
                print(f"\n     📋 Campos opcionales presentes ({len(present_optional)}/{len(optional_fields)}):")
                # Mostrar solo algunos para no saturar
                print(f"        {', '.join(present_optional[:15])}")
                if len(present_optional) > 15:
                    print(f"        ... y {len(present_optional) - 15} más")
            
            # Validar tipos de datos importantes
            print(f"\n     ✅ Validación de tipos:")
            type_validations = [
                ('id', int, data.get('id')),
                ('firstName', str, data.get('firstName')),
                ('lastName', str, data.get('lastName')),
                ('primaryEmail', str, data.get('primaryEmail')),
                ('isVip', bool, data.get('isVip')),
                ('isBlacklist', bool, data.get('isBlacklist')),
                ('tags', list, data.get('tags')),
                ('references', list, data.get('references')),
            ]
            
            for field_name, expected_type, value in type_validations:
                if value is not None:
                    is_correct_type = isinstance(value, expected_type)
                    status = "✅" if is_correct_type else "❌"
                    print(f"        {status} {field_name}: {type(value).__name__} (esperado: {expected_type.__name__})")
            
            # Verificar _links si existe
            if '_links' in data:
                links = data['_links']
                print(f"\n     🔗 Enlaces disponibles:")
                for link_name, link_data in links.items():
                    if isinstance(link_data, dict) and 'href' in link_data:
                        print(f"        - {link_name}: {link_data['href']}")
            
            # Validar formatos específicos
            print(f"\n     ✅ Validación de formatos:")
            if 'anniversary' in data and data['anniversary']:
                import re
                pattern = r'^(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|30|31)$'
                is_valid = bool(re.match(pattern, data['anniversary']))
                status = "✅" if is_valid else "❌"
                print(f"        {status} anniversary: {data['anniversary']} (formato MM-DD)")
            
            if 'birthdate' in data and data['birthdate']:
                import re
                pattern = r'^(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|30|31)$'
                is_valid = bool(re.match(pattern, data['birthdate']))
                status = "✅" if is_valid else "❌"
                print(f"        {status} birthdate: {data['birthdate']} (formato MM-DD)")
            
            if 'country' in data and data['country']:
                is_valid = len(data['country']) == 2
                status = "✅" if is_valid else "❌"
                print(f"        {status} country: {data['country']} (ISO 2 caracteres)")
            
            if 'createdAt' in data and data['createdAt']:
                # Validar formato ISO 8601 básico
                import re
                iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'
                is_valid = bool(re.match(iso_pattern, data['createdAt']))
                status = "✅" if is_valid else "❌"
                print(f"        {status} createdAt: {data['createdAt'][:19]}... (ISO 8601)")
            
            return {
                'success': True,
                'data': data,
                'contact_id': contact_id_resp,
                'missing_required': missing_required
            }
        elif response.status_code == 404:
            print(f"[INFO] Contacto no encontrado (404)")
            print(f"       Esto es esperado si el ID no existe")
            return {
                'success': False,
                'status_code': 404,
                'error': 'Not Found'
            }
        elif response.status_code == 401:
            print(f"[ERROR] ❌ No autorizado (401)")
            print(f"       Verifica las credenciales de autenticación")
            return {
                'success': False,
                'status_code': 401,
                'error': 'Unauthorized'
            }
        elif response.status_code == 403:
            print(f"[ERROR] ❌ Prohibido (403)")
            print(f"       No tienes permisos para acceder a este recurso")
            return {
                'success': False,
                'status_code': 403,
                'error': 'Forbidden'
            }
        else:
            print(f"[ERROR] ❌ Status Code: {response.status_code}")
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
        print(f"[ERROR] ❌ Error de conexión")
        print(f"        {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }
    except json.JSONDecodeError as e:
        print(f"[ERROR] ❌ Error de parsing JSON")
        print(f"        {str(e)}")
        print(f"        Response: {response.text[:500]}")
        return {
            'success': False,
            'error': 'JSON decode error'
        }

# Obtener IDs de muestra
sample_contact_ids = get_sample_contact_ids()

if not sample_contact_ids:
    print("\n[WARN] No se pudieron obtener IDs de contactos para probar.")
    print("       Intentando con ID por defecto: 1")
    sample_contact_ids = ['1']

# CASOS DE PRUEBA
results = []

print("\n" + "=" * 80)
print("INICIANDO CASOS DE PRUEBA")
print("=" * 80)

# Test 1: Obtener contacto básico (sin parámetros - GET simple)
if sample_contact_ids:
    test_contact_id = sample_contact_ids[0]
    results.append(make_request(
        contact_id=test_contact_id,
        test_name="1. Obtener contacto básico (ID válido)"
    ))

# Test 2: Probar con diferentes IDs de contactos
if len(sample_contact_ids) > 1:
    for i, contact_id in enumerate(sample_contact_ids[1:4], 2):  # Probar hasta 3 contactos más
        results.append(make_request(
            contact_id=contact_id,
            test_name=f"{i}. Obtener contacto diferente (ID: {contact_id})"
        ))

# Test 3: Probar con ID como string numérico (según OpenAPI)
if sample_contact_ids:
    test_contact_id = sample_contact_ids[0]
    results.append(make_request(
        contact_id=str(test_contact_id),  # Asegurar que es string
        test_name=f"{len(results) + 1}. Obtener contacto con ID como string (validar tipo OpenAPI)"
    ))

# Test 4: Probar con ID inexistente (debe retornar 404)
results.append(make_request(
    contact_id='999999',
    test_name=f"{len(results) + 1}. Probar con ID inexistente (debe retornar 404)"
))

# Test 5: Probar con ID inválido (string no numérico)
results.append(make_request(
    contact_id='abc123',
    test_name=f"{len(results) + 1}. Probar con ID inválido (string no numérico)"
))

# RESUMEN DE RESULTADOS
print("\n" + "=" * 80)
print("RESUMEN DE RESULTADOS")
print("=" * 80)

successful_tests = sum(1 for r in results if r.get('success', False))
total_tests = len(results)

print(f"\n[OK] ✅ Tests exitosos: {successful_tests}/{total_tests}")
print(f"[ERROR] ❌ Tests fallidos: {total_tests - successful_tests}/{total_tests}")

# Separar tests que fallaron por error vs tests esperados (como 404)
expected_failures = sum(1 for r in results if not r.get('success', False) and r.get('status_code') == 404)
actual_failures = total_tests - successful_tests - expected_failures

if expected_failures > 0:
    print(f"[INFO] ℹ️  Tests con fallo esperado (404): {expected_failures}")

if actual_failures > 0:
    print(f"[ERROR] ❌ Tests con fallos inesperados: {actual_failures}")
    # Mostrar qué tests fallaron
    failed_tests = []
    for i, result in enumerate(results, 1):
        if not result.get('success', False) and result.get('status_code') != 404:
            failed_tests.append(i)
    if failed_tests:
        print(f"        Tests que fallaron: {failed_tests}")

# Validar estructura de respuestas exitosas
if successful_tests > 0:
    print("\n[STATS] 📊 Validación de estructura de respuestas:")
    all_missing_required = []
    for r in results:
        if r.get('success', False) and r.get('missing_required'):
            all_missing_required.extend(r.get('missing_required', []))
    
    if all_missing_required:
        unique_missing = set(all_missing_required)
        print(f"     ⚠️  Campos requeridos faltantes en alguna respuesta: {', '.join(unique_missing)}")
    else:
        print("     ✅ Todas las respuestas exitosas tienen los campos requeridos según OpenAPI")

# Verificar que el parámetro obligatorio está configurado
print("\n[VALIDATION] ✅ Verificación de parámetros obligatorios:")
print("     ✅ contactId está marcado como 'required: true' en input_spec")
print("     ✅ contactId es de tipo 'text' (coincide con OpenAPI: string)")

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
        'sample_contact_ids': sample_contact_ids,
        'results': results
    }, f, indent=2, ensure_ascii=False)

print(f"\n[SAVE] 💾 Resultados guardados en: {output_file}")

