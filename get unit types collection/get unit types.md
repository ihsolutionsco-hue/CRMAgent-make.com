Get all Unit Types

# OpenAPI definition
```json
{
  "_id": "/branches/1.0/apis/channel-api.json",
  "openapi": "3.0.0",
  "info": {
    "title": "Channel API",
    "version": "1.0",
    "description": "This API is intended to be used in channel (OTA, channel managers, websites and other similar sites) integrations.\n\nAn account can limit which data is visible in this API to any given channel.",
    "contact": {
      "name": "Track Support",
      "email": "support@trackhs.com",
      "url": "https://support.trackhs.com"
    }
  },
  "tags": [
    {
      "name": "Unit Types",
      "description": "Endpoints which provide unit type data and information."
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
    "/pms/units/types": {
      "get": {
        "summary": "Get all Unit Types",
        "responses": {
          "200": {
            "description": "OK",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "_embedded": {
                      "type": "object",
                      "properties": {
                        "units": {
                          "type": "array",
                          "items": {
                            "title": "Unit Type Response",
                            "type": "object",
                            "description": "Unit Type Response",
                            "properties": {
                              "id": {
                                "type": "integer"
                              },
                              "name": {
                                "type": "string"
                              },
                              "nodeId": {
                                "type": "integer"
                              },
                              "shortDescription": {
                                "type": "string"
                              },
                              "longDescription": {
                                "type": "string"
                              },
                              "lodgingTypeId": {
                                "type": "integer"
                              },
                              "petFriendly": {
                                "type": "string"
                              },
                              "directions": {
                                "type": "string"
                              },
                              "checkinDetails": {
                                "type": "string"
                              },
                              "timezone": {
                                "type": "string",
                                "description": "timezone string."
                              },
                              "checkinTime": {
                                "type": "string"
                              },
                              "hasEarlyCheckin": {
                                "type": "boolean"
                              },
                              "earlyCheckinTime": {
                                "type": "string"
                              },
                              "checkoutTime": {
                                "type": "string"
                              },
                              "hasLateCheckout": {
                                "type": "boolean"
                              },
                              "lateCheckoutTime": {
                                "type": "string"
                              },
                              "websiteUrl": {
                                "type": "string"
                              },
                              "maxOccupancy": {
                                "type": "integer"
                              },
                              "phone": {
                                "type": "string"
                              },
                              "streetAddress": {
                                "type": "string"
                              },
                              "extendedAddress": {
                                "type": "string"
                              },
                              "locality": {
                                "type": "string"
                              },
                              "region": {
                                "type": "string"
                              },
                              "postal": {
                                "type": "string"
                              },
                              "country": {
                                "type": "string"
                              },
                              "longitude": {
                                "type": "string",
                                "description": "longitude in coordinate format."
                              },
                              "latitude": {
                                "type": "string",
                                "description": "longitude in coordinate format."
                              },
                              "petsFriendly": {
                                "type": "boolean"
                              },
                              "maxPets": {
                                "type": "integer"
                              },
                              "eventsAllowed": {
                                "type": "boolean"
                              },
                              "smokingAllowed": {
                                "type": "boolean"
                              },
                              "childrenAllowed": {
                                "type": "boolean"
                              },
                              "minimumAgeLimit": {
                                "type": "integer"
                              },
                              "isAccessible": {
                                "type": "boolean"
                              },
                              "area": {
                                "type": "string",
                                "description": "area of the unit in sq. ft."
                              },
                              "floors": {
                                "type": "integer",
                                "description": "Number of floors / level in unit type."
                              },
                              "securityDeposit": {
                                "type": "string",
                                "description": "should be a decimal number value."
                              },
                              "bedrooms": {
                                "type": "integer"
                              },
                              "fullBathrooms": {
                                "type": "integer"
                              },
                              "threeQuarterBathroom": {
                                "type": "integer"
                              },
                              "halfBathrooms": {
                                "type": "integer"
                              },
                              "houseRules": {
                                "type": "string"
                              },
                              "bedTypes": {
                                "type": "array",
                                "description": "Specify what bed types are available in this unit type. Inherits to unit."
                              },
                              "rooms": {
                                "type": "array",
                                "description": "Rooms configuration st up on the unit."
                              },
                              "amenities": {
                                "type": "array",
                                "items": {
                                  "type": "object",
                                  "properties": {
                                    "amenity": {
                                      "type": "object",
                                      "properties": {
                                        "id": {
                                          "type": "integer"
                                        },
                                        "name": {
                                          "type": "string"
                                        },
                                        "group": {
                                          "type": "object",
                                          "properties": {
                                            "id": {
                                              "type": "integer"
                                            },
                                            "name": {
                                              "type": "string"
                                            }
                                          }
                                        },
                                        "count": {
                                          "type": "integer"
                                        },
                                        "description": {
                                          "type": "string"
                                        },
                                        "instruction": {
                                          "type": "string"
                                        }
                                      }
                                    }
                                  }
                                },
                                "description": "List of amenities on this unit type"
                              },
                              "amenityDescription": {
                                "type": "string"
                              },
                              "custom": {
                                "type": "object",
                                "description": "Lists out the custom fields applied to unit types, and their current value on this specific type."
                              },
                              "updated": {
                                "type": "object",
                                "description": "Specifies when each part of the type was updated in ISO 8601 dateTime format.",
                                "properties": {
                                  "availability": {
                                    "type": "string"
                                  },
                                  "content": {
                                    "type": "string"
                                  },
                                  "pricing": {
                                    "type": "string"
                                  }
                                }
                              },
                              "localOfficeId": {
                                "type": "integer"
                              },
                              "taxId": {
                                "type": "integer"
                              },
                              "updatedAt": {
                                "type": "string",
                                "description": "DateTime that this was updated, in ISO 8601 dateTime format."
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
                              }
                            }
                          }
                        }
                      }
                    },
                    "page": {
                      "type": "number"
                    },
                    "page_count": {
                      "type": "number"
                    },
                    "page_size": {
                      "type": "number"
                    },
                    "total_items": {
                      "type": "number"
                    },
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
                    }
                  },
                  "required": [
                    "_embedded",
                    "page",
                    "page_count",
                    "page_size",
                    "total_items",
                    "_links"
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
        "operationId": "getUnitTypes",
        "description": "This endpoint will return all unit types.",
        "parameters": [
          {
            "schema": {
              "type": "integer",
              "maximum": 0,
              "minimum": 0
            },
            "in": "query",
            "name": "page",
            "description": "Page number of result set - Limited to 10k total results (page * size)"
          },
          {
            "schema": {
              "type": "integer"
            },
            "in": "query",
            "name": "size",
            "description": "Size of page - Limited to 10k total results (page * size)"
          },
          {
            "schema": {
              "type": "string",
              "default": "name",
              "enum": [
                "id",
                "name",
                "nodeName",
                "shortDescription",
                "longDescription",
                "createdAt"
              ]
            },
            "in": "query",
            "name": "sortColumn",
            "description": "Column to sort the result set."
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
            "name": "sortDirection",
            "description": "Direction to sort result set."
          },
          {
            "schema": {
              "oneOf": [
                {
                  "title": "Single Node",
                  "type": "integer"
                },
                {
                  "title": "Multiple Nodes",
                  "type": "array",
                  "items": {
                    "type": "integer"
                  }
                }
              ]
            },
            "in": "query",
            "name": "nodeId",
            "description": "Return all units that are decendents of the specific node ID(s). Can be single value or array."
          },
          {
            "schema": {
              "type": "string",
              "format": "date"
            },
            "in": "query",
            "name": "updatedSince",
            "deprecated": true,
            "description": "Date in ISO 8601 format. Will return all units updated since timestamp."
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "search",
            "description": "substring search matching on name or descriptions"
          },
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "term",
            "description": "substring search matching on term"
          },
          {
            "schema": {
              "type": "integer"
            },
            "in": "query",
            "name": "calendarId",
            "description": "Return all units matching this unit's type with calendar group id"
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
            "name": "allowUnitRates",
            "description": "Return all units who's type allows unit rates"
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
            "name": "isActive",
            "description": "Return active (true), inactive (false), or all (null) units"
          }
        ],
        "tags": [
          "Unit Types"
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
  "x-readme": {
    "explorer-enabled": true,
    "proxy-enabled": true
  }
}
```