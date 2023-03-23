from typing import Optional
from pydantic import BaseModel


class CreateAddress(BaseModel):
    street_name: str
    number: Optional[int]
    cep: str
    city_id: int


class UpdateAddress(BaseModel):
    street_name: Optional[str]
    number: Optional[int]
    cep: Optional[str]
    city_id: Optional[int]


class CreateAddressWithoutId(BaseModel):
    street_name: str
    number: Optional[int]
    cep: str
