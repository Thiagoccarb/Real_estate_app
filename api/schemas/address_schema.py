from typing import Optional
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from errors.status_error import StatusError
from schemas.base import BaseResponse
from database.dtos.addresses_dtos import CreateAddress
from database import mappings

Address = sqlalchemy_to_pydantic(mappings.Address)


class CreateAddressRequest(CreateAddress):
    number: Optional[int]
    cep: str

    class Config:
        schema_extra = {
            "example": {"street_name": "street_name", "city_id": 1, "cep": "11111-111"}
        }


class CreateAddressResponse(BaseResponse):
    result: Address
