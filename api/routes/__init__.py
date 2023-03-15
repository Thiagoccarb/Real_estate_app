from fastapi import APIRouter

from schemas.base import MissingFieldErrorSchema
from routes.property_route import property_router
from routes.image_route import image_router
from routes.city_route import city_router
from routes.address_route import address_router
from routes.auth_route import auth_router
from routes.user_route import user_router


app_router = APIRouter(redirect_slashes=True)

app_router.include_router(
    property_router,
    responses={
        201: {
            "description": "data created",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "error": None,
                        "result": {
                            "id": 7,
                            "name": "house 2",
                            "created_at": "2023-02-27T01:13:04",
                            "updated_at": None,
                        },
                    },
                }
            },
        },
        400: {
            "description": "missing_field",
            "model": MissingFieldErrorSchema,
        },
        422: {},
    },
)
app_router.include_router(
    image_router,
    responses={
        201: {
            "description": "data created",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "error": None,
                        "result": {
                            "id": 1,
                            "name": "city_name",
                            "state": "state",
                        },
                    },
                }
            },
        },
        400: {
            "description": "missing_field",
            "model": MissingFieldErrorSchema,
        },
        422: {
            "description": "unprocessable_entity",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "error": {
                            "type": "unprocessable_entity",
                            "description": f"invalid binary string",
                        },
                    }
                }
            },
        },
    },
)

app_router.include_router(
    city_router,
    responses={
        201: {
            "description": "data created",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "error": None,
                        "result": {
                            "id": 7,
                            "name": "city 1",
                            "state": "state",
                            "created_at": "2023-03-03T01:41:10",
                        },
                    },
                }
            },
        },
        400: {
            "description": "missing_field",
            "model": MissingFieldErrorSchema,
        },
        422: {},
    },
)

app_router.include_router(
    address_router,
    responses={
        201: {
            "description": "data created",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "error": None,
                        "result": {
                            "id": 7,
                            "street_name": "street_name",
                            "city_id": 1,
                            "number": 123,
                            "cep": "11111-111",
                        },
                    },
                }
            },
        },
        400: {
            "description": "missing_field",
            "model": MissingFieldErrorSchema,
        },
        422: {},
    },
)

app_router.include_router(
    auth_router,
    responses={
        200: {
            "description": "token granted",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "error": None,
                        "result": {"token": "eyJhbGc..."},
                    },
                }
            },
        },
        400: {
            "description": "missing_field",
            "model": MissingFieldErrorSchema,
        },
        401: {
            "description": "unauthorized",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                       	"error": {
		                    "type": "invalid_credentials",
		                    "description": "invalid credentials"
	                    }
                    },
                },
            },
        },
        422:{}
    },
)

app_router.include_router(
    user_router,
    responses={
        200: {
            "description": "user created",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "error": None,
                        "result": {
                            "id": 1,
                            "username": "username",
                            "email": "email",
                            "password": "password",
                            "created_at": "2023-03-08T17:19:19",
                            "updated_at": None,
                        },
                    },
                }
            },
        },
        400: {
            "description": "missing_field",
            "model": MissingFieldErrorSchema,
        },
        422: {},
    },
)
