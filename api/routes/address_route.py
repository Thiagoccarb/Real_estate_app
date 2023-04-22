from fastapi.routing import APIRouter

from schemas.address_schema import CreateAddressResponse
from controllers.address_controller import AddressController


address_controller = AddressController()


address_router = APIRouter(prefix="/addresses", tags=["addresses"])

# address_router.add_api_route(
#     "",
#     address_controller.add,
#     methods=["POST"],
#     status_code=201,
#     response_model=CreateAddressResponse,
# )
