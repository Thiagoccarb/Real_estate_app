from typing import Optional
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from pydantic import Field

from schemas.base import BaseResponse
from database import mappings
from database.dtos.users_dto import CreateUser

User = sqlalchemy_to_pydantic(mappings.User)


class PublicUser(User):
    password: Optional[str] = Field(exclude=True)


class CreateUserRequest(CreateUser):
    pass

    class Config:
        schema_extra = {
            "example": {
                "email": "user@email.com",
                "username": "username",
                "password": "sgfPDPNifa",
            }
        }


class CreateUserResponse(BaseResponse):
    result: PublicUser
