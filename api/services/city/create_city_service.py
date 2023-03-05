from fastapi import Depends

from schemas.city_schemas import CreateCityRequest, City
from database.repositories.city_repository import CitiesRepository


class AddCityService:
    def __init__(
        self,
        city_repository: CitiesRepository = Depends(CitiesRepository),
    ):
        self.city_repository = city_repository

    async def execute(self, request: CreateCityRequest) -> City:

        new_city = await self.city_repository.add(data=request)
        return new_city
