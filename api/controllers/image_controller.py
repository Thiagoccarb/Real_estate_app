from fastapi import Depends
import io
from services.image.create_image_service import AddImageService
from schemas.image_schemas import CreateImageRequest, CreateImageResponse, Image


class ImageController:
    async def add(
        self,
        request: CreateImageRequest,
        add_city_service: AddImageService = Depends(AddImageService),
    ) -> CreateImageResponse:
        new_image: Image = await add_city_service.execute(request)
        return CreateImageResponse(result=new_image)
