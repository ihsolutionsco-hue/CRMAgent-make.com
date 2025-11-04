#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de pruebas para la API de TrackHS CRM - Get Contacts Collection
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

ENDPOINT = f"{API_BASE_URL}/crm/contacts"

print("=" * 80)
print("TESTING API TRACKHS CRM - GET CONTACTS COLLECTION")
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
        print(f"[REQ] Parametros: {params}")
        
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
            contacts = data.get('_embedded', {}).get('contacts', [])
            page = data.get('page', 'N/A')
            page_count = data.get('page_count', 'N/A')
            page_size = data.get('page_size', 'N/A')
            total_items = data.get('total_items', 'N/A')
            
            print(f"[OK] EXITO")
            print(f"     Total de contactos en respuesta: {len(contacts)}")
            print(f"     Pagina: {page}")
            print(f"     Total de paginas: {page_count}")
            print(f"     Tamano de pagina: {page_size}")
            print(f"     Total de items: {total_items}")
            
            # Mostrar primeros 3 contactos como muestra
            if contacts:
                print(f"\n     Primeros contactos (muestra):")
                for i, contact in enumerate(contacts[:3], 1):
                    contact_id = contact.get('id', 'N/A')
                    first_name = contact.get('firstName', '')
                    last_name = contact.get('lastName', '')
                    email = contact.get('primaryEmail', 'N/A')
                    print(f"        {i}. ID: {contact_id} | Nombre: {first_name} {last_name} | Email: {email}")
            
            # Verificar estructura de respuesta
            has_embedded = '_embedded' in data
            has_contacts = 'contacts' in data.get('_embedded', {})
            has_links = '_links' in data
            
            print(f"\n     Validacion de estructura:")
            print(f"        [OK] _embedded: {has_embedded}")
            print(f"        [OK] contacts array: {has_contacts}")
            print(f"        [OK] _links: {has_links}")
            
            return {
                'success': True,
                'data': data,
                'contacts_count': len(contacts),
                'total_items': total_items
            }
        else:
            print(f"[ERROR] Status Code: {response.status_code}")
            print(f"        Response: {response.text[:500]}")
            return {
                'success': False,
                'status_code': response.status_code,
                'error': response.text
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

# Test 4: Ordenamiento por email
results.append(make_request(
    params={'sortColumn': 'email', 'sortDirection': 'desc', 'size': 5},
    test_name="4. Ordenamiento por email (descendente)"
))

# Test 5: Búsqueda por término search (un nombre)
results.append(make_request(
    params={'search': 'John', 'size': 5},
    test_name="5. Búsqueda con parámetro 'search' (un nombre)"
))

# Test 6: Búsqueda por término search (dos nombres - comportamiento AND)
results.append(make_request(
    params={'search': 'John Smith', 'size': 5},
    test_name="6. Búsqueda con 'search' (dos nombres - AND)"
))

# Test 7: Búsqueda por email específico
results.append(make_request(
    params={'email': 'test@example.com', 'size': 5},
    test_name="7. Búsqueda por email específico"
))

# Test 8: Búsqueda por term (ID o nombre preciso)
results.append(make_request(
    params={'term': '1', 'size': 5},
    test_name="8. Búsqueda por 'term' (valor preciso)"
))

# Test 9: Filtro por updatedSince (formato date)
today = datetime.now().strftime('%Y-%m-%d')
last_month = datetime.now().replace(day=1).strftime('%Y-%m-%d')
results.append(make_request(
    params={'updatedSince': last_month, 'size': 5},
    test_name=f"9. Filtro por updatedSince (desde {last_month})"
))

# Test 10: Ordenamiento por VIP
results.append(make_request(
    params={'sortColumn': 'vip', 'sortDirection': 'desc', 'size': 5},
    test_name="10. Ordenamiento por VIP (descendente)"
))

# Test 11: Combinación de parámetros
results.append(make_request(
    params={
        'search': 'John',
        'sortColumn': 'name',
        'sortDirection': 'asc',
        'page': 1,
        'size': 3
    },
    test_name="11. Combinación de parámetros (search + sort + pagination)"
))

# Test 12: Búsqueda por teléfono (numérico)
results.append(make_request(
    params={'search': '1234567890', 'size': 5},
    test_name="12. Búsqueda por número de teléfono"
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
    print("\n[STATS] Estadisticas de contactos encontrados:")
    contact_counts = [r.get('contacts_count', 0) for r in results if r.get('success', False)]
    if contact_counts:
        print(f"     - Promedio de contactos por respuesta: {sum(contact_counts) / len(contact_counts):.1f}")
        print(f"     - Minimo: {min(contact_counts)}")
        print(f"     - Maximo: {max(contact_counts)}")

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
        'results': results
    }, f, indent=2, ensure_ascii=False)

print(f"\n[SAVE] Resultados guardados en: {output_file}")

