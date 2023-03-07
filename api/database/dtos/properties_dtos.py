from pydantic import BaseModel


class CreateProperty(BaseModel):
    name: str
    action: str
    type: str
    address_id: int
