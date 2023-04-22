from fastapi.routing import APIRouter

from schemas.user_schemas import CreateUserResponse
from controllers.user_controller import UserController


user_controller = UserController()


user_router = APIRouter(prefix="/users", tags=["users"])

user_router.add_api_route(
    "",
    user_controller.add,
    methods=["POST"],
    status_code=201,
    response_model=CreateUserResponse,
)

user_router.add_api_route(
    "/send-email",
    user_controller.send_email,
    responses={
        200: {
            "description": "Ok",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "error": None,
                        "result": None,
                        "message": "Please, check your email.",
                    }
                },
            },
        },
        201: {"description": "N/A"},
    },
    methods=["POST"],
    status_code=200,
)

user_router.add_api_route(
    "/reset-password",
    user_controller.reset_password,
    responses={
        200: {
            "description": "Ok",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "error": None,
                        "result": None,
                        "message": "user password has been successfully changed",
                    }
                },
            },
        },
        201: {"description": "N/A"},
    },
    methods=["POST"],
    status_code=200,
)
