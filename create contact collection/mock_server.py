#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor Mock para la API de TrackHS CRM - Create Contact
Simula la API real sin afectar la base de datos para testing local
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import re
import json
from typing import Dict, Any, Optional

app = Flask(__name__)
CORS(app)  # Permitir CORS para testing

# Contador para IDs de contactos mock
mock_contact_counter = 1

def validate_email(email: Optional[str]) -> bool:
    """Valida formato de email"""
    if not email:
        return True  # Opcional
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: Optional[str]) -> bool:
    """Valida formato de teléfono E.164 (básico)"""
    if not phone:
        return True  # Opcional
    # E.164: puede empezar con + y tener entre 7-15 dígitos (mínimo razonable para un número válido)
    cleaned = phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
    pattern = r'^\+?[1-9]\d{6,14}$'  # Mínimo 7 dígitos (país + número local)
    return bool(re.match(pattern, cleaned))

def validate_date_format(date_str: Optional[str]) -> bool:
    """Valida formato MM-DD para fechas"""
    if not date_str:
        return True  # Opcional
    pattern = r'^(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|30|31)$'
    return bool(re.match(pattern, date_str))

def validate_country_code(country: Optional[str]) -> bool:
    """Valida código de país ISO de 2 caracteres"""
    if not country:
        return True  # Opcional
    return len(country) == 2 and country.isalpha()

def validate_ach_routing_number(routing: Optional[str]) -> bool:
    """Valida número de routing ACH (9 dígitos)"""
    if not routing:
        return True  # Opcional
    pattern = r'^[0-9]{9}$'
    return bool(re.match(pattern, routing))

def validate_request(data: Dict[str, Any]) -> tuple[bool, Optional[str], int]:
    """
    Valida el request contra la especificación OpenAPI
    Retorna: (is_valid, error_message, status_code)
    """
    # Validar que al menos uno de los campos requeridos esté presente
    required_fields = ['cellPhone', 'homePhone', 'otherPhone', 'primaryEmail', 'secondaryEmail']
    has_required = any(data.get(field) for field in required_fields)
    
    if not has_required:
        return False, "At least one of the following is required: cellPhone, homePhone, otherPhone, primaryEmail or secondaryEmail", 400
    
    # Validar campos de string con maxLength
    if 'firstName' in data and data['firstName'] and len(data['firstName']) > 32:
        return False, "firstName exceeds maximum length of 32 characters", 400
    
    if 'lastName' in data and data['lastName'] and len(data['lastName']) > 32:
        return False, "lastName exceeds maximum length of 32 characters", 400
    
    if 'primaryEmail' in data and data['primaryEmail']:
        if len(data['primaryEmail']) > 100:
            return False, "primaryEmail exceeds maximum length of 100 characters", 400
        if not validate_email(data['primaryEmail']):
            return False, "primaryEmail must be a valid email format", 400
    
    if 'secondaryEmail' in data and data['secondaryEmail']:
        if len(data['secondaryEmail']) > 100:
            return False, "secondaryEmail exceeds maximum length of 100 characters", 400
        if not validate_email(data['secondaryEmail']):
            return False, "secondaryEmail must be a valid email format", 400
    
    if 'proxyEmail' in data and data['proxyEmail']:
        if len(data['proxyEmail']) > 100:
            return False, "proxyEmail exceeds maximum length of 100 characters", 400
        if not validate_email(data['proxyEmail']):
            return False, "proxyEmail must be a valid email format", 400
    
    # Validar teléfonos
    phone_fields = ['homePhone', 'cellPhone', 'workPhone', 'otherPhone', 'fax']
    for field in phone_fields:
        if field in data and data[field]:
            if len(data[field]) > 16:
                return False, f"{field} exceeds maximum length of 16 characters", 400
            if not validate_phone(data[field]):
                return False, f"{field} must be in E.164 format", 400
    
    # Validar dirección
    if 'streetAddress' in data and data['streetAddress'] and len(data['streetAddress']) > 255:
        return False, "streetAddress exceeds maximum length of 255 characters", 400
    
    if 'country' in data and data['country']:
        if not validate_country_code(data['country']):
            return False, "country must be a 2-character ISO country code", 400
    
    if 'postalCode' in data and data['postalCode'] and len(data['postalCode']) > 16:
        return False, "postalCode exceeds maximum length of 16 characters", 400
    
    if 'extendedAddress' in data and data['extendedAddress'] and len(data['extendedAddress']) > 255:
        return False, "extendedAddress exceeds maximum length of 255 characters", 400
    
    if 'notes' in data and data['notes'] and len(data['notes']) > 4000:
        return False, "notes exceeds maximum length of 4000 characters", 400
    
    # Validar fechas
    if 'anniversary' in data and data['anniversary']:
        if not validate_date_format(data['anniversary']):
            return False, "anniversary must be in MM-DD format", 400
    
    if 'birthdate' in data and data['birthdate']:
        if not validate_date_format(data['birthdate']):
            return False, "birthdate must be in MM-DD format", 400
    
    # Validar taxId
    if 'taxId' in data and data['taxId'] and len(data['taxId']) > 16:
        return False, "taxId exceeds maximum length of 16 characters", 400
    
    # Validar ACH routing number
    if 'achRoutingNumber' in data and data['achRoutingNumber']:
        if not validate_ach_routing_number(data['achRoutingNumber']):
            return False, "achRoutingNumber must be exactly 9 digits", 400
    
    # Validar tags (array de objetos con id)
    if 'tags' in data and data['tags']:
        if not isinstance(data['tags'], list):
            return False, "tags must be an array", 400
        for tag in data['tags']:
            if not isinstance(tag, dict):
                return False, "tags must be an array of objects", 400
            if 'id' not in tag:
                return False, "each tag must have an 'id' field", 400
            if not isinstance(tag['id'], (int, float)):
                return False, "tag id must be a number", 400
    
    # Validar references (array de objetos)
    if 'references' in data and data['references']:
        if not isinstance(data['references'], list):
            return False, "references must be an array", 400
        for ref in data['references']:
            if not isinstance(ref, dict):
                return False, "references must be an array of objects", 400
    
    # Validar customValues (objeto)
    if 'customValues' in data and data['customValues']:
        if not isinstance(data['customValues'], dict):
            return False, "customValues must be an object", 400
    
    return True, None, 200

def create_mock_response(data: Dict[str, Any]) -> Dict[str, Any]:
    """Crea una respuesta mock que cumple con el esquema de respuesta"""
    global mock_contact_counter
    
    now = datetime.utcnow().isoformat() + 'Z'
    
    response = {
        "id": mock_contact_counter,
        "firstName": data.get("firstName", ""),
        "lastName": data.get("lastName", ""),
        "primaryEmail": data.get("primaryEmail"),
        "secondaryEmail": data.get("secondaryEmail"),
        "homePhone": data.get("homePhone"),
        "cellPhone": data.get("cellPhone"),
        "workPhone": data.get("workPhone"),
        "otherPhone": data.get("otherPhone"),
        "fax": data.get("fax"),
        "streetAddress": data.get("streetAddress"),
        "country": data.get("country"),
        "postalCode": data.get("postalCode"),
        "region": data.get("region"),
        "locality": data.get("locality"),
        "extendedAddress": data.get("extendedAddress"),
        "notes": data.get("notes"),
        "anniversary": data.get("anniversary"),
        "birthdate": data.get("birthdate"),
        "isVip": data.get("isVip", False),
        "isBlacklist": data.get("isBlacklist", False),
        "taxId": data.get("taxId"),
        "references": data.get("references", []),
        "tags": data.get("tags", []),
        "customValues": data.get("customValues", {}),
        "_links": {
            "self": {
                "href": f"/api/crm/contacts/{mock_contact_counter}"
            }
        },
        "updatedAt": now,
        "updatedBy": "mock_user",
        "createdAt": now,
        "createdBy": "mock_user",
        "noIdentity": False
    }
    
    mock_contact_counter += 1
    return response

@app.route('/api/crm/contacts', methods=['POST'])
def create_contact():
    """
    Endpoint mock para crear contacto
    Simula el comportamiento de la API real según la documentación OpenAPI
    """
    # Verificar autenticación básica
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({"error": "Unauthorized"}), 401
    
    # Obtener datos del request
    # Puede venir como JSON body o como query parameters
    if request.is_json:
        data = request.get_json()
    else:
        # Si viene como query parameters (como en Make.com)
        data = {}
        for key in request.args:
            value = request.args.get(key)
            # Intentar parsear JSON si es necesario
            if value and value.startswith('[') or value.startswith('{'):
                try:
                    value = json.loads(value)
                except:
                    pass
            data[key] = value
    
    # Validar request
    is_valid, error_message, status_code = validate_request(data)
    
    if not is_valid:
        return jsonify({
            "error": error_message,
            "status": status_code
        }), status_code
    
    # Crear respuesta mock
    response_data = create_mock_response(data)
    
    return jsonify(response_data), 201

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check"""
    return jsonify({"status": "ok", "service": "TrackHS CRM Mock API"}), 200

@app.route('/', methods=['GET'])
def root():
    """Endpoint raíz con información"""
    return jsonify({
        "service": "TrackHS CRM Mock API",
        "version": "1.0.0",
        "endpoints": {
            "POST /api/crm/contacts": "Create a new contact",
            "GET /health": "Health check"
        },
        "note": "This is a mock server for local testing. No data is persisted to the real database."
    }), 200

if __name__ == '__main__':
    print("=" * 80)
    print("TRACKHS CRM MOCK SERVER")
    print("=" * 80)
    print("Servidor mock iniciado en http://localhost:5000")
    print("Endpoints disponibles:")
    print("  POST http://localhost:5000/api/crm/contacts - Crear contacto")
    print("  GET  http://localhost:5000/health - Health check")
    print("  GET  http://localhost:5000/ - Información del servidor")
    print("=" * 80)
    print("\n⚠️  NOTA: Este es un servidor MOCK. No se guardan datos en la base de datos real.")
    print("=" * 80)
    app.run(host='0.0.0.0', port=5000, debug=True)

