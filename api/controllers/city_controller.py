from fastapi import Depends

from services.city.create_city_service import AddCityService
from schemas.city_schemas import CreateCityRequest, City, CreateCityResponse


class CityController:
    async def add(
        self,
        request: CreateCityRequest,
        add_city_service: AddCityService = Depends(AddCityService),
    ) -> CreateCityResponse:

        new_property: City = await add_city_service.execute(request)
        return CreateCityResponse(result=new_property)
