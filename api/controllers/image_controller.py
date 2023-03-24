from fastapi import Depends, Header

from services.image.batch_create_image_service import BatchAddImageService
from services.auth.auth import AuthService
from services.image.create_image_service import AddImageService
from schemas.image_schemas import BatchCreateImageRequest, BatchCreateImageResponse, CreateImageRequest, CreateImageResponse, Image


class ImageController:
    async def add(
        self,
        request: CreateImageRequest,
        add_city_service: AddImageService = Depends(AddImageService),
        auth_service: AuthService = Depends(AuthService),
        authorization=Header(None),
    ) -> CreateImageResponse:
        await auth_service.execute(authorization=authorization, decode=True)
        new_image: Image = await add_city_service.execute(request)
        return CreateImageResponse(result=new_image)
    
    async def batch_add(
        self,
        request: BatchCreateImageRequest,
        batch_add_city_service: BatchAddImageService = Depends(BatchAddImageService),
        auth_service: AuthService = Depends(AuthService),
        authorization=Header(None),
    ) -> BatchCreateImageResponse:
        await auth_service.execute(authorization=authorization, decode=True)
        data = await batch_add_city_service.execute(request)
        return BatchCreateImageResponse(**data.dict())
