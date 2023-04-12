from pydantic import BaseModel, Field
from typing import List, Any, Optional
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
import datetime

from schemas.base import BasePaginatedResponse, BaseResponse
from database import mappings
from database.dtos.addresses_dtos import AddressWithoutId, UpdateAddress
from database.dtos.cities_dtos import CreateCity, UpdateCity

Property = sqlalchemy_to_pydantic(mappings.Property)


class CreatePropertyRequest(BaseModel):
    name: str
    action: str
    type: str
    description: str
    bathrooms: int
    bedrooms: int
    price: float
    address: AddressWithoutId
    city: CreateCity

    class Config:
        schema_extra = {
            "example": {
                "name": "property",
                "action": "rent",
                "type": "apartment",
                "price": "1000",
                "address": {"street_name": "test", "cep": "11111-111"},
                "city": {"name": "São Paulo", "state": "SP"},
                "bedrooms": 3,
                "bathrooms": 4,
                "description": "beautiful house"
            }
        }

class CreatedProperty(CreatePropertyRequest):
    id: int

class UpdatePropertyRequest(BaseModel):
    updated_at: Optional[datetime.datetime] = datetime.datetime.now()
    name: Optional[str]
    action: Optional[str]
    type: Optional[str]
    description: Optional[str]
    bathrooms: Optional[int]
    bedrooms: Optional[int]
    price: Optional[float]
    address: Optional[UpdateAddress]
    city: Optional[UpdateCity]
    description: str
    bathrooms: int
    bedrooms: int
    
    class Config:
        schema_extra = {
            "example": {
                "name": "property",
                "action": "rent",
                "price": 2000,
                "type": "apartment",
                "address": {"street_name": "test", "cep": "11111-111"},
                "city": {"name": "São Paulo", "state": "SP"},
                "bedrooms": 3,
                "bathrooms": 4,
                "description": "beautiful house"
            }
        }


class CreatePropertyResponse(BaseResponse):
    result: CreatedProperty


class UpdatedProperty(UpdatePropertyRequest):
    pass


class RemovePropertyResponse(BaseResponse):
    pass


class UpdatePropertyResponse(BaseResponse):
    result: UpdatedProperty


class PropertyData(Property):
    id: Optional[int]
    description: Optional[str]
    bedrooms: Optional[int]
    bathrooms: Optional[int]
    image_urls: List[Any] = []
    address: AddressWithoutId
    city: CreateCity
    address_id: Optional[int] = Field(exclude = True)
    class Config:
        orm_mode: True


class ListPropertyResponse(BasePaginatedResponse):
    result: List[PropertyData]
