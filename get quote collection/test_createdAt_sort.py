#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba rápida para verificar el ordenamiento por createdAt
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

# Cargar variables de entorno
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
auth = HTTPBasicAuth(API_USERNAME, API_PASSWORD)

print("=" * 80)
print("TESTING ORDENAMIENTO POR createdAt")
print("=" * 80)
print(f"Endpoint: {ENDPOINT}")
print()

# Test 1: Ordenar por createdAt desc (última quote creada)
print("\n[TEST 1] Ordenar por createdAt desc (última quote creada)")
params1 = {
    "page": 1,
    "size": 3,
    "sortColumn": "createdAt",
    "sortDirection": "desc"
}
print(f"Parámetros: {params1}")

try:
    response1 = requests.get(ENDPOINT, auth=auth, params=params1, headers={'Accept': 'application/json'}, timeout=30)
    print(f"Status Code: {response1.status_code}")
    
    if response1.status_code == 200:
        data1 = response1.json()
        print(f"\n   Estructura completa de _embedded: {list(data1.get('_embedded', {}).keys())}")
        
        embedded_data = data1.get('_embedded', {})
        # Probar diferentes nombres posibles
        quotes = embedded_data.get('amenities', [])
        if not quotes:
            quotes = embedded_data.get('quotes', [])
        if not quotes:
            # Si no hay quotes, mostrar todas las claves disponibles
            print(f"   Claves en _embedded: {list(embedded_data.keys())}")
            if embedded_data:
                first_key = list(embedded_data.keys())[0]
                quotes = embedded_data.get(first_key, [])
        
        print(f"✅ Respuesta exitosa - {len(quotes)} quotes obtenidas")
        print(f"   Total items: {data1.get('total_items', 'N/A')}")
        print(f"   Página: {data1.get('page', 'N/A')}")
        
        if quotes:
            print("\n   Primeras 3 quotes ordenadas por createdAt desc:")
            for i, quote in enumerate(quotes, 1):
                quote_id = quote.get('id', 'N/A')
                created_at = quote.get('createdAt', 'N/A')
                arrival = quote.get('arrivalDate', 'N/A')
                print(f"   {i}. Quote ID: {quote_id}, createdAt: {created_at}, Arrival: {arrival}")
                
                # Verificar si el campo createdAt existe
                if 'createdAt' not in quote:
                    print(f"      ⚠️  ADVERTENCIA: El campo 'createdAt' NO existe en esta quote")
                    print(f"      Campos disponibles: {list(quote.keys())[:15]}...")
        else:
            print("   ⚠️  No se encontraron quotes en la respuesta")
            print(f"   Estructura de _embedded: {json.dumps(embedded_data, indent=2)[:500]}...")
    else:
        print(f"❌ Error: {response1.status_code}")
        print(f"   Respuesta: {response1.text[:500]}")
except Exception as e:
    print(f"❌ Excepción: {e}")

# Test 2: Ordenar por id desc (para comparar)
print("\n" + "=" * 80)
print("[TEST 2] Ordenar por id desc (para comparar)")
params2 = {
    "page": 1,
    "size": 3,
    "sortColumn": "id",
    "sortDirection": "desc"
}
print(f"Parámetros: {params2}")

try:
    response2 = requests.get(ENDPOINT, auth=auth, params=params2, headers={'Accept': 'application/json'}, timeout=30)
    print(f"Status Code: {response2.status_code}")
    
    if response2.status_code == 200:
        data2 = response2.json()
        embedded_data = data2.get('_embedded', {})
        quotes = embedded_data.get('amenities', [])
        if not quotes:
            quotes = embedded_data.get('quotes', [])
        if not quotes and embedded_data:
            first_key = list(embedded_data.keys())[0]
            quotes = embedded_data.get(first_key, [])
        
        print(f"✅ Respuesta exitosa - {len(quotes)} quotes obtenidas")
        print("\n   Primeras 3 quotes ordenadas por id desc:")
        for i, quote in enumerate(quotes, 1):
            quote_id = quote.get('id', 'N/A')
            created_at = quote.get('createdAt', 'N/A')
            arrival = quote.get('arrivalDate', 'N/A')
            print(f"   {i}. Quote ID: {quote_id}, createdAt: {created_at}, Arrival: {arrival}")
except Exception as e:
    print(f"❌ Excepción: {e}")

# Test 3: Sin ordenamiento (default)
print("\n" + "=" * 80)
print("[TEST 3] Sin ordenamiento (default - order asc)")
params3 = {
    "page": 1,
    "size": 3
}
print(f"Parámetros: {params3}")

try:
    response3 = requests.get(ENDPOINT, auth=auth, params=params3, headers={'Accept': 'application/json'}, timeout=30)
    print(f"Status Code: {response3.status_code}")
    
    if response3.status_code == 200:
        data3 = response3.json()
        embedded_data = data3.get('_embedded', {})
        quotes = embedded_data.get('amenities', [])
        if not quotes:
            quotes = embedded_data.get('quotes', [])
        if not quotes and embedded_data:
            first_key = list(embedded_data.keys())[0]
            quotes = embedded_data.get(first_key, [])
        
        print(f"✅ Respuesta exitosa - {len(quotes)} quotes obtenidas")
        print("\n   Primeras 3 quotes (ordenamiento por defecto):")
        for i, quote in enumerate(quotes, 1):
            quote_id = quote.get('id', 'N/A')
            created_at = quote.get('createdAt', 'N/A')
            arrival = quote.get('arrivalDate', 'N/A')
            print(f"   {i}. Quote ID: {quote_id}, createdAt: {created_at}, Arrival: {arrival}")
except Exception as e:
    print(f"❌ Excepción: {e}")

print("\n" + "=" * 80)
print("FIN DE PRUEBAS")
print("=" * 80)

