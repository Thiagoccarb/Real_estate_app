from typing import Any, Optional
from pydantic import BaseModel


class BaseResponse(BaseModel):
    success: Optional[bool] = True
    error: Optional[Any] = None
    result: Optional[Any]
    
class BasePaginatedResponse(BaseResponse):
    next_page: Optional[str]
    previous_page: Optional[str]

class Error(BaseModel):
    type: str
    description: str


class Token(BaseModel):
    token: str


class MissingFieldErrorSchema(BaseModel):
    success: bool
    error: Optional[Error]

    class Config:
        schema_extra = {
            "example": {
                "success": False,
                "error": {
                    "type": "missing_field",
                    "description": f"missing field `field_name`",
                },
            }
        }


class ListPropertyQueries(BaseModel):
    id: Optional[int]
    type: Optional[str]
    action: Optional[str]
    sort: Optional[str]
    offset: Optional[int]
    limit: Optional[int]
