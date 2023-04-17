from fastapi.routing import APIRouter

from schemas.city_schemas import CreateCityResponse
from controllers.city_controller import CityController


city_controller = CityController()


city_router = APIRouter(prefix="/cities", tags=["cities"])

# city_router.add_api_route(
#     "",
#     city_controller.add,
#     methods=["POST"],
#     status_code=201,
#     response_model=CreateCityResponse,
# )
