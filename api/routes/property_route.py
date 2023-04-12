from fastapi.routing import APIRouter

from schemas.property_schemas import (
    CreatePropertyResponse,
    ListPropertyResponse,
    RemovePropertyResponse,
    UpdatePropertyRequest,
    UpdatePropertyResponse,
)
from controllers.property_controller import PropertyController


property_controller = PropertyController()


property_router = APIRouter(prefix="/properties", tags=["properties"])

property_router.add_api_route(
    "",
    property_controller.add,
    methods=["POST"],
    status_code=201,
    response_model=CreatePropertyResponse,
)

property_router.add_api_route(
    "/{id}",
    property_controller.remove_by_id,
    methods=["DELETE"],
    status_code=200,
    response_model=RemovePropertyResponse,
)

property_router.add_api_route(
    "/{id}",
    property_controller.update_by_id,
    methods=["PATCH"],
    status_code=200,
    response_model=UpdatePropertyResponse,
    responses={
        200: {
            "success": True,
            "error": None,
            "result": {
                "name": "property",
                "action": "rent",
                "type": "apartment",
                "address": {"street_name": "test", "cep": "11111-111"},
                "city": {"name": "São Paulo", "state": "SP"},
            },
            "message": None,
        },
        201: {},
        422: {},
    },
)

property_router.add_api_route(
    "",
    property_controller.find_all,
    methods=["GET"],
    status_code=200,
    response_model=ListPropertyResponse,
    responses={
        200: {
            "description": "list properties",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "error": None,
                        "result": [
                            {
                                "id": 1,
                                "name": "property",
                                "action": "sale",
                                "type": "apartment",
                                "created_at": "2023-03-30T02:19:29",
                                "updated_at": None,
                                "price": 100000,
                                "bedrooms": 0,
                                "bathrooms": 0,
                                "description": "",
                                "image_urls": [],
                                "address": {
                                    "street_name": "",
                                    "number": 100,
                                    "cep": "11111-111"
                                },
                                "city": {
                                    "name": "teste",
                                    "state": "SP"
                                }
                                },
                                {
                                "id": 2,
                                "name": "property",
                                "action": "rent",
                                "type": "apartment",
                                "created_at": "2023-04-11T01:55:47",
                                "updated_at": None,
                                "price": 200000,
                                "bedrooms": 3,
                                "bathrooms": 4,
                                "description": "beautiful house",
                                "image_urls": [],
                                "address": {
                                    "street_name": "test street",
                                    "number": 100,
                                    "cep": "11111-112"
                                },
                                "city": {
                                    "name": "Ribeirão Preto",
                                    "state": "SP"
                                }
                            },
                        ],
                    },
                }
            },
        },
        201: {
            "description": "Not Available",
        },
        400: {
            "description": "invalid_query",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "error": {
                            "description": "Query limit must be no greater than 50"
                        },
                    },
                }
            },
        },
    },
)
