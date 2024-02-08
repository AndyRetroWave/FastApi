from typing import List

from pydantic import BaseConfig, BaseModel


class SRoom(BaseModel):
    id: int
    name: str
    description: str
    price: int
    services: List[str]  # Используйте List[str] вместо JSON

    class Config(BaseConfig):
        arbitrary_types_allowed = True