from typing import List, Any, Optional
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from schemas.base import BaseResponse
from database import mappings
from database.dtos.properties_dtos import CreateProperty

Property = sqlalchemy_to_pydantic(mappings.Property)


class CreatePropertyRequest(CreateProperty):
    pass

    class Config:
        schema_extra = {
            "example": {
                "name": "house 2",
            }
        }


class CreatePropertyResponse(BaseResponse):
    result: Property


class PropertyData(Property):
    id: Optional[int]
    image_urls: List[Any] = []

    class Config:
        orm_mode: True


class ListPropertyResponse(BaseResponse):
    result: List[PropertyData]
