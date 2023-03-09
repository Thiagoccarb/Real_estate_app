from fastapi import Depends, Header

from services.auth.auth import AuthService
from services.city.create_city_service import AddCityService
from schemas.city_schemas import CreateCityRequest, City, CreateCityResponse


class CityController:
    async def add(
        self,
        request: CreateCityRequest,
        authorization: str = Header(None),
        add_city_service: AddCityService = Depends(AddCityService),
        auth: AuthService = Depends(AuthService),
    ) -> CreateCityResponse:
        auth.validate_token(authorization)
        new_property: City = await add_city_service.execute(request)
        return CreateCityResponse(result=new_property)
