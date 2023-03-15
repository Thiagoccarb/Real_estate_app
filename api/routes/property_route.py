from fastapi.routing import APIRouter

from schemas.property_schemas import CreatePropertyResponse, ListPropertyResponse
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
    "",
    property_controller.find_all,
    methods=["GET"],
    status_code=200,
    response_model=ListPropertyResponse,
)
