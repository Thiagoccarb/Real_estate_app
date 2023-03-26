from pydantic import BaseModel


class CreateImage(BaseModel):
    url: str
    property_id: int
    audio_hash: str
    position: int
