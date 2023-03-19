from typing import Optional
from pydantic import BaseModel


class CreateProperty(BaseModel):
    name: str
    action: str
    type: str
    address_id: int


class UpdateProperty(CreateProperty):
    name: Optional[str]
    action: Optional[str]
    type: Optional[str]
    address_id: Optional[int]
