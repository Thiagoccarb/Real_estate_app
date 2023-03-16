from typing import List
from fastapi import Depends

from schemas.base import ListPropertyQueries
from schemas.property_schemas import Property
from database.repositories.property_repository import PropertiesRepository


class ListPropertyService:
    def __init__(
        self,
        property_repository: PropertiesRepository = Depends(PropertiesRepository),
    ):
        self.property_repository = property_repository

    async def execute(self, queries: ListPropertyQueries) -> List[Property]:
        properties = await self.property_repository.find_all(queries)
        return properties
