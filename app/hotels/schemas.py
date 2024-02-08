from typing import List

from pydantic import BaseConfig, BaseModel
from sqlalchemy import JSON


class SHotel(BaseModel):
    id: int
    name:str
    location:str
    services: List[str]
    rooms_quantity:int
    image_id:int

    class Config(BaseConfig):
        arbitrary_types_allowed = True