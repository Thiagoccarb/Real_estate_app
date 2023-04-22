from typing import Optional
from pydantic import BaseModel, Field

from schemas.address_schema import Address
from database.dtos.cities_dtos import CreateCity


class CreateAddress(BaseModel):
    street_name: str
    number: Optional[int]
    cep: str
    city_id: int


class AddressWithCity(Address):
    city: CreateCity


class UpdateAddress(BaseModel):
    street_name: Optional[str]
    number: Optional[int]
    cep: Optional[str]
    city_id: Optional[int] = Field(exclude=True)


class AddressWithoutId(BaseModel):
    street_name: str
    number: Optional[int]
    cep: str
