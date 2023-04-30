from fastapi import Depends, Header

from services.image.batch_create_image_service import BatchAddImageService
from services.auth.auth import AuthService
from schemas.image_schemas import BatchCreateImageRequest, BatchCreateImageResponse


class ImageController:
    async def batch_add(
        self,
        request: BatchCreateImageRequest,
        batch_add_city_service: BatchAddImageService = Depends(BatchAddImageService),
        auth_service: AuthService = Depends(AuthService),
        authorization=Header(None),
    ) -> BatchCreateImageResponse:
        await auth_service.execute(authorization=authorization, decode=True)
        data = await batch_add_city_service.execute(request)
        return BatchCreateImageResponse(success=True, result=data)
