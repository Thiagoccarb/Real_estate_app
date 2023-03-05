from fastapi import Depends
import base64

from database.repositories.property_repository import PropertiesRepository
from database.dtos.images_dtos import CreateImage
from schemas.image_schemas import CreateImageRequest, CreatedImageData
from database.repositories.image_repository import ImagesRepository
from errors.status_error import StatusError


class AddImageService:
    def __init__(
        self,
        image_repository: ImagesRepository = Depends(ImagesRepository),
        property_repository: PropertiesRepository = Depends(PropertiesRepository),
    ):
        self.image_repository = image_repository
        self.property_repository = property_repository

    async def execute(self, request: CreateImageRequest) -> CreatedImageData:
        existing_property = await self.property_repository.find_by_id(
            id=request.property_id
        )
        if not existing_property:
            raise StatusError(
                f"property with `id` {request.property_id} not found", 404, "not_found"
            )
        try:
            base64_decoded_data = base64.b64decode(request.str_binary)
            new_image_id = await self.image_repository.add(
                data=CreateImage(
                    **{
                        "binary": base64_decoded_data,
                        "property_id": request.property_id,
                    }
                )
            )
            return new_image_id
        except Exception:
            raise StatusError(f"invalid binary string", 422, "unprocessable_entity")
