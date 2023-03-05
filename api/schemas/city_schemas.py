from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from schemas.base import BaseResponse
from database import mappings
from database.dtos.cities_dtos import CreateCity

City = sqlalchemy_to_pydantic(mappings.City)


class CreateCityRequest(CreateCity):
    pass

    class Config:
        schema_extra = {"example": {"name": "city 1", "state": "state"}}


class CreateCityResponse(BaseResponse):
    result: City
