# Create Quote V2 - Documentación Completa

## Descripción
Herramienta de Make.com para crear cotizaciones (quotes) en el sistema TrackHS PMS. Genera cotizaciones de reserva con precios, tarifas, impuestos y políticas de garantía/cancelación.

## Endpoint API
```
POST https://ihmvacations.trackhs.com/api/v2/pms/quotes
```

## Autenticación
- **Usuario**: `{{var.auth.user}}`
- **Contraseña**: `{{var.auth.pass}}`
- **Tipo**: HTTP Basic Authentication

## Formato de Datos

**Implementación actual**: El endpoint envía los datos como **body JSON** (`application/json`), según la especificación OpenAPI.

- **Body Type**: `raw`
- **Content-Type**: `application/json`
- Los campos opcionales solo se incluyen si tienen valores (usando `isEmpty()`)
- Los arrays JSON (`occupants`, `guestFees`, `ownerFees`) se parsean desde strings JSON

---

# Especificación OpenAPI Completa

# OpenAPI definition
```json
{
  "_id": "/branches/1.0/apis/pms-quotes-v2-api.json",
  "openapi": "3.0.0",
  "info": {
    "title": "PMS Quotes V2 API",
    "version": "2.0",
    "description": "The full PMS API is large, as such we have broken down the files into related components. Since some of the components may share model files, models are referenced instead of embedded.\nThis API covers all endpoints related to unit, unit type and node configuration.\n\nWhen used externally, this API requires a server context key.\n\nWhen used in user context, endpoints may be restricted based on role.\n",
    "contact": {
      "name": "Track Support",
      "email": "support@trackhs.com",
      "url": "https://support.trackhs.com"
    }
  },
  "tags": [
    {
      "name": "Quote V2",
      "description": "Quote v2 system"
    }
  ],
  "paths": {
    "/v2/pms/quotes": {
      "post": {
        "summary": "Create Quote V2",
        "operationId": "createReservationQuoteV2",
        "responses": {
          "200": {
            "description": "OK",
            "content": {
              "application/json": {
                "schema": {
                  "title": "Calendar Response",
                  "type": "object",
                  "description": "Expected response when receiving an OK response from the API.",
                  "properties": {
                    "isValid": {
                      "type": "boolean"
                    },
                    "error": {
                      "type": "object",
                      "properties": {
                        "code": {
                          "type": "string"
                        },
                        "message": {
                          "type": "string"
                        }
                      }
                    },
                    "warnings": {
                      "type": "array",
                      "items": {
                        "type": "string"
                      }
                    },
                    "isAvailable": {
                      "type": "boolean"
                    },
                    "reservationId": {
                      "type": "integer"
                    },
                    "currency": {
                      "type": "string",
                      "description": "3 letter ISO Currency Code"
                    },
                    "arrivalDate": {
                      "type": "string"
                    },
                    "departureDate": {
                      "type": "string"
                    },
                    "unitId": {
                      "type": "integer"
                    },
                    "unitTypeId": {
                      "type": "integer"
                    },
                    "typeId": {
                      "type": "integer"
                    },
                    "guaranteePolicyId": {
                      "type": "integer"
                    },
                    "cancellationPolicyId": {
                      "type": "integer"
                    },
                    "securityDeposit": {
                      "type": "number"
                    },
                    "promoCodeId": {
                      "type": "integer"
                    },
                    "grossRent": {
                      "type": "string"
                    },
                    "discount": {
                      "type": "number"
                    },
                    "rateTypeId": {
                      "type": "integer"
                    },
                    "promoValue": {
                      "type": "string"
                    },
                    "discountTotal": {
                      "type": "string"
                    },
                    "netRent": {
                      "type": "string"
                    },
                    "guestNetDisplayRent": {
                      "type": "string"
                    },
                    "guestGrossDisplayRent": {
                      "type": "string"
                    },
                    "totalGuestFees": {
                      "type": "string"
                    },
                    "totalRentFees": {
                      "type": "string"
                    },
                    "totalItemizedFees": {
                      "type": "string"
                    },
                    "totalTaxFees": {
                      "type": "string"
                    },
                    "totalServiceFees": {
                      "type": "string"
                    },
                    "totalRentTaxes": {
                      "type": "string"
                    },
                    "totalGuestRentTaxes": {
                      "type": "string"
                    },
                    "totalFeeTaxes": {
                      "type": "string"
                    },
                    "totalGuestFeeTaxes": {
                      "type": "string"
                    },
                    "totalTaxes": {
                      "type": "string"
                    },
                    "total": {
                      "type": "string"
                    },
                    "actualAdr": {
                      "type": "string"
                    },
                    "guestAdr": {
                      "type": "string"
                    },
                    "guaranteePolicy": {
                      "type": "object",
                      "properties": {
                        "id": {
                          "type": "integer"
                        },
                        "name": {
                          "type": "string"
                        },
                        "type": {
                          "type": "string"
                        }
                      }
                    },
                    "cancellationPolicy": {
                      "type": "object",
                      "properties": {
                        "id": {
                          "type": "integer"
                        },
                        "name": {
                          "type": "string"
                        },
                        "time": {
                          "type": "string",
                          "description": "Time in hh:mm format"
                        },
                        "timezone": {
                          "type": "string",
                          "description": "example - \"America/Chicago\""
                        },
                        "breakpoints": {
                          "type": "array",
                          "items": {
                            "type": "object",
                            "properties": {
                              "start": {
                                "type": "integer"
                              },
                              "end": {
                                "type": "integer"
                              },
                              "nonRefundable": {
                                "type": "boolean"
                              },
                              "nonCancelable": {
                                "type": "boolean"
                              },
                              "penaltyNights": {
                                "type": "integer"
                              },
                              "penaltyPercent": {
                                "type": "string"
                              },
                              "penaltyFlat": {
                                "type": "string"
                              },
                              "description": {
                                "type": "string"
                              }
                            }
                          }
                        }
                      }
                    },
                    "rateType": {
                      "type": "object",
                      "properties": {
                        "id": {
                          "type": "integer"
                        },
                        "code": {
                          "type": "string"
                        },
                        "name": {
                          "type": "string"
                        }
                      }
                    },
                    "rates": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "date": {
                            "type": "string"
                          },
                          "nights": {
                            "type": "integer"
                          },
                          "rate": {
                            "type": "string"
                          }
                        }
                      }
                    },
                    "occupants": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "id": {
                            "type": "integer"
                          },
                          "handle": {
                            "type": "string"
                          },
                          "name": {
                            "type": "string"
                          },
                          "quantity": {
                            "type": "integer"
                          }
                        }
                      }
                    },
                    "additionalRates": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "id": {
                            "type": "integer"
                          },
                          "code": {
                            "type": "string"
                          },
                          "name": {
                            "type": "string"
                          },
                          "amount": {
                            "type": "string"
                          },
                          "isValid": {
                            "type": "boolean"
                          },
                          "error": {
                            "type": "string"
                          }
                        }
                      }
                    },
                    "guestFees": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "id": {
                            "type": "integer"
                          },
                          "name": {
                            "type": "string"
                          },
                          "type": {
                            "type": "string"
                          },
                          "displayName": {
                            "type": "string"
                          },
                          "quantity": {
                            "type": "integer"
                          },
                          "unitValue": {
                            "type": "string"
                          },
                          "value": {
                            "type": "string"
                          },
                          "estimatedTax": {
                            "type": "string"
                          },
                          "isTaxable": {
                            "type": "boolean"
                          },
                          "displayAs": {
                            "type": "string"
                          },
                          "allowFeeRemoval": {
                            "type": "boolean"
                          },
                          "allowFeeEdit": {
                            "type": "boolean"
                          },
                          "isRequired": {
                            "type": "boolean"
                          },
                          "isSuggested": {
                            "type": "boolean"
                          },
                          "maxEdit": {
                            "type": "integer"
                          }
                        }
                      }
                    },
                    "additionalGuestFees": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "id": {
                            "type": "integer"
                          },
                          "name": {
                            "type": "string"
                          },
                          "type": {
                            "type": "string"
                          },
                          "displayName": {
                            "type": "string"
                          },
                          "quantity": {
                            "type": "integer"
                          },
                          "unitValue": {
                            "type": "string"
                          },
                          "value": {
                            "type": "string"
                          },
                          "estimatedTax": {
                            "type": "string"
                          },
                          "isTaxable": {
                            "type": "boolean"
                          },
                          "displayAs": {
                            "type": "string"
                          },
                          "allowFeeRemoval": {
                            "type": "boolean"
                          },
                          "allowFeeEdit": {
                            "type": "boolean"
                          },
                          "isRequired": {
                            "type": "boolean"
                          },
                          "isSuggested": {
                            "type": "boolean"
                          },
                          "maxEdit": {
                            "type": "integer"
                          }
                        }
                      }
                    },
                    "ownerFees": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "id": {
                            "type": "integer"
                          },
                          "name": {
                            "type": "string"
                          },
                          "type": {
                            "type": "string"
                          },
                          "displayName": {
                            "type": "string"
                          },
                          "quantity": {
                            "type": "integer"
                          },
                          "unitValue": {
                            "type": "string"
                          },
                          "value": {
                            "type": "string"
                          },
                          "estimatedTax": {
                            "type": "string"
                          },
                          "isTaxable": {
                            "type": "boolean"
                          },
                          "displayAs": {
                            "type": "string"
                          },
                          "allowFeeRemoval": {
                            "type": "boolean"
                          },
                          "allowFeeEdit": {
                            "type": "boolean"
                          },
                          "isRequired": {
                            "type": "boolean"
                          },
                          "isSuggested": {
                            "type": "boolean"
                          },
                          "maxEdit": {
                            "type": "integer"
                          }
                        }
                      }
                    },
                    "ownerAdditionalFees": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "id": {
                            "type": "integer"
                          },
                          "name": {
                            "type": "string"
                          },
                          "type": {
                            "type": "string"
                          },
                          "displayName": {
                            "type": "string"
                          },
                          "quantity": {
                            "type": "integer"
                          },
                          "unitValue": {
                            "type": "string"
                          },
                          "value": {
                            "type": "string"
                          },
                          "estimatedTax": {
                            "type": "string"
                          },
                          "isTaxable": {
                            "type": "boolean"
                          },
                          "displayAs": {
                            "type": "string"
                          },
                          "allowFeeRemoval": {
                            "type": "boolean"
                          },
                          "allowFeeEdit": {
                            "type": "boolean"
                          },
                          "isRequired": {
                            "type": "boolean"
                          },
                          "isSuggested": {
                            "type": "boolean"
                          },
                          "maxEdit": {
                            "type": "integer"
                          }
                        }
                      }
                    },
                    "taxes": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "id": {
                            "type": "integer"
                          },
                          "name": {
                            "type": "string"
                          },
                          "rate": {
                            "type": "string"
                          },
                          "value": {
                            "type": "string"
                          }
                        }
                      }
                    },
                    "paymentPlan": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "date": {
                            "type": "string"
                          },
                          "amount": {
                            "type": "string"
                          }
                        }
                      }
                    },
                    "insuranceProducts": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "id": {
                            "type": "integer"
                          },
                          "name": {
                            "type": "string"
                          },
                          "type": {
                            "type": "string"
                          },
                          "value": {
                            "type": "boolean"
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          },
          "401": {
            "description": "Unauthorized",
            "content": {
              "application/json": {
                "schema": {
                  "title": "Api Problem Response",
                  "type": "object",
                  "x-examples": {
                    "Invalid Authentication": {
                      "type": "http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html",
                      "title": "Forbidden",
                      "status": 403,
                      "detail": "Forbidden"
                    }
                  },
                  "description": "In an error situation, we will return a json object with details of the error. This response is based on the following specification: https://tools.ietf.org/html/rfc7807",
                  "properties": {
                    "code": {
                      "type": "string",
                      "description": "New code structure to track errors for endpoints rather than matching description strings.\nThese will start to appear in all endpoints starting March 2021.\n"
                    },
                    "type": {
                      "type": "string",
                      "format": "uri",
                      "example": "http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html",
                      "description": "A URI reference that identifies the problem type."
                    },
                    "title": {
                      "type": "string",
                      "description": "A short, human-readable summary of the problem type."
                    },
                    "status": {
                      "example": 200,
                      "description": "HTTP status code",
                      "type": "integer"
                    },
                    "detail": {
                      "type": "string",
                      "description": "A human-readable explanation specific to this occurrence of the problem."
                    },
                    "validation_messages": {
                      "type": "array",
                      "description": "We use this to send validation message, often in conjunction with 400 or 422 status codes.",
                      "items": {
                        "type": "string"
                      }
                    }
                  },
                  "required": [
                    "type",
                    "title",
                    "status",
                    "detail"
                  ]
                }
              }
            }
          },
          "403": {
            "description": "Forbidden",
            "content": {
              "application/json": {
                "schema": {
                  "title": "Api Problem Response",
                  "type": "object",
                  "x-examples": {
                    "Invalid Authentication": {
                      "type": "http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html",
                      "title": "Forbidden",
                      "status": 403,
                      "detail": "Forbidden"
                    }
                  },
                  "description": "In an error situation, we will return a json object with details of the error. This response is based on the following specification: https://tools.ietf.org/html/rfc7807",
                  "properties": {
                    "code": {
                      "type": "string",
                      "description": "New code structure to track errors for endpoints rather than matching description strings.\nThese will start to appear in all endpoints starting March 2021.\n"
                    },
                    "type": {
                      "type": "string",
                      "format": "uri",
                      "example": "http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html",
                      "description": "A URI reference that identifies the problem type."
                    },
                    "title": {
                      "type": "string",
                      "description": "A short, human-readable summary of the problem type."
                    },
                    "status": {
                      "example": 200,
                      "description": "HTTP status code",
                      "type": "integer"
                    },
                    "detail": {
                      "type": "string",
                      "description": "A human-readable explanation specific to this occurrence of the problem."
                    },
                    "validation_messages": {
                      "type": "array",
                      "description": "We use this to send validation message, often in conjunction with 400 or 422 status codes.",
                      "items": {
                        "type": "string"
                      }
                    }
                  },
                  "required": [
                    "type",
                    "title",
                    "status",
                    "detail"
                  ]
                }
              }
            }
          },
          "500": {
            "description": "Internal Server Error",
            "content": {
              "application/json": {
                "schema": {
                  "title": "Api Problem Response",
                  "type": "object",
                  "x-examples": {
                    "Invalid Authentication": {
                      "type": "http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html",
                      "title": "Forbidden",
                      "status": 403,
                      "detail": "Forbidden"
                    }
                  },
                  "description": "In an error situation, we will return a json object with details of the error. This response is based on the following specification: https://tools.ietf.org/html/rfc7807",
                  "properties": {
                    "code": {
                      "type": "string",
                      "description": "New code structure to track errors for endpoints rather than matching description strings.\nThese will start to appear in all endpoints starting March 2021.\n"
                    },
                    "type": {
                      "type": "string",
                      "format": "uri",
                      "example": "http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html",
                      "description": "A URI reference that identifies the problem type."
                    },
                    "title": {
                      "type": "string",
                      "description": "A short, human-readable summary of the problem type."
                    },
                    "status": {
                      "example": 200,
                      "description": "HTTP status code",
                      "type": "integer"
                    },
                    "detail": {
                      "type": "string",
                      "description": "A human-readable explanation specific to this occurrence of the problem."
                    },
                    "validation_messages": {
                      "type": "array",
                      "description": "We use this to send validation message, often in conjunction with 400 or 422 status codes.",
                      "items": {
                        "type": "string"
                      }
                    }
                  },
                  "required": [
                    "type",
                    "title",
                    "status",
                    "detail"
                  ]
                }
              }
            }
          }
        },
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "title": "Create Reservation Quote V2",
                "type": "object",
                "description": "Expected response when receiving an OK response from the API.",
                "properties": {
                  "quotes": {
                    "type": "object",
                    "description": "This can be used to pass multiple quotes at once. If you use this, the body of each object should follow the body parameters listed below."
                  },
                  "unitId": {
                    "type": "number"
                  },
                  "arrivalDate": {
                    "type": "string",
                    "format": "date",
                    "description": "Date in ISO 8601 format."
                  },
                  "departureDate": {
                    "type": "string",
                    "format": "date",
                    "description": "Date in ISO 8601 format."
                  },
                  "rateTypeId": {
                    "type": "number",
                    "description": "Override the automated get Best Available Rate\n\nIf rate is not found or active\nthen a 422 error will be thrown `Rate type is invalid or not active.`\n"
                  },
                  "guaranteePolicyId": {
                    "type": "integer",
                    "nullable": true,
                    "description": "Override the automated Guarantee Policy Selection\n\n- must have Reservation Type set to allow Charge Rates\n- Policy must be active\n- Policy must be applied to or inherited by the unit (only required for channel contexts)\n    - Inheritance is OFF if defined on the unit, also can only inherits from the closest node.\n\nOtherwise defaults to automated selection of guarantee policy based on priority of policies set on unit, else default policy in system configuration.\n\n## other cases that will change the policy\n\n- `isVirtual` : will set the policy to #2 *Credit Card Guarantee*. Only if guaranteePolicyId is NOT set.\n- no active/matched : will set the policy to #3 *Non-Guaranteed Hold*\n"
                  },
                  "cancellationPolicyId": {
                    "type": "integer",
                    "description": "Manually set cancellation policy for reservation. If using channel, policy will automatically be set based on unit."
                  },
                  "typeId": {
                    "type": "integer",
                    "nullable": true,
                    "description": "server/unit only, defaults to typeId 1"
                  },
                  "occupants": {
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "type": {
                          "type": "string",
                          "description": "Either handle or integer of occupant type."
                        },
                        "count": {
                          "type": "number"
                        }
                      }
                    }
                  },
                  "discount": {
                    "type": "number"
                  },
                  "groupId": {
                    "type": "number"
                  },
                  "guestFees": {
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "chargeId": {
                          "type": "integer"
                        },
                        "quantity": {
                          "type": "number"
                        },
                        "unitValue": {
                          "type": "number"
                        },
                        "value": {
                          "type": "number",
                          "description": "Total fee value (Quantity * unitValue)"
                        }
                      }
                    }
                  },
                  "ownerFees": {
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "chargeId": {
                          "type": "integer"
                        },
                        "quantity": {
                          "type": "number"
                        },
                        "unitValue": {
                          "type": "number"
                        },
                        "value": {
                          "type": "number",
                          "description": "Total fee value (Quantity * unitValue)"
                        }
                      }
                    }
                  },
                  "channelId": {
                    "type": "number"
                  },
                  "contactId": {
                    "type": "number"
                  },
                  "unitTypeId": {
                    "type": "number"
                  },
                  "guestIntendsInsurance": {
                    "type": "boolean"
                  },
                  "guestIntendsWaiver": {
                    "type": "boolean"
                  },
                  "taxExempt": {
                    "type": "boolean"
                  },
                  "discountReason": {
                    "type": "number",
                    "description": "Discount reason ID"
                  },
                  "discountNotes": {
                    "type": "string"
                  },
                  "source": {
                    "type": "string"
                  },
                  "campaignId": {
                    "type": "number"
                  },
                  "leadId": {
                    "type": "number"
                  }
                },
                "required": [
                  "unitId",
                  "arrivalDate",
                  "departureDate"
                ]
              }
            }
          }
        },
        "description": "Create a new Reservation Quote V2.",
        "security": [
          {
            "basic": []
          },
          {
            "hmac": []
          }
        ],
        "tags": [
          "Quote V2"
        ]
      }
    }
  },
  "components": {
    "securitySchemes": {
      "hmac": {
        "type": "http",
        "scheme": "bearer",
        "description": "HMAC Authentication based on https://github.com/acquia/http-hmac-spec/tree/2.0"
      },
      "basic": {
        "type": "http",
        "scheme": "basic",
        "description": "Authentication is unique to each customer. Please request authorization keys from the customer you are integrating with."
      }
    }
  },
  "security": [
    {
      "basic": []
    },
    {
      "hmac": []
    }
  ],
  "servers": [
    {
      "url": "{customerDomain}/api",
      "variables": {
        "customerDomain": {
          "default": "https://api-integration-example.tracksandbox.io",
          "description": "API domain"
        }
      }
    }
  ],
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": true
  }
}
```