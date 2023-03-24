from fastapi.routing import APIRouter

from schemas.image_schemas import BatchCreateImageResponse, CreateImageResponse
from controllers.image_controller import ImageController

image_controller = ImageController()


image_router = APIRouter(prefix="/images", tags=["images"])

image_router.add_api_route(
    "",
    image_controller.add,
    methods=["POST"],
    status_code=201,
    response_model=CreateImageResponse,
)

image_router.add_api_route(
    "/batch",
    image_controller.batch_add,
    methods=["POST"],
    status_code=201,
    response_model=BatchCreateImageResponse,
)
