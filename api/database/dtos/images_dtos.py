from pydantic import BaseModel


class CreateImage(BaseModel):
    binary: bytes
    property_id: int
