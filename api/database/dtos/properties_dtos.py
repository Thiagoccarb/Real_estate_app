from typing import Optional
from pydantic import BaseModel


class CreateProperty(BaseModel):
    name: str
    action: str
    type: str
    price: float
    address_id: int
    description: str
    bathrooms: int
    bedrooms: int


class UpdateProperty(CreateProperty):
    name: Optional[str]
    action: Optional[str]
    type: Optional[str]
    address_id: Optional[int]
