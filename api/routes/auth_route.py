from fastapi.routing import APIRouter

from schemas.auth_schemas import UserCredentialsResponse
from controllers.auth_controller import AuthController

auth_controller = AuthController()


auth_router = APIRouter(prefix="/login", tags=["login"])

auth_router.add_api_route(
    "",
    auth_controller.login,
    methods=["POST"],
    status_code=200,
    response_model=UserCredentialsResponse,
)
