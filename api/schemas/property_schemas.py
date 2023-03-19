from typing import List, Any, Optional
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
import datetime

from schemas.base import BasePaginatedResponse, BaseResponse
from database import mappings
from database.dtos.properties_dtos import CreateProperty, UpdateProperty

Property = sqlalchemy_to_pydantic(mappings.Property)


class CreatePropertyRequest(CreateProperty):
    pass

    class Config:
        schema_extra = {
            "example": {
                "name": "house 2",
                "action": "rent",
                "type": "apartment",
                "address_id": 10,
            }
        }


class UpdatePropertyRequest(UpdateProperty):
    updated_at: Optional[datetime.datetime] = datetime.datetime.now()

    class Config:
        schema_extra = {
            "example": {
                "name": "house 2",
                "action": "rent",
                "type": "apartment",
            }
        }


class CreatePropertyResponse(BaseResponse):
    result: Property


class UpdatePropertyResponse(CreatePropertyResponse):
    pass


class RemovePropertyResponse(BaseResponse):
    pass


class PropertyData(Property):
    id: Optional[int]
    image_urls: List[Any] = []

    class Config:
        orm_mode: True


class ListPropertyResponse(BasePaginatedResponse):
    result: List[PropertyData]
