from typing import List
import datetime
from pydantic import BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from schemas.base import BaseResponse
from database import mappings

Image = sqlalchemy_to_pydantic(mappings.Image)


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
                "list_str_binary": ["/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAMCAgMCAgMDAwMEAwMEBQgFBQQEBQoHBwYIDAoMDAsKCwsNDhIQDQ4RDgsLEBYQERMUFRUVDA8XGBYUGBIUFRT/2wBDAQMEBAUEBQkFBQkUDQsNFBQUFBs..."],
                "property_id": 1,
            }
        }


class CreatedImageData(BaseModel):
    id: int
    created_at: datetime.datetime

class BatchCreatedImageData(BaseModel):
    ids: List[int]
    created_at: datetime.datetime

class CreateImageResponse(BaseResponse):
    result: CreatedImageData

class BatchCreateImageResponse(BaseResponse):
    result: BatchCreatedImageData