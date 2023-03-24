from fastapi import Depends
import base64

from database.repositories.property_repository import PropertiesRepository
from database.dtos.images_dtos import CreateImage
from utils.backblaze_b2 import B2skd
from schemas.image_schemas import BatchCreateImageRequest, BatchCreateImageResponse, BatchCreatedImageData, CreatedImageData
from database.repositories.image_repository import ImagesRepository
from errors.status_error import StatusError


class BatchAddImageService:
    def __init__(
        self,
        image_repository: ImagesRepository = Depends(ImagesRepository),
        property_repository: PropertiesRepository = Depends(PropertiesRepository),
        b2: B2skd = Depends(B2skd),
    ):
        self.image_repository = image_repository
        self.property_repository = property_repository
        self.b2 = b2

    async def execute(self, request:BatchCreateImageRequest) -> CreatedImageData:
        existing_property = await self.property_repository.find_by_id(
            id=request.property_id
        )
        if not existing_property:
            raise StatusError(
                f"property with `id` {request.property_id} not found", 404, "not_found"
            )
        try:
            ids = []
            for binary_str in request.list_str_binary:
                base64_decoded_data = base64.b64decode(binary_str)
                self.b2.upload_binary_to_blackblaze(base64_decoded_data)
                url: str = self.b2.get_download_url()
                new_image_data= await self.image_repository.add(
                    data=CreateImage(
                        **{
                            "url": url,
                            "property_id": request.property_id,
                        }
                    )
                )
                ids.append(new_image_data.id)
            return BatchCreateImageResponse(success=True, result=BatchCreatedImageData(ids=ids, created_at=new_image_data.created_at),)
        except Exception as e:
            print(e)
            raise StatusError(f"invalid binary string", 422, "unprocessable_entity")
