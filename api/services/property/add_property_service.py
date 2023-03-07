from fastapi import Depends

from schemas.property_schemas import CreatePropertyRequest, Property
from database.repositories.address_repository import AddressesRepository
from database.repositories.property_repository import PropertiesRepository
from errors.status_error import StatusError


class AddPropertyService:
    def __init__(
        self,
        property_repository: PropertiesRepository = Depends(PropertiesRepository),
        address_repository: AddressesRepository = Depends(AddressesRepository),
    ):
        self.property_repository = property_repository
        self.address_repository = address_repository

    async def execute(self, request: CreatePropertyRequest) -> Property:
        if request.type not in ("apartment", "house"):
            raise StatusError(
                'field `type` must be "apartment" or "house"',
                422,
                "unprocessable_entity",
            )

        if request.action not in ("rent", "sale"):
            raise StatusError(
                'field `action` must be "rent" or "sale"', 422, "unprocessable_entity"
            )

        existing_address = await self.address_repository.find_by_id(request.address_id)
        if not existing_address:
            raise StatusError(
                "address with `address_id not found` {id}",
                404,
                "unprocessable_entity",
                id=request.address_id,
            )

        new_property = await self.property_repository.add(data=request)
        return new_property
