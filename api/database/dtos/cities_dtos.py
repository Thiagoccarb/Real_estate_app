from typing import Optional
from pydantic import BaseModel


class CreateCity(BaseModel):
    name: str
    state: str


class UpdateCity(BaseModel):
    name: Optional[str]
    state: Optional[str]
