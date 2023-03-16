from typing import List
from fastapi import Depends

from schemas.property_schemas import CreatePropertyRequest, Property
from database.repositories.address_repository import AddressesRepository
from database.repositories.property_repository import PropertiesRepository
from errors.status_error import StatusError


class ListPropertyService:
    def __init__(
        self,
        property_repository: PropertiesRepository = Depends(PropertiesRepository),
    ):
        self.property_repository = property_repository

    async def execute(self) -> List[Property]:
        properties = await self.property_repository.find_all()
        return properties
