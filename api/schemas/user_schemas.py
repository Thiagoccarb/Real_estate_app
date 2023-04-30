from typing import Optional
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from pydantic import BaseModel, Field

from schemas.base import BaseResponse
from database import mappings
from database.dtos.users_dto import CreateUser, UpdateUser

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


class UpdateUserRequest(UpdateUser):
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


class EmailRequest(BaseModel):
    email: str

    class Config:
        schema_extra = {
            "example": {
                "email": "user@email.com",
            }
        }


class PasswordResetRequest(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {"email": "user@email.com", "password": "***********"}
        }
