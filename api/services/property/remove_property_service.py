from fastapi import Depends

from schemas.image_schemas import Image
from schemas.property_schemas import Property
from database.repositories.address_repository import AddressesRepository
from database.repositories.image_repository import ImagesRepository
from database.repositories.property_repository import PropertiesRepository
from errors.status_error import StatusError
from utils.backblaze_b2 import B2skd


class RemovePropertyService:
    def __init__(
        self,
        property_repository: PropertiesRepository = Depends(PropertiesRepository),
        address_repository: AddressesRepository = Depends(AddressesRepository),
        image_repository: ImagesRepository = Depends(ImagesRepository),
        b2: B2skd = Depends(B2skd),
    ):
        self.property_repository = property_repository
        self.address_repository = address_repository
        self.image_repository = image_repository
        self.b2 = b2

    async def execute(self, id: int) -> None:
        existing_property: Property = await self.property_repository.find_by_id(id)
        if not existing_property:
            raise StatusError(
                "Property with `id` {id} not found", 404, "not_found", id=id
            )
        list_image_data: Image = await self.image_repository.find_all_by_property_id(id)
        if list_image_data:
            list_audio_hashes = [image.audio_hash for image in list_image_data]
            for audio_hash in list_audio_hashes:
                self.b2.delete_file_by_audio_hash(audio_hash)
        await self.property_repository.remove_by_id(id)
