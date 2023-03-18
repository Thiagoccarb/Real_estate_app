from fastapi import Depends

from schemas.property_schemas import Property
from database.repositories.address_repository import AddressesRepository
from database.repositories.property_repository import PropertiesRepository
from errors.status_error import StatusError


class RemovePropertyService:
    def __init__(
        self,
        property_repository: PropertiesRepository = Depends(PropertiesRepository),
        address_repository: AddressesRepository = Depends(AddressesRepository),
    ):
        self.property_repository = property_repository
        self.address_repository = address_repository

    async def execute(self, id: int) -> None:
        existing_property: Property = await self.property_repository.find_by_id(id)
        if not existing_property:
            raise StatusError('Property with `id` {id} not found', 404, 'not_found', id = id)
        await self.address_repository.remove_by_id(existing_property.address_id)
        await self.property_repository.remove_by_id(id)
        