from typing import Optional
from pydantic import BaseModel


class CreateUser(BaseModel):
    email: str
    username: str
    password: str


class UpdateUser(BaseModel):
    email: Optional[str]
    username: Optional[str]
    password: Optional[str]
