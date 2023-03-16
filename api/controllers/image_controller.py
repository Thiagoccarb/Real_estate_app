from fastapi import Depends

from services.auth.auth import AuthService
from services.image.create_image_service import AddImageService
from schemas.image_schemas import CreateImageRequest, CreateImageResponse, Image


class ImageController:
    async def add(
        self,
        request: CreateImageRequest,
        add_city_service: AddImageService = Depends(AddImageService),
        auth_service: AuthService = Depends(AuthService),
    ) -> CreateImageResponse:
        await auth_service.execute(decode=True)
        new_image: Image = await add_city_service.execute(request)
        return CreateImageResponse(result=new_image)
