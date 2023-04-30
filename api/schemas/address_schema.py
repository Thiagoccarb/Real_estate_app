from typing import Optional
from pydantic import BaseModel, Field
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from schemas.base import BaseResponse
from database.dtos.cities_dtos import CreateCity, UpdateCity
from database import mappings

Address = sqlalchemy_to_pydantic(mappings.Address)


class CreateAddressRequest(BaseModel):
    street_name: str
    number: Optional[int]
    cep: str
    city_data: CreateCity

    class Config:
        schema_extra = {
            "example": {"street_name": "street_name", "city_id": 1, "cep": "11111-111"}
        }


class UpdateAddressRequest(BaseModel):
    street_name: Optional[str]
    number: Optional[int]
    cep: Optional[str]
    city: Optional[UpdateCity]

    class Config:
        schema_extra = {
            "example": {"street_name": "street_name", "city_id": 1, "cep": "11111-111"}
        }


class AddressWithoutCityId(Address):
    city_id: Optional[int] = Field(exclude=True)


class CreateAddressResponse(BaseResponse):
    result: AddressWithoutCityId


class UpdateAddressResponse(UpdateAddressRequest):
    city_id: int
