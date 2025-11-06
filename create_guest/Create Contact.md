Create Contact

# OpenAPI definition
```json
{
  "_id": "/branches/1.0/apis/crm-api.json",
  "openapi": "3.0.0",
  "info": {
    "title": "CRM API",
    "version": "1.0",
    "contact": {
      "name": "Track Support",
      "email": "support@trackhs.com",
      "url": "https://support.trackhs.com"
    },
    "description": "This provides access to the core entities which make up the CRM component of the platform.\n\nThis requires a server or user key conext to accesss."
  },
  "tags": [
    {
      "name": "Contact"
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
  "paths": {
    "/crm/contacts": {
      "post": {
        "tags": [
          "Contact"
        ],
        "summary": "Create Contact",
        "operationId": "createContact",
        "responses": {
          "201": {
            "description": "Created",
            "content": {
              "application/json": {
                "schema": {
                  "title": "Contact Response",
                  "type": "object",
                  "description": "",
                  "properties": {
                    "id": {
                      "type": "integer",
                      "description": "ID"
                    },
                    "firstName": {
                      "type": "string",
                      "description": "Name of policy",
                      "minLength": 1,
                      "maxLength": 64
                    },
                    "lastName": {
                      "type": "string"
                    },
                    "primaryEmail": {
                      "type": "string",
                      "format": "email",
                      "description": "Primary email assigned to contact. Must be unique."
                    },
                    "secondaryEmail": {
                      "type": "string",
                      "format": "email",
                      "description": "Alternative or secondary email assigned to contact. Must be unique."
                    },
                    "homePhone": {
                      "type": "string",
                      "description": "Use E.164 Format, non complaint numbers will be processed within US locale."
                    },
                    "cellPhone": {
                      "type": "string",
                      "description": "Use E.164 Format, non complaint numbers will be processed within US locale."
                    },
                    "workPhone": {
                      "type": "string",
                      "description": "Use E.164 Format, non complaint numbers will be processed within US locale."
                    },
                    "otherPhone": {
                      "type": "string",
                      "description": "Use E.164 Format, non complaint numbers will be processed within US locale."
                    },
                    "fax": {
                      "type": "string",
                      "description": "Use E.164 Format, non complaint numbers will be processed within US locale."
                    },
                    "streetAddress": {
                      "type": "string"
                    },
                    "country": {
                      "type": "string",
                      "example": "US",
                      "minLength": 2,
                      "maxLength": 2,
                      "description": "ISO 2 Character Country Code"
                    },
                    "postalCode": {
                      "type": "string"
                    },
                    "region": {
                      "type": "string"
                    },
                    "locality": {
                      "type": "string"
                    },
                    "extendedAddress": {
                      "type": "string",
                      "nullable": true
                    },
                    "notes": {
                      "type": "string"
                    },
                    "anniversary": {
                      "type": "string",
                      "pattern": "^(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|30|31)$"
                    },
                    "birthdate": {
                      "type": "string",
                      "pattern": "^(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|30|31)$"
                    },
                    "isVip": {
                      "type": "boolean"
                    },
                    "isBlacklist": {
                      "type": "boolean"
                    },
                    "taxId": {
                      "type": "string",
                      "nullable": true,
                      "description": "1099 Tax Id (Restricted)"
                    },
                    "paymentType": {
                      "type": "string",
                      "description": "Payment type, used for ACH or Check payments. (Restricted)",
                      "deprecated": true,
                      "enum": [
                        "print",
                        "direct"
                      ]
                    },
                    "achAccountNumber": {
                      "type": "string",
                      "description": "ACH Account Number (Restricted)",
                      "deprecated": true
                    },
                    "achRoutingNumber": {
                      "type": "string",
                      "description": "ACH Routing Number (Restricted)",
                      "deprecated": true,
                      "minLength": 9,
                      "maxLength": 9,
                      "pattern": "^[0-9]{9}$"
                    },
                    "achAccountType": {
                      "type": "string",
                      "enum": [
                        "business-checking",
                        "business-savings",
                        "personal-checking",
                        "personal-savings"
                      ],
                      "deprecated": true,
                      "description": "Used if payment type is ACH. (Restricted)"
                    },
                    "references": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "reference": {
                            "type": "string"
                          },
                          "salesLinkId": {
                            "type": "integer"
                          },
                          "channelId": {
                            "type": "integer"
                          }
                        }
                      }
                    },
                    "tags": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "id": {
                            "type": "integer",
                            "description": "ID"
                          },
                          "name": {
                            "type": "string"
                          }
                        }
                      }
                    },
                    "customValues": {
                      "type": "object",
                      "description": "Keys are determined by customer. Values are either string or array depending on type",
                      "properties": {
                        "custom_n": {
                          "oneOf": [
                            {
                              "type": "string"
                            },
                            {
                              "type": "array"
                            }
                          ],
                          "items": {}
                        }
                      }
                    },
                    "_links": {
                      "type": "object",
                      "properties": {
                        "self": {
                          "type": "object",
                          "properties": {
                            "href": {
                              "type": "string"
                            }
                          }
                        }
                      }
                    },
                    "updatedAt": {
                      "type": "string",
                      "format": "date-time",
                      "description": "Date as ISO 8601 format"
                    },
                    "updatedBy": {
                      "type": "string"
                    },
                    "createdAt": {
                      "type": "string",
                      "format": "date-time",
                      "description": "Date as ISO 8601 format"
                    },
                    "createdBy": {
                      "type": "string"
                    },
                    "noIdentity": {
                      "type": "boolean",
                      "description": "Contacts that do not have identity information"
                    }
                  },
                  "x-readme-ref-name": "ContactsResponse"
                }
              }
            }
          },
          "401": {
            "description": "Unauthorized"
          },
          "403": {
            "description": "Forbidden"
          },
          "500": {
            "description": "Internal Server Error"
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
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "title": "contact",
                "type": "object",
                "description": "At least one of the following is required: cellPhone, homePhone, otherPhone, primaryEmail or secondaryEmail",
                "properties": {
                  "firstName": {
                    "type": "string",
                    "description": "First Name",
                    "maxLength": 32
                  },
                  "lastName": {
                    "type": "string",
                    "description": "Last Name",
                    "maxLength": 32
                  },
                  "primaryEmail": {
                    "type": "string",
                    "format": "email",
                    "description": "Primary email assigned to contact. Must be unique from primary and secondary email addresses. Must be unique to primary and secondary emails for all contacts",
                    "maxLength": 100
                  },
                  "secondaryEmail": {
                    "type": "string",
                    "format": "email",
                    "description": "Alternative or secondary email assigned to contact. Must be unique to primary and secondary emails for all contacts.",
                    "maxLength": 100
                  },
                  "proxyEmail": {
                    "type": "string",
                    "format": "email",
                    "description": "Alternative or secondary email assigned to contact. Must be unique to primary and secondary emails for all contacts. Wont be used yet, but will be in the future\n",
                    "maxLength": 100
                  },
                  "homePhone": {
                    "type": "string",
                    "description": "Use E.164 Format, non complaint numbers will be processed within US locale. Must be unique to home, cell, and other phone numbers for all contacts",
                    "maxLength": 16
                  },
                  "cellPhone": {
                    "type": "string",
                    "description": "Use E.164 Format, non complaint numbers will be processed within US locale. Must be unique to home, cell, and other phone numbers for all contacts",
                    "maxLength": 16
                  },
                  "workPhone": {
                    "type": "string",
                    "description": "Use E.164 Format, non complaint numbers will be processed within US locale.",
                    "maxLength": 16
                  },
                  "otherPhone": {
                    "type": "string",
                    "description": "Use E.164 Format, non complaint numbers will be processed within US locale. Must be unique to home, cell, and other phone numbers for all contacts",
                    "maxLength": 16
                  },
                  "fax": {
                    "type": "string",
                    "description": "Use E.164 Format, non complaint numbers will be processed within US locale.",
                    "maxLength": 16
                  },
                  "streetAddress": {
                    "type": "string",
                    "maxLength": 255
                  },
                  "country": {
                    "type": "string",
                    "example": "US",
                    "minLength": 2,
                    "maxLength": 2,
                    "description": "ISO 2 Character Country Code"
                  },
                  "postalCode": {
                    "type": "string",
                    "maxLength": 16
                  },
                  "region": {
                    "type": "string"
                  },
                  "locality": {
                    "type": "string"
                  },
                  "extendedAddress": {
                    "type": "string",
                    "nullable": true,
                    "maxLength": 255
                  },
                  "notes": {
                    "type": "string",
                    "maxLength": 4000
                  },
                  "anniversary": {
                    "type": "string",
                    "pattern": "^(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|30|31)$"
                  },
                  "birthdate": {
                    "type": "string",
                    "pattern": "^(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|30|31)$"
                  },
                  "isBlacklist": {
                    "type": "boolean"
                  },
                  "taxId": {
                    "type": "string",
                    "nullable": true,
                    "description": "1099 Tax Id (Restricted)",
                    "maxLength": 16
                  },
                  "paymentType": {
                    "type": "string",
                    "description": "Payment type, used for ACH or Check payments. (Restricted)",
                    "deprecated": true,
                    "enum": [
                      "print",
                      "direct"
                    ]
                  },
                  "achAccountNumber": {
                    "type": "string",
                    "description": "ACH Account Number (Restricted)",
                    "deprecated": true
                  },
                  "achRoutingNumber": {
                    "type": "string",
                    "description": "ACH Routing Number (Restricted)",
                    "deprecated": true,
                    "minLength": 9,
                    "maxLength": 9,
                    "pattern": "^[0-9]{9}$"
                  },
                  "achAccountType": {
                    "type": "string",
                    "enum": [
                      "business-checking",
                      "business-savings",
                      "personal-checking",
                      "personal-savings"
                    ],
                    "deprecated": true,
                    "description": "Used if payment type is ACH. (Restricted)"
                  },
                  "references": {
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "reference": {
                          "type": "string"
                        },
                        "salesLinkId": {
                          "type": "integer",
                          "nullable": true
                        },
                        "channelId": {
                          "type": "integer",
                          "nullable": true
                        }
                      }
                    }
                  },
                  "tags": {
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "id": {
                          "type": "number"
                        }
                      }
                    }
                  },
                  "customValues": {
                    "type": "object",
                    "description": "Keys are determinied by customer. Values are either string or array depending on type",
                    "properties": {
                      "custom_n": {
                        "oneOf": [
                          {
                            "type": "string"
                          },
                          {
                            "type": "array"
                          }
                        ],
                        "items": {}
                      }
                    }
                  }
                },
                "required": [
                  "firstName",
                  "lastName",
                  "primaryEmail",
                  "homePhone",
                  "cellPhone",
                  "otherPhone"
                ],
                "x-readme-ref-name": "ContactsRequest"
              }
            }
          },
          "description": ""
        },
        "description": "Contacts include guests, owners, or vendor employees. This endpoint will add a new contact. "
      }
    }
  },
  "components": {
    "securitySchemes": {
      "basic": {
        "type": "http",
        "scheme": "basic",
        "description": "Authentication is unique to each customer. Please request authorization keys from the customer you are integrating with."
      },
      "hmac": {
        "type": "http",
        "scheme": "bearer",
        "description": "HMAC Authentication based on https://github.com/acquia/http-hmac-spec/tree/2.0"
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
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": true
  }
}
```