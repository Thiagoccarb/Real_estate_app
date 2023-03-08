from typing import Any, Optional
from pydantic import BaseModel


class BaseResponse(BaseModel):
    success: Optional[bool] = True
    error: Optional[Any] = None
    result: Optional[Any]


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
