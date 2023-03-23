from pydantic import BaseModel
from typing import List, Any, Optional
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
import datetime

from schemas.base import BasePaginatedResponse, BaseResponse
from database import mappings
from database.dtos.addresses_dtos import CreateAddressWithoutId, UpdateAddress
from database.dtos.cities_dtos import CreateCity, UpdateCity

Property = sqlalchemy_to_pydantic(mappings.Property)


class CreatePropertyRequest(BaseModel):
    name: str
    action: str
    type: str
    address: CreateAddressWithoutId
    city: CreateCity
    pass

    class Config:
        schema_extra = {
            "example": {
                "name": "property",
                "action": "rent",
                "type": "apartment",
                "address": {"street_name": "test", "cep": "11111-111"},
                "city": {"name": "São Paulo", "state": "SP"},
            }
        }


class UpdatePropertyRequest(BaseModel):
    updated_at: Optional[datetime.datetime] = datetime.datetime.now()
    name: Optional[str]
    action: Optional[str]
    type: Optional[str]
    address: Optional[UpdateAddress]
    city: Optional[UpdateCity]

    class Config:
        schema_extra = {
            "example": {
                "name": "property",
                "action": "rent",
                "type": "apartment",
                "address": {"street_name": "test", "cep": "11111-111"},
                "city": {"name": "São Paulo", "state": "SP"},
            }
        }


class CreatePropertyResponse(BaseResponse):
    result: Property


class UpdatedProperty(UpdatePropertyRequest):
    pass


class RemovePropertyResponse(BaseResponse):
    pass


class UpdatePropertyResponse(BaseResponse):
    result: UpdatedProperty


class PropertyData(Property):
    id: Optional[int]
    image_urls: List[Any] = []
    address: CreateAddressWithoutId
    city: CreateCity

    class Config:
        orm_mode: True


class ListPropertyResponse(BasePaginatedResponse):
    result: List[PropertyData]
