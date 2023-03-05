from pydantic import BaseModel


class CreateCity(BaseModel):
    name: str
    state: str
