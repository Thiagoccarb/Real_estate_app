from fastapi import Depends

from schemas.property_schemas import CreatePropertyRequest, Property
from database.repositories.property_repository import PropertiesRepository


class AddPropertyService:
    def __init__(
        self,
        property_repository: PropertiesRepository = Depends(PropertiesRepository),
    ):
        self.property_repository = property_repository

    async def execute(self, request: CreatePropertyRequest) -> Property:
        new_property = await self.property_repository.add(data=request)
        return new_property
