#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para obtener los tipos de limpieza (clean types) desde la API de TrackHS PMS
Hace una petición GET real al endpoint /api/pms/housekeeping/clean-types
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
project_root = pathlib.Path(__file__).parent
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

# Configuración
API_BASE_URL = os.getenv('TRACKHS_API_URL', 'https://ihmvacations.trackhs.com')
API_USERNAME = os.getenv('TRACKHS_USERNAME')
API_PASSWORD = os.getenv('TRACKHS_PASSWORD')

if not API_USERNAME or not API_PASSWORD:
    print("❌ ERROR: TRACKHS_USERNAME y TRACKHS_PASSWORD deben estar configurados en el archivo .env")
    sys.exit(1)

# Construir URL completa
if not API_BASE_URL.endswith('/api'):
    API_BASE_URL = f"{API_BASE_URL.rstrip('/')}/api"

ENDPOINT = f"{API_BASE_URL}/pms/housekeeping/clean-types"

print("=" * 80)
print("GET CLEAN TYPES - TRACKHS PMS API")
print("=" * 80)
print(f"Endpoint: {ENDPOINT}")
print(f"Usuario: {API_USERNAME[:20]}...")
print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)
print()

# Configurar autenticación
auth = HTTPBasicAuth(API_USERNAME, API_PASSWORD)

# Headers
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

try:
    print("🔄 Realizando petición GET...")
    print()
    
    # Realizar petición GET
    response = requests.get(
        ENDPOINT,
        auth=auth,
        headers=headers,
        timeout=120
    )
    
    # Mostrar información de la respuesta
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print()
    
    if response.status_code == 200:
        print("✅ Petición exitosa!")
        print()
        
        # Intentar parsear JSON
        try:
            data = response.json()
            print("📦 Respuesta JSON:")
            print("=" * 80)
            print(json.dumps(data, indent=2, ensure_ascii=False))
            print("=" * 80)
            print()
            
            # Mostrar información resumida si es un array
            if isinstance(data, list):
                print(f"📊 Total de tipos de limpieza: {len(data)}")
                if len(data) > 0:
                    print("\n📋 Resumen de tipos de limpieza:")
                    for i, item in enumerate(data, 1):
                        if isinstance(item, dict):
                            item_id = item.get('id', 'N/A')
                            item_name = item.get('name', item.get('title', 'N/A'))
                            print(f"  {i}. ID: {item_id}, Nombre: {item_name}")
            
        except json.JSONDecodeError:
            print("⚠️  La respuesta no es JSON válido")
            print("📄 Respuesta en texto:")
            print(response.text)
            
    else:
        print(f"❌ Error en la petición (Status: {response.status_code})")
        print()
        print("📄 Respuesta:")
        try:
            error_data = response.json()
            print(json.dumps(error_data, indent=2, ensure_ascii=False))
        except:
            print(response.text)
            
except requests.exceptions.Timeout:
    print("❌ ERROR: Timeout - La petición tardó demasiado")
    sys.exit(1)
except requests.exceptions.ConnectionError:
    print("❌ ERROR: Error de conexión - No se pudo conectar al servidor")
    sys.exit(1)
except requests.exceptions.RequestException as e:
    print(f"❌ ERROR: Error en la petición: {str(e)}")
    sys.exit(1)
except Exception as e:
    print(f"❌ ERROR inesperado: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("=" * 80)
print("✅ Proceso completado")
print("=" * 80)

