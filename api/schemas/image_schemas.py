from typing import List, Optional
import datetime
from pydantic import BaseModel, Field
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from schemas.base import BaseResponse
from database import mappings

Image = sqlalchemy_to_pydantic(mappings.Image)

class ImageWithoutIdAndPropertyId(Image):
    property_id: Optional[int] = Field(exclude = True)
    id: Optional[int] = Field(exclude = True)

class CreateImageRequest(BaseModel):
    str_binary: str
    property_id: int

    class Config:
        schema_extra = {
            "example": {
                "str_binary": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAMCAgMCAgMDAwMEAwMEBQgFBQQEBQoHBwYIDAoMDAsKCwsNDhIQDQ4RDgsLEBYQERMUFRUVDA8XGBYUGBIUFRT/2wBDAQMEBAUEBQkFBQkUDQsNFBQUFBs...",
                "property_id": 1,
            }
        }


class BatchCreateImageRequest(BaseModel):
    list_str_binary: List[str]
    property_id: int

    class Config:
        schema_extra = {
            "example": {
                "list_str_binary": [
                    "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAMCAgMCAgMDAwMEAwMEBQgFBQQEBQoHBwYIDAoMDAsKCwsNDhIQDQ4RDgsLEBYQERMUFRUVDA8XGBYUGBIUFRT/2wBDAQMEBAUEBQkFBQkUDQsNFBQUFBs...",
                    "/9j/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCg..."
                ],
                "property_id": 1,
            }
        }


class CreatedImageData(BaseModel):
    id: int
    created_at: datetime.datetime


class BatchCreateImageResponse(BaseResponse):
    result: List[ImageWithoutIdAndPropertyId]
