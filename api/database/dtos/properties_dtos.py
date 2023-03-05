from pydantic import BaseModel
from typing import Optional, Union, List


class CreateProperty(BaseModel):
    name: str
