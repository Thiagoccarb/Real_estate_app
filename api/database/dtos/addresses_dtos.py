from typing import Optional
from pydantic import BaseModel


class CreateAddress(BaseModel):
    street_name: str
    city_id: int
    number: Optional[int]
    cep: str
