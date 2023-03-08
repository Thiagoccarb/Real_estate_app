from pydantic import BaseModel

from schemas.base import BaseResponse, Token


class UserCredentialsRequest(BaseModel):
    email: str
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "enail": "user@email.com",
                "username": "username",
                "password": "password",
            }
        }


class UserCredentialsResponse(BaseResponse):
    result: Token
