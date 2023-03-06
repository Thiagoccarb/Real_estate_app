from pydantic import BaseModel


class CreateImage(BaseModel):
    url: str
    property_id: int
