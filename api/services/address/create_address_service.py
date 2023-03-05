from fastapi import Depends
import re

from schemas.address_schema import CreateAddressRequest, Address
from database.repositories.city_repository import CitiesRepository
from database.dtos.images_dtos import CreateImage
from schemas.image_schemas import CreatedImageData
from database.repositories.address_repository import AddressesRepository
from errors.status_error import StatusError


class AddAddressService:
    def __init__(
        self,
        address_repository: AddressesRepository = Depends(AddressesRepository),
        city_repository: CitiesRepository = Depends(CitiesRepository),
    ):
        self.address_repository = address_repository
        self.city_repository = city_repository

    async def execute(self, request: CreateAddressRequest) -> Address:
        existing_city = await self.city_repository.find_by_id(id=request.city_id)
        pattern = r"^\d{5}(-\d{3})?$"
        match = re.match(pattern, request.cep)
        if not match:
            raise StatusError(
                "cep must be in the format XXXXX-XXX or XXXXXXXX",
                422,
                "unprocessable_entity",
            )

        if not existing_city:
            raise StatusError(
                f"city with `id` {request.city_id} not found", 404, "not_found"
            )

        new_address = await self.address_repository.add(request)
        return new_address
