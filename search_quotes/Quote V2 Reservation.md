Quote V2 Reservation

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
      "get": {
        "summary": "Quote V2 Reservation",
        "operationId": "GetQuotesCollectionV2",
        "responses": {
          "200": {
            "description": "OK",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "_links": {
                      "title": "CollectionLinks",
                      "type": "object",
                      "properties": {
                        "self": {
                          "type": "object",
                          "required": [
                            "href"
                          ],
                          "properties": {
                            "href": {
                              "type": "string"
                            }
                          }
                        },
                        "first": {
                          "type": "object",
                          "properties": {
                            "href": {
                              "type": "string"
                            }
                          },
                          "required": [
                            "href"
                          ]
                        },
                        "last": {
                          "type": "object",
                          "properties": {
                            "href": {
                              "type": "string"
                            }
                          },
                          "required": [
                            "href"
                          ]
                        },
                        "next": {
                          "type": "object",
                          "properties": {
                            "href": {
                              "type": "string"
                            }
                          },
                          "required": [
                            "href"
                          ]
                        },
                        "prev": {
                          "type": "object",
                          "properties": {
                            "href": {
                              "type": "string"
                            }
                          },
                          "required": [
                            "href"
                          ]
                        }
                      },
                      "required": [
                        "self",
                        "first",
                        "last"
                      ],
                      "description": "All collections provide the following set of links. Next or prev will only be provided if there is a next or previous page.",
                      "x-examples": {}
                    },
                    "total_items": {
                      "type": "number"
                    },
                    "page_size": {
                      "type": "number"
                    },
                    "page_count": {
                      "type": "number"
                    },
                    "page": {
                      "type": "number"
                    },
                    "_embedded": {
                      "type": "object",
                      "properties": {
                        "amenities": {
                          "type": "array",
                          "items": {
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
                    }
                  },
                  "required": [
                    "_links",
                    "total_items",
                    "page_size",
                    "page_count",
                    "page",
                    "_embedded"
                  ]
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
          "404": {
            "description": "Not Found",
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
          "422": {
            "description": "Unprocessable Entity (WebDAV)"
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
        "description": "Get a quote for the unit that have been enabled for your channel key.",
        "parameters": [
          {
            "schema": {
              "type": "number",
              "maximum": 0,
              "minimum": 0
            },
            "in": "query",
            "name": "page",
            "description": "Page Number"
          },
          {
            "schema": {
              "type": "number"
            },
            "in": "query",
            "name": "size",
            "description": "Page Size"
          },
          {
            "schema": {
              "type": "string",
              "enum": [
                "id",
                "order",
                "isPublic",
                "publicSearchable",
                "isFilterable",
                "createdAt"
              ],
              "default": "order"
            },
            "in": "query",
            "name": "sortColumn",
            "description": ""
          },
          {
            "schema": {
              "type": "string",
              "enum": [
                "asc",
                "desc"
              ],
              "default": "asc"
            },
            "in": "query",
            "name": "sortDirection"
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "search",
            "description": "search on id and/or name"
          },
          {
            "schema": {
              "type": "number"
            },
            "in": "query",
            "name": "contactId",
            "description": "Search on contact id."
          },
          {
            "schema": {
              "type": "number"
            },
            "in": "query",
            "name": "unitId",
            "description": "Search on unit id."
          },
          {
            "schema": {
              "type": "number"
            },
            "in": "query",
            "name": "unitTypeId",
            "description": "Search on unit type id."
          },
          {
            "schema": {
              "type": "integer",
              "enum": [
                1,
                0
              ]
            },
            "in": "query",
            "name": "futureQuotes"
          },
          {
            "schema": {
              "type": "number"
            },
            "in": "query",
            "name": "activeQuotes"
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