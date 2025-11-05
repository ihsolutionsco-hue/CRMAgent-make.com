#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor Mock para la API de TrackHS PMS - Create Reservation
Simula la API real sin afectar la base de datos para testing local
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import re
import json
from typing import Dict, Any, Optional, Union

app = Flask(__name__)
CORS(app)  # Permitir CORS para testing

# Contador para IDs de reservas mock
mock_reservation_counter = 1

def validate_date(date_str: Optional[str]) -> bool:
    """Valida formato de fecha ISO 8601 (YYYY-MM-DD)"""
    if not date_str:
        return False
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(pattern, date_str):
        return False
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

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
    cleaned = phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
    pattern = r'^\+?[1-9]\d{6,14}$'
    return bool(re.match(pattern, cleaned))

def validate_country_code(country: Optional[str]) -> bool:
    """Valida código de país ISO de 2 caracteres"""
    if not country:
        return True  # Opcional
    return len(country) == 2 and country.isalpha()

def parse_json_string(value: str) -> Union[Dict, List, str]:
    """Intenta parsear un string JSON, si falla devuelve el string original"""
    if not value:
        return value
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return value

def validate_request(data: Dict[str, Any]) -> tuple[bool, Optional[str], int]:
    """
    Valida el request contra la especificación OpenAPI
    Retorna: (is_valid, error_message, status_code)
    """
    # Campos requeridos
    if 'unitId' not in data or not data['unitId']:
        return False, "unitId is required", 422
    
    if 'arrivalDate' not in data or not data['arrivalDate']:
        return False, "arrivalDate is required", 422
    
    if 'departureDate' not in data or not data['departureDate']:
        return False, "departureDate is required", 422
    
    # Validar formato de fechas
    if not validate_date(data['arrivalDate']):
        return False, "arrivalDate must be in ISO 8601 format (YYYY-MM-DD)", 422
    
    if not validate_date(data['departureDate']):
        return False, "departureDate must be in ISO 8601 format (YYYY-MM-DD)", 422
    
    # Validar que departureDate sea después de arrivalDate
    try:
        arrival = datetime.strptime(data['arrivalDate'], '%Y-%m-%d')
        departure = datetime.strptime(data['departureDate'], '%Y-%m-%d')
        if departure <= arrival:
            return False, "departureDate must be after arrivalDate", 422
    except ValueError:
        return False, "Invalid date format", 422
    
    # Validar unitId es integer
    try:
        unit_id = int(data['unitId'])
        if unit_id <= 0:
            return False, "unitId must be a positive integer", 422
    except (ValueError, TypeError):
        return False, "unitId must be an integer", 422
    
    # Validar contactId o contact (al menos uno requerido para crear contacto)
    has_contact_id = 'contactId' in data and data['contactId']
    has_contact = 'contact' in data and data['contact']
    
    if not has_contact_id and not has_contact:
        # En producción, esto podría ser opcional si se crea el contacto después
        # Pero para el mock, lo requerimos
        pass  # Permitimos que se cree sin contacto para algunos tests
    
    # Si hay contact, validarlo
    if has_contact:
        contact = parse_json_string(data['contact']) if isinstance(data['contact'], str) else data['contact']
        if isinstance(contact, dict):
            # Validar que tenga al menos un identificador único
            required_contact_fields = ['cellPhone', 'homePhone', 'otherPhone', 'primaryEmail', 'secondaryEmail']
            has_contact_id = any(contact.get(field) for field in required_contact_fields)
            if not has_contact_id:
                return False, "contact must have at least one of: cellPhone, homePhone, otherPhone, primaryEmail, secondaryEmail", 422
            
            # Validar email si existe
            if 'primaryEmail' in contact and contact['primaryEmail']:
                if not validate_email(contact['primaryEmail']):
                    return False, "contact.primaryEmail must be a valid email format", 422
                if len(contact['primaryEmail']) > 100:
                    return False, "contact.primaryEmail exceeds maximum length of 100 characters", 422
            
            if 'secondaryEmail' in contact and contact['secondaryEmail']:
                if not validate_email(contact['secondaryEmail']):
                    return False, "contact.secondaryEmail must be a valid email format", 422
                if len(contact['secondaryEmail']) > 100:
                    return False, "contact.secondaryEmail exceeds maximum length of 100 characters", 422
            
            # Validar teléfonos
            phone_fields = ['cellPhone', 'homePhone', 'otherPhone']
            for field in phone_fields:
                if field in contact and contact[field]:
                    if len(contact[field]) > 16:
                        return False, f"contact.{field} exceeds maximum length of 16 characters", 422
                    if not validate_phone(contact[field]):
                        return False, f"contact.{field} must be in E.164 format", 422
    
    # Validar status enum
    if 'status' in data and data['status']:
        valid_statuses = ['Hold', 'Confirmed', 'Checked Out', 'Checked In', 'Cancelled']
        if data['status'] not in valid_statuses:
            return False, f"status must be one of: {', '.join(valid_statuses)}", 422
    
    # Validar promoCode
    if 'promoCode' in data and data['promoCode']:
        if len(data['promoCode']) < 1 or len(data['promoCode']) > 16:
            return False, "promoCode must be between 1 and 16 characters", 422
    
    # Validar occupants si es string JSON
    if 'occupants' in data and data['occupants']:
        occupants = parse_json_string(data['occupants']) if isinstance(data['occupants'], str) else data['occupants']
        if not isinstance(occupants, dict):
            return False, "occupants must be a JSON object", 422
    
    # Validar addOns si es string JSON
    if 'addOns' in data and data['addOns']:
        add_ons = parse_json_string(data['addOns']) if isinstance(data['addOns'], str) else data['addOns']
        if not isinstance(add_ons, list):
            return False, "addOns must be a JSON array", 422
        for addon in add_ons:
            if not isinstance(addon, dict):
                return False, "addOns must be an array of objects", 422
            if 'id' not in addon:
                return False, "each addOn must have an 'id' field", 422
            if 'quantity' not in addon:
                return False, "each addOn must have a 'quantity' field", 422
    
    # Validar notes si es string JSON
    if 'notes' in data and data['notes']:
        notes = parse_json_string(data['notes']) if isinstance(data['notes'], str) else data['notes']
        if not isinstance(notes, list):
            return False, "notes must be a JSON array", 422
        for note in notes:
            if not isinstance(note, dict):
                return False, "notes must be an array of objects", 422
            if 'note' not in note:
                return False, "each note must have a 'note' field", 422
    
    # Validar payment si es string JSON
    if 'payment' in data and data['payment']:
        payment = parse_json_string(data['payment']) if isinstance(data['payment'], str) else data['payment']
        if not isinstance(payment, dict):
            return False, "payment must be a JSON object", 422
        
        # Validar paymentCard si existe
        if 'paymentCard' in payment and payment['paymentCard']:
            card = payment['paymentCard']
            if 'cardExp' in card and card['cardExp']:
                # Validar formato MM-YY o MM-YYYY
                pattern = r'^(0|1)([0-9]{1})[-/]([0-9]{2,4})$'
                if not re.match(pattern, card['cardExp']):
                    return False, "payment.paymentCard.cardExp must be in MM-YY or MM-YYYY format", 422
        
        # Validar bankAccount si existe
        if 'bankAccount' in payment and payment['bankAccount']:
            account = payment['bankAccount']
            if 'accountType' in account and account['accountType']:
                valid_types = ['business-checking', 'business-savings', 'personal-checking', 'personal-savings']
                if account['accountType'] not in valid_types:
                    return False, f"payment.bankAccount.accountType must be one of: {', '.join(valid_types)}", 422
    
    # Validar breakdown si es string JSON
    if 'breakdown' in data and data['breakdown']:
        breakdown = parse_json_string(data['breakdown']) if isinstance(data['breakdown'], str) else data['breakdown']
        if not isinstance(breakdown, dict):
            return False, "breakdown must be a JSON object", 422
        
        # Validar rates si existe
        if 'rates' in breakdown and breakdown['rates']:
            if not isinstance(breakdown['rates'], list):
                return False, "breakdown.rates must be an array", 422
            for rate in breakdown['rates']:
                if not isinstance(rate, dict):
                    return False, "breakdown.rates must be an array of objects", 422
                if 'date' not in rate or 'rate' not in rate:
                    return False, "each rate in breakdown.rates must have 'date' and 'rate' fields", 422
    
    return True, None, 200

def create_mock_response(data: Dict[str, Any]) -> Dict[str, Any]:
    """Crea una respuesta mock que cumple con el esquema de respuesta"""
    global mock_reservation_counter
    
    now = datetime.utcnow()
    arrival = datetime.strptime(data['arrivalDate'], '%Y-%m-%d')
    departure = datetime.strptime(data['departureDate'], '%Y-%m-%d')
    nights = (departure - arrival).days
    
    # Parsear objetos JSON si vienen como strings
    contact_obj = None
    if 'contact' in data and data['contact']:
        contact_obj = parse_json_string(data['contact']) if isinstance(data['contact'], str) else data['contact']
    
    occupants_obj = {}
    if 'occupants' in data and data['occupants']:
        occupants_obj = parse_json_string(data['occupants']) if isinstance(data['occupants'], str) else data['occupants']
    
    # Calcular quoteBreakdown básico
    quote_breakdown = {
        "currency": "USD",
        "totalRent": 1000.0 * nights,
        "adr": 1000.0,
        "rates": [
            {
                "date": data['arrivalDate'],
                "rate": 1000.0,
                "nights": 1
            }
        ],
        "discount": 0.0,
        "extraRates": [],
        "totalFees": 100.0,
        "fees": [
            {
                "label": "Cleaning Fee",
                "value": 100.0,
                "display": "itemize"
            }
        ],
        "subTotal": 1000.0 * nights + 100.0,
        "totalTaxes": 50.0,
        "taxes": [
            {
                "name": "Sales Tax",
                "total": 50.0
            }
        ],
        "total": 1000.0 * nights + 100.0 + 50.0,
        "insurance": 0.0,
        "grandTotal": 1000.0 * nights + 100.0 + 50.0,
        "payments": 0.0,
        "balance": 1000.0 * nights + 100.0 + 50.0
    }
    
    response = {
        "id": mock_reservation_counter,
        "altConf": data.get("confirmationNumber"),
        "unitId": int(data['unitId']),
        "isUnitLocked": False,
        "isUnitAssigned": True,
        "isUnitTypeLocked": False,
        "unitTypeId": 1,
        "arrivalDate": data['arrivalDate'],
        "departureDate": data['departureDate'],
        "earlyArrival": False,
        "lateDeparture": False,
        "arrivalTime": arrival.isoformat() + 'Z',
        "departureTime": departure.isoformat() + 'Z',
        "nights": nights,
        "status": data.get("status", "Hold"),
        "cancelledAt": None,
        "occupants": occupants_obj if occupants_obj else {"adults": 2, "children": 0, "pets": 0},
        "requiredSecurityDeposit": 0.0,
        "remainingSecurityDeposit": 0.0,
        "quoteBreakdown": quote_breakdown,
        "folioBreakdown": {
            "currency": "USD",
            "totalRent": 0.0,
            "adr": 0.0,
            "rates": [],
            "totalFees": 0.0,
            "totalCharges": 0.0,
            "fees": [],
            "subTotal": 0.0,
            "totalTaxes": 0.0,
            "taxes": [],
            "total": 0.0,
            "grandTotal": 0.0,
            "payments": 0.0,
            "transfers": 0.0,
            "insurance": 0.0,
            "balance": 0.0
        },
        "contactId": int(data.get("contactId", 1)) if data.get("contactId") else 1,
        "channelId": None,
        "channel": None,
        "folioId": mock_reservation_counter + 100,
        "guaranteePolicyId": data.get("guaranteePolicyId"),
        "subChannel": data.get("subChannel"),
        "cancellationPolicyId": 1,
        "cancellationReasonId": 1,
        "userId": None,
        "user": None,
        "travelAgentId": None,
        "travelAgent": None,
        "campaignId": data.get("campaignId"),
        "campaign": None,
        "typeId": 1,
        "rateTypeId": data.get("rateTypeId", 1),
        "unitCodeId": None,
        "cancelledById": None,
        "cancelledBy": None,
        "paymentMethodId": None,
        "holdExpiration": (now + timedelta(days=7)).isoformat() + 'Z',
        "isTaxable": data.get("isTaxable", True),
        "inviteUuid": None,
        "uuid": f"mock-uuid-{mock_reservation_counter}",
        "source": "channel",
        "agreementStatus": "not-sent",
        "automatePayment": True,
        "promoCodeId": None,
        "promoCode": data.get("promoCode"),
        "updatedBy": "mock_user",
        "createdBy": "mock_user",
        "updatedAt": now.isoformat() + 'Z',
        "createdAt": now.isoformat() + 'Z',
        "_embedded": {
            "contact": contact_obj if contact_obj else {
                "id": 1,
                "firstName": "John",
                "lastName": "Doe",
                "primaryEmail": "john.doe@example.com"
            },
            "folio": {
                "id": mock_reservation_counter + 100,
                "type": "guest",
                "status": "open"
            },
            "unit": {
                "id": int(data['unitId']),
                "name": f"Unit {data['unitId']}",
                "isActive": True
            }
        },
        "_links": {
            "self": {
                "href": f"/api/pms/reservations/{mock_reservation_counter}"
            },
            "cancel": {
                "href": f"/api/pms/reservations/{mock_reservation_counter}/cancel"
            }
        }
    }
    
    mock_reservation_counter += 1
    return response

@app.route('/api/pms/reservations', methods=['POST'])
def create_reservation():
    """
    Endpoint mock para crear reserva
    Simula el comportamiento de la API real según la documentación OpenAPI
    """
    # Verificar autenticación básica
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({"error": "Unauthorized"}), 401
    
    # Obtener datos del request
    # En Make.com se envían como query strings
    data = {}
    for key in request.args:
        value = request.args.get(key)
        # Si el valor es null o string "null", lo ignoramos
        if value and value.lower() != 'null':
            data[key] = value
    
    # También intentar obtener de JSON body si existe (para flexibilidad)
    if request.is_json:
        json_data = request.get_json()
        # Combinar, pero query params tienen prioridad
        for key, value in json_data.items():
            if key not in data:
                data[key] = value
    
    # Validar request
    is_valid, error_message, status_code = validate_request(data)
    
    if not is_valid:
        return jsonify({
            "type": "http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html",
            "title": "Invalid data provided",
            "status": status_code,
            "detail": error_message,
            "validation_messages": [error_message]
        }), status_code
    
    # Crear respuesta mock
    response_data = create_mock_response(data)
    
    return jsonify(response_data), 200

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check"""
    return jsonify({"status": "ok", "service": "TrackHS PMS Mock API"}), 200

@app.route('/', methods=['GET'])
def root():
    """Endpoint raíz con información"""
    return jsonify({
        "service": "TrackHS PMS Mock API",
        "version": "1.0.0",
        "endpoints": {
            "POST /api/pms/reservations": "Create a new reservation",
            "GET /health": "Health check"
        },
        "note": "This is a mock server for local testing. No data is persisted to the real database."
    }), 200

if __name__ == '__main__':
    print("=" * 80)
    print("TRACKHS PMS MOCK SERVER - CREATE RESERVATION")
    print("=" * 80)
    print("Servidor mock iniciado en http://localhost:5001")
    print("Endpoints disponibles:")
    print("  POST http://localhost:5001/api/pms/reservations - Crear reserva")
    print("  GET  http://localhost:5001/health - Health check")
    print("  GET  http://localhost:5001/ - Información del servidor")
    print("=" * 80)
    print("\n⚠️  NOTA: Este es un servidor MOCK. No se guardan datos en la base de datos real.")
    print("=" * 80)
    app.run(host='0.0.0.0', port=5001, debug=True)



