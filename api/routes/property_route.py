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
                                "name": "house 1",
                                "action": None,
                                "type": None,
                                "address_id": None,
                                "created_at": "2023-02-26T19:19:39",
                                "updated_at": None,
                                "image_ids": [
                                    1,
                                    2,
                                    3,
                                    4,
                                ],
                            },
                            {
                                "id": 11,
                                "name": "property",
                                "action": "rent",
                                "type": "apartment",
                                "address_id": 10,
                                "created_at": "2023-03-13T23:42:10",
                                "updated_at": None,
                                "image_ids": [],
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
